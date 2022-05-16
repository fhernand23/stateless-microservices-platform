"""
App0 Base Plan services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.services import IDX_PLAN
from app0.admin.subscription import AvailablePlan


async def get_plans(es, query: Query) -> List[AvailablePlan]:
    """
    Returns a list of queried AvailablePlan
    """
    sort_field = query.sort.field if query.sort else 'name'
    sort_order = query.sort.order if query.sort else 1

    if query.flts:
        cursor = es[IDX_PLAN].find(query.find_qry()).sort(sort_field, sort_order)
        # cursor = es[IDX_CLIENT].find({'enabled': {'$eq': True}})
    else:
        cursor = es[IDX_PLAN].find().sort(sort_field, sort_order)
    return [Payload.from_obj(doc, AvailablePlan) for doc in await cursor.to_list(length=query.max_items)]


async def get_plan(es, oid: str) -> Optional[AvailablePlan]:
    col = es[IDX_PLAN]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, AvailablePlan)


async def get_plan_by_name(es, name: str) -> Optional[AvailablePlan]:
    if name:
        col = es[IDX_PLAN]
        doc = await col.find_one({'name': {'$eq': name}})
        if doc:
            return Payload.from_obj(doc, AvailablePlan)
    return None


async def save_plan(es, plan: AvailablePlan) -> AvailablePlan:
    col = es[IDX_PLAN]
    await col.replace_one({'_id': ObjectId(plan.id)}, Payload.to_obj(plan), upsert=True)
    return plan


async def delete_plan(es, oid) -> dict:
    col = es[IDX_PLAN]
    return await col.delete_many({'_id': ObjectId(oid)})
