"""accounts.tests
Test Cases Defined for Accounts Application
"""

import json

from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode


class LoginAndLogoutTestCases(TestCase):
    """Login and Logout Test Cases"""

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_login(self):
        """
        Test Login if the user is active and his/her email is verified
        and the credentials are valid
        """
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(_res['username'], 'test')

    def test_login_wrong_password(self):
        """Test Login with wrong password"""
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test1'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_login_inactive_user(self):
        """test login if the user is inactive"""
        self.user.is_active = False
        self.user.is_email_verified = True
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_login_not_verified_email(self):
        """test login if the user's email is not verified"""
        self.user.is_active = True
        self.user.is_email_verified = False
        self.user.save()
        response = self.client.post('/auth/login/',
                                    {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_logout(self):
        """Test Logout if the user is logged in"""
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')

    def test_logout_not_logged_in(self):
        """Test Logout if the user is not logged in"""
        self.client.logout()
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')


class CheckIfAuthenticatedTestCases(TestCase):
    """
    Test the CheckIfAuthenticated view
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com')
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()

    def test_check_if_authenticated_true(self):
        """Test if the user is authenticated"""
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'true')

    def test_check_if_authenticated_false(self):
        """Test if the user is not authenticated"""
        response = self.client.post('/auth/check/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['Authenticated'], 'false')


class RegisterTestCases(TestCase):
    """Test cases for registering a new user"""

    def setUp(self):
        self.user_model = get_user_model()

    def test_register_success(self):
        """Test a successful registration"""
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
        """Test if the username already exists"""
        self.user_model.objects.create_user(
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
        """Test if the email already exists"""
        self.user_model.objects.create_user(
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
        """Test if the password is invalid"""
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
        """Test if the user's email is not verified"""
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
    """Test cases for verifying a user's email"""

    def setUp(self):
        self.user_model = get_user_model()

    def test_verify_email_failure(self):
        """Test if the verification link is invalid"""
        response = self.client.get(
            '/auth/verify/asdf/adsfasdfasdfasdfasdfasdf/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')


class ForgotPasswordTestCases(TestCase):
    """Test cases for resetting a user's password"""

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com'
        )

    def test_forgot_password_success(self):
        """Test a successful password reset"""
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
        """Test a if the email address is invalid"""
        response = self.client.post(
            "/auth/reset/",
            {'email': 'dummy@test.com'}
        )

        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(len(mail.outbox), 0)

    def test_forgot_password_logged_in(self):
        """Test if the user is already logged in"""
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
        """Test if the token or uidb64 is invalid"""
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


class FetchUserInformationTestCase(TestCase):
    """Test cases for fetching user information"""

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()

    def test_fetch_user_information_success(self):
        """Test if the user information is fetched successfully"""
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/user/info/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(_res['username'], 'test')
        self.assertEqual(_res['email'], 'test@test.com')

    def test_fetch_user_information_notloggedin(self):
        """Test if the user information is fetched successfully"""
        response = self.client.post('/auth/user/info/')
        self.assertEqual(response.status_code, 401)

    def test_fetch_user_information_notverified(self):
        """Test if the user information is fetched successfully"""
        self.user.is_email_verified = False
        self.user.save()
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/user/info/')
        self.assertEqual(response.status_code, 403)


class ChangePasswordTestCases(TestCase):
    """Test cases for changing a user's password"""

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()

    def test_change_password_success(self):
        """Test if the user's password is changed successfully"""
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/auth/password/change/',
            {'old_password': 'test', 'new_password1': 'testtesttest',
             'new_password2': 'testtesttest'}
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')

    def test_change_password_failure(self):
        """Test if the user's password is not changed successfully
        because of invalid old password"""
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/auth/password/change/',
            {'old_password': 'test2', 'new_password1': 'testtesttest',
             'new_password2': 'testtesttest'}
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')

    def test_change_password_notloggedin(self):
        """Test if the user's password is not changed successfully
        because of not being logged in"""
        response = self.client.post(
            '/auth/password/change/',
            {'old_password': 'test', 'new_password1': 'testtesttest',
             'new_password2': 'testtesttest'}
        )
        self.assertEqual(response.status_code, 401)

    def test_change_password_old_password_equal_new_password(self):
        """Test if the user's password is not changed successfully
        because of old password is equal to new password"""
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/auth/password/change/',
            {'old_password': 'test', 'new_password1': 'test',
             'new_password2': 'test'}
        )
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')


class ResendVerificationEmail(TestCase):
    """Test cases for resending verification email"""

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_resend_verification_email_success(self):
        """Test if the verification email is sent successfully"""
        session = self.client.session
        session['_id'] = urlsafe_base64_encode(str(self.user.id).encode())
        session.save()
        response = self.client.post('/auth/resend/verification/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'true')
        self.assertEqual(len(mail.outbox), 1)

    def test_resend_verification_email_no_session_id(self):
        """Test if the verification email is not sent successfully
        because there is no session id"""
        response = self.client.post('/auth/resend/verification/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')
        self.assertEqual(len(mail.outbox), 0)

    def test_resend_verification_email_logged_in(self):
        """Test if the verification email is not sent successfully
        because the user is logged in"""
        self.client.login(username='test', password='test')
        response = self.client.post('/auth/resend/verification/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')
        self.assertEqual(len(mail.outbox), 0)

    def test_resend_verification_email_already_verified(self):
        """Test if the verification email is not sent successfully
        because the user is already verified"""
        self.user.is_email_verified = True
        self.user.save()
        session = self.client.session
        session['_id'] = urlsafe_base64_encode(str(self.user.id).encode())
        session.save()
        response = self.client.post('/auth/resend/verification/')
        self.assertEqual(response.status_code, 200)
        _res = json.loads(response.content)
        self.assertEqual(_res['success'], 'false')
        self.assertEqual(len(mail.outbox), 0)
