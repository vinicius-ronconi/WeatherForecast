FROM python:3.6.3

ENV PYTHONUNBUFFERED 1

COPY ./docker/celery_worker/worker-entrypoint.sh /
COPY ./requirements.txt /django/

WORKDIR /django
RUN ["chmod", "+x", "/worker-entrypoint.sh"]

RUN pip install pip==9.0.1
RUN pip install -r requirements.txt
