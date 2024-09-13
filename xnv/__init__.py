from typing import NamedTuple, Literal

from .daemon import *
from .wallet import *
from .utils import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=1, minor=0, micro=0, release_level="alpha", serial=0
)
