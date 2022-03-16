"""
Platform Groups: group-save
"""
from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.db import db
from app0.admin.group import Group
from app0.admin.services.group_services import save_group

__steps__ = ['run']

__api__ = event_api(
    payload=(Group, "Group Info"),
    responses={
        200: (Group, "Group updated"),
        404: (str, "Group not found")
    }
)


async def run(payload: Group,
              context: EventContext) -> Group:
    es = db(context.env)
    await save_group(es, payload)

    return payload
