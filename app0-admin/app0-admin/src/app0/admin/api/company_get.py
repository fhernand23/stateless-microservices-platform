"""
Platform Company: company-get
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.company import Company
from app0.admin.db import db
from app0.admin.services.company_services import get_company

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('company_id', str, "Company Id")
    ],
    responses={
        200: (Company, "Company"),
        404: (str, "Role not found")
    }
)


async def run(payload: None,
              context: EventContext,
              company_id: str) -> Optional[Company]:
    es = db(context.env)

    return await get_company(es, company_id)


async def __postprocess__(payload: Optional[Company], context: EventContext,
                          response: PostprocessHook) -> Union[Company, str]:
    if payload is None:
        response.status = 404
        return "Company not found"
    return payload
