"""
App0Platform: Files
"""
from datetime import datetime, timezone
from dataclasses import field
from typing import List, Optional

from app0.admin import fd
from hopeit.dataobjects import BinaryDownload, dataclass, dataobject


@dataobject
@dataclass
class PlatformFile:
    """
    File uploaded
    """
    bucket: str = fd("Bucket")
    filename: str = fd("Filename")
    size: int = fd("Size")
    src_filename: str = fd("Source filename")
    object_id: str = fd("Full path filename Object Id")
    creation_date: Optional[datetime] = fd("Creation Date", default=None)

    def __post_init__(self):
        if self.creation_date is None:
            self.creation_date = datetime.now(tz=timezone.utc)


@dataclass
class ImgFile(BinaryDownload):
    """Image File info"""
    file_name: str
    file_path: str
    content_type: str = "application/octet-stream"
    content_disposition: Optional[str] = fd("Content disposition", default=None)


@dataobject
@dataclass
class UploadedFiles:
    """List of uploaded files"""
    uploaded_files: List[PlatformFile] = field(default_factory=list)
