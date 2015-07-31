# (C) British Crown Copyright 2015, Met Office
#
# This file is part of mo_pack.
#
# mo_pack is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mo_pack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mo_pack. If not, see <http://www.gnu.org/licenses/>.
"""Tests for the `mo_pack.compress_rle` function."""

from __future__ import absolute_import, division, print_function

import unittest

import numpy as np

from mo_pack import compress_rle


class Test(unittest.TestCase):
    def test_no_mdi(self):
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        compressed_data = compress_rle(data)
        expected = np.arange(42, dtype='f4')
        expected.byteswap(True)
        self.assertEqual(compressed_data, expected.data)

    def test_mdi(self):
        data = np.arange(12, dtype=np.float32).reshape(3, 4) + 5
        data[1, 1:] = 999
        compressed_data = compress_rle(data, missing_data_indicator=999)
        expected = np.array([5, 6, 7, 8, 9, 999, 3, 13, 14, 15, 16],
                                 dtype='f4')
        expected.byteswap(True)
        self.assertEqual(compressed_data, expected.data)

    def test_mdi_larger(self):
        # Check that everything still works if the compressed data are
        # *larger* than the original data.
        data = np.arange(12, dtype=np.float32).reshape(3, 4) + 5
        data[data % 2 == 0] = 666
        with self.assertRaises(ValueError):
            compress_rle(data, missing_data_indicator=666)


if __name__ == '__main__':
    unittest.main()
