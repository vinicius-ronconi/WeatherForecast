#!/usr/bin/env python

import sys
import os.path

rel_path_to_project_dir = '/../'
cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(cur_dir + rel_path_to_project_dir))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeatherForecast.settings")

from cities.factory import CitiesFactory


controller = CitiesFactory().make_cities_controller()
controller.update_cities()
print('{} cities loaded!'.format(controller.dao.get_record_count()))
