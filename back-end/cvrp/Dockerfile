FROM python:3.9

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip

COPY ./requirements.txt /app

RUN pip3 install --default-timeout=1000 --no-cache-dir -r requirements.txt