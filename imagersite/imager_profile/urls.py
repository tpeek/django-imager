from django.conf.urls import url
from .views import *


urlpatterns = [
     url(r'^$', profile_view, name='profile'),
     url(r'^edit/', edit_profile_view, name='edit_profile'),
]
