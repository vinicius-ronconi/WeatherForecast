from django.core.urlresolvers import reverse
from django.test import TestCase

from forecast.controllers import ForecastController
from forecast.apis import FakeWeatherApi


class ForecastControllerTestCase(TestCase):
    def setUp(self):
        self.controller = ForecastController(FakeWeatherApi())

    def test_it_handles_exception(self):
        response = self.client.get(reverse('search_forecast'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('location_id', response.json()['error'])

        response = self.client.get(reverse('search_forecast'), data={'location_id': 1})
        self.assertEqual(response.status_code, 400)
        self.assertIn('units', response.json()['error'])

        response = self.client.get(reverse('search_forecast'), data={'location_id': 1, 'units': 'X'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid units', response.json()['error'])

    def test_it_returns_current_weather_and_forecast(self):
        response = self.client.get(reverse('search_forecast'), data={'location_id': 1, 'units': 'C'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('city', response.json())
        self.assertIsInstance(response.json()['current_weather'], dict)
        self.assertIsInstance(response.json()['forecast'], list)
        self.assertIsInstance(response.json()['forecast'][0], dict)
