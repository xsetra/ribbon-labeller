FROM python:3.6-alpine

MAINTAINER xsetra

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/Ribbon/

WORKDIR /usr/src/Ribbon/

COPY . /usr/src/Ribbon/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD exec python manage.py runserver 0.0.0.0:8000

