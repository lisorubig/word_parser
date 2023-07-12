"""

Settings for all modules

"""
import os


WORK_DIR: str = os.environ.get("WORK_DIR", os.path.dirname(__file__))

# watch_dog
DIRECTORY_FROM_RESERVATION: str = f"{WORK_DIR}/files_to_process"
if not os.path.exists(DIRECTORY_FROM_RESERVATION):
    os.makedirs(DIRECTORY_FROM_RESERVATION)

PROCESSED_FILES: str = f"{WORK_DIR}/list_files"
CHECK_NEW_FILES_TIMEOUT: float = float(
    os.environ.get("CHECK_NEW_FILES_TIMEOUT", "60")
)  # seconds

# RabbitMQ
RMQ_HOST: str = os.environ.get("RMQ_HOST", "localhost")
RMQ_CONNECT_PARAMETERS: dict = {"host": RMQ_HOST}
RMQ_USER: str = os.environ.get("RMQ_USER", "admin")
RMQ_PASSWORD: str = os.environ.get("RMQ_PASSWORD", "admin")
CREDENTIALS: dict = {"username": RMQ_USER, "password": RMQ_PASSWORD}

# Celery
CELERY_QUEUE_PARSING: str = os.environ.get("PARSING", "Parsing")
CELERY_QUEUE_ERRORS: str = os.environ.get("ERRORS", "Errors")
CELERY_QUEUE_READER: str = os.environ.get("CELERY_QUEUE_READER", "Reader")
CELERY_RUN_PARAMETERS: dict = {
    "broker": f"amqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_HOST}//",
    "broker_connection_retry_on_startup": True,
}
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
SMTP_HOST: str = os.environ.get("SMTP_HOST", "localhost")
SMTP_PORT: int = int(os.environ.get("SMTP_SERVER", "1025"))
MAIL_SENDER: str = os.environ.get("MAIL_SENDER", "from@fromdomain.com")
MAIL_RECEIVERS: list = os.environ.get("MAIL_RECEIVERS", "to@todomain.com").split(" ")

# Reader
FRINGE_WRITE_TO_FILE: int = int(os.environ.get("FRINGE_WRITE_TO_FILE", "4300"))
CHECK_WORDS_FOR_WRITE: int = int(os.environ.get("CHECK_WORDS_FOR_WRITE", "5"))

RESULT_DIRECTORY: str = os.environ.get("RESULT_DIRECTORY", "results/")
RESULT_DIRECTORY_PATH: str = f"{WORK_DIR}/{RESULT_DIRECTORY}"
if not os.path.exists(RESULT_DIRECTORY_PATH):
    os.makedirs(RESULT_DIRECTORY_PATH)
