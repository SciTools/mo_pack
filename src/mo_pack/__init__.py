# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
from ._packing import compress_rle, compress_wgdos, decompress_rle, decompress_wgdos

try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = "unknown"
