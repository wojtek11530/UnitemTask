import threading
import time
from queue import Queue
from typing import Tuple

from unitem_task.data_source import Source

_MILLISECONDS_IN_SEC = 100


class Producer(threading.Thread):
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
        sent_data = 0
        while sent_data < self.data_limit:
            data_item = self._data_source.get_data()
            self._queue.put(data_item)
            sent_data += 1
            time.sleep(self.time_period_ms / _MILLISECONDS_IN_SEC)

        self._stop_event.set()
