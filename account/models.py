from django.db import models
from django.contrib.auth.models import User,auth

# Create your models here.
class dept(models.Model):
    name=models.CharField(max_length=20,null=False,blank=False)
    def __str__(self):
        return self.name
class availablepost(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class empdetails(models.Model):
    address=models.CharField(max_length=100,blank=False,null=False)
    phone_no=models.CharField(max_length=13,blank=False,null=False,unique=True)
    age=models.IntegerField()
    supervisor=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    salary=models.BigIntegerField()
    post=models.ForeignKey(availablepost,on_delete=models.SET_NULL,null=True)
    dno=models.ForeignKey(dept,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.phone_no
    
class project(models.Model):
    name=models.CharField(unique=True, max_length=100,null=False,blank=False)
    location=models.CharField( max_length=100,null=False,blank=False)
    hop=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    budget=models.BigIntegerField(null=False,blank=False)
    deadline=models.DateField(null=False,blank=False)
    no_of_emp=models.IntegerField(blank=True,default=0)
    def __str__(self):
        return self.name
    class Meta:
        unique_together=(("name","location"),)
class project_img(models.Model):
    pro=models.ForeignKey(project,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='media')
class dept_in_pro(models.Model):
    pro=models.ForeignKey(project, on_delete=models.CASCADE)
    dept=models.ForeignKey(dept, on_delete=models.CASCADE)
    mgr=models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together=(("pro","dept"),)
class attendance2020(models.Model):
    eid=models.ForeignKey(User,on_delete=models.CASCADE)
    month=models.CharField(max_length=20)
    day1=models.CharField(max_length=2,default="A")
    day2=models.CharField(max_length=2,default="A")
    day3=models.CharField(max_length=2,default="A")
    day4=models.CharField(max_length=2,default="A")
    day5=models.CharField(max_length=2,default="A")
    day6=models.CharField(max_length=2,default="A")
    day7=models.CharField(max_length=2,default="A")
    day8=models.CharField(max_length=2,default="A")
    day9=models.CharField(max_length=2,default="A")
    day10=models.CharField(max_length=2,default="A")
    day11=models.CharField(max_length=2,default="A")
    day12=models.CharField(max_length=2,default="A")
    day13=models.CharField(max_length=2,default="A")
    day14=models.CharField(max_length=2,default="A")
    day15=models.CharField(max_length=2,default="A")
    day16=models.CharField(max_length=2,default="A")
    day17=models.CharField(max_length=2,default="A")
    day18=models.CharField(max_length=2,default="A")
    day19=models.CharField(max_length=2,default="A")
    day20=models.CharField(max_length=2,default="A")
    day21=models.CharField(max_length=2,default="A")
    day22=models.CharField(max_length=2,default="A")
    day23=models.CharField(max_length=2,default="A")
    day24=models.CharField(max_length=2,default="A")
    day25=models.CharField(max_length=2,default="A")
    day26=models.CharField(max_length=2,default="A")
    day27=models.CharField(max_length=2,default="A")
    day28=models.CharField(max_length=2,default="A")
    day29=models.CharField(max_length=2,default="A")
    day30=models.CharField(max_length=2,default="A")
    day31=models.CharField(max_length=2,default="A")
    total_att=models.IntegerField()
    overtime=models.IntegerField()
    pendingsalary=models.IntegerField()
    recivedsalary=models.IntegerField()
    def __str__(self):
        return self.eid
class empmessages(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    reciver=models.ForeignKey(User, related_name='reciver',on_delete=models.CASCADE,null=False,blank=False)
    content=models.TextField()
    date=models.DateField()
    status=models.CharField(max_length=20,default="unread")
