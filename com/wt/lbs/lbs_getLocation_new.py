# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：lbs_getLocation_new.py
# 开发工具：PyCharm


#  start your code
# 导入selenium的驱动接口
import logging
import urllib3
import json
from com.wt.common import MongodbUtil
import requests
import paramiko
import time
import pandas as pd

# 忽略https的安全警告
urllib3.disable_warnings()

logging.basicConfig(filename='./log_lbs.txt',level=logging.DEBUG)

logging.info(time.strftime('%Y%m%d', time.localtime(time.time())))
# 从远程获取数据
def get_csv():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 正式环境
    client.connect("47.96.21.66", "6143", "cz_proftp", "#DFGcvbhu87ytr", timeout=5)
    # 测试环境
    # client.connect("120.26.146.183", "6143", "czsqauser", "#UIOP2wsxcde45", timeout=5)
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

    # test = pd.DataFrame(data=data)
    # test.to_csv('./test1.csv')
    return data


# 从百度地图获取经销商的数据
def get_log_lat_baidu(data):
    # 第一次获取百度要处理的数据
    du_data = []
    # 第二次获取到百度要处理的数据
    re_data = []
    pro_data = []
    # 第一次请求主要是获取到经纬度
    for k in range(0, len(data), 1):
        s = "武汉威汉汽车销售有限责任公司仙桃分公司"
        if s in data[k][4]:
            data[k][4] = s
        url = "http://api.map.baidu.com/geocoding/v3/?address=" + data[k][
            4] + "&ak=bRKF4EQsu45sSBqVYH4G9LykCwI2W6KD&output=json"
        resource_data2 = requests.get(url=url, verify=False)
        #  睡眠100ms，防止并发过量
        time.sleep(0.2)
        du_data.append(resource_data2.text)
    # 第二次请求通过获取到的经纬度，再获取到具体的省市区县信息
    for h in range(0, len(data), 1):
        one_d = json.loads(du_data[h])
        if one_d['status'] == 0:
            lng = one_d['result']['location']['lng']
            lat = one_d['result']['location']['lat']
            url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=bRKF4EQsu45sSBqVYH4G9LykCwI2W6KD&output=json&coordtype=wgs84ll&location=" + str(
                lat) + "," + str(lng)
            resource_data = requests.get(url=url, verify=False)
            re_data.append(resource_data.text + "&&" + ",".join(data[h]))
        else:
            pro_data.append(data[h])
        #  睡眠100ms，防止并发过量
        time.sleep(0.2)
    logging.info('----------------------百度部分数据获取完成---------------------------------')
    return re_data, pro_data




# 将获取的三部分数据进行处理，形成统一的数据格式
def analysis_data(an_data):
    re_data = []
    for i in range(0, len(an_data), 1):
        one_data = get_geo_data(an_data[i])
        re_data.append(one_data)
    return re_data


# 解析数据
def get_geo_data(data):
    """:arg
        将从远程获取的经销商的信息和从高德获取的信息合并之后再次分开,其中list_data[0]表示高德获取的信息，list_data[1]表示远程文件获取的
    """
    list_data = data.split("&&")
    # 把从高德获取的信息转化为字典
    data1 = json.loads(list_data[0])
    # 把从远程文件获取的信息转化为数组
    data2 = list_data[1].split(",")
    # old_id、
    one_data = [""]
    # 添加 name、
    one_data.append(data2[4])
    # 添加location（经纬度）、
    try:
        lng = data1['result']['location']['lng']
        lat = data1['result']['location']['lat']
    except KeyError as res:
        print(data)
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
    one_data.append(data2[2])
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


# 根据获取到的数据和已经存在的数据进行对比
def compare_data(source_data, existed_data):
    # 新增的经销商
    re_data = []
    flag = True
    # 对比是否有
    for i in range(0, len(source_data), 1):
        for j in range(0, len(existed_data), 1):
            if "武汉威汉汽车销售有限责任公司仙桃分公司" in source_data[i][4]:
                source_data[i][4] = '武汉威汉汽车销售有限责任公司仙桃分公司'
            if source_data[i][4] == existed_data[j]['name']:
                flag = False
                existed_data.pop(j)
                break
        if flag:
            re_data.append(source_data[i])
        else:
            flag = True
    # 消失的经销商
    delete_data = existed_data
    return re_data,delete_data


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
    MongodbUtil.update_data_ford(result_data)


if __name__ == '__main__':
    # 从远程的csv获取数据
    data = get_csv()

    # 获取mongodb中之前就存好的数据
    # get_data,count = MongodbUtil.select_fords_all()
    # if count != 0:
    #     existed_data = []
    #     # 将从mongodb中获取的数据格式转化为数组
    #     for i in range(0,count,1):
    #         existed_data.append(get_data[i])
    #     # 对比更新的数据
    #     not_exist_data,remove_data = compare_data(data, existed_data)
    #     MongodbUtil.remove_fords_data(remove_data)
    # else:
    #     not_exist_data = data

    # 去百度地图获取经纬度,拿到返回的数据
    if len(data) > 0:
        du_data, pro_data = get_log_lat_baidu(data)
        logging.info("==========第一次获取数据**开始**==========")
        # 处理百度返回的数据
        print("du_data:%d" % len(du_data))
        print("pro_data:%d" % len(pro_data))
        logging.info("==========第一次获取数据**结束**==========")

        logging.info("==========第二次获取数据**开始**==========")
        du_data2, pro_data2 = get_log_lat_baidu(pro_data)
        logging.info("==========第二次获取数据**结束**==========")
        result_data3 = analysis_data(du_data + du_data2)
        logging.info("result_data3:%d" % len(result_data3))
        for i in range(0, len(result_data3), 1):
            print(result_data3[i])
        # # 向mongodb插入数据
        # if len(result_data3) > 0:
        #     save(result_data3)
    test = pd.DataFrame(data=result_data3)
    test.to_csv('./rest.csv')
    logging.info("程序运行完成")