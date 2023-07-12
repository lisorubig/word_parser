FROM python:3.10
LABEL authors="alex"

ENV PYTHONPATH=/usr/project/src
WORKDIR /usr/project/src
COPY . .
RUN pip3 install -r ./requirements.txt
