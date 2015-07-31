from django.conf.urls import url
from .views import profile_view


urlpatterns = [
     url(r'^profile/$', profile_view, name='profile'),
]
