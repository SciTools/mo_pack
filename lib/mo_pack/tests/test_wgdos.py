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
"""Tests for the `mo_pack.pack_wgdos` and `mo_pack.unpack_wgdos` functions."""

import unittest

import numpy as np
from numpy.testing import assert_array_equal, assert_almost_equal

import mo_pack


class TestPackWGDOS(unittest.TestCase):
    def assert_equal_when_unpacked(self, packed_data, expected_array, mdi=0):
        x, y = expected_array.shape
        unpacked_data = mo_pack.unpack_wgdos(packed_data, x, y, mdi)
        np.testing.assert_array_equal(unpacked_data, expected_array)

    def test_pack_wgdos(self):
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        packed_data = mo_pack.pack_wgdos(data)
        self.assert_equal_when_unpacked(packed_data, data)

    def test_incorrect_size(self):
        data = np.arange(77, dtype=np.float32).reshape(7, 11)     
        packed_data = mo_pack.pack_wgdos(data)
        with self.assertRaises(ValueError):
            unpacked_data = mo_pack.unpack_wgdos(packed_data, 5, 6)

    def test_different_shape(self):
        data = np.arange(24, dtype=np.float32).reshape(8, 3)
        packed_data = mo_pack.pack_wgdos(data)
        unpacked_data = mo_pack.unpack_wgdos(packed_data, 4, 6)
        np.testing.assert_array_equal(unpacked_data, data.reshape(4, 6))

    def test_mdi(self):
        data = np.arange(12, dtype=np.float32).reshape(3, 4)
        packed_data = mo_pack.pack_wgdos(data, missing_data_indicator=4.0)
        expected_data = data
        data[1,0] = 4.0
        self.assert_equal_when_unpacked(packed_data, data, mdi=4.0)

    def test_accuracy(self):
        pass


class TestUnpackWGDOS(unittest.TestCase):
    def test_real_data(self):
        fname = 'test_data/nae.20100104-06_0001_0001.pp'
        with open(fname, 'rb') as fh:
            fh.seek(268)
            data = mo_pack.unpack_wgdos(fh.read(339464), 360, 600)
        assert_almost_equal(data.mean(), 130.84093, decimal=4)
        expected = [[ 388.78125 ,  389.46875 ,  384.0625  ,  388.46875 ],
                    [ 388.09375 ,  381.375   ,  374.28125 ,  374.875   ],
                    [ 382.34375 ,  373.671875,  371.171875,  368.25    ],
                    [ 385.265625,  373.921875,  368.5     ,  365.3125  ]]
        assert_array_equal(data[:4, :4], expected)


if __name__ == '__main__':
    unittest.main()
