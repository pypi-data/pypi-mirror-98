"""
CodePod is a cloud based compiler that support compiling all the supported
languages and can be deployed anywhere.
"""
import os

from codepod.queues.consumers import RabbitConsumer


def run():
    rc = RabbitConsumer(language=os.getenv("LANGUAGE"))
    rc.consume()


if __name__ == "__main__":
    exit(run())
