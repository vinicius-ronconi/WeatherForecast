from abc import ABCMeta, abstractmethod


class IWeather(object, metaclass=ABCMeta):
    class Units(object):
        CELSIUS = 'C'
        FAHRENHEIT = 'F'

        CHOICES = [CELSIUS, FAHRENHEIT]

    @abstractmethod
    def get_current(self, location_id, units):
        """
        :type location_id: int
        :type units: [forecast.interfaces.IWeather.Units.CELSIUS|forecast.interfaces.IWeather.Units.FAHRENHEIT]
        :rtype: forecast.beans.CurrentWeather
        """

    @abstractmethod
    def get_forecast(self, location_id, units):
        """
        :type location_id: int
        :type units: [forecast.interfaces.IWeather.Units.CELSIUS|forecast.interfaces.IWeather.Units.FAHRENHEIT]
        :rtype: forecast.beans.ForecastWeather
        """
