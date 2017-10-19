from time import time

from async.controllers import AsyncController
from cities.adapters import OpenWeatherMongoAdapter
from utils.logger import init_logger


class CitiesController(object):
    """
    :type dao: cities.interfaces.IDao
    :type downloader: cities.interfaces.IDownloader
    """
    DOWNLOAD_URL = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
    SEARCH_MIN_CHARS = 3
    SEARCH_LIMIT = 8

    adapter = OpenWeatherMongoAdapter()
    async_controller = AsyncController()
    dao = NotImplemented
    downloader = NotImplemented
    logger = init_logger('cities_updater')

    def update_cities_asynchronously(self):
        from cities.tasks import update_cities
        async_result = update_cities.delay()
        return self.async_controller.get_async_task_status_by_result(async_result)

    def update_cities(self):
        cities_json = self.downloader.download(self.DOWNLOAD_URL)
        self._update_db(cities_json)

    def _update_db(self, cities_json):
        timestamp = time()
        cities_json = self.adapter.prepare_to_mongo(cities_json, timestamp)
        # TODO: Create the Cities model in the future, since we will probably need it in more places
        for city in cities_json:
            try:
                self.dao.upsert_city(city)
            except Exception as e:
                self.logger.error('Error upserting {} - {}: {}'.format(city['_id'], e.__class__.__name__, e))

        self.dao.delete_old_records(timestamp)

    def search_cities(self, query):
        if len(query) < self.SEARCH_MIN_CHARS:
            return []
        cities = self.dao.get_by_partial_name(query, self.SEARCH_LIMIT)
        return self.adapter.prepare_to_open_weather(cities)
