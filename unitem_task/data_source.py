from typing import Tuple

import numpy as np


class Source:
    def __init__(self, source_shape: Tuple[int, int, int]):
        if len(source_shape) != 3:
            raise ValueError("'source_shape' should have three elements.")
        elif not all(dim > 0 for dim in source_shape):
            raise ValueError("All dims in 'source_shape' should be positive.")
        elif not all(type(dim) == int for dim in source_shape):
            raise ValueError("All dims in 'source_shape' should be integers.")

        self._source_shape: Tuple[int, int, int] = source_shape

    def get_data(self) -> np.ndarray:
        rows, cols, channels = self._source_shape
        return np.random.randint(
            256,
            size=rows * cols * channels,
            dtype=np.uint8,
        ).reshape(self._source_shape)
