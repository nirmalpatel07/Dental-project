from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class service(models.Model):
    service_title=models.CharField(max_length=50)
    service_des=models.TextField(blank=True)
    additional_details = HTMLField()  # Additional details for the service
    service_image=models.FileField(upload_to="media/%y",max_length=250,null=True,default=None)

    def __str__(self):
        return f"{self.service_title}"