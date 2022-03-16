"""
Platform Company: company-data
"""
from typing import Optional, Union

from hopeit.app.api import event_api
from hopeit.app.context import EventContext, PostprocessHook
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query, db
from app0.admin.http import Dto, HttpRespInfo
from app0.admin.services import (IDX_COMPANY_MAIL, IDX_CLAIM, IDX_INSURANCE_COMPANY, IDX_DAMAGE, IDX_EMPLOYEE,
                                  IDX_PROVIDER, IDX_SUBSCRIPTION, ROLE_ADMIN)
from app0.admin.subscription import Subscription

__steps__ = ['run']
__api__ = event_api(
    query_args=[
        ('company_id', str, "Company Id"),
        ('category', Optional[str], "Category of data to get")
    ],
    payload=(Query, "Filters to search"),
    responses={
        200: (Dto, "Dict with info"),
        400: (str, "Bad request"),
        403: (str, "Operation forbidden"),
        404: (str, "Object not found")
    }
)


async def run(payload: Query, context: EventContext,
              company_id: str, category: Optional[str] = None) -> Union[Dto, HttpRespInfo]:
    """get company data"""
    es = db(context.env)
    if ROLE_ADMIN not in context.auth_info['payload'].get('roles', 'noauth'):
        return HttpRespInfo(403, 'User is not admin')

    if category == 'BASIC':
        result = await _get_basic_data(es, company_id)
        return result

    return HttpRespInfo(404, 'Not category provided')


async def __postprocess__(payload: Union[Dto, HttpRespInfo],
                          context: EventContext,
                          response: PostprocessHook) -> Union[Dto, str]:
    if isinstance(payload, HttpRespInfo):
        response.status = payload.code
        return payload.msg
    return payload


async def _get_basic_data(es, company_id: str) -> Dto:
    """
    Retrieve company data
    """
    # IDX_COMPANY_MAIL, IDX_CLAIM, IDX_INSURANCE_COMPANY, IDX_DAMAGE
    result = {}
    result['claims'] = await es[IDX_CLAIM].count_documents({'owner_id': {'$eq': company_id}})
    result['insurance_companies'] = await es[IDX_INSURANCE_COMPANY].count_documents({'owner_id': {'$eq': company_id}})
    result['damages'] = await es[IDX_DAMAGE].count_documents({'owner_id': {'$eq': company_id}})
    result['tmails'] = await es[IDX_COMPANY_MAIL].count_documents({'owner_id': {'$eq': company_id}})
    result['employees'] = await es[IDX_EMPLOYEE].count_documents({'owner_id': {'$eq': company_id}})
    result['employees_pub_adjusters'] = await es[IDX_EMPLOYEE].count_documents(
        {'$and': [{'owner_id': {'$eq': company_id}},
                  {'public_adjuster_license': {'$eq': True}}]})
    result['service_providers'] = await es[IDX_PROVIDER].count_documents({'owner_id': {'$eq': company_id}})
    # get subscription data
    cursor = es[IDX_SUBSCRIPTION].find({'company_id': {'$eq': company_id}})
    doc: Optional[Subscription] = None
    for d in await cursor.to_list(length=1):
        doc = Payload.from_obj(d, Subscription)
    if doc:
        result['subscription_desc'] = doc.plan.name + ' - ' + doc.plan.description
        result['subscription_max_open_claims'] = doc.plan.max_open_claims
        result['subscription_max_adjusters'] = doc.plan.max_adjusters
    else:
        result['subscription_desc'] = 'No subscription found'

    return Dto(o=result)


async def _get_setup_data(es, company_id: str) -> Dto:
    """get company summary info"""
    # IDX_COMPANY_MAIL, IDX_CLAIM, IDX_INSURANCE_COMPANY, IDX_DAMAGE
    result = {}
    result['claims'] = await es[IDX_CLAIM].count_documents({'owner_id': {'$eq': company_id}})
    result['tmails'] = await es[IDX_COMPANY_MAIL].count_documents({'owner_id': {'$eq': company_id}})
    result['employees'] = await es[IDX_EMPLOYEE].count_documents({'owner_id': {'$eq': company_id}})
    result['employees_pub_adjusters'] = await es[IDX_EMPLOYEE].count_documents(
        {'$and': [{'owner_id': {'$eq': company_id}},
                  {'public_adjuster_license': {'$eq': True}}]})
    # get subscription data
    doc = await es[IDX_SUBSCRIPTION].find_one({'company_id': {'$eq': company_id}})
    if doc:
        subscription = Payload.from_obj(doc, Subscription)
        result['subscription_desc'] = subscription.plan.name + ' - ' + subscription.plan.description
        result['subscription_max_open_claims'] = subscription.plan.max_open_claims
        result['subscription_max_adjusters'] = subscription.plan.max_adjusters
    else:
        result['subscription_desc'] = 'No subscription found'

    return Dto(o=result)
