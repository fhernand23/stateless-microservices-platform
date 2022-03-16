"""
Platform Company Config: company-config-save
"""
from typing import Union

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload
from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook

from app0.admin.db import db
from app0.admin.http import HttpRespInfo
from app0.admin.services import IDX_COMPANY_CONFIG, ROLE_ADMIN
from app0.admin.company import CompanyConfig

__steps__ = ['run']

__api__ = event_api(
    payload=(CompanyConfig, "Object Info"),
    responses={
        200: (CompanyConfig, "Object updated"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: CompanyConfig, context: EventContext) -> Union[CompanyConfig, HttpRespInfo]:
    es = db(context.env)
    # check user admin
    if ROLE_ADMIN not in context.auth_info['payload'].get('roles', 'noauth'):
        return HttpRespInfo(403, 'User is not admin')

    await es[IDX_COMPANY_CONFIG].replace_one({'_id': ObjectId(payload.id)}, Payload.to_obj(payload), upsert=True)
    return payload


async def __postprocess__(payload: Union[CompanyConfig, HttpRespInfo], context: EventContext,
                          response: PostprocessHook) -> Union[CompanyConfig, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload
