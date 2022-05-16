"""
Platform Roles: role-list
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query, SearchResults, db
from app0.admin.services.app_services import get_roles

__steps__ = ['run']
__api__ = event_api(
    payload=(Query, "Filters to search"),
    responses={
        200: (SearchResults, "List of results")
    }
)


async def run(payload: Query, context: EventContext) -> SearchResults:
    es = db(context.env)
    results = await get_roles(es, payload)
    return SearchResults(results=[Payload.to_obj(result) for result in results])
