"""
Platform Roles: role-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.app import AppRole
from app0.admin.http import HttpRespInfo
from app0.admin.db import db
from app0.admin.services.app_services import save_role
from app0.admin.services import ROLE_ADMIN

__steps__ = ['run']

__api__ = event_api(
    payload=(AppRole, "Role Info"),
    responses={
        200: (AppRole, "Role updated"),
        403: (str, "Forbidden")
    }
)


async def run(payload: AppRole,
              context: EventContext) -> Union[AppRole, HttpRespInfo]:
    es = db(context.env)
    # check user admin
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')
    await save_role(es, payload)

    return payload


async def __postprocess__(payload: Union[AppRole, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[AppRole, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
