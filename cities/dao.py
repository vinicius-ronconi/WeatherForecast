from cities.interfaces import IDao
from utils.db import DbFactory
import re


class MongoDao(IDao):
    collection = DbFactory.get_cities_collection()

    def get_by_partial_name(self, query, limit):
        return list(self.collection.find(
            {'name': re.compile('^{}'.format(query), re.IGNORECASE)}
        ).sort('name').limit(limit))

    def upsert_city(self, city):
        self.collection.update_one({'_id': city['_id']}, {'$set': city}, upsert=True)

    def delete_old_records(self, timestamp):
        self.collection.delete_many({'timestamp': {'$lt': timestamp}})

    def get_record_count(self):
        return self.collection.count()


class FakeDao(IDao):
    CITIES_LIST = [
        {'_id': 1, 'name': 'Serra', 'country': 'BR', 'coord': {'lon': -40.307781, 'lat': -20.128611}, 'timestamp': 0},
        {'_id': 2, 'name': 'Vance', 'country': 'US', 'coord': {'lon': -87.233612, 'lat': 33.17}, 'timestamp': 0},
        {'_id': 3, 'name': 'Vancouver', 'country': 'US', 'coord': {'lon': -122.661491, 'lat': 45.63}, 'timestamp': 0},
        {'_id': 4, 'name': 'Vila Velha', 'country': 'BR', 'coord': {'lon': -40.2925, 'lat': -20.32972}, 'timestamp': 0},
        {'_id': 5, 'name': 'Viterbo', 'country': 'IT', 'coord': {'lon': 12.10856, 'lat': 42.417831}, 'timestamp': 0},
        {'_id': 6, 'name': 'Vitré', 'country': 'FR', 'coord': {'lon': -1.2, 'lat': 48.133331}, 'timestamp': 0},
        {'_id': 7, 'name': 'Vitoria', 'country': 'BR', 'coord': {'lon': -40.33778, 'lat': -20.319441}, 'timestamp': 0},
        {'_id': 8, 'name': 'Vitoria-Gasteiz', 'country': 'ES', 'coord': {'lon': -2.66976, 'lat': 42.8}, 'timestamp': 0},
        {'_id': 9, 'name': 'Vitoria da Conq', 'country': 'BR', 'coord': {'lon': -40.8, 'lat': -14.8}, 'timestamp': 0},
        {'_id': 10, 'name': 'Vitoria Sto Antao', 'country': 'BR', 'coord': {'lon': -35.2, 'lat': -8.1}, 'timestamp': 0},
        {'_id': 11, 'name': 'Vitorino das Donas', 'country': 'PT', 'coord': {'lon': -8.6, 'lat': 41.7}, 'timestamp': 0},
        {'_id': 12, 'name': 'Vittoria', 'country': 'IT', 'coord': {'lon': 14.53318, 'lat': 36.953739}, 'timestamp': 0},
    ]

    def get_by_partial_name(self, query, limit):
        return [city for city in self.CITIES_LIST if city.get('name').lower().startswith(query.lower())]

    def upsert_city(self, city):
        city_name = city.get('name').lower()
        existing_city_list = [city for city in self.CITIES_LIST if city.get('name').lower() == city_name]
        if existing_city_list:
            return None
        self.CITIES_LIST.append(city)

    def delete_old_records(self, timestamp):
        self.CITIES_LIST = [item for item in self.CITIES_LIST if item.get('timestamp', 0) >= timestamp]

    def get_record_count(self):
        return len(self.CITIES_LIST)
