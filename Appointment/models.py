# models.py
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Deletes all users'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All users have been deleted successfully'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    appointment_cancelled = models.BooleanField(default=False)


class Appointment(models.Model):
     STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),]
        # Add more status choices as needed
     patient = models.ForeignKey(User, on_delete=models.CASCADE,default='1')
     name = models.CharField(max_length=100)
     phone = models.CharField(max_length=15)
     Email = models.EmailField(default="example@example.com") 
     date = models.DateField()
     time = models.CharField(max_length=8, default='11:40 AM')
     Services = models.CharField(max_length=45 , default='select service' )
     comments = models.TextField(null = True , blank = True)
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Booked')

     def __str__(self):
      return self.name

     def save(self, *args, **kwargs):
         # Convert the time string to 24-hour format before saving
        if self.time:
            self.time = self._convert_to_24_hour_format(self.time)
        super().save(*args, **kwargs)

     def _convert_to_24_hour_format(self, time_str):
        # Split the time string into hours, minutes, and AM/PM
        time_parts = time_str.split(' ')
        hours, minutes = map(int, time_parts[0].split(':'))
        am_pm = time_parts[1].upper()

        # Adjust hours for PM
        if am_pm == 'PM' and hours < 12:
            hours += 12

        # Adjust hours for AM if it's 12:00 AM
        if am_pm == 'AM' and hours == 12:
            hours = 0

        # Create a time object
        return '{:02d}:{:02d}'.format(hours, minutes)
     
@receiver(post_delete, sender=Appointment)
def handle_appointment_cancellation(sender, instance, **kwargs):
    # Get the user profile associated with the patient
    user_profile, created = UserProfile.objects.get_or_create(user=instance.patient)
    # Update the user profile to indicate that an appointment has been cancelled
    user_profile.appointment_cancelled = True
    user_profile.save()


# @receiver(post_delete, sender=Appointment)
# def handle_appointment_cancellation(sender, instance, **kwargs):
#     # Get the user profile associated with the patient
#     user_profile = UserProfile.objects.get_or_create(user=instance.patient)
#     # Update the user profile to indicate that an appointment has been cancelled
#     user_profile.appointment_cancelled = True
#     user_profile.save()



post_delete.connect(handle_appointment_cancellation, sender=Appointment)

class Slot(models.Model):
    date = models.DateField()
    hour = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    minute = models.IntegerField(choices=[(i, f'{i:02d}') for i in range(0, 60, 5)])  # Choices for minutes (0, 5, 10, ..., 55)
    am_pm = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')])
    booked = models.BooleanField(default=False)  # New field to indicate whether the slot is booked

    def __str__(self):
        return f"{self.date} - {self.hour}:{self.minute} {self.am_pm}"
    
    
# class Slot(models.Model):
#     date = models.DateField()
#     start_time = models.TimeField(null=True, blank=True)
#     # end_time = models.TimeField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.date} - {self.start_time} "