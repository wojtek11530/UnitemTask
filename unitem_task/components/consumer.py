import logging
import threading
from queue import Empty, Queue

import cv2
import numpy as np

from unitem_task.settings import LOG_DATA_FORMAT, LOG_LVL, LOGGING_FORMAT

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOG_DATA_FORMAT,
    level=LOG_LVL,
)


class Consumer(threading.Thread):
    """
    Class for Consumer thread.

    It runs a task of consuming images from input queue, preprocessing them and passing to
    the output queue. It ends its work when the input queue is empty and when stop event is set.

    Args:
        in_queue (Queue): Input queue
        out_queue (Queue): Output queue
        stop_event (Event): Event which stops consumer work
    """

    def __init__(self, in_queue: Queue, out_queue: Queue, stop_event: threading.Event):
        super().__init__()
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._stop_event = stop_event

    def run(self) -> None:
        logging.info("Consumer starts working.")
        i = 0
        while not (self._in_queue.empty() and self._stop_event.is_set()):
            try:
                img = self._in_queue.get(block=False)
                i += 1
                logging.info("Consumer got image: %d.", i)
                processed_img = self.process_data(img)
                self._out_queue.put(processed_img)
            except Empty:
                logging.debug("Empty queue")

        logging.info("Consumer ends working.")

    @staticmethod
    def process_data(img: np.ndarray) -> np.ndarray:
        width = int(img.shape[1] / 2)
        height = int(img.shape[0] / 2)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img_blurred = cv2.medianBlur(resized, 5)
        return img_blurred
