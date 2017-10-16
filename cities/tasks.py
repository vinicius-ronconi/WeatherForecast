from __future__ import absolute_import, unicode_literals

from celery import shared_task

from cities.factory import CitiesFactory


@shared_task
def update_cities():
    controller = CitiesFactory.make_cities_controller()
    return controller.update_cities()
