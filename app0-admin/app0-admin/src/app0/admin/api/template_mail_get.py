"""
Platform TemplateMails: tmail-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.services.template_mail_services import get_tmail
from app0.admin.template_mail import TemplateMail

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (TemplateMail, "TemplateMail"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, obj_id: str) -> Optional[TemplateMail]:
    es = db(context.env)
    if obj_id:
        return await get_tmail(es, obj_id)

    return None


async def __postprocess__(payload: Optional[TemplateMail], context: EventContext,
                          response: PostprocessHook) -> Union[TemplateMail, str]:
    if payload is None:
        response.status = 404
        return "TemplateMail not found"
    return payload
