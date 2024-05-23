from django.db import models

# Create your models here.

class gallery(models.Model):
    image_title=models.CharField(max_length=50 , null =True ,blank = True)
    gallery_image=models.FileField(upload_to="media/%y",max_length=250,null=True,default=None)