# 开发团队：大数据组
# 开发者：albert·bing
# 开发时间：2020/7/5 20:13
# 文件名称：test.py
# 开发工具：PyCharm


#  start your code
import requests
import json

get_date = "20200705"
url = f"http://www.nongli.cn/rili/api/app/god/2020/07/{get_date}.js"


def getData():
    data = requests.get(url=url, verify=False)
    str = data.text
    res = str.replace("day", '"day"').replace("html", '"html"').replace("gongli", '"gongli"').replace("nongli", '"nongli"').\
        replace("start", '"start"').replace("jiri", '"jiri"').replace("suici", '"suici"').replace("wuxing", '"wuxing"').\
        replace("cai", '"cai"').replace("xi", '"xi"').replace("fu", '"fu"').replace("yi", '"yi"').replace("ji", '"ji"').\
        replace("chong", '"chong"').replace("dao", '"dao"').replace('"ji"ri', 'jiri').replace('wu"xi"ng', 'wuxing')
    dick_data = json.loads(res)
    json_data = json.dumps(dick_data)
    # ss = dict(json_data)
    # print(type(ss))
    print(dick_data['html']['nongli'])
#

if __name__ == '__main__':
    getData()
