"""Tests for the `mo_pack.pack_wgdos` and `mo_pack.unpack_wgdos` functions."""

import numpy as np
import unittest

import mo_pack


class TestPackWGDOS(unittest.TestCase):
    def test_WGDOS(self):
        data = np.arange(42, dtype=np.float32).reshape(7, 6)
        packed_data = mo_pack.pack_wgdos(data)
        unpacked_data = mo_pack.unpack_wgdos(packed_data, 7, 6)
        np.testing.assert_array_equal(unpacked_data, data)

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


if __name__ == '__main__':
    unittest.main()
