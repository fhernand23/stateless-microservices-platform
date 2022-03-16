"""
App0Platform: Damage
"""
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.location import City, State, County


@dataobject
@dataclass
class Damage:
    """
    Damage
    """
    name: str = fd("Name")
    category: str = fd("Category")
    image: str = fd("Related image", default='')
    owner_id: Optional[str] = fd("Owner Id", default=None)
    owner_name: Optional[str] = fd("Owner Name", default=None)
    id: Optional[str] = fd("Db id", default=None)
    description: Optional[str] = fd("description", default=None)
    enabled: bool = fd("Enabled?", default=True)
    from_date: Optional[datetime] = fd("From Date", default=None)
    to_date: Optional[datetime] = fd("To Date", default=None)
    states: List[State] = fd("States", default_factory=list)
    counties: List[County] = fd("Counties", default_factory=list)
    cities: List[City] = fd("Cities", default_factory=list)
    notes: Optional[str] = fd("Notes", default=None)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
