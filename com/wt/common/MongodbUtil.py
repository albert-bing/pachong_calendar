# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

import pymongo


# 将数据插入到mongodb中
def isnert_data_ford(result_data):
    myclient = pymongo.MongoClient('mongodb://root:autopai123@172.27.0.12:27017/poi?authSource=admin')
    dblist = myclient['poi']
    mycol = dblist['ford_website_sales']
    for i in range(0, len(result_data), 1):
        mycol.insert_one(eval(result_data[i]))
