from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Quote


class TestQuoteLoader(TestCase):

    def setUp(self):
        self.client = Client()
        self.quote = Quote.objects.create(content='test')

    def test_load_quote(self):
        response = self.client.get('/api/load/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in response.data)
        self.assertTrue('words' in response.data)
        self.assertEqual(response.data['words'], ['test'])
        self.assertContains(response, response.data['id'], 1)


class TestCsrfRequest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_csrf_request(self):
        response = self.client.get('/api/csrf/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)


class TestStartedTest(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_started_test_not_logged_in(self):
        response = self.client.post('/api/started-test/')
        self.assertEqual(response.status_code, 403)

    def test_started_test(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/api/started-test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.UserModel.objects.get(username='test')
        self.assertEqual(updated_user.statistics.tests_started, 1)


class TestCompletedTest(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@example.com')

    def test_completed_test_not_logged_in(self):
        response = self.client.post('/api/completed-test/')
        self.assertEqual(response.status_code, 403)

    def test_completed_test(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/api/completed-test/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.UserModel.objects.get(username='test')
        self.assertEqual(updated_user.statistics.tests_completed, 1)


class TestUpdateTotalTestsTime(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com')

    def test_update_total_tests_time_not_logged_in(self):
        response = self.client.post(
            '/api/update-total-tests-time/', {'time': 10})
        self.assertEqual(response.status_code, 403)

    def test_update_total_tests_time(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/api/update-total-tests-time/', {'time': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.UserModel.objects.get(username='test')
        self.assertEqual(updated_user.statistics.time_typing, 10)


class TestInsertUserTest(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.quote = Quote(content='test')
        self.quote.save()

    def test_insert_user_test_not_logged_in(self):
        response = self.client.post(
            '/api/insert-user-test/', {'quote_id': self.quote.id, 'time': 10, 'cpm': 10, 'acc': 10})
        self.assertEqual(response.status_code, 403)

    def test_insert_user_test(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            '/api/insert-user-test/', {'quote_id': self.quote.id, 'time': 10, 'cpm': 10, 'acc': 10})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], 'true')
        updated_user = self.UserModel.objects.get(username='test')
        test = updated_user.tests.all()[0]
        self.assertEqual(test.time, 10)
        self.assertEqual(test.cpm, 10)
        self.assertEqual(test.accuracy, 10)
        self.assertEqual(test.user_id, self.user.id)


class TestLoadStatistics(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com'
        )

    def test_load_statistics_not_logged_in(self):
        response = self.client.post('/api/load-statistics/')
        self.assertEqual(response.status_code, 403)

    def test_load_statistics(self):
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

    def setUp(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.user = self.UserModel.objects.create_user(
            username='test', password='test', email='test@test.com'
        )
        self.quote = Quote(content='test')
        self.quote.save()

    def test_load_user_tests_not_logged_in(self):
        response = self.client.post('/api/load-test-records/')
        self.assertEqual(response.status_code, 403)

    def test_load_user_tests(self):
        self.client.login(username='test', password='test')
        response = self.client.post('/api/load-test-records/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
        self.client.post('/api/insert-user-test/',
                         {'quote_id': self.quote.id, 'time': 10, 'cpm': 10, 'acc': 10})
        response = self.client.post('/api/load-test-records/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['time'], 10)
        self.assertEqual(response.data[0]['cpm'], 10)
        self.assertEqual(response.data[0]['acc'], 10)
        self.assertEqual(response.data[0]['quote_id'], self.quote.id)
