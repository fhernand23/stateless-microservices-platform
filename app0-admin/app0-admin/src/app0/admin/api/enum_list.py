"""
Platform Tools: enum-list
"""
from typing import List

from hopeit.app.api import event_api
from hopeit.app.context import EventContext
from hopeit.app.logger import app_extra_logger

from app0.admin.enums import config_path
from app0.admin.http import Dto
from app0.admin.enums import Enum

logger, extra = app_extra_logger()
EmployeePosition = Enum.load_csv(config_path, "EmployeePosition", '*')
ProviderType = Enum.load_csv(config_path, "ProviderType", '*')

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
    if list_type == "EmployeePosition":
        return [Dto({'id': a['id'], 'name': a['name']}) for a in EmployeePosition]
    if list_type == "ProviderType":
        return [Dto({'id': d['id'], 'name': d['name']}) for d in ProviderType]

    return []
