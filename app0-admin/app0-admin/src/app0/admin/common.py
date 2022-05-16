"""
App0Platform: Common
"""
from typing import Dict, Optional, List

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class IdDescription:
    """
    Id with description
    """
    value: str = fd("ObjectId")
    label: str = fd("Description")
    internal_id: Optional[str] = fd("Human readable internalID", default=None)
    details: Optional[Dict[str, str]] = fd("Human readable internalID", default=None)


@dataobject
@dataclass
class IdDescriptionField:
    """
    Id with description
    """
    value: str = fd("Id")
    label: str = fd("Description")
    fld_name_date: str = fd("Field Name to set date")
    fld_name_resource: str = fd("Field Name to set resource", default=None)


@dataobject
@dataclass
class ActionDetail:
    """
    Action - Subaction - WF
    """
    name: str = fd("Subaction name")
    desc: str = fd("Subaction description")
    wf_action: Optional[str] = fd("Action that change workflow state", default=None)


@dataobject
@dataclass
class SimplePerson:
    """
    Simple Person
    """
    role: str = fd("Role")
    name: str = fd("Name")
    id: Optional[str] = fd("Id", default=None)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class AddressGeoJson:
    """
    GeoJson
    """
    type: str = fd("Type", default="")
    coordinates: List[float] = fd("Coordinates", default_factory=list)
