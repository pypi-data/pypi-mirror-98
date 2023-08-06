import os
import json
import pika

from codepod.constants import QueueConstants


class RabbitQueue:

    queue = None
    exchange = ""

    def __init__(self, language=None):
        self._validate()

        connection_credentials = pika.PlainCredentials(
            os.getenv(QueueConstants.USERNAME, QueueConstants.DEFAULT_USERNAME),
            os.getenv(QueueConstants.PASSWORD, QueueConstants.DEFAULT_PASSWORD),
        )
        connection_parameters = pika.ConnectionParameters(
            os.getenv(QueueConstants.HOST, QueueConstants.DEFAULT_HOST),
            os.getenv(QueueConstants.PORT, QueueConstants.DEFAULT_PORT),
            "/",
            connection_credentials,
        )
        self.connection = pika.BlockingConnection(connection_parameters)

        self.channel = self.connection.channel()

        if language:
            self.queue = f"{self.queue}_{language}"

        self.channel.queue_declare(queue=self.queue)

    def _consume(self, ch, method, properties, body):
        message = json.loads(body)
        self.callback(message)

    def _validate(self):
        if not self.queue:
            raise NameError(".queue is not defined")

    def consume(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self._consume, auto_ack=True
        )
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            exit(1)

    def push(self, message):
        body = json.dumps(message)
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=self.queue, body=body
        )
        self.connection.close()

    def callback(self, message):
        raise NotImplementedError("callback is not implemented")
