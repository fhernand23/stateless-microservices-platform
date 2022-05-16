"""
Platform Plans: plan-list-enabled
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects.payload import Payload

from app0.admin.db import SearchResults, db
from app0.admin.services import IDX_PLAN
from app0.admin.subscription import AvailablePlan

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (SearchResults, "List of results")
    }
)


async def run(payload: None, context: EventContext) -> SearchResults:
    es = db(context.env)
    results = await get_plans_enabled(es)
    return SearchResults(results=[Payload.to_obj(result) for result in results])


async def get_plans_enabled(es) -> List[AvailablePlan]:
    """
    List of availables Plans
    """
    sort_fld = 'registration_order'
    sort_order = 1
    query = {'enabled': {'$eq': True}}
    cursor = es[IDX_PLAN].find(query).sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, AvailablePlan) for doc in await cursor.to_list(length=10)]
