"""
Platform Notifications: notification-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.notification import Notification
from app0.admin.services.notification_services import get_notification

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (Notification, "Notification"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, obj_id: str) -> Optional[Notification]:
    es = db(context.env)
    if obj_id:
        return await get_notification(es, obj_id)

    return None


async def __postprocess__(payload: Optional[Notification], context: EventContext,
                          response: PostprocessHook) -> Union[Notification, str]:
    if payload is None:
        response.status = 404
        return "Notification not found"
    return payload
