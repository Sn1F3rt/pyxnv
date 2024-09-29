# Nerva Python Library

[![black](https://github.com/Sn1F3rt/pyxnv/actions/workflows/black.yml/badge.svg)](https://github.com/Sn1F3rt/pyxnv/actions/workflows/black.yml)
[![isort](https://github.com/Sn1F3rt/pyxnv/actions/workflows/isort.yml/badge.svg)](https://github.com/Sn1F3rt/pyxnv/actions/workflows/isort.yml)
[![License](https://img.shields.io/github/license/Sn1F3rt/pyxnv)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/Sn1F3rt/pyxnv)](https://github.com/Sn1F3rt/pyxnv/commits/main/)
[![GitHub stars](https://img.shields.io/github/stars/Sn1F3rt/pyxnv)](https://github.com/Sn1F3rt/pyxnv/)

## Table of Contents

- [About](#about)
- [Installation](#installation)
  * [Requirements](#requirements)
  * [Setup](#setup)
- [Documentation](#documentation)
- [Support](#support)
- [License](#license)

## About

Python bindings for the JSON RPC interface of the Nerva cryptocurrency.

## Installation

### Requirements

- Python 3.8+
- [`poetry`](https://python-poetry.org/) _(for development only)_

### Setup

To install current latest release you can use following command:
```sh
pip install pyxnv
```

To install the latest development version you can use following command:
```sh
poetry add git+https://github.com/Sn1F3rt/pyxnv.git --branch main --with dev
```

## Documentation

Developers please refer to the docstrings in the code for more information. Full API reference will be available soon.

Here is a simple example to get you started:

```python
import asyncio

from xnv.daemon import DaemonJSONRPC


async def main():
    daemon = DaemonJSONRPC(
        host="x.y.z.w",
    )

    print(await daemon.get_info())


asyncio.run(main())
```

## Support

- [Project Issues](https://github.com/Sn1F3rt/pyxnv/issues)
- [Nerva Discord](https://discord.gg/ufysfvcFwe) (Contact `@sn1f3rt`)

## License

[MIT License](LICENSE)

Copyright &copy; 2024 [Sayan "Sn1F3rt" Bhattacharyya](https://sn1f3rt.dev)
