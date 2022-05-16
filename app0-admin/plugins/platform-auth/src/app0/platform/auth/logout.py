"""
Platform Auth: Logout
---------------------------------------------
Invalidates previous refresh cookies.
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.app.errors import Unauthorized

from app0.platform.auth import del_refresh_token


logger = app_logger()

__steps__ = ['logout']

__api__ = event_api(
    summary="Auth: Logout",
    responses={
        200: (str, "Logged out message."),
        401: (Unauthorized.ErrorInfo, "Login failed, invalid credentials or not logged in.")
    }
)


async def logout(payload: None, context: EventContext):
    assert context.auth_info['allowed']
    # if not context.auth_info['auth_type'] == AuthType.REFRESH:
    #     raise Unauthorized('Invalid authorization')


async def __postprocess__(payload: None, context: EventContext, *, response: PostprocessHook) -> str:
    del_refresh_token(context.app, context.auth_info, payload, response)
    return "Logged out."
