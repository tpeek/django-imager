from .models import *
from django.forms import ModelForm


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'privacy', 'cover', 'photos']


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'privacy', 'file']
