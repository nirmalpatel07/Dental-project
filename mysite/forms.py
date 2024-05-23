from django import forms
from Appointment.models import Appointment # Import the Appointment model
from django.core.exceptions import ValidationError




 
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'Email', 'date', 'time' ,'Services','comments']  # Add fields as needed

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) > 10:
            raise forms.ValidationError("Phone number must be 10 digits or less.")
        return phone