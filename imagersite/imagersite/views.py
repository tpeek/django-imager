from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Template
from django.template import loader
from django.views.generic import TemplateView

# Create your views here.
def home_view(request):
    # template = loader.get_template('templates/home.jinja2')
    # response_body = template.render(request, 'templates/home.jinja2')
    # return HttpResponse(response_body)
    return render(request, 'base.html')

def test_view(request, foo=0):
    return render(request, 'base.html')
