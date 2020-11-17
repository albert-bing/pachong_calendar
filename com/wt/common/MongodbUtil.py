# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code
import logging
import pymongo
from pymongo import GEO2D
# 正式
host = '62.234.72.139'
username = 'admin'
passwd = 'Autopai2018'

# 测试
host1 = '132.232.207.113'
username1 = 'root'
passwd1 = 'autopai123'

# 更新数据
def update_data_ford(result_data):
    logging.info("数据开始更新.....")
    myclient = pymongo.MongoClient(host='129.28.93.48', port=27017)
    db = myclient.admin
    db.authenticate("root", "autopai123")
    my_db = myclient.poi
    mycol = my_db.ford_website_sales
    for i in range(0, len(result_data), 1):
        mycol.insert_one(eval(result_data[i]))
    mycol.create_index([("location", GEO2D)], name='location')
    logging.info("数据更新完成！！")


def save_data_ford(result_data):
    logging.info("数据开始更新.....")
    myclient = pymongo.MongoClient(host=host1, port=27017)
    db = myclient.admin
    db.authenticate(username1,passwd1)
    my_db = myclient.poi
    mycol = my_db.ford_website_sales
    for i in range(0, len(result_data), 1):
        mycol.insert_one(eval(result_data[i]))
    mycol.create_index([("location", GEO2D)], name='location')
    logging.info("数据更新完成！！")


# 移除消失的经销商
def remove_fords_data(data):
    logging.info("数据开始移除.....")
    myclient = pymongo.MongoClient(host='129.28.93.48', port=27017)
    db = myclient.admin
    db.authenticate("root", "autopai123")
    my_db = myclient.poi
    mycol = my_db.ford_website_sales
    for i in range(0, len(data), 1):
        mycol.delete_one({'name': data[i]['name']})
    logging.info("数据移除完成！！")


# 查询所有已存好的数据
def select_fords_all():
    myclient = pymongo.MongoClient(host='62.234.72.139', port=27017)
    db = myclient.admin
    db.authenticate("admin", "Autopai2018")
    my_db = myclient.poi
    mycol = my_db.ford_website_sales
    data_all = mycol.find()
    count = mycol.count()
    return data_all, count
