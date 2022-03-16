"""
Platform Auth: auth-user-roles
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.app import AppRole
from app0.admin.db import db
from app0.admin.services.app_services import get_role_by_name

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (List[AppRole], "Roles of the authenticated user")
    }
)


async def run(payload: None, context: EventContext) -> List[AppRole]:
    es = db(context.env)
    roles = context.auth_info['payload']['roles']
    ret: List[AppRole] = []
    for r in roles:
        app_role = await get_role_by_name(es, r)
        if app_role:
            ret.append(app_role)
    return ret
