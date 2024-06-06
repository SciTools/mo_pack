from setuptools import Command, Extension, setup

from pathlib import Path

from Cython.Build import cythonize
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = "mo_pack"
SRC_DIR = BASE_DIR / "src"
PACKAGE_DIR = SRC_DIR / PACKAGE_NAME


class CleanCython(Command):
    description = "Purge artifacts built by Cython"
    user_options: list[tuple[str, str, str]] = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for path in PACKAGE_DIR.rglob("*"):
            if path.suffix in (".pyc", ".pyo", ".c", ".so"):
                msg = f"clean: removing file {path}"
                print(msg)
                path.unlink()


# https://setuptools.pypa.io/en/latest/userguide/ext_modules.html
extension = Extension(
    f"{PACKAGE_NAME}._packing",
    [f"src/{PACKAGE_NAME}/_packing.pyx"],
    include_dirs=[np.get_include()],
    libraries=["mo_unpack"],
    # https://cython.readthedocs.io/en/latest/src/userguide/migrating_to_cy30.html?highlight=NPY_NO_DEPRECATED_API#numpy-c-api
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    extra_compile_args=["-std=c99"],
)

setup(
    cmdclass={"clean_cython": CleanCython},
    ext_modules=cythonize(extension, language_level="3str"),
)
