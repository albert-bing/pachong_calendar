# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code
import datetime
import json
import time
from urllib.parse import quote
if __name__ == '__main__':
    data = '{"status":0,"result":{"location":{"lng":36.11512272009569,"lat":85.09099187480457},"formatted_address":"","business":"","addressComponent":{"country":"","country_code":-1,"country_code_iso":"","country_code_iso2":"","province":"","city":"","city_level":2,"district":"","town":"","town_code":"","adcode":"0","street":"","street_number":"","direction":"","distance":""},"pois":[],"roads":[],"poiRegions":[],"sematic_description":"","cityCode":0}}&&A37007,A3700701,80520,8052001,临汾天健宏远汽车销售服务有限公司洪洞分公司,临汾天健宏远洪洞分公司,1010406.0,1.01040612E8,1.01010208E8,1.0101020817E10,山西省临汾市洪洞县客运站往北30米路东（108国道旁）,,,0357-3999927,Y'
    list_data = data.split("&&")
    print(data)
    # 把从高德获取的信息转化为字典
    data1 = json.loads(list_data[0])
    # 把从远程文件获取的信息转化为数组
    data2 = list_data[1].split(",")

    # old_id、
    one_data = [""]
    # 添加 name、
    one_data.append(data2[4])
    # 添加location（经纬度）、
    lng = data1['result']['location']['lng']
    lat = data1['result']['location']['lat']
    one_data.append(str(lng) + "," + str(lat))
    # 添加type为null、
    one_data.append("")
    # 添加address
    one_data.append(data2[10])
    # 添加phone exp:"销售:021-57432116;服务：021-62176667",
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 获取postcode、
    one_data.append(data2[11])
    # 获取省份
    one_data.append(data1['result']['addressComponent'])
    print(one_data)
    # 获取省份编码
    p_code = data1['result']['addressComponent']['adcode']
    p_code = p_code[0:2] + "0000"
    one_data.append(p_code)
    # 获取城市名称
    one_data.append(['result']['addressComponent']['city'])
    # 获取城市编码
    c_code = data1['result']['addressComponent']['adcode']
    c_code = c_code[0:4] + "00"
    one_data.append(c_code)
    # 获取地区名称
    one_data.append(data1['result']['addressComponent']['district'])
    # 获取地区编码
    one_data.append(data1['result']['addressComponent']['adcode'])