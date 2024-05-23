from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def validate_contact_no(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError('Contact number must be a 10-digit number.')

class Dentist(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    contact_no = models.CharField(max_length=10, validators=[validate_contact_no])
    specialization = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
