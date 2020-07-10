# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code
import requests
import json
import re
import time

from com.wt.common import MysqlUtil


# 爬去一天的数据
def get_data_day(url):
    data = requests.get(url=url, verify=False)
    if data.status_code == 404:
        print(url)
        return "no"
    str = data.text
    res = str.replace("day", '"day"').replace("html", '"html"').replace("gongli", '"gongli"').replace("nongli",
                                                                                                      '"nongli"'). \
        replace("start", '"start"').replace("jiri", '"jiri"').replace("suici", '"suici"').replace("wuxing", '"wuxing"'). \
        replace("cai", '"cai"').replace("xi", '"xi"').replace("fu", '"fu"').replace("yi", '"yi"').replace("ji", '"ji"'). \
        replace("chong", '"chong"').replace("dao", '"dao"').replace('"ji"ri', 'jiri').replace('wu"xi"ng', 'wuxing'). \
        replace("\\", '')

    # 将json转化为字典
    # ss = dict(json_data)

    # 使用正则表达式去掉html标签
    re_h = re.compile('</?\w+[^>]*>')
    res = re_h.sub('', res)

    # 转化为字典
    dick_data = json.loads(res)
    gongli = dick_data['html']['gongli'].split(" ")
    dick_data['html']['gongli'] = gongli[0]
    dick_data['html']['constellation'] = gongli[1]

    nongli = dick_data['html']['nongli'].split(" ")
    dick_data['html']['nongli'] = nongli[0]
    dick_data['html']['chinese_zodiac'] = nongli[1]

    dick_data['html']['chong'] = dick_data['html']['chong'].replace('&nbsp;', ' ')
    # 将字典转化为json
    # json_data = json.dumps(dick_data)
    # print(dick_data['html']['nongli'])
    return dick_data
    # print(dick_data)


# 累加一个月的数据
def get_month_data(month_days_n, month, y_date):
    month_data = []
    for num in range(1, int(month_days_n) + 1, 1):
        if num < 10:
            d_date = y_date + '0' + str(num)
        else:
            d_date = y_date + str(num)
        day_tup = ()
        if d_date == '20200305' or d_date == '20190110':
            continue
        url = f"http://www.nongli.cn/rili/api/app/god/{y_date[0:4]}/{month}/{d_date}.js"
        print(f"获取{d_date}的数据 start")
        day_data = get_data_day(url)
        if day_data == "no":
            continue
        print(f"获取{d_date}的数据 end")
        # 将数据加入元组
        day_tup += (
            day_data['day'], day_data['html']['gongli'], day_data['html']['nongli'], day_data['html']['dao'], \
            day_data['html']['start'], day_data['html']['yi'], day_data['html']['ji'], day_data['html']['chong'], \
            day_data['html']['suici'], day_data['html']['wuxing'], day_data['html']['cai'], day_data['html']['xi'], \
            day_data['html']['fu'],day_data['html']['constellation'],day_data['html']['chinese_zodiac'])
        month_data.append(day_tup)
        # print("day", day_data)
        # print("-" * 60)
    return month_data


# 爬取一年，每月插入
def month_data_insert_for_one_year(year_num, fe_num):
    # 循环一年的月份，左闭右开
    for month_num in range(1, 13, 1):
        month_days_30 = 30
        month_days_31 = 31
        # 二月的天数
        month_days_Fe = fe_num
        # 对于 1-9 月做处理
        if month_num < 10:
            year = year_num + '0' + str(month_num)
            str_month = '0' + str(month_num)
        else:
            year = year_num + str(month_num)
            str_month = str(month_num)
        # 对大月还是小月做处理
        if month_num == 4 or month_num == 6 or month_num == 9 or month_num == 11:
            mdata = get_month_data(month_days_30, str_month, year)
        elif month_num == 2:
            mdata = get_month_data(month_days_Fe, str_month, year)
        else:
            mdata = get_month_data(month_days_31, str_month, year)
        # 插入数据库 一个月插入一次
        MysqlUtil.insert_data_yellow_calendar(mdata)
        print("行号【97】"+year + " " + str_month + "数据插入成功！")
        # 暂停2秒
        time.sleep(2)
        # 变量清空
        year = ""
        str_month = ""


def get_years_data(start_year, end_year):
    # 按输入的开始年份和结束年份遍历
    for year_num in range(start_year, end_year + 1, 1):
        # 闰年
        if (year_num % 4 == 0 and year_num % 100 != 0) or (year_num % 400 == 0):
            month_data_insert_for_one_year(str(year_num), 29)
        # 平年
        else:
            month_data_insert_for_one_year(str(year_num), 28)


if __name__ == '__main__':
    # 按年插入
    # month_data_insert_for_one_year('2020', 29)

    # 按年的时间段插入
    # get_years_data(2019, 2020)

    # 按月插入的代码测试
    days = 31
    str1 = '12'
    str2 = '201012'
    m_data = get_month_data(days,str1,str2)
    print(m_data)
    MysqlUtil.insert_data_yellow_calendar(m_data)
