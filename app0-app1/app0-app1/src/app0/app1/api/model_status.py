"""
App0Att Clients: client-get
"""
from typing import Optional, Union

from app0.admin.client import Client
from app0.app1.services.client_services import get_client
from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (Client, "Object"),
        403: (HttpRespInfo, "Operation forbidden"),
        404: (HttpRespInfo, "Object not found")
    }
)


async def run(payload: None, context: EventContext,
              obj_id: str = None) -> Optional[Union[Client, HttpRespInfo]]:
    es = db(context.env)
    if obj_id:
        return await get_client(es, obj_id)
    return None


async def __postprocess__(payload: Optional[Union[Client, HttpRespInfo]], context: EventContext,
                          response: PostprocessHook) -> Union[Client, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    if payload is None:
        response.status = 404
        return "Object not found"
    return payload
