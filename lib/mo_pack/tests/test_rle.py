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
"""
Integration tests for the `mo_pack.compress_rle` and
`mo_pack.decompress_rle` functions.

"""

from __future__ import absolute_import, division, print_function

import unittest

import numpy as np
from numpy.testing import assert_array_equal

from mo_pack import compress_rle, decompress_rle


MDI = 999


class Test(unittest.TestCase):
    def _test(self, original, rows, cols):
        compressed_data = compress_rle(original, missing_data_indicator=MDI)
        result = decompress_rle(compressed_data, rows, cols,
                                missing_data_indicator=MDI)
        assert_array_equal(result, original)

    def test_no_mdi(self):
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        self._test(data, 7, 6)

    def test_mdi(self):
        data = np.arange(12, dtype=np.float32).reshape(3, 4) + 5
        data[1, 1:] = 999
        self._test(data, 3, 4)


if __name__ == '__main__':
    unittest.main()
