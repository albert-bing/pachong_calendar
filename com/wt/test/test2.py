# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code

import paramiko
import time
import os
import pandas as pd
def test1 ():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 测试
    # client.connect("120.26.146.183", "6143", "czsqauser", "#UIOP2wsxcde45", timeout=5)
    # 正式
    client.connect("47.96.21.66", "6143", "cz_proftp", "#DFGcvbhu87ytr", timeout=5)
    sftp_client = client.open_sftp()
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

    test = pd.DataFrame(data=data)
    test.to_csv('./pro_score.xlsx.csv')

def test2():
    data = open("./get_baidu_info.txt",'r',encoding='utf-8')
    output_excel = {'name': [], 'addr': [], 'lng_lat': [], 'provin': [],'city':[],'area':[],'phone':[]}
    name = []
    addr = []
    lng_lat = []
    provin = []
    city = []
    area = []
    phone = []
    i = 0
    while True:
        line = data.readline()
        if line != "":
            print(line)
            i = i +1
            print(i)
            one_da = line.replace('[',"").replace(']',"").split(",")
            print(one_da)
            name.append(one_da[1])
            addr.append(one_da[5])
            lng_lat.append(one_da[2]+','+one_da[3])
            provin.append(one_da[8])
            city.append(one_da[10])
            area.append(one_da[12])
            phone.append(one_da[6])
        else:
            break

    output_excel['name'] = name
    output_excel['addr'] = addr
    output_excel['lng_lat'] = lng_lat
    output_excel['provin'] = provin
    output_excel['city'] = city
    output_excel['area'] = area
    output_excel['phone'] = phone
    output = pd.DataFrame(output_excel)
    output.to_excel('dev_score.xlsx', index=False)

if __name__ == '__main__':
    print(time.strftime('%Y%m%d', time.localtime(time.time())))

    test1()
