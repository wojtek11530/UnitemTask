import logging
from queue import Queue
from threading import Event

from unitem_task.components.consumer import Consumer
from unitem_task.components.producer import Producer
from unitem_task.components.save_task import SaveTask
from unitem_task.settings import LOG_DATA_FORMAT, LOG_LVL, LOGGING_FORMAT

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOG_DATA_FORMAT,
    level=LOG_LVL,
)


def run_app():
    data_shape = (768, 1024, 3)
    data_limit = 100
    time_period = 50

    queue_A = Queue()
    queue_B = Queue()
    stop_event = Event()

    producer = Producer(
        queue=queue_A,
        stop_event=stop_event,
        data_limit=data_limit,
        time_period=time_period,
        source_shape=data_shape,
    )
    consumer = Consumer(in_queue=queue_A, out_queue=queue_B, stop_event=stop_event)
    save_task = SaveTask(in_queue=queue_B, stop_event=stop_event)

    producer.start()
    consumer.start()
    save_task.start()
    consumer.join()
    producer.join()
    save_task.join()


if __name__ == "__main__":
    run_app()
