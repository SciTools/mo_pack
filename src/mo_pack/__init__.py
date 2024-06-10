# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Python bindings for the C library **libmo_unpack**.

Provides Python bindings to the C library
`libmo_unpack <https://github.com/SciTools/libmo_unpack>`_ , which contains
packing methods used to encode and decode the data payloads of Met Office UM
Post-Processing and Fields files.

Supports both RLE and WGDOS encoding methods.

"""

from ._packing import compress_rle, compress_wgdos, decompress_rle, decompress_wgdos

try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = "unknown"

__all__ = [
    "__version__",
    "compress_rle",
    "compress_wgdos",
    "decompress_rle",
    "decompress_wgdos",
]
