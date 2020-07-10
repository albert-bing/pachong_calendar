# @Team：Big Data Group
# @Time：2020/7/6 16:10
# @Author：albert·bing
# @File：MysqlUtil.py
# @Software：PyCharm


#  start your code

import pymysql


# 黄历数据入库
def insert_data_yellow_calendar(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    # sql = "select * from car_param_info limit 10;"
    sql = 'insert into date_yellow_calendar(`y_day`,`gregorian_calendar`,`lunar_calendar`,`dao`,`start`,`yi`,`ji`,`chong`,\
    `suici`,`wuxing`,`cai`,`xi`,`fu`,`constellation`,`chinese_zodiac`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.executemany(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")


# 星座日数据入库
def insert_data_cons_day(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    sql = 'insert into date_constellation_info_day(`constellation`,`con_date`,`com_fortune_index`,`love_fortune_index`,' \
          '`career_index`,`wealth_index`,`health_index`,`negotiation_index`,`lucky_color`,`lucky_number`,' \
          '`speed_dating_constellation`,`short_comment`,`com_fortune`,`love_fortune`,`career_fortune`,`wealth_fortune`,' \
          '`health_fortune`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")


# 星座周数据入库
def insert_data_cons_week(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    sql = 'insert into date_constellation_info_wmy(`constellation`,`con_date`,`com_fortune_index`,`love_fortune_index`,' \
          '`career_index`,`wealth_index`,`health_index`,`lucky_color`,`lucky_constellation`,' \
          '`beware_constellation`,`short_comment`,`com_fortune`,`love_fortune`,`career_fortune`,`wealth_fortune`,' \
          '`health_fortune`,`date_level`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")


# 星座月数据入库
def insert_data_cons_month(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    sql = 'insert into date_constellation_info_wmy(`constellation`,`con_date`,`com_fortune_index`,`love_fortune_index`,' \
          '`career_index`,`wealth_index`,`health_index`,`short_comment`,`com_fortune`,`love_fortune`,`career_fortune`,' \
          '`wealth_fortune`,`health_fortune`,`reduced_pressure`,`get_luck_way`,`date_level`) values (%s,%s,%s,%s,%s,' \
          '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")


# 星座年数据入库
def insert_data_cons_year(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    sql = 'insert into date_constellation_info_wmy(`constellation`,`con_date`,`com_fortune_index`,`love_fortune_index`,' \
          '`career_index`,`wealth_index`,`health_index`,`short_comment`,`com_fortune`,`love_fortune`,`career_fortune`,' \
          '`wealth_fortune`,`health_fortune`,`get_luck_way`,`date_level`) values (%s,%s,%s,%s,%s,' \
          '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")


# 星座详情码表入库
def insert_data_constellation_detail_info(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    sql = 'insert into date_constellation_detail_info(`constellation`,`date_range`,`cons_features`,`four_image_attributes`,' \
          '`palace`,`yin_yang_attributes`,`biggest_features`,`supervisor_plant`,`lucky_color`,`auspicious_items`,`lucky_number`,' \
          '`lucky_metal`,`performance`,`advantage`,`disadvantage`,`basic_traits`,`specific_traits`,`acting_style`,`blind_spot`,' \
          '`summary`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")


def insert_data_calendar(data):
    db = pymysql.connect(host='152.136.108.36', user='root', password='wutong123', port=3306, db='traffic')
    cursor = db.cursor()
    sql = 'insert into date_calendar(`y_date`,`lunar`,`week`,`solar_terms`,`gregorian_calendar`) values (%s,%s,%s,%s,%s);'
    cursor.executemany(sql, data)
    cursor.close()
    db.commit()
    db.close()
    print("mysql-插入成功！\n")
