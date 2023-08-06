from codepod.constants import QueueConstants
from codepod.queues.abstracts import RabbitQueue


class RabbitCallback(RabbitQueue):
    """
    RabbitMQ producer to push the message to the
    callback queue.
    """

    queue = f"{QueueConstants.DEFAULT_QUEUE}_callback"
