"""
Platform TemplateMails: tmail-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services.template_mail_services import save_template_mail
from app0.admin.template_mail import TemplateMail

__steps__ = ['run']

__api__ = event_api(
    payload=(TemplateMail, "Object Info"),
    responses={
        200: (TemplateMail, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: TemplateMail, context: EventContext) -> Union[TemplateMail, HttpRespInfo]:
    es = db(context.env)
    await save_template_mail(es, payload)
    return payload


async def __postprocess__(payload: Union[TemplateMail, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[TemplateMail, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
