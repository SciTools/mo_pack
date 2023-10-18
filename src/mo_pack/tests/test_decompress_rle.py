# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Tests for the `mo_pack.decompress_rle` function."""

import unittest

import numpy as np
from numpy.testing import assert_array_equal

from mo_pack import decompress_rle


class Test(unittest.TestCase):
    def test_no_mdi(self):
        # The input to decompress_rle must be big-endian 32-bit floats.
        src_buffer = np.arange(12, dtype='>f4').data
        result = decompress_rle(src_buffer, 3, 4)
        assert_array_equal(result, np.arange(12).reshape(3, 4))
        self.assertEqual(result.dtype, '=f4')

    def test_mdi(self):
        # The input to decompress_rle must be big-endian 32-bit floats.
        src_floats = np.arange(11, dtype='>f4')
        src_floats[5] = 666
        src_floats[6] = 3
        src_buffer = src_floats.data
        result = decompress_rle(src_buffer, 3, 4, missing_data_indicator=666)
        assert_array_equal(result, [[0, 1, 2, 3],
                                    [4, 666, 666, 666],
                                    [7, 8, 9, 10]])

    def test_not_enough_source_data(self):
        src_buffer = np.arange(4, dtype='>f4').data
        with self.assertRaises(ValueError):
            decompress_rle(src_buffer, 5, 6)

    def test_too_much_source_data(self):
        src_buffer = np.arange(10, dtype='>f4').data
        with self.assertRaises(ValueError):
            decompress_rle(src_buffer, 2, 3)


if __name__ == '__main__':
    unittest.main()
