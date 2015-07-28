from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Template
from django.template import loader
from django.views.generic import TemplateView
from imager_images.models import Photo
from django.conf import settings


def home_view(request):
    try:
        pic_url = Photo.objects.filter(
                  privacy='PU').order_by('?').first().file
    except AttributeError:
        pic_url = 'demo.jpg'
    return render(request, 'home.html', {'pic_url': pic_url})


def auth_view(request, foo=0):
    return
