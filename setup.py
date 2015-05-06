from __future__ import absolute_import, division, print_function

from distutils.core import setup

import numpy as np
import setuptools

from Cython.Build import cythonize


extensions = [setuptools.Extension(
    "mo_pack._packing",
    ["lib/mo_pack/_packing.pyx"],
    include_dirs=[np.get_include()],
    libraries=['mo_unpack'])]

setup(
    name='mo_pack',
    description='Python wrapper to libmo_unpack',
    version='0.1.0',
    ext_modules=cythonize(extensions),
    packages=['mo_pack'],
    package_dir={'': 'lib'},
    classifiers=[
            'Development Status :: 3 - Alpha',
            ('License :: OSI Approved :: '
             'GNU Lesser General Public License v3 or later (LGPLv3+)'),
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
