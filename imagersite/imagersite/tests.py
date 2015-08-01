from django.test import Client, TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
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


class HomeExists(TestCase):
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


class HomeRandomPhotos(TestCase):
    """Test for random photo selection on website"""
    def setUp(self):
        self.client = Client()
        owner = UserFactory.create()
        owner.save()
        self.photo1 = PhotoFactory.create(owner=owner, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=owner, privacy='Public',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()

    def test_random_photo_in_site(self):
        pics = set()
        for i in range(100):
            response = self.client.get('/')
            pics.add(response.context['pic_url'])
        self.assertEqual(len(pics), 2)


class HomeStaticPhoto(TestCase):
    """Test for static photo on website"""
    def setUp(self):
        self.client = Client()

    def test_random_photo_in_site(self):
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
    """Test for Profile view"""
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
