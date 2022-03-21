"""
App0Platform: Client
"""
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class Client:
    """
    Client
    """
    firstname: str = fd("Firstname", default='')
    middle_name: str = fd("Middle Name", default='')
    surname: str = fd("Surname", default='')
    email: str = fd("Email", default='')
    phone_number: str = fd("Phone Number", default='')
    mailing_address: str = fd("Mailing Address", default='')
    is_company: bool = fd("Is Company?", default=False)
    company_name: Optional[str] = fd("Company name if client is company", default=None)
    notes: Optional[str] = fd("Notes", default=None)
    image: Optional[str] = fd("Employee image", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class ClientService:
    """
    Client & Service
    """
    client_id: str = fd("Client ID", default='')
    client_name: str = fd("Client Name", default='')
    client_email: str = fd("Client Email", default='')
    service_type: str = fd("Service Types", default='')
    service_description: str = fd("Service Name", default='')
    property_type: str = fd("Property type", default='')
    from_date: Optional[datetime] = fd("From Date", default=None)
    to_date: Optional[datetime] = fd("To Date", default=None)
    notes: Optional[str] = fd("Notes", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
