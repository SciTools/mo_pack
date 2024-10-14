# Copyright mo_pack contributors
#
# This file is part of mo_pack and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
import numpy as np
cimport numpy as np

# Must be called to use the C-API with Numpy
np.import_array()

#: The WGDOS packing algorithm generally produces smaller data payloads
#: than the unpacked equivalent. However this is not a given, especially
#: for smaller data arrays. With the MINIMUM_WGDOS_PACK_SIZE global we
#: define what the smallest data buffer we are prepared to allocate for packed
#: data to be put into. Even with this safety net, it is assumed there are
#: configurations which will invoke a Seg Fault, in those cases, try setting
#: this even higher.
MINIMUM_WGDOS_PACK_SIZE = 2**8


cdef extern from "logerrors.h":
    ctypedef struct function:
        char name[128]
        function* parent

    void MO_syslog(int value, char* message, const function* const caller)


cdef extern from "rlencode.h":
    int runlen_decode(float* unpacked_data, int unpacked_size,
                      float* packed_data, int packed_size,
                      float mdi, function* parent) nogil

    int runlen_encode(float* unpacked_data, int unpacked_size,
                      float* packed_data, int* packed_size,
                      float mdi, function* parent) nogil


cdef extern from "wgdosstuff.h":
    long wgdos_unpack(char* packed_data,
                      long unpacked_len,
                      float* unpacked_data,
                      float mdi,
                      function* parent) nogil

    long wgdos_pack(long ncols, long nrows,
                    float* unpacked_data,
                    float mdi, long bacc,
                    unsigned char* packed_data,
                    int* packed_length,
                    function* parent) nogil



cdef void MO_syslog(int value, char* message, const function* const caller) noexcept:
    # A dumb implementation of the system logging - i.e. don't do anything.
    pass

## For debugging purposes, enable the following (and comment out the above).
#from libc.stdio cimport printf
#cdef void MO_syslog(int value, char* message, const function* const caller) noexcept:
#    printf(message)
#    printf('\n')


def decompress_rle(packed_data_buffer, int nrows, int ncols,
                   float missing_data_indicator=-1e30):
    """
    Decompress the given data using run-length encoding.

    Args:

    * packed_data_buffer: buffer/memoryview
        The big-endian bytes containing run-length encoded data.

    * nrows: int
        The number of rows in the result array.

    * ncols: int
        The number of columns in the result array.

    Kwargs:

    * missing_data_indicator: float
        The 32-bit floating point value to use as the MDI.
        Defaults to -1e30.

    """
    cdef np.ndarray[np.float32_t, ndim=2, mode="c"] unpacked_data
    unpacked_data = np.empty([nrows, ncols], dtype=np.float32)

    cdef np.ndarray[np.float32_t, ndim=1] packed_data
    packed_data = np.frombuffer(packed_data_buffer, dtype=np.float32)
    # Ensure we have native/host byte order.
    if not np.dtype('>f4').isnative:
        packed_data = packed_data.byteswap()

    cdef long ret_code

    with nogil:
        ret_code = runlen_decode(<float *>unpacked_data.data, nrows * ncols,
                                 <float *>packed_data.data,
                                 packed_data.shape[0], missing_data_indicator,
                                 <function*> None)
    if ret_code != 0:
        raise ValueError('RLE exit code was non-zero: {}'.format(ret_code))

    return unpacked_data


def decompress_wgdos(packed_data_buffer, int nrows, int ncols,
                     float missing_data_indicator=-1e30):
    """
    Decompress the given data using WGDOS encoding.

    """
    cdef np.ndarray[np.float32_t, ndim=2, mode="c"] unpacked_data
    unpacked_data = np.empty([nrows, ncols], dtype=np.float32)

    cdef np.ndarray[np.uint8_t, ndim=1] packed_data
    packed_data = np.frombuffer(packed_data_buffer, dtype=np.uint8)

    cdef long ret_code

    with nogil:
        ret_code = wgdos_unpack(packed_data.data, nrows * ncols,
                                <float *>unpacked_data.data,
                                missing_data_indicator, <function*> None)

    if ret_code != 0:
        raise ValueError('WGDOS exit code was non-zero: {}'.format(ret_code))

    return unpacked_data



def compress_rle(np.ndarray[np.float32_t, ndim=2] unpacked_data,
                 float missing_data_indicator=-1e30):
    """
    Compress the given 2D array with run-length encoding.

    Args:

    * unpacked_data: ndarray
        The 2D array of data to be compressed.

    Kwargs:

    * missing_data_indicator: float
        The 32-bit floating point value to use as the MDI.
        Defaults to -1e30.

    """
    # The x and y size of the input array.
    cdef int d0, d1
    d0, d1 = unpacked_data.shape[0], unpacked_data.shape[1]
    cdef int n_values = unpacked_data.size

    # Allocate the output array for the packing algorithm.
    cdef np.ndarray[np.float32_t, mode="c"] packed_data
    packed_data = np.zeros(d0 * d1, dtype=np.float32)

    # The length of the packed data. A pointer reference will be passed
    # for the packing algorithm to update.
    cdef int length = d0 * d1;

    cdef long ret_code
    with nogil:
        ret_code = runlen_encode(<float *>unpacked_data.data, n_values,
                                 <float *>packed_data.data, &length,
                                 missing_data_indicator, <function*> None)
    if ret_code != 0:
        raise ValueError('WGDOS exit code was non-zero: {}'.format(ret_code))

    # Ensure we have big-endian byte order.
    if not np.dtype('>f4').isnative:
        packed_data.byteswap(True)

    # Return the data buffer which is actually of interest.
    return packed_data[:length].data


def compress_wgdos(np.ndarray[np.float32_t, ndim=2] unpacked_data,
                   long accuracy=-6, float missing_data_indicator=-1e30):
    """
    Compress the given 2D array with the given accuracy using WGDOS encoding.

    """
    # The x and y size of the input array.
    cdef int d0, d1
    d0, d1 = unpacked_data.shape[0], unpacked_data.shape[1]

    # Allocate an array which can be used by the packing algorithm
    buffer_size = max(d0 * d1, MINIMUM_WGDOS_PACK_SIZE)
    cdef np.ndarray[np.float32_t, mode="c"] packed_data
    packed_data = np.zeros(buffer_size, dtype=np.float32)

    # The length of the packed data. A pointer reference will be passed for the
    # packing algorithm to update.
    cdef int length = -1

    cdef long ret_code
    with nogil:
        ret_code = wgdos_pack(d0, d1, <float *>unpacked_data.data,
                              missing_data_indicator, accuracy,
                              <unsigned char *>packed_data.data, &length,
                              <function*> None)

    if ret_code != 0:
        raise ValueError('WGDOS exit code was non-zero: {}'.format(ret_code))

    # Return the data buffer which is actually of interest.
    return packed_data[:length].data
