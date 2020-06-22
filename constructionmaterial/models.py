from django.db import models
from account import models as account
from django.contrib.auth.models import User
import datetime
# Create your models here.

class rawmaterial(models.Model):
    name=models.CharField(max_length=100,blank=False,unique=True)
    price_per_head=models.BigIntegerField(default=0)
    def __str__(self):
        return self.name
    
class machine_and_tools(models.Model):
    name=models.CharField(max_length=100,blank=False,unique=True)
    category=models.CharField(max_length=50,blank=False,default="machine")
    def __str__(self):
        return self.name
    
class mat_to_project(models.Model):
    pro=models.ForeignKey(account.project,on_delete=models.CASCADE)
    mat=models.ForeignKey(rawmaterial,on_delete=models.CASCADE)
    given_quantiy=models.IntegerField(default=0)
    used_qunatity=models.IntegerField(default=0)
    quantity_demand=models.IntegerField(default=0)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['pro','mat'],name='uniquec')
        ]
    
class machine_to_project(models.Model):
    machine_category=models.ForeignKey(machine_and_tools,on_delete=models.CASCADE)
    barcode=models.BigIntegerField(unique=True)
    ava_status=models.CharField(max_length=100,default="available")
    working_status=models.CharField(max_length=100,default="woking")
    pro=models.ForeignKey(account.project,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.barcode)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['barcode','pro'],name='uniquec2')
        ]
    
class tool_to_project(models.Model):
    tool_category=models.ForeignKey(machine_and_tools,on_delete=models.CASCADE)
    total_quantity=models.IntegerField(default=0)
    quantity_issued=models.IntegerField(default=0)
    pro=models.ForeignKey(account.project,on_delete=models.CASCADE)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['tool_category','pro'],name='unique3')
        ]
    
class machine_issued_details(models.Model):
    machine_category=models.ForeignKey(machine_and_tools,on_delete=models.CASCADE)
    emp=models.ForeignKey(User,on_delete=models.CASCADE)
    machine=models.ForeignKey(machine_to_project,on_delete=models.CASCADE)
    issued_date=models.DateField()
    returned_date=models.DateField()

    
class tools_issued_details(models.Model):
    tool=models.ForeignKey(machine_and_tools,on_delete=models.CASCADE)
    emp=models.ForeignKey(User,on_delete=models.CASCADE)
    qunatity_issued=models.IntegerField()
    issued_date=models.DateField()
    returned_date=models.DateField()
   
    
class machine_maintainance_cost(models.Model):
    machine=models.ForeignKey(machine_to_project,on_delete=models.CASCADE)
    project=models.ForeignKey(account.project,on_delete=models.CASCADE)
    amount=models.IntegerField()
   
    

