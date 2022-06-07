import logging
import threading
import time
from queue import Queue
from typing import Tuple

from unitem_task.components.data_source import Source
from unitem_task.settings import LOG_DATA_FORMAT, LOG_LVL, LOGGING_FORMAT

_MILLISECONDS_IN_SEC = 1000

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOG_DATA_FORMAT,
    level=LOG_LVL,
)


class Producer(threading.Thread):
    """
    Class for Producer thread.

    It runs a task of generating a number of images and passing it to the output queue.

    Args:
        queue (Queue): Output queue
        stop_event (Event): Event which is set when producer ends the task
        data_limit (int): Limit of generated images
        time_period (int): Period of time between producing data, in milliseconds
        source_shape (tuple): Tuple with dimension if generated images

    Attributes:
        data_limit (int): Limit of generated images
        time_period (int): Period of time between producing data, in milliseconds
    """

    def __init__(
        self,
        queue: Queue,
        stop_event: threading.Event,
        data_limit: int,
        time_period: int = 50,
        source_shape: Tuple[int, int, int] = (768, 1024, 3),
    ):
        super().__init__()
        self.data_limit = data_limit
        self.time_period_ms = time_period
        self._data_source = Source(source_shape=source_shape)
        self._queue = queue
        self._stop_event = stop_event

    def run(self) -> None:
        logging.info("Producer starts working.")
        sent_data = 0
        while sent_data < self.data_limit:
            data_item = self._data_source.get_data()
            self._queue.put(data_item)
            sent_data += 1
            logging.info(
                "Producer sent image: %d out of %d.", sent_data, self.data_limit
            )
            time.sleep(self.time_period_ms / _MILLISECONDS_IN_SEC)

        logging.info("Producer sends stop event.")
        self._stop_event.set()
        logging.info("Producer ends working.")
