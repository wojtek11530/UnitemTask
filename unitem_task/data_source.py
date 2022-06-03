from typing import Tuple

import numpy as np


class Source:
    def __init__(self, source_shape: Tuple[int, int, int]):
        self._source_shape: Tuple[int, int, int] = source_shape

    def get_data(self) -> np.ndarray:
        rows, cols, channels = self._source_shape
        return np.random.randint(
            256,
            size=rows * cols * channels,
            dtype=np.uint8,
        ).reshape(self._source_shape)
