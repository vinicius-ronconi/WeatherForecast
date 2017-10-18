from collections import namedtuple


City = namedtuple('City', [
    'id',  # str
    'name',  # str
    'country_code',  # str
    'flag_url',  # str
    'lat',  # float
    'lon',  # float
    'sunrise',  # int
    'sunset',  # int
])


Weather = namedtuple('Weather', [
    'id',  # str
    'description',  # str
    'icon',  # str
    'temperature',  # float
    'pressure',  # float
    'humidity',  # float
    'min_temperature',  # float
    'max_temperature',  # float
    'pressure_sea_level',  # float
    'pressure_ground_level',  # float
    'wind_speed',  # float
    'wind_degrees',  # float
    'rain_3h',  # float
    'snow_3h',  # float
    'cloudiness',  # float
    'forecast_dt',  # int
])


CurrentWeather = namedtuple('CurrentWeather', [
    'city',  # forecast.beans.City,
    'weather',  # forecast.beans.Weather,
])


ForecastWeather = namedtuple('ForecastWeather', [
    'city',  # forecast.beans.City,
    'weather',  # list[forecast.beans.Weather],
])
