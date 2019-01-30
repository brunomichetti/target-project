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
        response = self.client.post(
            '/rest-auth/login/', {'password': 'usertest1pass', 'email': 'usertest1@mail.com'})
        self.assertEqual(response.status_code, 200)

    def test_incorrect_password_login(self):
        response = self.client.post(
            '/rest-auth/login/', {'password': 'incorrectpass', 'email': 'usertest1@mail.com'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0]
                         [0:], 'Unable to log in with provided credentials.')


class SignUpTestCase(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = Client()
        call_command(
            'loaddata',
            'users/fixtures/users-fixture.json'
        )

    def test_correct_sign_up(self):
<<<<<<< HEAD
        response = self.client.post('/rest-auth/registration/', {'email': 'new-user@mail.com', 
        'password1': 'new-user-pass', 'password2': 'new-user-pass', 'name': 'New User', 'gender': 'M'})
        self.assertEqual(response.status_code, 201)

    def test_already_registered_error(self):
        response = self.client.post('/rest-auth/registration/', {'email': 'usertest1@mail.com', 
        'password1': 'new-user-pass', 'password2': 'new-user-pass', 'name': 'New User', 'gender': 'M'})
=======
        response = self.client.post('/rest-auth/registration/', {'email': 'new-user@mail.com', 'password1': 'new-user-pass', 'password2': 'new-user-pass',
                                                                 'name': 'New User', 'gender': 'M'})
        self.assertEqual(response.status_code, 201)

    def test_already_registered_error(self):
        response = self.client.post('/rest-auth/registration/', {'email': 'usertest1@mail.com', 'password1': 'new-user-pass', 'password2': 'new-user-pass',
                                                                 'name': 'New User', 'gender': 'M'})
>>>>>>> efad8eb... sign-up
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['email'][0][0:], 'A user is already registered with this e-mail address.')

    def test_not_matching_passwords_error(self):
<<<<<<< HEAD
        response = self.client.post('/rest-auth/registration/', {'email': 'new-user@mail.com', 
        'password1': 'new-user-pass', 'password2': 'different-pass', 'name': 'New User', 'gender': 'M'})
=======
        response = self.client.post('/rest-auth/registration/', {'email': 'new-user@mail.com', 'password1': 'new-user-pass', 'password2': 'different-pass',
                                                                 'name': 'New User', 'gender': 'M'})
>>>>>>> efad8eb... sign-up
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors']
                         [0][0:], "The two password fields didn't match.")

    def test_missing_fields_sign_up_error(self):
<<<<<<< HEAD
        response = self.client.post('/rest-auth/registration/', {'email': 'new-user@mail.com', 
        'password1': 'new-user-pass', 'password2': 'different-pass', 'gender': 'M'})
=======
        response = self.client.post('/rest-auth/registration/', {'email': 'new-user@mail.com', 'password1': 'new-user-pass', 'password2': 'different-pass',
                                                                 'gender': 'M'})
>>>>>>> efad8eb... sign-up
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0]
                         [0:], 'This field is required.')
