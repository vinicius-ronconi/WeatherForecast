import os

from django.conf import settings
from pymongo import MongoClient


class DbFactory(object):
    @classmethod
    def get_cities_collection(cls):
        """
        :rtype: pymongo.collection.Collection
        """
        instance = cls.make_instance()
        collection = instance.cities
        collection.create_index('name')
        collection.create_index('timestamp')
        return collection

    @classmethod
    def make_instance(cls):
        db_instance = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
        database = settings.MONGO_TEST_DB if cls.use_test_db() else settings.MONGO_DB
        return db_instance[database]

    @classmethod
    def use_test_db(cls):
        return os.environ.get('USE_TEST_DB')
