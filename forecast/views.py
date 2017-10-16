from django.views.generic import View

from forecast.factory import ForecastFactory
from utils.decorators import render_to_json


class ForecastView(View):
    controller = ForecastFactory().make_forecast_controller()

    @render_to_json
    def get(self, request):
        # TODO: Make it available only for admin users
        return self.controller.get_forecast(request)
