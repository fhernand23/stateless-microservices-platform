"""
Platform Roles: role-save
"""
from typing import Union, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_extra_logger

from app0.admin.app import AppRole
from app0.admin.http import HttpRespInfo
from app0.admin.db import db
from app0.admin.services.app_services import save_role
from app0.admin.services import ROLE_ADMIN, ACT_ROLE_ARCHIVE, ACT_ROLE_UNARCHIVE, IDX_ROLE

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(AppRole, "Role Info"),
    responses={
        200: (AppRole, "Role updated"),
        400: (str, "Request error"),
        403: (str, "Forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: AppRole, context: EventContext,
              action: Optional[str] = None) -> Union[AppRole, HttpRespInfo]:
    """Role save and actions"""
    es = db(context.env)
    # check user admin
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')

    if not action:
        await save_role(es, payload)
    elif action == ACT_ROLE_ARCHIVE:
        await _role_archive(es, payload, context)
    elif action == ACT_ROLE_UNARCHIVE:
        await _role_unarchive(es, payload, context)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[AppRole, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[AppRole, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _role_archive(es, app_role: AppRole, context: EventContext):
    logger.info(context, f"Archiving role {app_role}")
    await es[IDX_ROLE].update_one({'_id': ObjectId(app_role.id)}, {'$set': {'enabled': False}})


async def _role_unarchive(es, app_role: AppRole, context: EventContext):
    logger.info(context, f"Unarchiving role {app_role}")
    await es[IDX_ROLE].update_one({'_id': ObjectId(app_role.id)}, {'$set': {'enabled': True}})
