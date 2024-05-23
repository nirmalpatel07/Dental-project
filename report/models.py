# report/models.py
from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from service.models import service
from dentist.models import Dentist
from django.utils import timezone


class Report(models.Model):
    date_generated = models.DateField(auto_now_add=True)
    description = models.TextField()
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_email = models.EmailField(default='example@gmail.com')
    service = models.ForeignKey(service, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"Report for {self.dentist} generated on {self.date_generated}  (Patient: {self.patient.first_name} {self.patient.last_name}, Email: {self.patient.email})"
    

class PatientReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
