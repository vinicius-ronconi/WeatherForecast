from celery.result import AsyncResult
from django.core.exceptions import ValidationError


class AsyncController(object):
    def get_async_task_status_from_request(self, request):
        request = self._validate_status_request(request)
        response = self.get_async_task_status_by_result(AsyncResult(request.GET.get('result_id')))
        return response

    def get_async_task_status_by_result(self, result):
        """
        :type result: celery.result.AsyncResult
        :return: dict
        """
        return self._make_async_result_response(result)

    @staticmethod
    def _validate_status_request(request):
        if not request.GET.get('result_id'):
            raise ValidationError('result_id parameter not found.')
        return request

    @staticmethod
    def _make_async_result_response(async_result):
        return {
            'result_id': async_result.id,
            'result_status': async_result.status,
            'result_is_ready': async_result.ready(),
            'result': async_result.result if async_result.successful() else None
        }
