FROM python:3.11

RUN apt-get -y update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY .dockerignore /code/.dockerignore
COPY docker-entrypoint.sh  /code/docker-entrypoint.sh

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

EXPOSE 8000
COPY . /code/

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]