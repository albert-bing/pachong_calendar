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
    # myclient = pymongo.MongoClient(host='129.28.93.48', port=27017)
    # db = myclient.admin
    # db.authenticate("root", "autopai123")
    # my_db = myclient.poi
    # mycol = my_db.ford_website_sales
    print("数据开始插入......")
    myclient = pymongo.MongoClient(host='129.28.93.48', port=27017)
    db = myclient.admin
    db.authenticate("root", "autopai123")
    my_db = myclient.poi
    mycol = my_db.ford_website_sales
    for i in range(0, len(result_data), 1):
        mycol.insert_one(eval(result_data[i]))
    print("数据插入完成！！")