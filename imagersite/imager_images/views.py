from django.shortcuts import render
from imager_images.models import Photo, Album
from django.contrib.auth.decorators import login_required


@login_required
def photo_view(request, photo_id):
    photo = Photo.objects.filter(id=photo_id).first()
    return render(request, 'photo.html', {'photo': photo})


@login_required
def album_view(request, album_id):
    album = Album.objects.filter(id=album_id).first()
    return render(request, 'album.html', {'album': album})


@login_required
def library_view(request):
    return render(request, 'library.html')
