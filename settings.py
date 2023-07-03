import logging
import os


# Logging
LOGLEVEL = logging.WARNING
logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=LOGLEVEL)


BASE_DIR = os.path.dirname(__file__)
work_dir: str = f"{BASE_DIR}/files_to_process"

# watch_dog
list_files: str = "list_files"

REQUEST_PERIOD = 5

# RabbitMQ
RMQ_HOST: str = os.environ.get("RMQ_HOST", "localhost")
RMQ_CONNECT_PARAMETERS: dict = {"host": RMQ_HOST}

QUEUE_PARSING: str = os.environ.get("PARSING", "Parsing")
QUEUE_ERRORS: str = os.environ.get("ERRORS", "Errors")

RMQ_USER: str = os.environ.get("RMQ_USER", "admin")
RMQ_PASSWORD: str = os.environ.get("RMQ_PASSWORD", "admin")
CREDENTIALS: dict = {"username": RMQ_USER, "password": RMQ_PASSWORD}

# Celery
CELERY_RUN_PARAMETERS: dict = {
    "broker": f"amqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_HOST}//"
}
CELERY_ERROR_QUEUE: str = os.environ.get("CELERY_ERROR_QUEUE", "mail_notification")
ERROR_NOTIFICATIONS_MAX_RETRIES: int = int(
    os.environ.get("ERROR_NOTIFICATIONS_MAX_RETRIES", "5")
)
CELERY_TASK_RETRY_BACKOFF: int = int(os.environ.get("CELERY_TASK_RETRY_BACKOFF", "30"))
CELERY_TASK_RETRY_BACKOFF_MAX: int = int(
    os.environ.get("CELERY_TASK_RETRY_BACKOFF_MAX", "3840")
)

# MySQL
MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_DATABASE: str = os.environ.get("MYSQL_DATABASE", "word_parser")
MYSQL_USER: str = os.environ.get("MYSQL_USER", "admin")
MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD", "admin")

# SMTP
SMTP_SERVER: str = os.environ.get("SMTP_SERVER", "localhost:1025")
MAIL_SENDER: str = os.environ.get("MAIL_SENDER", "from@fromdomain.com")
MAIL_RECEIVERS: list = os.environ.get("MAIL_RECEIVERS", "to@todomain.com").split(" ")

# Reader
FRINGE_WRITE_TO_FILE: int = int(os.environ.get("FRINGE_WRITE_TO_FILE", "4300"))
