"""
App0 Admin Registration services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.registration import Registration
from app0.admin.services import IDX_REGISTRATION


async def get_registrations(es, query: Query) -> List[Registration]:
    """
    Returns a list of queried Registration
    """
    sort_field = query.sort.field if query.sort else 'creation_date'
    sort_order = query.sort.order if query.sort else -1

    if query.flts:
        cursor = es[IDX_REGISTRATION].find(query.find_qry()).sort(sort_field, sort_order)
    else:
        cursor = es[IDX_REGISTRATION].find().sort(sort_field, sort_order)
    return [Payload.from_obj(doc, Registration) for doc in await cursor.to_list(length=query.max_items)]


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
