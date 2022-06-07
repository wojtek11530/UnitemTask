import logging
import os
import threading
from queue import Empty, Queue
from threading import Event

import cv2

from unitem_task.consumer import Consumer
from unitem_task.producer import Producer
from unitem_task.settings import LOG_DATA_FORMAT, LOG_LVL, LOGGING_FORMAT, SAVE_DIR

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOG_DATA_FORMAT,
    level=LOG_LVL,
)


def run_app():
    data_shape = (768, 1024, 3)
    data_limit = 100
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
    save_task_thread = threading.Thread(
        target=save_task,
        args=(
            queue_B,
            stop_event,
        ),
    )

    producer.start()
    consumer.start()
    save_task_thread.start()
    consumer.join()
    producer.join()
    save_task_thread.join()


def save_task(queue: Queue, stop_event: Event):
    os.makedirs(SAVE_DIR, exist_ok=True)

    logging.info("Save task starts working.")
    i = 0
    while not (queue.empty() and stop_event.is_set()):
        try:
            img = queue.get(block=False)
            i += 1
            save_path = SAVE_DIR / f"image_{i}.png"
            logging.info("Save task got image: %d, saving to %s", i, save_path)
            cv2.imwrite(str(save_path), img)
        except Empty:
            logging.debug("Empty queue")

    logging.info("Save task ends working.")


if __name__ == "__main__":
    run_app()
