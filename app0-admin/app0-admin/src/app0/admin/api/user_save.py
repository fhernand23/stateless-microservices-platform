"""
Platform Users: user-save
"""
import uuid
from typing import Optional, Union
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_extra_logger
from hopeit.fs_storage import FileStorage
from hopeit.dataobjects.payload import Payload
from hopeit.app.client import app_call
from hopeit.dataobjects import dataobject

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services import (ACT_USER_DELETE_USER, ACT_USER_CREATE, IDX_USER_ROLE, ACT_USER_DISABLE_USER_EMPLOYEE,
                                 IDX_EMPLOYEE, IDX_USER, ROLE_ADMIN, IDX_NOTIFICATION)
from app0.admin.services.user_services import save_user
from app0.admin.user import User, UserAppRole
from app0.admin import mail
from app0.admin.template_mail import TemplateMailSend
from app0.platform.auth import AuthReset
from app0.admin.notification import Notification
from app0.admin.util import company_util

logger, extra = app_extra_logger()
fs_recover: Optional[FileStorage] = None
BASE_URL: Optional[str] = None


@dataobject
@dataclass
class AuthResetData:
    """
    Info for password reset
    """
    user: User
    recovery_token: str


__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(User, "User Info"),
    responses={
        200: (User, "User updated"),
        400: (str, "Request error"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def __init_event__(context: EventContext):
    global fs_recover, BASE_URL
    if fs_recover is None:
        fs_recover = FileStorage(path=str(context.env['fs']['recover_store']))
    if BASE_URL is None:
        BASE_URL = str(context.env["env_config"]["app0-admin_url"])


async def run(payload: User, context: EventContext, action: Optional[str] = None) -> Union[User, HttpRespInfo]:
    """User save & actions"""
    es = db(context.env)
    # check user admin
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')

    if not action:
        await save_user(es, payload)
    elif action == ACT_USER_CREATE:
        await _user_create(es, payload, context)
    elif action == ACT_USER_DELETE_USER:
        await _user_delete(es, payload, context)
    elif action == ACT_USER_DISABLE_USER_EMPLOYEE:
        await _user_employee_disable(es, payload, context)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[User, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[User, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _user_create(es, user: User, context: EventContext):
    """Create a user"""
    logger.info(context, f"Creating user {user}")
    await save_user(es, user)
    user_app_role = UserAppRole(user.username, ROLE_ADMIN)
    await es[IDX_USER_ROLE].replace_one({'_id': ObjectId(user_app_role.id)},
                                        Payload.to_obj(user_app_role), upsert=True)
    # generate token to set password
    await _register(user, context)
    await _create_notification_user(es, user)

    logger.info(context, "Creating user complete!")


async def _user_delete(es, user: User, context: EventContext):
    # check if user has employee_id & delete
    logger.info(context, f"Deleting user {user}")
    if user.employee_id:
        await es[IDX_EMPLOYEE].delete_one({'_id': ObjectId(user.employee_id)})
    await es[IDX_USER_ROLE].delete_many({'username': user.username})
    await es[IDX_USER].delete_one({'_id': ObjectId(user.id)})


async def _user_employee_disable(es, user: User, context: EventContext):
    # check if user has employee_id & delete
    logger.info(context, f"Disabling user {user}")
    if user.employee_id:
        await es[IDX_EMPLOYEE].update_one({'_id': ObjectId(user.employee_id)}, {'$set': {'enabled': False}})
    await es[IDX_USER].update_one({'_id': ObjectId(user.id)}, {'$set': {'enabled': False}})


async def _register(user: User, context: EventContext):
    """
    Register user and token with ttl for password setup
    """
    assert fs_recover
    auth_reset = AuthReset(user=user.username, id=user.id,
                           expire=datetime.now(tz=timezone.utc) + timedelta(seconds=3600),
                           first_access=True)
    notify: AuthResetData = AuthResetData(user=user, recovery_token=str(uuid.uuid4()))
    await fs_recover.store(notify.recovery_token, auth_reset)
    logger.info(context, f"User '{notify.user.id}' request password reset")
    # send mail
    tmail_send = TemplateMailSend(
        template=mail.MAIL_EMAIL_CONFIRMATION,
        destinations=[user.email],
        replacements={
            mail.VAR_USER_NAME: user.firstname + ' ' + user.surname,
            mail.VAR_CLAIMS_APP_URL: f'{BASE_URL}',
            mail.VAR_EMAIL_CONFIRM_URL: f'{BASE_URL}/fset/{notify.recovery_token}',
        },
        files=[])
    logger.info(context, f"Sending Mail {tmail_send}")
    tmail_send_r = await app_call(
        context.event_info.connections[0].app_connection,
        event=context.event_info.connections[0].event,
        datatype=TemplateMailSend, payload=tmail_send, context=context
    )
    logger.info(context, f"Mail queued OK {tmail_send_r}")


async def _create_notification_user(es, user: User):
    """
    Create Notification for User
    """
    notification = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=company_util.SYSTEM_USER,
        user_name=company_util.SYSTEM_USER_DESC,
        owner_id=user.owner_id if user.owner_id else "",
        owner_name=user.owner_name if user.owner_name else "",
        app_name=company_util.APP_BASE,
        content=f"User {user.email} has been added to Claims Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification.id)},
                                           Payload.to_obj(notification),
                                           upsert=True)

    notification2 = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=company_util.SYSTEM_USER,
        user_name=company_util.SYSTEM_USER_DESC,
        owner_id=user.owner_id if user.owner_id else "",
        owner_name=user.owner_name if user.owner_name else "",
        type=company_util.TYPE_DIRECT,
        app_name=company_util.APP_BASE,
        dest_user_id=user.id,  # type: ignore
        content=f"Welcome {user.email} to the Claims Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification2.id)},
                                           Payload.to_obj(notification2),
                                           upsert=True)
