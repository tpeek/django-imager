from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Template
from django.template import loader
from django.views.generic import TemplateView
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from django.conf import settings


def home_view(request):
    try:
        pic_url = Photo.objects.filter(
                  privacy='PU').order_by('?').first().file
    except AttributeError:
        pic_url = 'demo.jpg'
    return render(request, 'home.html', {'pic_url': pic_url})


def profile_view(request):
    return render(request, 'profile.html')


def photos_view(request, username):
    user = User.objects.filter(username=username).first()
    photos = Photo.objects.filter(owner=user).order_by('date_uploaded')
    return render(request, 'photos.html',
                 {'photos': photos, 'username': username.title()})


def auth_view(request, foo=0):
    return
