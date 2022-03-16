"""
db module

Helpers for common related DB operations.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from hopeit.dataobjects import dataclass, dataobject
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

__all__ = ['db']


def db(env: dict):
    """
    Return a reference to collection (no IO)
    """
    client = AsyncIOMotorClient(env['mongodb']['conn_str'])
    connection = client[env['mongodb']['dbname']]
    return connection


@dataobject
@dataclass
class Expr:
    eq: Optional[str] = None
    elem_match: Optional[Dict[str, str]] = None
    in_: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    not_eq: Optional[str] = None


@dataobject
@dataclass
class FldSrt:
    """Field order (1 asc, -1 desc) tuple"""
    fld: str
    rdr: int = 1


@dataobject
@dataclass
class Query:
    """
    Query handler
    """
    flts: Dict[str, Expr]
    flts_or: bool = True
    enabled: bool = True
    max_items: int = 100
    text: Optional[str] = None
    sort: Optional[FldSrt] = None

    def find_qry(self) -> dict:
        """
        Process filter and return valid ES Query
        """
        exp: List[Dict] = []
        for field, expr in self.flts.items():
            # TODO ver que hay para booleans
            if expr.eq:
                exp.append({field: {'$eq': expr.eq}})
            elif expr.elem_match:
                for field2, value in expr.elem_match.items():
                    exp.append({field: {'$elemMatch': {field2: {'$eq': value}}}})
            # elif (expr.from_date is not None) and (expr.to_date is not None):
            #     exp.append(f'({prefix}.{field}:[{expr.from_date.isoformat()} TO {expr.to_date.isoformat()}])')
            # elif expr.from_date is not None:
            #     exp.append(f'({prefix}.{field}:[{expr.from_date.isoformat()} TO *])')
            # elif expr.to_date is not None:
            #     exp.append(f'({prefix}.{field}:[* TO {expr.to_date.isoformat()}])')
            # if expr.not_eq is not None:
            #     exp.append(f'(NOT {prefix}.{field}:{expr.not_eq})')
        if len(exp) == 1:
            return exp[0]
        return {'$or' if self.flts_or else '$and': exp}


@dataobject
@dataclass
class SearchResults:
    results: List[Union[Dict[Any, Any], List[Any]]]
    total: int = 0
    page: int = 0
    page_size: int = 0
    offset: Optional[int] = None
    next_page: Optional[int] = None
    next_offset: Optional[int] = None
