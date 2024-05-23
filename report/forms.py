# report/forms.py
from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['description', 'dentist', 'patient','patient_email', 'service']
