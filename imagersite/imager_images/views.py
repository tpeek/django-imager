from django.shortcuts import render
from imager_images.models import Photo, Album


def photo_view(request, photo_id):
    photo = Photo.objects.filter(id=photo_id).first()
    return render(request, 'photo.html', {'photo': photo})


def album_view(request, album_id):
    album = Album.objects.filter(id=album_id).first()
    return render(request, 'album.html', {'album': album})


def library_view(request):
    return render(request, 'library.html')
