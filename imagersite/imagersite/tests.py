from django.test import Client, TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from django.template import Template, Context
from django.core.urlresolvers import reverse
# from imager_profile.models import User
import factory
from faker import Factory as FakeFaker
from django.conf import settings
import os
from django.core import mail
import re

fake = FakeFaker.create()


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo
    title = fake.sentence()
    description = fake.paragraph()


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album
    title = fake.sentence()
    description = fake.paragraph()


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


class HomeView(TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()

    def test_self_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_links_for_home(self):
        response = self.client.get('/')
        self.assertIn('<a href="/login/">login</a>', response.content)
        self.assertIn('<a href="/register/">register</a>', response.content)

    def test_random_photo_in_site(self):
        # Special setup
        owner = UserFactory.create()
        owner.save()
        self.photo1 = PhotoFactory.create(owner=owner, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=owner, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()
        # Test
        pics = set()
        for i in range(100):
            response = self.client.get('/')
            pics.add(response.context['pic_url'])
        self.assertEqual(len(pics), 2)

    def test_static_photo_in_site(self):
        pics = set()
        for i in range(100):
            response = self.client.get('/')
            pics.add(response.context['pic_url'])
        self.assertEqual(len(pics), 1)
        self.assertIn('demo.jpg', pics)


class LoginExists(TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()

    def test_self_exists(self):
        response = self.client.get('/login', follow=True)
        self.assertEqual(response.status_code, 200)


class LogoutExists(TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()

    def test_self_exists(self):
        response = self.client.get('/logout', follow=True)
        self.assertEqual(response.status_code, 200)


class RegisterUser(TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()

    def test_register_user(self):
        response = self.client.post('/register/', {'username': self.username,
            'password1': self.password, 'password2': self.password,
            'email': self.email}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('activate', response.content)

    def test_activate(self):
        register = self.client.post('/register/', {'username': self.username,
            'password1': self.password, 'password2': self.password,
            'email': self.email}, follow=True)
        # Regex lifted from:
        # http://stackoverflow.com/questions/9760588/how-do-you-extract-a-url-from-a-string-using-python
        link = re.search("(?P<url>https?://[^\s]+)",
            mail.outbox[0].body).group("url")
        link_bits = link.split('/')
        rel_uri = "/" + "/".join(link_bits[3:])
        activate = self.client.get(rel_uri, follow=True)
        self.assertIn('activate/complete', activate.wsgi_request.path)
        # Newly registered user now attempts to login
        logginin = self.client.post('/login/', {'username': self.username,
            'password': self.password}, follow=True)
        self.assertIn(self.username, logginin.content)


class ProfileTest(TestCase):
    """Tests for Profile view"""
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

    def test_count_no_photos(self):
        viewprof = self.client.get('/profile/')
        self.assertIn('>0</', viewprof.content)
        # Should do this check; a non logged in response could potentially
        # also display zero photos
        self.assertIn(self.username, viewprof.content)

    def test_count_photos_no_albums(self):
        viewprof = self.client.get('/profile/')
         # Add a couple photos to the user we created
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        response = self.client.get('/profile/')

        # Number of photos
        self.assertIn('>2</', response.content)
        # Number of albums
        self.assertIn('>0</', response.content)

    def test_count_photos_one_albums(self):
        viewprof = self.client.get('/profile/')

        # Add a couple photos to the user we created
        photo1 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        photo2 = PhotoFactory.create(owner=self.user, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        photo1.save()
        photo2.save()
        album = AlbumFactory.create(owner=self.user, cover=photo1)
        album.save()
        album.photos = [photo1, photo2]
        response = self.client.get('/profile/')

        # Number of photos
        self.assertIn('>2</', response.content)
        # Number of albums
        self.assertIn('>1</', response.content)

    def test_check_links(self):
        response = self.client.get('/profile/')
        self.assertIn('href="/images/library/"', response.content)

    def test_profile_after_user_login(self):
        self.assertEqual(self.login.wsgi_request.path, '/profile/')


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
