from django.shortcuts import render_to_response
from django.views.generic import View

from forecast.factory import ForecastFactory
from utils.decorators import render_to_json


class ForecastView(View):
    controller = ForecastFactory().make_forecast_controller()

    @render_to_json
    def get(self, request):
        return self.controller.get_forecast(request)


def dashboard(request):
    return render_to_response('dashboard/react_dashboard.html')
