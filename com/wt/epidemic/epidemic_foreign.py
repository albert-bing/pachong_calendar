# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code
import sys
sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
from com.wt.config import config
# 导入selenium的驱动接口
from selenium import webdriver
# 导入键盘操作的keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.chrome.options import Options


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


def get_source_data(driver):
    url = "https://voice.baidu.com/newpneumonia/get?target=trend&isCaseIn=1&stage=publish&callback=jsonp_1594965489703_79479"
    file = requests.get(url=url, verify=False)
    json_data = file.text.split("(")[1].split(")")[0]
    # 全国的省的数量
    dick_data = json.loads(json_data)

    # print(dick_data["data"][0])

    for num in range(0, len(dick_data["data"])):
        # 一个省的数据
        pro_data = dick_data["data"][num]

        # 一个省的计算数据
        insert_pro_data = []

        len1 = len(pro_data["trend"]["updateDate"])
        len2 = len(pro_data["trend"]["list"][0]["data"])
        len3 = len(pro_data["trend"]["list"][1]["data"])
        len4 = len(pro_data["trend"]["list"][2]["data"])
        len5 = len(pro_data["trend"]["list"][3]["data"])
        # 将日期、新增、治愈、累计确诊、死亡的数据长度排序，选最小
        list = [len1, len2, len3, len4, len5]
        d = list[0]
        for m in range(1, len(list), 1):
            if list[m] < d:
                d = list[m]

                # 将数据按省为单位插入
        for n in range(0, d, 1):
            # 添加 日期、国家名称、确诊(累计)人数、治愈人数、死亡人数、新增人数
            # 每日现有确诊人数
            every_day_data = int(pro_data["trend"]["list"][0]["data"][n]) - int(
                pro_data["trend"]["list"][1]["data"][n]) \
                             - int(pro_data["trend"]["list"][2]["data"][n])
            pro_day_data = ['2020.' + pro_data["trend"]["updateDate"][n], pro_data["name"],pro_data["trend"]["list"][0]["data"][n],
                            pro_data["trend"]["list"][1]["data"][n],pro_data["trend"]["list"][2]["data"][n],
                            pro_data["trend"]["list"][3]["data"][n],every_day_data]
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            pro_day_data.append(create_time)
            pro_day_data.append(update_time)
            # 添加进去
            insert_pro_data.append(pro_day_data)
            # 清空每天的数据
            pro_day_data = []


            # 插入一个省的所有数据
       # print(insert_pro_data)
        MysqlUtil.insert_foreign_data(insert_pro_data)


def get_every_data(driver):
    driver.get("https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3#tab4")
    # 点击打开省份的下拉列表
    # driver.find_element_by_class_name("Common_1-1-279_3lDRV2").click()
    driver.find_element_by_tag_name("span").click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    con_trs_data = soup.find_all("tr", attrs={"class": "VirusTable_1-1-287_2AH4U9"})


   # print(len(con_trs_data))


if __name__ == '__main__':
    driver = create_driver()
    get_source_data(driver)
