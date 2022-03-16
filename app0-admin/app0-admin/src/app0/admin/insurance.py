"""
App0Platform: Insurance
"""
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.common import IdDescription


@dataobject
@dataclass
class InsuranceCompany:
    """
    Insurance Company
    """
    name: str = fd("Name")
    email: str = fd("Email", default='')
    phone_number: str = fd("Phone Number", default='')
    notes: Optional[str] = fd("Notes", default=None)
    image: Optional[str] = fd("Company logo", default=None)
    address: Optional[str] = fd("Address", default=None)
    aptsuiteunit: Optional[str] = fd("Aptsuiteunit", default=None)
    city: Optional[str] = fd("City", default=None)
    state: Optional[str] = fd("State", default=None)
    zipcode: Optional[str] = fd("Zipcode", default=None)
    submission_link: Optional[str] = fd("Submission link", default=None)
    alt_emails: List[str] = fd("Alternative Emails", default_factory=list)
    alt_phones: List[str] = fd("Alternative Phone Numbers", default_factory=list)
    open_claim_requirement: Optional[str] = fd("Requirement to open a claim", default=None)
    owner_id: Optional[str] = fd("Owner Id", default=None)
    owner_name: Optional[str] = fd("Owner Name", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class InsuranceEmployee:
    """
    Insurance Employee
    """
    firstname: str = fd("Firstname")
    surname: str = fd("Surname")
    email: str = fd("Email")
    company_id: str = fd("Insurance Company id", default='')
    company_name: str = fd("Insurance Company name", default='')
    middle_name: str = fd("Middle Name", default='')
    phone_number: str = fd("Phone Number", default='')
    teams: List[IdDescription] = fd("Team", default_factory=list)
    notes: Optional[str] = fd("Notes", default='')
    creation_date: Optional[datetime] = fd("Creation date", default=None)
    owner_id: Optional[str] = fd("Owner Id", default=None)
    owner_name: Optional[str] = fd("Owner Name", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
