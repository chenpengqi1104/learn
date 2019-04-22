from django.shortcuts import render
from django.views.decorators import csrf
from TestModel.models import employee,project
def save(request):
    
    return render(request,'regist.html')

def new_emp(request):
    
    return render(request,'new_emp.html')

def new_pro(request):
    
    return render(request,'new_pro.html')

def add_emp(request):
    list=[]
    dic={}
    if request.method=='POST':
       
        empname=request.POST['empname']
        empsex=request.POST['empsex']
        empage=request.POST['empage']
        category=request.POST['category']+"-"+request.POST['class']
        list=employee.objects.filter(emp_name=empname)
        
    if len(list)!=0:
        dic['info']='该员工已存在，请勿重新添加！！'
        return render(request,'addPeople.html',dic)
    
    if len(list)==0:   
        admin=employee(emp_name=empname,emp_sex=empsex,emp_age=empage,emp_category=category)
        admin.save()
        dic['info']='新增员工成功！'
    

    return render(request,'addPeople.html',dic)



def add_pro(request):
    dic={}
    if request.method=='POST':
        proname=request.POST['proname']
        starttime=request.POST['starttime']
        endtime=request.POST['endtime']
        cycle=request.POST['cycle']
        category=request.POST['category']+"-"+request.POST['class']
        
        admin=project(pro_name=proname,pro_start=starttime,pro_end=endtime,pro_cycle=cycle,pro_category=category)
        admin.save()
        dic['info']='新增项目成功！'
        
    return render(request,'addProject.html',dic)

        
def list_emp(request):
    dic={}
   
   
    dic['id']=employee.objects.get(id=1)
    
    
    return render(request,'employee.html',dic)



def list_pro(request):
    
    return render(request,'employee.html')



def list_emp_pro(request):
    
    return render(request,'employee.html')
        
        
        
        
        
        
        
        
        
        
        