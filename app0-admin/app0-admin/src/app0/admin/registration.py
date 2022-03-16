"""
App0Platform: Registration
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.common import IdDescription


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
    position: Optional[IdDescription] = fd("Position", default=None)
    license_id: str = fd("License ID", default="")
    address: str = fd("Address", default="")
    company_id: str = fd("Company Id", default="")
    company_name: str = fd("Company Name", default="")
    company_phone: str = fd("Company Phone", default="")
    company_address: str = fd("Company Address", default="")
    company_email: str = fd("Company Email", default="")
    company_image: str = fd("Company Logo", default="")
    plan_id: str = fd("Plan id", default="")
    plan_name: str = fd("Plan Name", default="")
    plan_description: str = fd("Plan Description", default="")
    plan_annual_payment: bool = fd("Annual payment or Monthly payment?", default=True)
    plan_monthly_amount: Optional[Decimal] = fd("Plan Monthly Amount", default=None)
    plan_annual_amount: Optional[Decimal] = fd("Plan Annual Amount", default=None)
    plan_max_open_claims: Optional[int] = fd("Plan Max Open Claims", default=None)
    plan_max_adjusters: Optional[int] = fd("Plan Max Public Adjusters", default=None)
    plan_max_storage: Optional[int] = fd("Max Storage (in GB)", default=None)
    creation_date: Optional[datetime] = fd("Creation date", default=None)
    confirm_date: Optional[datetime] = fd("Confirm registration date", default=None)
    email_confirm_date: Optional[datetime] = fd("Email Confirm date", default=None)
    email_confirmed: bool = fd("Email Confirmed", default=False)
    phone_confirm_date: Optional[datetime] = fd("Phone Confirm date", default=None)
    phone_confirmed: bool = fd("Phone Confirmed", default=False)
    status: str = fd("Incomplete / Unprocessed / Confirmed / Error", default='Incomplete')
    status_error: Optional[str] = fd("Status error message", default=None)
    billing_card_holder: str = fd("Credit Card Holder", default="")
    billing_card_id: str = fd("Credit Card StripeID", default="")
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
