from abc import ABCMeta, abstractmethod


class IDownloader(object, metaclass=ABCMeta):
    @abstractmethod
    def download(self, url):
        """
        :type url: url
        :rtype:
        """
