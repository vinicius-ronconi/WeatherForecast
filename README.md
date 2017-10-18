# WeatherForecast
Show weather forecast for a city using OpenWeatherMap.org API

# Pre-requirements
* Python 3.6+ - https://www.python.org/downloads/
* Mongo 3.2+ - https://www.mongodb.com/download-center#community
* RabbitMQ - http://www.rabbitmq.com/download.html
* API Key - http://openweathermaps.org
* npm - https://www.npmjs.com/package/npm

# Attention
Before run manual_scripts/initial_cities_load.py from setup section, create a new file WeatherForecast/local_settings.py with at least:
```
SECRET_KEY = 'some_secret_key_for_the_app'
OPEN_WEATHER_API_KEY = 'api_key_created_on_openweathermap_org'
```

# Setup
```
git clone https://github.com/vinicius-ronconi/WeatherForecast.git
cd WeatherForecast
virtualenv weather_forecast_env
source weather_forecast_env/bin/activate
pip3 install -r requirements.txt
cd front-end
npm install
npm build
cd ..
python3 manual_scripts/initial_cities_load.py
python3 manage.py runserver
```

# Next Steps
* Create a periodic task to re-load cities every week. It should run asynchronously using celery.
* Allow admins to run the cities load manually from an admin interface. The back-end code to trigger it is done in this endpoint. It is possible to control the progress using this other endpoint.
* During city search, consider user's location, if available to return a list ordered by closest cities instead of an alphabetically ordered list.
* Background changes only for 3 weather conditions (sunny, cloudy and rainny). Apply more personalizations according to the openweathermap.org conditions.
* The API gets data from both current weather and forecast, but front-end only show the current weather. Add a scroll or a button to let user see a table with forecast data.
* After introduce the table with forecast data, create a line plot with changes of a selected variable across the time.
* Introduce pagination to display more city options to the users.
