from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import *


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            new_profile = form.save()
            return HttpResponseRedirect('/profile')
        else:
            return render(request, 'edit_profile.html',
                         {'form': form.as_p})
    else:
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'edit_profile.html',
                     {'form': form.as_p})
