# -*- coding: utf-8 -*-
"""Bapy Lib Module."""
from __future__ import annotations

import ast
import asyncio
import collections
import configparser
import dataclasses
import dis
import enum
import importlib.metadata
import inspect
import io
import itertools
import json
import logging
import logging.handlers
import mailbox
import os
import pathlib
import pkgutil
import platform
import pprint
import reprlib
import shlex
import shutil
import site
import socket
import subprocess
import sys
import threading
import time
import traceback
import tracemalloc
import typing
import warnings
from abc import ABCMeta
from abc import abstractmethod
from asyncio import to_thread
from collections import defaultdict
from collections import OrderedDict
from contextlib import suppress
from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field as datafield
from dataclasses import InitVar
from functools import partial
from functools import singledispatch
from functools import total_ordering
from functools import wraps
from json import JSONEncoder
from logging import Logger
from typing import Any
from typing import ByteString
from typing import Callable
from typing import cast
from typing import ClassVar
from typing import Coroutine
from typing import Generator
from typing import Iterable
from typing import Iterator
from typing import KeysView
from typing import Literal
from typing import Mapping
from typing import MutableMapping
from typing import MutableSequence
from typing import MutableSet
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar
from typing import Union
from typing import ValuesView

import _abc
import box
import click
import click_completion
import colorlog
import decorator
import distro
import dotenv
import dpath.util
import environs
import furl
import git
# noinspection PyCompatibility
import grp
import inflect
import jinja2
import jsonpickle.util
import psutil
# noinspection PyCompatibility
import pwd
import pytest
import requests
import rich
import rich.logging
import rich.prompt
import ruamel.yaml
import setuptools.command.develop
import setuptools.command.install
import shell_proc
import shellingham
import sty
import typer
import urllib3
import verboselogs
from bson import ObjectId
from icecream import IceCreamDebugger

from .enum import *

__all__ = [
    'datafield',
    '__version__',
    'app',
    'appcontext',
    'authorized_keys',
    'cprint',
    'gitconfig',
    'id_rsa',
    'id_rsa_pub',
    'fm',
    'fmi',
    'fmt',
    'plural',
    'ssh_dir',
    'GenericAlias',
    'Module',
    'LST',
    'LSTArgs',
    'SeqNoStr',
    'SeqNoStrArgs',
    'Seq',
    'SeqArgs',
    'LSTType',
    'LSTTypeArgs',
    'CallerVars',
    'Caller',
    'Cmd',
    'ConfLogPath',
    'DebugEnv',
    'LogEnv',
    '_Task',
    'TasksLiteral',
    'TasksNamed',
    'UserPasswd',
    'debug_defaults',
    'log_defaults',
    'tasks_named',
    'fixture_args',
    'memoize',
    'memonoself',
    'memonoself_aio',
    'memonone',
    'once',
    'runwarning',
    'Base',
    'BaseData',
    'BaseDataDescriptor',
    'AliasedGroup',
    'ArgsKwargs',
    'ChainMap',
    'DataPostDefault',
    'Distro',
    'Env',
    'EnvInterpolation',
    'Executable',
    'GitHub',
    'HashAuto',
    'hashdict',
    'Kill',
    'Log',
    'Machine',
    'Obj',
    'Path',
    'Py',
    'Sem',
    'SetUpToolsPostDevelopCommand',
    'SetUpToolsPostInstallCommand',
    'SetUpToolsScriptPath',
    'Up',
    'Url',
    'UserActual',
    'UserProcess',
    'User',
    'add_options',
    'aiocmd',
    'aioclosed',
    'aioloop',
    'aioloopid',
    'aiorunning',
    'appdir',
    'ask',
    'base64auth',
    'clean_empty',
    'click_custom_startswith',
    'click_completion',
    'cmd',
    'cmd_completion',
    'confirmation',
    'datafactory',
    'datafactorytype',
    'default_dict',
    'del_key',
    'dict_exclude',
    'dict_include',
    'dict_sort',
    '_info',
    'distribution',
    'dump_ansible_yaml',
    'executor',
    'flat_list',
    'force_async',
    'get_all',
    'get_choice_class',
    'gen_key',
    'get_context',
    'get_key',
    'get_vars_docs',
    'is_data',
    'is_pip',
    'iter_split',
    'list_utils',
    'literal',
    'load_modules',
    'mapped_commands',
    'metadata',
    'mod_name',
    'move_to_key',
    'namedtuple',
    'namedtype',
    'not_',
    '_package',
    'package_info',
    'package_latest',
    'package_latest_search',
    'pop_default',
    'prefix_suffix',
    'print_modules',
    'pypifree',
    'rename_keys',
    'reverse_dict',
    'secrets',
    'sub_run',
    'sub_run_sys',
    'tasks',
    'to_dict_or_list',
    'trace',
    'true_bool',
    'tty_max',
    'upcase_values',
    'upgrade_message',
    'upper_prefix',
    'value_from_dict',
    'vars_to_dict',
    '_version',
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'bblack',
    'bred',
    'bgreen',
    'byellow',
    'bblue',
    'bmagenta',
    'bcyan',
    'bwhite',
    'reset',
    'setup_bapy',
    'setup_package',
]

# <editor-fold desc="Constants & Typing">
__version__ = '0.22.34'
urllib3.disable_warnings()

app = typer.Typer()
appcontext = dict(help_option_names=['-h', '--help'], color=True)
authorized_keys = 'authorized_keys'
cprint = rich.console.Console().print
gitconfig = '.gitconfig'
ic = IceCreamDebugger(prefix=str())
icc = IceCreamDebugger(prefix=str(), includeContext=True)
id_rsa = 'id_rsa'
id_rsa_pub = 'id_rsa.pub'
fm = pprint.pformat
fmi = IceCreamDebugger(prefix=str()).format
fmt = IceCreamDebugger(prefix=str(), includeContext=True).format
plural = inflect.engine().plural
ssh_dir = '.ssh'

GenericAlias = typing._GenericAlias
Module = type(logging)
LST = Union[MutableSet, MutableSequence, tuple]
# noinspection PyUnresolvedReferences
LSTArgs = LST.__args__
SeqNoStr = Union[LST, KeysView, ValuesView, Iterator]
# noinspection PyUnresolvedReferences
SeqNoStrArgs = SeqNoStr.__args__
Seq = Union[SeqNoStr, Sequence, ByteString, str, bytes]
# noinspection PyUnresolvedReferences
SeqArgs = Seq.__args__

LSTType = TypeVar('LSTType', MutableSet, MutableSequence, tuple)
LSTTypeArgs = LSTType.__constraints__
# </editor-fold>

# <editor-fold desc="NamedTuple">
CallerVars = NamedTuple('CallerVars', glob=dict, loc=dict)
Cmd = NamedTuple('Cmd', stdout=Union[list, str], stderr=Union[list, str], rc=int)
ConfLogPath = NamedTuple('ConfLogPath', dir=Any, env=Any, file=Any, rlog=Any)
DebugEnv = NamedTuple('DebugEnv', debug_async=bool, ic=bool, verbose=bool)
LogEnv = NamedTuple('LogEnv', log_level=int, log_level_file=int, log_level_packages=int)
_Task = dict[str, dict[str, asyncio.Task]]
TasksLiteral = Literal['cancelled', 'finished', 'pending']
TasksNamed = NamedTuple('TasksNamed', cancelled=_Task, finished=_Task, pending=_Task)
UserPasswd = collections.namedtuple('UserPasswd', 'username password')

debug_defaults = DebugEnv(*[False] * len(DebugEnv._fields))
log_defaults = LogEnv(logging.ERROR, logging.DEBUG, logging.ERROR)
obj_defaults = NamedTuple('ObjDefaults', depth=Optional[int], ignore=bool, swith=str)(None, False, '__')
tasks_named = TasksNamed(*TasksNamed._fields)


# </editor-fold>

# <editor-fold desc="Decorators">
def _memoize(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args, frozenset(kw.items())
    else:
        key = args
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kw)
    return cache[key]


def _memonoself(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args[1:], frozenset(kw.items())
    else:
        key = args[1:]
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = func(*args, **kw)
    return cache[key]


async def _memonoself_aio(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args[1:], frozenset(kw.items())
    else:
        key = args[1:]
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        cache[key] = await func(*args, **kw)
    return cache[key]


def _memonone(func, *args, **kw):
    if kw:  # frozenset is used to ensure hashability
        key = args, frozenset(kw.items())
    else:
        key = args
    cache = func.cache  # attribute added by memoize
    if key not in cache:
        if (rv := func(*args, **kw)) is None:
            return None
        cache[key] = rv
    return cache[key]


def _omittable_parentheses_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs and len(args) == 1 and callable(args[0]):
            return func()(args[0])
        else:
            return func(*args, **kwargs)

    return wrapper


def _once(func, *args, **kw):
    # args[0] is self.
    if not func.cache:
        func.cache = func(*args, **kw)
    return func.cache


@_omittable_parentheses_decorator
def fixture_args(*pytest_fixture_args, **pytest_fixture_kwargs):
    def decorating(func):
        original_signature = inspect.signature(func)

        def new_parameters():
            for param in original_signature.parameters.values():
                if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                    yield param.replace(kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)

        new_signature = original_signature.replace(parameters=list(new_parameters()))

        if 'request' not in new_signature.parameters:
            raise AttributeError('Target function must have positional-only argument `request`')

        is_async_generator = inspect.isasyncgenfunction(func)
        is_async = is_async_generator or inspect.iscoroutinefunction(func)
        is_generator = inspect.isgeneratorfunction(func)

        if is_async:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                args, kwargs = ArgsKwargs.get_actual_args_kwargs(new_signature, args, kwargs)
                if is_async_generator:
                    async for result in func(*args, **kwargs):
                        yield result
                else:
                    yield await func(*args, **kwargs)
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                args, kwargs = ArgsKwargs.get_actual_args_kwargs(new_signature, args, kwargs)
                if is_generator:
                    yield from func(*args, **kwargs)
                else:
                    yield func(*args, **kwargs)

        wrapper.__signature__ = new_signature
        fixture = pytest.fixture(*pytest_fixture_args, **pytest_fixture_kwargs)(wrapper)
        fixture_name = pytest_fixture_kwargs.get('name', fixture.__name__)

        def parametrizer(*args, **kwargs):
            return pytest.mark.parametrize(fixture_name, [ArgsKwargs(args, kwargs)], indirect=True)

        fixture.arguments = parametrizer

        return fixture

    return decorating


def memoize(f):
    """
    A simple memoize implementation. It works by adding a .cache dictionary
    to the decorated function. The cache will grow indefinitely, so it is
    your responsibility to clear it, if needed.
    """
    f.cache = {}
    return decorator.decorate(f, _memoize)


def memonoself(f):
    """
    Does not cache and check args[0] -> self
    """
    f.cache = {}
    return decorator.decorate(f, _memonoself)


def memonoself_aio(f):
    """
    Does not cache and check args[0] -> self
    """
    f.cache = {}
    return decorator.decorate(f, _memonoself)


def memonone(f):
    """
    Cache after value has changed from None.
    """
    f.cache = {}
    return decorator.decorate(f, _memonone)


def once(f):
    """
    A simple memoize implementation. It works by adding a .cache dictionary
    to the decorated function. The cache will grow indefinitely, so it is
    your responsibility to clear it, if needed.
    """
    f.cache = None
    return decorator.decorate(f, _once)


@decorator.decorator
def runwarning(func, *args, **kwargs) -> Any:
    with warnings.catch_warnings(record=False):
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        warnings.showwarning = lambda *_args, **_kwargs: None
        rv = func(*args, **kwargs)
        return rv


# </editor-fold>


class AliasedGroup(click.Group):
    """
    Implements execution of the first partial match for a command. Fails with a
    message if there are no unique matches.

    See: https://click.palletsprojects.com/en/7.x/advanced/#command-aliases.
    """

    def get_command(self, ctx, cmd_name: str):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


_NOTHING = object()


@dataclass
class ArgsKwargs:
    args: ...
    kwargs: ...

    def __repr__(self):
        return ', '.join(itertools.chain(
            (repr(v) for v in self.args),
            (f'{k}={v!r}' for k, v in self.kwargs.items())))

    @staticmethod
    def flatten_arguments(sig, args, kwargs):
        assert len(sig.parameters) == len(args) + len(kwargs)
        for name, arg in itertools.zip_longest(sig.parameters, args, fillvalue=_NOTHING):
            yield arg if arg is not _NOTHING else kwargs[name]

    @staticmethod
    def get_actual_args_kwargs(sig, args, kwargs):
        request = kwargs["request"]
        try:
            request_args, request_kwargs = request.param.args, request.param.kwargs
        except AttributeError:
            request_args, request_kwargs = (), {}
        return tuple(ArgsKwargs.flatten_arguments(sig, args, kwargs)) + request_args, request_kwargs


class Base:
    """
    Dict and Attributes Class.

    Examples:
        json = jsonpickle.encode(col)
        obj = jsonpickle.decode(obj)
        col.to_file(name=col.col_name)
        assert (Path.cwd() / f'{col.col_name}.json').is_file()
        col.to_file(directory=tmpdir, name=col.col_name, regenerate=True)
        obj = col.from_file(directory=tmpdir, name=col.col_name)
        assert obj == col
    """
    __ignore_attr__ = ['m', 'd', 'v', 'i', 'n', 'w', 's', 'e', 'c', 'x', 'l', 'asdict', 'attrs', 'keys',
                       'kwargs', 'kwargs_dict', 'public', 'values', 'values_dict', ]

    def __init__(self, log: Log = None):
        self.l = log if log else logger if logger else Log.get()

    def child(self, c: Caller) -> Log:
        m = c.modulename
        module = f'{m}.' if m and m != '__main__' or m != '__init__' or '<' not in m else str()
        name = f'{module}{c.qual or c.function}'
        _l = self.l.getChild(name)
        _l.level_set()
        return _l

    @property
    def m(self) -> Any:
        c = Caller()
        return self.child(c).ma if c.coro else self.child(c).m

    @property
    def d(self) -> Any:
        c = Caller()
        return self.child(c).da if c.coro else self.child(c).d

    @property
    def v(self) -> Any:
        c = Caller()
        return self.child(c).va if c.coro else self.child(c).v

    @property
    def i(self) -> Any:
        c = Caller()
        return self.child(c).ia if c.coro else self.child(c).i

    @property
    def n(self) -> Any:
        c = Caller()
        return self.child(c).na if c.coro else self.child(c).n

    @property
    def w(self) -> Any:
        c = Caller()
        return self.child(c).wa if c.coro else self.child(c).w

    @property
    def s(self) -> Any:
        c = Caller()
        return self.child(c).sa if c.coro else self.child(c).s

    @property
    def e(self) -> Any:
        c = Caller()
        return self.child(c).ea if c.coro else self.child(c).e

    @property
    def c(self) -> Any:
        c = Caller()
        return self.child(c).ca if c.coro else self.child(c).c

    @property
    def x(self) -> Any:
        c = Caller()
        return self.child(c).xa if c.coro else self.child(c).x

    @property
    def asdict(self) -> dict:
        """
        Dict including properties without routines and recursive.

        Returns:
            dict:
        """
        return Obj(self).asdict()

    @property
    def attrs(self) -> list:
        """
        Attrs including properties.

        Excludes:
            __ignore_attr__
            __ignore_copy__ instances.
            __ignore_kwarg__

        Returns:
            list:
        """
        return Obj(self).attrs

    def attrs_get(self, *args, default: Any = None) -> dict:
        """
        Get One or More Attributes.

        Examples:
            >>> asdict = Base()
            >>> asdict.d1 = 1
            >>> asdict.d2 = 2
            >>> asdict.d3 = 3
            >>> assert asdict.attrs_get('d1') == {'d1': 1}
            >>> assert asdict.attrs_get('d1', 'd3') == {'d1': 1, 'd3': 3}
            >>> assert asdict.attrs_get('d1', 'd4', default=False) == {'d1': 1, 'd4': False}

        Raises:
            ValueError: ValueError

        Args:
            *args: attr(s) name(s).
            default: default.

        Returns:
            dict:
        """
        if not args:
            raise ValueError(f'args must be provided.')
        return {item: getattr(self, item, default) for item in args}

    def attrs_set(self, *args, **kwargs):
        """
        Sets one or more attributes.

        Examples:
            >>> asdict = Base()
            >>> asdict.attrs_set(d_1=31, d_2=32)
            >>> asdict.attrs_set('d_3', 33)
            >>> d_4_5 = dict(d_4=4, d_5=5)
            >>> asdict.attrs_set(d_4_5)
            >>> asdict.attrs_set('c_6', 36, c_7=37)


        Raises:
            ValueError: ValueError

        Args:
            *args: attr name and value.
            **kwargs: attrs names and values.
        """
        if args:
            if len(args) > 2 or (len(args) == 1 and not isinstance(args[0], dict)):
                raise ValueError(f'args, invalid args length: {args}. One dict or two args (var name and value.')
            kwargs.update({args[0]: args[1]} if len(args) == 2 else args[0])

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def defaults(cls, nested: bool = True) -> dict:
        """
        Return a dict with class attributes names and values.

        Returns:
            list:
        """
        return Obj(cls, depth=None if nested else 1).asdict(defaults=True)

    def from_file(self, directory: Path = None, name: str = None, keys: bool = True):
        name = name if name else self.__class__.__name__
        directory = Path(directory) if directory else Path.cwd()
        with (Path(directory) / f'{name}.json').open() as f:
            return jsonpickle.decode(json.load(f), keys=keys)

    @property
    def keys(self) -> list:
        """
        Keys from kwargs to init class (not InitVars), exclude __ignore_kwarg__ and properties.

        Returns:
            list:
        """
        return Obj(self).keys

    @property
    def kwargs(self) -> dict:
        """
        Kwargs to init class with python objects no recursive, exclude __ignore_kwarg__ and properties.

        Example: Mongo binary.

        Returns:
            dict:
        """
        return Obj(self).kwargs

    @property
    def kwargs_dict(self) -> dict:
        """
        Kwargs recursive to init class with python objects as dict, asdict excluding __ignore_kwarg__ and properties.

        Example: Mongo asdict.

        Returns:
            dict:
        """
        return Obj(self).kwargs_dict

    @property
    def public(self) -> dict:
        """
        Dict including properties without routines.

        Returns:
            dict:
        """
        return Obj(self).public

    def to_file(self, directory: Path = None, name: str = None, regenerate: bool = False, **kwargs):
        name = name if name else self.__class__.__name__
        directory = Path(directory) if directory else Path.cwd()
        with (Path(directory) / f'{name}.json').open(mode='w') as f:
            json.dump(obj=Obj(self).to_json(regenerate=regenerate, **kwargs), fp=f, indent=4, sort_keys=True)

    def to_json(self, regenerate: bool = True, indent: bool = 4, keys: bool = True, max_depth: int = -1) -> JSONEncoder:
        return Obj(self).to_json(regenerate=regenerate, indent=indent, keys=keys, max_depth=max_depth)

    def to_obj(self, keys: bool = True) -> Base:
        return Obj(self).to_obj(keys=keys)

    @property
    def values(self) -> list:
        """
        Init python objects kwargs values no properties and not __ignore_kwarg__.

        Returns:
            list:
        """
        return Obj(self).values

    @property
    def values_dict(self) -> list:
        """
        Init python objects kwargs values no properties and not __ignore_kwarg__.

        Returns:
            list:
        """
        return Obj(self).values_dict


@dataclass
class BaseData(Base):
    log: InitVar[Optional[Log]] = None

    __ignore_attr__ = ['initvars', ]

    def __post_init__(self, log: Optional[Log]):
        self.__init_vars__ = Caller(index=1).args
        super().__init__(log)

    @property
    def initvars(self) -> dict:
        return Obj(self).initvars


@total_ordering
class BaseDataDescriptor(BaseData):
    """
    Sets descriptors for class based on attribute descriptors.
    Class attribute to use the descriptors __descriptor_attr__.
    """
    __descriptor_attr__ = '_id'

    def __add__(self, other):
        return getattr(self, self.__descriptor_attr__).__add__(getattr(other, self.__descriptor_attr__))

    def __contains__(self, other):
        return getattr(self, self.__descriptor_attr__).__contains__(getattr(other, self.__descriptor_attr__))

    def __format__(self, fmt_):
        return getattr(self, self.__descriptor_attr__).__format__(fmt_)

    def __int__(self):
        return getattr(self, self.__descriptor_attr__).__int__()

    def __eq__(self, other):
        return getattr(self, self.__descriptor_attr__).__eq__(getattr(other, self.__descriptor_attr__))

    def __hash__(self):
        return getattr(self, self.__descriptor_attr__).__hash__()

    def __lt__(self, other):
        return getattr(self, self.__descriptor_attr__).__lt__(getattr(other, self.__descriptor_attr__))

    def __reduce__(self):
        return getattr(self, self.__descriptor_attr__).__reduce__()

    def __str__(self):
        return getattr(self, self.__descriptor_attr__).__str__()

    def __sub__(self, other):
        return getattr(self, self.__descriptor_attr__).__sub__(getattr(other, self.__descriptor_attr__))


@dataclass
class Caller:
    args: Optional[dict] = datafield(default=None, init=False)
    code: Optional[list] = datafield(default=None, init=False)
    coro: Optional[bool] = datafield(default=None, init=False)
    description: Optional[str] = datafield(default=None, init=False)
    email: Optional[str] = datafield(default=None, init=False)
    env: Optional[Env] = datafield(default=None, init=False)
    file: Optional[Path] = datafield(default=None, init=False)
    func: Optional[Union[Callable, property]] = datafield(default=None, init=False)
    function: Optional[str] = datafield(default=None, init=False)
    gecos: Optional[str] = datafield(default=None, init=False)
    github: Optional[GitHub] = datafield(default=None, init=False)
    globs: Optional[dict] = datafield(default=None, init=False)
    home: Optional[Path] = datafield(default=None, init=False)
    ic: Optional[IceCreamDebugger] = datafield(default=None, init=False)
    icc: Optional[IceCreamDebugger] = datafield(default=None, init=False)
    imported: Optional[bool] = datafield(default=None, init=False)
    inspect: Optional[dict] = datafield(default=None, init=False)
    installed: Optional[bool] = datafield(default=None, init=False)
    kill: Optional[Kill] = datafield(default=None, init=False)
    locs: Optional[dict] = datafield(default=None, init=False)
    log: Optional[Log] = datafield(default=None, init=False)
    logconf: Optional[ConfLogPath] = datafield(default=None, init=False)
    lineno: Optional[int] = datafield(default=None, init=False)
    module: Optional[Module] = datafield(default=None, init=False)
    modulename: Optional[str] = datafield(default=None, init=False)
    __name__: Optional[str] = datafield(default=None, init=False)
    __package__: Optional[str] = datafield(default=None, init=False)
    package: Optional[str] = datafield(default=None, init=False)
    packages: Optional[str] = datafield(default=None, init=False)
    parameter: Optional[str] = datafield(default=None, init=False)
    path: Optional[Path] = datafield(default=None, init=False)
    prefix: Optional[str] = datafield(default=None, init=False)
    project: Optional[Path] = datafield(default=None, init=False)
    qual: Optional[str] = datafield(default=None, init=False)
    repo: Optional[str] = datafield(default=None, init=False)
    readme: Optional[str] = datafield(default=None, init=False)
    requirements: Optional[dict] = datafield(default=None, init=False)
    scan: Optional[list] = datafield(default=None, init=False)
    scripts: Optional[list] = datafield(default=None, init=False)
    scripts_install: Optional[Path] = datafield(default=None, init=False)
    scripts_relative: Optional[list] = datafield(default=None, init=False)
    sem: Optional[Sem] = datafield(default=None, init=False)
    task: Optional[str] = datafield(default=None, init=False)
    tests: Optional[Path] = datafield(default=None, init=False)
    user: Optional[str] = datafield(default=None, init=False)
    url: Optional[str] = datafield(default=None, init=False)
    vars: Optional[CallerVars] = datafield(default=None, init=False)
    work: Optional[Path] = datafield(default=None, init=False)

    callervars: InitVar[bool] = False
    depth: InitVar[Optional[int]] = obj_defaults.depth
    filename: InitVar[Optional[Path]] = None
    glob: InitVar[bool] = False
    ignore: InitVar[bool] = obj_defaults.ignore
    index: InitVar[int] = 2
    loc: InitVar[bool] = False
    param: InitVar[Optional[str]] = None
    pypi: InitVar[Optional[str]] = str()
    setup: InitVar[bool] = False
    swith: InitVar[str] = obj_defaults.swith
    test: InitVar[bool] = False

    def __post_init__(self, callervars: bool, depth: Optional[None], filename: Optional[Path], glob: bool,
                      ignore: bool, index: int, loc: bool, param: Optional[str], pypi: Optional[str], setup: bool,
                      swith: str, test: bool):
        index_post_init = index + 1  # __init__ calls __post_init__
        with warnings.catch_warnings(record=False):
            warnings.filterwarnings('ignore', category=RuntimeWarning)
            warnings.showwarning = lambda *_args, **_kwargs: None
            try:
                frame = frame_b = inspect.stack()[index_post_init]
            except IndexError:
                index_post_init -= 1
                frame = frame_b = inspect.stack()[index_post_init]

            try:
                frame_b_b = inspect.stack()[index_post_init + 1]
            except IndexError:
                frame_b_b = frame

            if 'asyncio' in frame_b.filename:
                frame = frame_b_b
            if 'asyncio' in frame_b_b.filename:
                frame = frame_b
            self.file = Path(filename) if filename else Path(frame.filename)
            self.globs = frame.frame.f_globals.copy() if 'asyncio' not in frame.filename else dict()
            self.locs = frame.frame.f_locals.copy() if 'asyncio' not in frame.filename else dict()
            if not setup:
                inf = inspect.getargvalues(frame.frame)
                self.args = del_key({name: inf.locals[name] for name in inf.args} | (
                    {inf.varargs: val} if (val := inf.locals.get(inf.varargs)) else dict()) | (
                                        kw if (kw := inf.locals.get(inf.keywords)) else dict()))
                self.code = frame.code_context
                self.lineno = frame.lineno
                self.function = frame.function
                self.task = asyncio.current_task().get_name() if aioloop() else str()
            if index != 1 and not setup:
                self.has()
            if setup:
                self.__package__ = self.globs.get('__package__', str())
                self.parameter = param
                self.set(filename, pypi, test)
            self.globs = self.globs if glob and not setup else dict()
            self.locs = self.locs if loc and not setup else dict()
            self.modulename = inspect.getmodulename(self.file.text)
            self.vars = CallerVars(*[Obj(item, depth=depth, ignore=ignore, swith=swith).asdict()
                                     for item in [self.globs, self.locs]]) if callervars and not setup else CallerVars(
                dict(), dict())

    def get(self):
        if self.func:
            self.coro = Obj(self.func).coro
            self.qual = getattr(self.func, f'__qualname__')

    def get_extra(self):
        def _rv(r):
            self.coro = r[0]['coro']
            self.func = r[0]['value']
            self.qual = r[0]['qual']

        data = self.globs | self.locs
        self.inspect = Obj(data).inspect
        for item in ['self', 'cls']:
            if rv := self.inspect.get(item, dict()).get(self.function):
                _rv(rv)
                break
        if not rv and (rv := self.inspect.get(self.function, dict())):
            _rv(rv)

    def has(self):
        data = self.globs | self.locs
        with warnings.catch_warnings(record=False):
            warnings.filterwarnings('ignore', category=RuntimeWarning)
            warnings.showwarning = lambda *_args, **_kwargs: None
            for item in ['self', 'cls']:
                if obj := data.get(item):
                    if self.function in dir(obj):
                        if item == 'self':
                            cls = getattr(obj, '__class__')
                            self.func = getattr(cls, self.function)
                            if isinstance(self.func, property):
                                self.coro = inspect.isawaitable(getattr(obj, self.function))
                                self.qual = f'{cls.__name__}.{self.function}'
                                return
                            else:
                                self.func = getattr(obj, self.function)
                                self.get()
                        else:
                            self.func = getattr(obj, self.function)
                            self.get()
            if function := data.get(self.function):
                self.func = function
                self.get()

    def set(self, filename: Path, pypi: str, test: bool):
        user = User()
        self.__name__ = self.globs.get('__name__', str())
        self.imported = False
        if self.__name__ in ['importlib._bootstrap', ]:
            sys_path = Path(sys.argv[0]).resolved
            if 'PyCharm' not in sys_path.text:
                self.file = self.file if filename else sys_path
            self.imported = True
        self.installed = False
        self.path = self.file.parent
        self.package = self.path.name
        self.repo = pypi if pypi else self.package
        self.scripts_install = setuptools_script_install_dir()
        installed_bin = None
        if not filename and self.file.is_relative_to(self.scripts_install):
            self.installed = True
            self.package = self.file.name
            self.repo = pypi if pypi else self.package
            self.module = importlib.import_module(self.package)
            self.file = Path(self.module.__file__)
            # noinspection PyUnresolvedReferences
            self.path = Path(importlib.resources.files(self.package))
            installed_bin = True
        if not installed_bin:
            for s in set(site.getsitepackages() + [site.USER_SITE] + [f for f in sys.path if
                                                                      f.endswith('packages')]):
                if self.file.is_relative_to(Path(s)):
                    self.installed = True
                    relative_to = self.file.relative_to(Path(s))
                    self.package = self.file.parent.name if filename else relative_to.parts[0]
                    self.repo = pypi if pypi else self.package
                    self.path = self.file.parent if filename else Path(s) / self.package
                    break

        if not self.installed:
            if (found := self.file.resolved.find_up(file=PathIs.DIR, name=PathSuffix.GIT, previous=True)) == \
                    (None, None,):
                if (found := self.file.resolved.find_up(name='setup.py', previous=True)) == (None, None,):
                    found = (self.file, self.file)
            self.project = found[0].parent
            self.repo = pypi if pypi else self.project.name
            self.path = found[1] if found[1].is_dir() else found[1].parent
            self.package = self.path.name
            if 'importlib._bootstrap' in found[1].text and not filename:
                import setuptools
                self.packages = setuptools.find_packages()
                self.package = self.repo
                if self.packages:
                    self.package = self.repo if self.repo in self.packages else self.packages[0]
                self.path = self.project / self.package

            self.description = self.project.description
            self.email = Url.email()
            self.gecos = user.gecos
            self.readme = self.project.readme
            self.requirements = self.project.requirements
            self.scan = self.project.scan(PathOption.DIRS)
            self.scripts = self.project.scripts
            self.scripts_relative = self.project.scripts_relative
            self.url = Url.lumenbiomics(http=True, repo=self.repo)
        self.home = user.home
        log_dir = self.home.mkdir_add(PathSuffix.LOG.lowerdot)
        self.logconf = ConfLogPath(log_dir, log_dir.touch_add(f'{PathSuffix.LOG.lower}{PathSuffix.ENV.lowerdot}'),
                                   log_dir.touch_add(f'{self.package}{PathSuffix.LOG.lowerdot}'),
                                   log_dir.touch_add(f'{self.package}{PathSuffix.RLOG.lowerdot}'))
        try:
            self.module = self.module if self.module else importlib.import_module(self.package) \
                if self.package else None
        except ModuleNotFoundError:
            pass
        self.repo = pypi if pypi else self.repo
        self.project = self.project if self.project else self.home.mkdir_add(self.repo)
        self.prefix = f'{self.package.upper()}_'
        self.tests = self.project / PathSuffix.TESTS.lower
        self.user = user.name
        self.work = self.home.mkdir_add(f'.{self.package}')

        self.env = Env(prefix=self.prefix, file=self.logconf.env, test=test)
        self.env.call()
        self.ic = deepcopy(ic)
        self.icc = deepcopy(icc)
        self.ic.enabled = self.env.debug.ic
        self.icc.enabled = self.env.debug.ic
        self.log = Log.get(*[self.package, self.logconf.file, *self.env.log._asdict().values(), self.installed])
        self.github = GitHub(path=self.project, log=self.log)
        self.kill = Kill(command=self.package, parameter=self.parameter, log=self.log)
        # noinspection PyTypeChecker
        self.sem = Sem(**self.env.sem | dict(log=self.log))


class ChainMap(collections.ChainMap):
    """Variant of chain that allows direct updates to inner scopes and returns more than one value,
    not the first one."""

    def __init__(self, *maps, rv: ChainMapRV = ChainMapRV.UNIQUE):
        super().__init__(*maps)
        self.rv = rv

    def __getitem__(self, key):
        rv = []
        for mapping in self.maps:
            try:
                value = mapping[key]
                if self.rv is ChainMapRV.FIRST:
                    return value
                if (self.rv is ChainMapRV.UNIQUE and value not in rv) or self.rv is ChainMapRV.ALL:
                    rv.append(value)
            except KeyError:
                pass
        # noinspection PyUnresolvedReferences
        return self.__missing__(key) if self.rv is ChainMapRV.FIRST else rv

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value


@dataclasses.dataclass
class Count(BaseData):
    percentage: str = str()
    ok: int = int()
    error: int = int()
    no: int = int()
    count: int = int()
    total: int = 1
    verbose: bool = False

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)

    async def aouterr(self, msg: str = str()):
        await executor(self.outerr, msg)

    async def aoutno(self, msg: str = str()):
        await executor(self.outno, msg)

    async def aoutok(self, msg: str = str()):
        await executor(self.outok, msg)

    def console(self, msg, error: bool = False, no: bool = False):
        percentage = self.percentage
        ok = self.ok
        total = self.total

        if self.verbose:
            if error:
                cprint(f"[bold blue]{self.percentage}[white] "
                       f"\\[ok: [bold green]{self.ok}[white], "
                       f"error: [bold red]{self.error}[white], "
                       f"no: [bold magenta]{self.no}[white], "
                       f"total: [bold blue]{self.total}[white]] "
                       f"[bold red]{msg}")
                self.e(self.format(msg))
                return
            if no:
                cprint(f"[bold blue]{self.percentage}[white] "
                       f"\\[ok: [bold green]{self.ok}[white], "
                       f"error: [bold red]{self.error}[white], "
                       f"no: [bold magenta]{self.no}[white], "
                       f"total: [bold blue]{self.total}[white]] "
                       f"[bold magenta]{msg}")

            cprint(f"[bold green]{msg}[white] "
                   f"\\[ok: [bold green]{ok}[white], "
                   f"error: [bold red]{self.error}[white], "
                   f"no: [bold magenta]{self.no}[white], "
                   f"total: [bold blue]{total}[white]] "
                   f"[bold blue]{percentage}[white] ")
        self.d(msg, f'{ok=}', f'{total=}', f'{percentage=}')

    def format(self, msg) -> str:
        try:
            return fm(self, msg)
        except IndexError:
            self.d('fm IndexError')

    def get_percentage(self) -> str:
        return f'{round(self.count * 100 / self.total, 2)}%'

    def outerr(self, msg: str = str()):
        self.error += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg, error=True)

    def outno(self, msg: str = str()):
        self.no += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg, no=True)

    def outok(self, msg: str = str()):
        self.ok += 1
        self.count += 1
        self.percentage = self.get_percentage()
        self.console(msg)


@dataclass
class DataPostDefault:

    def post_init_default(self, cls: Any = None, type_index: int = 0):
        """Sets value of field to index of field type: `typing.Union[dict, str, NoneType]`."""
        if dataclasses.is_dataclass(cls):
            for field in dataclasses.fields(cls):
                if getattr(self, field.name) == field.default:
                    setattr(self, field.name, field.type.__args__[type_index]())


@dataclass
class Distro:
    """Distro Class."""
    _info: Any = collections.namedtuple('LinuxDistribution', tuple(distro.LinuxDistribution().info().keys()),
                                        defaults=tuple(distro.LinuxDistribution().info().values()))()
    _id: str = _info.id
    _codename: str = _info.codename
    _like: str = _info.like
    _distro_version_parts: Any = collections.namedtuple('DistroVersionParts', tuple(_info.version_parts.keys()),
                                                        defaults=tuple(_info.version_parts.values()))()
    _version_parts_major: int = int(_distro_version_parts.major)
    _version_parts_minor: int = int(_distro_version_parts.minor)
    _version_parts_build_number: Union[int, str] = int(_distro_version_parts.build_number) \
        if _distro_version_parts.build_number else str()
    CENTOS: bool = True if _id == 'centos' else False
    centos_codenames: tuple = ('Core', 'Final',)
    CENTOS_CORE: bool = True if _codename == 'Core' else False
    CENTOS_FINAL: bool = True if _codename == 'Final' else False
    centos_releases: tuple = ('8', '7', '6',)
    CENTOS_8: bool = True if _version_parts_major == '8' else False
    CENTOS_7: bool = True if _version_parts_major == '7' else False
    CENTOS_6: bool = True if _version_parts_major == '6' else False
    DEBIAN: bool = True if _id == 'debian' else False
    debian_codenames: tuple = ('bookworm', 'bullseye', 'buster', 'stretch',)
    DEBIAN_BOOKWORM: bool = True if _codename == 'bookworm' else False
    DEBIAN_BULLSEYE: bool = True if _codename == 'bullseye' else False
    DEBIAN_BUSTER: bool = True if _codename == 'buster' else False
    DEBIAN_STRETCH: bool = True if _codename == 'stretch' else False
    DEBIAN_LIKE: bool = True if _like == 'debian' or _id == 'debian' else False
    FEDORA: bool = True if _id == 'fedora' else False
    fedora_codenames: tuple = ('',)
    FEDORA_LIKE: bool = \
        True if _like == 'fedora' or _id == 'fedora' or 'fedora' in _like else False
    fedora_releases: tuple = ('33', '32',)
    FEDORA_33: bool = True if _version_parts_major == '33' else False
    FEDORA_32: bool = True if _version_parts_major == '32' else False
    KALI: bool = True if _id == 'kali' else False
    MACOS: bool = psutil.MACOS
    macos_codenames: tuple = ('',)
    POSIX: bool = psutil.POSIX
    RHEL: bool = True if _id == 'rhel' else False
    rhel_codenames: tuple = ('Ootpa', 'Maipo',)
    RHEL_LIKE: bool = True if 'rhel' in _like else False
    rhel_releases: tuple = ('8', '7',)
    RHEL_8: bool = True if _version_parts_major == '8' else False
    RHEL_7: bool = True if _version_parts_major == '7' else False
    UBUNTU: bool = True if _id == 'ubuntu' else False
    ubuntu_codenames: tuple = ('focal', 'bionic', 'xenial',)
    UBUNTU_FOCAL: bool = True if _codename == 'focal' else False
    UBUNTU_BIONIC: bool = True if _codename == 'bionic' else False
    UBUNTU_XENIAL: bool = True if _codename == 'xenial' else False
    kernel: str = _id  # darwin (macOS), linux (redhat, ubuntu) - os.uname().sysname is capitalized
    kernels: tuple = ('darwin', 'linux',)
    KERNEL_AIX: bool = psutil.AIX
    KERNEL_BSD: bool = psutil.BSD
    KERNEL_FREEBSD: bool = psutil.FREEBSD
    KERNEL_DARWIN: bool = True if _id == 'darwin' else False
    KERNEL_LINUX: bool = psutil.LINUX
    KERNEL_NETBSD: bool = psutil.NETBSD
    KERNEL_OPENBSD: bool = psutil.OPENBSD
    KERNEL_SUNOS: bool = psutil.SUNOS
    KERNEL_WINDOWS: bool = psutil.WINDOWS
    build: int = _version_parts_build_number
    codename: str = _codename
    distro: str = _id
    distros: tuple = ('centos', 'darwin', 'debian', 'fedora', 'rhel', 'ubuntu',)
    like: str = _like  # centos is like 'rhel fedora'
    likes: tuple = ('debian', 'fedora', 'rhel fedora',)
    major: int = _version_parts_major
    minor: int = _version_parts_minor
    version: str = _info.version  # macOS (19.5.0), Ubuntu (16.04), rhel (8.2)

    @classmethod
    def exec(cls, name) -> bool:
        """
        Checks if executable is in ``PATH``.

        Args:
            name: executable/command name.

        Returns:
            bool:
        """
        return True if shutil.which(name) is not None else False

    @classmethod
    def install(cls, name, cask: bool = False) -> str:
        """
        Installs package.

        Args:
            name: executable/command name.
            cask: brew cask.

        Raises:
            NotImplementedError: Not installer.
            FileNotFoundError: Not in PATH after install.

        Returns:
            Str:
        """
        brew_url = 'https://raw.githubusercontent.com/Homebrew/install/master/install.sh'
        if not cls.exec(name):
            if cls.MACOS:
                if not cls.exec('brew'):
                    out_cmd = cmd(f'yes yes | /bin/bash -c "$(curl -fsSL {brew_url})" ')
                    if out_cmd.rc != 0:
                        raise NotImplementedError(f'package not available {name}.')
                options = 'cask' if cask else str()
                command = f'brew {options} install'
            elif cls.DEBIAN_LIKE or cls.KALI:
                command = f'apt install -y'
            elif cls.FEDORA_LIKE:
                command = f'yum install -y'
            else:
                raise NotImplementedError('Not installer available.')

            out_cmd = cmd(f'{command} {name}')
            if out_cmd.rc != 0:
                red(pprint.pformat(out_cmd.stderr))

        if cls.exec(name):
            return shutil.which(name)
        raise FileNotFoundError(f'{name} not in PATH.')


@dataclass
class Env(environs.Env):
    """Env Class."""
    eager: bool = False
    expand: bool = True
    override: bool = True
    prefix: str = str()
    verbose: bool = True
    _environ: dict[str, Callable] = datafield(default_factory=dict, init=False)
    error: environs.ErrorMapping = datafield(init=False)
    data: Mapping = datafield(default_factory=dict, init=False)
    debug: DebugEnv = datafield(init=False)
    log: LogEnv = datafield(init=False)
    sem: dict[str, int] = datafield(init=False)
    file: InitVar[Optional[Union[Path, str]]] = None
    test: InitVar[bool] = False

    def __post_init__(self, file: Optional[Union[Path, str]], test: bool):
        super().__init__(eager=self.eager, expand_vars=self.expand)
        dotenv.load_dotenv(str(Path.cwd() / '.env'), verbose=self.verbose, override=self.override)
        if file and not test:
            dotenv.load_dotenv(str(file), verbose=self.verbose, override=self.override)

    def aiodebug(self, enable: bool = False):
        def ok():
            tracemalloc.start()
            self.environ = dict(PYTHONASYNCIODEBUG=1)
            logging.getLogger('asyncio').setLevel(logging.DEBUG)
            warnings.simplefilter('always', ResourceWarning)

        def no():
            tracemalloc.stop()
            self.environ = dict(PYTHONASYNCIODEBUG=0)
            logging.getLogger('asyncio').setLevel(logging.ERROR)
            warnings.simplefilter('ignore', ResourceWarning)

        if self.debug.debug_async or enable:
            return ok()
        return no()

    def call(self):
        self.environ = dict(PYTHONWARNINGS='ignore')
        with self.prefixed(self.prefix):
            self.debug = DebugEnv(*[self.bool(key.upper(), value) for key, value in debug_defaults._asdict().items()])
            self.log = LogEnv(*[self.log_level(key.upper(), value) for key, value in log_defaults._asdict().items()])
            self.sem = {key: self.int(key.upper(), value) for key, value in Sem.defaults().items()}

        self.aiodebug()
        self.error = self.seal()
        self.data = self.dump()

    @property
    def environ(self) -> dict:
        """
        OS Environ Vars Set.

        Returns:
            dict:
        """
        if self._environ:
            return {item: os.environ.get(item.upper()) for item in self._environ}

    @environ.setter
    def environ(self, value: dict):
        """
        Sets `os.environ` Vars and stores keys in `self.environ`.

        Args:
            value: value
        """
        for key, value in value.items():
            os.environ[key.upper()] = str(value)
            call = self.bool if isinstance(value, bool) else self.int if isinstance(value, int) else self.__call__
            self._environ |= {key: call}
            call(key)
            self.data = self.dump()


class EnvInterpolation(configparser.BasicInterpolation):
    """
    Extended Interpolation which expands environment variables in values.

    Examples:
        >>> import os
        >>> os.environ['PATH_TEST'] = '/tmp'
        >>> cfg = '''
        ...     [section]
        ...     key = value
        ...     my_path = ${PATH_TEST}:/private/tmp
        ... '''
        >>>
        >>> config = configparser.ConfigParser(interpolation=EnvInterpolation())
        >>> config.read_string(cfg)
        >>> my_path = config['section']['my_path']
        >>> assert my_path == f'{os.environ["PATH_TEST"]}:/private/tmp'
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

    @staticmethod
    def read_ini(p: Any, raw: bool = True) -> Union[configparser.RawConfigParser, configparser.ConfigParser]:
        """
        Read ini with :class:'~configparser.RawConfigParser` or :class:`EnvInterpolation`.

        Args:
            p: path.
            raw: raw.

        Returns:
            Union[configparser.RawConfigParser, configparser.ConfigParser]:
        """
        if raw:
            i = configparser.RawConfigParser()
            i.optionxform = str
        else:
            i = configparser.ConfigParser(interpolation=EnvInterpolation())

        i.read(str(p))
        return i


@dataclass
class Executable(DataPostDefault):
    apt: Union[Distro.exec, str] = 'apt'
    brew: Union[Distro.exec, str] = 'brew'
    curl: Union[Distro.exec, str] = 'curl'
    docker: Union[Distro.exec, str] = 'docker'
    go: Union[Distro.exec, str] = 'go'
    haproxy: Union[Distro.exec, str] = 'haproxy'
    make: Union[Distro.exec, str] = 'make'
    nmap: Union[Distro.exec, str] = 'nmap'
    npm: Union[Distro.exec, str] = 'npm'
    pip: Union[Distro.exec, str] = 'pip'
    pip3: Union[Distro.exec, str] = 'pip3'
    r: Union[Distro.exec, str] = 'r'
    yum: Union[Distro.exec, str] = 'yum'

    def __post_init__(self):
        self.post_init_default(Executable)


@dataclasses.dataclass
class GitHub(BaseData):
    path: Optional[Path] = None
    clone_rm: bool = None
    config_path: Any = None
    id_rsa: Any = None
    username: str = None
    _version_new: str = None
    _version_old: str = None
    cli: dict[str, list] = datafield(default_factory=dict, init=False)
    cmd: Optional[git.Repo.GitCommandWrapperType] = datafield(default=None, init=False)
    config: git.GitConfigParser = datafield(default=None, init=False)
    remote: git.Remote = datafield(default=None, init=False)
    remote_urls: list = datafield(default_factory=list, init=False)
    repo: git.Repo = datafield(default=None, init=False)
    repo_dirs: box.Box = datafield(default_factory=box.Box, init=False)
    url: Url = datafield(default=None, init=False)

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)
        # _path_installed.project \
        #     if _path_installed.project and not _path_installed.installed else None
        if self.path:
            self.init_clone()
            self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        self.cli = {
            'test_usable': ['git', 'rev-parse', '--git-dir'],
            'commit': ['git', 'commit', '-F'],
        }
        self.config_path = self.config_path if self.config_path else User().git_config_path
        self.config = git.GitConfigParser(self.config_path)
        self.id_rsa = self.id_rsa if self.id_rsa else User().id_rsa
        self.username = self.username if self.username else self.config.get_value(section='user', option='username',
                                                                                  default=str())
        os.environ['GIT_SSH_COMMAND'] = f'ssh -i {self.id_rsa} -o UserKnownHostsFile=/dev/null ' \
                                        f'-o StrictHostKeyChecking=no -o IdentitiesOnly=yes'

    def add(self, force: bool = False, write: bool = True):
        """
        Adds untracked files to Git.

        Args:
            force: force
            write: write
        """
        rv = list()
        if hasattr(self.repo, 'untracked_files'):
            for file in self.repo.untracked_files:
                added = self.repo.index.add(file, force=force, write=write)
                rv.append(added[0][3])
        self.m(rv)
        return rv

    def clone(self, url: str = None, p: Path = None, rm: bool = clone_rm):
        """
        Wrapper for :meth:`git.Repo.clone_from`.
        #
        # Examples:
        #     >>> from bapy import Path, m
        #     >>> ssh_options = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o IdentitiesOnly=yes'
        #     >>> os.environ['GIT_SSH_COMMAND'] = f'ssh -i {User.id_rsa} {ssh_options}'
        #     >>> repo = m.project.name
        #     >>> dest_dir = Path(f'/tmp/{repo}')
        #     >>> dest_dir.rm()
        #     >>> GitHub.clone(Url.lumenbiomics(http=False, repo=repo), dest_dir) #doctest: +ELLIPSIS
        #     <git.repo.base.Repo '/tmp/bapy/.git'>
        #     >>> dest_dir.rm()

        Args:
            url: git url
            p: destination path
            rm: remove before clone

        Returns:
            git.Repo:
        """
        self.clone_rm = rm if rm else self.clone_rm
        if self.clone_rm:
            self.path.rm()
        rv = git.Repo.clone_from(url=url if url else self.url, to_path=p.text if p else self.path.text)
        self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        self.m(rv)
        return rv

    def commit_cmd(self, message: str = None) -> None:
        if message is None:
            message = self.message
        commit = self.cmd.commit('-a', '-m', message)
        self.m(commit)
        return commit

    def fetch(self):
        rv = self.remote.fetch()
        self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        self.m(rv)
        return rv

    def init_clone(self):
        self.url = Url.lumenbiomics(repo=self.path.name)

        try:
            self.repo = git.Repo(self.path)
        except git.exc.NoSuchPathError:
            self.repo = self.clone()
        except git.exc.InvalidGitRepositoryError as exception:
            self.e(exception)

        if self.path.exists() is False:
            self.repo = self.clone()

        if self.repo:
            self.cmd = self.repo.git
            self.remote = self.repo.remote()
            self.remote_urls = [url for url in self.remote.urls]
            self.version_old = self.repo.tags[-1]
            self.repo_dirs = self.path.scan(option=PathOption.DIRS)

    @property
    def message(self) -> str:
        return f'Bump: {self.version_old} --> {self.version_new}'

    def pull(self):
        rv = self.remote.pull()
        self.repo_dirs = self.path.scan(option=PathOption.DIRS)
        self.m(rv)
        return rv

    def push(self, remote: str = 'origin'):
        rv = self.repo.remote(remote).push()
        self.m(f'{rv[0].summary=}', f'{rv[0].flags=}')
        return rv[0].summary, rv[0].flags

    @property
    def status(self) -> str:
        rv = self.cmd.status('--porcelain')
        self.m(rv)
        return rv

    def tag(self, v: str = None):
        if v is None:
            v = self.version_new
        rv = self.repo.create_tag(v)
        self.m(rv)
        return rv

    @property
    def version_new(self):
        return self._version_new

    @version_new.setter
    def version_new(self, v: str):
        self._version_new = v

    @property
    def version_old(self):
        return self._version_old

    @version_old.setter
    def version_old(self, v: str):
        self._version_old = v


class HashAuto:
    """
    Wrapper to make an object hashable, while preserving equality.

    For each known container type, we can optionally provide a tuple
    specifying: type, transform, aggregator
    even immutable types need to be included, since their items
    may make them unhashable

    transformation may be used to enforce the desired iteration
    the result of a transformation must be an iterable
    default: no change; for dictionaries, we use .items() to see values

    usually transformation choice only affects efficiency, not correctness

    aggregator is the function that combines all items into one object
    default: frozenset; for ordered containers, we can use tuple

    aggregator choice affects both efficiency and correctness
    e.g., using a tuple aggregator for a set is incorrect,
    since identical sets may end up with different hash values
    frozenset is safe since at worst it just causes more collisions
    unfortunately, no collections.ABC class is available that helps
    distinguish ordered from unordered containers
    so we need to just list them out manually as needed

    Examples:
        d1 = {'a':[1,2], 2:{3:4}}
        print(hash(AutoHash(d1, cache=True, verbose=True)))

        d = AutoHash(dict(a=1, b=2, c=3, d=[4,5,6,7], e='a string of chars'),cache=True, verbose=True)
        print(hash(d))
    """
    type_info = collections.namedtuple(
        'type_info',
        'type transformation aggregator')

    ident = lambda x: x
    # order matters; first match is used to handle a datatype
    known_types = (
        # dict also handles defaultdict
        type_info(dict, lambda d: d.items(), frozenset),
        # no need to include set and frozenset, since they are fine with defaults
        type_info(collections.OrderedDict, ident, tuple),
        type_info(list, ident, tuple),
        type_info(tuple, ident, tuple),
        type_info(collections.deque, ident, tuple),
        type_info(collections.Iterable, ident, frozenset)  # other iterables
    )

    # hash_func can be set to replace the built-in hash function
    # cache can be turned on; if it is, cycles will be detected,
    # otherwise cycles in a data structure will cause failure
    def __init__(self, data, hash_func=hash, cache=False, verbose=False):
        self._data = data
        self.hash_func = hash_func
        self.verbose = verbose
        self.cache = cache
        # cache objects' hashes for performance and to deal with cycles
        if self.cache:
            self.seen = {}

    def hash_ex(self, o):
        # note: isinstance(o, Hashable) won't check inner types
        try:
            if self.verbose:
                print(type(o), reprlib.repr(o), self.hash_func(o), file=sys.stderr)
            return self.hash_func(o)
        except TypeError:
            pass

        # we let built-in hash decide if the hash value is worth caching
        # so we don't cache the built-in hash results
        if self.cache and id(o) in self.seen:
            return self.seen[id(o)][0]  # found in cache

        # check if o can be handled by decomposing it into components
        for typ, transformation, aggregator in HashAuto.known_types:
            if isinstance(o, typ):
                # another option is:
                # result = reduce(operator.xor, map(_hash_ex, handler(o)))
                # but collisions are more likely with xor than with frozenset
                # e.g. hash_ex([1,2,3,4])==0 with xor

                try:
                    # try to frozenset the actual components, it's faster
                    h = self.hash_func(aggregator(transformation(o)))
                except TypeError:
                    # components not hashable with built-in;
                    # apply our extended hash function to them
                    h = self.hash_func(aggregator(map(self.hash_ex, transformation(o))))
                if self.cache:
                    # storing the object too, otherwise memory location will be reused
                    self.seen[id(o)] = (h, o)
                if self.verbose:
                    print(type(o), reprlib.repr(o), h, file=sys.stderr)
                return h

        raise TypeError('Object {} of type {} not hashable'.format(repr(o), type(o)))

    def __hash__(self):
        return self.hash_ex(self._data)

    def __eq__(self, other):
        # short circuit to save time
        if self is other:
            return True

        # 1) type(self) a proper subclass of type(other) => self.__eq__ will be called first
        # 2) any other situation => lhs.__eq__ will be called first

        # case 1. one side is a subclass of the other, and AutoHash.__eq__ is not overridden in either
        # => the subclass instance's __eq__ is called first, and we should compare self._data and other._data
        # case 2. neither side is a subclass of the other; self is lhs
        # => we can't compare to another type; we should let the other side decide what to do, return NotImplemented
        # case 3. neither side is a subclass of the other; self is rhs
        # => we can't compare to another type, and the other side already tried and failed;
        # we should return False, but NotImplemented will have the same effect
        # any other case: we won't reach the __eq__ code in this class, no need to worry about it

        if isinstance(self, type(other)):  # identifies case 1
            return self._data == other._data
        else:  # identifies cases 2 and 3
            return NotImplemented


class hashdict(dict):
    def __hash__(self):
        return hash((frozenset(self.items())))


@dataclasses.dataclass
class Kill(BaseData):
    """Exit class"""
    signal: str = '9'
    cmd: str = datafield(default='sudo kill', init=False)
    command: str = None
    count_values: tuple = ('nmap', 'ping', 'ssh',)
    parameter: str = str()
    current_process: psutil.Process = None
    current_pid: int = datafield(default=int(), init=False)
    exception: sys.exc_info = datafield(default=None, init=False)
    exception_thread: str = datafield(default=str(), init=False)

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)
        self.cmd = f'{self.cmd} -{self.signal}'
        self.current_pid = os.getpid()
        self.current_process = psutil.Process(self.current_pid)

    @staticmethod
    def count(text: str = count_values[0]) -> int:
        out_cmd = cmd(Kill.count_cmd(text=text))
        return len(out_cmd.stdout) if out_cmd.stdout else 0

    @staticmethod
    async def count_async(text: str = count_values[0]) -> int:
        out_cmd = await aiocmd(Kill.count_cmd(text=text), utf8=True, lines=True)
        return len(out_cmd.stdout) if out_cmd.stdout else 0

    @staticmethod
    def count_cmd(text: str = count_values[0]) -> str:
        return f'pgrep -a -c {shlex.quote(text)}'

    def exit(self):
        function = inspect.currentframe().f_code.co_name
        self.m(f'{function=}', f'{self.current_pid=}')
        try:
            for child in self.current_process.children(recursive=True):
                child.kill()
                cmd(f'{self.cmd} {child.pid}')
                self.m('Killed current child', f'{function=}', f'{self.current_pid=}', f'{child.pid=}')
        except psutil.AccessDenied as exception:
            self.m('Kill current child', f'{function=}', f'{self.current_pid=}', f'{exception=}')
        except psutil.NoSuchProcess as exception:
            self.m('Killed current child sudo', f'{function=}', f'{self.current_pid=}', f'{exception=}')

    def stat(self, verbose: bool = True) -> dict:
        stat = {item: int() for item in ['children', ''] if item}
        stat['threads'] = self.current_process.threads()
        stat['memory_percent'] = self.current_process.memory_percent()
        stat['cpu_percent'] = self.current_process.cpu_percent()

        if verbose:
            self.d('Process', f'{stat=}')
        return stat

    def stop(self, command: str = None, parameter: str = None):
        function = inspect.currentframe().f_code.co_name
        self.command = command if command else self.command
        self.parameter = parameter if parameter else self.parameter
        text = f'{function=}', f'{self.current_pid=}', f'{self.command=}'
        if self.command:
            self.d(text)
        else:
            self.e(text)
            return
        attrs = ['pid', 'cmdline', 'username']
        for process in psutil.process_iter(attrs):
            if isinstance(process.info['cmdline'], list):
                if len(process.info['cmdline']) > 1:
                    if (self.command in process.info['cmdline'][0] or self.command in process.info['cmdline'][1]) \
                            and self.parameter in process.info['cmdline'][1:]:
                        self.m(f'{function=}', f'{process.info=}')
                        if self.parameter in process.info['cmdline']:
                            self.m(f'{function=}', f'{self.parameter=}', f'{process.info["cmdline"]=}')
                            try:
                                for p in process.children(recursive=True):
                                    p.kill()
                                    cmd(f'{self.cmd} {p.pid}')
                                    self.m('Killed child', f'{function=}', f'{p.pid=}')
                            except psutil.AccessDenied as exception:
                                self.m('Kill child', f'{function=}', f'{exception=}')
                            except psutil.NoSuchProcess as exception:
                                self.m(exception)
                            try:
                                if self.current_pid != process.pid:
                                    process.kill()
                                    self.m('Killed other', f'{function=}', f'{process.pid=}', f'{self.current_pid=}')
                            except psutil.AccessDenied as exception:
                                self.m('Kill other', f'{function=}', f'{process.pid=}', f'{self.current_pid=}',
                                       f'{exception=}')
                                cmd(f'{self.cmd} {process.pid}')
                                self.m('Killed other sudo', f'{function=}', f'{process.pid=}',
                                       f'{self.current_pid=}')
                            except psutil.NoSuchProcess as exception:
                                self.m(exception)


@dataclass
class Machine:
    """Server OS and Platform Class."""
    fqdn: str = socket.getfqdn()
    hostname: str = os.uname().nodename.split('.')[0]  # pro, repo
    machine: str = os.uname().machine  # x86_64
    nodename: str = os.uname().nodename  # pro, repo.nferx.com
    processor: str = platform.processor()  # amdk6,


# @dataclass
class Log(verboselogs.VerboseLogger):
    name: str = None
    level: int = log_defaults.log_level
    all: ClassVar[dict] = dict(package={}, packages={}, handlers=set(), root=set())
    colors: ClassVar[tuple] = ('white', 'cyan', 'green', 'yellow', 'purple', 'blue', 'red', 'fg_bold_red',)
    file: ClassVar[int] = log_defaults.log_level_file
    Format: ClassVar[Any] = NamedTuple('Format', fh=Any, rh=Any)
    formats: ClassVar[Any] = Format(
        dict(short='%(thin)s%(white)s[ %(log_color)s%(levelname)-8s%(white)s ] [ %(log_color)s%(name)-30s%(white)s ] '
                   '%(white)s %(log_color)s%(message)s %(white)s%(reset)s',
             large_func='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%('
                        'white)s] '
                        '%(white)s[%(log_color)s%(name)s%(white)s] '
                        '%(white)s[%(log_color)s%(funcName)s%(white)s:%(log_color)s%(lineno)d%(white)s] '
                        '%(log_color)s%(message)s%(white)s%(reset)s',
             large='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%('
                   'white)s] '
                   '%(white)s[%(log_color)s%(name)s%(white)s] '
                   '%(log_color)s%(message)s%(white)s%(reset)s',
             large_thread='%(thin)s%(white)s[%(log_color)s%(asctime)s%(white)s] %(white)s[%(log_color)s%(levelname)s%('
                          'white)s] '
                          '%(white)s[%(log_color)s%(name)s%(white)s] '
                          '%(white)s[%(log_color)s%(funcName)s%(white)s:%(log_color)s%(lineno)d%(white)s] '
                          '%(white)s[%(log_color)s%(threadName)s%(white)s] '
                          '%(log_color)s%(message)s%(white)s%(reset)s',
             date='%(thin)s%(white)s[%(log_color)s%(asctime)s%(reset)s%(white)s] '
                  '%(white)s[%(log_color)s%(levelname)s%(white)s] %(white)s[%(log_color)s%(name)s%(white)s] '
                  '%(white)s[%(log_color)s%(filename)s%(reset)s:%(log_color)s%(lineno)d%(reset)s - '
                  '%(log_color)s%(module)s%(reset)s - %(log_color)s%(funcName)s%(reset)s%(white)s] '
                  '%(white)s %(log_color)s%(message)s %(white)s%(reset)s'),
        dict(short='%(message)s',
             large='[%(name)s| %(module)s | %(funcName)s %(lineno)s] - %(message)s',
             large_thread='[%(name)s| %(module)s| %(threadName)s | %(funcName)s %(lineno)s] - %(message)s'))
    format: ClassVar[dict] = Format('large', 'large')
    manager: ClassVar[Optional[Union[Logger, Log]]] = None
    mode: ClassVar[str] = 'a'
    package: ClassVar[str] = str()
    packages: ClassVar[int] = log_defaults.log_level_packages
    propagate: ClassVar[bool] = True
    rotate: ClassVar[dict] = dict(count=5, interval=1, when='d')
    tracebacks: ClassVar[bool] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def child(self, name: str = None):
        """
        Child logger with module name.

        Returns:
            child logger
        """
        if not name:
            c = Caller()
            m = c.modulename
            module = f'{m}.' if m and m != '__main__' or m != '__init__' or '<' not in m else str()
            name = f'{module}{c.qual or c.function}'
        _l = self.getChild(name)
        _l.level_set()
        return _l

    @classmethod
    def get(cls, name: Any = None, path: Any = None, level: Union[str, int] = level, file: Union[str, int] = file,
            packages: Union[str, int] = packages, installed: bool = True, markup: bool = True) -> Log:
        """
        Sets Logger.

        Args:
            name: name
            path: path
            file: file
            level: stream
            packages: packages
            installed: installed
            markup: markup

        Returns:
            Union[Log, Logger]:
        """
        cls.name = name if name else Caller(setup=True).package
        cls.file = file
        cls.level = level
        cls.packages = packages
        logging.setLoggerClass(Log)
        l = logging.getLogger(name)
        if l.hasHandlers():
            l.handlers.clear()
        l.propagate = cls.propagate
        l.package = l.name
        if root := (getattr(l, 'parent', None)):
            root.setLevel(cls._get_level(cls.packages))
        l.setLevel(cls._get_min(cls.file, cls.level))

        if file:
            if installed or cls.mode == 'a':
                fh = logging.handlers.TimedRotatingFileHandler(
                    str(path), when=cls.rotate['when'], interval=cls.rotate['interval'],
                    backupCount=cls.rotate['count'])
            else:
                fh = logging.FileHandler(str(path), cls.mode)
            fh_formatter = colorlog.ColoredFormatter(fmt=cls.formats.fh[cls.format.fh],
                                                     log_colors=dict(zip(LogLevel.attrs(), cls.colors)))
            fh.setLevel(cls.file)
            fh.setFormatter(fh_formatter)
            l.addHandler(fh)

        rh_formatter = logging.Formatter(fmt=cls.formats.rh[cls.format.rh])
        rh = rich.logging.RichHandler(rich_tracebacks=cls.tracebacks, markup=markup)
        rh.setLevel(cls.level)
        rh.setFormatter(rh_formatter)
        l.addHandler(rh)

        cls.manager = getattr(l, 'manager', None)
        cls.level_set('packages', cls._get_level(cls.packages))
        return cast(cls, l)

    @classmethod
    def _get_level(cls, level: Union[str, int]) -> int:
        """
        Get Level Value

        Args:
            level: level

        Returns:
            int:
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        return level

    @classmethod
    def _get_min(cls, x: Union[str, int], y: Union[str, int]) -> int:
        """
        Get Min Value

        Args:
            x: x
            y: y

        Returns:
            int:
        """
        return min(cls._get_level(x), cls._get_level(y))

    @classmethod
    def level_set(cls, attr: str = None, value: Union[str, int] = None):
        """
        Helper to sets Handler or Logger Level for caller setter.

        Args:
            attr: handler or logger attribute.
            value: level value to set.
        """
        if attr is not None:
            value = getattr(cls, attr) if value is None else cls._get_level(value)
            setattr(cls, attr, value)

        cls._level_set_logger('root', cls.packages)
        if (loggerDict := getattr(cls.manager, 'loggerDict', None)) is not None:
            for name in loggerDict:
                key = 'package' if name.startswith(cls.package if cls.package else name) else 'packages'
                level = cls._get_min(cls.file, cls.level) if key == 'package' else cls.packages
                cls._level_set_logger(name, level, key)

    @classmethod
    def _level_set_handler(cls, l):
        """
        Sets Handler Level.

        Args:
            l: logger
        """
        if l.hasHandlers():
            for handler in l.handlers:
                if isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        or isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.file))
                if isinstance(handler, logging.StreamHandler) \
                        and not isinstance(handler, logging.handlers.TimedRotatingFileHandler) \
                        and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(cls._get_level(cls.level))
                key = l.name if l.name == 'root' else 'handlers'
                cls.all[key].add(handler)

    @classmethod
    def _level_set_logger(cls, name: str, level: Union[str, int], key: str = None):
        """
        Sets Logger Level.

        Args:
            name: logger name.
            level: level value.
            key: `Log.all` key.
        """
        l = logging.getLogger(name)
        l.setLevel(cls._get_level(level))
        if key is None:
            cls.all[name].add(l)
        else:
            cls.all[key][name] = l
        if name == cls.package:
            cls._level_set_handler(l)

    @classmethod
    def prepare_msg(cls, *args, **kwargs) -> str:
        def _caller(c: Caller, l: bool = False) -> str:
            p = str() if l else f'Called: '
            return f'{p}{c.file.parent.name}/{c.module} | {c.function}({c.args if params and not l else str()}): ' \
                   f'{c.lineno}'

        params, kwargs = pop_default(kwargs, 'params')
        args = list(args)
        called = None
        for arg in args:
            if isinstance(arg, Caller):
                called = arg
                args.remove(args)
                break
        if not called:
            for key, value in kwargs.items():
                if isinstance(value, Caller):
                    called = value
                    kwargs.pop(key)
                    break
        task = str()
        call = str()
        if called:
            task = f'Task: {called.task}' if called.task else str()
            call = _caller(called)

        msg = {_caller(Caller(), l=True), task, call,
               *[f'{key.upper()}: {value}' for key, value in kwargs.items()], *{repr(item) for item in args}}
        if str() in msg:
            msg.remove(str())
        return ' '.join([f'[{item}]' for item in msg])
        # try:
        #     add = caller_msg(Path.caller())
        #     # frame_2 = inspect.stack()[2]
        #     # frame_3 = inspect.stack()[3]
        #     # frame = frame_2
        #     # if 'asyncio' in frame_2.filename:
        #     #     frame = frame_3
        #     # if 'asyncio' in frame_3.filename:
        #     #     frame = frame_2
        #     # frame_path = Path(frame.filename)
        #     # add = f'[{frame_path.parent.name}/{frame_path.name} | {frame.function}: {frame.lineno}]'
        # except IndexError:
        #     add = str()
        # rv = ', '.join(str(item) for item in (*args, **kwargs,))
        # rv = add + rv if add else rv
        # return rv

    def log(self, level, *args, **kwargs):
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    async def loga(self, level, *args, **kwargs):
        if not isinstance(level, int):
            if logging.raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            await to_thread(self._log, level, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def m(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SPAM):
            self._log(verboselogs.SPAM, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def ma(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SPAM):
            await to_thread(self._log, verboselogs.SPAM, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def d(self, *args, **kwargs):  # Start, End
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def da(self, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            await to_thread(self._log, logging.DEBUG, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def v(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.VERBOSE):
            self._log(verboselogs.VERBOSE, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def va(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.VERBOSE):
            await to_thread(self._log, verboselogs.VERBOSE, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def i(self, *args, **kwargs):  # Released
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def ia(self, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            await to_thread(self._log, logging.INFO, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def n(self, *args, **kwargs):  # Acquired
        if self.isEnabledFor(verboselogs.NOTICE):
            self._log(verboselogs.NOTICE, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def na(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.NOTICE):
            await to_thread(self._log, verboselogs.NOTICE, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def w(self, *args, **kwargs):  # Waiting
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def wa(self, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            await to_thread(self._log, logging.WARNING, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def s(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SUCCESS):
            self._log(verboselogs.SUCCESS, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def sa(self, *args, **kwargs):
        if self.isEnabledFor(verboselogs.SUCCESS):
            await to_thread(self._log, verboselogs.SUCCESS, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def e(self, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def ea(self, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            await to_thread(self._log, logging.ERROR, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def c(self, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, self.prepare_msg(*args, **kwargs), (), **kwargs)

    async def ca(self, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            await to_thread(self._log, logging.CRITICAL, self.prepare_msg(*args, **kwargs), tuple(), **dict())

    def x(self, *args, exc_info=True, **kwargs):
        self.error(self.prepare_msg(False, *args), (), exc_info=exc_info, **kwargs)

    async def xa(self, *args, exc_info=True, **kwargs):
        await to_thread(self.error, self.prepare_msg(*args, **kwargs), tuple(), exc_info=exc_info, **dict())


@dataclass
class Obj:
    data: Any = None
    depth: Optional[int] = obj_defaults.depth
    ignore: bool = obj_defaults.ignore
    swith: str = obj_defaults.swith

    util = jsonpickle.util

    __ignore_attr__ = ['util', ]  # Exclude instance attribute.
    __ignore_copy__ = []  # True or class for repr instead of nested asdict and deepcopy.
    __ignore_kwarg__ = []  # Exclude attr from kwargs.

    def __post_init__(self):
        self.__ignore_str__ = [pathlib.Path, ObjectId]  # str value
        self.__ignore_copy__ = [environs.Env, git.Remote, git.SymbolicReference, git.config.GitConfigParser,
                                threading._CRLock]  # no deep copy

        if self.dict:
            self.data = self.data.copy()

    def annotation(self, attr: str) -> Any:
        annotation = None
        value = None
        if self.dataclass or self.dataclass_instance:
            for field in dataclasses.fields(self.getcls):
                if field.name == attr:
                    if field.type:
                        value = field.type
        if value or (annotation := vars(self.getcls).get('__annotations__', dict())):
            if annotation and hasattr(annotation, 'get'):
                value = annotation.get(attr)
            if value:
                value = eval(value) if isinstance(value, str) else value
                if hasattr(value, '__args__'):
                    return value.__args__
                return value,

    def asdict(self, count: int = 1, defaults: bool = False) -> Any:
        """
        Dict excluding.

        Returns:
            dict:
        """
        convert = self.depth is None or self.depth > 1
        if self.enuminstance:
            self.data = {self.data.name: self.data.value}
        elif self.namedtuple:
            self.data = self.data._asdict().copy()
        elif isinstance(self.data, self.getmroattr('__ignore_str__')) and convert:
            self.data = str(self.data)
        elif isinstance(self.data, asyncio.Semaphore) and convert:
            self.data = dict(locked=self.data.locked(), value=self.data._value)
        elif isinstance(self.data, git.SymbolicReference) and convert:
            self.data = dict(repo=self.data.repo, path=self.data.path)
        elif isinstance(self.data, git.Remote) and convert:
            self.data = dict(repo=self.data.repo, name=self.data.name)
        elif isinstance(self.data, environs.Env) and convert:
            self.data = self.data.dump()
        elif isinstance(self.data, logging.Logger) and convert:
            self.data = dict(name=self.data.name, level=self.data.level)
        elif self.enumcls:
            self.data = {key: value._value_ for key, value in self.getcls.__members__.items()}
        elif self.chainmap and convert:
            self.data.rv = ChainMapRV.FIRST
            self.data = dict(self.data).copy()
        elif any([self.dataclass, self.dataclass_instance, self.dict_cls, self.dict_instance, self.slots_cls,
                  self.slots_instance]):
            self.data = self.defaults if defaults else self.defaults | self.vars
        elif self.mutablemapping and convert:
            self.data = dict(self.data).copy()
        if self.mlst:
            rv = dict() if (mm := isinstance(self.data, MutableMapping)) else list()
            for key in self.data:
                value = self.data.get(key) if mm else key
                if value:
                    if (inc := self.include(key, self.data if mm else None)) is None:
                        continue
                    else:
                        value = inc[1]
                        if self.depth is None or count < self.depth:
                            value = self.new(value).asdict(count=count + 1, defaults=defaults)
                rv.update({key: value}) if mm else rv.append(value)
            return rv if mm else type(self.data)(rv)
        if (inc := self.include(self.data)) is not None:
            if self.getsetdescriptor() or self.coro or isinstance(inc[1], (*self.getmroattr('__ignore_copy__'),)) \
                    or (self.depth is not None and self.depth > 1):
                return inc[1]
            try:
                return deepcopy(inc[1])
            except TypeError as exception:
                if "cannot pickle '_thread.lock' object" == str(exception):
                    return inc[1]
        return self.data

    @property
    def attrs(self) -> list:
        """
        Attrs including properties if not self.ignore.

        Excludes:
            __ignore_attr__
            __ignore_kwarg__ if not self.ignore.

        Returns:
            list:
        """
        i = self.clsinspect()
        return sorted([attr for attr in {*self.attrs_cls, *i[AttributeKind.MEMBER],
                                         *(vars(self.data) if self.dataclass_instance or self.dict_instance else []),
                                         *(i[AttributeKind.PROPERTY] if not self.ignore else [])}
                       if self.attrs_include(attr, i[AttributeKind.CALLABLE])])

    @property
    def attrs_cls(self) -> list:
        attrs = {item for item in self.dir_cls if
                 self.attrs_include(item) and item in self.clsinspect(AttributeKind.DATA) and item}
        if self.dataclass or self.dataclass_instance:
            _ = {attrs.add(item.name) for item in dataclasses.fields(self.getcls) if self.attrs_include(item.name)}
        return sorted(list(attrs))

    def attrs_include(self, name: str, exclude: Seq = tuple()) -> bool:
        ignore = {*self.getmroattr(), *(self.getmroattr('__ignore_kwarg__') if self.ignore else set()), *exclude,
                  *self.initvars_attrs}
        return not any([Obj(name).start, name in ignore, f'_{self.getcls.__name__}' in name])

    @property
    @runwarning
    def awaitable(self) -> bool:
        return inspect.isawaitable(self.data)

    @property
    def bytes(self) -> bool:
        return isinstance(self.data, bytes)

    @property
    def callable(self) -> bool:
        return isinstance(self.data, Callable)

    @property
    def chainmap(self) -> bool:
        return isinstance(self.data, ChainMap)

    @property
    def classmethods(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: isinstance(x, classmethod)):
            rv, _ = zip(*rv)
        return rv

    def classvar(self, attr: str) -> bool:
        return self.origin(attr) is ClassVar

    @property
    def cls(self) -> bool:
        return inspect.isclass(self.data)

    def clsinspect(self, kind: Optional[AttributeKind] = None, cls: Any = None, exclude: bool = True,
                   rv_kind: bool = True) -> Optional[Union[dict[AttributeKind, list], dict[str, Attribute], list]]:
        """
        Class attrs info.

        Args:
            kind: return attrs kind list instead of dict with all.
            cls: cls.
            exclude: exclude.
            rv_kind: dict with by AttributeKind keys.

        Returns:
            Optional[Union[dict[str, Attribute], list]]:
        """

        def _include(name):
            if not exclude:
                return True
            return not all([obj.memberdescriptor(name), obj.getsetdescriptor(name), self.new(name).start, name in excl])

        obj = self if cls is None else self.new(cls)
        excl = self.getmroattr()
        if kind is AttributeKind.MEMBER:
            rv = sorted(self.getmroattr('__slots__'))
        elif kind is AttributeKind.GETSET:
            rv = sorted([attr.name for attr in inspect.classify_class_attrs(obj.getcls)
                         if obj.getsetdescriptor(attr.name)])
        elif kind:
            rv = sorted([item.name for item in inspect.classify_class_attrs(obj.getcls)
                         if item.kind == kind.value and _include(item.name)])
        elif rv_kind:
            rv = {kind: [attr.name for attr in inspect.classify_class_attrs(obj.getcls)
                         if attr.kind == kind.value and _include(attr.name)] for kind in AttributeKind}
            rv[AttributeKind.CALLABLE] = rv[AttributeKind.CLASS] + rv[AttributeKind.METHOD] + rv[AttributeKind.STATIC]
            rv[AttributeKind.MEMBER] = sorted([attr for attr in self.getmroattr('__slots__') if attr not in excl])
            rv[AttributeKind.GETSET] = sorted([attr.name for attr in inspect.classify_class_attrs(obj.getcls)
                                               if obj.getsetdescriptor(attr.name) and not self.new(attr.name).start
                                               and attr.name not in excl])
        else:
            rv = {item.name: Attribute(item.defining_class, AttributeKind[iter_split(item.kind)[0].upper()],
                                       item.object) for item in inspect.classify_class_attrs(obj.getcls)}
        return rv

    @property
    def clsmethod(self) -> bool:
        return isinstance(self.data, classmethod)

    @property
    def clsproperty(self) -> bool:
        return isinstance(self.data, property)

    @property
    @runwarning
    def coro(self) -> bool:
        return any([self.awaitable, self.coroutinefunction,
                    inspect.isasyncgenfunction(self.data), inspect.isasyncgen(self.data)])

    @property
    def coroscls(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: self.is_coro(x)):
            rv, _ = zip(*rv)
        return rv

    @property
    @runwarning
    def coroutine(self) -> bool:
        return asyncio.coroutines.iscoroutine(self.data)

    @property
    @runwarning
    def coroutinefunction(self) -> bool:
        return inspect.iscoroutinefunction(self.data)

    @property
    def dataclass(self) -> bool:
        return self.cls and dataclasses.is_dataclass(self.data)

    @property
    def dataclass_instance(self) -> bool:
        return not self.cls and hasattr(type(self.data), dataclasses._FIELDS)

    @property
    def defaults(self) -> dict:
        """Class defaults."""
        rv = dict()
        rv_data = dict()
        attrs = self.attrs_cls
        if self.dataclass or self.dataclass_instance:
            rv_data = {f.name: f.default if isinstance(
                f.default, dataclasses._MISSING_TYPE) and isinstance(
                f.default_factory, dataclasses._MISSING_TYPE) else f.default if isinstance(
                f.default_factory, dataclasses._MISSING_TYPE) else f.default_factory() for f in
                       dataclasses.fields(self.getcls) if f.name in attrs}
        if self.dict_cls or self.dict_instance or self.slots_cls or self.slots_instance:
            rv = {key: inc[1] for key in attrs if (inc := self.include(key, self.getcls)) is not None}
        return rv | rv_data

    @property
    def dict_cls(self) -> bool:
        return self.cls and hasattr(self.data, '__dict__') and not self.namedtuple

    @property
    def dict_instance(self) -> bool:
        return not self.cls and hasattr(self.data, '__dict__') and not self.namedtuple

    @property
    def dir(self) -> list:
        return list({*(self.dir_cls + self.dir_instance)})

    @property
    def dir_cls(self) -> list:
        return dir(self.getcls)

    @property
    def dir_instance(self) -> list:
        return dir(self.data)

    @property
    def dlst(self) -> bool:
        return any([isinstance(self.data, item) for item in [dict, list, set, tuple]])

    @property
    def end(self) -> bool:
        return self.str and self.data.endswith(self.swith)

    @property
    def enumcls(self) -> bool:
        return isinstance(self.data, enum.EnumMeta) \
               and self.cls and hasattr(self.data, '__members__')

    @property
    def enuminstance(self) -> bool:
        classes = [enum.Enum, enum.IntEnum, enum.IntFlag, enum.Flag]
        return not self.cls and any([issubclass(self.getcls, cls) for cls in classes]) and any(
            [isinstance(self.data, cls) for cls in classes]) and hasattr(
            self.data, 'name') and hasattr(self.data, 'value')

    @property
    def enumdictcls(self) -> bool:
        return self.enumcls \
               and issubclass(AttributeKind, Enum) \
               and hasattr(self.data, 'asdict')

    @property
    def enumdictinstance(self) -> bool:
        return not self.cls \
               and self.enuminstance \
               and issubclass(self.getcls, Enum) \
               and isinstance(self.data, Enum)

    def exclude(self, data: Any, key: bool = True) -> bool:
        obj = self.new(data)
        call = (environs.Env,)
        return any([obj.getmodule == typing, obj.getmodule == _abc, obj.module,
                    False if type(data) in call else obj.callable, obj.cls, obj.start if key else False])

    @property
    def float(self) -> bool:
        return isinstance(self.data, float)

    @property
    def generator(self) -> bool:
        return isinstance(self.data, Generator)

    def get(self, name: str, default: Any = None) -> Any:
        return self.data.get(name, default) if self.mutablemapping else getattr(self.data, name, default)

    @property
    def getcls(self) -> Any:
        return self.data if self.cls else type(self.data)

    def getclsattr(self, name: str, default: Any = None) -> Any:
        return getattr(self.getcls, name, default)

    @property
    def getmodule(self) -> Any:
        return inspect.getmodule(self.data)

    @property
    def getmodulename(self) -> Any:
        return mod.__name__ if (mod := self.getmodule) else str()

    def getmroattr(self, name: str = '__ignore_attr__') -> tuple:
        return tuple({attr for item in [*self.mro, Obj(), self.data] for attr in getattr(item, name, list())})

    def getsetdescriptor(self, name: str = None) -> bool:
        return inspect.isgetsetdescriptor(self.getclsattr(name) if name else self.data)

    @runwarning
    def include(self, key: Any = None, data: Any = None) -> Optional[tuple]:
        obj = Obj(data)
        if (not obj.mutablemapping and obj.memberdescriptor(key) and key not in obj.getmroattr()) \
                or not self.exclude(key):
            if not obj.none:
                if (value := obj.get(key)) and self.exclude(value, key=False):
                    return None
                return key, value
            return key, key
        return None

    def initvar(self, attr: str) -> Optional[bool]:
        if value := self.annotation(attr):
            return isinstance(value[0], InitVar)

    @property
    def initvars_attrs(self) -> list:
        rv = list()
        if self.dataclass or self.dataclass_instance:
            with suppress(KeyError):
                for cls in self.mro:
                    vs = dict(vars(cls))
                    for key, value in vs.get('__annotations__', dict()).items():
                        value = eval(value) if isinstance(value, str) else value
                        if isinstance(value, InitVar):
                            rv.append(key)
        return rv

    @property
    def initvars(self) -> dict:
        return getattr(self.data, '__init_vars__', dict())

    @property
    def inspect(self) -> defaultdict:
        data = self.data.copy() if self.mutablemapping else dict()
        return default_dict(
            init={key: Obj(value).inspect for key, value in data.items() if self.include(key, data)}
            if self.mutablemapping else
            {i.name: dict(annotation=self.annotation(i.name), callable=callable(i.object),
                          classvar=self.classvar(i.name), cls=i.defining_class, coro=Obj.is_coro(i.object),
                          getset=inspect.isgetsetdescriptor(i.object), initvar=self.initvar(i.name),
                          kind=AttributeKind[iter_split(i.kind)[0].upper()],
                          member=inspect.ismemberdescriptor(i.object),
                          qual=getattr(i.object, '__qualname__', i.name), routine=inspect.isroutine(i.object),
                          type=type(i.object), value=i.object) for i in inspect.classify_class_attrs(self.getcls)
             if not self.swith or not self.start})

    def instance(self, cls: Union[tuple, Any]) -> bool:
        return isinstance(self.data, cls)

    @property
    def int(self) -> bool:
        return isinstance(self.data, int)

    def isattr(self, name: str) -> bool:
        return name in self.dir

    @classmethod
    def is_coro(cls, obj: Any) -> bool:
        return cls(obj).coro

    @property
    def iterable(self) -> bool:
        return isinstance(self.data, Iterable)

    @property
    def keys(self) -> list:
        """
        Keys from kwargs to init class (not InitVars), exclude __ignore_kwarg__ and properties.

        Returns:
            list:
        """
        return sorted(list(self.kwargs.keys()))

    @property
    def kwargs(self) -> dict:
        """
        Kwargs to init class with python objects no recursive, exclude __ignore_kwarg__ and properties.

        Includes InitVars.

        Example: Mongo binary.

        Returns:
            dict:
        """
        ignore = self.ignore
        self.ignore = True
        rv = {key: self.get(key) for key in self.attrs_cls} | \
             {key: value for key, value in self.initvars.items()
              if key not in {*self.getmroattr(), *self.getmroattr('__ignore_kwarg__')}}
        self.ignore = ignore
        return rv

    @property
    def kwargs_dict(self) -> dict:
        """
        Kwargs recursive to init class with python objects as dict, asdict excluding __ignore_kwarg__ and properties.

        Example: Mongo asdict.

        Returns:
            dict:
        """
        ignore = self.ignore
        self.ignore = True
        rv = self.asdict()
        self.ignore = ignore
        return rv

    @property
    def list(self) -> bool:
        return isinstance(self.data, list)

    @property
    def lst(self) -> bool:
        return any([isinstance(self.data, item) for item in [list, set, tuple]])

    @property
    def memberdescriptors(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: inspect.ismemberdescriptor(x)):
            rv, _ = zip(*rv)
        return rv

    @property
    def methods(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: inspect.ismethod(x)):
            rv, _ = zip(*rv)
        return rv

    @property
    def methoddescriptors(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: inspect.ismethoddescriptor(x)):
            rv, _ = zip(*rv)
        return rv

    @property
    def mlst(self) -> bool:
        return any([isinstance(self.data, item) for item in [MutableMapping, list, set, tuple]])

    def memberdescriptor(self, name: str = None) -> bool:
        return name in self.getmroattr('__slots__') if name else inspect.ismemberdescriptor(self.data)

    @property
    def module(self) -> bool:
        return inspect.ismodule(self.data)

    # noinspection PyTypeChecker
    @property
    def mro(self) -> tuple[Type, ...]:
        return inspect.getmro(self.getcls)
        # return self.data.__mro__ if self.cls and hasattr(self.data, '__mro__') else self.getcls.__mro__ \
        #     if hasattr(self.getcls, '__mro__') else tuple()

    @property
    def mutablemapping(self) -> bool:
        return isinstance(self.data, MutableMapping)

    @property
    def namedtuple(self) -> bool:
        return not self.cls and self.tuple and hasattr(self.data, '_asdict')

    def new(self, data: Any = None, /, **kwargs) -> Obj:
        return Obj(**{field.name: getattr(self, field.name) for field in dataclasses.fields(self)} | dict(
            data=self.data if data is None else data) | kwargs)

    @property
    def none(self) -> bool:
        return self.data is None

    @property
    def ordereddict(self) -> bool:
        return isinstance(self.data, OrderedDict)

    def origin(self, attr: str) -> Any:
        value = None
        if hasattr(self.getcls, attr) and (value := getattr(self.getcls, attr)):
            return value.__origin__ if hasattr(value, '__origin__') else None

    @property
    def properties(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: isinstance(x, property)):
            rv, _ = zip(*rv)
        return rv

    @property
    def public(self) -> dict:
        self.swith = '_'
        return self.asdict()

    def routine(self, name: str = None) -> bool:
        return inspect.isroutine(self.getclsattr(name) if name else self.data)

    @property
    def seq(self):
        return isinstance(self.data, SeqArgs) and not hasattr(self, 'data')

    @property
    def set(self) -> bool:
        return isinstance(self.data, set)

    @property
    def slots_cls(self) -> bool:
        return self.cls and hasattr(self.data, '__slots__') and not self.namedtuple

    @property
    def slots_instance(self) -> bool:
        return not self.cls and hasattr(self.data, '__slots__') and not self.namedtuple

    @property
    def start(self) -> bool:
        return self.str and (self.data.startswith(self.swith) if self.swith else False)

    @property
    def staticmethods(self) -> list:
        if rv := inspect.getmembers(self.getcls, lambda x: isinstance(x, staticmethod)):
            rv, _ = zip(*rv)
        return rv

    @property
    def str(self) -> bool:
        return isinstance(self.data, str)

    @property
    def to_iterable(self) -> Iterable:
        if self.str:
            return self.data.split() if ' ' in self.data else [self.data]
        elif not self.iterable:
            return [self.data]
        return self.data

    def yield_if(self, condition: Callable = lambda x: True if x else False, to_iterable: bool = True) -> Generator:
        data = self.to_iterable if to_iterable else self.data
        for item in data:
            if condition(item):
                yield item

    def map_sync(self, func: Callable, /, *args, condition: Callable = lambda x: True if x else False,
                 to_iterable: bool = True, **kwargs) -> list:
        return [func(item, *args, **kwargs) for item in self.yield_if(condition=condition, to_iterable=to_iterable)]

    def to_json(self, regenerate: bool = True, indent: bool = 4, keys: bool = True, max_depth: int = -1) -> JSONEncoder:
        return jsonpickle.encode(self.data, unpicklable=regenerate, indent=indent, keys=keys, max_depth=max_depth)

    def to_obj(self, keys: bool = True) -> Any:
        return jsonpickle.decode(self.data, keys=keys)

    @property
    def tuple(self) -> bool:
        return isinstance(self.data, tuple)

    @property
    def values(self) -> list:
        """
        Init python objects kwargs values no properties and not __ignore_kwarg__.

        Returns:
            list:
        """
        return list(self.kwargs.values())

    @property
    def values_dict(self) -> list:
        """
        Init python objects as dict kwargs values no properties and not __ignore_kwarg__.

        Returns:
            list:
        """
        return list(self.kwargs_dict.values())

    @property
    def vars(self) -> dict:
        attrs = self.attrs
        return {key: inc[1] for key in attrs if (inc := self.include(key, self.data)) is not None}

    @property
    def defaultdict(self) -> bool:
        return isinstance(self.data, defaultdict)

    @property
    def dict(self) -> bool:
        return isinstance(self.data, dict)

    @property
    def bool(self) -> bool:
        if self.int:
            return isinstance(self.data, bool)
        return False


class Path(pathlib.Path, pathlib.PurePosixPath):
    """
    Path Helper Class.

    Examples:
        # >>> from bapy import System
        # >>> os.chdir('/usr/local')
        # >>> path = Path('/usr/local').parent
        # >>> path.text, path.str, path.resolved, path.cwd()
        # ('/usr', '/usr', Path('/usr'), Path('/usr/local'))
        # >>> path.cd(System.sys_site)  # cd to post_init path
        # Path('/usr/local/lib/python3.8/site-packages')
        # >>> path.cd()  # cd to previous
        # Path('/usr/local')
        # >>> path_new = path.cd(System.sys_site)
        # >>> path_new
        # Path('/usr/local/lib/python3.8/site-packages')
        # >>> path_previous = path_new.cd()
        # >>> path_previous
        # Path('/usr/local')
        # >>> path_mkdir_add_test = Path('/tmp').mkdir_add('path_mkdir_add_test')
        # >>> assert '/tmp/path_mkdir_add_test' in path_mkdir_add_test.text
        # >>> path_touch_add_test = Path('/tmp').touch_add('path_touch_add_test')
        # >>> assert '/tmp/path_touch_add_test' in path_touch_add_test.text
        # >>> for glob_test in Path('/tmp').rglob('path*'):
        # ...     glob_test
        # Path('/tmp/path_mkdir_add_test')
        # Path('/tmp/path_touch_add_test')
        # >>> path_mkdir_add_test.rmdir()
        # >>> os.remove(path_touch_add_test.text)
        # >>>
        # >>> from bapy import User
        # >>> Path('/tmp/templates').rm()
        # >>> test = Path('/tmp').mkdir_add('templates') / 'test.templates'
        # >>> test.write_text('Defaults: {{ User.name }} !logfile, !syslog') #doctest: +ELLIPSIS
        # 43
        # >>> Path('/tmp').templates['test'].dump(dest='/tmp/sudoers')
        # >>> Path('/tmp/sudoers').read_text() #doctest: +ELLIPSIS
        # 'Defaults:... !logfile, !syslog'
        # >>> Path('/tmp/templates').rm()
        # >>> Path('/tmp/sudoers').rm()
    """
    cd_: Optional[Path] = None

    def append_text(self, data, encoding=None, errors=None):
        """
        Open the file in text mode, append to it, and close the file.
        """
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' %
                            data.__class__.__name__)
        with self.open(mode='a', encoding=encoding, errors=errors) as f:
            return f.write(data)

    def cd(self, p: Any = '-') -> Path:
        """
        Change working dir, returns post_init Path and stores previous.

        Args:
            p: path

        Returns:
            Path:
        """
        if self.cd_ is None:
            self.cd_ = self.cwd()
        p = self.cd_ if p == '-' else p
        cd_ = self.cwd()
        os.chdir(Path(str(p)).text)
        p = self.cwd()
        p.cd_ = cd_
        return p

    def chmod(self, mode):
        super().chmod(mode)
        return self

    @property
    def description(self) -> str:
        try:
            return self.readme.splitlines()[0].strip('# ')
        except IndexError:
            return str()

    @property
    def endseparator(self) -> str:
        """
        Add trailing separator at the end of path if does not exist.

        Returns:
            Str: path with separator at the end.
        """
        return self.text + os.sep

    def find_up(self, file: PathIs = PathIs.FILE, name: Union[str, PathSuffix] = PathSuffix.ENV,
                previous: bool = False) -> Optional[Union[tuple[Optional[Path], Optional[Path]], Path]]:
        """
        Find file or dir up.

        Args:
            file: file.
            name: name.
            previous: if found return also previous path.

        Returns:
            Optional[Union[tuple[Optional[Path], Optional[Path]]], Path]:
        """
        name = name if isinstance(name, str) else name.lowerdot
        start = self if self.is_dir() else self.parent
        before = self
        while True:
            find = start / name
            if getattr(find, file.value)():
                if previous:
                    return find, before
                return find
            before = start
            start = start.parent
            if start == Path('/'):
                if previous:
                    return None, None
                return

    def fd(self, *args, **kwargs):
        return os.open(self.text, *args, **kwargs)

    @staticmethod
    def j2(src: Path = None, dest: Path = None, variables: dict = None, stream: bool = True):
        called = Caller(glob=True, loc=True)
        variables = variables if variables else called.globs | called.locs

        if stream:
            jinja2.Template(src.read_text(), autoescape=True).stream(variables).dump(Path(dest).text)
        else:
            jinja2.Template(src.read_text(), autoescape=True).render(variables)

    def mkdir_add(self, name, mode=0o700, parents=True, exist_ok=True) -> Path:
        """
        Add directory, make directory and return post_init Path.

        Args:
            name: name
            mode: mode
            parents: parents
            exist_ok: exist_ok

        Returns:
            Path:
        """
        if not (p := (self / name).resolved).is_dir():
            p.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
        return p

    @property
    def pwd(self) -> Path:
        return self.cwd().resolved

    @property
    def readme(self) -> str:
        if (self / PathSuffix.GIT.lowerdot).is_dir():
            readme = self / 'README.md'
            if not readme.is_file():
                readme.write_text(f'# {self.name.capitalize()}')
            return readme.read_text()
        return str()

    @property
    def requirements(self) -> dict:
        try:  # for pip >= 10
            # noinspection PyCompatibility
            from pip._internal.req import parse_requirements
        except ImportError:  # for pip <= 9.0.3
            # noinspection PyUnresolvedReferences
            from pip.req import parse_requirements
        # noinspection PydanticTypeChecker,PyTypeChecker
        return {
            item.stem: sorted([str(req.requirement) for req in parse_requirements(str(item), session='workaround')])
            for item in self.glob('requirements*')
        }

    @property
    def resolved(self) -> Path:
        return self.resolve()

    def rm(self, missing_ok=True):
        """
        Delete a folder/file (even if the folder is not empty)

        Args:
            missing_ok: missing_ok
        """
        if not missing_ok and not self.exists():
            raise
        if self.exists():
            # It exists, so we have to delete it
            if self.is_dir():  # If false, then it is a file because it exists
                shutil.rmtree(self)
            else:
                self.unlink()

    def scan(self, option: PathOption = PathOption.FILES,
             output: PathOutput = PathOutput.BOX, suffix: PathSuffix = PathSuffix.NO,
             level: bool = False, hidden: bool = False, frozen: bool = False) -> Union[box.Box, dict, list]:
        """
        Scan Path.

        Args:
            option: what to scan in path.
            output: scan return type.
            suffix: suffix to scan.
            level: scan files two levels from path.
            hidden: include hidden files and dirs.
            frozen: frozen box.

        Returns:
            Union[box.Box, dict, list]: list [paths] or dict {name: path}.
        """

        def scan_level():
            b = box.Box()
            for level1 in self.iterdir():
                if not level1.stem.startswith('.') or hidden:
                    if level1.is_file():
                        if option is PathOption.FILES:
                            b[level1.stem] = level1
                    else:
                        b[level1.stem] = {}
                        for level2 in level1.iterdir():
                            if not level2.stem.startswith('.') or hidden:
                                if level2.is_file():
                                    if option is PathOption.FILES:
                                        b[level1.stem][level2.stem] = level2
                                else:
                                    b[level1.stem][level2.stem] = {}
                                    for level3 in level2.iterdir():
                                        if not level3.stem.startswith('.') or hidden:
                                            if level3.is_file():
                                                if option is PathOption.FILES:
                                                    b[level1.stem][level2.stem][level3.stem] = level3
                                            else:
                                                b[level1.stem][level2.stem][level3.stem] = {}
                                                for level4 in level3.iterdir():
                                                    if not level3.stem.startswith('.') or hidden:
                                                        if level4.is_file():
                                                            if option is PathOption.FILES:
                                                                b[level1.stem][level2.stem][level3.stem][level4.stem] \
                                                                    = level4
                                                if not b[level1.stem][level2.stem][level3.stem]:
                                                    b[level1.stem][level2.stem][level3.stem] = level3
                                    if not b[level1.stem][level2.stem]:
                                        b[level1.stem][level2.stem] = level2
                        if not b[level1.stem]:
                            b[level1.stem] = level1
            return b

        def scan_dir():
            both = box.Box({Path(item).stem: Path(item) for item in self.glob(f'*{suffix.lowerdot}')
                            if not item.stem.startswith('.') or hidden})
            if option is PathOption.BOTH:
                return both
            if option is PathOption.FILES:
                return box.Box({key: value for key, value in both.items() if value.is_file()})
            if option is PathOption.DIRS:
                return box.Box({key: value for key, value in both.items() if value.is_dir()})

        rv = scan_level() if level else scan_dir()
        if output is PathOutput.LIST:
            return list(rv.values())
        if frozen:
            return rv.frozen
        return rv

    @property
    def scripts(self) -> list:
        directory = self / 'scripts'
        if directory.is_dir():
            return [item.chmod(PathMode.X.value) for item in directory.iterdir() if directory.is_dir()]
        return list()

    @property
    def scripts_relative(self) -> list:
        return sorted([str((item.relative_to(self))) for item in self.scripts])

    @property
    def str(self) -> str:
        return self.text

    @property
    def templates(self) -> dict:
        """
        Iter dir for templates and create dict with name and dump func

        Returns:
            dict:
        """
        if self.name != 'templates':
            # noinspection PyMethodFirstArgAssignment
            self /= 'templates'

        if self.is_dir():
            return {item.stem: self.j2(item) for item in self.glob(f'*.{PathSuffix[self.j2.__name__].lowerdot}')}
        return dict()

    def touch_add(self, name, mode=0o600, exist_ok=True) -> Path:
        """
        Add file, touch and return post_init Path.

        Args:
            name: name
            mode: mode
            exist_ok: exist_ok

        Returns:
            Path:
        """
        if (p := (self / name).resolved).is_file() is False:
            p.touch(mode=mode, exist_ok=exist_ok)
        return p

    @property
    def text(self) -> str:
        return str(self)


@dataclass
class Py:
    """Python Server Information Class."""
    python_version: tuple[int] = platform.python_version_tuple()
    PY2: bool = True if int(python_version[0]) == 2 else False
    PY3: bool = True if int(python_version[0]) == 3 else False
    PY310: bool = True if PY3 and int(python_version[1]) == 10 else False
    PY39: bool = True if PY3 and int(python_version[1]) == 9 else False
    PY38: bool = True if PY3 and int(python_version[1]) == 8 else False
    PY37: bool = True if PY3 and int(python_version[1]) == 7 else False
    sys_executable: Any = sys.executable
    sys_executable_name: str = str()
    sys_base_prefix: Any = sys.base_prefix
    sys_prefix: Any = sys.prefix
    sys_base_site_packages: Any = None
    sys_site_packages: Any = None
    VENV: bool = None
    exception: tuple = tuple()

    def __post_init__(self):
        self.sys_executable = Path(sys.executable).resolved
        self.sys_executable_name = self.sys_executable.name
        self.sys_base_prefix = Path(sys.base_prefix).resolved
        self.sys_prefix = Path(sys.prefix).resolved
        # self.sys_base_site_packages = self.sys_base_prefix / 'lib' / self.sys_executable_name / 'site-packages'
        # self.sys_site_packages = self.sys_prefix / 'lib' / self.sys_executable_name / 'site-packages'
        # self.VENV: bool = True if self.sys_base_prefix != self.sys_prefix else False

        if set(self.exception) == {True}:
            raise RuntimeError('Invalid python version', f'{self.python_version=}')


@dataclass
class Sem(BaseData):
    http: Union[int, dict[Priority, asyncio.Semaphore]] = 500
    max: Union[int, dict[Priority, asyncio.Semaphore]] = 2000
    mongo: Union[int, dict[Priority, asyncio.Semaphore]] = 499
    nmap: Union[int, dict[Priority, asyncio.Semaphore]] = 500
    os: Union[int, dict[Priority, asyncio.Semaphore]] = 300
    ssh: Union[int, dict[Priority, asyncio.Semaphore]] = 500
    ping: Union[int, dict[Priority, asyncio.Semaphore]] = 750
    socket: Union[int, dict[Priority, asyncio.Semaphore]] = 400
    tests: Union[int, dict[Priority, asyncio.Semaphore]] = 2

    __ignore_attr__ = ['sems', ]

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)
        for name in self.attrs:
            value = getattr(self, name)
            if isinstance(value, int):
                low = val if (val := round(getattr(self, name) / Priority.LOW.value)) else 1
                setattr(self, name,
                        {
                            Priority.LOW: asyncio.Semaphore(low),
                            Priority.HIGH: asyncio.Semaphore(val if (val := round(low / Priority.HIGH.value)) else 1)
                        })

    async def run(self, func: Union[Callable, Coroutine], /, *args, priority: Priority = Priority.LOW,
                  sem: Sems = Sems.MONGO, **kwargs) -> Any:
        """
        Sem run.

        Args:
            func: func.
            priority: priority.
            sem: sem.
            **kwargs: **kwargs.

        Returns:
            Any:
        """

        def _msg(prefix: str = 'Waiting') -> dict:
            return dict(called=call) | cast(Mapping, {prefix: func.__qualname__}) | dict(
                Priority=priority.name, Using=using, Value=_sem._value, Status=value) | (
                       dict(Running=Kill.count()) if sem.lower in Kill.count_values else dict())

        call = Caller(index=cast(int, Caller.index) + 1 if sem is Sems.MONGO else Caller.index)
        value = getattr(self, sem.lower)
        _sem = value[Priority.LOW]
        using = Priority.LOW.name
        if priority is Priority.HIGH and sem.locked():
            _sem = value[priority]
            using = priority.name
        await self.w(**_msg())
        # TODO: Poner el retry aqui y un run con retry de sync, aqui run_sync y run_async!!!!.
        async with _sem:
            await self.n(**_msg('Acquired'))
            with warnings.catch_warnings(record=False):
                warnings.filterwarnings('ignore', category=RuntimeWarning)
                warnings.showwarning = lambda *_args, **_kwargs: None
                obj = Obj(func)
                if obj.coroutinefunction:
                    rv = await func(*args, **kwargs)
                elif obj.coroutine:  # includes property and coro.
                    rv = await func
                elif obj.awaitable:
                    rv = await func(*args, **kwargs)
                elif obj.routine:
                    rv = func(*args, **kwargs)
                else:
                    rv = func
        await self.n(**_msg('Released'))
        return rv

    @property
    def sems(self) -> dict[str, dict[Priority, dict[str, Union[bool, int]]]]:
        return self.asdict

    def value(self, sem: Sems = Sems.MONGO) -> dict[Priority, dict[str, Union[bool, int]]]:
        return self.sems[sem.lower]


class SetUpToolsPostDevelopCommand(setuptools.command.develop.develop):
    """Post-installation for development mode."""
    function = None

    def run(self):
        if self.function:
            self.function()
        setuptools.command.develop.develop.run(self)


class SetUpToolsPostInstallCommand(setuptools.command.install.install):
    """Post-installation for installation mode."""
    function = None

    def run(self):
        if self.function:
            self.function()
        setuptools.command.install.install.run(self)


class SetUpToolsScriptPath(setuptools.command.install.install):
    def run(self):
        # does not call install.run() by design
        # noinspection PyUnresolvedReferences
        self.distribution.install_scripts = Path(self.install_scripts)


@dataclass
class System(Distro, Executable, Machine, Py):
    """Distro, Executable/Commands Installed, Server OS, Platform and Python Information Class."""
    pass


class Url(furl.furl, Base):
    """
    Furl Class.

    GitHub repositories http
    GitHub repos ssh
    Go
    Api Rest
    Repo test and prod
    Ports and Docker host

    Examples:
        >>> assert Url.email(os.environ.get('USER')) == Url.email(User().name)
        >>> Url.github()
        Url('https://github.com')
        >>> Url.wiki(number=183238657, page='Hola', stdout=False)
        Url('https://nferx.atlassian.net/wiki/spaces/DevOps/pages/183238657/Hola')
        >>> Url.lumenbiomics(repo='test')
        'org-4379404@github.com:lumenbiomics/test'
        >>> http_url = Url.lumenbiomics(http=True, repo='test', username=User().github_username, password='password')
        >>> u = f'{Url.scheme_default}://{User().github_username}:password@{Url.github().host}/{Url.organization}/test'
        >>> assert http_url.url == u
        >>> repo = Url(host=Url.nferx(), name='repotest', bind=9091)
        >>> repo.url
        'https://repotest.nferx.com'
        >>> url = Url(host=repo, name='nexus', port=8080, bind=3001)
        >>> url.url, url.name, url.bind
        ('https://nexus.repotest.nferx.com:8080', 'nexus', 3001)
    """
    Domain: Any = collections.namedtuple('Domain', 'nference nferxops nferx')
    domain: Domain = Domain('nference.net', 'nferxops.net', 'nferx.com')
    bind: int = None
    company: str = domain.nference
    container: int = None
    group: str = 'DevOps'
    id: str = 'org-4379404'
    ops: str = domain.nferxops
    organization: str = 'lumenbiomics'
    scheme_default: str = 'https'
    server: str = domain.nferx

    def __init__(self, host, name: str = None, **kwargs):
        if not kwargs.get('scheme', None):
            kwargs.update(scheme=self.scheme_default)
        self.bind, kwargs = pop_default(kwargs, 'bind')
        self.container, kwargs = pop_default(kwargs, 'container')
        host = host.host if isinstance(host, Url) else host
        prefix = f'{name}.' if name else str()
        kwargs.update(host=f'{prefix}{host.host if isinstance(host, Url) else host}')
        super(Url, self).__init__(**kwargs)

    @staticmethod
    @app.command(context_settings=appcontext)
    def email(username: str = str(), stdout: bool = False) -> str:
        """
        User Email.

        Args:
            username: username.
            stdout: stdout.

        Returns:
            Str:
        """
        username = username if username else User().name
        rv = f'{username}@{Url.nference().host}'
        if stdout:
            cprint(rv)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def github(stdout: bool = False) -> Url:
        """
        GitHub Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url('github.com')
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def lumenbiomics(repo: str = None, http: bool = False, username: str = None, password: str = None,
                     suffix: bool = False, stdout: bool = False) -> Union[Url, str]:
        """
        Lumenbiomics repos url.

        Args:
            repo: repo
            http: http
            username: username
            password: GitHub API token
            suffix: suffix
            stdout: stdout.

        Returns:
            Union[Url, str]:
        """
        repo = repo if repo else setup_bapy.repo
        password = password if password else Url.token()
        g = PathSuffix.GIT.lowerdot if suffix else str()
        p = '/'.join((Url.organization, repo)) + g

        if http:
            # https://jose-nferx:<api_token>@github.com/lumenbiomics/configs.git
            rv = Url(Url.github(), **dict(path=f'{p}', **(
                dict(username=username, password=password) if password and username else dict())))
            if stdout:
                cprint(rv.url)
            return rv
        rv = f'{Url.id}@{Url.github().host}:{p}'  # org-4379404@github.com:lumenbiomics/repos.git
        if stdout:
            cprint(rv)
        return rv

    @property
    def name(self) -> str:
        """
        Last path or first subdomain.

        Returns:
            Str:
        """
        return self.path.split('/')[-1] if self.path else self.host.split('.')[0]

    @staticmethod
    @app.command(context_settings=appcontext)
    def nference(stdout: bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.company)
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def nferx(stdout: bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.server)
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def nferxops(stdout: bool = False) -> Url:
        """
        Nferx Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(Url.ops)
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def repo(stdout: bool = False) -> Url:
        """
        Repo Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(host=Url.nferx(), name='repo')
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def repository(stdout: bool = False) -> Url:
        """
        Repository repo Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url.repo() / 'repository'
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def repotest(stdout: bool = False) -> Url:
        """
        Repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url(host=Url.nferx(), name='repotest')
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def repositorytest(stdout: bool = False) -> Url:
        """
        Repository repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = Url.repotest() / 'repository'
        if stdout:
            cprint(rv.url)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def token(stdout: bool = False) -> str:
        """
        Repository repotest Url.

        Args:
            stdout: stdout.

        Returns:
            Url:
        """
        rv = os.environ.get('NFERX_GITHUB_PASSWORD', str())
        if stdout:
            cprint(rv)
        return rv

    @staticmethod
    @app.command(context_settings=appcontext)
    def wiki(space: str = group, number: int = int(), page: str = str(), stdout: bool = True) -> Url:
        """
        Confluence Wiki Url.

        https://nferx.atlassian.net/wiki/spaces/DevOps/pages/183238657/Repository+Manager

        Args:
            space: space
            number: number
            page: page
            stdout: stdout

        Returns:
            Any:
        """
        name = Url.nferx().name
        p = f'wiki/spaces/{space}/pages/{number}/{page.replace(" ", "+")}' if number and page else 'wiki'
        rv = Url('atlassian.net', name=name, path=p)
        if stdout:
            cprint(rv.url)
        return rv


class Up:
    """APP/CLI PathOption."""
    Bump: Any = Literal['patch', 'minor', 'major']

    @classmethod
    def args(cls):
        return cls.Bump.__args__

    @classmethod
    def option(cls):
        return typer.Option(cls.args()[0], help='Version part to be increased.', autocompletion=cls.args)


@dataclasses.dataclass
class UserActual:
    """User Base."""
    name: str = datafield(init=False)
    passwd: Any = datafield(init=False)
    gecos: Any = datafield(init=False)
    gid: Any = datafield(init=False)
    gname: Any = datafield(init=False)
    home: Any = datafield(init=False)
    id: Any = datafield(init=False)
    shell: Any = datafield(init=False)
    ssh: Any = datafield(init=False)
    id_rsa: Any = datafield(init=False)
    id_rsa_pub: Any = datafield(init=False)
    auth_keys: Any = datafield(init=False)
    git_config_path: Any = datafield(init=False)
    git_config: Any = datafield(init=False)
    github_username: Any = datafield(init=False)
    GITHUB_USERNAME: bool = datafield(init=False)

    def __post_init__(self):
        try:
            self.name = pathlib.Path('/dev/console').owner() if psutil.MACOS else os.getlogin()
        except OSError:
            self.name = pathlib.Path('/proc/self/loginuid').owner()

        try:
            self.passwd = pwd.getpwnam(self.name)
        except KeyError:
            red(f'Invalid user: {self.name}')
        else:
            self.gecos = self.passwd.pw_gecos
            self.gid = self.passwd.pw_gid
            self.gname = grp.getgrgid(self.gid).gr_name
            self.home = Path(self.passwd.pw_dir)
            self.id = self.passwd.pw_uid
            self.shell = Path(self.passwd.pw_shell)
            self.ssh = self.home / ssh_dir
            self.id_rsa = self.ssh / id_rsa
            self.id_rsa_pub = self.ssh / id_rsa_pub
            self.auth_keys = self.ssh / authorized_keys
            self.git_config_path = self.home / gitconfig
            self.git_config = git.GitConfigParser(self.git_config_path.text)
            self.github_username = self.git_config.get_value(section='user', option='username', default=str())
            self.GITHUB_USERNAME = True if self.github_username else False


@dataclasses.dataclass
class UserProcess:
    """User Process Class."""
    sudo_user: str = os.getenv('SUDO_USER')
    SUDO: bool = True if sudo_user is not None else False
    gid: int = os.getgid()
    gname: str = grp.getgrgid(gid).gr_name
    id: int = os.getuid()
    passwd: pwd.struct_passwd = pwd.getpwuid(id)
    gecos: str = pwd.getpwuid(id).pw_gecos
    home: Path = datafield(default=pwd.getpwuid(id).pw_dir, init=False)
    name: str = pwd.getpwuid(id).pw_name
    shell: Path = datafield(default=pwd.getpwuid(id).pw_shell, init=False)
    ssh: Path = datafield(init=False)
    id_rsa: Path = datafield(init=False)
    id_rsa_pub: Path = datafield(init=False)
    auth_keys: Path = datafield(init=False)
    ROOT: bool = True if id == 0 else False
    git_config_path: Path = datafield(init=False)
    git_config: git.GitConfigParser = datafield(init=False)
    github_username: str = datafield(init=False)
    GITHUB_USERNAME: bool = datafield(init=False)

    def __post_init__(self):
        self.home = Path(self.home)
        self.shell = Path(self.shell)
        self.ssh = self.home / ssh_dir
        self.id_rsa = self.ssh / id_rsa
        self.id_rsa_pub = self.ssh / id_rsa_pub
        self.auth_keys = self.ssh / authorized_keys
        self.git_config_path = self.home / gitconfig
        self.git_config = git.GitConfigParser(self.git_config_path.text)
        self.github_username = self.git_config.get_value(section='user', option='username', default=str())
        self.GITHUB_USERNAME = True if self.github_username else False


@dataclasses.dataclass
class User:
    """User Class."""
    username: str = 'upload'
    admin: Any = UserPasswd('admin', os.environ.get('REPO_DEFAULT_ADMIN_PASSWORD'))
    default: Any = UserPasswd(username, username)
    actual: UserActual = datafield(init=False)
    process: UserProcess = datafield(init=False)
    ROOT: bool = datafield(init=False)
    SUDO: bool = datafield(init=False)
    sudo_user: str = datafield(init=False)
    passwd: pwd.struct_passwd = datafield(init=False)
    gecos: str = datafield(init=False)
    gid: int = datafield(init=False)
    gname: str = datafield(init=False)
    home: Path = datafield(init=False)
    id: int = datafield(init=False)
    name: str = datafield(init=False)
    shell: Path = datafield(init=False)
    ssh: Path = datafield(init=False)
    id_rsa: Path = datafield(init=False)
    id_rsa_pub: Path = datafield(init=False)
    auth_keys: Path = datafield(init=False)
    git_config_path: Path = datafield(init=False)
    git_config: git.GitConfigParser = datafield(init=False)
    github_username: str = datafield(init=False)
    GITHUB_USERNAME: bool = datafield(init=False)

    def __post_init__(self):
        self.actual = UserActual()
        self.process = UserProcess()
        self.ROOT = self.process.ROOT
        self.SUDO = self.process.SUDO
        self.sudo_user = self.process.sudo_user
        self.passwd = self.process.passwd if self.SUDO else self.actual.passwd
        self.gecos = self.process.gecos if self.SUDO else self.actual.gecos
        self.gid = self.process.gid if self.SUDO else self.actual.gid
        self.gname = self.process.gname if self.SUDO else self.actual.gname
        self.home = self.process.home if self.SUDO else self.actual.home
        self.id = self.process.id if self.SUDO else self.actual.id
        self.name = self.process.name if self.SUDO else self.actual.name
        self.shell = self.process.shell if self.SUDO else self.actual.shell
        self.ssh = self.process.ssh if self.SUDO else self.actual.ssh
        self.id_rsa = self.process.id_rsa if self.SUDO else self.actual.id_rsa
        self.id_rsa_pub = self.process.id_rsa_pub if self.SUDO else self.actual.id_rsa_pub
        self.auth_keys = self.process.auth_keys if self.SUDO else self.actual.auth_keys
        self.git_config_path = self.process.git_config_path if self.SUDO else self.actual.git_config_path
        self.git_config: git.GitConfigParser = self.process.git_config if self.SUDO else self.actual.github_username
        self.github_username = self.process.github_username if self.SUDO else self.actual.github_username
        self.GITHUB_USERNAME = self.process.GITHUB_USERNAME if self.SUDO else self.actual.GITHUB_USERNAME


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


async def aiocmd(command: Union[str, list], decode: bool = True, utf8: bool = False,
                 lines: bool = False) -> Union[Cmd, int, list, str]:
    """
    Asyncio run cmd.

    Args:
        command: command.
        decode: decode and strip output.
        utf8: utf8 decode.
        lines: split lines.

    Returns:
        Union[CmdOut, int, list, str]: [stdout, stderr, proc.returncode].
    """
    proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE, loop=asyncio.get_running_loop())
    stdout, stderr = await proc.communicate()
    if decode:
        stdout = stdout.decode().rstrip('.\n')
        stderr = stderr.decode().rstrip('.\n')
    elif utf8:
        stdout = stdout.decode('utf8').strip()
        stderr = stderr.decode('utf8').strip()

    out = stdout.splitlines() if lines else stdout

    return Cmd(out, stderr, proc.returncode)


def aioclosed() -> bool:
    return asyncio.get_event_loop().is_closed()


def aioloop() -> Optional[asyncio.events._RunningLoop]:
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


def aioloopid():
    try:
        return asyncio.get_running_loop()._selector
    except RuntimeError:
        return None


def aiorunning() -> bool:
    return asyncio.get_event_loop().is_running()


@app.command(context_settings=appcontext)
def appdir(stdout: bool = False) -> None:
    """
    CLI/APP dir.

    Args:
        stdout: stdout.

    Returns:
        None:
    """
    if stdout:
        green(typer.get_app_dir(str(pathlib.Path(__file__).parent)))
    else:
        return green(typer.get_app_dir(str(pathlib.Path(__file__).parent)))


@app.command(context_settings=appcontext)
def ask(msg: str) -> bool:
    """
    Ask Yes or No.

    Args:
        msg: text message.

    Returns:
        bool:
    """
    from rich.prompt import Prompt
    if Prompt.ask(msg, choices=['Yes', 'No'], default='Yes') == 'Yes':
        return True
    return False


@app.command(context_settings=appcontext)
def base64auth(username: str, password: str, stdout: bool = False) -> str:
    """
    Generates a base64 auth for usage with .npmrc.

    Args:
        username: user name.
        password: user password.
        stdout: stdout.

    Returns:
        Str: openssl base64.
    """
    rv = os.popen(f'echo -n "{username}:{password}" | openssl base64').read().splitlines()[0]
    if stdout:
        cprint(rv)
    return rv


@singledispatch
def clean_empty(obj: Any) -> Any:
    """
    Clean empty keys in nested dict.

    isinstance() checks are taken care of by @singledispatch based on the type annotations of the registered functions.

    Any values set to numeric 0 (integer 0, float 0.0) will also be cleared. Numeric 0 values can be retained
    with if v or v == 0.

    Args:
        obj:

    Returns:

    """
    return obj


@clean_empty.register
def _dicts(dct: dict) -> dict:
    items = ((k, clean_empty(v)) for k, v in dct.items())
    return {k: v for k, v in items if v}


@clean_empty.register
def _lists(l: list) -> list:
    items = map(clean_empty, l)
    return [v for v in items if v]


@clean_empty.register
def _sets(l: set) -> set:
    items = map(clean_empty, l)
    return {v for v in items if v}


def click_custom_startswith(string: str, incomplete: str) -> bool:
    """
    A custom completion matching that supports case insensitive matching.

    Args:
        string: string
        incomplete: incomplete

    Returns:
        bool:
    """
    case_insensitive_completion: str = '_CLICK_COMPLETION_COMMAND_CASE_INSENSITIVE_COMPLETE'

    if os.environ.get(case_insensitive_completion):
        string = string.lower()
        incomplete = incomplete.lower()
    return string.startswith(incomplete)


click_completion.core.startswith = click_custom_startswith


def cmd(command: Iterable, shell: bool = True, sysexec: bool = False,
        lines: bool = True) -> Union[Cmd, int, list, str]:
    """
    Runs a cmd.

    Examples:
        >>> cmd('ls a')
        CmdOut(stdout=[], stderr=['ls: a: No such file or directory'], rc=1)
        >>> assert 'Requirement already satisfied' in cmd('pip install pip', sysexec=True)[0][0]
        >>> cmd('ls a', shell=False, lines=False)  # Extra '\' added to avoid docstring error.
        CmdOut(stdout='', stderr='ls: a: No such file or directory\\n', rc=1)
        >>> cmd('echo a', lines=False)  # Extra '\' added to avoid docstring error.
        CmdOut(stdout='a\\n', stderr='', rc=0)

    Args:
        command: command.
        shell: expands shell variables and one line (shell True expands variables in shell).
        sysexec: runs with sys executable.
        lines: split lines so ``\\n`` is removed from all lines (extra '\' added to avoid docstring error).

    Returns:
        Union[CmdOut, int, list, str]:
    """
    if sysexec:
        command = f'{sys.executable} -m {command}'
    elif not shell:
        command = shlex.split(command)

    if lines:
        text = False
    else:
        text = True

    proc = subprocess.run(command, shell=shell, capture_output=True, text=text)

    def rv(out=True):
        if out:
            if lines:
                return proc.stdout.decode("utf-8").splitlines()
            else:
                # return proc.stdout.decode("utf-8").rstrip('.\n')
                return proc.stdout
        else:
            if lines:
                return proc.stderr.decode("utf-8").splitlines()
            else:
                # return proc.stderr.decode("utf-8").rstrip('.\n')
                return proc.stderr

    return Cmd(rv(), rv(False), proc.returncode)


def cmd_completion(cls, append, case_insensitive, p):
    def provide_default():
        if os.name == 'posix':
            return os.path.basename(os.environ['SHELL'])
        elif os.name == 'nt':
            return os.path.basename(os.environ['COMSPEC'])
        raise NotImplementedError(f'OS {os.name!r} support not available')

    try:
        shell = shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        shell = provide_default()

    extra_env = {cls.case_insensitive_completion: 'ON OFF'} if case_insensitive else {}
    shell, p = click_completion.core.install(shell=shell, path=p, append=append, extra_env=extra_env)
    click.echo(f'{shell} completion installed in {p}')


@app.command(context_settings=appcontext)
def confirmation(msg: str) -> bool:
    """
    Ask for Yes/no and confirmation.

    Args:
        msg: text message.

    Returns:
        bool:
    """
    if ask(msg):
        are_you_sure = rich.prompt.Confirm.ask(f'Are you sure?')
        assert are_you_sure
        return True
    return False


def datafactory(data: Union[dict, list, collections.OrderedDict, set]) -> \
        Union[dict, list, collections.OrderedDict, set]:
    return data


def datafactorytype(cls, field) -> Any:
    """
    Default factory for dataclass field with type.

    Args:
        cls:
        field:

    Returns:
        Any:
    """
    for attr in dataclasses.fields(cls):
        if attr.name == field:
            return attr.type()


def default_dict(*args, factory: Optional[Callable] = dict, init: Any = dict, **kwargs) -> collections.defaultdict:
    return collections.defaultdict(factory, init(*args, **kwargs) if callable(init) else init)


def del_key(data: Union[dict, list], key: Iterable = ('self', 'cls',)) -> Optional[dict, list]:
    rv = None
    key = iter_split(key)
    if isinstance(data, dict):
        rv = data.copy()
        for item in key:
            with suppress(KeyError):
                del rv[item]
    elif isinstance(data, list):
        for item in key:
            with suppress(ValueError):
                data.remove(item)
        rv = data
    return rv


def dict_exclude(data: dict, exclude: Union[list, tuple] = None) -> Optional[dict]:
    """
    Dict with vars in `exclude`. Default: private vars.

    Args:
        data: input dict.
        exclude: vars to exclude.

    Example:
        >>> import inspect
        >>>
        >>> new_dict = dict_include(inspect.stack(2)[0].frame.f_locals, include=('__annotations__', ))

    Returns:
        Optional[dict]:
    """
    if exclude:
        return {key: value for key, value in data.items() if key != exclude}
    else:
        return {key: value for key, value in data.items() if key[:1] != '_'}


def dict_include(data: dict, include: Union[list, tuple] = None) -> Optional[dict]:
    """
    Dict with vars in `include`. Default: ``(str, int, tuple, set, list, bool, float, dict)``.

    Example:
        >>> import inspect
        >>>
        >>> new_dict = dict_include(inspect.stack(2)[0].frame.f_globals)

    Args:
        data: input dict.
        include: vars to include.

    Returns:
        Optional[dict]:
    """
    if include:
        return {key: value for key, value in data.items() if key in include}
    else:
        return {key: value for key, value in data.items()
                if key[:1] != '_' and type(value) in (str, int, tuple, set, list, bool, float, dict)}


def dict_sort(name: dict, ordered: bool = False) -> Union[dict, collections.OrderedDict]:
    """
    Order a dict based on keys.

    Args:
        name: dict to be ordered.
        ordered: OrderedDict

    Returns:
        Union[dict, collections.OrderedDict]:
    """
    rv = {key: name[key] for key in sorted(name)}
    if ordered:
        return collections.OrderedDict(rv)
    return rv.copy()


def distribution(p: str, stdout: bool = False) -> importlib.metadata.Distribution:
    """
    Package/Project Distribution Information.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        importlib_metadata.Distribution:
    """
    try:
        rv = importlib.metadata.distribution(p)
        if stdout:
            cprint(rv)
        return rv
    except importlib.metadata.PackageNotFoundError:
        pass


def dump_ansible_yaml(p: Any, data: dict):
    """
    Dump yaml with ansible format.

    Args:
        p: path
        data: data
    """
    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=2, offset=2)
    # yaml.compact(seq_seq=False, seq_map=False)
    yaml.dump(data, p.open('w+'))


async def executor(func: Any, *args: Any, pool: Optional[Executor] = None, **kwargs: Any) -> Any:
    """
    Run in :lib:func:`loop.run_in_executor` with :class:`concurrent.futures.ThreadPoolExecutor`,
        :class:`concurrent.futures.ProcessPoolExecutor` or
        :lib:func:`asyncio.get_running_loop().loop.run_in_executor` or not poll.

    Args:
        func: func
        *args: args
        pool: pool
        **kwargs: kwargs

    Raises:
        ValueError: ValueError

    Returns:
        Awaitable:
    """
    loop = asyncio.get_running_loop()
    call = partial(func, *args, **kwargs)
    if not func:
        raise ValueError

    if pool:
        with pool.value() as p:
            return await loop.run_in_executor(p, call)
    return await loop.run_in_executor(pool, call)


def flat_list(l: Iterable, recurse: bool = False, unique: bool = False, sort: bool = True) -> Union[list, Iterable]:
    """
    Flattens an Iterable

    Args:
        l: iterable
        recurse: recurse
        unique: when recurse
        sort: sort

    Returns:
        Union[list, Iterable]:
    """
    if unique:
        recurse = True

    flat = []
    _ = [flat.extend(flat_list(item, recurse, unique) if recurse else item)
         if isinstance(item, list) else flat.append(item) for item in l if item]
    if unique:
        rv = list(set(flat))
        return sorted(rv) if sort else rv
    return flat


def force_async(fn):
    """
    Turns a sync function to async function using threads.
    """
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    pool = ThreadPoolExecutor()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def get_all(obj: dict, get: GetAll = GetAll.KEYS, generator: bool = False) -> Iterable:
    # noinspection PyUnresolvedReferences
    """
    All keys or values of nested dict or List.

    Examples:
        >>> data = dict(key1=dict(key2=dict(key3=dict(key4='value1'))))
        >>> keys = tuple(item for item in get_all(data))
        >>> keys
        ('key1', 'key2', 'key3', 'key4')
        >>> values = tuple(item for item in get_all(data, GetAll.VALUES))
        >>> values
        ('value1',)

    Args:
        obj: obj
        get: get
        generator: generator or return

    Raises:
        ValueError: ValueError

    Yields:
        Iterable:
    """

    def _get_all(o, g):
        if isinstance(o, dict):
            for key, value in o.items():
                if g is GetAll.KEYS:
                    yield key
                elif g == GetAll.VALUES:
                    if not (isinstance(value, dict) or isinstance(value, list)):
                        yield value
                else:
                    raise ValueError('`GetAll.KEYS` or `GetAll.VALUES`')
                for ret in _get_all(value, g=g):
                    yield ret
        elif isinstance(o, list):
            for el in o:
                for ret in _get_all(el, g=g):
                    yield ret

    if generator:
        return _get_all(obj, get)
    return [item for item in _get_all(obj, get)]


def get_choice_class(data: Union[Iterable, GenericAlias], case_sensitive: bool = True) -> click.Choice:
    """
    :class:`click.Echo` from different data sources.

    Examples:
        >>> choice = get_choice_class(Literal['a'])
        >>> choice
        Choice('['a']')
        >>> choice = get_choice_class(choice.choices)
        >>> choice
        Choice('['a']')
        >>> choice = get_choice_class(''.join(choice.choices))
        >>> choice
        Choice('['a']')

    Args:
        data: data
        case_sensitive: case_sensitive

    Returns:
        click.Choice:
    """
    if isinstance(data, GenericAlias):
        data = data.__args__
    elif isinstance(data, str):
        data = data.split()
    return click.Choice(data, case_sensitive)


# noinspection StrFormat
def gen_key(home: Any = None, private: Any = None, public: Any = None, text: Any = None,
            email: Any = None):
    """
    Gpg key generation and exporting public and private keys.

    Args:
        home: gpg home path
        private: gpg private dest path
        public: gpg public dest path
        text: render template
        email: author email
    """
    home = shlex.quote(str(home))
    private = shlex.quote(str(private))
    public = shlex.quote(str(public))
    text = shlex.quote(str(text))
    email = shlex.quote(email)

    with shell_proc.Shell(stdout=sys.stdout, stderr=sys.stderr, blocking=False) as sh:
        sh(
            f'mkdir -p {home}; chmod go-rwx {home}; '
            f'rm -rf {home}/*; '
            f'rm -rf {private} {public}; '
            f'gpg --homedir {home} --batch --gen-key {text}; '
            f'gpg --homedir {home} --export --armor --output {public} {email};'
            f'gpg --homedir {home} --export-secret-key --armor {email} > {private}; '
            f'sudo rm -rf {home}/S.gpg-agent*;'
        )

    time.sleep(1)
    print('1 Second has passed', 'Running:', sh.current_command)
    time.sleep(1)
    print('2 Seconds have passed', 'Running:', sh.current_command)
    time.sleep(1)
    print('3 Seconds have passed', 'Running:', sh.current_command)

    sh.wait()

    table = '|{:_<20}|{:_<20}|{:_<20}|{:_<50}|'
    print(table.format(str(), str(), str(), str()).replace('|', '_'))
    print(table.format("Exit Code", "Has Error", "Has Output", "Command").replace('_', ' '))
    print(table.format(str(), str(), str(), str()))
    for item in sh.history:
        print(table.format(item.exit_code, item.has_error(), item.has_output(), item.cmd).replace('_', ' '))
    print(table.format(str(), str(), str(), str()).replace('|', '_'))


def get_context(variables=str()):
    locals_context_dict = sys._getframe(2).f_locals
    if locals_context_dict.get('l'):
        del locals_context_dict['l']

    if locals_context_dict.get('cls'):
        del locals_context_dict['cls']
    aiotask_context_dict = {}
    try:
        # noinspection PyUnresolvedReferences
        aiotask_context_dict = {key: asyncio.current_task().get(key) for key in asyncio.current_task()}
    except (RuntimeError, AttributeError, NameError,):
        pass

    context_dict = {**locals_context_dict, **aiotask_context_dict, **sys._getframe(2).f_globals}
    context_dict_clean = {key: context_dict.get(key) for key in context_dict if not_(key)
                          and is_data(context_dict.get(key))}
    if variables:
        try:
            msg_dict = {var: str() for var in variables.split() if not context_dict_clean.get(var, None)}
            variables_dict = {var: eval(var, context_dict_clean, msg_dict) for var in variables.split()
                              if not_(var) and is_data(eval(var, context_dict, msg_dict))}
        except (AttributeError, NameError, KeyError):
            pass
        else:
            context_dict_clean = variables_dict
    else:
        if context_dict_clean.get('self', None):
            add = {'self': context_dict_clean['self']}
            context_dict_clean = {**context_dict_clean, **add}
    final = {**context_dict_clean}
    msg = ", ".join("{}: {}".format(key, value) for key, value in {
        var.replace("\\", ""): vars(final.get(var))
        if getattr(final.get(var), '__dict__', None) and var[:1] != '_'
        else final.get(var) for var in list(final)
    }.items() if not_(key) and is_data(key))
    # exception = sys.exc_info()[1]
    # if exception:
    #     exception.args = ('{} [{}]'.format(exception.args[0], msg) if exception.args else msg,) + exception.args[1:]
    return msg


def get_key(data: dict, value: Any) -> Any:
    """
    Get Dict Key from Value.

    Args:
        data: data
        value: value

    Returns:
        Any:
    """
    for key, val in data.items():
        if val == value:
            return key


def get_vars_docs(fname: str) -> dict:
    """
    Read the module referenced in fname (often <module>.__file__) and return a
    dict with global variables, their value and the "docstring" that follows
    the definition of the variable.

    Args:
        fname: fname

    Returns:
        dict:
    """
    file = os.path.splitext(fname)[0] + '.lib'  # convert .pyc to .lib
    with open(file, 'r') as f:
        fstr = f.read()
    rv = {}
    key = None
    for node in ast.walk(ast.parse(fstr)):
        if isinstance(node, ast.Assign):
            key = node.targets[0].id
            rv[key] = [node.value.id, str()]
            continue
        elif isinstance(node, ast.Expr) and key:
            rv[key][1] = node.value.s.strip()
        key = None
    return rv


@app.command(context_settings=appcontext, name='info')
def _info(dist: str = None, executable: bool = False, linux: bool = False,
          machine: bool = False, project: bool = False, py: bool = False, user: bool = False) -> None:
    """
    Command to provide info.

    Args:
        dist: importlib distribution.
        executable: executables in server.
        linux: linux distribution.
        machine: machine information.
        project: package and path information.
        py: python information.
        user: user data.
    """
    dist = dist if dist else setup_bapy.repo

    if not (bool(dist) | executable | linux | machine | project | py | user):
        executable = linux = machine = project = py = user = True

    if dist:
        distri = distribution(dist)
        cprint('[bold blue]Distribution: ', Obj(distri).asdict, '\n', '[bold blue]Metadata: ', metadata(dist), str())
    if executable:
        cprint('[bold blue]Executable: ', dataclasses.asdict(Executable()), str())
    if linux:
        cprint('[bold blue]Distro: ', dataclasses.asdict(Distro()), str())
    if machine:
        cprint('[bold blue]Machine: ', dataclasses.asdict(Machine()), str())
    if project:
        cprint('[bold blue]Path: ', dataclasses.asdict(setup_package), str())
    if py:
        cprint('[bold blue]Py: ', dataclasses.asdict(Py()), str())
    if user:
        cprint('[bold blue]User: ', dataclasses.asdict(User()), str())


def is_data(obj) -> bool:
    def exclude():
        for module in [typing, ]:
            if module is inspect.getmodule(obj):
                return True
        if 'wrapper' in str(type(obj)) or ('__' in str(obj) and '__main__' not in str(obj)):
            return True
        return False

    return not \
        inspect.isabstract(obj) | inspect.isroutine(obj) | inspect.iscode(obj) | inspect.isframe(obj) | \
        inspect.istraceback(obj) | inspect.isawaitable(obj) | inspect.iscoroutine(obj) | inspect.isgenerator(obj) | \
        inspect.isasyncgen(obj) | inspect.isasyncgenfunction(obj) | inspect.iscoroutinefunction(obj) | \
        inspect.isgeneratorfunction(obj) | inspect.isgetsetdescriptor(obj) | inspect.isdatadescriptor(obj) | \
        inspect.ismodule(obj) | inspect.isclass(obj) | exclude()


@app.command(context_settings=appcontext)
def is_pip(stdout: bool = False) -> bool:
    """
    Checks if pip is installed.

    Args:
        stdout: stdout.

    Returns:
        bool
    """
    try:
        # noinspection PyCompatibility
        import pip
        if stdout:
            green(str(True))
        return True
    except ModuleNotFoundError:
        if stdout:
            red(str(False))
        return False


def iter_split(data: Iterable) -> Any:
    """
    Item str().split() and Iterables.

    Args:
        data: data

    Raises:
        TypeError: TypeError

    Returns:
        Any:
    """
    if isinstance(data, Iterable):
        if isinstance(data, str):
            return data.split() if ' ' in data else [data]
        return data
    else:
        raise TypeError(f'{data=} must be iterable.')


def list_utils(list_: [list, tuple] = None, option: ListUtils = ListUtils.LOWER) -> list:
    return [getattr(item, option.lower)() for item in list_]


def literal(data, index: int = None) -> Union[list[str], str]:
    if index is None:
        return list(data.__args__)
    return data.__args__[index]


def load_modules(p) -> None:
    """
    Load Modules of Package.

    Args:
        p: package.
    """
    p._modules = []

    pkgname = p.__name__
    pkgpath = pathlib.Path(p.__file__).parent

    # noinspection PyTypeChecker
    for mod in pkgutil.iter_modules([pkgpath]):
        modulename = pkgname + '.' + mod[1]
        __import__(modulename, locals(), globals())
        module = sys.modules[modulename]

        module._package = p
        # module._packageName = pkgname

        p._modules.append(module)
        if pathlib.Path(module.__file__).parent == pkgpath:
            module._isPackage = False
        else:
            module._isPackage = True
            # noinspection PyTypeChecker,PydanticTypeChecker
            load_modules(module)


def mapped_commands(command_map: dict) -> Any:
    """
    Commands mapping.

    Args:
        command_map: command_map

    Returns:
        Any:
    """

    class CommandGroup(click.Group):
        def get_command(self, ctx, cmd_name):
            for real_command, aliases in command_map.items():
                if cmd_name in aliases:
                    return click.Group.get_command(self, ctx, real_command)
            return None

        def list_commands(self, ctx):
            return [a for b in command_map.values() for a in b]

    return CommandGroup


def metadata(p: str = None, stdout: bool = False) -> mailbox.Message:
    """
    Package/Project Metadata Information.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        dict:
    """
    p = p if p else setup_package.repo
    try:
        rv = importlib.metadata.metadata(p)
        if stdout:
            cprint(rv)
        return rv
    except importlib.metadata.PackageNotFoundError:
        pass


def mod_name(mod):
    return mod.__name__.rpartition('.')[-1]


def move_to_key(mydict: dict, new_key: str, keys_to_move: Union[list, tuple]):
    if set(mydict.keys()).intersection(keys_to_move):
        mydict[new_key] = {}
        for k in keys_to_move:
            mydict[new_key][k] = mydict[k]
            del mydict[k]


def namedtuple(typename: Any, fields: Union[list, str, tuple] = None, defaults: tuple = None,
               fieldtype: Any = str) -> Any:
    """
    Makes a post_init typing `collections.namedtuple`.

    Examples:
        >>> import pathlib
        >>> domain_fields: tuple = ('company', 'server', )
        >>> Domain = namedtype('Domain', domain_fields)
        >>> assert 'Domain' in str(Domain)
        >>> domain_values: tuple = ('nference.net', 'nferx.com', )
        >>> domain: Domain = namedtuple('Domain', domain_fields, defaults=domain_values)
        >>> domain
        Domain(company='nference.net', server='nferx.com')
        >>> assert 'Domain' in str(type(domain))
        >>> dir_names: tuple = 'download', 'generated',
        >>> # noinspection PyUnresolvedReferences
        >>> dir_defaults: tuple = tuple(pathlib.Path('/tmp') / item for item in dir_names)
        >>> dir_defaults
        (Path('/tmp/download'), Path('/tmp/generated'))
        >>> dirs = namedtuple('TmpDir', dir_names, dir_defaults, pathlib.Path)
        >>> dirs
        TmpDir(download=Path('/tmp/download'), generated=Path('/tmp/generated'))
        >>> assert'TmpDir' in str(type(dirs))

    Args:
        typename: Named Tuple Yyping Name.
        fields: Named Tuple Field Names.
        fieldtype: Named Tuple Fields typing.
        defaults: Creates Named Tuple with defaults values.

    Returns:
        Any: post_init typing `collections.namedtuple`.
    """
    fields = fields.split() if isinstance(fields, str) else fields
    typename = namedtype(typename, fields, fieldtype) if isinstance(typename, str) else typename
    TypeNameDefaults: typename = collections.namedtuple(typename.__name__, typename._fields, defaults=defaults)
    name_defaults: typename = TypeNameDefaults()
    return name_defaults


def namedtype(typename, fields: Union[list, str, tuple], fieldtype: Any = str) -> Any:
    """
    Returns a typing NamedTuple associating fieldtype to fields.

    Examples:
        >>> import pathlib
        >>> domain_fields: tuple = ('company', 'server', )
        >>> Domain = namedtype('Domain', domain_fields)
        >>> assert 'Domain' in str(Domain)
        >>> type(Domain)
        <class 'type'>
        >>> home_dir_names: tuple = ('download', 'generated', 'github', 'log', 'tmp', )
        >>> HomeDir = namedtype('HomeDir', home_dir_names, pathlib.Path)
        >>> assert 'HomeDir' in str(HomeDir)
        >>> type(HomeDir)
        <class 'type'>

    Args:
        typename: Named Tuple Typing Name.
        fields: Named Tuple Field Names.
        fieldtype: Named Tuple Fields typing.

    Returns:
        Any: post_init typing `collections.namedtuple`.
    """
    fields = fields.split() if isinstance(fields, str) else fields
    return NamedTuple(typename, **{item: fieldtype for item in fields})


def not_(name: str) -> bool:
    """
    Is not private?

    Args:
        name: name

    Returns:
        bool:
    """
    return name[:1] != '_'


@app.command(context_settings=appcontext, name='package')
def _package():
    """Package."""
    setup_bapy.ic.enabled = True
    setup_bapy.ic(setup_package)


@app.command(context_settings=appcontext)
def package_info(p: str = None, stdout: bool = False) -> tuple[bool, str, str]:
    """
    Check if installed version of package is the latest.

    Args:
        p: package name.
        stdout: stdout.

    Returns:
        tuple[bool, str, str]: [``upgrade_version`` upgrade version current != latest, ``current_version``,
            ``latest_version``].
    """
    p = p if p else setup_package.repo
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(p)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]

    current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(p)],
                                         capture_output=True, text=True))
    current_version = current_version[current_version.find('Version:') + 8:]
    current_version = current_version[:current_version.find('\\n')].replace(' ', '')

    upgrade_version = False if latest_version == current_version else True
    if stdout:
        cprint(upgrade_version, current_version, latest_version)
    return upgrade_version, current_version, latest_version


@app.command(context_settings=appcontext)
def package_latest(p: str = None, stdout: bool = False) -> str:
    """
    Latest version of package using pip install random as version.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        Str: latest_version.
    """
    p = p if p else setup_package.repo
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(p)],
                                        capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:') + 15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ', '').split(',')[-1]
    if stdout:
        cprint(latest_version)
    return latest_version


@app.command(context_settings=appcontext)
def package_latest_search(p: str = None, stdout: bool = False) -> str:
    """
    Latest version of package using pip search.

    Args:
        p: package.
        stdout: stdout.

    Returns:
        Str: latest_version.
    """
    p = p if p else setup_package.repo
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'search', p], capture_output=True, text=True))
    text = f'{p} ('
    latest_version = latest_version[latest_version.find(text) + len(text):]
    latest_version = latest_version[:latest_version.find(')')]
    if stdout:
        cprint(latest_version)
    return latest_version


def pop_default(data: dict, key: Any, default: Any = None) -> tuple[Any, dict]:
    """
    Dict Pop with Default.

    Examples:
        >>> pop_default(dict(a=1), 'b', True) #doctest: +ELLIPSIS
        (True, {'a': 1})
        >>> pop_default(dict(a=1), 'b') #doctest: +ELLIPSIS
        (None, {'a': 1})
        >>> pop_default(dict(a=1), 'a') #doctest: +ELLIPSIS
        (1, {})

    Args:
        data: data
        key: key
        default: default

    Returns:
        tuple[Any, dict]:
    """
    try:
        value = data.pop(key)
    except KeyError:
        value = default
    return value, data


def prefix_suffix(string: str, fix: str, add: bool = True, prefix: bool = True, separator: str = '_') -> str:
    """
    Adds or removes prefix with separator from string.

    Examples:
        >>> from bapy import prefix_suffix
        >>> prefix_suffix('open', 'scan')
        'scan_open'
        >>> prefix_suffix('open', 'scan', prefix=False)
        'open_scan'
        >>> prefix_suffix('scan_open', 'open', add=False, prefix=False)
        'scan'

    Args:
        string: To add or remove.
        fix: prefix or suffix.
        add: add prefix/suffix or remove.
        prefix: True for prefix and False for suffix.
        separator: separator between prefix/suffix and string.

    Returns:

    """
    if add:
        return f'{fix}{separator}{string}' if prefix else f'{string}{separator}{fix}'
    return string.removeprefix(f'{fix}{separator}') if prefix else string.removesuffix(f'{separator}{fix}')


def print_modules(p: str):
    p = importlib.import_module(p)
    # noinspection PydanticTypeChecker
    cprint(mod_name(p))
    # noinspection PyUnresolvedReferences
    for mod in p._modules:
        if mod._isPackage:
            print_modules(mod)
        else:
            # noinspection PyCallingNonCallable
            cprint(mod_name(mod))


@app.command(context_settings=appcontext)
def pypifree(name: str, stdout: bool = False) -> bool:
    """
    Pypi name available.

    Examples:
        >>> assert pypifree('common') is False
        >>> assert pypifree('sdsdsdsd') is True

    Args:
        name: package.
        stdout: stdout.

    Returns:
        bool: True if available.
    """
    r = requests.get(f'https://pypi.org/pypi/{name}/json')

    if r:
        if stdout:
            red('Taken')
        return False
    else:
        if stdout:
            green('Available')
        return True


def rename_keys(mydict: dict, rename_map: dict) -> dict:
    for current_name, new_name in rename_map.items():
        if mydict.get(current_name) is not None:
            mydict[new_name] = mydict[current_name]
            del mydict[current_name]
    return mydict


def reverse_dict(data: dict) -> dict:
    """
    Reverse a Dict.

    Args:
        data: data

    Returns:
        dict:
    """
    keys_list = list(map(lambda k: k, data))
    reverse_key_list = keys_list[::-1]
    reverse_d = dict()
    i = 0
    while i < len(reverse_key_list):
        key = reverse_key_list[int(i)]
        reverse_d[key] = data[key]
        i += 1
    if len(reverse_d) > 0:
        return reverse_d


@app.command(context_settings=appcontext)
def secrets():
    """Secrets Update."""
    dist = distro.LinuxDistribution().info()['id']
    if dist == 'darwin':
        os.system(f'secrets-push.sh')
    elif dist == 'Kali':
        os.system(f'secrets-pull.sh')


def setuptools_script_install_dir():
    dist = setuptools.Distribution({'cmdclass': {'install': SetUpToolsScriptPath}})
    dist.dry_run = True  # not sure if necessary, but to be safe
    dist.parse_config_files()
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return Path(dist.install_scripts)


def sub_run(command: str = None, arguments: tuple = tuple()) -> Any:
    """
    Subprocess run.

    Args:
        command: os command to run.
        arguments: os command arguments.

    Returns:
        Union[subprocess.CompletedProcess[Str], subprocess.CompletedProcess]:
    """
    try:
        return subprocess.run([command, *arguments], stdout=subprocess.PIPE, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        repr(e)


def sub_run_sys(command: str = None, arguments: tuple = tuple()) -> int:
    """
    Subprocess run with the same interpreter as the module has been invoked.

    Args:
        command: command to run.
        arguments: command arguments.

    Returns:
        int:
    """
    try:
        ret = subprocess.check_call([sys.executable, '-m', command, *arguments])
        return ret
    except subprocess.CalledProcessError as e:
        repr(e)


def tasks(count: bool = False, find: str = False, name: str = False,
          state: TasksLiteral = None) -> Union[dict, str, TasksNamed]:
    ts = asyncio.all_tasks() if aioloop() else dict()
    rv = {task_state: {task.get_name(): task for task in ts if task._state == task_state.upper()}
          for task_state in TasksNamed._fields}

    if state:
        return rv.get(state, dict())
    elif count:
        return TasksNamed(*[len(rv.get(task_state, 0)) for task_state in TasksNamed._fields])
    elif find:
        return {name: task for name, task in rv[tasks_named.pending].items() if find in name}
    elif name:
        for task_state in TasksNamed._fields:
            if name in rv.get(task_state).keys():
                return task_state
    return TasksNamed(*[rv.get(task_state, dict()) for task_state in TasksNamed._fields])


def to_dict_or_list(data: Union[dict, list], name: str = None) -> Union[dict, list]:
    """
    Converts dictionaries to list and list of dicts to dicts.

    Args:
        data: data.
        name: key name for the dict key to add for list or to delete for dict.

    Returns:
        Union[dict, list]
    """
    if isinstance(data, dict):
        rv = list()
        for key, value in data.items():
            if isinstance(value, dict):
                value[name] = key
            else:
                value = {key: value}
            rv.append(value)
    else:
        rv = dict()
        for item in data:
            if isinstance(item, dict):
                if key := item.get(name):
                    del item[key]
                    rv |= {key: item}
    return rv


def trace(frame, evnt, args):
    """
    Examples:
        sys.settrace(trace)

    Args:
        frame:
        evnt:
        args:

    Returns:

    """
    frame.f_trace_opcodes = True
    stack = traceback.extract_stack(frame)
    pad = "   " * len(stack) + "|"
    if evnt == 'opcode':
        with io.StringIO() as out:
            dis.disco(frame.f_code, frame.f_lasti, file=out)
            lines = out.getvalue().split('\\n')
            [print(f"{pad}{l}") for l in lines]
    elif evnt == 'call':
        print(f"{pad}Calling {frame.f_code}")
    elif evnt == 'return':
        print(f"{pad}Returning {args}")
    elif evnt == 'line':
        print(f"{pad}Changing line to {frame.f_lineno}")
    else:
        print(f"{pad}{frame} ({evnt} - {args})")
    print(f"{pad}----------------------------------")
    return trace


def true_bool(value: Union[str, bool] = None, none_as_false: bool = True) -> Optional[bool]:
    """
    Return a bool for the arg.

    Args:
        value: value
        none_as_false: returns False if None or None.

    Returns:
        Optional[bool]:
    """
    if isinstance(value, bool):
        return value
    if value is None and not none_as_false:
        return None
    if isinstance(value, str):
        value = value.lower()
    if value in ('yes', 'on', '1', 'true', 1):
        return True
    return False


@app.command(context_settings=appcontext)
def tty_max(stdout: bool = False) -> int:
    """
    Max tty width.

    Args:
        stdout: stdout.

    Returns:
        int:
    """
    try:
        tty_max_width = shutil.get_terminal_size().columns
    except OSError:
        tty_max_width = 80
    if stdout:
        cprint(tty_max_width)
    return tty_max_width


def upcase_values(mydict: dict, keys: list = None) -> dict:
    if keys is None:
        keys = []
    for key in keys:
        value = mydict.get(key)
        if value is not None:
            mydict[key] = value.upper()
    return mydict


def upgrade_message(p: str, out: bool = False):
    """
    Prints message to user if package must be upgraded.

    Args:
        p: package.
        out: exit.
    """
    upgrade, current, latest = package_info(p)
    latest = package_latest(p)
    if latest != current:
        sty.fg.orange = sty.Style(sty.RgbFg(255, 150, 50))
        print(sty.fg.orange + f'Please upgrade: {p} ({latest})' + sty.fg.rs)
        print(f'  INSTALLED: {current}')
        print(f'  LATEST:    {latest}')
        print(sty.fg.orange + f'python3 -m pip install --upgrade {p}' + sty.fg.rs)
        print()
    if out:
        sys.exit(1)


def upper_prefix(data: Union[dict, list, set, str, tuple] = None, *, prefix: str = None,
                 envs: environs.Env = None) -> Optional[Union[dict, list, set, str, tuple]]:
    """
    Dict/List/Tuple Upper Items/Keys and Prefix Add.

    Examples:
        >>> upper_prefix()
        >>> pfx = 'repo'
        >>> tests = {'first': 1, 'second': 2}
        >>> upper_prefix(prefix=pfx)
        'REPO_'
        >>> upper_prefix(tests)
        {'FIRST': 1, 'SECOND': 2}
        >>> upper_prefix(tests, prefix=pfx)
        {'REPO_FIRST': 1, 'REPO_SECOND': 2}
        >>> data_new = tuple(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ('REPO_FIRST', 'REPO_SECOND')
        >>> data_new = list(tests.keys())
        >>> upper_prefix(data_new, prefix=pfx)
        ['REPO_FIRST', 'REPO_SECOND']
        >>> upper_prefix('first', prefix=pfx)
        'REPO_FIRST'

    Args:
        data: data to upper and to add prefix.
        prefix: prefix to add.
        envs: `environs.Env` file.

    Returns:
        Optional[Union[dict, list, set, str, tuple]]:
    """

    def get_prefix(v: str):
        p = f'{prefix.upper()}_' if prefix and not prefix.endswith('_') else prefix
        return f'{p.upper()}{v.upper()}' if prefix else v.upper()

    if data is None and prefix and envs is None:
        return get_prefix(str())
    if isinstance(data, dict):
        return {get_prefix(key): value for key, value in data.items()}
    else:
        for item in (list, set, tuple):
            if isinstance(data, item):
                if envs is None:
                    return item(get_prefix(var) for var in data)
                else:
                    return {var: envs(get_prefix(var), None) for var in data}
        if isinstance(data, str):
            return get_prefix(data)


def value_from_dict(data: MutableMapping, key: Any = None, first: bool = True) -> Union[Any, Generator[Any]]:
    """
    Get values from dict.

    Args:
        data: dict.
        key: key or keys to get values, default IP keys.
        first: get the first value or all.

    Returns:
        Union[Any, Generator[Any]]:
    """
    key = iter_split(key) if key else ['addr', 'exploded', '_id', '_ip', 'ip', 'IPv4']
    for item in key:
        if rv := dpath.util.values(data, f'**/{item}', dirs=False):
            if first:
                return rv[0]
            else:
                yield rv


def vars_to_dict(search_dict: dict, variables: Union[str, list, dict]) -> dict:
    """
    List or string words to dict with vars and values from dict.

    Args:
        search_dict: search_dict
        variables: variables

    Returns:
        dict:
    """
    if isinstance(variables, str):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in variables.split()}
    elif isinstance(variables, list):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in variables}
    elif isinstance(variables, dict):
        return {var: search_dict.get(var, '') if '.' not in var else getattr(
            search_dict.get(var.split('.')[0]), var.split('.')[1], '') for var in list(variables)}


@app.command(context_settings=appcontext, name='v')
def _version():
    """Version."""
    typer.echo(__version__)
    raise typer.Exit()


# <editor-fold desc="Echo">
@app.command(context_settings=appcontext)
def black(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Black.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='black', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def red(msg: str, bold: bool = False, underline: bool = False,
        blink: bool = False, err: bool = True, e: bool = True) -> None:
    """
    Red.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='red', err=err)
    if e:
        sys.exit(1)


@app.command(context_settings=appcontext)
def green(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Green.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='green', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def yellow(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = True, e: bool = False) -> None:
    """
    Yellow.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='yellow', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def blue(msg: str, bold: bool = False, underline: bool = False,
         blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Blue.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='blue', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def magenta(msg: str, bold: bool = False, underline: bool = False,
            blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Magenta.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='magenta', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def cyan(msg: str, bold: bool = False, underline: bool = False,
         blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Cyan.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='cyan', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def white(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    White.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='white', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def bblack(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Black.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_black', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def bred(msg: str, bold: bool = False, underline: bool = False,
         blink: bool = False, err: bool = True, e: bool = True) -> None:
    """
    Bred.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_red', err=err)
    if e:
        sys.exit(1)


@app.command(context_settings=appcontext)
def bgreen(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bgreen.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_green', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def byellow(msg: str, bold: bool = False, underline: bool = False,
            blink: bool = False, err: bool = True, e: bool = False) -> None:
    """
    Byellow.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_yellow', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def bblue(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bblue.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_blue', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def bmagenta(msg: str, bold: bool = False, underline: bool = False,
             blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bmagenta.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_magenta', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def bcyan(msg: str, bold: bool = False, underline: bool = False,
          blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bcyan.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_cyan', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def bwhite(msg: str, bold: bool = False, underline: bool = False,
           blink: bool = False, err: bool = False, e: bool = False) -> None:
    """
    Bwhite.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='bright_white', err=err)
    if e:
        sys.exit(0)


@app.command(context_settings=appcontext)
def reset(msg: str = str(), bold: bool = False, underline: bool = False, blink: bool = False, err: bool = False,
          e: bool = False) -> None:
    """
    Reset.

    Args:
        msg: msg
        bold: bold
        underline: underline
        blink: blink
        err: err
        e: e
    """
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True, fg='reset', err=err)
    if e:
        sys.exit(0)


# </editor-fold>


Py(exception=(not Py.PY39, not Py.PY310))

setup_bapy = Caller(filename=__file__, setup=True)
setup_package = Caller(setup=True)
logger = setup_bapy.log
