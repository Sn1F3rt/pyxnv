from typing import Tuple

import argparse
import sys

import xnv
import aiohttp
import platform


def show_version() -> None:
    entries = list()

    v = sys.version_info
    entries.append(
        f"- Python v{v.major}.{v.minor}.{v.micro}"
        + (f"-{v.releaselevel}" if v.releaselevel != "final" else "")
    )

    v = xnv.version_info
    entries.append(
        f"- pyxnv v{v.major}.{v.minor}.{v.micro}"
        + (f"{v.releaselevel[0]}{v.serial}" if v.releaselevel != "final" else "")
    )

    entries.append(f"- aiohttp v{aiohttp.__version__}")

    uname = platform.uname()
    entries.append(f"- System Info: {uname.system} {uname.release} {uname.version}")

    print("\n".join(entries))


def core(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.version:
        show_version()
    else:
        parser.print_help()


def parse_args() -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    parser = argparse.ArgumentParser(
        prog="pyxnv", description="Tools for helping with the library"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Shows the library version"
    )
    parser.set_defaults(func=core)

    return parser, parser.parse_args()


def main() -> None:
    parser, args = parse_args()
    args.func(parser, args)


if __name__ == "__main__":
    main()
