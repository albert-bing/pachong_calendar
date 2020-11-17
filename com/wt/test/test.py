# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code

import paramiko
import time
from urllib.parse import quote

def test1 ():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("120.26.146.183", "6143", "czsqauser", "#UIOP2wsxcde45", timeout=5)
    sftp_client = client.open_sftp()
    print(sftp_client.listdir('./fm02'))
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

    for i in range(0, 20):
        print(data[i])

if __name__ == '__main__':
    # print(time.strftime('%Y%m%d', time.localtime(time.time())))
    #
    # pro_text = quote("北京")
    # print(pro_text)
    list1 = []
    list1.append([1,2,3])
    print(list1)
