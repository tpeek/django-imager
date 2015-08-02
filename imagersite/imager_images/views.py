from django.shortcuts import render
from imager_images.models import Photo, Album
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.conf import settings
from .forms import *

import Algorithmia
import base64


def get_faces(path):
    with open(settings.MEDIA_ROOT + "/" + path, "rb") as img:
        bimage = base64.b64encode(img.read())
    Algorithmia.apiKey = "Simple simivSeptsC+ZsLks5ia0wXmFbC1"
    result = Algorithmia.algo('/ANaimi/FaceDetection').pipe(bimage)
    faces = []
    for rect in result:
        face = Face()
        face.name = "Petter Rabbit"
        face.x = rect['x']
        face.y = rect['y']
        face.width = rect['width']
        face.height = rect['height']
        faces.append(face)
        for face in faces:
            face.save()
    return faces


def set_faces(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    face_id = request.POST.get('photo_id', '0')
    face = Face.objects.get(id=face_id)
    face.name = Face.objects.get('name', 'Unknown')
    face.save()


@login_required
def photo_view(request, photo_id):
    if request.user != Photo.objects.filter(pk=photo_id).first().owner:
        raise PermissionDenied
    photo = Photo.objects.filter(pk=photo_id).first()
    if request.method == 'POST':
        faces = get_faces(str(photo.file))
        # set_faces(request, photo_id)
        return render(request, 'photo.html', {'photo': photo, 'faces': faces})
    else:
        return render(request, 'photo.html', {'photo': photo})


@login_required
def album_view(request, album_id):
    if request.user != Album.objects.filter(pk=album_id).first().owner:
        raise PermissionDenied
    album = Album.objects.filter(id=album_id).first()
    return render(request, 'album.html', {'album': album})


@login_required
def library_view(request):
    return render(request, 'library.html')


@login_required
def add_album_view(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        form.fields['photos'].queryset = Photo.objects.filter(owner=request.user)
        form.fields['cover'].queryset = Photo.objects.filter(owner=request.user)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.owner = request.user
            new_album.save()
            form.save_m2m()
            return HttpResponseRedirect('/images/library')
        else:
            return render(request, 'add_album.html', {'form': form.as_p})
    else:
        form = AlbumForm()
        form.fields['photos'].queryset = Photo.objects.filter(owner=request.user)
        form.fields['cover'].queryset = Photo.objects.filter(owner=request.user)
        return render(request, 'add_album.html', {'form': form.as_p})


@login_required
def add_photo_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.owner = request.user
            new_photo.save()
            return HttpResponseRedirect('/images/library')
        else:
            return render(request, 'add_photo.html', {'form': form.as_p})
    else:
        form = PhotoForm()
        return render(request, 'add_photo.html', {'form': form.as_p})


@login_required
def edit_album_view(request, album_id):
    if request.user != Album.objects.filter(pk=album_id).first().owner:
        raise PermissionDenied
    album = Album.objects.filter(id=album_id).first()
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.owner = request.user
            new_album.save()
            form.save_m2m()
            return HttpResponseRedirect('/images/library')
        else:
            form.fields['photos'].queryset = Photo.objects.filter(owner=request.user)
            form.fields['cover'].queryset = Photo.objects.filter(owner=request.user)
            return render(request, 'edit_album.html',
                         {'form': form.as_p, 'album_id': album_id})
    else:
        form = AlbumForm(instance=album)
        form.fields['photos'].queryset = Photo.objects.filter(owner=request.user)
        form.fields['cover'].queryset = Photo.objects.filter(owner=request.user)
        return render(request, 'edit_album.html',
                     {'form': form.as_p, 'album_id': album_id})


@login_required
def edit_photo_view(request, photo_id):
    if request.user != Photo.objects.filter(pk=photo_id).first().owner:
        raise PermissionDenied
    photo = Photo.objects.filter(id=photo_id).first()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.owner = request.user
            new_photo.save()
            return HttpResponseRedirect('/images/library')
        else:
            return render(request, 'edit_photo.html',
                         {'form': form.as_p, 'album_id': photo_id})
    else:
        form = PhotoForm(instance=photo)
        return render(request, 'edit_photo.html',
                     {'form': form.as_p, 'photo_id': photo_id})
