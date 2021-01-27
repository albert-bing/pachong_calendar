# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

import sys
sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
# 导入selenium的驱动接口
from selenium import webdriver
# 导入键盘操作的keys包
from selenium.webdriver.common.action_chains import ActionChains
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

def get_data_resource_province(driver):
    driver.get("https://wp.m.163.com/163/page/news/virus_report/index.html?_nw_=1&_anw_=1")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    source_data = soup.find_all("div", attrs={"class": "overseas_list_row"})

    total_list=[]

    for i in range(1,len(source_data),1):
        every_list = []
        # 国家名称
        area_name = source_data[i].find_all("div",attrs={"class","overseas_list_name"})[0].text
        # 新增
        new_add = source_data[i].find_all("div",attrs={"class","overseas_list_today_confirm"})[0].text
        # 累计确诊
        cumulative_diagnosis = source_data[i].find_all("div",attrs={"class","overseas_list_confirm"})[0].text
        # 累计治愈
        cumulative_cure = source_data[i].find_all("div",attrs={"class","overseas_list_heal"})[0].text
        # 累计死亡
        cumulative_deaths = source_data[i].find_all("div",attrs={"class","overseas_list_dead"})[0].text
        # 现有确诊
        existing_diagnosis = int(cumulative_diagnosis) - int(cumulative_cure) - int(cumulative_deaths)

        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        every_list.append(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        every_list.append(area_name)
        every_list.append(new_add)
        every_list.append(existing_diagnosis)
        every_list.append(cumulative_diagnosis)
        every_list.append(cumulative_cure)
        every_list.append(cumulative_deaths)
        every_list.append(create_time)
        every_list.append(update_time)

        total_list.append(every_list)

    MysqlUtil.insert_foreign_data(total_list)
    print(total_list)



if __name__ == '__main__':
    driver = create_driver()
    pro_list = get_data_resource_province(driver)
