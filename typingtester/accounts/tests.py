import json

from django.test import TestCase, client
from django.contrib.auth import get_user_model


class LoginAndLogoutTestCases(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = client.Client()
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
