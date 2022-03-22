"""
App0Platform: Employee
"""
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.common import IdDescription


@dataobject
@dataclass
class Employee:
    """
    Employee
    """
    firstname: str = fd("Firstname")
    surname: str = fd("Surname")
    email: str = fd("Email")
    middle_name: str = fd("Middle Name", default='')
    phone_number: str = fd("Phone Number", default='')
    ssn_ein: str = fd("SSN/EIN", default='')
    birthday: Optional[datetime] = fd("Birthay", default=None)
    start_date: Optional[datetime] = fd("Starting Date", default=None)
    position: Optional[IdDescription] = fd("Position", default=None)
    teams: List[IdDescription] = fd("Team", default_factory=list)
    notes: Optional[str] = fd("Notes", default='')
    notes_work: Optional[str] = fd("Notes", default='')
    image: Optional[str] = fd("Employee image", default=None)
    employee_id: Optional[str] = fd("Employee id", default=None)
    license_id: Optional[str] = fd("License id", default=None)
    address: Optional[str] = fd("Address", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
