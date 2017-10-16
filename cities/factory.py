from cities.controllers import CitiesController
from cities.downloaders import CompressedJsonDownloader, FakeJsonDownloader
from utils.db import DbFactory


class CitiesFactory(object):
    db_factory = DbFactory()

    @classmethod
    def make_cities_controller(cls):
        """
        :rtype: cities.controllers.CitiesController
        """
        downloader = cls.make_downloader()
        return CitiesController(downloader)

    @classmethod
    def make_downloader(cls):
        return FakeJsonDownloader([]) if cls.db_factory.use_test_db() else CompressedJsonDownloader()
