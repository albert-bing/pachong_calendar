# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/9 17:13
# @Author：albert·bing
# @File：date_calendar.py
# @Software：PyCharm


#  start your code

# 导入selenium的驱动接口
from selenium import webdriver
# 导入键盘操作的keys包
from selenium.webdriver.common.keys import Keys
# 导入chrome选项
from selenium.webdriver.chrome.options import Options

import requests
from bs4 import BeautifulSoup
import urllib3

from com.wt.common import MysqlUtil

# 忽略https的安全警告
urllib3.disable_warnings()
# 导入时间
import time
from com.wt.config import config


# 创建driver
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=config._CHROME_DRIVER_WIN, options=chrome_options)
    return driver


def analyze_data(driver, dump):
    list_data = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 年月、星期的爬取
    year_month_data = soup.find(name='div', attrs={'id': 'MonthStr'}).text
    # 2020年7月
    yy = year_month_data.split('年')[0]
    mm = year_month_data.split('年')[1].split('月')[0]
    if int(mm) < 10:
        mm = '0'+mm
    y_m_data = yy+mm

    # week_data = soup.find(name='div', attrs={'id': 'gregorianDayStr'}).text
    # print(week_data)
    # 农历、公历、节气、节日的爬取
    m_data = soup.find_all(name='div', attrs={'class': 'mainCal'})
    tbody_data = m_data[0].select('tbody')
    # 一整个月的农历和公历日期
    gongli_data = tbody_data[0].find_all(name="div", attrs={"class", "number5"})
    if gongli_data == []:
        gongli_data = tbody_data[0].find_all(name="div", attrs={"class", "number6"})
    if gongli_data == []:
        gongli_data = tbody_data[0].find_all(name="div", attrs={"class", "number4"})
    if gongli_data == []:
        print(y_m_data+"is wrong")
        return
    nongli_data = tbody_data[0].find_all(name="div", attrs={"class", "chinaday"})

    # 获取表示星期的维度的集合
    td_list = tbody_data[0].select("td")
    # print(td_list)
    # 节气表
    solar_terms_list = ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋',
                        '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']

    flag = 0
    for num in range(0, len(gongli_data), 1):
        g_data = gongli_data[num].text
        n_data = nongli_data[num].text

        # 节气
        solar = ''
        # 元组
        r_data = []
        # 首先判断是不是一个月的第一天
        if g_data == '1':
            flag += 1
        if flag == 1:
            # 公历的处理
            if int(g_data) < 10:
                g = '0'+g_data
            else:
                g = g_data
            gr_data = y_m_data+g
            # 获取星期维度
            # print("num=",num)
            j = str(td_list[num]).split("j=")[1].split('"')[1]
            # print("j=",j)
            # 节气的处理
            for n in range(0,len(solar_terms_list),1):
                if n_data == solar_terms_list[n]:
                    solar = n_data
                    break
            r_data.append(gr_data)
            r_data.append(n_data)
            r_data.append(str(int(j)+1))
            r_data.append(solar)
            r_data.append(g)

            list_data.append(tuple(r_data))
    return list_data,y_m_data


# 解析数据：
#     month_num : 月份数量
#     dump : 上下跳
def get_data(driver, month_num, dump):
    driver.get("https://wannianli.tianqi.com/")
    time.sleep(2)
    for num in range(0,month_num,1):

        if num < 432:
            driver.find_element_by_id('prev_buttons').click()
            continue
        # 判断前后跳
        # 后跳
        if dump == 'down':
            driver.find_element_by_id('next_buttons').click()
            time.sleep(2)
        # 前跳
        elif dump == 'up':
            driver.find_element_by_id('prev_buttons').click()
            time.sleep(2)
        # 本页
        else:
            data, y_m_data = analyze_data(driver, dump)
            print(y_m_data)
            MysqlUtil.insert_data_calendar(data)
            break

        data, y_m_data = analyze_data(driver, dump)
        print(num,"次")
        print(y_m_data)
        MysqlUtil.insert_data_calendar(data)
        # 沉睡一秒，防止插入数据时的丢失
        time.sleep(2)


if __name__ == '__main__':
    # 获取driver
    driver = create_driver()

    get_data(driver,607,"up")

    # data,y_m_data = analyze_data(driver, 'none')
    # print(y_m_data)
    driver.close()
