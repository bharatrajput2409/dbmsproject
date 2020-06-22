from django.urls import path
from . import views

urlpatterns = [
    path('allmaterial',views.allmaterial,name="allmaterial"),
    path('machinery',views.machinery,name="machinery"),
    path('addmachine',views.addmachine,name="addmachine"),
    path('addtools',views.addtools,name="addtools"),
    path('issuemachine',views.machineissue,name="machineissue"),
    path('checkoutmachine',views.checkoutmachine,name="chekoutmachine"),
    path('issuetools',views.issuetools,name="issuetools"),
    path('checkout',views.checkout),
    path('previousmachines',views.previousmachines,name="previousmachines"),
    path('checkstatus',views.checkstatus,name="checkstatus"),
    path('addmat',views.addmat,name="addmat"),
    path('demandmat',views.demandmat,name="demandmat")
]