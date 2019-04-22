from django.db import models
class Test(models.Model):
    name = models.CharField(max_length=20)
#    age=models.CharField(max_length=20)
# Create your models here.

class administrator(models.Model):
    adm_name=models.CharField(max_length=20)
    adm_password=models.CharField(max_length=20)
    adm_email=models.CharField(max_length=20)
#    adm_time=models.DateField()
    
class employee(models.Model):
    emp_name=models.CharField(max_length=20)
    emp_sex=models.CharField(max_length=10)
    emp_age=models.IntegerField()
    emp_category=models.CharField(max_length=50)
    pro_id=models.IntegerField()
    pro_name=models.CharField(max_length=50)
    
class project(models.Model):
    pro_name=models.CharField(max_length=50)
    pro_start=models.DateField()
    pro_end=models.DateField()
    pro_cycle=models.CharField(max_length=20)
    pro_category=models.CharField(max_length=50)
    
    