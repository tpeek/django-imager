from django.shortcuts import render, get_object_or_404
from imager_images.models import Photo, Album
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.conf import settings
from .forms import *
from djgeojson.serializers import Serializer as GeoJSONSerializer


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
    photo = get_object_or_404(Photo, pk=photo_id)
    if request.user != photo.owner:
        raise PermissionDenied
    if request.method == 'POST':
        faces = get_faces(str(photo.file))
        # set_faces(request, photo_id)
        return render(request, 'photo.html', {'photo': photo, 'faces': faces})
    else:
        return render(request, 'photo.html', {'photo': photo})


@login_required
def album_view(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.user != album.owner:
        raise PermissionDenied
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
    form = AlbumForm()
    form.fields['photos'].queryset = Photo.objects.filter(owner=request.user)
    form.fields['cover'].queryset = Photo.objects.filter(owner=request.user)
    return render(request, 'add_album.html', {'form': form.as_p})


@login_required
def add_photo_view(request):
    if request.method == 'POST':
        picform1 = PhotoForm(request.POST, request.FILES)
        picform2 = LocationForm(request.POST)
        if picform1.is_valid() and picform2.is_valid():
            new_photo = picform1.save(commit=False)
            new_photo.geom = picform2.cleaned_data['point']
            new_photo.owner = request.user
            new_photo.save()

            return HttpResponseRedirect('/images/library')
        else:
            return render(request, 'add_photo.html', {'form1': picform1.as_p,
                'form2': picform2})
    else:
        picform1 = PhotoForm()
        picform2 = LocationForm()
        return render(request, 'add_photo.html', {'form1': picform1.as_p,
                'form2': picform2})


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
        picform1 = PhotoForm(request.POST, request.FILES, instance=photo)
        picform2 = LocationForm(request.POST)
        if picform1.is_valid() and picform2.is_valid():
            new_photo = picform1.save(commit=False)
            new_photo.owner = request.user
            new_photo.geom = picform2.cleaned_data['point']
            new_photo.save()
            return HttpResponseRedirect('/images/library')
        else:
            return render(request, 'edit_photo.html',
                          {'form1': picform1.as_p,
                           'form2': picform2,
                           'photo_id': photo_id})
    else:
        picform1 = PhotoForm(instance=photo)
        picform2 = LocationForm()
        # picform2.fields['point'] = photo.geom
        return render(request, 'edit_photo.html',
                      {'form1': picform1.as_p,
                       'form2': picform2,
                       'photo_id': photo_id,
                       'loc': photo.geom})


def p_geoview(request, photo_id):
    """Geo data for photo"""
    owner = Photo.objects.get(pk=photo_id).owner
    privacy = Photo.objects.get(pk=photo_id).privacy

    if (request.user != owner) and (privacy == 'Private'):
        raise PermissionDenied
    else:
        photo_lst = Photo.objects.filter(pk=photo_id).all()
        return HttpResponse(GeoJSONSerializer().serialize(
            photo_lst, use_natural_keys=True, with_modelname=False,
            properties=['geom']))


def a_geoview(request, album_id):
    """Geo data for album"""
    owner = Album.objects.get(pk=album_id).owner
    privacy = Album.objects.get(pk=album_id).privacy

    if (request.user != owner) and (privacy == 'Private'):
        raise PermissionDenied
    else:
        photo_lst = Album.objects.get(pk=album_id).photos.all()
        return HttpResponse(GeoJSONSerializer().serialize(
            photo_lst, use_natural_keys=True, with_modelname=False,
            properties=['geom']))
