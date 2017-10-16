from forecast.apis import OpenWeatherApi, FakeWeatherApi
from forecast.controllers import ForecastController
from utils.db import DbFactory


class ForecastFactory(object):
    db_factory = DbFactory()

    @classmethod
    def make_forecast_controller(cls):
        """
        :rtype: forecat.controllers.ForecastController
        """
        api = cls.make_forecast_api()
        return ForecastController(api)

    @classmethod
    def make_forecast_api(cls):
        """
        :rtype: forecast.interfaces.IWeather
        """
        return FakeWeatherApi() if cls.db_factory.use_test_db() else OpenWeatherApi()
