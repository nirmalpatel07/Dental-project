from django.contrib import admin
from .models import Dentist


class Dentistadmin(admin.ModelAdmin):
    list_display =('first_name','last_name','email','contact_no','specialization')


admin.site.register(Dentist,Dentistadmin)