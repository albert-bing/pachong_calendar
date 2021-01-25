# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')


import urllib3

from com.wt.common import MongodbUtil

import pandas as pd

import xlrd
# 忽略https的安全警告
urllib3.disable_warnings()


def read_data():
    sb = xlrd.open_workbook('E:\\项目文件\\C490\\保存数据\\save_data.xlsx')
    sheet = sb.sheets()[0]
    list_all = []
    for ss in range(1, sheet.nrows):
        cells = sheet.row_values(ss)
        tup = [cells[1], cells[5]]
        list_all.append(tup)
    return list_all


if __name__ == '__main__':
    sour_data = read_data()
    MongodbUtil.update_address_all(sour_data)