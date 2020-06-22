from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib import messages
from account.models import project
from account.models import dept
from account.models import dept_in_pro
from account.models import empdetails
from account.models import availablepost
from .models import machine_and_tools
from .models import machine_to_project
from .models import tool_to_project
from .models import machine_issued_details
from .models import tools_issued_details
from .models import mat_to_project
from .models import rawmaterial
from django.http import HttpResponseRedirect
import datetime
def allmaterial(request):
    pass
def machinery(request):
    emp=request.user
    if request.user.is_authenticated and empdetails.objects.get(id=emp.id).post_id == 2:
        pro=project.objects.get(id=dept_in_pro.objects.get(mgr_id=emp.id).pro_id)
        machines=machine_and_tools.objects.all()
        context={
            'machines':machines,
            'pro':pro
        }
        return render(request,'project/machinery.htm',context)
    else:
        return render(request,'account/notauthorised.htm')
def addmachine(request):
    if request.method=='POST':
        user=request.user
        obj=machine_to_project()
        obj.machine_category=machine_and_tools.objects.get(name=request.POST['item_cat'])
        obj.pro=project.objects.get(hop_id=empdetails.objects.get(id=user.id).supervisor_id)
        obj.barcode=request.POST['barcode']
        try:
            obj.save()
            messages.add_message(request,messages.SUCCESS,"item added successfully!")
        except IntegrityError:
            messages.add_message(request,messages.SUCCESS,"item already exist !")    
        
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated and empdetails.objects.get(id=request.user.id).post_id == 2:
            machine=machine_and_tools.objects.filter(category="machine")
            return render(request,'project/addmachine.htm',{'machines':machine})
        else:
            return render(request,'account/notauthorised.htm')
def addtools(request):
    if request.method=="POST":
        user=request.user
        pro=project.objects.get(hop_id=empdetails.objects.get(id=user.id).supervisor_id)
        toolcat=machine_and_tools.objects.get(name=request.POST['item_cat'])
        try:
             temp=tool_to_project.objects.get(pro_id=pro.id,tool_category_id=toolcat)
             temp.total_quantity=temp.total_quantity + int(request.POST['total_quantity'])
             temp.save()
        except tool_to_project.DoesNotExist:
            obj=tool_to_project()
            obj.tool_category=toolcat
            obj.pro=pro
            obj.total_quantity=request.POST['total_quantity']
            obj.save()
        messages.add_message(request,messages.SUCCESS,"item added successfully!")
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated and empdetails.objects.get(id=request.user.id).post_id == 2:
            tools=machine_and_tools.objects.filter(category="tools")
            return render(request,'project/addtools.htm',{'tools':tools})
        else:
            return render(request,'account/notauthorised.htm')
def machineissue(request):
    if request.method=='POST':
        empid=request.POST['empid']
        machineid=request.POST['machineid']
        try:
            emp=empdetails.objects.get(id=empid)
            try:
                machine_to_be_issued=machine_to_project.objects.get(barcode=machineid)
                if machine_to_be_issued.ava_status=="not available":
                    messages.add_message(request,messages.SUCCESS,'item already issued !')
                else:
                    if emp.post_id==5 or emp.post_id==3 or emp.post_id==6:
                        obj=machine_issued_details()
                        obj.issued_date=datetime.date.today()
                        obj.emp_id=empid
                        obj.machine=machine_to_be_issued
                        obj.machine_category_id=machine_to_be_issued.machine_category_id
                        obj.returned_date=datetime.date(1212,12,12)
                        obj.save()
                        machine_to_be_issued.ava_status="not available"
                        machine_to_be_issued.save()
                        messages.add_message(request,messages.SUCCESS,'item issued successfully !')
                    else:
                        messages.add_message(request,messages.ERROR,"Employee with id " + empid + " can't issue a machine!")
            except machine_to_project.DoesNotExist:
                messages.add_message(request,messages.ERROR,"provided machine id is either invalid or does not exist!")
            
        except empdetails.DoesNotExist:
            messages.add_message(request,messages.SUCCESS,"provided employee id does not exist !")
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated and empdetails.objects.get(id=request.user.id).post_id == 2:
            return render(request,'project/machineissue.htm')
        else:
            return render(request,'account/notauthorised.htm')
        
def issuetools(request):
    if request.method=='POST':
        empid=request.POST['empid']
        tool_name=request.POST['tool_name']
        try:
            emp=empdetails.objects.get(id=empid)
            try:
                temp=tool_to_project.objects.get(tool_category__name=tool_name,pro_id=project.objects.get(hop_id=empdetails.objects.get(id=request.user.id).supervisor_id))
                
                if temp.total_quantity - temp.quantity_issued >= int(request.POST['toolquantity']):
                    obj=tools_issued_details()
                    obj.qunatity_issued=request.POST['toolquantity']
                    obj.emp_id=empid
                    obj.issued_date=datetime.date.today()
                    obj.returned_date=datetime.date(1212,12,12)
                    obj.tool_id=temp.tool_category_id
                    obj.save()
                    temp.quantity_issued= int(temp.quantity_issued) + int(obj.qunatity_issued)
                    temp.save()
                    messages.add_message(request,messages.SUCCESS,"item issued successfully !")
                else:
                    messages.add_message(request,messages.ERROR,"tool quantity is not sufficient ,available quantity is " + str(temp.total_quantity))
                
            except tool_to_project.DoesNotExist:
                messages.add_message(request,messages.ERROR,"selected tool is either invalid or not present !")
        except empdetails.DoesNotExist:
            messages.add_message(request,messages.ERROR,"provided employee id does not exist !")
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated and empdetails.objects.get(id=request.user.id).post_id == 2:
            tools=machine_and_tools.objects.filter(category="tools")
            return render(request,'project/issuetools.htm',{'tools':tools})
        else:
            return render(request,'account/notauthorised.htm')
def checkoutmachine(request):
    if 'employeeid' not in request.POST and 'employeeid' not in request.GET:
        return render(request,'account/notauthorised.htm')
    if 'employeeid' in request.POST:
        emp_id=request.POST['employeeid']
    if 'employeeid' in request.GET:
        emp_id=request.GET['employeeid']
    emp=dict()
    try:
        emp['user1']=User.objects.get(id=emp_id)
        emp['user2']=empdetails.objects.get(id=emp_id)
        post=availablepost.objects.get(id=emp['user2'].post_id)
        if post.name=="owner" or post.name=="head of project":
            return render(request,'project/checkoutmachine.htm',{'emp':emp})
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
                'date':datetime.date(1212,12,12)
            }
            if emp['user2'].post_id==5 or emp['user2'].post_id==3 or emp['user2'].post_id==6:
                machine_issued=machine_issued_details.objects.filter(emp_id=emp['user2'].id,returned_date=datetime.date(1212,12,12))
                tool_issued=tools_issued_details.objects.filter(emp_id=emp['user2'].id,returned_date=datetime.date(1212,12,12))
                context['machine_issued']=machine_issued
                context['tool_issued']=tool_issued
            
            return render(request,'project/checkoutmachine.htm',context)
    except User.DoesNotExist:
        messages.add_message(request,messages.ERROR,"user does not exist !")
        return redirect("/project/machinery")
def checkout(request):
    employeeid=request.GET['empid']
    print(employeeid)
    if 'tool' in request.GET:
        tool=request.GET['tool']
        issued_tool=tools_issued_details.objects.get(id=tool)
        tool_to_checkout=tool_to_project.objects.get(tool_category_id=issued_tool.tool_id)                
        issued_tool.returned_date=datetime.date.today()
        issued_tool.save()
        tool_to_checkout.quantity_issued= tool_to_checkout.quantity_issued - int(issued_tool.qunatity_issued)
        tool_to_checkout.save()
    else:
        machine=request.GET['machine']
        machine_to_checkout=machine_to_project.objects.get(id=machine)
        issued_machine=machine_issued_details.objects.get(machine_id=machine_to_checkout.id,returned_date=datetime.date(1212,12,12))
        issued_machine.returned_date=datetime.date.today()
        issued_machine.save()
        machine_to_checkout.ava_status="available"
        machine_to_checkout.save()
    messages.add_message(request,messages.SUCCESS,"item checked out successfully !")
        
    return redirect('/project/checkoutmachine?employeeid=' + str(employeeid))
def previousmachines(request):
    if 'employeeid' not in request.POST and 'employeeid' not in request.GET:
        return render(request,'account/notauthorised.htm')
    if 'employeeid' in request.POST:
        emp_id=request.POST['employeeid']
    if 'employeeid' in request.GET:
        emp_id=request.GET['employeeid']
    print(emp_id)
    emp=dict()
    try:
        emp['user1']=User.objects.get(id=emp_id)
        emp['user2']=empdetails.objects.get(id=emp_id)
        post=availablepost.objects.get(id=emp['user2'].post_id)
        if post.name=="owner" or post.name=="head of project":
            return render(request,'project/checkoutmachine.htm',{'emp':emp})
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
                'date': datetime.date(1212,12,12)
            }
            if emp['user2'].post_id==5 or emp['user2'].post_id==3 or emp['user2'].post_id==6:
                machine_issued=machine_issued_details.objects.filter(emp_id=emp['user2'].id)
                tool_issued=tools_issued_details.objects.filter(emp_id=emp['user2'].id)
                context['machine_issued']=machine_issued
                context['tool_issued']=tool_issued
            
            return render(request,'project/checkoutmachine.htm',context)
    except User.DoesNotExist:
        messages.add_message(request,messages.ERROR,"user does not exist !")
        return redirect("/project/machinery")
def checkstatus(request):
    itemname=request.POST['itemname']
    print(itemname)
    item=machine_and_tools.objects.get(name=itemname)
    proid=dept_in_pro.objects.get(mgr_id=request.user.id).pro_id
    if item.category == "machine":
        countitems=machine_to_project.objects.filter(machine_category_id=item.id , pro_id=proid).count()
        availableitems=machine_to_project.objects.filter(machine_category_id=item.id , pro_id=proid,ava_status="available").count()
        if countitems==0:
            messages.add_message(request,messages.ERROR,"No "+itemname + " available !")
        else:
            messages.add_message(request,messages.SUCCESS,str(availableitems) +" "+ itemname + " available out of " + str(countitems) + " !")
    else:
        try:
            countitems=tool_to_project.objects.get(tool_category_id=item.id , pro_id=proid)
            messages.add_message(request,messages.SUCCESS,str(countitems.total_quantity - countitems.quantity_issued) + " " + itemname + " available !")
        except tool_to_project.DoesNotExist:
            messages.add_message(request,messages.SUCCESS,"No item found !")
    return HttpResponseRedirect("")
def addmat(request):
    if request.method=="POST":
        total_quantity=request.POST['total_quantity']
        item_cat=request.POST['item_cat']
        pro=project.objects.get(hop_id=empdetails.objects.get(id=request.user.id).supervisor_id)
        mat=rawmaterial.objects.get(name=item_cat)
        try:
            matinpro=mat_to_project.objects.get(mat=mat,pro=pro)
            matinpro.given_quantiy= matinpro.given_quantiy +  int(total_quantity);
            matinpro.save()
        except mat_to_project.DoesNotExist:
            obj=mat_to_project()
            obj.given_quantiy=total_quantity;
            obj.pro=pro
            obj.mat=mat
            obj.save()
        e="item added succesfully !"
        messages.add_message(request,messages.ERROR,e)
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated and empdetails.objects.get(id=request.user.id).post_id==2:
            mat=rawmaterial.objects.all()
            return render(request,'project/addmat.htm',{'mat':mat})
        else:
            return render(request,'account/notauthorised.htm')
def demandmat(request):
    if request.method=="POST":
        total_quantity=request.POST['total_quantity']
        item_cat=request.POST['item_cat']
        pro=project.objects.get(hop_id=empdetails.objects.get(id=request.user.id).supervisor_id)
        mat=rawmaterial.objects.get(name=item_cat)
        try:
            matinpro=mat_to_project.objects.get(mat=mat,pro=pro)
            try:
                matinpro.quantity_demand= matinpro.quantity_demand +  int(total_quantity);
            except ValueError:
                e="provided input is not meaningfull"
                messages.add_message(request,messages.ERROR,e)
                return HttpResponseRedirect("")
            matinpro.save()
        except mat_to_project.DoesNotExist:
            obj=mat_to_project()
            obj.quantity_demand=total_quantity;
            obj.pro=pro
            obj.mat=mat
            obj.save()
        e="Demand added succesfully !"
        messages.add_message(request,messages.ERROR,e)
        return HttpResponseRedirect("")
    else:
        if request.user.is_authenticated and empdetails.objects.get(id=request.user.id).post_id==2:
            mat=rawmaterial.objects.all()
            return render(request,'project/demandmat.htm',{'mat':mat})
        else:
            return render(request,'account/notauthorised.htm')