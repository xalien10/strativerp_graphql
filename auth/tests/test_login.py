from django.test import Client
from django.test.testcases import SimpleTestCase, TestCase
from django.urls import reverse

from user.models import User
from utils.urls import names


class TestUrls(TestCase):
    client = Client()
    user = {
        'username': 'apon@strativ.se',
        'password': 'Apon1234'
        # 'password': 'pbkdf2_sha256$150000$7i0Mi8EjeSNx$BjjrSnMefRKvJJEkvBFJIGC6yqVMTpfWbdihm2zWd/A='
    }

    def setUp(self):
        u = User.objects.create(username=self.user.get('username'), password=self.user.get('password'))
        u.set_password(self.user.get('password'))
        u.save()
        login = self.client.login(username=self.user.get('username'), password=self.user.get('password'))
        print(login)

    def test_logout(self):
        response = self.client.get('/logout/')
        print(response)
        self.assertEquals(response.status_code, 200)
        pass
