#!/usr/bin/env bash

# wait for RabbitMQ server to start
sleep 10

celery -A WeatherForecast worker -l info --hostname rabbit
