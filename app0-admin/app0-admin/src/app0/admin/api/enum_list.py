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
BaseDamages = Enum.load_csv(config_path, "BaseDamages", '*')
BaseInsuranceCompanies = Enum.load_csv(config_path, "BaseInsuranceCompanies", '*')
BaseMails = Enum.load_csv(config_path, "BaseMails", '*')

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
    if list_type == "BaseDamages":
        return [Dto({'id': a['id'], 'name': a['name']}) for a in BaseDamages]
    if list_type == "BaseInsuranceCompanies":
        return [Dto({'id': d['id'], 'name': d['name']}) for d in BaseInsuranceCompanies]
    if list_type == "BaseMails":
        return [Dto({'id': d['id'], 'name': d['name']}) for d in BaseMails]

    return []
