import gzip
from io import BytesIO

import requests
from bson import json_util

from cities.interfaces import IDownloader


class CompressedJsonDownloader(IDownloader):
    def download(self, url):
        response = requests.get(url)
        decompressed_file = gzip.GzipFile(fileobj=BytesIO(response.content))
        json_content = json_util.loads(decompressed_file.read().decode('utf-8'))
        return json_content


class FakeJsonDownloader(IDownloader):
    def __init__(self, dataset):
        self.dataset = dataset

    def download(self, url):
        return self.dataset
