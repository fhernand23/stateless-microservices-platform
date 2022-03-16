"""
Platform Users: user-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.services.user_services import (get_user, get_user_by_employee,
                                                get_user_by_username)
from app0.admin.user import User

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('obj_id', Optional[str], "User ID"),
        ('username', Optional[str], "username"),
        ('employee_id', Optional[str], "employee id")
    ],
    responses={
        200: (User, "User"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, user_id: Optional[str] = None,
              username: Optional[str] = None, employee_id: Optional[str] = None) -> Optional[User]:
    es = db(context.env)
    if user_id:
        return await get_user(es, user_id)
    if username:
        return await get_user_by_username(es, username)
    if employee_id:
        return await get_user_by_employee(es, employee_id)
    return None


async def __postprocess__(payload: Optional[User], context: EventContext,
                          response: PostprocessHook) -> Union[User, str]:
    if payload:
        return payload
    response.status = 404
    return "Object not found"
