"""
Platform Tools: enum-list
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

# from app0.admin.enums import config_path
from app0.admin.http import Dto
# from app0.admin.enums import Enum

logger, extra = app_extra_logger()

__steps__ = ['get_lists']
__api__ = event_api(
    query_args=[
        ("list_type", str, "List type"),
    ],
    responses={
        200: (List[Dto], "List of Dicts with info")
    }
)


async def get_lists(payload: None,
                    context: EventContext,
                    list_type: str) -> List[Dto]:
    """Get enums as list of DTOs"""
    return []
