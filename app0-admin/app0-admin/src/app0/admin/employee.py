"""
App0Platform: Employee
"""
from datetime import datetime
from decimal import Decimal
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
    exempt_employee: bool = fd("Exempt Employee", default=False)
    public_adjuster_license: bool = fd("Is a Public Adjuster with License?", default=False)
    birthday: Optional[datetime] = fd("Birthay", default=None)
    start_date: Optional[datetime] = fd("Starting Date", default=None)
    position: Optional[IdDescription] = fd("Position", default=None)
    teams: List[IdDescription] = fd("Team", default_factory=list)
    assistant: Optional[IdDescription] = fd("Assistant or Desk Adjuster", default=None)
    emergency_contact_name: Optional[str] = fd("Emergency Contact Name", default=None)
    emergency_contact_phone: Optional[str] = fd("Emergency Contact Phone Number", default=None)
    notes: Optional[str] = fd("Notes", default='')
    notes_work: Optional[str] = fd("Notes", default='')
    image: Optional[str] = fd("Employee image", default=None)
    employee_id: Optional[str] = fd("Employee id", default=None)
    license_id: Optional[str] = fd("License id", default=None)
    address: Optional[str] = fd("Address", default=None)
    base_salary: Decimal = fd("Base salary", default=Decimal("0.00"))
    recurrency: Optional[IdDescription] = fd("Recurrency", default=None)
    commission: Optional[IdDescription] = fd("Commission percentage", default=None)
    fixed_fee: Decimal = fd("Fixed fee per claim", default=Decimal("0.00"))
    teacher: Optional[IdDescription] = fd("Teacher", default=None)
    teacher_perc: Decimal = fd("Teacher percentage", default=Decimal("0.00"))
    mentor: Optional[IdDescription] = fd("Mentor", default=None)
    mentor_perc: Decimal = fd("Mentor percentage", default=Decimal("0.00"))
    owner_id: Optional[str] = fd("Owner Id", default=None)
    owner_name: Optional[str] = fd("Owner Name", default=None)
    company_representative: bool = fd("Company Representative?", default=False)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
