from django.test import TestCase
from cities.dao import MongoDao


class MongoDaoTestCase(TestCase):
    def setUp(self):
        self.dao = MongoDao()
        self.dao.collection.delete_many({})
        self.current_timestamp = 10
        self.city_1 = {
            '_id': 1,
            'name': 'Serra',
            'country': 'BR',
            'coord': {'lon': -40.307781, 'lat': -20.128611},
            'timestamp': self.current_timestamp - 5,
        }
        self.city_2 = {
            '_id': 2,
            'name': 'Vance',
            'country': 'US',
            'coord': {'lon': -87.233612, 'lat': 33.17},
            'timestamp': self.current_timestamp + 5,
        }

    def test_it_upsert_records(self):
        self.assertEqual(self.dao.get_record_count(), 0)
        self.dao.upsert_city(self.city_1)
        self.assertEqual(self.dao.get_record_count(), 1)
        self.dao.upsert_city(self.city_1)
        self.assertEqual(self.dao.get_record_count(), 1)
        self.dao.upsert_city(self.city_2)
        self.assertEqual(self.dao.get_record_count(), 2)

    def test_it_deletes_old_records(self):
        self.dao.collection.update_one({'_id': self.city_1['_id']}, {'$set': self.city_1}, upsert=True)
        self.dao.collection.update_one({'_id': self.city_2['_id']}, {'$set': self.city_2}, upsert=True)
        self.dao.delete_old_records(self.current_timestamp)
        self.assertEqual(self.dao.get_record_count(), 1)

    def test_it_gets_by_partial_name(self):
        self.dao.collection.update_one({'_id': self.city_1['_id']}, {'$set': self.city_1}, upsert=True)
        self.dao.collection.update_one({'_id': self.city_2['_id']}, {'$set': self.city_2}, upsert=True)
        result = self.dao.get_by_partial_name('Ser', 1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get('name'), 'Serra')
