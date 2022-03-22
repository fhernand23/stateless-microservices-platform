"""
Platform Auth: Login
--------------------------------------------------------------------
Handles users login using basic-auth
and generate access tokens for external services invoking apps
plugged in with basic-auth plugin.
"""
import base64
from typing import Optional

from app0.platform.auth import (AuthInfo, UserPassword, _password_hash)
from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.errors import Unauthorized
from hopeit.app.logger import app_logger
from hopeit.fs_storage import FileStorage

logger = app_logger()
fs_user: Optional[FileStorage] = None
fs_auth: Optional[FileStorage] = None

__steps__ = ['register_password']

__api__ = event_api(
    summary="Auth: Register password",
    responses={
        200: (AuthInfo, "Authentication information to be used for further API calls"),
        401: (Unauthorized.ErrorInfo, "Login failed, invalid credentials")
    }
)


async def __init_event__(context: EventContext):
    global fs_user, fs_auth
    if fs_user is None:
        fs_user = FileStorage(path=str(context.env['fs']['user_store']))
    if fs_auth is None:
        fs_auth = FileStorage(path=str(context.env['fs']['auth_store']))


async def register_password(payload: None, context: EventContext) -> str:
    """
    Register encoded new user password
    """
    assert context.auth_info['allowed']
    username, password = base64.b64decode(context.auth_info['payload'].encode()).decode().split(":")
    if await _register(username, password):
        return "OK"

    raise Unauthorized('Invalid password set')


async def _register(username: str, password: str, user_id: Optional[str] = None) -> bool:
    if fs_auth is None:
        return False
    auth_info = await fs_auth.get(key=username, datatype=UserPassword)
    if auth_info is not None:
        # exists user
        return False
    # register password
    await fs_auth.store(key=username, value=_password_hash(password))  # Improve process
    return True
