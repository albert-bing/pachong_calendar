# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code
import datetime
import time
from urllib.parse import quote
if __name__ == '__main__':
    url = "https://ncov.html5.qq.com/api/getNewestCommunityNew?&province="
    ll = url+quote("山西省")
    print(ll)