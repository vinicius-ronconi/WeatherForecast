from cities.controllers import CitiesController
from cities.dao import FakeDao, MongoDao
from cities.downloaders import CompressedJsonDownloader, FakeJsonDownloader
from utils.db import DbFactory


class CitiesFactory(object):
    db_factory = DbFactory()

    @classmethod
    def make_cities_controller(cls):
        """
        :rtype: cities.controllers.CitiesController
        """
        controller = CitiesController()
        controller.downloader = cls.make_downloader()
        controller.dao = cls.make_dao()
        return controller

    @classmethod
    def make_downloader(cls):
        return FakeJsonDownloader([]) if cls.db_factory.use_test_db() else CompressedJsonDownloader()

    @classmethod
    def make_dao(cls):
        return FakeDao() if cls.db_factory.use_test_db() else MongoDao()
