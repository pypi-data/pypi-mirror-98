#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Enum Module."""
import collections
import concurrent.futures
import enum
import inspect
import logging
import typing
from typing import Any
from typing import NamedTuple
from typing import Type

import box
import verboselogs

__all__ = [
    'AliasType',
    'Enum',
    'EnumType',
    'AttributeKind',
    'Attribute',
    'ChainMapRV',
    'Executor',
    'GetAll',
    'ListUtils',
    'LogLevel',
    'PathIs',
    'PathMode',
    'PathOption',
    'PathOutput',
    'PathSuffix',
    'Priority',
    'Sems',
]

AliasType = typing._alias


class Enum(enum.Enum):

    @staticmethod
    def _check_methods(C, *methods):
        # collections.abc._check_methods
        mro = C.__mro__
        for method in methods:
            for B in mro:
                if method in B.__dict__:
                    if B.__dict__[method] is None:
                        return NotImplemented
                    break
            else:
                return NotImplemented
        return True

    @classmethod
    def asdict(cls):
        return {key: value._value_ for key, value in cls.__members__.items()}

    @classmethod
    def attrs(cls):
        return list(cls.__members__)

    @staticmethod
    def auto():
        return enum.auto()

    @classmethod
    def default(cls):
        return cls._member_map_[cls._member_names_[0]]

    @classmethod
    def default_attr(cls):
        return cls.attrs()[0]

    @classmethod
    def default_dict(cls):
        return {cls.default_attr(): cls.default_value()}

    @classmethod
    def default_value(cls):
        return cls[cls.default_attr()]

    @property
    def describe(self):
        """
        Returns:
            tuple:
        """
        # self is the member here
        return self.name, self.value

    @property
    def lower(self):
        return self.name.lower()

    @property
    def lowerdot(self):
        return self.value if self.name == 'NO' else f'.{self.name.lower()}'

    def prefix(self, prefix):
        return f'{prefix}_{self.name}'

    @classmethod
    def values(cls):
        return list(cls.asdict().values())

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Enum:
            attrs = [C] + ['asdict', 'attrs', 'auto', 'default', 'default_attr', 'default_dict', 'default_value',
                           'describe', 'lower', 'lowerdot', 'prefix', 'values', '_generate_next_value_', '_missing_',
                           'name', 'value'] + inspect.getmembers(C)
            return cls._check_methods(*attrs)
        return NotImplemented


EnumType = AliasType(Enum, 1, name=Enum.__name__)


class AttributeKind(Enum):
    CALLABLE = 'callable'
    CLASS = 'class method'
    DATA = 'data'
    GETSET = 'getset descriptor'
    MEMBER = 'member descriptor'
    METHOD = 'method'
    PROPERTY = 'property'
    STATIC = 'static method'


Attribute = NamedTuple('Attribute', cls=Type, kind=AttributeKind, object=Any)


class ChainMapRV(Enum):
    ALL = enum.auto()
    FIRST = enum.auto()
    UNIQUE = enum.auto()


class Executor(Enum):
    THREAD = concurrent.futures.ThreadPoolExecutor
    PROCESS = concurrent.futures.ProcessPoolExecutor


class GetAll(Enum):
    KEYS = Enum.auto()
    VALUES = Enum.auto()


class ListUtils(Enum):
    LOWER = Enum.auto()
    UPPER = Enum.auto()
    CAPITALIZE = Enum.auto()


class LogLevel(Enum):
    SPAM = verboselogs.SPAM
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    NOTICE = verboselogs.NOTICE
    WARNING = logging.WARNING
    SUCCESS = verboselogs.SUCCESS
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class PathIs(Enum):
    DIR = 'is_dir'
    FILE = 'is_file'


class PathMode(Enum):
    DIR = 0o666
    FILE = 0o777
    X = 0o755


class PathOption(Enum):
    BOTH = Enum.auto()
    DIRS = Enum.auto()
    FILES = Enum.auto()


class PathOutput(Enum):
    BOTH = 'both'
    BOX = box.Box
    DICT = dict
    LIST = list
    NAMED = collections.namedtuple
    TUPLE = tuple


class PathSuffix(Enum):
    NO = str()
    BASH = Enum.auto()
    ENV = Enum.auto()
    GIT = Enum.auto()
    INI = Enum.auto()
    J2 = Enum.auto()
    JINJA2 = Enum.auto()
    LOG = Enum.auto()
    MONGO = Enum.auto()
    OUT = Enum.auto()
    PY = Enum.auto()
    RLOG = Enum.auto()
    SH = Enum.auto()
    TESTS = Enum.auto()
    TOML = Enum.auto()
    YAML = Enum.auto()
    YML = Enum.auto()


class Priority(Enum):
    HIGH = 20
    LOW = 1


class Sems(Enum):
    HTTP = enum.auto()
    MAX = enum.auto()
    MONGO = enum.auto()
    NMAP = enum.auto()
    OS = enum.auto()
    SSH = enum.auto()
    PING = enum.auto()
    SOCKET = enum.auto()
    TESTS = enum.auto()


class TaskAsync(Enum):
    CANCELLED = enum.auto()
    FINISHED = enum.auto()
    PENDING = enum.auto()


class TaskProducer(Enum):
    WAITING = enum.auto()
    PRODUCED = enum.auto()
    RUNNING = enum.auto()
    DONE = enum.auto()


class TaskSync(Enum):
    WAITING = enum.auto()
    ACQUIRED = enum.auto()
    RELEASED = enum.auto()
