# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')


import requests
from bs4 import BeautifulSoup
import urllib3

from com.wt.common import MysqlUtil
import re
# 忽略https的安全警告
urllib3.disable_warnings()
# 导入时间
import time
from com.wt.config import config
from collections import OrderedDict

# 获取数据
def get_data(url):
    list_data = []
    data = requests.get(url=url, verify=False)
    soup = BeautifulSoup(data.text, "html.parser")
    #  获取日历信息
    calendar = soup.find_all("td",attrs={"class":"t_1"})
    # 农历
    lunar_calendar = calendar[0].text.replace("\r\n", "").replace(" ","").split("(")[0]
    # 公历
    gregorian_calendar = calendar[1].text.replace("\r\n", "").replace(" ","").split("星")[0]
    # 日期
    y_day = gregorian_calendar.replace('公历','').replace('年','').replace('月','').replace('日','')
    # 无法对应的数据
    dao = ""
    start = ""
    # 获取宜事和忌事
    yi_ji = soup.find_all("td",attrs={"class":"t_4"})
    list_yi = yi_ji[0].text.replace("\r\n", "").split(" ")
    # 宜
    yi = sub_str(list_yi)
    list_ji = yi_ji[1].text.replace("\r\n", "").split(" ")
    # 忌
    ji = sub_str(list_ji)
    chong_text = soup.find_all("td",attrs={"class":"t_5"})
    chong_1 = chong_text[1].text.split("相冲:")[1].split("\n岁煞:")[0][2:]
    chong_2 = chong_text[1].text.split("相冲:")[1].split("\n岁煞:")[1].split("\u3000星宿")[0]
    # 冲
    chong = chong_1 + " " + chong_2
    # 岁次
    sui_ci_text = soup.find_all("font",attrs={"color":"#990000"})
    sui_ci = sui_ci_text[0].text + " " + sui_ci_text[1].text + " " + sui_ci_text[2].text
    shen_text = soup.find_all("td",attrs={"class":"t_6"})
    # 胎神
    tai = shen_text[2].text.split("神")[2][1:]
    # 五行
    wuxing = shen_text[4].text.split("日五行")[1].strip()
    shen_list = shen_text[0].text.split(" ")
    # 喜神
    xi = shen_list[18].split("：")[1]
    # 福神
    fu = shen_list[19].split("：")[1]
    # 财神
    cai = shen_list[20].split("：")[1]
    # 星座
    constellation = calendar[1].text.replace("\r\n", "").replace(" ", "").split("星")[1][2:5]
    # 属相
    chinese_zodias_text = soup.find_all("div",attrs={"align":"center"})
    chinese_zodias = chinese_zodias_text[7].text.split(" ")[0].split("\u3000")[1]

    xiong_ji = soup.find_all("td",attrs={"class":"t_3"})
    xiongshen = xiong_ji[0].text.split("：")[1]
    jishen = xiong_ji[1].text.split("：")[1]
    
    list_data.append(y_day,gregorian_calendar,lunar_calendar,dao,start,yi,ji,chong,sui_ci,tai,wuxing,cai,xi,fu,constellation,chinese_zodias,xiongshen,jishen)

    return list_data



def get_url():
    url = "http://www.laohuangli.net/2009/2009-12-28.html"

    return url


def sub_str(str):
    s = ""
    for i in range(0,len(str),1):
        if str[i] != '':
            s = s + str[i] + " "
    return s.rstrip()
if __name__ == '__main__':
    url = get_url()

    list_data = get_data(url)

