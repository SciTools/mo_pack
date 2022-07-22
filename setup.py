from __future__ import absolute_import, division, print_function

from distutils.core import setup
import os

import numpy as np
import setuptools

from Cython.Build import cythonize


def file_walk_relative(top, remove=''):
    """
    Returns a generator of files from the top of the tree, removing
    the given prefix from the root/file result.

    """
    top = top.replace('/', os.path.sep)
    remove = remove.replace('/', os.path.sep)
    for root, dirs, files in os.walk(top):
        for file in files:
            yield os.path.join(root, file).replace(remove, '')


extensions = [setuptools.Extension('mo_pack._packing',
                                   ['lib/mo_pack/_packing.pyx'],
                                   include_dirs=[np.get_include()],
                                   libraries=['mo_unpack'])]

setup(
    name='mo_pack',
    description='Python wrapper to libmo_unpack',
    version='0.2.0',
    ext_modules=cythonize(extensions),
    packages=['mo_pack', 'mo_pack.tests'],
    package_dir={'': 'lib'},
    package_data={'mo_pack': list(
        file_walk_relative('lib/mo_pack/tests/test_data/',
                           remove='lib/mo_pack/'))},
    classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: AIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: GIS',
    ],
)
