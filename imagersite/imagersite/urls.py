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
    #url(r'^profile/', include('imager_profiles.urls'))
    url(r'^$', 'imagersite.views.home_view', name='homepage'),
    url(r'^(?P<foo>\d+)/$', 'imagersite.views.test_view', name='testme'),
    # https://docs.djangoproject.com/en/1.8/topics/auth/default/#using-the-views
    # Includes all auth views, including login, logout, etc:
    #
    # ^login/$ [name='login']
    # ^logout/$ [name='logout']
    # ^password_change/$ [name='password_change']
    # ^password_change/done/$ [name='password_change_done']
    # ^password_reset/$ [name='password_reset']
    # ^password_reset/done/$ [name='password_reset_done']
    # ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
    # ^reset/done/$ [name='password_reset_complete']
    # url('^', include('django.contrib.auth.urls')),

    # Here's the django-registration-redux implementation
    url(r'^accounts/', include('registration.backends.default.urls'))
]
