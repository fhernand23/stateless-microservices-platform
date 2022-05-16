"""
App0 Admin Notification services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.notification import Notification
from app0.admin.services import IDX_NOTIFICATION


async def get_notifications(es, query: Query) -> List[Notification]:
    """
    Returns a list of queried Notification
    """
    sort_field = query.sort.field if query.sort else 'creation_date'
    sort_order = query.sort.order if query.sort else -1

    if query.flts:
        cursor = es[IDX_NOTIFICATION].find(query.find_qry()).sort(sort_field, sort_order)
    else:
        cursor = es[IDX_NOTIFICATION].find().sort(sort_field, sort_order)
    return [Payload.from_obj(doc, Notification) for doc in await cursor.to_list(length=query.max_items)]


async def get_notification(es, oid: str) -> Optional[Notification]:
    col = es[IDX_NOTIFICATION]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Notification)


async def save_notification(es, notification: Notification) -> Notification:
    col = es[IDX_NOTIFICATION]
    await col.replace_one({'_id': ObjectId(notification.id)}, Payload.to_obj(notification), upsert=True)
    return notification


async def delete_notification(es, oid: str) -> dict:
    col = es[IDX_NOTIFICATION]
    return await col.delete_many({'_id': ObjectId(oid)})
