# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')

import pymysql


host = 'localhost'
password = '123456'
port = 3306

def select_data_1(str1,str2):
    db = pymysql.connect(host=host, user='root', password=password, port=port, db='mytest')
    cursor = db.cursor()
    sql = "SELECT area_id from area_code where city_name = '"+str1+"' and area_name = '"+str2+"';"
    # print(sql)
    # sql = 'insert into date_yellow_calendar(`y_day`,`gregorian_calendar`,`lunar_calendar`,`dao`,`start`,`yi`,`ji`,`chong`,\
    # `suici`,`wuxing`,`cai`,`xi`,`fu`,`constellation`,`chinese_zodiac`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql)
    record = cursor.fetchone()
    cursor.close()
    db.commit()
    db.close()
    print("mysql-查询成功！\n")
    return record

def select_data_2(str2):
    db = pymysql.connect(host=host, user='root', password=password, port=port, db='mytest')
    cursor = db.cursor()
    sql = "SELECT city_id from area_code where  city_name = '"+str2+"';"
    # print(sql)
    # sql = 'insert into date_yellow_calendar(`y_day`,`gregorian_calendar`,`lunar_calendar`,`dao`,`start`,`yi`,`ji`,`chong`,\
    # `suici`,`wuxing`,`cai`,`xi`,`fu`,`constellation`,`chinese_zodiac`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql)
    record = cursor.fetchone()
    cursor.close()
    db.commit()
    db.close()
    print("mysql-查询成功！\n")
    return record

def select_data_3(str2):
    db = pymysql.connect(host=host, user='root', password=password, port=port, db='mytest')
    cursor = db.cursor()
    sql = "SELECT province_id from area_code where province_name = '"+str2+"';"
    # sql = 'insert into date_yellow_calendar(`y_day`,`gregorian_calendar`,`lunar_calendar`,`dao`,`start`,`yi`,`ji`,`chong`,\
    # `suici`,`wuxing`,`cai`,`xi`,`fu`,`constellation`,`chinese_zodiac`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql)
    record = cursor.fetchone()
    cursor.close()
    db.commit()
    db.close()
    print("mysql-查询成功！\n")
    return record