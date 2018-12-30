FROM python:3.6

MAINTAINER xsetra

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/Ribbon/

COPY . /usr/src/Ribbon/

RUN pip install -r requirements.txt
