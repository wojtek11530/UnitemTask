import unittest

import numpy as np

from unitem_task.components.data_source import Source


class DataSourceTestSuite(unittest.TestCase):
    def test_get_data_shape(self):
        given_shape = (2, 4, 6)

        source = Source(given_shape)
        data = source.get_data()
        self.assertEqual(data.shape, given_shape)

    def test_get_data_dtype(self):
        given_shape = (2, 4, 6)

        source = Source(given_shape)
        data = source.get_data()
        self.assertEqual(data.dtype, np.uint8)

    def test_get_data_randomness(self):
        given_shape = (2, 4, 6)

        source = Source(given_shape)
        data1 = source.get_data()
        data2 = source.get_data()
        self.assertFalse(np.array_equal(data1, data2))

    def test_source_incorrect_shape(self):
        given_shape = (2, 4)

        with self.assertRaises(ValueError):
            source = Source(given_shape)
            source.get_data()

    def est_source_negative_dim(self):
        given_shape = (-100, 200, 3)

        with self.assertRaises(ValueError):
            source = Source(given_shape)
            source.get_data()

    def test_source_negative_dim(self):
        given_shape = (2, 4, 10.2)

        with self.assertRaises(ValueError):
            source = Source(given_shape)
            source.get_data()
