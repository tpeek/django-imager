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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/profile/', include('imager_profiles.urls')),
    url(r'^$', 'imagersite.views.home_view', name='homepage'),
    url(r'^profile/$', 'imagersite.views.profile_view', name='profile'),
    url(r'^images/library/$', 'imagersite.views.library_view', name='library'),
    url(r'^images/photos/(?P<photo_id>\w+)/$', 'imagersite.views.photo_view', name='photo'),
    url(r'^images/albums/(?P<album_id>\w+)/$', 'imagersite.views.album_view', name='album'),
    url(r'^', include('registration.backends.default.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
