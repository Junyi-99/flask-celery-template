# pull official base image
# FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime
FROM python:3.11.0a7-slim-buster

# set work directory
WORKDIR /flask-celery-app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
