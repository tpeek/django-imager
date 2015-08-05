from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^images/library/$', library_view, name='library'),
    url(r'^images/photos/(?P<photo_id>\d+)/$', photo_view, name='photo'),
    url(r'^images/albums/(?P<album_id>\d+)/$', album_view, name='album'),
    url(r'^images/photos/add/$', add_photo_view, name='add_photo'),
    url(r'^images/albums/add/$', add_album_view, name='add_album'),
    url(r'^images/albums/(?P<album_id>\d+)/edit/', edit_album_view, name='edit_album'),
    url(r'^images/photos/(?P<photo_id>\d+)/edit/', edit_photo_view, name='edit_photo'),
    url(r'^images/photos/data.geojson/(?P<photo_id>\d+)/$', p_geoview, name='p_geodata'),
    url(r'^images/albums/data.geojson/(?P<album_id>\d+)/$', a_geoview, name='a_geodata')
]