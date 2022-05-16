"""
App0Platform: Notification
"""
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject


from app0.admin import fd
from app0.admin.file import PlatformFile


@dataobject
@dataclass
class Notification:
    """
    Notification or log
    """
    creation_date: datetime = fd("Creation date")
    user_id: str = fd("User id", default="")
    user_name: str = fd("Username", default="")
    content: str = fd("Description or Text", default="")
    app_name: str = fd("App", default="")
    object_type: str = fd("Object type", default="")
    object_id: str = fd("Object id", default="")
    object_internal_id: Optional[str] = fd("Human readable id if exists", default=None)
    object_name: Optional[str] = fd("Object name if exists", default=None)
    type: str = fd("log/error/direct/upload/mail/call/papers/event/state-change"
                   "/estimation/negotiation/agreement/decline", default="log")
    dest_user_id: str = fd("Destination User id", default="")
    tags: str = fd("Tags", default="")
    id_file: Optional[str] = fd("Related file id", default=None)
    file_resource: Optional[PlatformFile] = fd("Related file resource", default=None)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
