# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""
Tests for the `mo_pack.compress_wgdos` and `mo_pack.decompress_wgdos`
functions.

"""

import os
import unittest

import numpy as np
from numpy.testing import assert_array_equal, assert_almost_equal

import mo_pack


class TestPackWGDOS(unittest.TestCase):
    def assert_equal_when_decompressed(self, compressed_data, expected_array, mdi=0):
        x, y = expected_array.shape
        decompressed_data = mo_pack.decompress_wgdos(compressed_data, x, y, mdi)
        np.testing.assert_array_equal(decompressed_data, expected_array)

    def test_pack_wgdos(self):
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        compressed_data = mo_pack.compress_wgdos(data)
        self.assert_equal_when_decompressed(compressed_data, data)

    def test_mdi(self):
        data = np.arange(12, dtype=np.float32).reshape(3, 4)
        compressed_data = mo_pack.compress_wgdos(data, missing_data_indicator=4.0)
        expected_data = data
        data[1, 0] = 4.0
        self.assert_equal_when_decompressed(compressed_data, expected_data, mdi=4.0)

    def test_accuracy(self):
        data = np.array(
            [[0.1234, 0.2345, 0.3456], [0.4567, 0.5678, 0.6789]], dtype=np.float32
        )
        compressed = mo_pack.compress_wgdos(data, accuracy=-4)
        decompressed_data = mo_pack.decompress_wgdos(compressed, 2, 3)
        expected = np.array(
            [
                [0.12340003, 0.18590003, 0.34560001],
                [0.40810001, 0.56779999, 0.63029999],
            ],
            dtype=np.float32,
        )
        np.testing.assert_array_equal(decompressed_data, expected)


class TestdecompressWGDOS(unittest.TestCase):
    def test_incorrect_size(self):
        data = np.arange(77, dtype=np.float32).reshape(7, 11)
        compressed_data = mo_pack.compress_wgdos(data)
        with self.assertRaises(ValueError):
            _ = mo_pack.decompress_wgdos(compressed_data, 5, 6)

    def test_different_shape(self):
        data = np.arange(24, dtype=np.float32).reshape(8, 3)
        compressed_data = mo_pack.compress_wgdos(data)
        decompressed_data = mo_pack.decompress_wgdos(compressed_data, 4, 6)
        np.testing.assert_array_equal(decompressed_data, data.reshape(4, 6))

    def test_real_data(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        fname = os.path.join(test_dir, "test_data", "nae.20100104-06_0001_0001.pp")
        with open(fname, "rb") as fh:
            fh.seek(268)
            data = mo_pack.decompress_wgdos(fh.read(339464), 360, 600)
        assert_almost_equal(data.mean(), 130.84694, decimal=1)
        expected = [
            [388.78125, 389.46875, 384.0625, 388.46875],
            [388.09375, 381.375, 374.28125, 374.875],
            [382.34375, 373.671875, 371.171875, 368.25],
            [385.265625, 373.921875, 368.5, 365.3125],
        ]
        assert_array_equal(data[:4, :4], expected)


if __name__ == "__main__":
    unittest.main()
