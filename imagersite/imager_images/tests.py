from __future__ import unicode_literals
from .models import Photo, Album
from django.contrib.auth.models import User
from django.test import TestCase
import factory
from faker import Faker

fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda a: '{}.{}@example.com'.format(
                                  a.first_name, a.last_name).lower())
    username = factory.LazyAttribute(lambda a: '{}{}{}{}'.format(
                                     a.last_name[:1], a.first_name[1:],
                                     a.first_name[:1], a.last_name[1:]).lower())


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album


class PhotoTestCase(TestCase):
    def setUp(self):
        owner = UserFactory.create()
        owner.save()
        self.photo1 = PhotoFactory.create(owner=owner)

    def tearDown(self):
        Photo.objects.all().delete()
        User.objects.all().delete()

    def test_photo_exists(self):
        self.assertFalse(Photo.objects.all())
        self.photo1.save()
        self.assertTrue(Photo.objects.all())

    def test_photo_user(self):
        self.assertTrue(self.photo1.owner)
        self.assertFalse(self.photo1.owner is UserFactory.create())


class AlbumTestCase(TestCase):
    def setUp(self):
        owner = UserFactory.create()
        owner.save()
        cover = PhotoFactory.create(owner=owner)
        cover.save()
        self.album1 = AlbumFactory.create(owner=owner, cover=cover)

    def tearDown(self):
        Album.objects.all().delete()
        Photo.objects.all().delete()
        User.objects.all().delete()

    def test_album_exists(self):
        self.assertFalse(Album.objects.all())
        self.album1.save()
        self.assertTrue(Album.objects.all())

    def test_album_user(self):
        self.album1.save()
        self.assertTrue(self.album1.owner)
        self.assertFalse(self.album1.owner is
                         UserFactory.create(username='Penelope'))

    def test_add_photos(self):
        self.album1.save()
        photos = [PhotoFactory.create(owner=self.album1.owner) for x in range(10)]
        for photo in photos:
            photo.save()
        self.album1.photos.add(*photos)
        self.assertTrue(self.album1.photos.count() == 10)
