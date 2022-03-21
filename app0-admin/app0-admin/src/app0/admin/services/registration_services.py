"""
App0 Admin Registration services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.registration import Registration
from app0.admin.services import IDX_REGISTRATION


async def get_registrations(es, qry: Optional[Query] = None) -> List[Registration]:
    """
    Returns a list of queried Registration
    """
    sort_fld = 'name'
    sort_order = -1
    assert qry
    if qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        cursor = es[IDX_REGISTRATION].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_REGISTRATION].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, Registration) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_registration(es, oid: str) -> Optional[Registration]:
    col = es[IDX_REGISTRATION]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Registration) if doc else None


async def get_registration_by_mail(es, email: str) -> Optional[Registration]:
    col = es[IDX_REGISTRATION]

    doc = await col.find_one({'email': {'$eq': email}})
    if doc:
        return Payload.from_obj(doc, Registration)
    return None


async def save_registration(es, registration: Registration) -> Registration:
    col = es[IDX_REGISTRATION]
    await col.replace_one({'_id': ObjectId(registration.id)}, Payload.to_obj(registration), upsert=True)
    return registration


async def delete_registration(es, oid) -> dict:
    col = es[IDX_REGISTRATION]
    return await col.delete_many({'_id': ObjectId(oid)})
