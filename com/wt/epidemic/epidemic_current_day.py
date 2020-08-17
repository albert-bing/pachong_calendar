# -*- encoding:utf-8 -*-

# @Team：Big Data Group
# @Time：2020/7/15 19:22
# @Author：albert·bing
# @File：epidemic_current_day.py
# @Software：PyCharm


#  start your code
# 导入selenium的驱动接口
from selenium import webdriver
# 导入键盘操作的keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.chrome.options import Options

from com.wt.config import config

from com.wt.common import MysqlUtil

import requests
from bs4 import BeautifulSoup
import urllib3
import time
# 忽略https的安全警告
urllib3.disable_warnings()

# 8.3  11：00
# 8.7  283
# 8.11 284

number = "284"

# 创建driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=config._CHROME_DRIVER_WIN, options=chrome_options)
    return driver


# 获取国内现有数据
def get_internal_data(driver):
    driver.get("https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3#tab0")
    # 获取网页源文件
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 拿到所有的累计数据
    ptab0 = soup.find_all(name='div', attrs={'class': 'VirusSummarySix_1-1-'+number+'_3haLBF VirusSummarySix_1-1-'+number+'_2ZJJBJ'})
    # 拿到比较昨日的数据
    ptab1 = soup.find_all(name='span', attrs={'class': 'VirusSummarySix_1-1-'+number+'_2ZJJBJ'})
    # 获取时间
    return analysis_data(ptab0, ptab1, soup)


def get_foreign_data(driver):
    driver.get("https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3#tab4")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ptab0 = soup.find_all(name='div', attrs={
        'class': 'VirusSummary_1-1-'+number+'_1lOkwH VirusSummary_1-1-'+number+'_2fhqEt VirusSummary_1-1-'+number+'_3Iv8cV'})
    ptab1 = soup.find_all(name='span', attrs={'class': 'VirusSummary_1-1-'+number+'_2fhqEt'})
    # 获取时间
    return analysis_data(ptab0, ptab1, soup)


def analysis_data(ptab0, ptab1, soup):
    # 获取当前时间
    cur_time_text = soup.find_all(name='div', attrs={'class': 'Virus_1-1-'+number+'_32Y_aO'})[0].select('span')[0].text.split(
        " ")
    ymd = cur_time_text[1]
    cur_time = cur_time_text[1] + " " + cur_time_text[2]
    list_data = []
    list_data.append(ymd)
    list_data.append(cur_time)
    for num in range(0, len(ptab0), 1):
        list_data.append(ptab0[num].text)
        list_data.append(ptab1[num].text)

    return list_data


if __name__ == '__main__':
    driver = create_driver()
    # 国内数据
    in_data = get_internal_data(driver)
    in_data.append('国内')
    # create_time
    in_data.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    # update_time
    in_data.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print(in_data)
    # MysqlUtil.insert_current_epidemic_internal(in_data)

    # 国外数据
    fo_data = get_foreign_data(driver)
    fo_data.append('国外')
    # create_time
    fo_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # update_time
    fo_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print(fo_data)
    # MysqlUtil.insert_current_epidemic_foreign(fo_data)

    driver.quit()

