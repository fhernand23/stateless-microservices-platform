"""
Platform Roles: role-save
"""
from typing import Union, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_extra_logger

from app0.admin.app import AppDef
from app0.admin.http import HttpRespInfo
from app0.admin.db import db
from app0.admin.services.app_services import save_app
from app0.admin.services import ROLE_ADMIN, ACT_APP_ARCHIVE, ACT_APP_UNARCHIVE, IDX_APP

logger, extra = app_extra_logger()

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(AppDef, "App Info"),
    responses={
        200: (AppDef, "App updated"),
        400: (str, "Request error"),
        403: (str, "Forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: AppDef, context: EventContext,
              action: Optional[str] = None) -> Union[AppDef, HttpRespInfo]:
    """App save and actions"""
    es = db(context.env)
    # check user admin
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')

    if not action:
        await save_app(es, payload)
    elif action == ACT_APP_ARCHIVE:
        await _app_archive(es, payload, context)
    elif action == ACT_APP_UNARCHIVE:
        await _app_unarchive(es, payload, context)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[AppDef, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[AppDef, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _app_archive(es, app_def: AppDef, context: EventContext):
    logger.info(context, f"Archiving app {app_def}")
    await es[IDX_APP].update_one({'_id': ObjectId(app_def.id)}, {'$set': {'enabled': False}})


async def _app_unarchive(es, app_def: AppDef, context: EventContext):
    logger.info(context, f"Unarchiving app {app_def}")
    await es[IDX_APP].update_one({'_id': ObjectId(app_def.id)}, {'$set': {'enabled': True}})
