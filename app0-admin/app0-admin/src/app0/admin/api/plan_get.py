"""
Platform Plans: plan-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.services.plan_services import get_plan
from app0.admin.subscription import AvailablePlan

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('obj_id', str, "Object ID")
    ],
    responses={
        200: (AvailablePlan, "AvailablePlan"),
        404: (str, "Object not found")
    }
)


async def run(payload: None,
              context: EventContext,
              obj_id: str) -> Optional[AvailablePlan]:
    es = db(context.env)
    if obj_id:
        return await get_plan(es, obj_id)

    return None


async def __postprocess__(payload: Optional[AvailablePlan], context: EventContext,
                          response: PostprocessHook) -> Union[AvailablePlan, str]:
    if payload is None:
        response.status = 404
        return "AvailablePlan not found"
    return payload
