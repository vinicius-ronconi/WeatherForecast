import requests
from django.conf import settings

from forecast import beans, exceptions
from forecast.interfaces import IWeather


class OpenWeatherApi(IWeather):
    API_UNITS_TO_OPEN_WEATHER_MAP = {
        IWeather.Units.CELSIUS: 'metric',
        IWeather.Units.FAHRENHEIT: 'imperial',
    }
    BASE_API_URL = 'http://api.openweathermap.org/data/2.5'

    def get_current(self, location_id, units):
        url = '{}/weather'.format(self.BASE_API_URL)
        params = '?id={}&units={}'.format(location_id, self.API_UNITS_TO_OPEN_WEATHER_MAP[units])
        data = self._get_api_data(url, params)
        return beans.CurrentWeather(
            city=self._make_city_bean_from_current_content(data),
            weather=self._make_weather_bean(data),
        )

    @staticmethod
    def _make_city_bean_from_current_content(data):
        return beans.City(
            id=data.get('id'),
            name=data.get('name'),
            country_code=data.get('sys', {}).get('country'),
            lat=data.get('coord', {}).get('lat'),
            lon=data.get('coord', {}).get('lon'),
            sunrise=data.get('sys', {}).get('sunrise'),
            sunset=data.get('sys', {}).get('sunset'),
        )

    def get_forecast(self, location_id, units):
        url = '{}/forecast'.format(self.BASE_API_URL)
        params = '?id={}&units={}'.format(location_id, self.API_UNITS_TO_OPEN_WEATHER_MAP[units])
        data = self._get_api_data(url, params)
        return beans.ForecastWeather(
            city=self._make_city_bean_from_forecast_content(data),
            weather=list(map(self._make_weather_bean, data.get('list', [])))
        )

    @staticmethod
    def _make_city_bean_from_forecast_content(data):
        return beans.City(
            id=data.get('city', {}).get('id'),
            name=data.get('city', {}).get('name'),
            country_code=data.get('city', {}).get('country'),
            lat=data.get('city', {}).get('coord', {}).get('lat'),
            lon=data.get('city', {}).get('coord', {}).get('lon'),
            sunrise=0,
            sunset=0,
        )

    @staticmethod
    def _get_api_data(url, params):
        """
        :type url: str
        :type params: str
        :rtype: dict
        """
        params += '&appid={}'.format(settings.OPEN_WEATHER_API_KEY)
        response = requests.get('{}{}'.format(url, params))
        content = response.json()
        if response.status_code != 200:
            raise exceptions.ForecastException(content.get('message'))
        return content

    @staticmethod
    def _make_weather_bean(data):
        return beans.Weather(
            id=data.get('weather', [{}])[0].get('id'),
            description=data.get('weather', [{}])[0].get('description'),
            icon=data.get('weather', [{}])[0].get('icon'),
            temperature=data.get('main', {}).get('temp'),
            pressure=data.get('main', {}).get('pressure'),
            humidity=data.get('main', {}).get('humidity'),
            min_temperature=data.get('main', {}).get('temp_min'),
            max_temperature=data.get('main', {}).get('temp_max'),
            pressure_sea_level=data.get('main', {}).get('sea_level'),
            pressure_ground_level=data.get('main', {}).get('grnd_level'),
            wind_speed=data.get('wind', {}).get('speed'),
            wind_degrees=data.get('wind', {}).get('deg'),
            rain_3h=data.get('rain', {}).get('3h'),
            snow_3h=data.get('snow', {}).get('3h'),
            cloudiness=data.get('clouds', {}).get('all'),
            forecast_dt=data.get('dt'),
        )


class FakeWeatherApi(IWeather):
    def get_current(self, location_id, units):
        return beans.CurrentWeather(
            city=self._make_city_bean(),
            weather=self._make_weather_bean(),
        )

    def get_forecast(self, location_id, units):
        return beans.ForecastWeather(
            city=self._make_city_bean(),
            weather=[self._make_weather_bean()] * 20,
        )

    @staticmethod
    def _make_city_bean():
        return beans.City(
            id=3444924,
            name='Vitoria',
            country_code='BR',
            lat=-20.32,
            lon=-40.34,
            sunrise=1508141357,
            sunset=1508186663,
        )

    @staticmethod
    def _make_weather_bean():
        return beans.Weather(
            id=803,
            description='broken clouds',
            icon='04d',
            temperature=23,
            pressure=1021,
            humidity=94,
            min_temperature=23,
            max_temperature=23,
            pressure_sea_level=1022,
            pressure_ground_level=1023,
            wind_speed=5.1,
            wind_degrees=210,
            rain_3h=20,
            snow_3h=0,
            cloudiness=75,
            forecast_dt=1508169600,
        )
