"""
Platform Registrations: registration-process
"""
import uuid
import os
from dataclasses import dataclass
import traceback
from datetime import datetime, timedelta, timezone
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger
from hopeit.fs_storage import FileStorage
from hopeit.dataobjects.payload import Payload
from hopeit.app.client import app_call
from hopeit.dataobjects import dataobject

from app0.admin.db import db
from app0.admin.registration import Registration
from app0.admin.user import User, UserAppRole
from app0.admin.notification import Notification
from app0.admin.services import (IDX_USER, IDX_USER_ROLE, ROLE_USER, IDX_NOTIFICATION)
from app0.admin.services.registration_services import save_registration
from app0.admin import mail
from app0.admin.tmail import MailTemplate, TmailSend
from app0.admin.util import app_util
from app0.platform.auth import AuthReset

logger, extra = app_extra_logger()
DEF_ROLES = [ROLE_USER]
fs_recover: Optional[FileStorage] = None
APP0_ADMIN_URL: Optional[str] = None
TEMPLATES_FOLDER: Optional[str] = None


@dataobject
@dataclass
class AuthResetData:
    """
    Info for password reset
    """
    user: User
    recovery_token: str


__steps__ = ['create_user', 'user_context_init']


class BadRegistration(Exception):
    """Raised when something go wrong"""


async def __init_event__(context: EventContext):
    global fs_recover, APP0_ADMIN_URL, TEMPLATES_FOLDER
    if fs_recover is None:
        fs_recover = FileStorage(path=str(context.env['fs']['recover_store']))
    if APP0_ADMIN_URL is None:
        APP0_ADMIN_URL = str(context.env["env_config"]["app0_admin_url"])
    if TEMPLATES_FOLDER is None:
        TEMPLATES_FOLDER = str(context.env["email_templates"]["templates_folder"])


async def create_user(payload: Registration, context: EventContext) -> Optional[Registration]:
    """
    Validate, Create User
    """
    es = db(context.env)

    if isinstance(payload, Registration) and payload.status == 'Unprocessed':
        try:
            logger.info(context, f"Processing {payload}")
            # validate registration
            await _validate(es, payload)
            # create user & employee
            user = User(firstname=payload.firstname, surname=payload.surname, username=payload.email,
                        email=payload.email, phone_number=payload.phone)
            user = await _create_user(es, user, context)

        except BadRegistration as ex:
            payload.status = 'Error'
            payload.status_error = str(ex)
        except Exception as ex:  # pylint: disable=W0703
            traceback.print_exc()
            payload.status = 'Error'
            payload.status_error = str(ex)
        else:
            payload.confirm_date = datetime.now().astimezone(timezone.utc)
            payload.status = 'Confirmed'
        finally:
            await save_registration(es, payload)

        logger.info(context, "Processing complete!")
        return payload if payload.status == 'Confirmed' else None

    return None


async def user_context_init(payload: Registration, context: EventContext) -> Optional[Registration]:
    """Initialize user context"""
    logger.info(context, "User Context init START!")
    if payload:
        es = db(context.env)

        logger.info(context, f"Init {payload}")
        # get user
        colu = es[IDX_USER]
        docu = await colu.find_one({'username': {'$eq': payload.email}})

        user = Payload.from_obj(docu, User)
        # create notifications
        await _create_notification_user(es, user)

        logger.info(context, "Processing complete!")

    return payload


async def _validate(es, registration: Registration):
    doc = await es[IDX_USER].find_one({'username': {'$eq': registration.email}})
    if doc:
        raise BadRegistration('There is already a User with that email address')


async def _create_user(es, user: User, context: EventContext) -> User:
    """
    Create employee
    """
    await es[IDX_USER].replace_one({'_id': ObjectId(user.id)}, Payload.to_obj(user), upsert=True)
    # set user roles
    for role in DEF_ROLES:
        user_app_role = UserAppRole(user.username, role)
        await es[IDX_USER_ROLE].replace_one({'_id': ObjectId(user_app_role.id)},
                                            Payload.to_obj(user_app_role), upsert=True)
    # generate token to set password
    await _register(user, context)

    return user


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
    tmail_send = TmailSend(
        template=MailTemplate(collection=mail.MAIL_COLLECTION_BASE, name=mail.MAIL_EMAIL_CONFIRMATION),
        destinations=[user.email],
        replacements={
            mail.VAR_USER_NAME: user.firstname + ' ' + user.surname,
            mail.VAR_ADMIN_APP_URL: f'{APP0_ADMIN_URL}',
            mail.VAR_EMAIL_CONFIRM_URL: f'{APP0_ADMIN_URL}/fset/{notify.recovery_token}',
        },
        files=[])
    logger.info(context, f"Sending Mail {tmail_send}")
    tmail_send_r = await app_call(
        context.event_info.connections[0].app_connection,
        event=context.event_info.connections[0].event,
        datatype=TmailSend, payload=tmail_send, context=context
    )
    logger.info(context, f"Mail queued OK {tmail_send_r}")


async def _create_notification_user(es, user: User):
    """
    Create Notification for User
    """
    notification = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=app_util.SYSTEM_USER,
        user_name=app_util.SYSTEM_USER_DESC,
        app_name=app_util.APP_ADMIN,
        content=f"User {user.email} has been added to App0 Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification.id)},
                                           Payload.to_obj(notification),
                                           upsert=True)

    notification2 = Notification(
        creation_date=datetime.now(tz=timezone.utc),
        user_id=app_util.SYSTEM_USER,
        user_name=app_util.SYSTEM_USER_DESC,
        type=app_util.TYPE_DIRECT,
        app_name=app_util.APP_ADMIN,
        dest_user_id=user.id,  # type: ignore
        content=f"Welcome {user.email} to the App0 Platform")
    await es[IDX_NOTIFICATION].replace_one({'_id': ObjectId(notification2.id)},
                                           Payload.to_obj(notification2),
                                           upsert=True)


async def _load_mail_base_content(did):
    assert TEMPLATES_FOLDER
    file_path = os.path.join(TEMPLATES_FOLDER, did + '_base_content.txt')
    if os.path.isfile(file_path):
        file = open(file_path, "r", encoding="utf-8")
        cont = file.read()
        file.close()
        return cont
    return ''
