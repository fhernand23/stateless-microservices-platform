"""
Platform Auth: Refresh
-------------------------------------------------------------------------------------
This event can be used for obtain new access token and update refresh token (http cookie),
with no need to re-login the user if there is a valid refresh token active.
"""
from datetime import datetime, timezone

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.logger import app_logger
from hopeit.server.config import AuthType
from hopeit.app.errors import Unauthorized
from app0.platform.auth import ContextUserInfo, AuthInfo, AuthInfoExtended, authorize, set_refresh_token

logger = app_logger()

__steps__ = ['refresh']

__api__ = event_api(
    summary="Auth: Refresh",
    responses={
        200: (AuthInfo, "Refreshed authentication information to be used for further API calls"),
        401: (Unauthorized.ErrorInfo, "Login failed, invalid credentials. An http-cookie is expected")
    }
)


async def refresh(payload: None, context: EventContext) -> AuthInfoExtended:
    """
    Returns a new access and refresh tokens, from a request containing a valid refresh token.
    """
    assert context.auth_info['allowed']
    now = datetime.now().astimezone(timezone.utc)
    if context.auth_info['auth_type'] == AuthType.REFRESH:
        user_info = ContextUserInfo(
            id=context.auth_info['payload']['id'],
            user=context.auth_info['payload']['user'],
            email=context.auth_info['payload']['email'],
            fullname=context.auth_info['payload']['fullname'],
            owner_id=context.auth_info['payload']['owner_id'],
            owner_name=context.auth_info['payload']['owner_name'],
            employee_id=context.auth_info['payload']['employee_id'],
            image=context.auth_info['payload']['image'],
            roles=context.auth_info['payload']['roles'],
            groups=context.auth_info['payload']['groups'],
        )
        return authorize(context, user_info, now)
    raise Unauthorized('Invalid authorization')


async def __postprocess__(payload: AuthInfoExtended,
                          context: EventContext, *,
                          response: PostprocessHook) -> AuthInfo:
    set_refresh_token(context.app, context.auth_info, payload, response)
    return payload.to_auth_info()
