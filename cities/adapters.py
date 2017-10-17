class OpenWeatherMongoAdapter(object):
    def prepare_to_mongo(self, list_of_dicts, timestamp):
        for item in list_of_dicts:
            item['timestamp'] = timestamp
            if 'id' in item:
                item['_id'] = item['id']
                del item['id']
        return list_of_dicts

    def prepare_to_open_weather(self, list_of_dicts):
        for item in list_of_dicts:
            item['id'] = item['_id']
            del item['_id']
            del item['timestamp']
        return list_of_dicts
