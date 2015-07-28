"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import django

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/profile/', include('imager_profiles.urls')),
    url(r'^$', 'imagersite.views.home_view', name='homepage'),
    url(r'^(?P<foo>\d+)/$', 'imagersite.views.test_view', name='testme'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/login', include('registration.backends.default.urls')),
    url(r'^accounts/login/$', 'imagersite.views.auth_view',
          {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^accounts/logout/$', 'imagersite.views.auth_view',
          {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^accounts/register/$', 'imagersite.views.auth_view',
          {'template_name': 'registration/registration_form.html'}, name='auth_register'),
]
