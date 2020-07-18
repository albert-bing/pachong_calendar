# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# 导入selenium的驱动接口
from selenium import webdriver
# 导入键盘操作的keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.chrome.options import Options

from com.wt.config import config

import json

from com.wt.common import MysqlUtil

import requests
from bs4 import BeautifulSoup
import urllib3
import time

# 忽略https的安全警告
urllib3.disable_warnings()


# 创建driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=config._CHROME_DRIVER_WIN, options=chrome_options)
    return driver


# 获取网页源码
def get_data_resource(driver):
    driver.get("https://ncov.html5.qq.com/community")
    time.sleep(3)
    # driver.find_elements_by_class_name("area-sele-wrapper")[0].click()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    tabs = soup.find_all(name="div", attrs={"class": "area-sele-item"})

    # 顶部的导航按钮  省 0  市  1
    tabs_btn = driver.find_elements_by_class_name("area-sele-item")

    # 实现思路：
    '''
        1.点击省级的下拉菜单，选一个省，并且获取所有的省份，形成一个列表
        2.点击市的下拉菜单，获取选中的省的所有的市，并且点选第一个市，
        然后获取数据，插入（一个市的数据批量插入一次）
    '''

    # 点击省份的下拉菜单
    tabs_btn[0].click()
    tab1_file = BeautifulSoup(driver.page_source, "html.parser")
    # 获取所有的省份
    pros = tab1_file.find_all(name="div", attrs={"class": "item"})

    # 将省份放入列表中
    pros_list = []
    for num in range(0, len(pros), 1):
        pros_list.append(pros[num].text)
    print("line:71 ===  省份", pros_list)

    # 将省的下拉菜单收起
    tabs_btn[0].click()

    # 通过循环实现所有省份的数据获取
    for nn in range(0, len(pros), 1):
        # 再次点开省级下拉菜单
        tabs_btn[0].click()
        # 获取所有省份的点击事件---列表
        pros_tabs = driver.find_elements_by_class_name("item")
        # 点击某个省份  点击完之后会下拉菜单自动收起
        pros_tabs[nn].click()
        # 延迟两秒，否则获取不到界面内容
        time.sleep(1)
        # 点击市的名单获取该省的所有的市
        tabs_btn[1].click()
        # 获取该省的所有的市 -- 列表
        cities = driver.find_elements_by_class_name("item")
        # 将一个省城市放入列表中
        cities_list = []
        for num in range(0, len(cities), 1):
            cities_list.append(cities[num].text)
        print("line:64 ===  城市", cities_list)
        # 收起城市下拉菜单
        tabs_btn[1].click()
        # 循环点击每一个市
        for mm in range(0, len(cities_list), 1):
            # 点开下拉菜单
            tabs_btn[1].click()
            # 获取该省的所有的市点击事件
            cities_tabs = driver.find_elements_by_class_name("item")
            # 点击一个市
            cities_tabs[mm].click()
            # 延迟一秒
            time.sleep(1)

            # 如果有查看更多，则点开
            try:
                viewmore = driver.find_elements_by_class_name("more-box")
                for c in range(0,len(viewmore),1):
                    viewmore[c].click()
            except Exception:
                pass

            # print("line:108 一个城市的数据", BeautifulSoup(driver.page_source, "html.parser").text)
            city_file = BeautifulSoup(driver.page_source, "html.parser")
            analyze_data(driver, pros_list[nn], cities_list[mm],city_file)
    driver.quit()


# 解析数据
def analyze_data(driver, pro_name, city_name, source_data):
    # 一个城市的数据
    city_data = []
    # 获取日期
    spans = source_data.find_all(name='div', attrs={"class": "banner-data-from"})
    date_today = spans[0].select("span")[1].text.split("更")[0].strip()
    print("line:119 日期：", date_today)
    print("省份：", pro_name)
    print("城市：", city_name)

    # 名称 & 人数
    city_info = source_data.find_all(name="div", attrs={"class": "info"})
    city_people = city_info[0].select("span")[0].text
    print("line:129 城市人数：", city_people)
    # 获取 每一个区 & ’最新消息‘ 的单元的信息
    items_list = source_data.find_all(name="div", attrs={"class": "train-lst"})
    # 使用循环实现 遍历所有的区、县
    for a in range(0, len(items_list), 1):
        area_name = items_list[a].find_all(name="div", attrs={"class": "title"})[0].text
        print("line:134  地区名称：", area_name)
        total_place_number = ''
        total_person_number = ''
        if area_name != "最近更新":
            subs = items_list[a].find_all(name="div", attrs={"class": "sub"})
            spans = subs[0].select("span")
            # 涉事地区数量
            total_place_number = spans[0].text
            print("涉事地区数量：", total_place_number)
            # 涉事人员数量
            total_person_number = spans[1].text
            print("涉事人员数量：", total_person_number)

        # 社区信息
        tbody = items_list[a].select("tbody")

        # 获取小区信息列表
        trs = tbody[0].select("tr")

        # 通过循环获取小区的信息
        for b in range(0, len(trs), 1):
            one_piece_data = []
            tds = trs[b].select("td")
            stay_place = tds[0].select("p")[0].text
            nature_of_stay = tds[0].select("span")[0].text
            # 逗留日期
            release_date = ""
            # 逗留人数
            stay_people_number = ""
            date_or_people = tds[1].select("p")[0].text
            if "日" in date_or_people:
                release_date = date_or_people
            else:
                stay_people_number = date_or_people.split("人")[0]
            # 与我距离
            distance_from_me = tds[2].select("p")[0].text

            # 拼接一条数据  当前日期、省份名称、市名称、地区、城市确诊人数、逗留地点、逗留性质、逗留人数、发布日期、与我距离、共计涉事地区、攻击涉事人员
            one_piece_data = [date_today, pro_name, city_name, area_name, city_people, stay_place, nature_of_stay,
                              stay_people_number, release_date, distance_from_me, total_place_number,
                              total_person_number]
            print("line:178 小区：", one_piece_data)
            driver.quit()
            city_data.append(one_piece_data)
    driver.quit()


if __name__ == '__main__':
    driver = create_driver()
    get_data_resource(driver)
