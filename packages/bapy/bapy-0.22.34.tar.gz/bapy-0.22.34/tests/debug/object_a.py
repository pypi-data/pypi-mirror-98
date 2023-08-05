# -*- coding: utf-8 -*-
from object_main import a, integer, dictionary, string
from bapy.utils import ic

ic('1: object_a.py', id(a), a.a)
print()

a.a = '2: object_a.py'
ic('2: object_a.py', id(a), a.a)
print()


value_a = '3: object_a.py'


class B:
    b = a   # NO CHANGE ID
    
    def __init__(self):
        self.b.a = value_a


b = B()
ic('3: object_a.py', id(a), a.a, id(b.b), b.b.a)
print()


ic('4: object_a.py', id(integer), integer)
ic('4: object_a.py', id(dictionary), dictionary)
ic('4: object_a.py', id(string), string)
print()

integer_a = integer  # CHANGE ID
integer_a += 1
dictionary_a = dictionary  # NO CHANGE ID
dictionary_a['a'] = 'a'
string_a = string  # CHANGE ID
string_a = 'a'

ic('4: object_a.py', id(integer), integer, id(integer_a), integer_a)
ic('4: object_a.py', id(dictionary), dictionary, id(dictionary_a), dictionary_a)
ic('4: object_a.py', id(string), string, id(string_a), string_a)
print()
