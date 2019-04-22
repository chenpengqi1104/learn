# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
import re
import hashlib
from TestModel.models import administrator
import datetime
def check2(request):
    info={}
    list=[]
#接受注册页传回的数据并存入数据库
    if request.method=='POST':
        username=request.POST['username']
        list=administrator.objects.filter(adm_name=username)
        
    if len(list)!=0:
        info['message']='该用户名已存在，请重新注册！！'
        return render(request,'register.html',info)
    
    if request.POST['password']!=request.POST['password2']:
        info['message']='两次密码不一致，请重新输入！！'
        return render(request,'register.html',info)
    
    if  not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$', request.POST['email']):
        info['message']='邮箱格式不正确，请重新输入！！'
        return render(request,'register.html',info)
    
    if len(list)==0:
        str=request.POST['password']
        
        password=hashlib.md5(str.encode('utf-8')).hexdigest()
        admin1=administrator(adm_name=request.POST['username'],adm_password=password,adm_email=request.POST['email'])
        admin1.save()
        info['message']='恭喜您，注册成功，点击此处去登录>>'
        return render(request,'registactive.html',info)

  
