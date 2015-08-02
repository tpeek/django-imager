from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = ImagerProfile
        fields = ['nickname', 'camera', 'address',
                  'website_url', 'photography_type']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
