#!/usr/bin/env bash

cd front-end
npm install
npm run build

cd ..
python manual_scripts/initial_cities_load.py
python manage.py runserver 0.0.0.0:8000
