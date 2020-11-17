# -*- encoding:utf-8 -*-
# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：yellow_calendar.py
# 开发工具：PyCharm


#  start your code

# import sys
# sys.path.append('/home/hadoop/programs/spider/WTP66_BigdataCrawler')
import urllib
from urllib.parse import quote
import requests
import json
import pandas as pd
import urllib3
from com.wt.common import MysqlUtil
# 忽略https的安全警告
urllib3.disable_warnings()


# 获取ford的市区信息
def get_lbs_new():
    url = "https://www.ford.com.cn/content/ford/cn/zh_cn/configuration/application-and-services-config/provinceCityDropDowns.multiFieldDropdownChina.data"
    resource_data = requests.get(url=url, verify=False)
    dick_data = json.loads(resource_data.text)
    for j in range(len(dick_data)):
        for i in range(0,len(dick_data[j]['cityList']),1):
            print(dick_data[j]['cityList'][i]['cityValue'])


def get_headers():
    url = "https://www.ford.com.cn/locate-a-dealer/"
    file = urllib.request.urlopen(url)
    # print('获取当前url:',file.geturl() )
    # print('file.getcode,HTTPResponse类型:',file.getcode )
    # print('file.info 返回当前环境相关的信息：' ,file.info())
    print(file.headers)


# 获取到每一个城市对应的区域的经纬度 lng 和 lat
def get_lbs():
    # 获取所有要查询的市、区
    result = MysqlUtil.select_area()
    data = pd.DataFrame(result)
    # print(data[0][0])
    url = "https://restapi.amap.com/v3/geocode/geo?key=84b31c0b9ebe60f23788d6b6f0c96aa5&address="
    city_location = []
    for i in range(len(data[0])):
        # 拼接上市区
        new_url = url + data[0][i]
        # 获取内容
        req = requests.get(url=new_url, verify=False)
        str = req.text
        # 将内容转化为字典形式
        dick_data = json.loads(str)
        print(dick_data)
        # 过滤只有是市、区的数据
        if dick_data['count'] == '1' and (
                dick_data['geocodes'][0]['level'] == '市' or dick_data['geocodes'][0]['level'] == '区县'):
            city_location.append(dick_data)
    # print(dick_data['geocodes'][0]['location'])
    return city_location

# 获取经销商的信息
def get_dealers(j_data):
    re_data = []
    headers = {
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkVoWUZnbTkxTW5faVIzdlI2ei1DbkNKNjJTdyIsImtpZCI6IkVoWUZnbTkxTW5faVIzdlI2ei1DbkNKNjJTdyJ9.eyJhdWQiOiJmMmQzNWM4OC0zMzFjLTQ2MGUtODQ2Ny0zNmFmMGRmYzUwY2IiLCJpc3MiOiJodHRwczovL3N0cy5jaGluYWNsb3VkYXBpLmNuLzM5NTMzOTZjLTgxNGMtNGRiZS1iNTQzLWFlNDk5OTk3ODIwNi8iLCJpYXQiOjE2MDA4NjQ1NDYsIm5iZiI6MTYwMDg2NDU0NiwiZXhwIjoxNjAwODY4NDQ2LCJhaW8iOiI0MkJnWU9DNTExTmE2ZnAzOCtQMGF5bFpwblpPQUE9PSIsImFwcGlkIjoiYTdmODFkMGEtNzU3ZS00NzIzLWIzZGItMDk2MDYwMTAxNWRiIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMuY2hpbmFjbG91ZGFwaS5jbi8zOTUzMzk2Yy04MTRjLTRkYmUtYjU0My1hZTQ5OTk5NzgyMDYvIiwib2lkIjoiNDkxYWJkNzAtZGQxNy00N2JmLTlkZWEtNWQ3MWY4OTA3MzYyIiwicmgiOiIwLkFBQUFiRGxUT1V5QnZrMjFRNjVKbVplQ0Jnb2QtS2QtZFNOSHM5c0pZR0FRRmRzQkFBQS4iLCJyb2xlcyI6WyJMZWFkcy5BcHAuV3JpdGUiLCJVc2VyVmVoaWNsZS5BcHAuQ29uc3VtZXIiLCJTaG9wLkFwcC5Db25zdW1lciIsIkFjY291bnQuQXBwLkNvbnN1bWVyIiwiVXRpbC5BcHAuQ29uc3VtZXIiXSwic3ViIjoiNDkxYWJkNzAtZGQxNy00N2JmLTlkZWEtNWQ3MWY4OTA3MzYyIiwidGlkIjoiMzk1MzM5NmMtODE0Yy00ZGJlLWI1NDMtYWU0OTk5OTc4MjA2IiwidXRpIjoiNFV3TTVyY2REVUdvLXlvUHhKWVhBQSIsInZlciI6IjEuMCJ9.kWz2jEPt7_V9Ob1XOpXLbOxi3xWycz-x4dyE_buc-73HaXtRnYXm2nLXtbQbBb87Y1lqvbjLIKgvPckUnpafXPQP6PNURz0EyHlNFh_toXhoFAzw0ontnosKrjxWgmL1NDpD9quNgxm1cNwrNiVqly-LV8TkOjSBJsv4YswGfEjRX4fUSrg5loumqjleHuIs9iho9qOF_I-47_1rVzSGuuWpJrNgIee_QksbcgfgkjMFB63YQBcODNlGRjuwMWUeglgR34mbjbFE6c46j4zameZ59W-oYXj6yJUnXSSUTM7dozNyw4EoWKc9NOCoeOaLdINNDcdabKnh0EqWW3QaIw',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'origin': 'https://www.ford.com.cn',
        'application-id': '05F9DDAA-6C8F-48FB-A7A2-475D2C585900',
        'Referer': 'https://www.ford.com.cn/locate-a-dealer/'}
    # print(j_data[0]['cityList'][0]['cityKey'])
    for i in range(0,len(j_data),1):
        for j in range(0,len(j_data[i]['cityList']),1):
            print(j_data[i]['cityList'][j]['cityKey'])
            city = j_data[i]['cityList'][j]['cityKey']
            city_code =  quote(city)
            url = 'https://cn.api.mps.ford.com.cn/api/dsl/utility/v1/dealer/ford/local?center=116.4133836971231,39.910924547299565&city='+city_code
            resource_data = requests.get(url=url, headers=headers)
            dict_data = json.loads(resource_data.text)
            for h in range(0,len(dict_data['datas']),1):
                re_data.append(dict_data['datas'][h])
    return re_data

def json_data():
    with open('./ford_cities.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    return json_data


if __name__ == '__main__':

    j_data = json_data()
    dict_data = get_dealers(j_data)

    print(len(dict_data))
    print(dict_data)