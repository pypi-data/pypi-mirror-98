# coding=utf-8
import asyncio
import inspect

from bapy import Base
from bapy import Caller


def exclude(d, data_attrs: tuple[str, tuple] = None):
    if isinstance(d, str):
        if d.startswith('__'):
            return True

    if data_attrs:
        if data_attrs[0] not in data_attrs[1]:
            return True

    if any([inspect.ismodule(d), inspect.isroutine(d), isinstance(d, property)]):
        return True

# v = {
#     'open': {
#         'ip': {},
#         'sctp': {},
#         'tcp': {
#             80: {'open': True, 'script': {}, 'service': 'http'},
#             443: {'open': True, 'script': {}, 'service': 'https'}
#         },
#         'udp': {}
#     },
#     'filtered': {
#         'ip': {},
#         'sctp': {1: 'http'},
#         'tcp': {
#             80: {'open': True, 'script': {}, 'service': 'http'},
#             443: {'open': True, 'script': {}, 'service': 'https'}
#         },
#         'udp': {
#             80: {'open': True, 'script': {}, 'service': 'https'},
#             72: {'open': True, 'script': {'a': 4}, 'service': 'https'}
#         }
#     }
# }
# ic(Nested(v, 0, 'service'))
# assert not Nested(v, 0, 'service').values('x')
# assert Nested(v, 0, 'service').exclude('service')
# assert not dpath.util.search(Nested(v, 0, 'service').run(), '**/service')
# assert not dpath.util.search(Nested(v, 0, values='http').run(), '**', afilter=lambda x: 'http' == x)
# assert not dpath.util.search(Nested(v, 0, 'service', values='http').run(), '**', afilter=lambda x: 'http' == x)


# noinspection PyUnusedLocal
def arg(b, x=1, *args, **kwargs):
    return Caller(depth=1, index=1)


def test_caller():
    class A(Base):
        g = 1

        def __init__(self):
            super().__init__()
            self.a_1 = 1

        def a1(self):
            self.a_1 = 2
            index = 2
            c = Caller(callervars=True, depth=2, glob=True, index=index, loc=True)
            assert not c.coro
            assert c.function == 'test_caller'
            assert c.qual == 'test_caller'

        async def c1(self):
            index = 2
            c = Caller(callervars=True, index=index)
            if c.function == '_run':
                assert not c.coro
                assert not c.vars.glob
                assert not c.vars.loc
            if c.function == 'f1':
                assert c.coro
            self.d1()
            return c

        @classmethod
        def d1(cls):
            index = 2
            c = Caller(callervars=True, index=index)
            if c.function == 'c1':
                assert c.coro
                assert 'Task' in c.task
            return c

        @property
        async def f1(self):
            index = 2
            c = Caller(callervars=True, index=index)
            await self.c1()
            return c

    obj = A()
    obj.a1()
    asyncio.run(obj.c1(), debug=True)


def test_arg():
    arg_caller_local = arg(2)
    assert arg_caller_local.function == arg.__name__
    assert arg_caller_local.coro is None
    assert arg_caller_local.args == {'b': 2, 'x': 1}
    assert arg(3, 7, 9).args == {'args': (9,), 'b': 3, 'x': 7}
    assert arg(3, 7, 9, first=2, second=3).args == {'args': (9,), 'b': 3, 'first': 2, 'second': 3, 'x': 7}
    assert arg(3, 8, 7, first=2, second=3).args == {'args': (7,), 'b': 3, 'first': 2, 'second': 3, 'x': 8}
    assert arg(3, 8, first=2, second=3).args == {'b': 3, 'first': 2, 'second': 3, 'x': 8}
