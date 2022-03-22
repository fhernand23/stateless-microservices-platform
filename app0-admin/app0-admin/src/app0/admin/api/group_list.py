"""
Platform Groups: group-list
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.db import db
from app0.admin.group import Group
from app0.admin.services.group_services import get_groups

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (List[Group], "Group List")
    }
)


async def run(payload: None, context: EventContext) -> List[Group]:
    es = db(context.env)
    return await get_groups(es)
