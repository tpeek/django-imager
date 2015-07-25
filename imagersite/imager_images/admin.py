from django.contrib import admin
from .models import Photo, Album

admin.site.register(Photo, Album)
