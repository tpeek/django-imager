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
    email = factory.LazyAttribute(
        lambda a: '{}.{}@example.com'.format(a.first_name, a.last_name).lower()
        )
    username = factory.LazyAttribute(
        lambda a: '{}{}{}{}'.format(a.last_name[:1], a.first_name[1:],
        a.first_name[:1], a.last_name[1:]).lower()
        )


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album


##### Helper functions #####
def make_one_photo():
    """Make one photo attached to a single user with default settings"""
    owner = UserFactory.create()
    owner.save()
    photo = PhotoFactory.create(owner=owner)
    return owner, photo


def make_one_photo_album():
    """Make one photo attached to an album"""
    owner = UserFactory.create()
    owner.save()
    cover = PhotoFactory.create(owner=owner)
    cover.save()
    album = AlbumFactory.create(owner=owner, cover=cover)
    return owner, album


def make_user_and_login(client):
    # Fake data
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    # Create user
    user = User.objects.create_user(username=username,
        password=password, email=email)
    login = client.post('/login/', {'username': username,
        'password': password}, follow=True)
    return user, username


def attach_two_photos_to_user(user):
        photo1 = PhotoFactory.create(owner=user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=user)
        album.save()
        album.photos = [photo1, photo2]

        return album, [photo1, photo2]


##### Test Cases #####
class PhotoModelTestCase(TestCase):
    """Create a photo owner and associate a generic photo"""
    def setUp(self):
        self.owner, self.photo1 = make_one_photo()

    def test_photo_exists(self):
        self.assertFalse(Photo.objects.all())
        self.photo1.save()
        self.assertTrue(Photo.objects.all())

    def test_photo_user(self):
        self.assertEqual(self.photo1.owner, self.owner)
        self.assertFalse(self.photo1.owner is UserFactory.create())


class AlbumModelTestCase1(TestCase):
    """Create an owner, then an empty album, then add photos to album"""
    def setUp(self):
        owner, self.album1 = make_one_photo_album()

    def test_album_exists(self):
        self.assertFalse(Album.objects.all())
        self.album1.save()
        self.assertTrue(Album.objects.all())

    def test_album_user(self):
        self.album1.save()
        self.assertTrue(self.album1.owner)
        self.assertFalse(self.album1.owner ==
                         UserFactory.create(username='Penelope'))

    def test_add_photos(self):
        self.album1.save()
        photos = [
            PhotoFactory.create(owner=self.album1.owner) for x in range(10)]
        for photo in photos:
            photo.save()
        self.album1.photos.add(*photos)
        self.assertTrue(self.album1.photos.count() == 10)


class AlbumModelTestCase2(TestCase):
    """Create a user and associate pictures with that user; add these
    public pictures to both this user and another's albums"""
    def setUp(self):
        owner1, owner2 = UserFactory.create(),\
            UserFactory.create(username='bob')
        self.owners = (owner1, owner2)
        self.albums = []
        for owner in self.owners:
            owner.save()
            cover = PhotoFactory.create(owner=owner)
            cover.save()
            album = AlbumFactory.create(owner=owner, cover=cover)
            album.save()
            self.albums.append(album)
        self.photos = [
            PhotoFactory.create(owner=self.albums[0].owner) for x in range(10)]
        for photo in self.photos:
            photo.save()

    def test_many_to_many(self):
        self.albums[0].photos.add(*self.photos)
        self.albums[1].photos.add(*self.photos)
        for p1, p2 in zip(self.albums[0].photos.all(),
                          self.albums[1].photos.all()):
            self.assertEqual(p1, p2)


class LibraryPageTestCase(TestCase):
    """Tests for Library view"""
    def setUp(self):
        """Make a User no photos"""
        self.user, self.username = make_user_and_login(self.client)

    def test_thumbnails_for_album_with_null_cover(self):
        album, photos = attach_two_photos_to_user(self.user)
        response = self.client.get('/images/library/')
        # Getting the html tag content for thumbnail
        atemp = Template('src="/static/imager_images/seattle.jpg')
        srclink = atemp.render(Context({'STATIC_URL': settings.STATIC_URL,
            'album': album}))
        # Assert that thumbnail exists as src attribute
        self.assertIn(srclink, response.content)

    def test_thumbnails_for_all_albums_user_defined(self):
        album, photos = attach_two_photos_to_user(self.user)
        album.cover = photos[1]
        response = self.client.get('/images/library/')
        # Getting the html tag content for thumbnail
        atemp = Template('src="{{ MEDIA_URL }}{{ album.cover.file }}"')
        srclink = atemp.render(Context({'MEDIA_URL': settings.MEDIA_URL,
            'album': album}))
        # Assert that thumbnail exists as src attribute
        self.assertIn(srclink, response.content)

    def test_titles_for_all_albums_user_defined(self):
        album, photos = attach_two_photos_to_user(self.user)
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

        album, photos = attach_two_photos_to_user(self.user)
        photo1 = photos[1]
        # Get response and test
        response = self.client.get('/images/library/')
        self.assertIn('/images/photos/add/', response.content)
        self.assertIn('/images/albums/add/', response.content)
        self.assertIn('/images/photos/{}/edit/'.format(photo1.id),
                      response.content)
        self.assertIn('/images/albums/{}/edit/'.format(album.id),
                      response.content)


class PhotoViewTestCase(TestCase):
    """Tests for Photo view"""
    def setUp(self):
        self.client = Client()
        self.user, username = make_user_and_login(self.client)
        album, photos = attach_two_photos_to_user(self.user)
        self.photo1, self.photo2 = photos[0], photos[1]
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


class AlbumViewTestCase(TestCase):
    """Tests for Album view"""
    def setUp(self):
        self.client = Client()
        self.user, username = make_user_and_login(self.client)
        self.album, photos = attach_two_photos_to_user(self.user)
        self.photo1, self.photo2 = photos[0], photos[1]
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


class PhotoAddTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, username = make_user_and_login(self.client)

    def test_photo_has_form(self):
        response = self.client.get('/images/photos/add/')
        self.assertTrue(response.context['form1'])

    def test_photo_form_has_all_fields(self):
        fields = dict(title=fake.sentence(), description=fake.paragraph(),
            privacy="Private", file=os.path.join(
            settings.MEDIA_ROOT, 'googlephoto.jpg'))
        response = self.client.post('/images/photos/add/', data=fields)
        self.assertEqual(response.status_code, 200)


class PhotoEditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, username = make_user_and_login(self.client)
        self.album, photos = attach_two_photos_to_user(self.user)
        self.photo1, self.photo2 = photos[0], photos[1]

    def test_photo_edit_has_form(self):
        response = self.client.get(
            '/images/photos/{}/edit/'.format(self.photo1.id))
        self.assertTrue(response.context['form1'])
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


class AlbumAddTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, username = make_user_and_login(self.client)

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


class AlbumEditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, username = make_user_and_login(self.client)
        self.album, photos = attach_two_photos_to_user(self.user)
        self.photo1, self.photo2 = photos[0], photos[1]

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
