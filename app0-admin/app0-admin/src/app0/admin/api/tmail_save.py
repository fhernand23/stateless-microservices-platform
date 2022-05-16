"""
Platform Tmails: tmail-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services.tmail_services import save_tmail
from app0.admin.tmail import Tmail

__steps__ = ['run']

__api__ = event_api(
    payload=(Tmail, "Object Info"),
    responses={
        200: (Tmail, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Tmail, context: EventContext) -> Union[Tmail, HttpRespInfo]:
    es = db(context.env)
    await save_tmail(es, payload)
    return payload


async def __postprocess__(payload: Union[Tmail, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[Tmail, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
