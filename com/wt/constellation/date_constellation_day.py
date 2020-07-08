# @Team：Big Data Group
# @Time：2020/7/7 10:05
# @Author：albert·bing
# @File：date_constellation_day.py
# @Software：PyCharm


#  start your code

import requests
import time
from bs4 import BeautifulSoup
import urllib3
from com.wt.common import MysqlUtil
from com.wt.common import FormatDataUtil

# 忽略https的安全警告
urllib3.disable_warnings()


def save_data(url):
    # 获取元数据
    d1, d2, d3 = FormatDataUtil.get_source_data(url,'day')
    # d1, d2, d3 = get_source_data(url)
    # 获取整理后的数据
    year = time.strftime("%Y",time.localtime())
    result_data = FormatDataUtil.format_data(d1, d2, d3, year,'day')
    MysqlUtil.insert_data_cons_day(result_data)


if __name__ == '__main__':
    # 星座列表
    com_astro = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn',
                 'aquarius', 'pisces'];

    for num in range(0,len(com_astro),1):
        # 今日运势
        # url = f"https://www.xzw.com/fortune/{com_astro[num]}/"
        # 明日运势
        url = f"https://www.xzw.com/fortune/{com_astro[num]}/1.html"
        save_data(url)