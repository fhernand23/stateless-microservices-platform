"""
App0Platform: Token
"""
from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId  # type: ignore  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class AppToken:
    """
    App Access Token
    """
    creation_date: datetime = fd("Creation date")
    token_id: str = fd("Token id")
    expire: datetime = fd("Expiration date")
    user_id: str = fd("User id", default="")
    user_name: str = fd("Username", default="")
    provider_id: Optional[str] = fd("Provider Id", default=None)
    provider_name: Optional[str] = fd("Provider name", default=None)
    client_id: Optional[str] = fd("Client Id", default=None)
    client_name: Optional[str] = fd("Client name", default=None)
    app_name: str = fd("App", default="")
    object_type: str = fd("Object type", default="")
    object_id: str = fd("Object id", default="")
    id: Optional[str] = fd("Db id", default=None)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())
