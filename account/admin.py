from django.contrib import admin
from .models import dept
from .models import project
from .models import dept_in_pro
from .models import empdetails
from .models import availablepost
from .models import project_img

admin.site.register(dept)
admin.site.register(dept_in_pro)
admin.site.register(empdetails)
admin.site.register(project)
admin.site.register(availablepost)
admin.site.register(project_img)