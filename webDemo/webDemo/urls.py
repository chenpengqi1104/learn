"""webDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from TestModel import views
from TestModel import jshcbd,login,regist,regist2
#from django.urls import path
from django.views.generic import RedirectView
urlpatterns = [
    url(r'index', views.index), 
    url(r'register', views.register), 
    url(r'show_emp', views.show_emp),
    url(r'search_emp', views.search_emp),
    url(r'search_pro', views.search_pro),
    url(r'show_pro', views.show_pro), 
    url(r'del_emp', views.del_emp), 
    url(r'del_pro', views.del_pro), 
    url(r'modify_emp', views.modify_emp), 
    url(r'delete_emp', views.delete_emp),
    url(r'modify_pro', views.modify_pro), 
    url(r'help', views.help), 
    url(r'delete_pro', views.delete_pro),
    
    url(r'mod_emp', views.mod_emp),
    url(r'mod_pro', views.mod_pro),
    url(r'regist2/', regist2.check2),
    url(r'login/', login.check),
    url(r'addPeople/', views.addPeople),
    url(r'addProject/', views.addProject),
    url(r'managePerson', views.managePerson),
   
    url(r'manageProject/', views.manageProject),
    
    url(r'jshcbd/', jshcbd.jshcbd),
    
    url(r'regist/', regist.save),
#    url(r'regist/', views.skip),
   
    url(r'new_emp/', regist.new_emp),
    url(r'new_pro/', regist.new_pro),
    url(r'add_emp/', regist.add_emp),
    url(r'add_pro/', regist.add_pro),
    url(r'list_emp/', regist.list_emp),
    url(r'list_pro/', regist.list_pro),
    url(r'list_emp_pro/', regist.list_emp_pro),
   
    url(r'list', views.list),
   
#    url(r'register/', views.skip),
#    url(r'', views.skip),
#    path('admin/', admin.site.urls),
#   path('',views.skip),
#    path("register/",views.skip),
#    path("regist/",views.register),
#    path("login/",views.login),

]
