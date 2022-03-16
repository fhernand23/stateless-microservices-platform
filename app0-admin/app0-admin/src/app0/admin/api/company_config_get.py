"""
Platform Company Config: company-config-get
"""
from typing import Optional, Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.dataobjects.payload import Payload

from app0.admin.db import db
from app0.admin.services import IDX_COMPANY_CONFIG
from app0.admin.company import CompanyConfig

__steps__ = ['run']

__api__ = event_api(
    query_args=[
        ('obj_id', Optional[str], "Object ID"),
        ('company_id', Optional[str], "company id")
    ],
    responses={
        200: (CompanyConfig, "CompanyConfig"),
        404: (str, "Object not found")
    }
)


async def run(payload: None, context: EventContext, obj_id: Optional[str] = None,
              company_id: Optional[str] = None) -> Optional[CompanyConfig]:
    """get CompanyConfig"""
    es = db(context.env)
    if obj_id:
        doc = await es[IDX_COMPANY_CONFIG].find_one(ObjectId(obj_id))
        if doc:
            return Payload.from_obj(doc, CompanyConfig)
    elif company_id:
        doc = await es[IDX_COMPANY_CONFIG].find_one({'owner_id': {'$eq': company_id}})
        if doc:
            return Payload.from_obj(doc, CompanyConfig)

    return None


async def __postprocess__(payload: Optional[CompanyConfig], context: EventContext,
                          response: PostprocessHook) -> Union[CompanyConfig, str]:
    if payload:
        return payload
    response.status = 404
    return "Object not found"
