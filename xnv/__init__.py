from typing import NamedTuple, Literal

from .daemon import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=1, minor=0, micro=0, releaselevel="alpha", serial=0
)
