"""
db module

Helpers for common related DB operations.
"""
from typing import Any, Dict, List, Optional, Union

from hopeit.dataobjects import dataclass, dataobject
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app0.admin import fd

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
    eq: Optional[str] = fd("Match str field equal to", default=None)
    eq_bool: Optional[bool] = fd("Match bool field equal to", default=None)
    elem_match: Optional[Dict[str, str]] = fd("Match at least one element of array field", default=None)
    text: Optional[str] = fd("Match text index", default=None)
    regex: Optional[str] = fd("Match field by regex", default=None)
    or_regex: Optional[Dict[str, str]] = fd("Match OR a list of fields by regex", default=None)
    # in_: Optional[List[str]] = None
    # from_date: Optional[datetime] = None
    # to_date: Optional[datetime] = None
    # not_eq: Optional[str] = fd("Event type", default=None)


@dataobject
@dataclass
class FieldSort:
    """Field order tuple"""
    field: str = fd("Field to order")
    order: int = fd("Type 1 asc, -1 desc", default=1)


@dataobject
@dataclass
class Query:
    """
    Query handler
    """
    flts: Dict[str, Expr]
    max_items: int = 100
    sort: Optional[FieldSort] = None

    def find_qry(self) -> dict:
        """
        Process filter and return valid Mongo Query
        """
        exp: List[Dict] = []
        for field, expr in self.flts.items():
            if expr.eq:
                exp.append({field: {'$eq': expr.eq}})
            elif expr.eq_bool:
                exp.append({field: {'$eq': expr.eq_bool}})
            elif expr.elem_match:
                for field2, value in expr.elem_match.items():
                    exp.append({field: {'$elemMatch': {field2: {'$eq': value}}}})
            elif expr.text:
                exp.append({'$text': {'$search': expr.text}})
            elif expr.regex:
                exp.append({field: {'$regex': expr.regex, '$options': 'i'}})
            elif expr.or_regex:
                exp.append(
                    {'$or': [{field2: {'$regex': value, '$options': 'i'}} for field2, value in expr.or_regex.items()]}
                )
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
        return {'$and': exp}


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


async def filtered_search(query_func, page: int, page_size: int, offset: int = 0) -> SearchResults:
    """
    Return a SearchResult
    param query_func: partial function
    param page: int Page Number
    param page_size: Number of returned pages
    param offset:
    """
    results: List[Union[Dict[Any, Any], List[Any]]] = []
    no_hits = False
    total_fetch, total, skip, page_count = 0, 0, 0, 0
    page_it = page - 1
    while (not no_hits) and len(results) < page_size:
        hits, total = await query_func(page_it, page_size)
        no_hits = len(hits) == 0
        page_count = 0
        for hit in hits:
            page_count += 1
            if skip < offset:
                skip += 1
            else:
                total_fetch += 1
                results.append(hit.to_dict())
                if len(results) >= page_size:
                    break
        if len(results) < page_size:
            page_it += 1

    return SearchResults(total=total, page=page, page_size=page_size, offset=offset,
                         next_page=(0 if no_hits else page_it+1 if page_count < page_size else page_it+2),
                         next_offset=(page_count if page_count < page_size else 0), results=results)
