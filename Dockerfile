FROM python:3.11.6
LABEL authors="yeren.palacios"
COPY . ./app
WORKDIR ./app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 9000