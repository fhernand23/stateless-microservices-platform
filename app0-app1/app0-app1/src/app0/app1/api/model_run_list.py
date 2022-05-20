"""
App0Att Clients: client-list
{"flts": {"company.name": {"eq": "Titanic"}}}
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook, PreprocessHook
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Expr, Query, SearchResults, db
from app0.app1.services.client_services import get_clients

__steps__ = ['run']

__api__ = event_api(
    payload=(Query, "Filters to search"),
    responses={
        200: (SearchResults, "List of results"),
        403: (str, "Unauthorized request")
    }
)


# pylint: disable=invalid-name
async def __preprocess__(payload: Query, context: EventContext,
                         request: PreprocessHook) -> Query:
    owner_id: Optional[str] = context.auth_info['payload'].get('owner_id')
    payload.flts['owner_id'] = Expr(eq=owner_id)

    return payload


async def run(payload: Query, context: EventContext) -> Optional[SearchResults]:
    es = db(context.env)
    results = await get_clients(es, payload)
    return SearchResults(results=[Payload.to_obj(result) for result in results])


async def __postprocess__(payload: Optional[SearchResults],
                          context: EventContext,
                          response: PostprocessHook) -> Union[SearchResults, str]:
    if payload:
        return payload
    response.status = 403
    return 'Unauthorized request'
