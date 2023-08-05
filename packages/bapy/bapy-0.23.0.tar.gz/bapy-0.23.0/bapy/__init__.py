#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""Bapy Package."""
import typer

from .enum import *
from .ip import *
from .lib import *
from .mongo import *
from .nmap import *
from .utils import *

from .enum import __all__ as enum
from .ip import __all__ as ip
from .lib import __all__ as lib
from .mongo import __all__ as mongo
from .nmap import __all__ as nmap
from .utils import __all__ as utils

__all__ = enum + ip + lib + mongo + nmap + utils

if __name__ == '__main__':
    try:
        typer.Exit(app())
    except KeyboardInterrupt:
        red('Aborted!')
        typer.Exit()
