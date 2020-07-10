# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/9 10:32
# @Author：albert·bing
# @File：date_constellation_info.py
# @Software：PyCharm


#  start your code

import requests
from bs4 import BeautifulSoup
import urllib3
from com.wt.common import MysqlUtil

# 忽略https的安全警告
urllib3.disable_warnings()


def get_source_data(url):
    file = requests.get(url=url, verify=False)
    soup = BeautifulSoup(file.text, 'html.parser')
    content = soup.find(name='div', attrs={'class', 'sContent'})

    list_data = []

    # 第一部分：日期范围和星座
    cons = soup.select('dt')[1].select('h2')[0].text
    date_ran = soup.select('dt')[1].select('strong')[0].text

    list_data.append(cons)
    list_data.append(date_ran)

    # 第二部分：详细的指标
    info2 = soup.find(name='ul', attrs={'class': 'liBasic'}).select('li')
    for num in range(0, len(info2), 1):
        li_data = ""
        li_txt = info2[num].text
        li_data = li_txt.split("：")[1]
        list_data.append(li_data)

    info3 = soup.find(name='ul', attrs={'class': 'liAdvan'}).select('li')
    for num in range(0, len(info3), 1):
        li_data = ""
        li_txt = info3[num].text
        li_data = li_txt.split("：")[1]
        list_data.append(li_data)

    # 第三部分：特点说明
    info4 = soup.find(name='div', attrs={'class': 'liAnalys'}).select('p')
    info5 = soup.find(name='div', attrs={'class': 'liAnalys'}).select('strong')

    for num in range(0, len(info4), 1):
        li_data = ""
        li_data = info4[num].text.replace(info5[num].text, "")
        list_data.append(li_data)
    return list_data


if __name__ == '__main__':
    month_list = [
        '063097095050109080', '063097095051109080', '063097095052109080', '063097095053109080',
        '063097095054109080', '063097095055109080', '063097095056109080', '063097095057109080',
        '063097095058109080', '063097095050062118059', '063097095050063118059', '063097095050064118059'
    ]
    for num in range(0, len(month_list), 1):
        url = f'https://www.xzw.com/cquery/view/{month_list[num]}.html'
        list_data = get_source_data(url)
        MysqlUtil.insert_data_constellation_detail_info(list_data)