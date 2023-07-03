FROM python:3.10-alpine
LABEL authors="alex"

COPY . .
RUN pip3 install ./requirements.txt
