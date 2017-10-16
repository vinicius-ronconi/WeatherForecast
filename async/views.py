from django.views.generic import View

from async.controllers import AsyncController
from utils.decorators import render_to_json


class AsyncResultView(View):
    controller = AsyncController()

    @render_to_json
    def get(self, request):
            return self.controller.get_async_task_status_from_request(request)
