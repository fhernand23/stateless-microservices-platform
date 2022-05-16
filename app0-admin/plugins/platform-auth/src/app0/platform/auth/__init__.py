"""
platform-auth plugin app, helper classes and methods
"""
import random
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from cryptography.fernet import Fernet
from hopeit.toolkit import auth
from hopeit.app.config import AppDescriptor
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.dataobjects import dataobject
from hopeit.server.config import AuthType
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

__all__ = [
    'ContextUserInfo',
    'ContextUserInfoAuth',
    'AuthInfoExtended',
    'AuthInfo',
    'authorize',
    'set_refresh_token'
]


@dataobject
@dataclass
class UserPassword:
    """
    User info that will be available in context during events execution
    """
    salt: str
    hash: str
    last_update: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None


@dataobject
@dataclass
class ContextUserInfo:
    """
    User info that will be available in context during events execution
    """
    id: str
    user: str
    fullname: str
    email: str
    employee_id: str
    image: str
    roles: List[str]
    groups: List[str]


@dataobject
@dataclass
class ContextUserInfoAuth(ContextUserInfo):
    """
    Extended ContextUserInfo with authentication fields
    """
    password: str


@dataobject
@dataclass
class AuthInfoExtended:
    """
    Internal class containing auth info to be passed from events
    to postprocess hooks.
    To share data with external apps or engine use to_auth_info()
    """
    access_token: str
    refresh_token: str
    token_type: str
    access_token_expiration: int
    refresh_token_expiration: int
    renew: int
    app: str
    user_info: ContextUserInfo

    def to_auth_info(self):
        return AuthInfo(
            access_token=self.access_token,
            token_type=self.token_type,
            renew=self.renew
        )


@dataobject
@dataclass
class AuthInfo:
    """
    Minimal auth info that should be returned outside this app
    """
    access_token: str
    token_type: str
    renew: int


@dataobject
@dataclass
class AuthReset:
    """
    Minimal auth info for password reset
    """
    user: str
    id: Optional[str]
    expire: Optional[datetime]
    first_access: Optional[bool] = False

    def __post_init__(self):
        if self.expire is None:
            self.expire = datetime.now(tz=timezone.utc) + timedelta(seconds=3600)


@dataobject
@dataclass
class AuthNew:
    """
    Password reset data
    """
    auth_token: str
    password: str


def db(env: dict):
    """
    Return a reference to collection (no IO)
    """
    client = AsyncIOMotorClient(env['mongodb']['conn_str'])
    conn = client[env['mongodb']['dbname']]

    return conn


def authorize(context: EventContext,
              user_info: ContextUserInfo,
              now: datetime) -> AuthInfoExtended:
    """
    Authorize user and returns auth info containing tokens for api access and authorization renewal

    :param context: event context from app requesting authorization or login happened
    :param user_info: already validated user info to be encoded in tokens:
        Notice this method wont check if user is valid, invoking app should ensure this.
    :param now: current datetime, fixed as start of authorization process
    :return: AuthInfoExtended, containing new access and refresh tokens
    """
    ate = int(context.env['auth']['access_token_expiration'])
    rte = int(context.env['auth']['refresh_token_expiration'])
    atr = int(context.env['auth']['access_token_renew_window'])
    renew_in = int(1000.0 * max(
        1.0 * ate - 1.0 * atr * (1.0 + 0.5 * random.random()),
        0.5 * ate * (0.5 * random.random() + 0.5)))
    token = _new_access_token(asdict(user_info), context, now, ate, renew_in)
    refresh_token = _new_refresh_token(asdict(user_info), context, now, rte)
    result = AuthInfoExtended(
        app=context.app_key,
        access_token=token,
        refresh_token=refresh_token,
        token_type=AuthType.BEARER.name,
        access_token_expiration=ate,
        refresh_token_expiration=rte,
        renew=renew_in,
        user_info=user_info
    )
    return result


def set_refresh_token(app: AppDescriptor, auth_info: dict, payload: AuthInfoExtended, response: PostprocessHook):
    """
    sets information to a hook providing a way for http servers
    to set an http-only cookie containing the refresh_token
    """

    response.set_cookie(
        name=f"{app.app_key()}.refresh",
        value=f"Refresh {payload.refresh_token}",
        httponly="true",
        expires=payload.refresh_token_expiration,
        max_age=payload.refresh_token_expiration,
        path="/",
        domain=auth_info.get("domain"),
        samesite="Lax"
    )


def del_refresh_token(app: AppDescriptor, auth_info: dict, payload: None, response: PostprocessHook):
    """
    delete information to a hook providing a way for http servers
    to unset an http-only cookie containing the refresh_token
    """
    response.del_cookie(
        name=f"{app.app_key()}.refresh",
        domain=auth_info.get("domain"),
        path="/",
    )


def _new_access_token(info: dict, context: EventContext, now: datetime, timeout: int, renew: int):
    """
    Returns a new access token encoding `info` and expiring in `access_token_expiration` seconds
    """
    auth_payload = {
        **info,
        "app": context.app_key,
        "iat": now,
        "exp": now + timedelta(seconds=timeout),
        "renew": renew
    }
    return auth.new_token(context.app_key, auth_payload)


def _new_refresh_token(info: dict,
                       context: EventContext,
                       now: datetime,
                       timeout: int):
    """
    Returns a new refresh token encoding `info` and expiring in `refresh_token_expiration` seconds
    """
    auth_payload = {
        **info,
        "iat": now,
        "exp": now + timedelta(seconds=timeout)
    }
    return auth.new_token(context.app_key, auth_payload)


def _authorize_password(password, auth_info):
    return str.encode(password) == Fernet(str.encode(auth_info.salt)).decrypt(str.encode(auth_info.hash))


def _password_hash(password):
    salt = Fernet.generate_key()
    new_hash = Fernet(salt).encrypt(str.encode(password))
    return UserPassword(salt.decode(), new_hash.decode())
