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
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            new_profile = profile_form.save()
            new_user = user_form.save()
            return HttpResponseRedirect('/profile')
        else:
            return render(request, 'edit_profile.html',
                         {'profile_form': profile_form.as_p,
                          'user_form': user_form.as_p})
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
        return render(request,'edit_profile.html',
                      {'profile_form': profile_form.as_p,
                       'user_form': user_form.as_p})
