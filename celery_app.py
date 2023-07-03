import abc
import re
import smtplib

import celery
from celery import Celery

import settings
from database import db_connect
from message_senders import mail
import watch_dog

app = Celery("word_parser", **settings.CELERY_RUN_PARAMETERS)

app.conf.beat_schedule = {
    'run-every-5-seconds': {
        'task': 'celery_app.task_watch_dog',
        'schedule': 5.0,
    },
}


class BaseTransactionsTask(celery.Task, abc.ABC):
    retry_backoff = settings.CELERY_TASK_RETRY_BACKOFF
    retry_backoff_max = settings.CELERY_TASK_RETRY_BACKOFF_MAX
    autoretry_for = (smtplib.SMTPException,)


@app.task
def to_process(body):
    path_to_file = body.decode()
    file_name = path_to_file.split("/")[-1]

    hash_map = {}
    with open(path_to_file, "r", encoding="utf-8") as f:
        lines = f.read()
        words = re.findall("[a-zA-Z]+|[а-яА-Я]+", lines)
        for word in words:
            w = hash_map.get(word.lower(), 0)
            hash_map[word.lower()] = w + 1

    with db_connect.DBConnection() as connection:
        counter = 0
        for k, v in hash_map.items():
            insert_or_update_words = (
                f"INSERT INTO words (word, count_words, in_files) VALUES ('{k}', {v}, '{file_name}')  "
                f"ON DUPLICATE KEY UPDATE count_words=count_words+{v}, in_files=CONCAT(in_files,', {file_name}');"
            )
            connection.cursor.execute(insert_or_update_words)


@app.task(
    base=BaseTransactionsTask,
    max_retries=settings.ERROR_NOTIFICATIONS_MAX_RETRIES,
    queue=settings.CELERY_ERROR_QUEUE,
)
def error_to_process(body):
    mail.sent_notification(body)

@app.task
def task_watch_dog():
    watch_dog.z()
