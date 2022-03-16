"""
Claims Base Subscription services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.services import IDX_SUBSCRIPTION
from app0.admin.subscription import Subscription


async def get_subscriptions(es, qry: Query = None) -> List[Subscription]:
    """
    Returns a list of queried Suscription
    """
    sort_fld = 'name'
    sort_order = -1
    assert qry
    if qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        cursor = es[IDX_SUBSCRIPTION].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_SUBSCRIPTION].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, Subscription) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_subscription(es, oid: str) -> Optional[Subscription]:
    col = es[IDX_SUBSCRIPTION]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Subscription)


async def get_subscription_by_email(es, email: str) -> Optional[Subscription]:
    col = es[IDX_SUBSCRIPTION]
    doc = await col.find_one({'email': {'$eq': email}})
    if doc:
        return Payload.from_obj(doc, Subscription)
    return None


async def get_subscription_by_company(es, company_id: str) -> Optional[Subscription]:
    col = es[IDX_SUBSCRIPTION]
    doc = await col.find_one({'company_id': {'$eq': company_id}})
    if doc:
        return Payload.from_obj(doc, Subscription)
    return None


async def save_subscription(es, subscription: Subscription) -> Subscription:
    col = es[IDX_SUBSCRIPTION]
    await col.replace_one({'_id': ObjectId(subscription.id)}, Payload.to_obj(subscription), upsert=True)
    return subscription


async def delete_subscription(es, oid) -> dict:
    col = es[IDX_SUBSCRIPTION]
    return await col.delete_many({'_id': ObjectId(oid)})
