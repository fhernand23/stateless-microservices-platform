"""
Platform Users: user-employee-create
"""
import uuid
from typing import Optional
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.fs_storage import FileStorage
from hopeit.dataobjects.payload import Payload
from hopeit.app.client import app_call
from hopeit.dataobjects import dataobject

from app0.admin.db import db
from app0.admin.employee import Employee
from app0.admin.services import IDX_USER, IDX_USER_ROLE, IDX_NOTIFICATION, ROLE_USER
from app0.admin.user import User, UserAppRole
from app0.admin import mail
from app0.admin.template_mail import TemplateMailSend
from app0.platform.auth import AuthReset
from app0.admin.notification import Notification
from app0.admin.util import company_util

logger, extra = app_extra_logger()
DEF_ROLES = [ROLE_USER]
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


async def __init_event__(context: EventContext):
    global fs_recover, BASE_URL
    if fs_recover is None:
        fs_recover = FileStorage(path=str(context.env['fs']['recover_store']))
    if BASE_URL is None:
        BASE_URL = str(context.env["env_config"]["app0-admin_url"])


async def run(payload: Employee,
              context: EventContext) -> Employee:
    """Save"""
    es = db(context.env)

    if isinstance(payload, Employee):
        logger.info(context, f"Creating user from employee {payload}")
        doc = await es[IDX_USER].find_one({'employee_id': {'$eq': payload.id}})
        if not doc:
            # create user
            user = User(firstname=payload.firstname, surname=payload.surname, username=payload.email,
                        email=payload.email, phone_number=payload.phone_number, owner_id=payload.owner_id,
                        owner_name=payload.owner_name, employee_id=payload.id)
            await es[IDX_USER].replace_one({'_id': ObjectId(user.id)}, Payload.to_obj(user), upsert=True)
            # set user roles
            for role in DEF_ROLES:
                user_app_role = UserAppRole(user.username, role)
                await es[IDX_USER_ROLE].replace_one({'_id': ObjectId(user_app_role.id)},
                                                    Payload.to_obj(user_app_role), upsert=True)
            # generate token to set password
            await _register(user, context)
            await _create_notification_user(es, user)

    logger.info(context, "Creating user complete!")

    return payload


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
