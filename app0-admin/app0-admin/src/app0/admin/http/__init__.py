"""
http module
"""
from typing import Any, Dict
from hopeit.dataobjects import dataclass, dataobject


@dataobject
@dataclass
class HttpRespInfo:
    """
    HTTP response code with message
    """
    code: int
    msg: str


@dataobject
@dataclass
class Dto:
    """
    Generic object with a Dict with values for return in hopeit.engine
    """
    o: Dict[str, Any]
