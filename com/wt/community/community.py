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

from urllib.parse import quote

from com.wt.common import MysqlUtil

import requests
from bs4 import BeautifulSoup
import urllib3
import time

# 忽略https的安全警告
# urllib3.disable_warnings()




# 创建driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=config._CHROME_DRIVER_WIN, options=chrome_options)
    return driver


def get_source_data(driver):
    driver.get("https://ncov.html5.qq.com/community")
    time.sleep(3)

    # print("line:108 一个城市的数据", BeautifulSoup(driver.page_source, "html.parser").text)
    city_file = BeautifulSoup(driver.page_source, "html.parser")

    # 获取日期
    spans = city_file.find_all(name='div', attrs={"class": "banner-data-from"})
    date_today = spans[0].select("span")[1].text.split("更")[0].strip()

    print("日期：", date_today)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    tabs = soup.find_all(name="div", attrs={"class": "area-sele-item"})

    # 顶部的导航按钮  省 0  市  1
    tabs_btn = driver.find_elements_by_class_name("area-sele-item")

    # 点击省份的下拉菜单
    tabs_btn[0].click()
    tab1_file = BeautifulSoup(driver.page_source, "html.parser")
    # 获取所有的省份
    pros = tab1_file.find_all(name="div", attrs={"class": "item"})

    # 将省份放入列表中
    pros_list = []
    for num in range(0, len(pros), 1):
        pros_list.append(pros[num].text)
    # print("line:71 ===  省份", pros_list)
    # 进行Urlcode编码的转码  %E%T%R 类似这样的
    scope = quote("全部")
    # 将省的下拉菜单收起
    tabs_btn[0].click()

    # 通过循环实现所有省份的数据获取
    for nn in range(0, len(pros_list), 1):
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

        # print("line:64 ===  城市", cities_list)

        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/84.0.4147.89 Mobile Safari/537.36', 'Referer':
                       'https://ncov.html5.qq.com/community'}
        for mm in range(0, len(cities_list), 1):
            pro_text = quote(pros_list[nn])
            city_text = quote(cities_list[mm])
            # 拼接链接
            url = f"https://ncov.html5.qq.com/api/getNewestCommunityNew?&province={pro_text}&city={city_text}&district={scope}"
            # 加入一个headers，因为持续的外部请求，会导致请求失败的
            city_source_file = requests.get(url=url, headers=headers)
            dick_data = json.loads(city_source_file.text)
            # print(dick_data["data"][0]["province"])
            # print(dick_data)
            one_city = analysis_data(dick_data, date_today)
            # 判断是否为空，如果城市数据为空，那么就只存城市名称等信息
            if not one_city:
                one_city = [date_today, pros_list[nn], cities_list[mm], "", "", "", "", "", "", "", "", "", "",
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),"Point(0,0)"]
            else:
                MysqlUtil.insert_community_data(one_city)
                # pass
            print(one_city)
        time.sleep(1)

    driver.quit()


def analysis_data(dick_data, date_today):
    d_data = dick_data["data"]
    one_city_data = []
    # 将一个城市的数据整理好
    for d in range(0, len(d_data), 1):
        one_data = [date_today, d_data[d]["province"], d_data[d]["city"], d_data[d]["district"]]
        try:
            one_data.append(d_data[d]["street"])
        except Exception:
            one_data.append("")

        try:
            one_data.append(d_data[d]["middle_address"])
        except Exception:
            one_data.append("")

        try:
            one_data.append(d_data[d]["community"])
        except Exception:
            one_data.append("")

        try:
            one_data.append(d_data[d]["show_address"])
        except Exception:
            one_data.append("")

        one_data.append(d_data[d]["full_address"])
        one_data.append(d_data[d]["lng"])
        one_data.append(d_data[d]["lat"])
        one_data.append(d_data[d]["cnt_sum_certain"])
        one_data.append(d_data[d]["release_date"])

        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        one_data.append(create_time)
        one_data.append(update_time)

        one_data.append(f'Point({d_data[d]["lng"]} {d_data[d]["lat"]})')

        one_city_data.append(one_data)

        print(one_data)
    return one_city_data
    # print(one_city_data)


if __name__ == '__main__':
    driver = create_driver()
    get_source_data(driver)


