"""
App0Platform: Event
"""
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd
from app0.admin.common import SimplePerson, IdDescription


@dataobject
@dataclass
class Event:
    """
    Calendar Event
    """
    creation_date: datetime = fd("Creation date")
    event_date: datetime = fd("Event date")
    people: List[SimplePerson] = fd("Event guests")
    type: Optional[IdDescription] = fd("Event type", default=None)
    notes: str = fd("Notes", default="")
    user_id: str = fd("User id", default="")
    user_name: str = fd("Username", default="")
    owner_id: str = fd("owner id", default="")
    owner_name: str = fd("owner name", default="")
    app_name: str = fd("App", default="")
    object_type: str = fd("Object type", default="")
    object_id: str = fd("Object id", default="")
    address: Optional[str] = fd("Address", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
