# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Integration tests for `mo_pack.compress_rle` and `mo_pack.decompress_rle`."""

import numpy as np
from numpy.testing import assert_array_equal
from numpy.typing import NDArray

from mo_pack import compress_rle, decompress_rle

MDI = 999


class Test:
    """Integration tests for run-length encoding compression."""

    def _test(self, original: NDArray, rows: int, cols: int) -> None:
        compressed_data = compress_rle(original, missing_data_indicator=MDI)
        result = decompress_rle(compressed_data, rows, cols, missing_data_indicator=MDI)
        assert_array_equal(result, original)

    def test_no_mdi(self) -> None:
        """Test RLE compression of data with no MDI values."""
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        self._test(data, 7, 6)

    def test_mdi(self) -> None:
        """Test RLE compression of data with MDI values."""
        data = np.arange(12, dtype=np.float32).reshape(3, 4) + 5
        data[1, 1:] = 999
        self._test(data, 3, 4)
