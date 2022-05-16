"""
App0Platform: App
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class AppRole:
    """
    Application role
    """
    name: str = fd("Role name")
    description: str = fd("Description")
    id: Optional[str] = None
    enabled: bool = fd("Document enabled", default=True)
    application: Optional[str] = fd("Application", default=None)
    can_delete: bool = fd("Can be deleted?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class AppDef:
    """
    Application definition
    """
    name: str = fd("Name")
    description: str = fd("Description")
    url: str = fd("Url Info")
    image: Optional[str] = fd("Principal app image", default=None)
    default_role: str = fd("Default App Role", default=None)
    roles: List[str] = fd("List of App Roles", default_factory=list)
    id: Optional[str] = None
    enabled: bool = fd("Document enabled", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
