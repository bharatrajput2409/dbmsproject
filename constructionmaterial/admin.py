from django.contrib import admin
from .models import machine_to_project
from .models import machine_and_tools
from .models import machine_maintainance_cost
from .models import tool_to_project
from .models import tools_issued_details
from .models import machine_issued_details
from .models import mat_to_project
from .models import rawmaterial




admin.site.register(machine_to_project)
admin.site.register(machine_and_tools)
admin.site.register(machine_maintainance_cost)
admin.site.register(tools_issued_details)
admin.site.register(tool_to_project)
admin.site.register(mat_to_project)
admin.site.register(rawmaterial)
admin.site.register(machine_issued_details)