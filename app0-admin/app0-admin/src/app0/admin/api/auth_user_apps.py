"""
Platform Auth: auth-user-apps
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.app import AppDef
from app0.admin.db import db
from app0.admin.services.app_services import get_apps_by_roles

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (List[AppDef], "Apps")
    }
)


async def run(payload: None, context: EventContext) -> List[AppDef]:
    es = db(context.env)
    roles = context.auth_info['payload']['roles']

    return await get_apps_by_roles(es, roles)
