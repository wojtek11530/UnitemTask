import logging
import os
import threading
from queue import Empty, Queue

import cv2

from unitem_task.settings import LOG_DATA_FORMAT, LOG_LVL, LOGGING_FORMAT, SAVE_DIR

logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOG_DATA_FORMAT,
    level=LOG_LVL,
)


class SaveTask(threading.Thread):
    """
    Class for thread with save task.

    It runs a task which saves images from input queue as png files. It ends its work when the
    input queue is empty and when the stop event is set.

    Args:
        in_queue (Queue): Input queue
        stop_event (Event): Event which stops consumer work
    """

    def __init__(self, in_queue: Queue, stop_event: threading.Event):
        super().__init__()
        self._in_queue = in_queue
        self._stop_event = stop_event

    def run(self) -> None:
        logging.info("Save task starts working.")
        os.makedirs(SAVE_DIR, exist_ok=True)

        i = 0
        while not (self._in_queue.empty() and self._stop_event.is_set()):
            try:
                img = self._in_queue.get(block=False)
                i += 1
                save_path = SAVE_DIR / f"image_{i}.png"
                logging.info("Save task got image: %d, saving to %s", i, save_path)
                cv2.imwrite(str(save_path), img)
            except Empty:
                logging.debug("Empty queue")

        logging.info("Save task ends working.")
