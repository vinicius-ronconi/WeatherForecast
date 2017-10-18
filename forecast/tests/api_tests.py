import mock
from django.test import TestCase
from forecast.apis import OpenWeatherApi
from forecast import beans, exceptions


class OpenWeatherApiTestCase(TestCase):
    CITY_ID = 123
    CITY_NAME = 'Vitoria'
    CITY_COUNTRY_CODE = 'BR'
    CITY_LAT = -20
    CITY_LON = -40
    CITY_SUNRISE = 1500000000
    CITY_SUNSET = 1500009999
    WEATHER_ID = 999
    WEATHER_DESCRIPTION = 'Sunny'
    WEATHER_ICON = '01a'
    WEATHER_TEMPERATURE = 10.0
    WEATHER_PRESSURE = 20.0
    WEATHER_HUMIDITY = 30.0
    WEATHER_MIN_TEMPERATURE = 40.0
    WEATHER_MAX_TEMPERATURE = 50.0
    WEATHER_PRESSURE_SEA_LEVEL = 60.0
    WEATHER_PRESSURE_GROUND_LEVEL = 70.0
    WEATHER_WIND_SPEED = 80.0
    WEATHER_WIND_DEGREES = 90.0
    WEATHER_RAIN_3H = 100.0
    WEATHER_SNOW_3H = 110.0
    WEATHER_CLOUDINESS = 120.0
    WEATHER_FORECAST_DT = 1500000000

    def setUp(self):
        self.api = OpenWeatherApi()

    @mock.patch('forecast.apis.requests.get')
    def test_it_gets_current_weather(self, mock_get):
        expected_dict = {
            'coord': {'lon': self.CITY_LON, 'lat': self.CITY_LAT},
            'weather': [{
                'id': self.WEATHER_ID,
                'main': 'Clouds',
                'description': self.WEATHER_DESCRIPTION,
                'icon': self.WEATHER_ICON,
            }],
            'base': 'stations',
            'main': {
                'temp': self.WEATHER_TEMPERATURE,
                'pressure': self.WEATHER_PRESSURE,
                'humidity': self.WEATHER_HUMIDITY,
                'temp_min': self.WEATHER_MIN_TEMPERATURE,
                'temp_max': self.WEATHER_MAX_TEMPERATURE,
                'sea_level': self.WEATHER_PRESSURE_SEA_LEVEL,
                'grnd_level': self.WEATHER_PRESSURE_GROUND_LEVEL,
            },
            'visibility': 6000,
            'wind': {'speed': self.WEATHER_WIND_SPEED, 'deg': self.WEATHER_WIND_DEGREES},
            'clouds': {'all': self.WEATHER_CLOUDINESS},
            'rain': {'3h': self.WEATHER_RAIN_3H},
            'snow': {'3h': self.WEATHER_SNOW_3H},
            'dt': self.WEATHER_FORECAST_DT,
            'sys': {
                'type': 1,
                'id': 4601,
                'message': 0.003,
                'country': self.CITY_COUNTRY_CODE,
                'sunrise': self.CITY_SUNRISE,
                'sunset': self.CITY_SUNSET,
            },
            'id': self.CITY_ID,
            'name': self.CITY_NAME,
            'cod': 200
        }
        mock_response = self._make_mocked_response(expected_dict, status_code=200)
        mock_get.return_value = mock_response

        response = self.api.get_current(location_id=1, units='C')
        self.assertIsInstance(response, beans.CurrentWeather)
        self._assert_city_attributes(response.city)
        self._assert_weather_attributes(response.weather, multiplier=1)

    @mock.patch('forecast.apis.requests.get')
    def test_it_gets_forecast(self, mock_get):
        expected_dict = {
            'cod': '200',
            'message': 0.0019,
            'cnt': 3,
            'list': [
                {
                    'dt': self.WEATHER_FORECAST_DT,
                    'main': {
                        'temp': self.WEATHER_TEMPERATURE,
                        'temp_min': self.WEATHER_MIN_TEMPERATURE,
                        'temp_max': self.WEATHER_MAX_TEMPERATURE,
                        'pressure': self.WEATHER_PRESSURE,
                        'sea_level': self.WEATHER_PRESSURE_SEA_LEVEL,
                        'grnd_level': self.WEATHER_PRESSURE_GROUND_LEVEL,
                        'humidity': self.WEATHER_HUMIDITY,
                        'temp_kf': 0.59
                    },
                    'weather': [
                        {
                            'id': self.WEATHER_ID,
                            'main': 'Rain',
                            'description': self.WEATHER_DESCRIPTION,
                            'icon': self.WEATHER_ICON,
                        }
                    ],
                    'sun': {'rise': self.CITY_SUNRISE, 'set': self.CITY_SUNSET},
                    'clouds': {'all': self.WEATHER_CLOUDINESS},
                    'wind': {'speed': self.WEATHER_WIND_SPEED, 'deg': self.WEATHER_WIND_DEGREES},
                    'rain': {'3h': self.WEATHER_RAIN_3H},
                    'snow': {'3h': self.WEATHER_SNOW_3H},
                    'sys': {'pod': 'n'},
                    'dt_txt': '2017-10-16 21:00:00'
                },
                {
                    'dt': self.WEATHER_FORECAST_DT * 2,
                    'main': {
                        'temp': self.WEATHER_TEMPERATURE * 2,
                        'temp_min': self.WEATHER_MIN_TEMPERATURE * 2,
                        'temp_max': self.WEATHER_MAX_TEMPERATURE * 2,
                        'pressure': self.WEATHER_PRESSURE * 2,
                        'sea_level': self.WEATHER_PRESSURE_SEA_LEVEL * 2,
                        'grnd_level': self.WEATHER_PRESSURE_GROUND_LEVEL * 2,
                        'humidity': self.WEATHER_HUMIDITY * 2,
                        'temp_kf': 0.59
                    },
                    'weather': [
                        {
                            'id': self.WEATHER_ID,
                            'main': 'Rain',
                            'description': self.WEATHER_DESCRIPTION,
                            'icon': self.WEATHER_ICON,
                        }
                    ],
                    'sun': {'rise': self.CITY_SUNRISE, 'set': self.CITY_SUNSET},
                    'clouds': {'all': self.WEATHER_CLOUDINESS * 2},
                    'wind': {'speed': self.WEATHER_WIND_SPEED * 2, 'deg': self.WEATHER_WIND_DEGREES * 2},
                    'rain': {'3h': self.WEATHER_RAIN_3H * 2},
                    'snow': {'3h': self.WEATHER_SNOW_3H * 2},
                    'sys': {'pod': 'n'},
                    'dt_txt': '2017-10-16 21:00:00'
                },
                {
                    'dt': self.WEATHER_FORECAST_DT * 3,
                    'main': {
                        'temp': self.WEATHER_TEMPERATURE * 3,
                        'temp_min': self.WEATHER_MIN_TEMPERATURE * 3,
                        'temp_max': self.WEATHER_MAX_TEMPERATURE * 3,
                        'pressure': self.WEATHER_PRESSURE * 3,
                        'sea_level': self.WEATHER_PRESSURE_SEA_LEVEL * 3,
                        'grnd_level': self.WEATHER_PRESSURE_GROUND_LEVEL * 3,
                        'humidity': self.WEATHER_HUMIDITY * 3,
                        'temp_kf': 0.59
                    },
                    'weather': [
                        {
                            'id': self.WEATHER_ID,
                            'main': 'Rain',
                            'description': self.WEATHER_DESCRIPTION,
                            'icon': self.WEATHER_ICON,
                        }
                    ],
                    'sun': {'rise': self.CITY_SUNRISE, 'set': self.CITY_SUNSET},
                    'clouds': {'all': self.WEATHER_CLOUDINESS * 3},
                    'wind': {'speed': self.WEATHER_WIND_SPEED * 3, 'deg': self.WEATHER_WIND_DEGREES * 3},
                    'rain': {'3h': self.WEATHER_RAIN_3H * 3},
                    'snow': {'3h': self.WEATHER_SNOW_3H * 3},
                    'sys': {'pod': 'n'},
                    'dt_txt': '2017-10-16 21:00:00'
                },
            ],
            'city': {
                'id': self.CITY_ID,
                'name': self.CITY_NAME,
                'coord': {'lat': self.CITY_LAT, 'lon': self.CITY_LON},
                'country': self.CITY_COUNTRY_CODE,
            }
        }
        mock_response = self._make_mocked_response(expected_dict, status_code=200)
        mock_get.return_value = mock_response

        response = self.api.get_forecast(location_id=1, units='C')
        self.assertIsInstance(response, beans.ForecastWeather)
        self._assert_city_attributes(response.city)
        self.assertIsInstance(response.weather, list)
        self._assert_weather_attributes(response.weather[0], multiplier=1)
        self._assert_weather_attributes(response.weather[1], multiplier=2)
        self._assert_weather_attributes(response.weather[2], multiplier=3)

    @mock.patch('forecast.apis.requests.get')
    def test_it_raises_exception(self, mock_get):
        expected_dict = {
            'cod': 401,
            'message': 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'
        }
        mock_response = self._make_mocked_response(expected_dict, status_code=401)
        mock_get.return_value = mock_response
        self.assertRaises(
            exceptions.ForecastException,
            self.api.get_current,
            location_id=1,
            units='C',
        )

        self.assertRaises(
            exceptions.ForecastException,
            self.api.get_forecast,
            location_id=1,
            units='C',
        )

    @staticmethod
    def _make_mocked_response(expected_dict, status_code):
        mock_response = mock.Mock()
        mock_response.json.return_value = expected_dict
        mock_response.status_code = status_code
        return mock_response

    def _assert_city_attributes(self, city):
        self.assertIsInstance(city, beans.City)
        self.assertEqual(city.id, self.CITY_ID)
        self.assertEqual(city.name, self.CITY_NAME)
        self.assertEqual(city.country_code, self.CITY_COUNTRY_CODE)
        self.assertEqual(city.flag_url, '/flags-100px/{}.png'.format(self.CITY_COUNTRY_CODE.lower()))
        self.assertEqual(city.lat, self.CITY_LAT)
        self.assertEqual(city.lon, self.CITY_LON)

    def _assert_weather_attributes(self, weather, multiplier):
        self.assertIsInstance(weather, beans.Weather)
        self.assertEqual(weather.id, self.WEATHER_ID)
        self.assertEqual(weather.description, self.WEATHER_DESCRIPTION)
        self.assertEqual(weather.icon, self.WEATHER_ICON)
        self.assertEqual(weather.temperature, self.WEATHER_TEMPERATURE * multiplier)
        self.assertEqual(weather.pressure, self.WEATHER_PRESSURE * multiplier)
        self.assertEqual(weather.humidity, self.WEATHER_HUMIDITY * multiplier)
        self.assertEqual(weather.min_temperature, self.WEATHER_MIN_TEMPERATURE * multiplier)
        self.assertEqual(weather.max_temperature, self.WEATHER_MAX_TEMPERATURE * multiplier)
        self.assertEqual(weather.pressure_sea_level, self.WEATHER_PRESSURE_SEA_LEVEL * multiplier)
        self.assertEqual(weather.pressure_ground_level, self.WEATHER_PRESSURE_GROUND_LEVEL * multiplier)
        self.assertEqual(weather.wind_speed, self.WEATHER_WIND_SPEED * multiplier)
        self.assertEqual(weather.wind_degrees, self.WEATHER_WIND_DEGREES * multiplier)
        self.assertEqual(weather.rain_3h, self.WEATHER_RAIN_3H * multiplier)
        self.assertEqual(weather.snow_3h, self.WEATHER_SNOW_3H * multiplier)
        self.assertEqual(weather.cloudiness, self.WEATHER_CLOUDINESS * multiplier)
        self.assertEqual(weather.forecast_dt, self.WEATHER_FORECAST_DT * multiplier)
