from django.shortcuts import render
from imager_images.models import Photo


def home_view(request):
    try:
        pic_url = Photo.objects.filter(
            privacy='Public').order_by('?').first().file
    except AttributeError:
        pic_url = ''
    return render(request, 'home.html', {'pic_url': pic_url})


def auth_view(request):
    return
