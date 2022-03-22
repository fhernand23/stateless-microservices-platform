"""
Platform Registrations: registration-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.registration import Registration
from app0.admin.services.registration_services import get_registration

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (Registration, "Registration"),
        404: (str, "Object not found")
    }
)


async def run(payload: None,
              context: EventContext,
              obj_id: str) -> Optional[Registration]:
    es = db(context.env)
    if obj_id:
        return await get_registration(es, obj_id)

    return None


async def __postprocess__(payload: Optional[Registration], context: EventContext,
                          response: PostprocessHook) -> Union[Registration, str]:
    if payload is None:
        response.status = 404
        return "Registration not found"
    return payload
