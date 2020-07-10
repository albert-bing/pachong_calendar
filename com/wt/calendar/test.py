# coding=utf-8

# @Team：Big Data Group
# @Time：2020/7/10 11:37
# @Author：albert·bing
# @File：test.py
# @Software：PyCharm


#  start your code

if __name__ == '__main__':
    str = '2020年7月'
    da = str.split('年')[0]
    data = str.split('年')[1].split('月')[0]
    print(da+data)