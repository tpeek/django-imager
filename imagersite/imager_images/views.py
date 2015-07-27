from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template
from django.template import loader
from django.views.generic import TemplateView

# Create your views here.
def home_view(request):
    template = loader.get_template('home.html')
    response_body = template.render()
    return HttpResponse(response_body)
