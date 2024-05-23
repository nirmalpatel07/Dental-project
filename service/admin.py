from django.contrib import admin
from service.models import service

# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display=('service_title','service_des','additional_details','service_image')




admin.site.register(service,ServiceAdmin)


