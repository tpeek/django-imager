import unittest
from django.test import Client
from imager_images.models import Photo
from imager_profile.models import User
import factory
from faker import Factory as FakeFaker
from django.conf import settings
import os

fake = FakeFaker.create()


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo
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


class HomeExists(unittest.TestCase):
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


class HomeRandomPhotos(unittest.TestCase):
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

    def tearDown(self):
        self.photo1.delete()
        self.photo2.delete()

    def test_random_photo_in_site(self):
        pics = set()
        for i in range(100):
            response = self.client.get('/')
            pics.add(response.context['pic_url'])
        print pics
        self.assertEqual(len(pics), 2)


class HomeStaticPhoto(unittest.TestCase):
    """Test for static photo on website"""
    def setUp(self):
        self.client = Client()

    def test_random_photo_in_site(self):
        pics = set()
        for i in range(100):
            response = self.client.get('/')
            pics.add(response.context['pic_url'])
        print pics
        self.assertEqual(len(pics), 1)
        self.assertIn('demo.jpg', pics)


class LoginExists(unittest.TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()

    def test_self_exists(self):
        response = self.client.get('/login', follow=True)
        self.assertEqual(response.status_code, 200)


class LogoutExists(unittest.TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()

    def test_self_exists(self):
        response = self.client.get('/logout', follow=True)
        self.assertEqual(response.status_code, 200)


class RegisterUser(unittest.TestCase):
    """Test for 200 OK at '/'"""
    def setUp(self):
        self.client = Client()
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()

    def test_register_user(self):
        submitdis = self.client.post('/register/', {'username': self.username, 
            'password1': self.password, 'password2': self.password,
            'email': self.email}, follow=True)
        #print submitdis.content, submitdis.status_code
