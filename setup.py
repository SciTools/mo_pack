"""Register the Cython extension."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Self

from Cython.Build import cythonize
import numpy as np
from setuptools import Command, Extension, setup

BASE_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = "mo_pack"
SRC_DIR = BASE_DIR / "src"
PACKAGE_DIR = SRC_DIR / PACKAGE_NAME


class CleanCython(Command):  # type: ignore[misc]
    """Command for purging artifacts built by Cython."""

    description = "Purge artifacts built by Cython"
    user_options: ClassVar[list[tuple[str, str, str]]] = []

    def initialize_options(self: Self) -> None:
        """Set options/attributes/caches used by the command to default values."""

    def finalize_options(self: Self) -> None:
        """Set final values for all options/attributes used by the command."""

    def run(self: Self) -> None:
        """Execute the actions intended by the command."""
        for path in PACKAGE_DIR.rglob("*"):
            if path.suffix in (".pyc", ".pyo", ".c", ".so"):
                msg = f"clean: removing file {path}"
                print(msg)  # noqa: T201
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
