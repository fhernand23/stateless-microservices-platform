import pytest  # type: ignore

from hopeit.toolkit import auth

from hopeit.app.context import EventContext, PostprocessHook
from hopeit.app.errors import Unauthorized
from hopeit.server.config import AuthType

from app0.platform.auth import AuthInfoExtended, AuthInfo, login
from . import mock_app_config, plugin_config  # noqa: F401


async def invoke_login(context: EventContext):
    await login.__init_event__(context)
    auth_info = await login.login(None, context)

    assert auth_info.token_type == 'BEARER'

    access_token_info = auth.decode_token(auth_info.access_token)
    assert access_token_info['app'] == 'test_app.test'
    assert access_token_info['id'] == 'a471a12d-a199-4194-b5b4-dda2bc6928e4f'
    assert access_token_info['email'] == 'user@super'
    assert access_token_info['user'] == 'superuser'
    iat = access_token_info['iat']
    assert access_token_info['exp'] == iat + context.env['auth']['access_token_expiration']
    assert access_token_info['renew'] > 0
    assert access_token_info['renew'] < 1000.0 * (
        int(context.env['auth']['access_token_expiration']) - int(context.env['auth']['access_token_renew_window']))
    refresh_token_info = auth.decode_token(auth_info.refresh_token)
    assert refresh_token_info['app'] == 'test_app.test'
    assert refresh_token_info['id'] == 'a471a12d-a199-4194-b5b4-dda2bc6928e4f'
    assert refresh_token_info['email'] == 'user@super'
    assert refresh_token_info['user'] == 'superuser'
    iat = refresh_token_info['iat']
    assert refresh_token_info['exp'] == iat + context.env['auth']['refresh_token_expiration']

    # assert auth_info.user_info == ContextUserInfo(id='id', user='test', fullname="",
    #                                               email='test@email', roles=[], groups=[])
    assert auth_info.access_token_expiration == context.env['auth']['access_token_expiration']
    assert auth_info.refresh_token_expiration == context.env['auth']['refresh_token_expiration']
    assert auth_info.renew == access_token_info['renew']
    return auth_info


async def invoke_postprocess(payload: AuthInfoExtended, context: EventContext):
    hook = PostprocessHook()
    result = await login.__postprocess__(payload, context, response=hook)
    assert hook.cookies['test_app.test.refresh'] == (
        f"Refresh {payload.refresh_token}",
        tuple(), {'expires': 3600,
                  'httponly': 'true',
                  'max_age': 3600,
                  'path': '/', 'domain': None, 'samesite': 'Lax'}
    )
    assert result == AuthInfo(
        access_token=payload.access_token,
        token_type=payload.token_type,
        renew=payload.renew
    )


async def execute_flow(context):
    auth_info = await invoke_login(context)
    await invoke_postprocess(auth_info, context)


def _event_context(mock_app_config, plugin_config):  # noqa: F811
    return EventContext(
        app_config=mock_app_config,
        plugin_config=plugin_config,
        event_name='login',
        track_ids={},
        auth_info={
            'allowed': True,
            'fullname': 'superuser',
            'auth_type': AuthType.BASIC,
            'payload': 'c3VwZXJ1c2VyOjEyMw=='
        }
    )


@pytest.mark.asyncio
async def test_login(mock_app_config, plugin_config):  # noqa: F811
    auth.init(mock_app_config.app_key(), mock_app_config.server.auth)
    context = _event_context(mock_app_config, plugin_config)
    await execute_flow(context)


@pytest.mark.asyncio
async def test_login_unauthorized(mock_app_config, plugin_config):  # noqa: F811
    auth.init(mock_app_config.app_key(), mock_app_config.server.auth)
    context = _event_context(mock_app_config, plugin_config)
    context.auth_info['auth_type'] = "UNKNOWN"
    with pytest.raises(Unauthorized):
        await execute_flow(context)
