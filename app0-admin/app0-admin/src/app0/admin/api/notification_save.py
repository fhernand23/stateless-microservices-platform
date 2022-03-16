"""
Platform Notifications: notification-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.notification import Notification
from app0.admin.services.notification_services import save_notification

__steps__ = ['run']

__api__ = event_api(
    payload=(Notification, "Object Info"),
    responses={
        200: (Notification, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Notification, context: EventContext) -> Union[Notification, HttpRespInfo]:
    es = db(context.env)
    payload.user_id = context.auth_info['payload'].get('user', 'noauth')
    payload.user_name = context.auth_info['payload'].get('fullname', 'Noauth User')
    payload.owner_id = context.auth_info['payload'].get('owner_id', 'noauth')
    payload.owner_name = context.auth_info['payload'].get('owner_name', 'noauth')
    await save_notification(es, payload)
    return payload


async def __postprocess__(payload: Union[Notification, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[Notification, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
