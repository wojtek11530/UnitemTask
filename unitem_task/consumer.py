import logging
import threading
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np

_SLEEP_TIME = 0.05  # in seconds

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d.%m.%y %H:%M:%S",
    level=logging.INFO,
)


class Consumer(threading.Thread):
    def __init__(self, in_queue: Queue, out_queue: Queue, stop_event: threading.Event):
        super().__init__()
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._stop_event = stop_event

    def run(self) -> None:
        logging.info("Consumer starts working.")
        i = 0
        while not (self._in_queue.empty() and self._stop_event.is_set()):
            logging.info("Consumer tries to get image.")
            try:
                img = self._in_queue.get()
                i += 1
                logging.info("Consumer got image: %d", i)
                processed_img = self.process_data(img)
                self._out_queue.put(processed_img)
            except Empty:
                logging.info("Empty queue")

            sleep(_SLEEP_TIME)

        logging.info("Consumer ends working.")

    @staticmethod
    def process_data(img: np.ndarray) -> np.ndarray:
        width = int(img.shape[1] / 2)
        height = int(img.shape[0] / 2)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img_blurred = cv2.medianBlur(resized, 5)
        return img_blurred
