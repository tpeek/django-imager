from django.test import Client, TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
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


class AccessTest(TestCase):
    def setUp(self):
        # Setting up for user #1 who has private photos and album
        self.client1 = Client()
        self.username1 = fake.user_name()
        self.password1 = fake.password()
        self.email1 = fake.email()
        self.user1 = User.objects.create_user(username=self.username1,
            password=self.password1, email=self.email1)
        self.photo1 = PhotoFactory.create(owner=self.user1, privacy='Private',
            file=os.path.join(settings.MEDIA_ROOT, 'amoosing.jpg'))
        self.photo2 = PhotoFactory.create(owner=self.user1, privacy='Private',
            file=os.path.join(settings.MEDIA_ROOT, 'googlephoto.jpg'))
        self.photo1.save()
        self.photo2.save()
        self.album = AlbumFactory.create(owner=self.user1, cover=self.photo1,
            privacy="Private")
        self.album.save()
        self.album.photos = [self.photo1, self.photo2]
        # Setting up for user #2 who has no photos
        self.client2 = Client()
        self.username2 = fake.user_name()
        self.password2 = fake.password()
        self.email2 = fake.email()
        self.user2 = User.objects.create_user(username=self.username2,
            password=self.password2, email=self.email2)
        self.login2 = self.client2.post('/login/', {'username': self.username2,
            'password': self.password2}, follow=True)

    def test_photo_access(self):
        response1 = self.client2.get('/images/photos/{}/'.format(
            self.photo1.id), follow=True)
        response2 = self.client2.get('/images/photos/{}/'.format(
            self.photo2.id), follow=True)
        response3 = self.client2.get('/images/photos/{}/edit/'.format(
            self.photo1.id), follow=True)
        response4 = self.client2.get('/images/photos/{}/edit/'.format(
            self.photo2.id), follow=True)
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(response3.status_code, 403)
        self.assertEqual(response4.status_code, 403)

    def test_album_access(self):
        response1 = self.client2.get(
            '/images/albums/{}/'.format(self.album.id))
        response2 = self.client2.get(
            '/images/albums/{}/edit/'.format(self.album.id))
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)
