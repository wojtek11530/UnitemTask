import threading
from queue import Queue

import cv2
import numpy as np


class Consumer(threading.Thread):
    def __init__(self, in_queue: Queue, out_queue: Queue, stop_event: threading.Event):
        super().__init__()
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._stop_event = stop_event

    def run(self) -> None:
        while not (self._in_queue.empty() and self._stop_event.is_set()):
            img = self._in_queue.get()
            processed_img = self.process_data(img)
            self._out_queue.put(processed_img)

    @staticmethod
    def process_data(img: np.ndarray) -> np.ndarray:
        width = int(img.shape[1] / 2)
        height = int(img.shape[0] / 2)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img_blurred = cv2.medianBlur(resized, 5)
        return img_blurred
