"""
App0Platform: Porvider
"""
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.common import IdDescription


@dataobject
@dataclass
class Provider:
    """
    Service Provider
    """
    firstname: str = fd("Firstname")
    surname: str = fd("Surname")
    email: str = fd("Email")
    middle_name: str = fd("Middle Name", default='')
    phone_number: str = fd("Phone Number", default='')
    ssn_ein: str = fd("SSN/EIN", default='')
    company_name: Optional[str] = fd("Company name if provider is company", default=None)
    company_ssn_ein: Optional[str] = fd("Company SSN/EIN if provider is company", default=None)
    birthday: Optional[datetime] = fd("Birthay", default=None)
    start_date: Optional[datetime] = fd("Starting Date", default=None)
    service_types: List[IdDescription] = fd("Type of service", default_factory=list)
    notes: Optional[str] = fd("Notes", default=None)
    image: Optional[str] = fd("Provider image", default=None)
    address: Optional[str] = fd("Address", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
