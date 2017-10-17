from abc import ABCMeta, abstractmethod


class IDownloader(object, metaclass=ABCMeta):
    @abstractmethod
    def download(self, url):
        """
        :type url: url
        :rtype:
        """


class IDao(object, metaclass=ABCMeta):
    @abstractmethod
    def get_by_partial_name(self, query, limit):
        """
        :type query: str
        :type limit: int
        :rtype: list(dict)
        """

    @abstractmethod
    def upsert_city(self, city):
        """
        :type city: dict
        :rtype: None
        """
    @abstractmethod
    def delete_old_records(self, timestamp):
        """
        :type timestamp: int
        :rtype: None
        """

    @abstractmethod
    def get_record_count(self):
        """
        :rtype: int
        """
