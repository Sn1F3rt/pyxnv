from typing import NamedTuple, Literal

from . import (
    daemon as daemon,
    wallet as wallet,
    utils as utils,
)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=1, minor=0, micro=0, releaselevel="beta", serial=0
)

del NamedTuple, Literal, VersionInfo
