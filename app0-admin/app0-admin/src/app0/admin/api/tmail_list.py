"""
Platform Tmails: tmail-list
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Expr, Query, SearchResults, db
from app0.admin.services import ROLE_ADMIN
from app0.admin.services.tmail_services import get_tmails

__steps__ = ['run']

__api__ = event_api(
    payload=(Query, "Filters to search"),
    responses={
        200: (SearchResults, "List of results")
    }
)


async def run(payload: Query, context: EventContext) -> SearchResults:
    es = db(context.env)
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        owner_id = context.auth_info['payload'].get('owner_id', 'noauth')
        # if not admin list by company / noauth return []
        payload.flts['owner_id'] = Expr(eq=owner_id)
    results = await get_tmails(es, payload)
    return SearchResults(results=[Payload.to_obj(result) for result in results])
