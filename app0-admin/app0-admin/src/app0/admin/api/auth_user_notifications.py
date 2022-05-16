"""
Platform Users: auth-user-notifications
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Expr, Query, SearchResults, db
from app0.admin.services.notification_services import get_notifications

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (SearchResults, "List of results")
    }
)


async def run(payload: None, context: EventContext) -> SearchResults:
    es = db(context.env)
    usr_id = context.auth_info['payload'].get('id', 'noauth')
    query = Query(flts={'dest_user_id': Expr(eq=usr_id)}, max_items=100)
    results = await get_notifications(es, query)
    return SearchResults(results=[Payload.to_obj(result) for result in results])
