import json

from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class LoginAndLogoutTestCases(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_login(self):
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(_res['username'], 'test')

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.is_email_verified = True
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_login_not_verified_email(self):
        self.user.is_active = True
        self.user.is_email_verified = False
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_logout(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')

    def test_logout_not_logged_in(self):
        self.client.logout()
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')


class CheckIfAuthenticatedTestCases(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com')
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()

    def test_check_if_authenticated_true(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'true')

    def test_check_if_authenticated_false(self):
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'false')


class RegisterTestCases(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()

    def test_register_success(self):
        response = self.client.post(
            '/auth/register/',
            {
                'username': 'test', 'password1': 'testtesttest',
                'password2': 'testtesttest', 'email': 'test@test.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'unknown')
        self.assertEqual(len(mail.outbox), 1)
        url = mail.outbox[0].message().as_string().split('\n')[-1]
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.post(
            '/auth/login/', {'username': 'test', 'password': 'testtesttest'}
        )
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'true')

    def test_register_username_exists(self):
        self.UserModel.objects.create_user(
            username='test4', password='test', email='test4@test.com'
        )
        response = self.client.post(
            '/auth/register/',
            {
                'username': 'test4', 'password1': 'test',
                'password2': 'test', 'email': 'test4@test.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_register_email_exists(self):
        self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        response = self.client.post(
            '/auth/register/',
            {
                'username': 'test3', 'password1': 'test',
                'password2': 'test', 'email': 'test3@test.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_register_invalid_password(self):
        response = self.client.post(
            '/auth/register/',
            {
                'username': 'test5', 'password1': 'test',
                'password2': 'test', 'email': 'test5@test.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_register_unverified_email_login(self):
        response = self.client.post(
            '/auth/register/',
            {
                'username': 'test2', 'password1': '0s5I6vjDCKeo',
                'password2': '0s5I6vjDCKeo', 'email': 'test2@test.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'unknown')
        self.assertEqual(len(mail.outbox), 1)
        self.client.post(
            '/auth/login/', {'username': 'test2', 'password': '0s5I6vjDCKeo'}
        )
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'false')


class VerifyEmailTestCases(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()

    def test_verify_email_failure(self):
        response = self.client.get(
            '/auth/verify/asdf/adsfasdfasdfasdfasdfasdf/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')


class ForgotPasswordTestCases(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()

    def test_forgot_password_success(self):
        self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com'
        )

        response = self.client.post(
            "/auth/reset/",
            {'email': 'test@test.com'}
        )

        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(len(mail.outbox), 1)
        url = mail.outbox[0].message().as_string().split('\n')[-1]
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        uidb64 = url.split('/')[-3]
        token = url.split('/')[-2]
        response = self.client.post(
            '/auth/reset/confirm/',
            {
                'password1': 'testtesttest',
                'password2': 'testtesttest',
                'uidb64': uidb64,
                'token': token
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.client.post(
            '/auth/login/', {'username': 'test', 'password': 'testtesttest'}
        )
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'true')

    def test_forgot_password_failure(self):
        response = self.client.post(
            "/auth/reset/",
            {'email': 'dummy@test.com'}
        )

        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(len(mail.outbox), 0)

    def test_forgot_password_logged_in(self):
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.user.is_email_verified = True
        self.user.is_active = True
        self.user.save()

        self.client.post(
            '/auth/login/', {'username': 'test', 'password': 'test'}
        )

        response = self.client.post(
            "/auth/reset/",
            {'email': 'test@test.com'}
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, 'logged in')

    def test_forgot_password_confirm_bad_token(self):
        response = self.client.post(
            '/auth/reset/confirm/',
            {
                'password1': 'testtesttest',
                'password2': 'testtesttest',
                'uidb64': 'asldkfj',  # invalid data
                'token': 'asldfjalskdfjalsjkdfl;a'  # invalid data
            }
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')
        self.assertEqual(len(mail.outbox), 0)
