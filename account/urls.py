from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home_page"),
    path('account/logout',views.logout,name="logout"),
    path('account/updatedatabase',views.updatedatabase,name="updatadatabase"),
    path('account/addemployee',views.addemployee,name="addemployee"),
    path('project/loadprodetails',views.prodetails,name="prodetails"),
    path('account/employeeprofile/<emp_id>/',views.employeeprofile,name="employeeprofile"),
    path('account/addproject',views.newproject,name="newproject"),
    path('account/signin',views.signin,name="signin"),
    path('account/sendmessage',views.sendmessage,name="sendmessage"),
    path('account/viewmessage',views.viewmessage,name="viewmessage"),
    path('account/checkmatstatus',views.checkmatstatus,name="checkmatstatus"),
    
]
