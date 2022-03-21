"""
App0Platform: TemplateMail
"""
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId  # type: ignore  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class User:
    """
    Platform user
    """
    firstname: str = fd("Firstname")
    surname: str = fd("Surname")
    username: str = fd("Username")
    email: str = fd("Email")
    phone_number: str = fd("Phone Number", default='')
    password: str = fd("Password", default='')
    activated: bool = fd("Activated?", default=True)
    email_confirm_date: Optional[datetime] = fd("Email Confirm date", default=None)
    email_confirmed: bool = fd("Email Confirmed", default=False)
    phone_confirm_date: Optional[datetime] = fd("Phone Confirm date", default=None)
    phone_confirmed: bool = fd("Phone Confirmed", default=False)
    id: Optional[str] = fd("Db id", default=None)
    employee_id: Optional[str] = fd("Employee Id", default=None)
    image: Optional[str] = fd("User image", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class UserAppRole:
    """
    User & Application Role
    """
    username: str = fd("Username")
    role: str = fd("Role name")
    id: Optional[str] = fd("Db id", default=None)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
