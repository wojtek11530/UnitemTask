import unittest
from queue import Queue
from threading import Event
from unittest.mock import patch

import numpy as np

from unitem_task.consumer import Consumer


class ConsumerTestCase(unittest.TestCase):
    def test_number_of_data_put_to_queue(self):
        items_in_queue = 15
        in_queue = Queue()
        for i in range(items_in_queue):
            in_queue.put(1)

        out_queue = Queue()
        stop_event = Event()
        consumer = Consumer(
            in_queue=in_queue, out_queue=out_queue, stop_event=stop_event
        )

        with patch("unitem_task.consumer.Consumer.process_data") as mock:
            mock.return_value = 1
            consumer.start()
            stop_event.set()
            consumer.join()

        data_put_into_queue_counter = 0
        while not out_queue.empty():
            out_queue.get()
            data_put_into_queue_counter += 1

        self.assertEqual(data_put_into_queue_counter, items_in_queue)

    def test_shape_of_process_data(self):
        input_shape = (3, 1000, 500)
        rows, cols, channels = (1000, 600, 3)
        img = np.random.randint(
            256,
            size=rows * cols * channels,
            dtype=np.uint8,
        ).reshape(input_shape)

        out_img = Consumer.process_data(img)
        out_rows, out_cols, out_channels = out_img.shape

        self.assertEqual(out_rows, 500)
        self.assertEqual(out_rows, 300)
