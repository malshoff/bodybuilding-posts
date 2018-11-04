FROM ubuntu:18.04
FROM python:3.6-onbuild
RUN  apt-get update &&apt-get upgrade -y&& apt-get install python-pip -y
RUN pip install --upgrade pip
COPY /scraper /scraper
WORKDIR /scraper
RUN python rundock.py