"""
Platform Auth: Login
--------------------------------------------------------------------
Handles users login using basic-auth
and generate access tokens for external services invoking apps
plugged in with basic-auth plugin.
"""
import base64
from datetime import datetime, timezone
from typing import Optional

from app0.admin.services.user_services import (get_user_by_username, get_user_roles_by_username)
from app0.admin.user import User
from app0.platform.auth import (AuthInfo, AuthInfoExtended, ContextUserInfo, UserPassword, _authorize_password,
                                authorize, db, set_refresh_token)
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.errors import Unauthorized
from hopeit.app.logger import app_logger
from hopeit.fs_storage import FileStorage
from hopeit.toolkit.auth import AuthType

logger = app_logger()
fs_auth: Optional[FileStorage] = None

__steps__ = ['login']

__api__ = event_api(
    summary="Auth: Login",
    responses={
        200: (AuthInfo, "Authentication information to be used for further API calls"),
        401: (Unauthorized.ErrorInfo, "Login failed, invalid credentials")
    }
)


async def __init_event__(context: EventContext):
    global fs_auth
    if fs_auth is None:
        fs_auth = FileStorage(path=str(context.env['fs']['auth_store']))


async def login(payload: None, context: EventContext) -> AuthInfoExtended:
    """
    Returns a new access and refresh token for a set of given basic-auth credentials
    """
    assert context.auth_info['allowed']
    now = datetime.now().astimezone(timezone.utc)
    username, password = base64.b64decode(context.auth_info['payload'].encode()).decode().split(":")
    if context.auth_info['auth_type'] == AuthType.BASIC:
        # authenticate against mongodb
        es = db(context.env)
        if await _authorized(username, password):
            user: Optional[User] = await get_user_by_username(es, username)
            if user:
                roles = await get_user_roles_by_username(es=es, username=username)
                user_info = ContextUserInfo(
                    id=str(user.id),
                    user=user.username,
                    fullname=f"{user.firstname} {user.surname}",
                    email=str(user.email),
                    employee_id=user.employee_id if user.employee_id else '',
                    image=user.image if user.image else '',
                    roles=[r.role for r in roles],
                    groups=[]
                )
                return authorize(context, user_info, now)

    raise Unauthorized('Invalid authorization, status not catched')


async def __postprocess__(payload: AuthInfoExtended,
                          context: EventContext, *,
                          response: PostprocessHook) -> AuthInfo:
    set_refresh_token(context.app, context.auth_info, payload, response)
    return payload.to_auth_info()


async def _authorized(username: str, password: str, user_id: Optional[str] = None) -> bool:
    if fs_auth is None:
        return False
    auth_info = await fs_auth.get(key=username, datatype=UserPassword)

    if auth_info is not None:
        return _authorize_password(password, auth_info)
    # TODO register & hash password
    # await fs_auth.store(key=username, value=_password_hash(password))  # Comment this line on production
    return False
