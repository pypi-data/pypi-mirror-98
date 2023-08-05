# -*- coding: utf-8 -*-
from contextvars import Context
from contextvars import ContextVar
from contextvars import copy_context

from object_main import a, get_a, set_a, value_main, integer, get, dictionary, string, B
from bapy.utils import ic

# status.set(B())
status: ContextVar[B] = ContextVar('status')
entero: ContextVar[int] = ContextVar('status')

ctx: Context = copy_context()
ic(list(ctx.keys()))
print()

for var in ctx.keys():
    if var.name == 'status':
        status = var
        break

status_value = status.get()
ic(status_value)
print()

status_value.b = '1. object_b.py'
status.set(status_value)
ic(status.get())
print()

from object_main import status
ic(status.get())
print()

exit()
ic('1: object_b.py', id(a), a.a)
print()

from object_a import ic as ica
ica('2: object_b.py', id(a), a.a)
print()

get_a()
ica('3: object_b.py', id(a), a.a)
print()

from object_a import b
ica('4: object_b.py', id(a), a.a, id(b.b), b.b.a)
print()

get_a()
ica('5: object_b.py', id(a), a.a, id(b.b), b.b.a)
print()

from object_a import value_a
assert a.a == b.b.a == value_a
assert id(a.a) == id(b.b.a)


set_a()
ica('6: object_b.py', id(a), a.a, id(b.b), b.b.a)
assert a.a == b.b.a == value_main
assert id(a.a) == id(b.b.a)
print()


ic('7: object_b.py', id(integer), integer)
print()

from object_a import integer_a, dictionary_a, string_a

integer_main, dictionary_main, string_main = get()

ica('8: object_b.py', id(integer), integer, id(integer_a), integer_a, id(integer_main), integer_main)
ica('8: object_b.py', id(dictionary), dictionary, id(dictionary_a), dictionary_a, id(dictionary_main), dictionary_main)
ica('8: object_b.py', id(string), string, id(string_a), string_a, id(string_main), string_main)
print()

assert integer == integer_main
assert id(integer) == id(integer_main)
assert integer_a != integer_main
assert id(integer_a) == id(integer_main)


assert dictionary == dictionary_a == dictionary_main
assert id(dictionary) == id(dictionary_a) == id(dictionary_main)

assert string == string_main
assert id(string) == id(string_main)
assert string_a != string_main
assert id(string_a) == id(string_main)
