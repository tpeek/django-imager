from imager_images.models import Photo
from rest_framework import viewsets
from .serializers import PhotoSerializer
from django.db.models import Q


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        qs = super(PhotoViewSet, self).get_queryset()
        is_mine = Q(owner=self.request.user)
        is_public = Q(privacy='Public')
        if self.request.user.is_anonymous():
            qs = qs.filter(is_public)
        else:
            qs = qs.filter((is_public | is_mine)).distinct()
        return qs
