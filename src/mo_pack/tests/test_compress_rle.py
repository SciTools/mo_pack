# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Tests for the `mo_pack.compress_rle` function."""

import unittest

import numpy as np

from mo_pack import compress_rle


class Test(unittest.TestCase):
    def test_no_mdi(self):
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        compressed_data = compress_rle(data)
        expected = np.arange(42, dtype="f4")
        expected.byteswap(True)
        self.assertEqual(compressed_data, expected.data)

    def test_mdi(self):
        data = np.arange(12, dtype=np.float32).reshape(3, 4) + 5
        data[1, 1:] = 999
        compressed_data = compress_rle(data, missing_data_indicator=999)
        expected = np.array([5, 6, 7, 8, 9, 999, 3, 13, 14, 15, 16], dtype="f4")
        expected.byteswap(True)
        self.assertEqual(compressed_data, expected.data)

    def test_mdi_larger(self):
        # Check that everything still works if the compressed data are
        # *larger* than the original data.
        data = np.arange(12, dtype=np.float32).reshape(3, 4) + 5
        data[data % 2 == 0] = 666
        with self.assertRaises(ValueError):
            compress_rle(data, missing_data_indicator=666)


if __name__ == "__main__":
    unittest.main()
