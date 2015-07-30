from django.conf.urls import url
from .views import library_view, photo_view, album_view


urlpatterns = [
    url(r'^images/library/$', library_view, name='library'),
    url(r'^images/photos/(?P<photo_id>\w+)/$', photo_view, name='photo'),
    url(r'^images/albums/(?P<album_id>\w+)/$', album_view, name='album'),
]
