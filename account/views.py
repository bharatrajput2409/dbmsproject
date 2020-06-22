from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect
from django.contrib import messages
from .models import project
from .models import dept
from .models import dept_in_pro
from .models import empdetails
from .models import availablepost
from .models import project_img
from django.db.models import Q
from .models import empmessages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
import string
import random
import datetime
# Create your views here.
def home(request):
    projects=project.objects.all()
    if request.user.is_authenticated:
        try:
            post=availablepost.objects.get(id=empdetails.objects.get(id=request.user.id).post_id).name
        except empdetails.DoesNotExist:
            post=="labour"
            messages.add_message(request,messages.ERROR,"employee details does not exist. There might be problem in inserting employee details...")
        if post=="techician":
            post="labour"
    else:
        post="labour"
    return render(request,'account/home_page.htm',{'projects':projects,'post':post})

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        print(username=="surendra")
        print(password)
        user=auth.authenticate(password=password,username=username)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"No user found!!!")
            return HttpResponseRedirect("")
    else:
        return render(request,'account/login.htm')
def prodetails(request):
    if request.user.is_authenticated and (empdetails.objects.get(id=request.user.id).post_id==3 or empdetails.objects.get(id=request.user.id).post_id==5):
        return render(request,'account/notauthorised.htm')
    proid=request.GET['id']
    pro=project.objects.get(id=proid)
    allmgrs=[]
    siteeng=[]
    hop=User.objects.get(project__id=pro.id)
    hop_details=empdetails.objects.get(id=hop.id)
    prodept=dept_in_pro.objects.filter(pro_id=pro.id)
    for k in prodept:
        temp=dict()
        temp['user1']=User.objects.get(id=k.mgr_id)
        temp['user2']=empdetails.objects.get(id=temp['user1'].id)
        allmgrs=allmgrs +[temp]
        eng=empdetails.objects.filter(supervisor=temp['user1'].id,post_id=6)
        for e in eng:
            temp1=dict()
            temp1['user2']=e
            temp1['user1']=User.objects.get(id=e.id)
            siteeng=siteeng+[temp1]
    photos=project_img.objects.filter(pro_id=proid)
    context={
        'hop':hop,
        'hop_details':hop_details,
        'project':pro,
        'allmgrs':allmgrs,
        'siteengs':siteeng,
        'photos':photos
    }

    for k in allmgrs:
        print(k['user1'].first_name)
    return render(request,'project/project_details.htm',context)
def logout(request):
    auth.logout(request)
    return redirect("/")
def updatedatabase(request):
    # projects=project.objects.all()
    # for pro in projects:
    #     allmgrs=[]
    #     siteeng=[]
    #     allworker=[]
    #     hop=employee.objects.get(project__id=pro.id)
    #     prodept=dept_in_pro.objects.filter(pro_id=pro.id)
    #     for k in prodept:
    #         temp=employee.objects.get(id=k.mgr_id)
    #         allmgrs=allmgrs +[temp]
    #         eng=employee.objects.filter(supervisor=temp.id)
    #         for e in eng:
    #             siteeng=siteeng + [e]
    #             worker=employee.objects.filter(supervisor=e.id)
    #             for w in worker:
    #                 allworker=allworker +[w]
    #     print(allmgrs)
    #     print(siteeng)
    #     print(allworker)
    #     pro.no_of_emp=len(allmgrs)+len(siteeng)+len(allworker)
    #     pro.save()
    return redirect('/')
def employeeprofile(request,emp_id):
    print(emp_id)
    emp=dict()
    emp['user1']=User.objects.get(id=emp_id)
    emp['user2']=empdetails.objects.get(id=emp_id)
    logedinpostid=empdetails.objects.get(id=request.user.id).post_id
    post=availablepost.objects.get(id=emp['user2'].post_id)
    msgcount=empmessages.objects.filter(reciver_id=emp_id,status="unread").count()
    allunderworker=[]
    k=empdetails.objects.filter(supervisor_id=emp['user1'].id)
    for i in k:
        d=dict()
        d['user1']=User.objects.get(id=i.id)
        d['user2']=i
        allunderworker=allunderworker +[d]
    if post.name=="owner" or post.name=="head of project":
        
        return render(request,'account/ownerpage.htm',{'emp':emp,'msgcount':msgcount,'allunderworkers':allunderworker,'logedinpostid':logedinpostid})
    else:
        if post.name=="labour" or post.name=='technician':
            siteeng=empdetails.objects.get(id=emp['user2'].supervisor_id)
            if siteeng.post_id == 6:
                try:
                    pro=project.objects.get(dept_in_pro__mgr_id=siteeng.id)
                except project.DoesNotExist:
                    mgr=empdetails.objects.get(id=siteeng.supervisor_id)
                    pro=project.objects.get(dept_in_pro__mgr_id=mgr.id)
            elif siteeng.post_id==1 or siteeng.post_id==2:
                pro=project.objects.get(dept_in_pro__mgr_id=siteeng.id)
            else:
                pro=""
        elif post.name=="site engineer":
            try:
                pro=project.objects.get(dept_in_pro__mgr_id=emp['user1'].id)
            except project.DoesNotExist:
                mgr=User.objects.get(id=emp['user2'].supervisor_id)
                pro=project.objects.get(dept_in_pro__mgr_id=mgr)
        else:
            pro=project.objects.get(dept_in_pro__mgr_id=emp['user1'])
        
        context={
            'emp':emp,
            'pro':pro,
            'msgcount':msgcount,
            'allunderworkers':allunderworker,
            'logedinpostid':logedinpostid
        }
        return render(request,'account/userprofile.htm',context)
def addemployee(request):
    if request.method=="POST":
        try:
            obj=User.objects.get(username=request.POST['username'])
            e="this username already exist !"
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect("")
        except User.DoesNotExist:
            try:
                empdetails.objects.get(phone_no=request.POST['phoneno'])
                e="This phone no already exist !"
                messages.add_message(request,messages.ERROR,e)
                return HttpResponseRedirect("")
            except empdetails.DoesNotExist:
                
                flag=True
                for k in request.POST['supervisor']:
                    if k.isalpha()==True:
                        flag=False
                        break
                print(flag)
                if flag==True:
                    try:
                        empsupervisor=empdetails.objects.get(id=request.POST['supervisor'])
                        
                    except empdetails.DoesNotExist:
                        e="There is no supervisor with given id !"
                        messages.add_message(request,messages.ERROR,e)
                        return HttpResponseRedirect("")
                else:
                    try:
                        empsupervisor=User.objects.get(username=request.POST['supervisor'])
                        empsupervisor=empdetails.objects.get(id=empsupervisor.id)
                    except User.DoesNotExist:
                        e="There is no supervisor with given id !"
                        messages.add_message(request,messages.ERROR,e)
                        return HttpResponseRedirect("")
                if empsupervisor.post_id ==3 or empsupervisor.post_id==5:
                    e="provided supervisor is not eligible for supervisor post !"
                    messages.add_message(request,messages.ERROR,e)
                    return HttpResponseRedirect("")
                post=availablepost.objects.get(name=request.POST['post'])
                if empsupervisor.post_id==2 and post.id==6:
                    e="machinery manager can not have site engineer" 
                    messages.add_message(request,messages.ERROR,e)
                    return HttpResponseRedirect("")
                obj=User.objects.create_user(first_name=request.POST['first_name'] ,last_name=request.POST['last_name'] ,username=request.POST['username'] ,password=request.POST['password1'],email=request.POST['email'] )
                objtemp=empdetails()
                objtemp.address=request.POST['address']
                objtemp.phone_no=request.POST['phoneno']
                objtemp.age=request.POST['age']
                objtemp.salary=request.POST['salary']
                objtemp.post_id=post.id
                if objtemp.post_id==3 or objtemp.post_id==5 or objtemp.post_id==6 :
                    objtemp.dno_id=empsupervisor.dno_id
                else:
                    objtemp.dno_id=dept.objects.get(name=request.POST['department']).id
                objtemp.supervisor_id=empsupervisor.id
                objtemp.save()
        depts=dept.objects.all()
        posts=availablepost.objects.all()
        if objtemp.post_id==1 or objtemp.post_id==2:
            prodept=dept_in_pro()
            prodept.mgr_id=obj.id
            prodept.dept_id=objtemp.dno_id
            try:
                prodept.pro_id=project.objects.get(hop_id=objtemp.supervisor).id
            except project.DoesNotExist:
                obj.delete()
                objtemp.delete()
                messages.add_message(request,messages.ERROR,"either project does not exist or supervisor is not a head of project !")
                return HttpResponseRedirect("")
            try:
                prodept.save()
            except IntegrityError as e:
                e="There is already a manager for provide department !"
                obj.delete()
                objtemp.delete()
                messages.add_message(request,messages.ERROR,e)
                return HttpResponseRedirect("")


        messages.add_message(request,messages.SUCCESS,"user created successfuly with id "+str(obj.id))
        return HttpResponseRedirect("")
    else:
        post=empdetails.objects.get(id=request.user.id).post_id
        print(post)
        if post==4 or post==7:
            depts=dept.objects.all()
            posts=availablepost.objects.all()
            return render(request,'account/addemployee.htm',{'depts':depts,'posts':posts})
        else:
            return render(request,'account/notauthorised.htm')
def newproject(request):
    if request.method=="POST":
        try:
            temp=project.objects.get(hop_id=request.POST['hop_id'])
            e="Provided employee is already a head of project for another project !"
            messages.add_message(request,messages.ERROR,e)

        except project.DoesNotExist:
            try:
                emp=empdetails.objects.get(id=request.POST['hop_id'])
                if emp.post_id==7:
                    obj=project()
                    obj.name=request.POST['name']
                    obj.location=request.POST['location']
                    obj.budget=request.POST['budget']
                    obj.deadline=request.POST['deadline']
                    obj.hop_id=request.POST['hop_id']
                    messages.add_message(request,messages.SUCCESS,"project added successfully!")
                    obj.save()
                else:
                    e="This employee cant be a head of project !"
                    messages.add_message(request,messages.ERROR,e)
            except empdetails.DoesNotExist:
                e="Employee with provided id does not exist"
                messages.add_message(request,messages.ERROR,e)


        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated:
            post=availablepost.objects.get(id=empdetails.objects.get(id=request.user.id).post_id).name
        else:
            post="labour"
        if post=="owner":
            return render(request,'account/newproject.htm')
        else:
            return render(request,'account/notauthorised.htm')
def markattendance(request):
    return render(request,'account/markattendance.htm')
def sendmessage(request):
    if request.method=="POST":
        empid=request.POST['empid']
        flag=True
        for k in empid:
            if k.isalpha()==True:
                flag=False
                break
        if flag==True:
            try:
                reciver=User.objects.get(id=empid)
                sendm=empmessages()
                sendm.sender_id=request.user.id
                sendm.reciver=reciver
                sendm.content=request.POST['content']
                sendm.date=datetime.date.today()
                sendm.save()
                e="message sent"
            except User.DoesNotExist:
                e="reciver does not exist"
        else:
            try:
                reciver_id=User.objects.get(username=empid).id
                sendm=empmessages()
                sendm.sender_id=request.user.id
                sendm.reciver_id=reciver_id
                sendm.content=request.POST['content']
                sendm.date=datetime.date.today()
                sendm.save()
                e="message sent"
            except User.DoesNotExist:
                e="reciver does not exist"

        messages.add_message(request,messages.ERROR,e)
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated:
            return render(request,'account/sendmessage.htm')
        else:
            return render(request,'account/notauthorised.htm')
def viewmessage(request):
    if request.user.is_authenticated:
        empid=request.user.id
        empmessage=empmessages.objects.filter(Q(reciver_id=empid)| Q(sender_id=empid)).order_by('-id')
        listofmessage=[]
        for e in empmessage:
            listofmessage=listofmessage + [e]
            if e.sender_id != request.user.id:
                if e.status == "unread":
                    e.status="read"
                    e.save()
                    e.status="unread"

        return render(request,'account/viewmessage.htm',{'empmessage':listofmessage})
    else:
        return render(request,'account/notauthorised.htm')
def checkmatstatus(request):

    return render(request,'/project/checkmaterial.htm')