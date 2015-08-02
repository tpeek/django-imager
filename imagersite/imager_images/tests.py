from __future__ import unicode_literals
from .models import Photo, Album
from django.contrib.auth.models import User
import factory
from django.test import Client, TestCase
from django.template import Template, Context
from faker import Factory as FakeFaker
from django.conf import settings
import os

fake = FakeFaker.create()


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


class AlbumTestCase1(TestCase):
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
        photos = [
            PhotoFactory.create(owner=self.album1.owner) for x in range(10)]
        for photo in photos:
            photo.save()
        self.album1.photos.add(*photos)
        self.assertTrue(self.album1.photos.count() == 10)


class AlbumTestCase2(TestCase):
    def setUp(self):
        owner1, owner2 = UserFactory.create(),\
            UserFactory.create(username='bob')
        owner1.save()
        owner2.save()
        cover1 = PhotoFactory.create(owner=owner1)
        cover2 = PhotoFactory.create(owner=owner2)
        cover1.save()
        cover2.save()
        self.album1 = AlbumFactory.create(owner=owner1, cover=cover1)
        self.album2 = AlbumFactory.create(owner=owner2, cover=cover2)
        self.album1.save()
        self.album2.save()
        self.photos = [
            PhotoFactory.create(owner=self.album1.owner) for x in range(10)]
        for photo in self.photos:
            photo.save()

    def tearDown(self):
        Album.objects.all().delete()
        Photo.objects.all().delete()
        User.objects.all().delete()

    def test_many_to_many(self):
        self.album1.photos.add(*self.photos)
        self.album2.photos.add(*self.photos)
        for p1, p2 in zip(self.album1.photos.all(), self.album2.photos.all()):
            self.assertEqual(p1, p2)


class LibraryPage(TestCase):
    """Tests for Library view"""
    def setUp(self):
        """Make a User no photos"""
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)

    def test_thumbnails_for_album_with_null_cover(self):
        # Add photos to album
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=self.user)
        album.save()
        album.photos = [photo1, photo2]
        response = self.client.get('/images/library/')
        # Getting the html tag content for thumbnail
        atemp = Template('src="{{ MEDIA_URL }}seattle.jpg')
        srclink = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'album': album}))
        # Assert that thumbnail exists as src attribute
        self.assertIn(srclink, response.content)

    def test_thumbnails_for_all_albums_user_defined(self):
        # Add photos to album
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=self.user, cover=photo1)
        album.save()
        album.photos = [photo1, photo2]
        response = self.client.get('/images/library/')
        # Getting the html tag content for thumbnail
        atemp = Template('src="{{ MEDIA_URL }}{{ album.cover.file }}"')
        srclink = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'album': album}))
        # Assert that thumbnail exists as src attribute
        self.assertIn(srclink, response.content)

    def test_titles_for_all_albums_user_defined(self):
        # Add photos to album
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=self.user, cover=photo1)
        album.save()
        album.photos = [photo1, photo2]
        response = self.client.get('/images/library/')
        # Getting the html tag content for thumbnail
        atemp = Template("{{ album.title }}")
        atitle = atemp.render(Context({'album': album}))
        # Assert that thumbnail exists as src attribute
        self.assertIn(atitle, response.content)

    def test_library_url(self):
        response = self.client.get('/images/library/')
        self.assertEqual('/images/library/', response.wsgi_request.path)

    def test_library_links_to_add_views_no_photos_albums(self):
        """Check that library page has a link to add photo and add album
        views"""
        response = self.client.get('/images/library/')
        # No photos this fct; add buttons still present
        self.assertIn('/images/photos/add/', response.content)
        self.assertIn('/images/albums/add/', response.content)

    def test_library_links_to_add_edit_views_with_photos_albums(self):
        """Check that the library page has a link to add photo/album as
        well as edit photo/album when these exist"""
        # Add photos to album
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=self.user, cover=photo1)
        album.save()
        album.photos = [photo1, photo2]
        # Get response and test
        response = self.client.get('/images/library/')
        self.assertIn('/images/photos/add/', response.content)
        self.assertIn('/images/albums/add/', response.content)
        self.assertIn('/images/photos/{}/edit/'.format(photo1.id),
                      response.content)
        self.assertIn('/images/albums/{}/edit/'.format(album.id),
                      response.content)


class PhotoView(TestCase):
    """Tests for Photo view"""
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)
        # Make photos
        self.photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()
        self.response1 = self.client.get('/images/photos/' +
                                    str(self.photo1.id) +'/')
        self.response2 = self.client.get('/images/photos/' +
                                    str(self.photo2.id) +'/')

    def test_check_photo_url_exists(self):
        self.assertEqual(self.response1.status_code, 200)
        self.assertEqual(self.response2.status_code, 200)

    def test_photo_displayed(self):
        # Getting the html tag content for thumbnail
        atemp = Template('src="{{ MEDIA_URL }}{{ photo.file }}"')
        srclink1 = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'photo': self.photo1}))
        srclink2 = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'photo': self.photo2}))
        self.assertIn(srclink1, self.response1.content)
        self.assertIn(srclink2, self.response2.content)


class AlbumView(TestCase):
    """Tests for Album view"""
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)
        # Make photos
        self.photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()
        self.album = AlbumFactory.create(owner=self.user, cover=self.photo1)
        self.album.save()
        self.album.photos = [self.photo1, self.photo2]
        self.response = self.client.get('/images/albums/' +
                                        str(self.album.id) + '/')

    def test_photo_view_url_exists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_photos_displayed(self):
        # Getting the html tag content for thumbnails
        atemp = Template('src="{{ MEDIA_URL }}{{ photo.file }}"')
        srclink1 = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'photo': self.photo1}))
        srclink2 = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'photo': self.photo2}))
        self.assertIn(srclink1, self.response.content)
        self.assertIn(srclink2, self.response.content)


class PhotoAdd(TestCase):
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)

    def test_photo_has_form(self):
        response = self.client.get('/images/photos/add/')
        self.assertTrue(response.context['form'])

    def test_photo_form_has_all_fields(self):
        fields = dict(title=fake.sentence(), description=fake.paragraph(),
            privacy="Private", file=os.path.join(
            settings.MEDIA_ROOT, 'googlephoto.jpg'))
        response = self.client.post('/images/photos/add/', data=fields)
        self.assertEqual(response.status_code, 200)


class PhotoEdit(TestCase):
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)
        # Make photos
        self.photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()

    def test_photo_edit_has_form(self):
        response = self.client.get(
            '/images/photos/{}/edit/'.format(self.photo1.id))
        self.assertTrue(response.context['form'])
        self.assertEqual(response.status_code, 200)

    def test_photo_edit_has_populated_data(self):
        response = self.client.get(
            '/images/photos/{}/edit/'.format(self.photo1.id))
        self.assertIn(self.photo1.title, response.content)
        self.assertIn(self.photo1.description, response.content)
        self.assertIn(self.photo1.privacy, response.content)
        # Getting the link for the photo
        phototemp = Template("{{ photo.file }}")
        photolink = phototemp.render(Context({'photo': self.photo1}))
        self.assertIn(photolink, response.content)

    def test_photo_edit_submits(self):
        fields = dict(title=fake.sentence(), description=fake.paragraph(),
            privacy="Private", file=os.path.join(
            settings.MEDIA_ROOT, 'googlephoto.jpg'))
        response = self.client.post('/images/photos/add/', data=fields)
        self.assertEqual(response.status_code, 200)


class AlbumAdd(TestCase):
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)

    def test_album_has_form(self):
        response = self.client.get('/images/albums/add/')
        self.assertTrue(response.context['form'])
        self.assertEqual(response.status_code, 200)

    def test_photo_form_has_all_fields(self):
        # Make photos
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        # Post album fields
        fields = dict(title=fake.sentence(), description=fake.paragraph(),
            privacy="Public", photos=[photo1, photo2], cover=photo2)
        response = self.client.post('/images/photos/add/', data=fields)
        self.assertEqual(response.status_code, 200)


class AlbumEdit(TestCase):
    def setUp(self):
        self.client = Client()
        # Fake data
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        # Create user
        self.user = User.objects.create_user(username=self.username,
            password=self.password, email=self.email)
        self.login = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)
        # Make photos
        self.photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()
        self.album = AlbumFactory.create(owner=self.user, cover=self.photo1)
        self.album.save()
        self.album.photos = [self.photo1, self.photo2]

    def test_album_edit_has_form(self):
        response = self.client.get(
            '/images/albums/{}/edit/'.format(self.album.id))
        self.assertTrue(response.context['form'])
        self.assertEqual(response.status_code, 200)

    def test_album_edit_has_populated_data(self):
        response = self.client.get(
            '/images/albums/{}/edit/'.format(self.album.id))
        self.assertIn(self.album.title, response.content)
        self.assertIn(self.album.description, response.content)
        self.assertIn(self.album.privacy, response.content)

    def test_album_edit_submits(self):
        fields = dict(title=fake.sentence(), description=fake.paragraph(),
            privacy="Private", cover=self.photo2, photos=[self.photo2])
        response = self.client.post('/images/albums/{}/edit/'.format(
                                    self.album.id), data=fields)
        self.assertEqual(response.status_code, 200)