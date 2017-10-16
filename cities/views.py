from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from cities.factory import CitiesFactory
from utils.decorators import render_to_json


class DownloadView(View):
    controller = CitiesFactory().make_cities_controller()

    # FIXME: Before make this project go to real deploy, get rid of this
    @csrf_exempt
    @render_to_json
    def get(self, _):
        # TODO: Make it available only for admin users
        return self.controller.update_cities_asynchronously()


class SearchView(View):
    controller = CitiesFactory().make_cities_controller()

    @render_to_json
    def get(self, request):
        return self.controller.search_cities(request.GET.get('q'))
