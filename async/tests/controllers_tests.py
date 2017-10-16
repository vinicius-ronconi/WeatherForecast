import mock
from django.core.urlresolvers import reverse
from django.test import TestCase


class AsyncControllerTestCase(TestCase):
    def setUp(self):
        self._mock_async_result()

    def test_it_gets_async_task_status_from_request(self):
        response = self.client.get(reverse('async_status'))
        content = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('result_id', content.get('error'))

        response = self.client.get(reverse('async_status'), data={'result_id': 'qwe-123-asd'})
        content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('error', content)
        self.assertIn('result_id', content)

    def _mock_async_result(self):
        self.mocked_async_result = mock.Mock(return_value=MockedAsyncResult('my_result_id', status='PENDING'))
        async_result_patcher = mock.patch('async.controllers.AsyncResult', self.mocked_async_result)
        async_result_patcher.start()
        self.addCleanup(async_result_patcher.stop)


class MockedAsyncResult(object):
    result = ''
    is_successful = False

    def __init__(self, result_id, status):
        self.id = result_id
        self.status = status
        self.is_ready = status in ['SUCCESS', 'FAILURE']
        self.is_successful = status == 'SUCCESS'

    def ready(self):
        return self.is_ready

    def successful(self):
        return self.is_successful
