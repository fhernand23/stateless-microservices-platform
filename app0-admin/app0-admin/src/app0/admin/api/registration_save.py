"""
Platform Registrations: registration-save
"""
from typing import Optional, Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.registration import Registration
from app0.admin.services import (ACT_REGISTRATION_DELETE, IDX_REGISTRATION,
                                  ROLE_ADMIN)
from app0.admin.services.registration_services import save_registration

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(Registration, "Object Info"),
    responses={
        200: (Registration, "Object updated"),
        400: (str, "Request error"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Registration, context: EventContext,
              action: Optional[str] = None) -> Union[Registration, HttpRespInfo]:
    """
    Save Registration
    """
    es = db(context.env)
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')
    if not action:
        await save_registration(es, payload)
    elif action == ACT_REGISTRATION_DELETE:
        await _registration_delete(es, payload)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[Registration, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[Registration, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _registration_delete(es, registration: Registration):
    # delete related info
    await es[IDX_REGISTRATION].delete_one({'_id': ObjectId(registration.id)})
