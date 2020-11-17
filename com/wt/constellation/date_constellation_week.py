# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/8 16:16
# @Author：albert·bing
# @File：date_constellation_week.py
# @Software：PyCharm


#  start your code

from bs4 import BeautifulSoup
import urllib3
from com.wt.common import MysqlUtil
from com.wt.common import FormatDataUtil
import time
# 忽略https的安全警告
urllib3.disable_warnings()


if __name__ == '__main__':
    # 星座列表
    com_astro = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn',
                 'aquarius', 'pisces'];

    for num in range(0,len(com_astro),1):
        url = f"https://www.xzw.com/fortune/{com_astro[num]}/2.html"
        d1, d2, d3 = FormatDataUtil.get_source_data(url, 'week')
        year = time.strftime("%Y", time.localtime())
        result_data = FormatDataUtil.format_data(d1, d2, d3, year,'week')
        result_data.append('week')
        # print(result_data)
        MysqlUtil.insert_data_cons_week(result_data)