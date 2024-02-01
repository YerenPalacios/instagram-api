FROM python:3.11.6-slim-bullseye
LABEL authors="yeren.palacios"
COPY . ./app
RUN apt-get update

RUN apt-get install -y  gcc libpq-dev python3-dev 
RUN pip install --upgrade pip
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000
