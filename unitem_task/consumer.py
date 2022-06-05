import threading
from queue import Queue

import numpy as np


class Consumer(threading.Thread):
    def __init__(self, in_queue: Queue, out_queue: Queue, stop_event: threading.Event):
        super().__init__()

    def run(self) -> None:
        pass

    @staticmethod
    def process_data(img: np.ndarray) -> np.ndarray:
        pass
