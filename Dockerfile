FROM python:3.8-slim

# MAINTAINER aadarshverma

#ENV PYTHONBUFFERED 1
RUN mkdir /app

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/





