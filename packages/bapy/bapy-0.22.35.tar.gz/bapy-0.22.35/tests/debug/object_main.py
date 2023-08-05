# -*- coding: utf-8 -*-
from __future__ import annotations
import dataclasses
from contextvars import Context
from contextvars import ContextVar
from contextvars import copy_context

from bapy.utils import ic

status: ContextVar[B] = ContextVar('status')

@dataclasses.dataclass
class B:
    _b: str = '1: object_main.py'

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value


status.set(B())
ctx: Context = copy_context()
ic(list(ctx.keys()))
print()

status_value = ctx.get(status)
status_value = ctx.context(status)
status_value.b = '2. object_main.py'
status.set(status_value)
ic(status.get())
print()

@dataclasses.dataclass
class A:
    _a: str = '1: utils.py'

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value


a = A()

ic('1: object_main.py', id(a), a.a)
print()


def get_a():
    ic('2: object_main.py', id(a), a.a)
    print()


value_main = '3: object_main.py'


def set_a():
    a.a = value_main
    ic('3: object_main.py', id(a), a.a)
    print()


integer = 1
dictionary = dict(main='main')
string = 'main'


def get():
    ic('4: object_main.py', id(integer), integer)
    ic('4: object_main.py', id(dictionary), dictionary)
    ic('4: object_main.py', id(string), string)
    print()
    return integer, dictionary, string
