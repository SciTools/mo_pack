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
    version='0.1.0dev0',
    ext_modules=cythonize(extensions),
    packages=['mo_pack'],
    package_dir={'': 'lib'},
)
