from django.contrib import admin
from Gallery.models import gallery

# Register your models here.

class galleryAdmin(admin.ModelAdmin):
    list_display=('image_title','gallery_image')


admin.site.register(gallery,galleryAdmin)