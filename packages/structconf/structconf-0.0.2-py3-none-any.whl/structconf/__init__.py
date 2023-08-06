from . import shell
from . import version
from .src import StructConf

__version__ = version.VERSION

__all__ = [
    "shell",
    "version",
    "StructConf"
]
