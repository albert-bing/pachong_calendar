# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code
import pymongo
import requests
import json
import time

def test(arr):
    result_data = []
    for i in range(0,len(arr),1):
        d = arr[i]
        if not d[11] or not d[10]:
            d[11] = ""
        try:
            re_data = '{"old_id":"'+d[0]+'","name":"'+d[1]+'","location":"'+d[2]+'","type":['+d[3]+'],"address":"'+d[4]+'","phone":"'+d[5]+'"' \
                  ',"postcode":"'+d[6]+'","pname":"'+d[7]+'","pcode":"'+d[8]+'","cityname":"'+d[9]+'","citycode":"'+d[10]+'"' \
                  ',"adname":"'+d[11]+'","adcode":"'+d[12]+'","email":"'+d[13]+'","salesPhoneNum":"'+d[14]+'","dealerAffiliation":"'+d[15]+'",' \
                  '"serviceHistoryID":"'+d[16]+'","saleshours":"'+d[17]+'","administrativeArea":"'+d[18]+'","eDaijiaCustomerID":"'+d[19]+'",' \
                  '"servicehours":"'+d[20]+'","primaryPhone":"'+d[21]+'","localcity":"'+d[22]+'","OSBDealerID":"'+d[23]+'","weiboURL":"'+d[24]+'"' \
                  ',"OSBPhone":"'+d[25]+'","servicePhoneNumber":"'+d[26]+'","dealerNewVehicle":"'+d[27]+'","eDaijiaPhone":"'+d[28]+'","weChatUrl":"'+d[29]+'"' \
                  ',"eDaijiaFlag":"'+d[30]+'","JVFlag":"'+d[31]+'","fax":"'+d[32]+'","createtime":"'+d[33]+'","updatetime":"'+d[34]+'","dealerId":"'+d[35]+'","_class":"'+d[36]+'"}'
            result_data.append(re_data)
        except TypeError as res:
            print(res)
        finally:
            pass

    print(result_data)
    print(len(result_data))


def test2():
    url = "https://restapi.amap.com/v3/geocode/geo?key=84b31c0b9ebe60f23788d6b6f0c96aa5&address=广西贵港市福瀚汽车销售服务有限公司"
    resource_data = requests.get(url=url, verify=False)
    data1 = json.loads(resource_data.text)
    one_data = []
    if [] == data1['geocodes'][0]['district']:
        one_data.append("")
    else:
        one_data.append(data1['geocodes'][0]['district'])

    print(one_data)

def test3():
    t_data = []
    str = '{"status":"1","info":"OK","infocode":"10000","count":"1","geocodes":[{"formatted_address":"广西壮族自治区贵港市","country":"中国","province":"广西壮族自治区","citycode":"1755","city":"贵港市","district":[],"township":[],"neighborhood":{"name":[],"type":[]},"building":{"name":[],"type":[]},"adcode":"450800","street":[],"number":[],"location":"109.598926,23.111530","level":"市"}]}&&A42641,,32700,,广西贵港市福瀚汽车销售服务有限公司,广西贵港福瀚,1010404.0,1.0104041E8,1.0101021E8,1.010102101E10,广西贵港市西环路与金港大道交汇处西南角金泰汽车城内,537100,0775-4596011,0775-4238889,N'
    str1 = '{"status":"1","info":"OK","infocode":"10000","count":"1","geocodes":[{"formatted_address":"广西壮族自治区贵港市","country":"中国","province":"广西壮族自治区","citycode":"1755","city":"贵港市","district":[],"township":[],"neighborhood":{"name":[],"type":[]},"building":{"name":[],"type":[]},"adcode":"450800","street":[],"number":[],"location":"109.598926,23.111530","level":"市"}]}&&A42641,,32700,,广西贵港市福瀚汽车销售服务有限公司,广西贵港福瀚,1010404.0,1.0104041E8,1.0101021E8,1.010102101E10,广西贵港市西环路与金港大道交汇处西南角金泰汽车城内,537100,0775-4596011,0775-4238889,N'
    t_data.append(str.split("&&")[1].split(","))
    t_data.append(str1.split("&&")[1].split(","))
    r_data = get_log_lat_baidu(t_data)
    return r_data

# 从百度地图获取经销商的数据
def get_log_lat_baidu(data):
    # 第一次获取百度要处理的数据
    du_data = []
    # 第二次获取到百度要处理的数据
    re_data = []
    # 第一次请求主要是获取到经纬度
    for k in range(0, len(data), 1):
        url = "http://api.map.baidu.com/geocoding/v3/?address=" + data[k][
            4] + "&ak=d0FaYLZV11VDUPifOWdSPsItnIvBkKeR&output=json"
        resource_data2 = requests.get(url=url, verify=False)
        du_data.append(resource_data2.text)
    # 第二次请求通过获取到的经纬度，再获取到具体的省市区县信息
    for h in range(0,len(du_data),1):
        one_d = json.loads(du_data[h])
        lng = one_d['result']['location']['lng']
        lat = one_d['result']['location']['lat']
        url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=d0FaYLZV11VDUPifOWdSPsItnIvBkKeR&output=json&coordtype=wgs84ll&location="+str(lat)+","+str(lng)
        resource_data = requests.get(url=url,verify=False)
        re_data.append(resource_data.text + "&&" + ",".join(data[h]))
    return re_data

def get_geo_data3(data):
    """:arg
        将从远程获取的经销商的信息和从高德获取的信息合并之后再次分开,其中list_data[0]表示高德获取的信息，list_data[1]表示远程文件获取的
    """
    list_data = data.split("&&")
    print(data)
    # 把从高德获取的信息转化为字典
    data1 = json.loads(list_data[0])
    # 把从远程文件获取的信息转化为数组
    data2 = list_data[1].split(",")
    # old_id、
    one_data = [""]
    # 添加 name、
    one_data.append(data2[4])
    # 添加location（经纬度）、
    lng = data1['result']['location']['lng']
    lat = data1['result']['location']['lat']
    one_data.append(str(lng)+","+str(lat))
    # 添加type为null、
    one_data.append("")
    # 添加address
    one_data.append(data2[10])
    # 添加phone exp:"销售:021-57432116;服务：021-62176667",
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 获取postcode、
    one_data.append(data2[11])
    # 获取省份
    one_data.append(data1['result']['addressComponent']['province'])
    # 获取省份编码
    p_code = data1['result']['addressComponent']['adcode']
    p_code = p_code[0:2] + "0000"
    one_data.append(p_code)
    # 获取城市名称
    one_data.append(data1['result']['addressComponent']['city'])
    # 获取城市编码
    c_code = data1['result']['addressComponent']['adcode']
    c_code = c_code[0:4] + "00"
    one_data.append(c_code)
    # 获取地区名称
    one_data.append(data1['result']['addressComponent']['district'])
    # 获取地区编码
    one_data.append(data1['result']['addressComponent']['adcode'])
    # 添加邮箱
    one_data.append("")
    # 添加销售电话 salesPhoneNum
    one_data.append(data2[13])
    # 添加 dealerAffiliation
    one_data.append("")
    # 添加 serviceHistoryID
    one_data.append("")
    # 添加 saleshours
    one_data.append("")
    # 添加 administrativeArea
    one_data.append("")
    # 添加 eDaijiaCustomerID
    one_data.append("")
    # 添加 servicehours
    one_data.append("")
    # 添加 primaryPhone
    one_data.append("销售：" + data2[13] + ";服务：" + data2[12])
    # 添加 localcity
    one_data.append(data1['result']['addressComponent']['city'])
    # 添加 OSBDealerID
    one_data.append(data2[0])
    # 添加 weiboURL
    one_data.append("")
    # 添加 OSBPhone 和 servicePhoneNumber
    if data2[13] != "":
        one_data.append(data2[13])
        one_data.append(data2[13])
    else:
        one_data.append(data2[12])
        one_data.append(data2[12])
    # 添加 dealerNewVehicle 、 eDaijiaPhone 、weChatUrl、eDaijiaFlag、JVFlag
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    one_data.append("")
    # 添加 fax
    one_data.append(data2[12])
    # 添加 createtime 、 updatetime
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    one_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 添加 dealerId
    one_data.append(data2[0])
    # 添加 _class
    one_data.append("")

    return one_data

if __name__ == '__main__':
    myclient = pymongo.MongoClient(host='localhost',port=27017)
    my_db = myclient.poi
    mycol = my_db.ford_website_sales1
    mycol.insert_one({"name":"zhangsan","age":18})

