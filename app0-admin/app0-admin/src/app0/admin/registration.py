"""
App0Platform: Registration
"""
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class Registration:
    """
    Registration
    """
    firstname: str = fd("Firstname")
    surname: str = fd("Surname")
    email: str = fd("Email")
    phone: str = fd("Phone", default="")
    license_id: str = fd("License ID", default="")
    address: str = fd("Address", default="")
    creation_date: Optional[datetime] = fd("Creation date", default=None)
    confirm_date: Optional[datetime] = fd("Confirm registration date", default=None)
    email_confirm_date: Optional[datetime] = fd("Email Confirm date", default=None)
    email_confirmed: bool = fd("Email Confirmed", default=False)
    phone_confirm_date: Optional[datetime] = fd("Phone Confirm date", default=None)
    phone_confirmed: bool = fd("Phone Confirmed", default=False)
    status: str = fd("Incomplete / Unprocessed / Confirmed / Error", default='Incomplete')
    status_error: Optional[str] = fd("Status error message", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
