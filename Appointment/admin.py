from django.contrib import admin
from .models import Appointment
from .models import Slot


class Appointmentadmin(admin.ModelAdmin):
    list_display = ('name','phone','Email','date','time','Services','comments','status') 
    actions = ['cancel_selected_appointments']

    def cancel_selected_appointments(self, request, queryset):
        # Update the status of selected appointments to 'Cancelled'
        queryset.update(status='Cancelled')
        self.message_user(request, "Selected appointments have been cancelled successfully.")

class slotadmin(admin.ModelAdmin):
    list_display = ('date','hour','minute','am_pm','booked') 



admin.site.register(Slot,slotadmin)
admin.site.register(Appointment,Appointmentadmin)
