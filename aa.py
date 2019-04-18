#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
基于python3.6开发的。
分析

请求 url
https://movie.douban.com/j/search_subjects

请求方式
get

请求参数
type: movie
tag: 热门
sort: recommend
page_limit: 20
page_start: 60

请求头
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
"Referer"
"Cookie"

'''

# 先实现一次请求
# 然后在实现循环请求

import requests

import json


url = "https://movie.douban.com/j/search_subjects"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
doc=open("e://data/douban.txt",'w+')

for page_start in range(0,100,20):
    params = {
        "type":"movie",
        "tag":"热门",
        "sort":"recommend",
        "page_limit":"20",
        "page_start":page_start
    }

    response = requests.get(
        url=url,
        headers=headers,
        params=params
    )

    # 方式一:直接转换json方法
    # results = response.json()
    # 方式二: 手动转换
    # 获取字节串
    content = response.content
    # 转换成字符串
    string = content.decode('utf-8')
    # 把字符串转成python数据类型
    results = json.loads(string)
    # 解析结果
    for movie in results["subjects"]:
        doc.write(movie["title"]+','+movie["rate"]+'\n')
        print(movie["title"],movie["rate"])

doc.close()