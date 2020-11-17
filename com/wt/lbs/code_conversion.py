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

from com.wt.common import MysqlUtil_localhost

# 忽略https的安全警告
urllib3.disable_warnings()


def read_xlsx():
    sb = xlrd.open_workbook('E:\\项目文件\C490\\1109数据核对\\online_data_pre400.xlsx')
    sheet = sb.sheets()[2]
    list_all_old = []
    for ss in range(0, sheet.nrows):
        cells = sheet.row_values(ss)
        tup = [cells[0], str(cells[1]).split(".")[0], cells[2], str(cells[3]).split(".")[0], cells[4], str(cells[5]).split(".")[0]]
        # print(tup)
        list_all_old.append(tup)

    list_all_new = []
    for ss in range(0, sheet.nrows):
        cells = sheet.row_values(ss)
        tup = [cells[7], cells[8], cells[9]]
        list_all_new.append(tup)

    return list_all_old, list_all_new


def save(list_all_old, list_all_new):
    res_list = []
    for i in range(0,len(list_all_new),1):
        time.sleep(0.05)
        sub_list = []
        if list_all_old[i][2] == 'test' or list_all_old[i][4] == 'test' or list_all_new[i][1] == 'test' or list_all_new[i][2] == 'test':
            print(list_all_old[i])
            res_list.append(sub_list)
        else:
            # 省份相同
            if(list_all_old[i][0] == list_all_new[i][0]):
                # 城市相同
                if list_all_old[i][2] == list_all_new[i][1]:
                    # 区县相同
                    if list_all_old[i][4] == list_all_new[i][2]:
                        # 依次追加 省份、省份id，城市、城市id、区县和区县id
                        sub_list.append(list_all_old[i][0])
                        sub_list.append(list_all_old[i][1])
                        sub_list.append(list_all_old[i][2])
                        sub_list.append(list_all_old[i][3])
                        sub_list.append(list_all_old[i][4])
                        sub_list.append(list_all_old[i][5])
                        res_list.append(sub_list)
                    else:
                        res1 = MysqlUtil_localhost.select_data_1(str(list_all_new[i][1]),str(list_all_new[i][2]))
                        # 判断是否区县不存在
                        if res1 == None:
                            print("p:73")
                            print(list_all_old[i])
                        else:
                            # 依次追加 省份、省份id，城市、城市id、区县和区县id
                            sub_list.append(list_all_old[i][0])
                            sub_list.append(list_all_old[i][1])
                            sub_list.append(list_all_old[i][2])
                            sub_list.append(list_all_old[i][3])
                            sub_list.append(list_all_new[i][2])
                            sub_list.append(res1[0])
                            res_list.append(sub_list)
                #  城市不同、区县肯定也不同
                else:
                    res2 = MysqlUtil_localhost.select_data_2(str(list_all_new[i][1]))
                    res3 = MysqlUtil_localhost.select_data_1(str(list_all_new[i][1]),str(list_all_new[i][2]))
                    # 判断是否区县不存在
                    if res2 == None:
                        print("p:90")
                        print(list_all_old[i])
                    else:
                        pass
                    if res3 == None:
                        print("p:95")
                        print(list_all_old[i])
                    else:
                        # 依次追加 省份、省份id，城市、城市id、区县和区县id
                        sub_list.append(list_all_old[i][0])
                        sub_list.append(list_all_old[i][1])
                        sub_list.append(list_all_new[i][1])
                        sub_list.append(res2[0])
                        sub_list.append(list_all_new[i][2])
                        sub_list.append(res3[0])
                        res_list.append(sub_list)
            # 省份不同，市区县肯定也不同
            else:
                # 省份
                res4 = MysqlUtil_localhost.select_data_3(str(list_all_new[i][0]))
                # 城市
                res2 = MysqlUtil_localhost.select_data_2(str(list_all_new[i][1]))
                # 区县
                res3 = MysqlUtil_localhost.select_data_1(str(list_all_old[i][3]), str(list_all_new[i][2]))
                # 判断是否区县不存在
                if res2 == None:
                    print("p:116")
                    print(list_all_old[i])
                else:
                    pass
                if res3 == None:
                    print("p:121")
                    print(list_all_old[i])
                else:
                    # 依次追加 省份、省份id，城市、城市id、区县和区县id
                    sub_list.append(list_all_new[i][0])
                    sub_list.append(res4[0])
                    sub_list.append(list_all_new[i][1])
                    sub_list.append(res2[0])
                    sub_list.append(list_all_new[i][2])
                    sub_list.append(res1[0])
                    res_list.append(sub_list)
    return res_list

def save_xlxs(res_list):
    workbook = xlwt.Workbook()
    f = faker.Faker("zh_CN")
    sheet = workbook.add_sheet("rest", cell_overwrite_ok=True)
    sheet.write(0, 0, label="省份")
    sheet.write(0, 1, label="省份id")
    sheet.write(0, 2, label="城市")
    sheet.write(0, 3, label="城市id")
    sheet.write(0, 4, label="地区")
    sheet.write(0, 5, label="地区id")
    for i in range(0, len(res_list)):
        time.sleep(0.05)
        try:
            sheet.write(i, 0, label=res_list[i][0])
        except Exception:
            pass
        try:
            sheet.write(i, 1, label=res_list[i][1])
        except Exception:
            pass
        try:
            sheet.write(i, 2, label=res_list[i][2])
        except Exception:
            pass
        try:
            sheet.write(i, 3, label=res_list[i][3])
        except Exception:
            pass
        try:
            sheet.write(i, 4, label=res_list[i][4])
        except Exception:
            pass
        try:
            sheet.write(i, 5, label=res_list[i][5])
        except Exception:
            pass

    workbook.save("E:\\项目文件\\C490\\1109数据核对\\tencent_rest22.xlsx")


if __name__ == '__main__':
    list_all_old, list_all_new = read_xlsx()
    res_list = save(list_all_old, list_all_new)
    save_xlxs(res_list)