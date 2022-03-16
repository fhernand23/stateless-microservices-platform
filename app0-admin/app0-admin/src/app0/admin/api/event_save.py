"""
Platform Events: event-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.event import Event
from app0.admin.http import HttpRespInfo
from app0.admin.services.event_services import save_event

__steps__ = ['run']

__api__ = event_api(
    payload=(Event, "Object Info"),
    responses={
        200: (Event, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Event, context: EventContext) -> Union[Event, HttpRespInfo]:
    es = db(context.env)
    if not payload.owner_id:
        payload.user_id = context.auth_info['payload'].get('user', 'noauth')
        payload.user_name = context.auth_info['payload'].get('fullname', 'Noauth User')
        payload.owner_id = context.auth_info['payload'].get('owner_id', 'noauth')
        payload.owner_name = context.auth_info['payload'].get('owner_name', 'noauth')
    await save_event(es, payload)
    return payload


async def __postprocess__(payload: Union[Event, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[Event, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
