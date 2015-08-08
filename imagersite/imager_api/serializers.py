from rest_framework import serializers
from imager_images.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Photo
        fields = ('title', 'description', 'privacy', 'file', 'owner',
                  'date_uploaded', 'date_modified', 'geom')
