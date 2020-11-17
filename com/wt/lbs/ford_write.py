# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
import logging
import urllib3
import json
from com.wt.common import MongodbUtil
import requests
import paramiko
import time
import pandas as pd

import xlrd
import xlwt
import faker
# 忽略https的安全警告
urllib3.disable_warnings()

def read_data():
    sb = xlrd.open_workbook('E:\\项目文件\\C490\\保存数据\\save_data.xlsx')
    sheet = sb.sheets()[0]
    list_all = []
    for ss in range(1, sheet.nrows):
        cells = sheet.row_values(ss)
        tup = [cells[1], cells[2], cells[5], cells[8],cells[9], cells[10], cells[11], cells[12], cells[13], cells[24],
               cells[26], cells[27], cells[36]]
        list_all.append(tup)
    return list_all


def analysis_data(an_data):
    re_data = []
    for i in range(0, len(an_data), 1):
        one_data = get_geo_data(an_data[i])
        re_data.append(one_data)
    return re_data

def get_geo_data(data):
    # old_id、
    one_data = [""]
    # 添加 name
    one_data.append(data[0])
    # 添加location（经纬度）
    one_data.append(data[1])
    # 添加type为null
    one_data.append("")
    # 添加address
    one_data.append(data[2])
    # 添加phone exp:"销售:021-57432116;服务：021-62176667",
    one_data.append(str(data[10]).split(".")[0])
    # 获取postcode、
    one_data.append("")
    # 获取省份
    one_data.append(data[3])
    # 获取省份编码
    one_data.append(str(data[4]).split(".")[0])
    # 获取城市名称
    one_data.append(data[5])
    # 获取城市编码
    one_data.append(str(data[6]).split(".")[0])
    # 获取地区名称
    one_data.append(data[7])
    # 获取地区编码
    one_data.append(str(data[8]).split(".")[0])
    # 添加邮箱
    one_data.append("")
    # 添加销售电话 salesPhoneNum
    one_data.append(str(data[10]).split(".")[0])
    # 添加 dealerAffiliation
    one_data.append("")
    # 添加 serviceHistoryID
    one_data.append("")
    # 添加 saleshours
    one_data.append("")
    # 添加 administrativeArea
    one_data.append("")
    # 添加 eDaijiaCustomerID
    one_data.append("")
    # 添加 servicehours
    one_data.append("")
    # 添加 primaryPhone
    one_data.append(str(data[10]).split(".")[0])
    # 添加 localcity
    one_data.append(data[5])
    # 添加 OSBDealerID
    one_data.append(str(data[9]).split(".")[0])
    # 添加 weiboURL
    one_data.append("")
    # 添加 OSBPhone 和 servicePhoneNumber
    one_data.append(str(data[10]).split(".")[0])
    one_data.append(str(data[10]).split(".")[0])
    # 添加 dealerNewVehicle 、 eDaijiaPhone 、weChatUrl、eDaijiaFlag、JVFlag
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    # 添加 fax
    one_data.append(str(data[11]).split(".")[0])
    # 添加 createtime 、 updatetime
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 添加 dealerId
    one_data.append(data[12])
    # 添加 _class
    one_data.append("")
    return one_data

# 保存数据
def save(data):
    result_data = []
    for i in range(0, len(data), 1):
        d = data[i]
        try:
            re_data = '{"old_id":"' + d[0] + '","name":"' + d[1] + '","location":[' + d[2] + '],"type":"' + d[
                3] + '","address":"' + d[4] + '","phone":"' + d[5] + '"' \
                                                                     ',"postcode":"' + d[6] + '","pname":"' + d[
                          7] + '","pcode":"' + d[8] + '","cityname":"' + d[9] + '","citycode":"' + d[10] + '"' \
                                                                                                           ',"adname":"' + \
                      d[11] + '","adcode":"' + d[12] + '","email":"' + d[13] + '","salesPhoneNum":"' + d[
                          14] + '","dealerAffiliation":"' + d[15] + '",' \
                                                                    '"serviceHistoryID":"' + d[
                          16] + '","saleshours":"' + d[17] + '","administrativeArea":"' + d[
                          18] + '","eDaijiaCustomerID":"' + d[19] + '",' \
                                                                    '"servicehours":"' + d[20] + '","primaryPhone":"' + \
                      d[21] + '","localcity":"' + d[22] + '","OSBDealerID":"' + d[23] + '","weiboURL":"' + d[24] + '"' \
                                                                                                                   ',"OSBPhone":"' + \
                      d[25] + '","servicePhoneNumber":"' + d[26] + '","dealerNewVehicle":"' + d[
                          27] + '","eDaijiaPhone":"' + d[28] + '","weChatUrl":"' + d[29] + '"' \
                                                                                           ',"eDaijiaFlag":"' + d[
                          30] + '","JVFlag":"' + d[31] + '","fax":"' + d[32] + '","createtime":"' + d[
                          33] + '","updatetime":"' + d[34] + '","dealerId":"' + d[35] + '","_class":"' + d[36] + '"}'
            result_data.append(re_data)
        except Exception as res:
            print("抛出异常：")
            print(data[i])
            print(res)
    # 保存数据
    MongodbUtil.save_data_ford(result_data)

if __name__ == '__main__':
    list_all = read_data()
    re_data = analysis_data(list_all)
    save(re_data)
