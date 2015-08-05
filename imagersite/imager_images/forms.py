from .models import *
from django.forms import ModelForm
from django.contrib.gis import forms as geoforms
# import floppyforms as geoforms

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'privacy', 'cover', 'photos']


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'privacy', 'file']


class LocationForm(geoforms.Form):
    class Meta:
        model = Photo
        fields = ['geom']
    # point = geoforms.PointField()
    point = geoforms.PointField(widget=
        geoforms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

# class LocationForm(geoforms.gis.PointWidget, geoforms.gis.BaseGMapWidget):
#     pass

# class LocationForm(geoforms.Form):
#     class Meta:
#         model = Photo
#         fields = ['geom']

#     point = geoforms.gis.PointField()


# class ReadSingleLocationForm(geoforms.Form):
#     class Meta:
#         model = Photo
#         fields = ['geom']
#         readonly_fields = ['geom']

#     point = geoforms.gis.PointField()