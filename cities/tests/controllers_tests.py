from django.core.urlresolvers import reverse
from django.test import TestCase

from cities.controllers import CitiesController
from cities.downloaders import FakeJsonDownloader
from cities.dao import FakeDao


class CitiesControllerTestCase(TestCase):
    def setUp(self):
        self.controller = CitiesController()
        self.controller.dao = FakeDao()
        self.controller.downloader = FakeJsonDownloader(FakeDao.CITIES_LIST)

    def test_it_updates_database(self):
        self.controller.update_cities()
        self.assertEqual(self.controller.dao.get_record_count(), 12)

        self.controller.downloader = FakeJsonDownloader(FakeDao.CITIES_LIST[:5])
        self.controller.update_cities()
        self.assertEqual(self.controller.dao.get_record_count(), 5)

    def test_it_searches_case_insensitive(self):
        result = self.controller.search_cities('Van')
        expected_result = [
            {'id': 2, 'name': 'Vance', 'country': 'US', 'coord': {'lon': -87.233612, 'lat': 33.17}},
            {'id': 3, 'name': 'Vancouver', 'country': 'US', 'coord': {'lon': -122.661491, 'lat': 45.63}},
        ]
        self.assertListEqual(result, expected_result)
        result = self.controller.search_cities('Serra')
        expected_result = [{'id': 1, 'name': 'Serra', 'country': 'BR', 'coord': {'lon': -40.307781, 'lat': -20.128611}}]
        self.assertListEqual(result, expected_result)

    def test_it_does_not_search_if_query_does_not_have_three_chars(self):
        result = self.controller.search_cities('')
        self.assertEqual(result, [])
        result = self.controller.search_cities('N')
        self.assertEqual(result, [])
        result = self.controller.search_cities('Ne')
        self.assertEqual(result, [])

    def test_it_does_not_find_any_result(self):
        result = self.controller.search_cities('invalidcity')
        self.assertListEqual(result, [])

    def test_it_triggers_async_download(self):
        response = self.client.get(reverse('download_cities'))
        content = response.json()
        self.assertIn('result_id', content)
