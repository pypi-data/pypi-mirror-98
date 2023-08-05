# -*- coding: utf-8 -*-
import contextvars
from contextvars import copy_context
from contextvars import ContextVar

from typing import Any
from typing import Type
from typing import Union


class Context(contextvars.Context):

    def __init__(self):
        super(Context, self).__init__()

    def __call__(self, name: Union[str, ContextVar], default: Any = None, cls: Type = Any) -> Union[ContextVar, Any]:
        if isinstance(name, str):
            # noinspection PyUnresolvedReferences
            rv: ContextVar[Any] = ContextVar(name)
            if cls:
                # noinspection PyUnresolvedReferences
                rv: ContextVar[cls] = ContextVar(name)

            ctx = copy_context()
            for var in ctx.keys():
                if var.name == name:
                    rv = var
                    if cls:
                        # noinspection PyUnresolvedReferences
                        rv: ContextVar[cls] = var
                    break
        else:
            rv = copy_context().get(name)
        return rv

    def set(self, name: Union[str, ContextVar]):
        pass
