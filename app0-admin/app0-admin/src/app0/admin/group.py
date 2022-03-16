"""
App0Platform: Group
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class Group:
    """
    Group
    """
    name: str = fd("Name")
    description: str = fd("Description")
    tags: List[str] = fd("Tags", default_factory=list)
    id_parent_group: Optional[str] = fd("Higher hierarchy group", default=None)
    id_responsible: List[str] = fd("Heads of the Group", default_factory=list)
    roles: List[str] = fd("Group roles", default_factory=list)
    users: List[str] = fd("Users belonging to the group", default_factory=list)
    id: Optional[str] = None
    enabled: Optional[bool] = None

    def __post_init__(self):
        if self.enabled is None:
            self.enabled = True
        if self.id is None:
            self.id = str(ObjectId())
