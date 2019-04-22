# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators import csrf
from TestModel.models import administrator
import hashlib
def check(request):
    dic={}
    list=[]
    if request.method=='POST':
        username=request.POST['username']     
        str=request.POST['password']
        password=hashlib.md5(str.encode('utf-8')).hexdigest()
        
        list=administrator.objects.filter(adm_name=username,adm_password=password)
    if len(list)==1:
        dic['info']=username
        request.session['username'] = username
        return render(request,'list.html',dic)
    elif len(list)==0:
        dic['info']='用户名或密码错误，请重试!!'    
        return render(request,'index.html',dic)
  
