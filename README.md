# mo_pack

|            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ⚙️ CI      | [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/SciTools/mo_pack/main.svg)](https://results.pre-commit.ci/latest/github/SciTools/mo_pack/main) [![ci-tests](https://github.com/SciTools/mo_pack/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/SciTools/mo_pack/actions/workflows/ci-tests.yml)                                                                                                                                                    |
| ✨ Meta     | [![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![SPEC 0 — Minimum Supported Dependencies](https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038)](https://scientific-python.org/specs/spec-0000/) [![license - bds-3-clause](https://img.shields.io/github/license/SciTools/mo_pack)](https://github.com/SciTools/mo_pack/blob/main/LICENSE) |
| 📦 Package | [![conda-forge](https://img.shields.io/conda/vn/conda-forge/mo_pack?color=orange&label=conda-forge&logo=conda-forge&logoColor=white)](https://anaconda.org/conda-forge/mo_pack)                                                                                                                                                                                                                                                                                                       |
| 🧰 Repo    | [![commits-since](https://img.shields.io/github/commits-since/SciTools/mo_pack/latest.svg)](https://github.com/SciTools/mo_pack/commits/main) [![contributors](https://img.shields.io/github/contributors/SciTools/mo_pack)](https://github.com/SciTools/mo_pack/graphs/contributors) [![release](https://img.shields.io/github/v/release/SciTools/mo_pack)](https://github.com/SciTools/mo_pack/releases)                                                                            |
|            |

Provides Python bindings to the C library [libmo_unpack](https://github.com/SciTools/libmo_unpack) which contains packing methods used to encode and decode the data payloads of Met Office UM Post-Processing and Fields files.

Supports both **RLE** and **WGDOS** encoding methods.

## Developer

Creating a development environment, installing and building `mo_pack` then testing it couldn't be easier!

For example, simply:
```shell
> pixi run --environment py313-test pytest
```

Alternatively:
```shell
> pixi shell --environment py313-test
> python setup.py clean_cython
> python setup.py build_ext --inplace
> pytest
```

## License

`mo_pack` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
