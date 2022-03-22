"""
Platform Users: user-password
"""
from dataclasses import dataclass
from typing import Optional

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.dataobjects import dataobject

__steps__ = ['set_password']


@dataobject
@dataclass
class PasswordParams:
    """Params to create and save Something"""
    password: str
    user: Optional[str]
    old_password: Optional[str]


__api__ = event_api(
    payload=(PasswordParams, "hashed password"),
    responses={
        200: (bool, "Success Operation")
    }
)


async def set_password(payload: PasswordParams, context: EventContext) -> bool:
    print(payload)
    return True
