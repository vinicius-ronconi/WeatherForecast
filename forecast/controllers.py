import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from forecast.interfaces import IWeather


class ForecastController(object):
    ICON_URL_PREFIX = 'http://openweathermap.org/img/w/'
    ICON_FILE_FORMAT = '.png'

    def __init__(self, api):
        self.api = api

    def get_forecast(self, request):
        request = self._validate_request(request)
        location_id = request.GET.get('location_id')
        units = request.GET.get('units')
        current_weather = self.api.get_current(location_id, units)
        forecast_weather = self.api.get_forecast(location_id, units)
        res = self._jsonify_result(current_weather, forecast_weather)
        return res

    @staticmethod
    def _validate_request(request):
        if 'location_id' not in request.GET:
            raise ValidationError('location_id parameter not found.')
        if 'units' not in request.GET:
            raise ValidationError('units parameter not found.')
        if request.GET.get('units') not in IWeather.Units.CHOICES:
            raise ValidationError('Invalid units. Value must be C or F')
        return request

    def _jsonify_result(self, current_weather, forecast_weather):
        return {
            'city': self._jsonify_city(current_weather.city),
            'current_weather': self._jsonify_weather(current_weather.weather),
            'forecast': list(map(self._jsonify_weather, forecast_weather.weather)),
        }

    @staticmethod
    def _jsonify_city(city):
        """
        :type city: forecast.beans.City
        :rtype: dict
        """
        return {
                'id': city.id,
                'name': city.name,
                'country_code': city.country_code,
                'lat': city.lat,
                'lon': city.lon,
                'sunrise': city.sunrise,
                'sunset': city.sunset,
            }

    def _jsonify_weather(self, weather):
        """
        :type weather: forecast.beans.Weather
        :rtype: dict
        """
        return {
            'id': weather.id,
            'description': weather.description,
            'icon': '{}{}{}'.format(self.ICON_URL_PREFIX, weather.icon, self.ICON_FILE_FORMAT),
            'temperature': weather.temperature,
            'pressure': weather.pressure,
            'humidity': weather.humidity,
            'min_temperature': weather.min_temperature,
            'max_temperature': weather.max_temperature,
            'pressure_sea_level': weather.pressure_sea_level,
            'pressure_ground_level': weather.pressure_ground_level,
            'wind_speed': weather.wind_speed,
            'wind_degrees': weather.wind_degrees,
            'rain_3h': weather.rain_3h,
            'snow_3h': weather.snow_3h,
            'cloudiness': weather.cloudiness,
            'forecast_dt': weather.forecast_dt,
        }


class ReactAppController(object):
    def get_react_app(self):
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as file:
                return HttpResponse(file.read())
        except:
            return HttpResponse('index.html not found! Rebuild your react app.', status=501)
