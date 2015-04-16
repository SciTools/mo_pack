# (C) British Crown Copyright 2014, Met Office
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
"""Tests for the `mo_pack.encode_rle` and `mo_pack.decode_rle` functions."""

import unittest

import numpy as np
from numpy.testing import assert_array_equal, assert_almost_equal

import mo_pack


class TestEncodeRLE(unittest.TestCase):
    def assert_equal_when_decoded(self, encoded_data, expected_array, mdi=0):
        x, y = expected_array.shape
        decoded_data = mo_pack.decode_rle(encoded_data, x, y, mdi)
        np.testing.assert_array_equal(decoded_data, expected_array)

    def test_encode_RLE(self):
        data = np.ones([21, 20], dtype=np.float32)
        encoded_data = mo_pack.encode_rle(data)
        self.assert_equal_when_decoded(encoded_data, data)
       
    def test_incorrect_size(self):
        data = np.arange(40, dtype=np.float32).reshape(8, 5)
        packed_data = mo_pack.pack_wgdos(data)
        with self.assertRaises(ValueError):
            unpacked_data = mo_pack.unpack_wgdos(packed_data, 3, 4)

    def test_different_shape(self):
        data = np.arange(48, dtype=np.float32).reshape(8, 6)
        packed_data = mo_pack.pack_wgdos(data)
        unpacked_data = mo_pack.unpack_wgdos(packed_data, 4, 12)
        np.testing.assert_array_equal(unpacked_data, data.reshape(4, 12))

    def test_mdi(self):
        data = np.arange(16, dtype=np.float32).reshape(4, 4)
        packed_data = mo_pack.pack_wgdos(data, missing_data_indicator=4.0)
        expected_data = data
        data[1,0] = 4.0
        self.assert_equal_when_unpacked(packed_data, data, mdi=4.0)


class TestDecodeRLE(unittest.TestCase):
    def test_real_data(self):
        fname = 'test_data/ocean_rle_0001.pp'
        mdi = -1.07374e+09
        with open(fname, 'rb') as fh:
            fh.seek(268)
            data = mo_pack.decode_rle(fh.read(217712), 216, 360, mdi)

        assert_almost_equal(data.mean(), 285.99753, decimal=4) 
        expected = np.array([[mdi, mdi, mdi, mdi],
                          [ mdi,  mdi,  mdi, mdi],
                          [ mdi,  mdi,  mdi, mdi],
                          [  1.98283630e+02,   2.09119446e+02,   1.97984482e+02, 1.85603378e+02]],   
                          dtype=float32)
        assert_array_equal(data[18:22, 35:39], expected)


if __name__ == '__main__':
    unittest.main()
