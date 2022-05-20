"""
App0Att Clients: client-save
"""
from typing import Union

from app0.admin.client import Client
from app0.app1.services.client_services import save_client
from app0.admin.db import db
from app0.admin.db.counter import incr
from app0.admin.http import HttpRespInfo
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

__steps__ = ['run']

__api__ = event_api(
    payload=(Client, "Object Info"),
    responses={
        200: (Client, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Client,
              context: EventContext) -> Union[Client, HttpRespInfo]:
    """save a client"""
    es = db(context.env)
    if not payload.owner_id:
        payload.owner_id = context.auth_info['payload'].get('owner_id')
        payload.owner_name = context.auth_info['payload'].get('owner_name')
    if not payload.client_number:
        payload.client_number = await _generate_client_number(context)
    await save_client(es, payload)

    return payload


async def __postprocess__(payload: Union[Client, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[Client, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _generate_client_number(context: EventContext) -> str:
    key = 'client'
    owner_id = context.auth_info['payload'].get('owner_id', 'noauth')
    if owner_id:
        key += f'_company_{owner_id}'
    fn = await incr(key)

    return str(fn).zfill(3)
