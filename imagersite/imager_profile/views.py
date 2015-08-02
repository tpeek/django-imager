from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def edit_profile_view(request):
    form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html',
                 {'form': form.as_p})
