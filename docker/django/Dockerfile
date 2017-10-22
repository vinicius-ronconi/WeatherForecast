FROM python:3.6.3

ENV PYTHONUNBUFFERED 1

COPY ./docker/django/django-entrypoint.sh /
COPY ./requirements.txt /django/

WORKDIR /django
RUN ["chmod", "+x", "/django-entrypoint.sh"]

RUN pip install pip==9.0.1
RUN pip install -r requirements.txt
