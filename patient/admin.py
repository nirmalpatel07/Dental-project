# admin.py
from django.contrib import admin
from .models import Patient
from django.db import models
from django.forms import DateInput

class patientadmin(admin.ModelAdmin):
    list_display =('first_name','last_name','contact_no','address','DOB','gender' ,'email')

    formfield_overrides = {
        models.DateField: {'widget': DateInput(attrs={'type': 'date'})},
    }



admin.site.register(Patient,patientadmin)



