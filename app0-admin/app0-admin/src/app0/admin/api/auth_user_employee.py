"""
Platform Users: auth-user-employee
"""
from typing import Optional, Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.dataobjects.payload import Payload

from app0.admin.db import db
from app0.admin.employee import Employee
from app0.admin.services import IDX_EMPLOYEE

__steps__ = ['run']

__api__ = event_api(
    responses={
        200: (Employee, "Employee"),
        404: (str, "Employee not found")
    }
)


async def run(payload: None, context: EventContext) -> Optional[Employee]:
    es = db(context.env)
    employee_id = context.auth_info['payload'].get('employee_id', None)
    if employee_id:
        return await _get_employee(es, employee_id)
    return None


async def __postprocess__(payload: Optional[Employee], context: EventContext,
                          response: PostprocessHook) -> Union[Employee, str]:
    if payload is None:
        response.status = 404
        return "Employee not found"
    return payload


async def _get_employee(es, employee_id: str) -> Optional[Employee]:
    doc = await es[IDX_EMPLOYEE].find_one(ObjectId(employee_id))
    if doc:
        return Payload.from_obj(doc, Employee)

    return None
