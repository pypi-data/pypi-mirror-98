# -*- coding: utf-8 -*-
__all__ = [
    'NmapCommandPortTyping',
    'NmapCommandScriptTyping',
    'ProtoStatus',
]

from typing import Any
from typing import Literal
from typing import NamedTuple
from typing import Optional
from typing import Union

NmapCommandPortTyping = Optional[Union[Literal['-'], str, int]]
NmapCommandScriptTyping = Union[Literal['complete'], str]
ProtoStatus = NamedTuple('ProtoStatus', ip=Any, port=Any, proto=Any, open=Any)
