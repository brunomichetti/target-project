from django.core.management import call_command
from django.test import TestCase, Client
from django.test.utils import override_settings

from target import settings
from users.models import CustomUser


class SetUpUsersTestsClass(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.client = Client()
        call_command(
            'loaddata',
            'users/fixtures/users-fixture.json'
        )

    def login(self, email, password):
        return self.client.post(
            '/rest-auth/login/',
            {'email': email, 'password': password}
        )

    def signup(self, email, password1, password2, name, gender, id_n):
        return self.client.post(
            '/rest-auth/registration/',
            {'email': email,
             'password1': password1,
             'password2': password2,
             'name': name,
             'gender': gender,
             'id_notifications': id_n}
        )

    def logout(self):
        return self.client.post('/rest-auth/logout/')

    def update_logged_user(self, new_name, new_gender):
        return self.client.put(
            '/rest-auth/user/',
            data={"name": new_name, "gender": new_gender},
            content_type='application/json'
        )

    def send_email_for_password_reset(self, email):
        return self.client.post('/rest-auth/password/reset/', {'email': email})

    def reset_password(self, uid, token, new_password1, new_password2):
        return self.client.post(
            '/rest-auth/password/reset/confirm/',
            {'uid': uid,
             'token': token,
             'new_password1': new_password1,
             'new_password2': new_password2}
        )


@override_settings(
    ACCOUNT_EMAIL_VERIFICATION='optional')
class LoginTestCase(SetUpUsersTestsClass):

    def test_correct_login(self):
        response = self.login('usertest1@mail.com', 'usertest1pass')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_password_login(self):
        response = self.login('usertest1@mail.com', 'incorrectpass')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0]
                         [0:], 'Unable to log in with provided credentials.')


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
class SignUpTestCase(SetUpUsersTestsClass):

    def test_correct_sign_up(self):
        response = self.signup('new-user@mail.com', 'new-user-pass',
                               'new-user-pass', 'New User', 'M', 'testtoken')
        confirmation_key = response.context['key']
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Verification e-mail sent.')
        self.assertTrue(CustomUser.objects.filter(
            email='new-user@mail.com').exists())
        self.client.post('/rest-auth/registration/verify-email/',
                         {'key': confirmation_key})
        response = self.login('new-user@mail.com', 'new-user-pass')
        self.assertEqual(response.status_code, 200)

    def test_email_not_verified_error(self):
        response = self.signup('new-user@mail.com', 'new-user-pass',
                               'new-user-pass', 'New User', 'M', 'testtoken')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['detail'], 'Verification e-mail sent.')
        response = self.login('new-user@mail.com', 'new-user-pass')
        self.assertEqual(response.data['non_field_errors'][0]
                         [0:], 'E-mail is not verified.')

    def test_already_registered_error(self):
        response = self.signup('usertest1@mail.com', 'new-user-pass',
                               'new-user-pass', 'New User', 'M', 'testtoken')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0][0:],
                         'A user is already registered '
                         'with this e-mail address.')

    def test_not_matching_passwords_error(self):
        response = self.signup('new-user@mail.com', 'new-user-pass',
                               'different-pass', 'New User', 'M', 'testtoken')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors']
                         [0][0:], "The two password fields didn't match.")

    def test_missing_fields_sign_up_error(self):
        response = self.client.post(
            '/rest-auth/registration/',
            {'email': 'new-user@mail.com',
             'password1': 'new-user-pass',
             'password2': 'different-pass',
             'gender': 'M'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0]
                         [0:], 'This field is required.')


@override_settings(
    ACCOUNT_EMAIL_VERIFICATION='optional')
class LogoutTestCase(SetUpUsersTestsClass):

    def test_correct_logout(self):
        response = self.login('usertest1@mail.com', 'usertest1pass')
        self.assertEqual(response.status_code, 200)
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['detail'], 'Successfully logged out.')


@override_settings(
    ACCOUNT_EMAIL_VERIFICATION='optional')
class TestUpdateProfile(SetUpUsersTestsClass):

    def test_correct_update_profile(self):
        response = self.login('usertest1@mail.com', 'usertest1pass')
        self.assertEqual(response.status_code, 200)
        response = self.update_logged_user('New Name', 'M')
        self.assertEqual(response.status_code, 200)
        current_user = CustomUser.objects.get(email='usertest1@mail.com')
        self.assertEqual(current_user.name, 'New Name')
        self.assertEqual(current_user.gender, 'M')

    def test_not_logged_user_error(self):
        response = self.update_logged_user('New Name', 'M')
        self.assertEqual(response.status_code, 403)

    def test_correct_update_profile_with_missing_field(self):
        response = self.login('usertest1@mail.com', 'usertest1pass')
        self.assertEqual(response.status_code, 200)
        response = self.client.put(
            '/rest-auth/user/',
            data={"name": "New Name"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        current_user = CustomUser.objects.get(email='usertest1@mail.com')
        self.assertEqual(current_user.name, 'New Name')
        self.assertEqual(current_user.gender, 'F')

    def test_incorrect_gender_update_profile(self):
        response = self.login('usertest1@mail.com', 'usertest1pass')
        self.assertEqual(response.status_code, 200)
        response = self.update_logged_user('New Name', 'Wrong')
        self.assertEqual(response.status_code, 400)
        current_user = CustomUser.objects.get(email='usertest1@mail.com')
        self.assertEqual(current_user.name, 'User ForTest')
        self.assertEqual(current_user.gender, 'F')


@override_settings(
    ACCOUNT_EMAIL_VERIFICATION='optional',
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
class TestResetPassword(SetUpUsersTestsClass):

    def test_correct_reset_password(self):
        response = self.send_email_for_password_reset('usertest1@mail.com')
        self.assertEqual(response.data['detail'],
                         'Password reset e-mail has been sent.')
        uid_reset = response.context['uid']
        token_reset = response.context['token']
        response = self.reset_password(
            uid_reset,
            token_reset,
            'new_pass_for_test1',
            'new_pass_for_test1'
        )
        self.assertEqual(response.status_code, 200)
        response = self.login('usertest1@mail.com', 'new_pass_for_test1')
        self.assertEqual(response.status_code, 200)

    def test_not_matching_password_reset_error(self):
        response = self.send_email_for_password_reset('usertest1@mail.com')
        uid_reset = response.context['uid']
        token_reset = response.context['token']
        response = self.reset_password(
            uid_reset, token_reset,
            'new_pass_for_test1',
            'new_pass_for_test1_not_matching'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['new_password2'][0]
                         [0:], "The two password fields didn't match.")

    def test_incorrect_token_reset_password_error(self):
        response = self.send_email_for_password_reset('usertest1@mail.com')
        uid_reset = response.context['uid']
        token_reset = response.context['token']
        token_reset = token_reset + 'incorrect'
        response = self.reset_password(
            uid_reset,
            token_reset,
            'new_pass_for_test1',
            'new_pass_for_test1'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['token'][0]
                         [0:], 'Invalid value')
