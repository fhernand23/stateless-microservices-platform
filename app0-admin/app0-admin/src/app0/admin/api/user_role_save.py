"""
Platform Users: user-role-save
"""
from typing import Optional, Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_extra_logger

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services import (ACT_USERROLE_DELETE, IDX_USER_ROLE, ROLE_ADMIN)
from app0.admin.services.user_services import save_user_role
from app0.admin.user import UserAppRole

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(UserAppRole, "UserRole"),
    responses={
        200: (UserAppRole, "UserRole updated"),
        400: (str, "Request error"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: UserAppRole, context: EventContext,
              action: Optional[str] = None) -> Union[UserAppRole, HttpRespInfo]:
    """User save & actions"""
    es = db(context.env)
    # check user admin
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not Administrator')

    if not action:
        await save_user_role(es, payload)
    elif action == ACT_USERROLE_DELETE:
        await _user_role_delete(es, payload, context)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[UserAppRole, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[UserAppRole, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _user_role_delete(es, userrole: UserAppRole, context: EventContext):
    # check if user has employee_id & delete
    logger.info(context, f"Deleting userrole {userrole}")
    await es[IDX_USER_ROLE].delete_one({'_id': ObjectId(userrole.id)})
