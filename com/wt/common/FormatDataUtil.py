# -*- encoding:utf-8 -*-

# @Team：Big Data Group
# @Time：2020/7/8 17:12
# @Author：albert·bing
# @File：FormatDataUtil.py
# @Software：PyCharm


#  start your code

import requests
from bs4 import BeautifulSoup
import urllib3

# 忽略https的安全警告
urllib3.disable_warnings()


# 得到原市标签数据
def get_source_data(url, date_level):
    file = requests.get(url=url, verify=False)
    soup = BeautifulSoup(file.text, "html.parser")
    # 星座和日期
    info1 = soup.select('h4')[0]
    print(info1.text)
    info2_c = soup.select('li')
    # 运势和幸运指数
    info2 = []
    # 循环数量
    level_num = 0
    if date_level == 'week':
        level_num = 21
    elif date_level == 'month' or date_level == 'year':
        level_num = 18
    elif date_level == 'day':
        level_num = 22

    for num in range(12, level_num, 1):
        info2.append(info2_c[num])

    # print(info2)

    intro_c = soup.find(name="div", attrs={"class": "c_cont"})
    # print(intro_c)
    return info1, info2, intro_c


# 依据获取的源数据，需要提供三部分数据
# 清洗元数据
def format_data(data1, data2, data3, year, level):
    list_data = []
    # 第一部分：星座和日期的提取
    soup_data1 = BeautifulSoup(data1.text, "html.parser")
    constellation = soup_data1.text[0:3]
    # 切片末尾数
    slice_last_num = 0
    if level == 'year':
        slice_last_num = -11
    elif level == 'month' or level == 'week':
        slice_last_num = -8
    elif level == 'day':
        slice_last_num = -4
    today_date = year + '年' + soup_data1.text[slice_last_num:]
    list_data.append(constellation)
    list_data.append(today_date)

    # 第二部分：指数的数据获取

    for num in range(0, len(data2), 1):
        soup_data2 = BeautifulSoup(data2[num].text, "html.parser")
        w = soup_data2.select('em')
        res = data2[num].select('em')
        if res:
            star = str(int(int(res[0].get('style').split(':')[1].split('p')[0]) / 16))
            list_data.append(star)
        else:
            list_data.append(soup_data2.text.split('：')[1])

    # 第三部分：详细运势的描述数据获取
    span_datas = data3.find_all("span")
    for num in range(0, len(span_datas), 1):
        span_data = BeautifulSoup(span_datas[num].text, "html.parser")
        list_data.append(str(span_data))
    return list_data