import re
from time import time

from async.controllers import AsyncController
from cities.adapters import OpenWeatherMongoAdapter
from utils.db import DbFactory
from utils.logger import init_logger


class CitiesController(object):
    DOWNLOAD_URL = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
    SEARCH_MIN_CHARS = 3
    SEARCH_LIMIT = 10

    adapter = OpenWeatherMongoAdapter()
    async_controller = AsyncController()
    collection = DbFactory.get_cities_collection()
    logger = init_logger('cities_updater')

    def __init__(self, downloader):
        """
        :type downloader: cities.interfaces.IDownloader
        """
        self.downloader = downloader

    def update_cities_asynchronously(self):
        from cities.tasks import update_cities
        async_result = update_cities.delay()
        return self.async_controller.get_async_task_status_by_result(async_result)

    def update_cities(self):
        cities_json = self.downloader.download(self.DOWNLOAD_URL)
        self._update_db(cities_json)

    def _update_db(self, cities_json):
        cities_json = self.adapter.prepare_to_mongo(cities_json)
        timestamp = time()
        # TODO: Create the Cities model in the future, since we will probably need it in more places
        for city in cities_json:
            city.update({'timestamp': timestamp})
            try:
                self.collection.update_one(
                    {'_id': city['_id']},
                    {'$set': city},
                    upsert=True)
            except Exception as e:
                self.logger.error('Error upserting {} - {}: {}'.format(city['_id'], e.__class__.__name__, e))

        self.collection.delete_many({'timestamp': {'$lt': timestamp}})

    def search_cities(self, query):
        if len(query) < self.SEARCH_MIN_CHARS:
            return []

        cities = list(self.collection.find(
            {'name': re.compile('^{}'.format(query), re.IGNORECASE)}
        ).sort('name').limit(self.SEARCH_LIMIT))
        return self.adapter.prepare_to_open_weather(cities)
