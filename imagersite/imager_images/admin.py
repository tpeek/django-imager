from django.contrib import admin
from .models import Photo, Album
from django.contrib.gis import forms as geoforms


class LocationForm(geoforms.Form):
    class Meta:
        model = Photo
        fields = ['geom']
    point = geoforms.PointField(widget=
        geoforms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))


admin.site.register(Photo)
admin.site.register(Album)