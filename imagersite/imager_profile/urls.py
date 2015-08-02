from django.conf.urls import url
from .views import *


urlpatterns = [
     url(r'^profile/$', profile_view, name='profile'),
     url(r'^profile/edit/', edit_profile_view, name='edit_profile'),
]
