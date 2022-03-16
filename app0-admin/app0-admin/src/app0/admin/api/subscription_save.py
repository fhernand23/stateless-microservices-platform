"""
Platform Subscriptions: subscription-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services.subscription_services import save_subscription
from app0.admin.subscription import Subscription

__steps__ = ['run']

__api__ = event_api(
    payload=(Subscription, "Object Info"),
    responses={
        200: (Subscription, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Subscription, context: EventContext) -> Union[Subscription, HttpRespInfo]:
    es = db(context.env)
    await save_subscription(es, payload)

    return payload


async def __postprocess__(payload: Union[Subscription, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[Subscription, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
