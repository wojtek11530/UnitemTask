import unittest
from queue import Queue
from threading import Event

from unitem_task.components.producer import Producer


class ProducerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.source_shape = (2, 4, 6)
        self.queue: Queue = Queue()
        self.stop_event = Event()
        self.data_limit = 10
        self.time_period = 1  # ms

    def test_number_of_data_put_to_queue(self):
        data_limit = 10
        producer = Producer(
            source_shape=self.source_shape,
            queue=self.queue,
            stop_event=self.stop_event,
            data_limit=data_limit,
            time_period=self.time_period,
        )

        producer.start()
        producer.join()

        data_put_into_queue_counter = 0
        while not self.queue.empty():
            self.queue.get()
            data_put_into_queue_counter += 1

        self.assertEqual(data_put_into_queue_counter, self.data_limit)

    def test_shape_of_producer_data(self):
        data_limit = 1
        producer = Producer(
            source_shape=self.source_shape,
            queue=self.queue,
            stop_event=self.stop_event,
            data_limit=data_limit,
            time_period=self.time_period,
        )

        producer.start()
        producer.join()

        while not self.queue.empty():
            data_item = self.queue.get()
            self.assertEqual(data_item.shape, self.source_shape)
