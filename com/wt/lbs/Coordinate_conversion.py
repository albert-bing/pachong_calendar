# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')

import xlrd
import xlwt
import faker
import requests
import urllib3
import json
import time
# 忽略https的安全警告
urllib3.disable_warnings()

def read_xlsx():
    sb = xlrd.open_workbook('E:\项目文件\C490\\1109数据核对\online_data_pre400.xlsx')
    sheet = sb.sheets()[1]
    list_all = []
    for ss in range(0, sheet.nrows):
        cells = sheet.row_values(ss)
        # data = cells[0]
        # list = data.replace('[', '').replace(']', '').replace('"', '').split(",")
        tup = [cells[0], cells[5]]
        # print(tup)
        list_all.append(tup)
    return list_all

def get_new_position(list_all):
    list_all_res = []
    for i in range(0,len(list_all),1):
        tmp_list = []
        tmp_list.append(list_all[i][0])
        time.sleep(0.2)
        lng = list_all[i][1].split(",")[0]
        lat = list_all[i][1].split(",")[1]
        ll = lat+","+ lng
        # print(ll)
        url = "https://apis.map.qq.com/ws/coord/v1/translate?locations="+ll+"&type=3&key=ITUBZ-XDCL6-GFRSL-MB6MR-SP2Y6-KBFG3"
        sub_data = requests.get(url=url, verify=False)
        try:
            ll_res = str(json.loads(sub_data.text)['locations'][0]['lng'])+","+str(json.loads(sub_data.text)['locations'][0]['lat'])
            tmp_list.append(ll_res)
            list_all_res.append(tmp_list)
        except Exception:
            print(list_all[i][0])
            print(json.loads(sub_data.text))
    return list_all_res
        # print(sub_data.text)

def save(list_all_res):
    workbook = xlwt.Workbook()
    f = faker.Faker("zh_CN")
    sheet = workbook.add_sheet("rest", cell_overwrite_ok=True)
    sheet.write(0, 0, label="公司名称")
    sheet.write(0, 1, label="经纬度")
    for i in range(0, len(list_all_res)):
        try:
            sheet.write(i, 0,label=list_all_res[i][0])
        except Exception:
            pass
        try:
            sheet.write(i, 1,label=list_all_res[i][1])
        except Exception:
            pass

    workbook.save("E:\\项目文件\\C490\\1109数据核对\\tencent_rest.xlsx")


if __name__ == '__main__':
    list_all = read_xlsx()
    # print(list_all)
    list_all_res = get_new_position(list_all)
    print(list_all_res)

    save(list_all_res)