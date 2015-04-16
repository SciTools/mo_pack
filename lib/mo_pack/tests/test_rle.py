"""Tests for the `mo_pack.encode_rle` and `mo_pack.decode_rle` functions."""

import numpy as np
import unittest

import mo_pack


class TestEncodeRLE(unittest.TestCase):
    def test_RLE(self):
        data = np.arange(56, dtype=np.float32).reshape(7, 8)
        encoded_data = mo_pack.encode_rle(data)
        decoded_data = mo_pack.decode_rle(encoded_data, 7, 8)
        np.testing.assert_array_equal(decoded_data, data)

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


if __name__ == '__main__':
    unittest.main()
