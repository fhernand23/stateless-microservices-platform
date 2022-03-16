"""
Claims Base Event services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.event import Event
from app0.admin.services import IDX_EVENT


async def get_events(es, qry: Query = None) -> List[Event]:
    """
    Returns a list of queried Event
    """
    sort_fld = 'event_date'
    sort_order = -1
    assert qry
    if qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        print(qry.find_qry())
        # {'enabled': {'$eq': True}}
        cursor = es[IDX_EVENT].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_EVENT].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, Event) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_event(es, oid: str) -> Optional[Event]:
    col = es[IDX_EVENT]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Event)


async def save_event(es, event: Event) -> Event:
    col = es[IDX_EVENT]
    await col.replace_one({'_id': ObjectId(event.id)}, Payload.to_obj(event), upsert=True)
    return event


async def delete_event(es, oid: str) -> dict:
    col = es[IDX_EVENT]
    return await col.delete_many({'_id': ObjectId(oid)})
