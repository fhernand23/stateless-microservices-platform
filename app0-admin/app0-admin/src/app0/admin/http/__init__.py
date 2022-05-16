"""
http module
"""
from typing import Any, Dict
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


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


@dataobject
@dataclass
class CodeDescription:
    """
    Application return code with description
    """
    id: int = fd("Code Id")
    description: str = fd("Description")
