"""
App0Platform: Subscription
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.registration import Registration


@dataobject
@dataclass
class AvailablePlan:
    """
    Available Plan
    """
    name: str = fd("Name", default="")
    subtitle: str = fd("Subtitle", default="")
    description: str = fd("Description", default="")
    learn_more_url: str = fd("Learn more url", default="")
    contact_url: str = fd("Contact url", default="")
    annual_payment: bool = fd("Annual payment or Monthly payment?", default=True)
    monthly_amount: Optional[Decimal] = fd("Monthly Amount", default=None)
    annual_amount: Optional[Decimal] = fd("Annual Amount", default=None)
    claims_limit: bool = fd("Open Claims Limit?", default=False)
    adjusters_limit: bool = fd("Public Adjusters Limit?", default=True)
    storage_limit: bool = fd("Storage Limit?", default=True)
    max_open_claims: Optional[int] = fd("Max Open Claims Limit", default=None)
    max_adjusters: Optional[int] = fd("Max Public Adjusters", default=None)
    max_storage: Optional[int] = fd("Max Storage (in GB)", default=None)
    most_recommended: bool = fd("Most Recommended Mark", default=False)
    discount: str = fd("Discount", default="")
    registration_order: Optional[int] = fd("Registration Order", default=None)
    image: Optional[str] = fd("Plan logo", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class PlanInfo:
    """
    PlanInfo
    """
    start_date: datetime = fd("Start subscription date")
    name: str = fd("Plan Name", default="")
    description: str = fd("Plan Description", default="")
    annual_payment: bool = fd("Annual payment or Monthly payment?", default=True)
    monthly_amount: Decimal = fd("Plan Monthly Amount", default=Decimal(0.00))
    annual_amount: Decimal = fd("Annual Amount", default=Decimal(0.00))
    max_open_claims: int = fd("Plan Max Open Claims", default=0)
    max_adjusters: int = fd("Plan Max Public Adjusters", default=0)
    max_storage: int = fd("Plan Max Storage", default=0)
    end_date: Optional[datetime] = fd("End subscription date", default=None)


@dataobject
@dataclass
class BillingInfo:
    """
    BillingInfo
    """
    card_holder: str = fd("Credit Card Holder", default="")
    card_id: str = fd("Credit Card StripeID", default="")


@dataobject
@dataclass
class InvoiceItem:
    """
    Invoice
    """
    description: str = fd("Description")
    amount: Decimal = fd("Amount")
    tax: Decimal = fd("Tax Amount")
    total: Decimal = fd("Total Amount")
    from_date: Optional[datetime] = fd("From date", default=None)
    to_date: Optional[datetime] = fd("To date", default=None)
    quantity: Optional[int] = fd("Quantity", default=None)


@dataobject
@dataclass
class Invoice:
    """
    Invoice
    """
    invoice_date: datetime = fd("Invoice date")
    invoice_number: str = fd("Invoice number")
    remit_to: str = fd("Remit To")
    invoice_to: str = fd("Invoice To")
    subtotal: Decimal = fd("Subtotal")
    tax: Decimal = fd("Tax")
    total: Decimal = fd("Total")
    items: List[InvoiceItem] = fd("Items")


@dataobject
@dataclass
class PaymentItem:
    """
    Payment Item
    """
    description: str = fd("Description")
    payment_date: datetime = fd("Payment date")
    amount: Decimal = fd("Amount")


@dataobject
@dataclass
class Payment:
    """
    Payment
    """
    payment_date: datetime = fd("Payment date")
    payment_number: str = fd("Payment number")
    remit_to: str = fd("Remit To")
    invoice_to: str = fd("Invoice To")
    total: Decimal = fd("Total")
    items: List[PaymentItem] = fd("Items")


@dataobject
@dataclass
class Subscription:
    """
    Subscription
    """
    start_date: datetime = fd("Start subscription date")
    plan: PlanInfo = fd("Plan")
    billing: BillingInfo = fd("Billing")
    user_id: str = fd("User ID")
    user_name: str = fd("User Name")
    company_id: str = fd("Company ID")
    company_name: str = fd("Company Name")
    registration: Optional[Registration] = fd("Registration Origin", default=None)
    end_date: Optional[datetime] = fd("End subscription date", default=None)
    invoices: List[Invoice] = fd("Invoices", default_factory=list)
    payments: List[Payment] = fd("Payments", default_factory=list)
    plan_history: List[PlanInfo] = fd("Plan history", default_factory=list)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
