"""
Platform Roles: role-save
"""
from typing import Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.app import AppDef
from app0.admin.http import HttpRespInfo
from app0.admin.db import db
from app0.admin.services.app_services import save_app
from app0.admin.services import ROLE_ADMIN

__steps__ = ['run']

__api__ = event_api(
    payload=(AppDef, "App Info"),
    responses={
        200: (AppDef, "App updated"),
        403: (str, "Forbidden")
    }
)


async def run(payload: AppDef,
              context: EventContext) -> Union[AppDef, HttpRespInfo]:
    es = db(context.env)
    # check user admin
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')
    await save_app(es, payload)

    return payload


async def __postprocess__(payload: Union[AppDef, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[AppDef, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
