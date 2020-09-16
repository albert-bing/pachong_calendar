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
    # 首先要删除上一个备份的集合
    my_cols = my_db.list_collection_names()
    if "ford_website_sales_bak_last" in my_cols:
        # 删除集合
        my_db.ford_website_sales2.drop()
        print("文件已删除！")
    # 将现在的文件备份
    my_db["ford_website_sales"].rename("ford_website_sales_bak_last")
    print("文件备份已完成！")
    # 生成新的文件
    mycol = my_db.ford_website_sales
    for i in range(0, len(result_data), 1):
        mycol.insert_one(eval(result_data[i]))
    print("数据插入完成！！")