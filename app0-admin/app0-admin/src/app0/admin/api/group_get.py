"""
Platform Groups: group-get
"""
from typing import Optional, Union

from app0.admin.db import db
from app0.admin.group import Group
from app0.admin.services.group_services import get_group_by_name

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('name', str, "Group name")
    ],
    responses={
        200: (Group, "Group"),
        404: (str, "Group not found")
    }
)


async def run(payload: None,
              context: EventContext,
              name: str) -> Optional[Group]:
    es = db(context.env)
    return await get_group_by_name(es, name)


async def __postprocess__(payload: Optional[Group], context: EventContext,
                          response: PostprocessHook) -> Union[Group, str]:
    if payload is None:
        response.status = 404
        return "Group not found"
    return payload
