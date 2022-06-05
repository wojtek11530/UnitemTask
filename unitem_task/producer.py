import threading
from queue import Queue
from typing import Tuple

import numpy as np


class Producer(threading.Thread):
    def __init__(
        self,
        source_shape: Tuple[int, int, int],
        queue: Queue,
        stop_event: threading.Event,
        data_limit: int,
        time_period: int = 50,
    ):
        super().__init__()

    def run(self) -> None:
        pass
