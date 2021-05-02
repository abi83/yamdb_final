FROM python:3.8.5
LABEL author='Wladimir Kromm' version=1.0


WORKDIR /code

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /code

ARG DJANGO_ENV=settings
ENV DJANGO_SETTINGS_MODULE=api_yamdb.${DJANGO_ENV}

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000