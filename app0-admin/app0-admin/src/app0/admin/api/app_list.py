"""
Platform Apps: app-list
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.app import AppDef
from app0.admin.db import db
from app0.admin.services.app_services import get_apps

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (List[AppDef], "Apps list")
    }
)


async def run(payload: None, context: EventContext) -> List[AppDef]:
    es = db(context.env)
    return await get_apps(es)
