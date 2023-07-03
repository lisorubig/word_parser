import json
import os

import pika

import settings


def read_from_file():
    if os.path.exists(settings.list_files):
        with open(settings.list_files, "r", encoding="utf-8") as f:
            file = f.read()
        return json.loads(file)
    else:
        return []


def write_processed_files(processed_files):
    with open(settings.list_files, "w", encoding="utf-8") as wf:
        wf.write(json.dumps(processed_files))


def write_to_rmq(
    rmq_channel: pika.BlockingConnection.channel,
    file_name: str,
) -> None:
    path_to_file = f"{settings.work_dir}/{file_name}"
    try:
        with open(path_to_file, "r", encoding="utf-8") as f:
            f.readline()
    except UnicodeDecodeError:
        rmq_queue = settings.QUEUE_ERRORS
    else:
        rmq_queue = settings.QUEUE_PARSING

    rmq_channel.basic_publish(
        exchange="",
        routing_key=rmq_queue,
        body=path_to_file.encode(),
    )


def main(rmq_channel: pika.BlockingConnection.channel) -> None:
    files_in_directory = os.listdir(path=settings.work_dir)
    old_files = read_from_file()

    new_files = set(files_in_directory) - set(old_files)
    print("new_files", new_files)

    for file_name in new_files:
        write_to_rmq(rmq_channel, file_name)
        old_files.append(file_name)
        write_processed_files(old_files)

        print(file_name)


def z():
    credentials = pika.PlainCredentials(**settings.CREDENTIALS)

    with pika.BlockingConnection(
        pika.ConnectionParameters(
            **settings.RMQ_CONNECT_PARAMETERS, credentials=credentials
        )
    ) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=settings.QUEUE_PARSING)
        channel.queue_declare(queue=settings.QUEUE_ERRORS)
        main(channel)
