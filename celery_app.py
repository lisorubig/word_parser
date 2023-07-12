"""

Celery application with tasks and beat_sheduler

"""
import abc
import re
import smtplib

import celery

import settings
from database import db_connect
from message_senders import mail
import handler_module
import reader


app = celery.Celery("word_parser", **settings.CELERY_RUN_PARAMETERS)

app.conf.beat_schedule = {
    "check_new_files_in_directory": {
        "task": "watch_dog",
        "schedule": settings.CHECK_NEW_FILES_TIMEOUT,
    },
    "write_word_to_file": {
        "task": "task_reader",
        "schedule": settings.CHECK_WORDS_FOR_WRITE,
    },
}


class BaseTransactionsTask(celery.Task, abc.ABC):
    """
    Config class for task
    """

    retry_backoff = settings.CELERY_TASK_RETRY_BACKOFF
    retry_backoff_max = settings.CELERY_TASK_RETRY_BACKOFF_MAX
    autoretry_for = (smtplib.SMTPException,)


@app.task(queue=settings.CELERY_QUEUE_PARSING)
def task_file_parsing(path_to_file: str) -> None:
    """
    Create task for file parsing
    """
    handler_module.parse_word(path_to_file)


@app.task(
    base=BaseTransactionsTask,
    max_retries=settings.ERROR_NOTIFICATIONS_MAX_RETRIES,
    queue=settings.CELERY_QUEUE_ERRORS,
)
def error_to_process(path_to_file) -> None:
    """
    Create task for sending mail
    """
    mail.sent_notification(path_to_file)


@app.task(name="task_reader", queue=settings.CELERY_QUEUE_READER)
def create_task_reader():
    """
    Create task reader
    """
    reader.reader()


@app.task(name="watch_dog")
def task_watch_dog() -> None:
    """
    Create task for scan parsing directory
    """
    handler_module.watch_dog()
