from queue import Queue
from threading import Event

from unitem_task.consumer import Consumer
from unitem_task.producer import Producer


def run_app():
    data_shape = (768, 1024, 3)
    data_limit = 10
    time_period = 5

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

    producer.start()
    consumer.start()
    consumer.join()
    producer.join()


if __name__ == "__main__":
    run_app()
