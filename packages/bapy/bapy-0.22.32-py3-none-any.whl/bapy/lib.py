# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import enum
import functools
import json
import random
import socket
import time
import urllib.error
import warnings
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import cast
from typing import Coroutine
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Union

import pymongo.errors

from .enum import *
from .utils import *
from .utils import logger

__all__ = [
    'MinMax',
    'NapValue',
    'Nap',
]


MinMax = NamedTuple('MinMax', min=Union[float, int], max=Union[float, int])
NapValue = NamedTuple('NapValue', exceptions=Optional[Union[Any, tuple[Any]]], retries=int, timeout=MinMax)


class Nap(Enum):
    """Nap Helper Class."""
    HTTPJSON = NapValue((urllib.error.HTTPError, json.decoder.JSONDecodeError), 4, MinMax(2, 3))
    LOCK = NapValue(None, 0, MinMax(3, 5))
    MONGO = NapValue((socket.gaierror, pymongo.errors.ConnectionFailure, pymongo.errors.AutoReconnect,
                      pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.ConfigurationError,),
                     0, MinMax(7, 11))
    OSERROR = NapValue(OSError, 0, MinMax(0, 2))
    QUEUE = NapValue(None, 0, MinMax(2, 2))

    @property
    def time(self) -> Union[int, float]:
        return round(random.uniform(self.value.timeout.min, self.value.timeout.max), 2)

    def sleep(self) -> None:
        time.sleep(self.time)

    async def asleep(self) -> None:
        await asyncio.sleep(self.time)

    def retry_sync(self, value: NapValue = None) -> Any:
        """
        1 is like normal run withouth retry_sync.

        Args:
            value: value.

        Returns:
            Any:
        """
        value = value if value else self.value
        log = logger.child()

        def decorate(func):
            @functools.wraps(func)
            def loop(*args, **kwargs):
                called = Caller()
                log.debug(called=called, Start=func.__qualname__)
                count = 0
                while True if value.retries == 0 else count < value.retries:
                    try:
                        rv = func(*args, **kwargs)
                        log.debug(called=called, End=func.__qualname__)
                        return rv
                    except value.exceptions as exception:
                        count += 1
                        if count == value.retries:
                            raise exception
                        log.spam(called=called, Waiting=f'{func.__qualname__} | {exception}')
                        self.sleep()
                        continue

            return loop

        return decorate

    def retry_async(self, value: NapValue = None) -> Any:
        """
        1 is like normal run withouth retry_sync.

        Args:
            value: value.

        Returns:
            Any:
        """
        value = value if value else self.value
        log = logger.child()

        def decorate(func):
            @functools.wraps(func)
            async def loop(*args, **kwargs):
                called = Caller()
                if called.function == 'sem':
                    called = Caller(index=3)
                count = 0
                await log.adebug(called=called, Start=func.__qualname__)
                while True if value.retries == 0 else count < value.retries:
                    try:
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
                            await log.adebug(called=called, End=func.__qualname__)
                            return rv
                    except value.exceptions as exception:
                        count += 1
                        if count == value.retries:
                            raise exception
                        await log.aspam(called=called, Waiting=f'{func.__qualname__} | {exception}')
                        self.sleep()
                        continue

            return loop

        return decorate

#
# class SemEnum(Enum):
#
#     # noinspection PyUnusedLocal
#     def _generate_next_value_(self, start, count, last_values) -> dict[Priority, asyncio.Semaphore]:
#         return setup_bapy.env.sem[self.lower()]
#
#     def _msg(self, prefix: str = 'Waiting') -> dict:
#         return dict(called=self.call) | cast(Mapping, {prefix: self.func.__qualname__}) | dict(
#             Priority=self.priority.name, Using=self.using, Value=self._sem._value, Status=self.status) | (
#             dict(Running=Kill.count()) if self.name in Kill.count_values else dict())
#
#     # noinspection PyAttributeOutsideInit
#     async def sem(self, func: Union[Callable, Coroutine], /, *args, priority: Priority = Priority.LOW, **kwargs) -> Any:
#         """
#         Sem.
#
#         Args:
#             func: func.
#             priority: priority.
#             **kwargs: **kwargs.
#
#         Returns:
#             Any:
#         """
#         index = 3 if self.name == 'MONGO' else 2
#         self.call = Caller(index=index)
#         self.func = func
#         self.priority = priority
#         self._sem = self.value[Priority.LOW]
#         self.using = Priority.LOW.name
#         if self.priority == Priority.HIGH and self.value[Priority.LOW].locked():
#             self._sem = self.value[self.priority]
#             self.using = self.priority.name
#         log = logger.child()
#         await log.awarning(**self._msg())
#         async with self._sem:
#             await log.anotice(**self._msg('Acquired'))
#             with warnings.catch_warnings(record=False):
#                 warnings.filterwarnings('ignore', category=RuntimeWarning)
#                 warnings.showwarning = lambda *_args, **_kwargs: None
#                 obj = Obj(func)
#                 if obj.coroutinefunction:
#                     rv = await func(*args, **kwargs)
#                 elif obj.coroutine:  # includes property and coro.
#                     rv = await func
#                 elif obj.awaitable:
#                     rv = await func(*args, **kwargs)
#                 elif obj.routine:
#                     rv = func(*args, **kwargs)
#                 else:
#                     rv = func
#         await log.anotice(**self._msg('Released'))
#         return rv
#
#     @property
#     def high(self) -> dict[str, int]:
#         return self.value[Priority.HIGH]._value
#
#     @property
#     def low(self) -> dict[str, int]:
#         return self.value[Priority.LOW]._value
#
#     @property
#     def status(self) -> dict[str, int]:
#         return {priority.name: sem._value for priority, sem in self.value.items()}
#
#     @property
#     def total(self) -> dict[str, int]:
#         return {priority.name: sem._value for priority, sem in setup_bapy.sem[self.name].items()}
#
#
# class Sem(SemEnum):
#     MAX = enum.auto()
#     MONGO = enum.auto()
#     NMAP = enum.auto()
#     OS = enum.auto()
#     SSH = enum.auto()
#     PING = enum.auto()
#     SOCKET = enum.auto()
