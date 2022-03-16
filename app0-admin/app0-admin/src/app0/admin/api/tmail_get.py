"""
Platform Tmails: tmail-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.services.tmail_services import get_tmail
from app0.admin.tmail import Tmail

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (Tmail, "Tmail"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, obj_id: str) -> Optional[Tmail]:
    es = db(context.env)
    if obj_id:
        return await get_tmail(es, obj_id)

    return None


async def __postprocess__(payload: Optional[Tmail], context: EventContext,
                          response: PostprocessHook) -> Union[Tmail, str]:
    if payload is None:
        response.status = 404
        return "Tmail not found"
    return payload
