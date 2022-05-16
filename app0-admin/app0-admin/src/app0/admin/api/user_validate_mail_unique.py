"""
Platform Users: user-validate-mail
"""
import re

from hopeit.app.api import event_api
from hopeit.app.context import EventContext

from app0.admin.db import db
from app0.admin.http import CodeDescription
from app0.admin.services import IDX_USER

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('email', str, "Email"),
    ],
    responses={
        200: (CodeDescription, "Email valid")
    }
)


async def run(payload: None, context: EventContext, email: str) -> CodeDescription:
    es = db(context.env)
    if not EMAIL_REGEX.match(email):
        return CodeDescription(400, 'Email is not a valid email address')
    if await _exists_in_active_user(es, email):
        return CodeDescription(400, 'Email address in use by another user')
    return CodeDescription(200, 'Email is valid')


async def _exists_in_active_user(es, email: str) -> bool:
    """get company summary info"""
    result = await es[IDX_USER].count_documents(
        {'$and': [{'email': {'$eq': email}},
                  {'enabled': {'$eq': True}}]})

    return result > 0
