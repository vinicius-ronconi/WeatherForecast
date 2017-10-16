from django.core.urlresolvers import reverse
from django.test import TestCase

from cities.controllers import CitiesController
from cities.downloaders import FakeJsonDownloader


class CitiesControllerTestCase(TestCase):
    def setUp(self):
        self.downloader_dataset = [
            {'id': 707860, 'name': 'Hurzuf', 'country': 'UA', 'coord': {'lon': 34.283333, 'lat': 44.549999}},
            {'id': 519188, 'name': 'Novinki', 'country': 'RU', 'coord': {'lon': 37.666668, 'lat': 55.683334}},
            {'id': 1283378, 'name': 'Gorkhā', 'country': 'NP', 'coord': {'lon': 84.633331, 'lat': 28}},
            {'id': 2641519, 'name': 'Newtownards', 'country': 'GB', 'coord': {'lon': -5.69092, 'lat': 54.592361}},
            {'id': 3489297, 'name': 'New Kingston', 'country': 'JM', 'coord': {'lon': -76.783188, 'lat': 18.007469}},
            {'id': 5128638, 'name': 'New York', 'country': 'US', 'coord': {'lon': -75.499901, 'lat': 43.000351}},
            {'id': 7839758, 'name': 'Newcastle', 'country': 'AU', 'coord': {'lon': 151.708435, 'lat': -32.876282}},
        ]
        self.controller = CitiesController(FakeJsonDownloader(self.downloader_dataset))
        self.controller.update_cities()

    def test_it_updates_database(self):
        self.assertEqual(self.controller.collection.count(), 7)

        self.controller.downloader = FakeJsonDownloader(self.downloader_dataset[:3])
        self.controller.update_cities()
        self.assertEqual(self.controller.collection.count(), 3)

    def test_it_searches_case_insensitive(self):
        result = self.controller.search_cities('new')
        expected_result = [
            {'id': 3489297, 'name': 'New Kingston', 'country': 'JM', 'coord': {'lon': -76.783188, 'lat': 18.007469}},
            {'id': 5128638, 'name': 'New York', 'country': 'US', 'coord': {'lon': -75.499901, 'lat': 43.000351}},
            {'id': 7839758, 'name': 'Newcastle', 'country': 'AU', 'coord': {'lon': 151.708435, 'lat': -32.876282}},
            {'id': 2641519, 'name': 'Newtownards', 'country': 'GB', 'coord': {'lon': -5.69092, 'lat': 54.592361}},
        ]
        self.assertListEqual(result, expected_result)
        result = self.controller.search_cities('GORK')
        expected_result = [{'id': 1283378, 'name': 'Gorkhā', 'country': 'NP', 'coord': {'lon': 84.633331, 'lat': 28}}]
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
