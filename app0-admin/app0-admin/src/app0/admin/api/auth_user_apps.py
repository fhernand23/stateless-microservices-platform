"""
Platform Auth: auth-user-apps
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects.payload import Payload

from app0.admin.app import AppDef
from app0.admin.db import db
from app0.admin.services import IDX_APP

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (List[AppDef], "Apps")
    }
)


async def run(payload: None, context: EventContext) -> List[AppDef]:
    es = db(context.env)
    roles = context.auth_info['payload']['roles']

    return await _get_apps_by_roles(es, roles)


async def _get_apps_by_roles(es, roles: List[str]) -> List[AppDef]:
    if roles:
        cursor = es[IDX_APP].find(
            {'$and': [{'default_role': {'$in': roles}},
                      {'enabled': {'$eq': True}}]})

        return [Payload.from_obj(doc, AppDef) for doc in await cursor.to_list(length=100)]
    return []
