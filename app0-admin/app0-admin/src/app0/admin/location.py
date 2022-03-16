"""
App0Platform: Location
"""
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class State:
    """
    State
    """
    id: Optional[str] = fd("Db id", default=None)
    name: str = fd("State", default="")
    abbr: str = fd("State abbreviation", default="")

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class County:
    """
    County
    """
    id: Optional[str] = fd("Db id", default=None)
    name: str = fd("County", default="")
    abbr: str = fd("County abbreviation", default="")

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class City:
    """
    City
    """
    id: Optional[str] = fd("Db id", default=None)
    name: str = fd("Name", default="")
    state: Optional[State] = fd("State", default=None)
    county: Optional[County] = fd("County", default=None)
    zip_code: str = fd("Zip code", default="")

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class Address:
    """
    Address
    """
    description: str = fd("Street & Number", default="")
    city: Optional[City] = fd("City", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
