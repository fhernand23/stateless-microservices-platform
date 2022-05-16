"""
App0Platform: Subscription
"""
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


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
    end_date: Optional[datetime] = fd("End subscription date", default=None)
