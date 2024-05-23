from django.db import models

# Create your models here.


from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime




class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default = "om@gmail.com")
    contact_no = models.CharField(max_length=15)  # Assuming contact number as a string
    address = models.TextField()
    DOB = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def clean(self):
        if self.DOB > datetime.now().date():
            raise ValidationError({'DOB': 'Date of birth cannot be in the future.'})
        
    def __str__(self):
         return f"{self.email}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
   