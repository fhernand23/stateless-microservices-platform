"""
Platform Subscriptions: subscription-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.services.subscription_services import get_subscription
from app0.admin.subscription import Subscription

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (Subscription, "Subscription"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, obj_id: str) -> Optional[Subscription]:
    es = db(context.env)
    if obj_id:
        return await get_subscription(es, obj_id)

    return None


async def __postprocess__(payload: Optional[Subscription], context: EventContext,
                          response: PostprocessHook) -> Union[Subscription, str]:
    if payload is None:
        response.status = 404
        return "Subscription not found"
    return payload
