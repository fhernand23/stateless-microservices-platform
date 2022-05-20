"""
App0Platform: Tmail
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects import dataclass, dataobject

from app0.admin import fd


@dataobject
@dataclass
class Tmail:
    """
    Mail template
    """
    name: str = fd("Key Name")
    subject: str = fd("Subject")
    template: str = fd("Template file")
    description: str = fd("Description", default="")
    keywords: List[str] = fd("All variables that can be setted", default_factory=list)
    keywords_required: List[str] = fd("Mandatory variables that should be setted", default_factory=list)
    content: Optional[str] = fd("Html Content embedded in template", default=None)
    tags: List[str] = fd("Tags", default_factory=list)
    id: Optional[str] = fd("Db id", default=None)
    enabled: bool = fd("Enabled?", default=True)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class MailAttachment:
    """Mail attachment"""
    doc_id: str = fd("Document Id", default="")
    doc_name: str = fd("Document Name", default="")


@dataobject
@dataclass
class TmailSend:
    """
    Mail template send
    """
    template: str = fd("Template name")
    destinations: List[str] = fd("Destinations", default_factory=list)
    replacements: Optional[Dict[str, str]] = fd("Text to dynamic replace", default=None)
    files: List[MailAttachment] = fd("Files to attach", default_factory=list)
    sent_date: datetime = fd("Start subscription date", default=None)
    sent_message: str = fd("Start subscription date", default="")
    id: Optional[str] = fd("Db id", default=None)

    def __post_init__(self):
        if self.id is None:
            self.id = str(ObjectId())


@dataobject
@dataclass
class MailLog:
    subject: str
    destination: str
    log_date: datetime = datetime.now(tz=timezone.utc)
    message_id: Optional[str] = None
    error: Optional[str] = None
