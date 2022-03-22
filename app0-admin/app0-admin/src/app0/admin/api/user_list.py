"""
Platform Users: user-list
"""
from typing import List, Optional

from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.db import db
from app0.admin.services.user_services import get_users
from app0.admin.user import User

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('search', Optional[str], "filter string")
    ],
    responses={
        200: (List[User], "List of User")
    }
)


async def run(payload: None,
              context: EventContext,
              search: Optional[str] = None) -> List[User]:
    es = db(context.env)
    return await get_users(es, search)
