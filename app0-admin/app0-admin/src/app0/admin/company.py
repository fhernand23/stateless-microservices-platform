"""
App0Platform: Company
"""
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.file import PlatformFile


@dataobject
@dataclass
class Company:
    """
    Platform company
    """
    name: str = fd("Name")
    phone_number: str = fd("Phone Number")
    email: str = fd("Email")
    fantasy_name: str = fd("Fantasy Name", default='')
    ssn_ein: str = fd("SSN/EIN", default='')
    address: str = fd("Address", default='')
    image: Optional[str] = fd("Company logo", default=None)
    alt_emails: List[str] = fd("Alternative Emails", default_factory=list)
    alt_phones: List[str] = fd("Alternative Phone Numbers", default_factory=list)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class CompanyConfig:
    """
    Platform company configuration
    """
    w9_document_mandatory: bool = fd("W9 Document Mandatory?", default=True)
    w9_document_date: Optional[datetime] = fd("W9 upload date", default=None)
    w9_document_resource: Optional[PlatformFile] = fd("W9 Document", default=None)
    attorney_list_mandatory: bool = fd("Attorney List document Mandatory?", default=False)
    attorney_list_date: Optional[datetime] = fd("Attorney List upload date", default=None)
    attorney_list_resource: Optional[PlatformFile] = fd("Attorney List document", default=None)
    owner_id: Optional[str] = fd("Owner Id", default=None)
    owner_name: Optional[str] = fd("Owner Name", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
