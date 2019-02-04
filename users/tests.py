from django.core.management import call_command
from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User

class LoginTestCase(TestCase):
        
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = Client()
        call_command(
            'loaddata',
            'users/fixtures/users-fixture.json'
        )

    def test_correct_login(self):
        response = self.client.post('/rest-auth/login/',{'password':'usertest1pass', 'email':'usertest1@mail.com'})
        self.assertEqual(response.status_code, 200)

    def test_incorrect_password_login(self):
        response = self.client.post('/rest-auth/login/',{'password':'incorrectpass', 'email':'usertest1@mail.com'})
        self.assertEqual(response.status_code, 400)
