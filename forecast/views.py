from django.views.generic import View

from forecast.factory import ForecastFactory
from forecast.controllers import ReactAppController
from utils.decorators import render_to_json


class ForecastView(View):
    controller = ForecastFactory().make_forecast_controller()

    @render_to_json
    def get(self, request):
        return self.controller.get_forecast(request)


class DashboardView(View):
    controller = ReactAppController()

    def get(self, _):
        return self.controller.get_react_app()
