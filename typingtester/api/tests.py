"""api.tests
Test cases for the api application.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Quote


class TestQuoteLoader(TestCase):
    """
    Tests for the quote loader.
    """

    def setUp(self):
        self.quote = Quote.objects.create(content='test')

    def test_load_quote(self):
        """Tests the quote loader."""
        response = self.client.get('/api/load/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in response.data)
        self.assertTrue('words' in response.data)
        self.assertEqual(response.data['words'], ['test'])
        self.assertContains(response, response.data['id'], 1)


class TestCsrfRequest(TestCase):
    """
    Tests for the csrf token loader view.
    """

    def test_csrf_request(self):
        """Tests the csrf token loader view."""
        response = self.client.get('/api/csrf/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)


class TestStartedTest(TestCase):
    """
    Tests for the started test view.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_started_test_not_logged_in(self):
        """
        Tests that the started test view requires the user to be logged in.
        but the user is not logged in.
        """
        response = self.client.post('/api/started-test/')
        self.assertEqual(response.status_code, 403)

    def test_started_test(self):
        """
        Tests that the started test view requires the user to be logged in.
        and the user is logged in.
        """
        self.client.login(username='test', password='test')
        response = self.client.post('/api/started-test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.user_model.objects.get(username='test')
        self.assertEqual(updated_user.statistics.tests_started, 1)


class TestCompletedTest(TestCase):
    """
    Tests for the completed test view.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@example.com')

    def test_completed_test_not_logged_in(self):
        """
        Tests that the completed test view requires the user to be logged in.
        but the user is not logged in.
        """
        response = self.client.post('/api/completed-test/')
        self.assertEqual(response.status_code, 403)

    def test_completed_test(self):
        """
        Tests that the completed test view requires the user to be logged in.
        and the user is logged in.
        """
        self.client.login(username='test', password='test')
        response = self.client.post('/api/completed-test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.user_model.objects.get(username='test')
        self.assertEqual(updated_user.statistics.tests_completed, 1)


class TestUpdateTotalTestsTime(TestCase):
    """
    tests the update total tests time view.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_update_total_tests_time_not_logged_in(self):
        """
        Tests that the update total tests time view requires the user to be
        logged in, but the user is not logged in.
        """
        response = self.client.post(
            '/api/update-total-tests-time/', {'time': 10})
        self.assertEqual(response.status_code, 403)

    def test_update_total_tests_time(self):
        """
        Tests that the update total tests time view requires the user to be
        logged in, and the user is logged in.
        and the time is a valid value.
        """
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/api/update-total-tests-time/', {'time': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.user_model.objects.get(username='test')
        self.assertEqual(updated_user.statistics.time_typing, 10)

    def test_update_total_tests_time_with_negative_time(self):
        """
        Tests that the update total tests time view requires the user to be
        logged in, and the user is logged in.
        and the time is a invalid value.
        """
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/api/update-total-tests-time/', {'time': -10})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], 'false')
        updated_user = self.user_model.objects.get(username='test')
        self.assertEqual(updated_user.statistics.time_typing, 0)


class TestInsertUserTest(TestCase):
    """
    Tests for the insert user test view.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.quote = Quote(content='test')
        self.quote.save()

    def test_insert_user_test_not_logged_in(self):
        """
        Tests that the insert user test view requires the user to be logged in,
        but the user is not logged in.
        """
        response = self.client.post(
            '/api/insert-user-test/',
            {
                'quote_id': self.quote.id,  # pylint: disable=no-member
                'time': 10,
                'cpm': 10,
                'acc': 10
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_insert_user_test(self):
        """
        Tests that the insert user test view requires the user to be logged in,
        and the user is logged in.
        and the data is valid.
        """
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/api/insert-user-test/',
            {
                'quote_id': self.quote.id,  # pylint: disable=no-member
                'time': 10,
                'cpm': 10,
                'acc': 10
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.user_model.objects.get(username='test')
        self.assertEqual(updated_user.tests.count(), 1)
        test = updated_user.tests.all()[0]
        self.assertEqual(test.time, 10)
        self.assertEqual(test.cpm, 10)
        self.assertEqual(test.accuracy, 10)
        self.assertEqual(test.user_id, self.user.id)

    def test_insert_user_test_with_invalid_data(self):
        """
        Tests that the insert user test view requires the user to be logged in,
        and the user is logged in.
        and the data is invalid.
        """
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/api/insert-user-test/',
            {
                'quote_id': -1,
                'time': -10,
                'cpm': -10,
                'acc': -10
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], 'false')
        updated_user = self.user_model.objects.get(username='test')
        self.assertEqual(updated_user.tests.count(), 0)


class TestLoadStatistics(TestCase):
    """
    Tests for the load statistics view.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com'
        )

    def test_load_statistics_not_logged_in(self):
        """
        Tests that the load statistics view requires the user to be logged in,
        but the user is not logged in.
        """
        response = self.client.post('/api/load-statistics/')
        self.assertEqual(response.status_code, 403)

    def test_load_statistics(self):
        """
        Tests that the load statistics view requires the user to be logged in,
        and the user is logged in.
        """
        self.client.login(username='test', password='test')
        response = self.client.post('/api/load-statistics/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tests_started' in response.data)
        self.assertTrue('tests_completed' in response.data)
        self.assertTrue('time_typing' in response.data)
        self.assertEqual(response.data['tests_started'], 0)
        self.assertEqual(response.data['tests_completed'], 0)
        self.assertEqual(response.data['time_typing'], 0)
        self.client.post('/api/started-test/')
        self.client.post('/api/completed-test/')
        self.client.post('/api/update-total-tests-time/', {'time': 10})
        response = self.client.post('/api/load-statistics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tests_started'], 1)
        self.assertEqual(response.data['tests_completed'], 1)
        self.assertEqual(response.data['time_typing'], 10)


class TestLoadUserTests(TestCase):
    """
    Tests for the load user tests view.
    """

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.quote = Quote(content='test')
        self.quote.save()

    def test_load_user_tests_not_logged_in(self):
        """
        Tests that the load user tests view requires the user to be logged in,
        but the user is not logged in.
        """
        response = self.client.get('/api/load-test-records/')
        self.assertEqual(response.status_code, 403)

    def test_load_user_tests(self):
        """
        Tests that the load user tests view requires the user to be logged in,
        and the user is logged in.
        """
        self.client.login(username='test', password='test')
        response = self.client.get('/api/load-test-records/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
        self.client.post(
            '/api/insert-user-test/',
            {
                'quote_id': self.quote.id,  # pylint: disable=no-member
                'time': 10,
                'cpm': 10,
                'acc': 10
            }
        )
        response = self.client.get('/api/load-test-records/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['time'], 10)
        self.assertEqual(response.data[0]['cpm'], 10)
        self.assertEqual(response.data[0]['accuracy'], 10)
        self.assertEqual(response.data[0]['quote_id'],
                         self.quote.id)  # pylint: disable=no-member
        self.assertTrue('date' in response.data[0])
