FROM python:3.8.12


WORKDIR src

COPY ./requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

COPY . .
