# mo_pack 

|            |                                                                                                                                                                                                                                                                                                                                                                                                            |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ⚙️ CI      | [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/SciTools/mo_pack/main.svg)](https://results.pre-commit.ci/latest/github/SciTools/mo_pack/main) [![ci-tests](https://github.com/SciTools/mo_pack/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/SciTools/mo_pack/actions/workflows/ci-tests.yml)                                                                         |
| ✨ Meta     | [![NEP29](https://raster.shields.io/badge/follows-NEP29-orange.png)](https://numpy.org/neps/nep-0029-deprecation_policy.html) [![license - bds-3-clause](https://img.shields.io/github/license/SciTools/mo_pack)](https://github.com/SciTools/mo_pack/blob/main/LICENSE)                                                                                                                                   |
| 📦 Package | [![conda-forge](https://img.shields.io/conda/vn/conda-forge/mo_pack?color=orange&label=conda-forge&logo=conda-forge&logoColor=white)](https://anaconda.org/conda-forge/mo_pack)                                                                                                                                                                                                                            |
| 🧰 Repo    | [![commits-since](https://img.shields.io/github/commits-since/SciTools/mo_pack/latest.svg)](https://github.com/SciTools/mo_pack/commits/main) [![contributors](https://img.shields.io/github/contributors/SciTools/mo_pack)](https://github.com/SciTools/mo_pack/graphs/contributors) [![release](https://img.shields.io/github/v/release/SciTools/mo_pack)](https://github.com/SciTools/mo_pack/releases) |
|            |

Provides Python bindings to the C library [libmo_unpack](https://github.com/SciTools/libmo_unpack) which contains packing methods used to encode and decode the data payloads of Met Office UM Post-Processing and Fields files.

Supports both **RLE** and **WGDOS** encoding methods.

## Developer Installation

First, create a `conda` environment with the required `mo_pack` package dependencies:
```shell
conda env create --file requirements/mo_pack.yml
```

Then activate the `conda` environment:
```shell
conda activate mo-pack-dev
```

Now, perform a developer (editable) installation of `mo_pack`:
```shell
pip install --no-deps --editable .
```

Before testing `mo_pack` to ensure that the installation is successful, build the `cython` extension:
```shell
python setup.py clean_cython
python setup.py build_ext --inplace
```

Now run the `mo_pack` tests:
```shell
pytest
```

## License

`mo_pack` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
