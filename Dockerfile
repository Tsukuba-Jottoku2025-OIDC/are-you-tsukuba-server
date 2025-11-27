FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Tokyo

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt
