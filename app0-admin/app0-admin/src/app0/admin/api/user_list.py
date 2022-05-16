"""
Platform Users: user-list
"""
from typing import List, Optional, Tuple
from functools import partial

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects.payload import Payload

from app0.admin.user import User
from app0.admin.db import db, Query, SearchResults, filtered_search
from app0.admin.services import IDX_USER

es: Optional[AsyncIOMotorClient] = None

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('page', Optional[int], "Page number 1=first page"),
        ('page_size', Optional[int], "Page size")
    ],
    payload=(Query, "Filters to search"),
    responses={
        200: (SearchResults, "List of User")
    }
)


async def __init_event__(context: EventContext):
    global es
    if es is None:
        es = db(context.env)
        # es[IDX_USER].createIndex({'surname': "text", "firstname": "text", "email": "text"})


async def run(payload: Query, context: EventContext, page: int = 1, page_size: int = 20) -> SearchResults:
    assert es
    page, page_size = int(page), int(page_size)
    query_func = partial(_search_users, IDX_USER, payload)
    return await filtered_search(query_func, page, page_size)


async def _search_users(index: str, query: Query, page: int = 0, page_size: int = 20) -> Tuple[List[User], int]:
    """
    Returns a list of queried Users
    """
    assert es
    cursor: Optional[AsyncIOMotorCollection] = None
    assert query
    count: int
    sort_field = query.sort.field if query.sort else 'name'
    sort_order = query.sort.order if query.sort else 1

    if query.flts:
        search_query = query.find_qry()
        cursor = es[index].find(search_query)
        count = await es[index].count_documents(search_query)
    else:
        cursor = es[index].find()
        count = await es[index].estimated_document_count()

    cursor = cursor.sort(sort_field, sort_order)
    results = await cursor.skip((page)*page_size).to_list(length=page_size)

    return ([Payload.from_obj(doc, User) for doc in results], count)
