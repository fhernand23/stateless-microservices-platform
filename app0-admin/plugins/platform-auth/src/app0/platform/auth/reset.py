"""
Auth: Reset
---------------------------------------------
Reset user passowrd.
"""
from datetime import datetime, timezone
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.fs_storage import FileStorage

from app0.admin import mail
from app0.admin.http import HttpRespInfo
from app0.admin.services.user_services import get_user
from app0.admin.template_mail import TemplateMailSend
from app0.admin.user import User
from app0.platform.auth import AuthNew, AuthReset, _password_hash, db


logger = app_logger()
fs_recover: Optional[FileStorage] = None
fs_auth: Optional[FileStorage] = None
BASE_URL: Optional[str] = None

__steps__ = ['reset', 'notify_reset']

__api__ = event_api(
    payload=(AuthNew, "Expected data for password reset"),
    responses={
        200: (str, "Reset precedure succcess."),
        403: (str, "Operation forbidden"),
    }
)


async def __init_event__(context: EventContext):
    global fs_recover, fs_auth, BASE_URL
    if fs_auth is None:
        fs_auth = FileStorage(path=str(context.env['fs']['auth_store']))
    if fs_recover is None:
        fs_recover = FileStorage(path=str(context.env['fs']['recover_store']))
    if BASE_URL is None:
        BASE_URL = str(context.env["env_config"]["app0-admin_url"])


async def reset(auth_info: AuthNew, context: EventContext) -> Union[HttpRespInfo, AuthReset]:
    """
    Reset user password if token is valid
    """
    assert fs_recover and fs_auth
    auth_reset: Optional[AuthReset] = await fs_recover.get(key=auth_info.auth_token, datatype=AuthReset)
    if auth_reset:
        assert auth_reset.id and auth_reset.expire
        if auth_reset.expire > datetime.now(tz=timezone.utc):
            auth_reset.expire = datetime.now(tz=timezone.utc)
            await fs_recover.store(key=auth_info.auth_token, value=auth_reset)
            # await fs_auth.store(key=f"{auth_reset.user}_", value=_password_hash(auth_info.password))
            # TODO make a backup of old password?
            await fs_auth.store(key=f"{auth_reset.user}", value=_password_hash(auth_info.password))
            logger.info(context, f"User '{auth_reset.id}' has reset his password")
            return auth_reset
        logger.warning(context, f"User '{auth_reset.id}' expire")
        return HttpRespInfo(403, 'Operation forbidden')
    logger.warning(context, f"Reset password token '{auth_info.auth_token}' missing")
    return HttpRespInfo(403, 'Operation forbidden')


async def notify_reset(auth_reset: AuthReset, context: EventContext) -> Optional[TemplateMailSend]:
    """
    Send Recovery Mail
    """
    assert auth_reset.id
    es = db(context.env)
    user: Optional[User] = await get_user(es, auth_reset.id)
    if user:
        # if first access, send welcome mail
        return TemplateMailSend(
            template=mail.MAIL_WELCOME if auth_reset.first_access else mail.MAIL_PASSWORD_RESET_OK,
            destinations=[user.email],
            replacements={
                mail.VAR_USER_NAME: user.firstname + ' ' + user.surname,
                mail.VAR_CLAIMS_APP_URL: f'{BASE_URL}',
            },
            files=[])
    return None


async def __postprocess__(payload: Optional[Union[HttpRespInfo, TemplateMailSend]], context: EventContext,
                          *, response: PostprocessHook) -> str:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return "Something is wrong"
