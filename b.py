#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
import string

headers = {

        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'

    }
doc = open("e://data/qq.txt", 'w+',encoding='utf-8')
response = requests.get('https://www.qq.com', headers=headers)
html = response.text

doc=open("e://data/qq_href.txt",'w+',encoding='utf-8')


soup=BeautifulSoup(html,'lxml')

#获取腾讯首页的所有链接
list=[]
for ul in soup.find_all(name='ul'):
    for li in ul.find_all(name='li'):
        for a in li.find_all(name='a'):
            if a.string==None:
                pass
            if re.match('https',a['href'])==None:
                pass
            else:
                list.append(a['href'])

print(list)
f=open("e://data/aaaa.txt",'w+',encoding='utf-8')
for url in list:
    res=requests.get(url)
    ht=res.text
    so=BeautifulSoup(ht,'lxml')
    for p in so.find_all(name='p'):
        if p.string==None:
            pass
        else:
            f.write(p.string+'\n')







