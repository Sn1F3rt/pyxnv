# Nerva Python Library

[![Lint](https://github.com/Sn1F3rt/pyxnv/actions/workflows/black.yml/badge.svg)](https://github.com/Sn1F3rt/pyxnv/actions/workflows/black.yml)
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
- aiohttp

### Setup

To install current latest release you can use following command:
```sh
python -m pip install pyxnv
```

## Documentation

Developers please refer to the docstrings in the code for more information. Full API reference will be available soon.

Here is a simple example to get you started:

```python
import asyncio

from xnv import Daemon


async def main():
    daemon = Daemon(
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
