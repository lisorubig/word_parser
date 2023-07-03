import pika

import celery_app
import settings


def callback(ch, method, properties, body) -> None:
    celery_app.error_to_process.apply_async(kwargs={"body": body})


def main():
    credentials = pika.PlainCredentials(**settings.CREDENTIALS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            **settings.RMQ_CONNECT_PARAMETERS, credentials=credentials
        )
    )

    with connection.channel() as channel:
        channel.queue_declare(queue=settings.QUEUE_PARSING)
        channel.queue_declare(queue=settings.QUEUE_ERRORS)
        channel.basic_consume(
            queue=settings.QUEUE_ERRORS, on_message_callback=callback, auto_ack=True
        )

        channel.start_consuming()


if __name__ == "__main__":
    main()
