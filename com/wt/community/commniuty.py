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

    soup = BeautifulSoup(driver.page_source,"html.parser")

    tabs = soup.find_all(name="div",attrs={"class":"area-sele-item"})

    tabs_btn = driver.find_elements_by_class_name("area-sele-item")

    # 点击省份的下拉菜单
    tabs_btn[0].click()
    tab1_file = BeautifulSoup(driver.page_source,"html.parser")
    # 获取所有的省份
    items = tab1_file.find_all(name="div",attrs={"class":"item"})
    print(items)

    # 名称
    # city_name = soup.find_all(name="div",attrs={"class":"info"})
    # print(city_name)
    # 获取最新
    # new_info = soup.find_all(name="div",attrs={"class":"wrap"})
    # print(new_info)
    # 获取其他地区的
    # items_list = soup.find_all(name="div", attrs={"class": "train-lst"})
    # print(items_list)
    driver.quit


if __name__ == '__main__':
    driver = create_driver()
    get_data_resource(driver)
