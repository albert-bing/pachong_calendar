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
from pymongo import GEO2D
from geopy.distance import geodesic
from com.wt.common import MongodbUtil

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


    s = ['{"status":0,"result":{"location":{"lng":106.70793295538208,"lat":31.821236990377785},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":110.1406820448425,"lat":22.61478603599128},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":113.17892896341418,"lat":29.430779006603463},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":121.55822845288475,"lat":31.136241153904856},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":111.53112505040798,"lat":36.11551567610248},"precise":0,"confidence":80,"comprehension":6,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":110.96738496980528,"lat":21.619225969368697},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":121.62857249434141,"lat":29.866033045866055},"precise":0,"confidence":20,"comprehension":100,"level":"城市"}}', '{"status":0,"result":{"location":{"lng":111.38371599079824,"lat":30.67129589873593},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":109.55117803716931,"lat":23.113082989740005},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.59361234853988,"lat":35.420177394529648},"precise":0,"confidence":20,"comprehension":100,"level":"城市"}}', '{"status":0,"result":{"location":{"lng":117.23840643173311,"lat":37.73592450080975},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":117.18948103060713,"lat":36.67673091012701},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.00542541805672,"lat":36.65186219609679},"precise":0,"confidence":75,"comprehension":0,"level":"购物"}}', '{"status":0,"result":{"location":{"lng":118.1774894423699,"lat":36.19091698584845},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":119.90365112219743,"lat":37.1500790214469},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":120.44060165264568,"lat":37.36113714256612},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":122.3205540442564,"lat":43.64367312811889},"precise":1,"confidence":70,"comprehension":18,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":103.94828399141589,"lat":30.697459837239067},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":112.95444699790295,"lat":28.14631401217038},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":113.73572110078048,"lat":34.053257706517708},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":106.70793295538208,"lat":31.821236990377785},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":112.92405399878006,"lat":23.20463303902938},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":121.39201900956052,"lat":28.40821800556456},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":112.88778897058005,"lat":35.49908492155502},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.03089852744778,"lat":22.655981918507196},"precise":0,"confidence":75,"comprehension":0,"level":"购物"}}', '{"status":0,"result":{"location":{"lng":118.76579304458486,"lat":37.447279987002769},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.18691732114357,"lat":34.426972637748587},"precise":0,"confidence":75,"comprehension":100,"level":"宾馆"}}', '{"status":0,"result":{"location":{"lng":119.19289895693409,"lat":36.761069945581109},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":103.64346701322595,"lat":36.143218927376469},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.3758009664879,"lat":30.601906854168015},"precise":0,"confidence":50,"comprehension":100,"level":"NoClass"}}', '{"status":0,"result":{"location":{"lng":116.02751800260089,"lat":36.430013937036267},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.41457869478904,"lat":40.051508786394858},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":117.14228756250437,"lat":39.22902269084472},"precise":0,"confidence":50,"comprehension":0,"level":"NoClass"}}', '{"status":0,"result":{"location":{"lng":121.15696596447246,"lat":28.826294016017888},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.41124997347134,"lat":27.849739027574644},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":113.58693303777283,"lat":24.73902202572107},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":124.07025203737757,"lat":47.350189511590198},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.14228756250437,"lat":39.22902269084472},"precise":0,"confidence":50,"comprehension":0,"level":"NoClass"}}', '{"status":0,"result":{"location":{"lng":120.43581997241607,"lat":41.542713901506157},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.1146014455186,"lat":39.00018011949929},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":120.42127200451252,"lat":36.409167864349978},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.22593302872829,"lat":40.22157902612984},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.97879802579105,"lat":35.44512290968728},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.49108401597485,"lat":36.57384693144587},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.1724489811672,"lat":23.30363452186039},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":117.14228756250437,"lat":39.22902269084472},"precise":0,"confidence":50,"comprehension":0,"level":"NoClass"}}', '{"status":0,"result":{"location":{"lng":116.24285674521406,"lat":37.689390588685707},"precise":0,"confidence":80,"comprehension":24,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":119.83160603216115,"lat":31.342956624267875},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":114.70424318495056,"lat":23.739624177535324},"precise":0,"confidence":50,"comprehension":0,"level":"村庄"}}', '{"status":0,"result":{"location":{"lng":112.34244242768281,"lat":37.36413128347519},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":119.19146705795117,"lat":32.27809048316069},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":115.76717199800457,"lat":33.837138085612},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":106.28576097384864,"lat":29.9605609426507},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.24285674521406,"lat":37.689390588685707},"precise":0,"confidence":80,"comprehension":3,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":117.9057510374655,"lat":30.942732876721057},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":118.0774094949949,"lat":34.86361638543997},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":113.45473103286297,"lat":22.53644601338965},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":120.5301960391249,"lat":31.29604884935482},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":120.05468698372713,"lat":29.36640104654285},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.37778715533908,"lat":40.63949807870581},"precise":0,"confidence":50,"comprehension":0,"level":"村庄"}}', '{"status":0,"result":{"location":{"lng":119.22330947302447,"lat":34.27706452168103},"precise":0,"confidence":80,"comprehension":10,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":117.18062113319276,"lat":36.98397051831499},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":118.79401196472255,"lat":32.97369514060615},"precise":0,"confidence":70,"comprehension":0,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":118.42146012978772,"lat":29.866287675757314},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":116.7901151517282,"lat":35.557952373283438},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":117.64654058086437,"lat":35.51201963664022},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":113.38960596405809,"lat":33.73845910778366},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":121.16779604264146,"lat":32.298883078436919},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.04542103359967,"lat":36.16453189371488},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":113.35788300908375,"lat":23.186875976043006},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":119.74746382114418,"lat":31.65540505481647},"precise":0,"confidence":50,"comprehension":0,"level":"村庄"}}', '{"status":0,"result":{"location":{"lng":114.89258615518705,"lat":33.737347183458407},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":115.31989212017335,"lat":33.02594877010587},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":118.13782995663594,"lat":24.53406903713055},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":104.31551019438138,"lat":24.89051972489473},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":111.10384854984238,"lat":37.50566935643673},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.37371109408756,"lat":39.165839105489627},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.45315099971335,"lat":37.10589896228625},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":109.46544098782633,"lat":34.52184001455495},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":106.65413397737281,"lat":30.495814933328377},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":93.58368163934625,"lat":42.88290927074924},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":118.74066034285724,"lat":32.071267015593289},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":112.82933497341807,"lat":35.48492590303196},"precise":1,"confidence":70,"comprehension":3,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":121.3506708640397,"lat":31.18127293063938},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":120.92460803260795,"lat":30.86216683758359},"precise":1,"confidence":80,"comprehension":100,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":110.52988296793359,"lat":29.123366000724869},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":118.07039040523159,"lat":36.81820603446294},"precise":0,"confidence":80,"comprehension":0,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":119.50895301840947,"lat":39.929681055166877},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":119.6935070108568,"lat":30.213662738789944},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":116.4354989906427,"lat":39.136970103425358},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":120.17485336206231,"lat":22.99280495989136},"precise":0,"confidence":25,"comprehension":100,"level":"乡镇"}}', '{"status":0,"result":{"location":{"lng":119.42791598004884,"lat":32.358303083454128},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":107.15591951767282,"lat":29.159070360026026},"precise":0,"confidence":80,"comprehension":35,"level":"公司企业"}}', '{"status":0,"result":{"location":{"lng":119.43919501420158,"lat":35.39673093182605},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.14997795597528,"lat":39.137109117324488},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":105.62316912312731,"lat":29.411894573867149},"precise":0,"confidence":50,"comprehension":100,"level":"NoClass"}}', '{"status":0,"result":{"location":{"lng":119.63112202878317,"lat":31.73825393057277},"precise":1,"confidence":70,"comprehension":100,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":114.89368602541225,"lat":25.848893033511314},"precise":1,"confidence":70,"comprehension":35,"level":"汽车服务"}}', '{"status":0,"result":{"location":{"lng":117.64654058086437,"lat":35.51201963664022},"precise":0,"confidence":20,"comprehension":100,"level":"区县"}}', '{"status":0,"result":{"location":{"lng":118.8325184592216,"lat":32.12261401761017},"precise":1,"confidence":70,"comprehension":57,"level":"汽车服务"}}']
    l = json.loads(s[0])['result']['location']['lng']

    print(str(l))

    # myclient = pymongo.MongoClient(host='localhost',port=27017)
    # my_db = myclient.testdb
    # my_col = my_db.ford
    # my_col.create_index([("location", GEO2D)],name='location')

    # str = "武汉威汉汽车销售有限责任公司仙桃分公司Wuhan Headman Auto Sales Co. Ltd. Xiantao Branch"
    # str2 = "武汉威汉汽车销售有限责任公司潜江分公司"
    # if str2 in str:
    #     print(1)
    # else:
    #     print(2)
    # myclient = pymongo.MongoClient(host='129.28.93.48', port=27017)
    # db = myclient.admin
    # db.authenticate("root", "autopai123")
    # my_db = myclient.poi
    # # mycol = my_db.ford_website_sales
    # my_cols = my_db.list_collection_names()
    # if "ford_website_sales2" in my_cols:
    #     result = my_db["ford_website_sales2"].rename("ford_website_sales1")
    # print(result)

    # time.sleep(0.05)
    # print(geodesic((35.568013, 119.372785), (35.547410, 118.882959)).km)  # 计算两个坐标直线距离,


    # str = '{"status":0,"result":{"location":{"lng":102.74637780164196,"lat":25.087568971510807},"formatted_address":"云南省昆明市盘龙区北辰东路","business":"江东花园,北辰,霖雨路","addressComponent":{"country":"中国","country_code":0,"country_code_iso":"CHN","country_code_iso2":"CN","province":"云南省","city":"昆明市","city_level":2,"district":"盘龙区","town":"","town_code":"","adcode":"530103","street":"北辰东路","street_number":"","direction":"","distance":""},"pois":[],"roads":[],"poiRegions":[],"sematic_description":"","cityCode":104}}&&A02157,,50310,,云南万福汽车销售服务有限公司,云南万福,1010408.0,1.01040806E8,1.01010211E8,1.0101021106E10,昆明市北京路延长线金泉汽车广场,650224,0871-65727467,0871-65727125,N'
    # arr = str.split("&&")
    #
    # if json.loads(arr[0])['status'] == 0:
    #     print(True)
    # else:
    #     print(False)

    # arr1 = [1,2,4,5,6]
    # arr2 = [2,3,5,8,9]
    # flag = True
    # for i in range(0,len(arr1),1):
    #     for j in range(0,len(arr2),1):
    #         if arr1[i] == arr2[j]:
    #             flag = False
    #             arr2.pop(j)
    #             break
    #     if flag:
    #         print(arr1[i])
    #     else:
    #         flag = True
    # print(arr2)
