"""
Auth: Recovery
---------------------------------------------
Request for reset user passowrd.
"""
import uuid
from dataclasses import dataclass
from typing import Optional

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.dataobjects import dataobject
from hopeit.fs_storage import FileStorage


from app0.admin import mail
from app0.admin.services.user_services import get_user_by_username
from app0.admin.tmail import TmailSend
from app0.admin.user import User
from app0.platform.auth import AuthReset, db

logger = app_logger()
fs_recover: Optional[FileStorage] = None
APP0_ADMIN_URL: Optional[str] = None


@dataobject
@dataclass
class AuthResetData:
    """
    Info for password reset
    """
    user: User
    recovery_token: str


__steps__ = ['process_recovery', 'notify_recovery']

__api__ = event_api(
    payload=(AuthReset, "Expected data for password reset"),
    responses={
        200: (str, "Reset request succcess."),
    }
)


async def __init_event__(context: EventContext):
    global fs_recover, APP0_ADMIN_URL
    if fs_recover is None:
        fs_recover = FileStorage(path=str(context.env['fs']['recover_store']))
    if APP0_ADMIN_URL is None:
        APP0_ADMIN_URL = str(context.env["env_config"]["app0-admin_url"])


async def process_recovery(payload: AuthReset, context: EventContext) -> Optional[AuthResetData]:
    """
    Process requested user password recovery
    """
    assert fs_recover
    es = db(context.env)
    if payload.user:
        user: Optional[User] = await get_user_by_username(es, payload.user)
        if user:
            notify: AuthResetData = AuthResetData(user=user, recovery_token=str(uuid.uuid4()))
            payload.id = user.id
            await fs_recover.store(notify.recovery_token, payload)
            logger.info(context, f"User '{notify.user.id}' request password reset")
            return notify
        logger.warning(context, f"Missing user '{payload.user}' request password reset")
        return None
    logger.warning(context, "Empty request for password reset")
    return None


async def notify_recovery(data: AuthResetData, context: EventContext) -> TmailSend:
    """
    Send Recovery Mail
    """
    return TmailSend(
        template=mail.MAIL_PASSWORD_RESET,
        destinations=[data.user.email],
        replacements={
            mail.VAR_PASSWORD_RESET_URL: f'{APP0_ADMIN_URL}/reset/{data.recovery_token}',
        },
        files=[])


async def __postprocess__(payload: Optional[TmailSend], context: EventContext, *, response: PostprocessHook) -> str:
    if payload:
        return "Notification submited to proccess"
    return "Something is wrong"
