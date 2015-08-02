from .models import *
from django.forms import ModelForm


class ProfileForm(ModelForm):
    class Meta:
        model = ImagerProfile
        fields = ['name', 'camera', 'address',
                  'website_url', 'photography_type']
