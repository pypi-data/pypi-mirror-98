from codepod.constants import QueueConstants, CodePodEngineStatus
from codepod.engine import CodePodEngine
from codepod.queues.abstracts import RabbitQueue
from codepod.queues.callbacks import RabbitCallback


class RabbitConsumer(RabbitQueue):
    """
    RabbitMQ consumer that gets the messages and process
    it with the help of codepod engine.
    """

    queue = QueueConstants.DEFAULT_QUEUE

    def callback(self, message):
        try:
            cpe = CodePodEngine(data=message)
            message = cpe.run()
        except Exception as ex:
            message["status"] = CodePodEngineStatus.ERROR
            message["error_message"] = str(ex)

        RabbitCallback().push(message)
