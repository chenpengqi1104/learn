from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
import json 
from django.core import serializers
#from HcOA.models import UserName
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
import re
from TestModel.models import employee, project,administrator


# Create your views here.

def index(request):
    return render(request,'index.html')
def help(request):
    return render(request,'help.html')

def register(request):
    return render(request,'register.html')

def addPeople(request):
    
    
    return render(request,'addPeople.html')


def addProject(request):
    return render(request,'addProject.html')

def list(request):
    username = request.session.get('username')
    dic={}
    list=[]
    list=administrator.objects.filter(adm_name=username)
    if len(list)!=0:
        return render(request,'list.html')
    if len(list)==0: 
        dic['a']='请您先登录！'  
        return render(request,'index.html',dic)

def managePerson(request):
   
        return render(request,'managePerson.html')


def show_emp(request):
   
    
    n=10
    data=[]
    datas=employee.objects.all()[0:n]
    for data1 in datas:
        data.append({
            'id':data1.id,
            'name':data1.emp_name,           
            'sex':data1.emp_sex,         
            'age':data1.emp_age,
            'category':data1.emp_category,
            'pro_id':data1.pro_id,
            'pro_name':data1.pro_name          
    })
        
    return JsonResponse(data,safe=False)


def show_pro(request):
    
    data=[]
    datas=project.objects.all()
    for data1 in datas:
        data.append({
            'id':data1.id,
            'name':data1.pro_name,           
            'start':data1.pro_start,         
            'end':data1.pro_end,
            'cycle':data1.pro_cycle, 
            'category':data1.pro_category         
    })
        
    return JsonResponse(data,safe=False)  

def del_emp(request):
    list=[]
    data={}
    if request.method=="POST":
        num=request.POST['emp_id']
        list=employee.objects.filter(id=num)
        
        if len(list)!=0:
            test1 = employee.objects.get(id=num)
            test1.delete()
            data['message']='删除数据成功！'
            return render(request,'managePerson.html',data)
        if len(list)==0:
            data['message']='员工不存在，无法删除！'
            return render(request,'managePerson.html',data)
        
def del_pro(request):
    list=[]
    data={}
    if request.method=="POST":
        num=request.POST['pro_id']
        list=project.objects.filter(id=num)
        
        if len(list)!=0:
            test1 = project.objects.get(id=num)
            test1.delete()
            data['message']='删除数据成功！'
            return render(request,'manageProject.html',data)
        if len(list)==0:
            data['message']='项目不存在，无法删除！'
            return render(request,'manageProject.html',data)
        
def mod_emp(request):
    data={}
    if request.method=="POST":
        
        num=request.POST['empid']
        category=request.POST['category']
        eclass=request.POST['class']
        proid=request.POST['proid']
        proname=request.POST['proname']
        list=employee.objects.filter(id=num)
        if len(list)!=0:
            test1 = employee.objects.get(id=num)
            test1.emp_category=category+eclass
            test1.pro_id=proid
            test1.pro_name=proname
            test1.save()
            data['message1']='修改信息成功'
            return render(request,'managePerson.html',data)
        if len(list)==0:
            data['message1']='员工不存在，无法修改'
            return render(request,'managePerson.html',data)
def modify_emp(request):
    
    
    return render(request,'mod_emp.html')

def delete_emp(request):
    
        return render(request,'delete_emp.html')
    
def modify_pro(request):
    
    
    return render(request,'mod_pro.html')

def delete_pro(request):
    
        return render(request,'del_pro.html')
    
def search_emp(request):
    data={}
    
    if request.method=="POST":
        name=request.POST['value']
        lists=employee.objects.filter(emp_name=name)
        for list in lists:
            data['id']=list.id
            data['name']=list.emp_name
            data['sex']=list.emp_sex
            data['age']=list.emp_age
            data['category']=list.emp_category
            data['proid']=list.pro_id
            data['proname']=list.pro_name
        
        
    return render(request,'search.html',data)
def search_pro(request):
    data={}
    
    if request.method=="POST":
        name=request.POST['value']
        lists=project.objects.filter(pro_name=name)
        for list in lists:
            data['id']=list.id
            data['name']=list.pro_name
            data['start']=list.pro_start
            data['end']=list.pro_end
            data['cycle']=list.pro_cycle
            data['category']=list.pro_category
            
            
        
        
    return render(request,'search_pro.html',data)
    
def mod_pro(request):
    data={}
    if request.method=="POST":
        num=request.POST['proid']
        start=request.POST['starttime']
        end=request.POST['endtime']
        cycle=request.POST['cycle']
        category=request.POST['category']
        pclass=request.POST['class']
        
        list=project.objects.filter(id=num)
        if len(list)!=0:
            test1 = project.objects.get(id=num)
            test1.pro_start=start
            test1.pro_end=end
            test1.pro_cycle=cycle
            test1.pro_category=category+pclass
            test1.save()
            data['message1']='修改项目信息成功'
            return render(request,'manageProject.html',data)
        if len(list)==0:
            data['message1']='项目不存在，无法修改'
            return render(request,'manageProject.html',data)
        
    

def manageProject(request):
    dic={}
    #num为数据库中总数据的条数
   
    return render(request,'manageProject.html',dic)



    



#def skip(request):

#    res = request.path
#    if re.match(r"^/register$",res):
#        return  render(request,"register.html")
#    elif re.match(r"^/$",res):
#        return  render(request,"index.html")
#    elif re.match(r"login_success",res):
#        return render(request,"list.html")

@csrf_exempt
def register1(request):
    context={}
    if request.POST:
        name=request.POST.get("name")
        list =User.objects.all()
        for var in list:
            if name==var.username:
                context["error"]="用户已存在"
                return render(request, "register.html", context)

        password=request.POST.get("password")
        email=request.POST.get("email")
        User.objects.create_superuser(username=name,password=password,email=email)
        context["message"]="注册成功，欢迎"+name+"回来！"
        return render(request, "index.html", context)

@csrf_exempt
def login(request):
    context ={}
    if request.method=="POST":
        name=request.POST.get("name")
        pwd=request.POST.get("password")
        user = auth.authenticate(username=name,password=pwd)
        if user is not None :
            auth.login(request,user)
            request.session["user"]=name
            return HttpResponseRedirect("/login_success/")
        else:
            context["error"]="用户名或密码错误"
            return render(request,"index.html",context)
    else:
        context["error"] = "没有成功提交"
        return render(request,"index.html",context)

#@login_required
#def loginAction(request):


