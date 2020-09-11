# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code
# 导入selenium的驱动接口
import logging

import pandas as pd
import urllib3
import json
from com.wt.common import MysqlUtil
import requests
import paramiko
import time

# 忽略https的安全警告
urllib3.disable_warnings()


# 从远程获取数据
def get_csv():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("120.26.146.183", "6143", "czsqauser", "#UIOP2wsxcde45", timeout=5)
    sftp_client = client.open_sftp()
    logging.info(sftp_client)
    date_str = time.strftime('%Y%m%d', time.localtime(time.time()))
    remote_file = sftp_client.open("/fm02/DMS-FM-DFM02-" + date_str + "-01.csv", 'r')
    # 读取一行数据，并且去掉换行符，读两次是因为可以去掉表头
    line = remote_file.readline().strip()
    line = remote_file.readline().strip()
    data = []
    # 循环读取文件信息--按行读取
    while line:
        one_data = line.split(",")
        data.append(one_data)
        line = remote_file.readline().strip()
    return data


# 获取经纬信息
""":arg
    实现思路：
        1.需要请求两次高德的接口
        2.将第一次请求不到的经销商的名称再进行一次请求
        3.将第二次依旧请求不到的数据返回，向百度地图请求
"""


def get_log_lat(data):
    num = 0
    # 需要高德第二次请求的数据
    back_data = []
    # 高德第一次获取的要处理的数据
    geo_data1 = []
    # 高德第二次获取的要处理的数据
    geo_data2 = []
    for i in range(0, len(data), 1):
        url = "https://restapi.amap.com/v3/geocode/geo?key=84b31c0b9ebe60f23788d6b6f0c96aa5&address=" + data[i][4]
        resource_data = requests.get(url=url, verify=False)
        try:
            if json.loads(resource_data.text)['count'] == '0' and data[i][4] != 'test':
                print(data[i][4] + "------" + resource_data.text)
                back_data.append(data[i])
            elif data[i][4] != 'test':
                geo_data1.append(resource_data.text + "&&" + ",".join(data[i]))
        except Exception as result:
            print("++++++" + data[i][4] + "+++++++" + result)
    print("-------------------------------------------------------")

    # 需要百度地图解析的经销商
    re_data = []
    for j in range(0, len(back_data), 1):
        url1 = "https://restapi.amap.com/v3/place/text?key=3bfeccd1063286c0ccb0600555909e2d&keywords=" + \
               back_data[j][4] + "&extensions=all&types=020000"
        resource_data1 = requests.get(url=url1, verify=False)
        if json.loads(resource_data1.text)['count'] == '0':
            num += 1
            re_data.append(back_data[j])
            print(back_data[j][4] + "==" + resource_data1.text)
        else:
            geo_data2.append(resource_data1.text + "&&" + ",".join(back_data[j]))
    print("+++++++++++++++++++++++++++++++++++++++++")
    return re_data, geo_data1, geo_data2


# 从百度地图获取经销商的数据
def get_log_lat_baidu(data):
    # 第一次获取百度要处理的数据
    du_data = []
    # 第二次获取到百度要处理的数据
    re_data = []
    # 第一次请求主要是获取到经纬度
    for k in range(0, len(data), 1):
        url = "http://api.map.baidu.com/geocoding/v3/?address=" + data[k][
            4] + "&ak=d0FaYLZV11VDUPifOWdSPsItnIvBkKeR&output=json"
        resource_data2 = requests.get(url=url, verify=False)
        du_data.append(resource_data2.text)
    # 第二次请求通过获取到的经纬度，再获取到具体的省市区县信息
    for h in range(0,len(du_data),1):
        one_d = json.loads(du_data[h])
        lng = one_d['result']['location']['lng']
        lat = one_d['result']['location']['lat']
        url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=d0FaYLZV11VDUPifOWdSPsItnIvBkKeR&output=json&coordtype=wgs84ll&location="+str(lat)+","+str(lng)
        resource_data = requests.get(url=url,verify=False)
        re_data.append(resource_data.text + "&&" + ",".join(data[h]))
    return re_data


# 将获取的三部分数据进行处理，形成统一的数据格式
def analysis_data(n, an_data):
    re_data = []
    # 处理高德第一次返回的数据
    if n == 1:
        for i in range(0, len(an_data), 1):
            one_data = get_geo_data1(an_data[i])
            re_data.append(one_data)
    # 处理高德第二次返回的数据
    elif n == 2:
        for i in range(0, len(an_data), 1):
            one_data = get_geo_data2(an_data[i])
            re_data.append(one_data)
    # 处理百度返回的数据
    else:
        for i in range(0, len(an_data), 1):
            one_data = get_geo_data3(an_data[i])
            re_data.append(one_data)
    return re_data


# 解析数据 一
def get_geo_data1(data):
    """:arg
        将从远程获取的经销商的信息和从高德获取的信息合并之后再次分开,其中list_data[0]表示高德获取的信息，list_data[1]表示远程文件获取的
    """
    list_data = data.split("&&")
    print(data)
    # 把从高德获取的信息转化为字典
    data1 = json.loads(list_data[0])
    # 把从远程文件获取的信息转化为数组
    data2 = list_data[1].split(",")
    """:arg
         "_id": {"$oid": "5f51dab03a7dd915d0be8de2"},  // key值
        "old_id": "44021", // null
        "name": "上海金旋铃铃汽车销售服务有限公司", // 名称
        "location": [121.442588, 30.95778],
        "type": "", // null
        "address": "上海市奉贤区肖塘镇沪杭公路1058号（近大叶公路）", // 地址
        "phone": "销售:021-57432116;服务：021-62176667", // 电话取一个
        "postcode": "200140", // 表格中的邮政编码
        "pname": "上海市", // 省份
        "pcode": "310000", //
        "cityname": "上海市",  // 可获取
        "citycode": "310100", // 不可获取
        "adname": "奉贤区", // 可获取
        "adcode": "310120", // 可获取
        "email": "mailto:shjl@jmc.com.cn",
        "salesPhoneNum": "021-57432116",
        "dealerAffiliation": "江铃汽车福特品牌经销商",// null
        "serviceHistoryID": "", // null
        "saleshours": "08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00", // null
        "administrativeArea": "上海",// null
        "eDaijiaCustomerID": "", // null
        "servicehours": "08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00",// null
        "primaryPhone": "销售:021-57432116;服务：021-62176667",// 电话取一个
        "localcity": "上海", // city
        "OSBDealerID": "", //DealerID
        "weiboURL": "", // null
        "OSBPhone": "", // 电话取一个
        "servicePhoneNumber": "021-62176667",  // 电话取一个
        "dealerNewVehicle": "福特新世代全顺,福特新全顺,福特途睿欧,全新福特撼路者,全新福特领界",// null
        "eDaijiaPhone": "",// null
        "weChatUrl": "",// null
        "eDaijiaFlag": "",// null
        "JVFlag": "JMC",// null
        "fax": "021-65931838",// 电话取一个
        "createtime": "2020-03-09 22:04:14",
        "updatetime": "2020-03-09 22:04:14",
        "dealerId": "1108101A",//DealerID
        "_class": "com.autopai.poi.model.mongo.FordWebsiteSales"// null
    """
    # old_id、添加 name、 添加location（经纬度）、 添加type为null、 添加address
    # 添加phone exp:"销售:021-57432116;服务：021-62176667",获取postcode、 获取省份
    one_data = ["", data2[4], data1['geocodes'][0]['location'], "", data2[10], "销售：" + data2[13] + ";服务：" + data2[12],
                data2[11], data1['geocodes'][0]['province']]
    # 获取省份编码
    p_code = data1['geocodes'][0]['adcode']
    p_code = p_code[0:2] + "0000"
    one_data.append(p_code)
    # 获取城市名称
    one_data.append(data1['geocodes'][0]['city'])
    # 获取城市编码
    c_code = data1['geocodes'][0]['adcode']
    c_code = c_code[0:4] + "00"
    one_data.append(c_code)
    # 获取地区名称
    one_data.append(data1['geocodes'][0]['district'])
    # 获取地区编码
    one_data.append(data1['geocodes'][0]['adcode'])
    # 添加邮箱
    one_data.append("")
    # 添加销售电话 salesPhoneNum
    one_data.append(data2[13])
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
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 添加 localcity
    one_data.append(data1['geocodes'][0]['city'])
    # 添加 OSBDealerID
    one_data.append(data2[0])
    # 添加 weiboURL
    one_data.append("")
    # 添加 OSBPhone 和 servicePhoneNumber
    if data2[13] != "":
        one_data.append(data2[13])
        one_data.append(data2[13])
    else:
        one_data.append(data2[12])
        one_data.append(data2[12])
    # 添加 dealerNewVehicle 、 eDaijiaPhone 、weChatUrl、eDaijiaFlag、JVFlag
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    # 添加 fax
    one_data.append(data2[12])
    # 添加 createtime 、 updatetime
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 添加 dealerId
    one_data.append(data2[0])
    # 添加 _class
    one_data.append("")

    return one_data


# 解析数据 二
def get_geo_data2(data):
    """:arg
        将从远程获取的经销商的信息和从高德获取的信息合并之后再次分开,其中list_data[0]表示高德获取的信息，list_data[1]表示远程文件获取的
    """
    list_data = data.split("&&")
    # 把从高德获取的信息转化为字典
    data1 = json.loads(list_data[0])
    # 把从远程文件获取的信息转化为数组
    data2 = list_data[1].split(",")
    """:arg
         "_id": {"$oid": "5f51dab03a7dd915d0be8de2"},  // key值
        "old_id": "44021", // null
        "name": "上海金旋铃铃汽车销售服务有限公司", // 名称
        "location": [121.442588, 30.95778],
        "type": "", // null
        "address": "上海市奉贤区肖塘镇沪杭公路1058号（近大叶公路）", // 地址
        "phone": "销售:021-57432116;服务：021-62176667", // 电话取一个
        "postcode": "200140", // 表格中的邮政编码
        "pname": "上海市", // 省份
        "pcode": "310000", //
        "cityname": "上海市",  // 可获取
        "citycode": "310100", // 不可获取
        "adname": "奉贤区", // 可获取
        "adcode": "310120", // 可获取
        "email": "mailto:shjl@jmc.com.cn",
        "salesPhoneNum": "021-57432116",
        "dealerAffiliation": "江铃汽车福特品牌经销商",// null
        "serviceHistoryID": "", // null
        "saleshours": "08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00", // null
        "administrativeArea": "上海",// null
        "eDaijiaCustomerID": "", // null
        "servicehours": "08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00",// null
        "primaryPhone": "销售:021-57432116;服务：021-62176667",// 电话取一个
        "localcity": "上海", // city
        "OSBDealerID": "", //DealerID
        "weiboURL": "", // null
        "OSBPhone": "", // 电话取一个
        "servicePhoneNumber": "021-62176667",  // 电话取一个
        "dealerNewVehicle": "福特新世代全顺,福特新全顺,福特途睿欧,全新福特撼路者,全新福特领界",// null
        "eDaijiaPhone": "",// null
        "weChatUrl": "",// null
        "eDaijiaFlag": "",// null
        "JVFlag": "JMC",// null
        "fax": "021-65931838",// 电话取一个
        "createtime": "2020-03-09 22:04:14",
        "updatetime": "2020-03-09 22:04:14",
        "dealerId": "1108101A",//DealerID
        "_class": "com.autopai.poi.model.mongo.FordWebsiteSales"// null
    """
    # old_id、添加 name、 添加location（经纬度）、 添加type为null、 添加address
    # 添加phone exp:"销售:021-57432116;服务：021-62176667",获取postcode、 获取省份
    one_data = ["", data2[4], data1['pois'][0]['location'], "", data2[10], "销售：" + data2[13] + ";服务：" + data2[12],
                data2[11], data1['pois'][0]['pname']]
    # 获取省份编码
    one_data.append(data1['pois'][0]['pcode'])
    # 获取城市名称
    one_data.append(data1['pois'][0]['cityname'])
    # 获取城市编码
    c_code = data1['pois'][0]['adcode']
    c_code = c_code[0:4] + "00"
    one_data.append(c_code)
    # 获取地区名称
    one_data.append(data1['pois'][0]['adname'])
    # 获取地区编码
    one_data.append(data1['pois'][0]['adcode'])
    # 添加邮箱
    one_data.append("")
    # 添加销售电话 salesPhoneNum
    one_data.append(data2[13])
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
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 添加 localcity
    one_data.append(data1['pois'][0]['cityname'])
    # 添加 OSBDealerID
    one_data.append(data2[0])
    # 添加 weiboURL
    one_data.append("")
    # 添加 OSBPhone 和 servicePhoneNumber
    if data2[13] != "":
        one_data.append(data2[13])
        one_data.append(data2[13])
    else:
        one_data.append(data2[12])
        one_data.append(data2[12])
    # 添加 dealerNewVehicle 、 eDaijiaPhone 、weChatUrl、eDaijiaFlag、JVFlag
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    # 添加 fax
    one_data.append(data2[12])
    # 添加 createtime 、 updatetime
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 添加 dealerId
    one_data.append(data2[0])
    # 添加 _class
    one_data.append("")

    return one_data


# 解析数据 三
def get_geo_data3(data):
    """:arg
        将从远程获取的经销商的信息和从高德获取的信息合并之后再次分开,其中list_data[0]表示高德获取的信息，list_data[1]表示远程文件获取的
    """
    list_data = data.split("&&")
    print(data)
    # 把从高德获取的信息转化为字典
    data1 = json.loads(list_data[0])
    # 把从远程文件获取的信息转化为数组
    data2 = list_data[1].split(",")
    """:arg
         "_id": {"$oid": "5f51dab03a7dd915d0be8de2"},  // key值
        "old_id": "44021", // null
        "name": "上海金旋铃铃汽车销售服务有限公司", // 名称
        "location": [121.442588, 30.95778],
        "type": "", // null
        "address": "上海市奉贤区肖塘镇沪杭公路1058号（近大叶公路）", // 地址
        "phone": "销售:021-57432116;服务：021-62176667", // 电话取一个
        "postcode": "200140", // 表格中的邮政编码
        "pname": "上海市", // 省份
        "pcode": "310000", //
        "cityname": "上海市",  // 可获取
        "citycode": "310100", // 不可获取
        "adname": "奉贤区", // 可获取
        "adcode": "310120", // 可获取
        "email": "mailto:shjl@jmc.com.cn",
        "salesPhoneNum": "021-57432116",
        "dealerAffiliation": "江铃汽车福特品牌经销商",// null
        "serviceHistoryID": "", // null
        "saleshours": "08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00", // null
        "administrativeArea": "上海",// null
        "eDaijiaCustomerID": "", // null
        "servicehours": "08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00;08:00,17:00",// null
        "primaryPhone": "销售:021-57432116;服务：021-62176667",// 电话取一个
        "localcity": "上海", // city
        "OSBDealerID": "", //DealerID
        "weiboURL": "", // null
        "OSBPhone": "", // 电话取一个
        "servicePhoneNumber": "021-62176667",  // 电话取一个
        "dealerNewVehicle": "福特新世代全顺,福特新全顺,福特途睿欧,全新福特撼路者,全新福特领界",// null
        "eDaijiaPhone": "",// null
        "weChatUrl": "",// null
        "eDaijiaFlag": "",// null
        "JVFlag": "JMC",// null
        "fax": "021-65931838",// 电话取一个
        "createtime": "2020-03-09 22:04:14",
        "updatetime": "2020-03-09 22:04:14",
        "dealerId": "1108101A",//DealerID
        "_class": "com.autopai.poi.model.mongo.FordWebsiteSales"// null
    """
    # old_id、
    one_data = [""]
    # 添加 name、
    one_data.append(data2[4])
    # 添加location（经纬度）、
    lng = data1['result']['location']['lng']
    lat = data1['result']['location']['lat']
    one_data.append(str(lng)+","+str(lat))
    # 添加type为null、
    one_data.append("")
    # 添加address
    one_data.append(data2[10])
    # 添加phone exp:"销售:021-57432116;服务：021-62176667",
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 获取postcode、
    one_data.append(data2[11])
    # 获取省份
    one_data.append(data1['result']['addressComponent']['province'])
    # 获取省份编码
    p_code = data1['result']['addressComponent']['adcode']
    p_code = p_code[0:2] + "0000"
    one_data.append(p_code)
    # 获取城市名称
    one_data.append(data1['result']['addressComponent']['city'])
    # 获取城市编码
    c_code = data1['result']['addressComponent']['adcode']
    c_code = c_code[0:4] + "00"
    one_data.append(c_code)
    # 获取地区名称
    one_data.append(data1['result']['addressComponent']['district'])
    # 获取地区编码
    one_data.append(data1['result']['addressComponent']['adcode'])
    # 添加邮箱
    one_data.append("")
    # 添加销售电话 salesPhoneNum
    one_data.append(data2[13])
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
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 添加 localcity
    one_data.append(data1['result']['addressComponent']['city'])
    # 添加 OSBDealerID
    one_data.append(data2[0])
    # 添加 weiboURL
    one_data.append("")
    # 添加 OSBPhone 和 servicePhoneNumber
    if data2[13] != "":
        one_data.append(data2[13])
        one_data.append(data2[13])
    else:
        one_data.append(data2[12])
        one_data.append(data2[12])
    # 添加 dealerNewVehicle 、 eDaijiaPhone 、weChatUrl、eDaijiaFlag、JVFlag
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    # 添加 fax
    one_data.append(data2[12])
    # 添加 createtime 、 updatetime
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 添加 dealerId
    one_data.append(data2[0])
    # 添加 _class
    one_data.append("")

    return one_data


if __name__ == '__main__':
    # 从远程的csv获取数据
    data = get_csv()
    # re_data:在高德请求剩余的数据，geo_data1：第一次高德请求到的数据，geo_data2：第二次高德请求到的数据
    re_data, geo_data1, geo_data2 = get_log_lat(data)
    # 去百度地图获取经纬度,拿到返回的数据
    du_data = get_log_lat_baidu(re_data)

    # 处理高德第一次返回的数据
    result_data1 = analysis_data(1, geo_data1)
    # 处理高德第二次返回的数据
    result_data2 = analysis_data(2, geo_data2)
    # 处理百度返回的数据
    result_data3 = analysis_data(3, du_data)
    # 将处理好的三个数据进行合并
    result_data = result_data1 + result_data2 + result_data3

    print(result_data)

