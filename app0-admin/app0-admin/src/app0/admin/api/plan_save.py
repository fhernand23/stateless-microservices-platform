"""
Platform Plans: plan-save
"""
from typing import Optional, Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services.plan_services import save_plan
from app0.admin.subscription import AvailablePlan
from app0.admin.services import (ACT_PLAN_DELETE, IDX_PLAN, ROLE_ADMIN)

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('action', Optional[str], "Apply some action")
    ],
    payload=(AvailablePlan, "Object Info"),
    responses={
        200: (AvailablePlan, "Object updated"),
        400: (str, "Request error"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: AvailablePlan, context: EventContext,
              action: Optional[str] = None) -> Union[AvailablePlan, HttpRespInfo]:
    """Save Plan"""
    es = db(context.env)
    roles = context.auth_info['payload'].get('roles', 'noauth')
    if ROLE_ADMIN not in roles:
        return HttpRespInfo(403, 'User is not admin')
    if not action:
        await save_plan(es, payload)
    elif action == ACT_PLAN_DELETE:
        await _plan_delete(es, payload)
    else:
        return HttpRespInfo(400, 'Action not recognized')
    return payload


async def __postprocess__(payload: Union[AvailablePlan, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[AvailablePlan, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _plan_delete(es, available_plan: AvailablePlan):
    # delete related info
    await es[IDX_PLAN].delete_one({'_id': ObjectId(available_plan.id)})
