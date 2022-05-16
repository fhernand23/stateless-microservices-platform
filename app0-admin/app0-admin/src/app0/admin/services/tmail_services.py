"""
Platform Tmail services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.services import IDX_BASE_MAIL
from app0.admin.tmail import MailTemplate, Tmail


async def get_tmails(es, query: Query) -> List[Tmail]:
    """
    Returns a list of queried Tmail
    """
    sort_field = query.sort.field if query.sort else 'name'
    sort_order = query.sort.order if query.sort else 1

    if query.flts:
        cursor = es[IDX_BASE_MAIL].find(query.find_qry()).sort(sort_field, sort_order)
    else:
        cursor = es[IDX_BASE_MAIL].find().sort(sort_field, sort_order)
    return [Payload.from_obj(doc, Tmail) for doc in await cursor.to_list(length=query.max_items)]


async def get_tmail(es, oid: str) -> Optional[Tmail]:
    col = es[IDX_BASE_MAIL]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Tmail)


async def save_tmail(es, tmail: Tmail) -> Tmail:
    col = es[IDX_BASE_MAIL]
    await col.replace_one({'_id': ObjectId(tmail.id)}, Payload.to_obj(tmail), upsert=True)
    return tmail


async def get_tmail_by_name(es, template: MailTemplate) -> Optional[Tmail]:
    """Get template mail by collection-name"""
    col = es[template.collection]
    doc = await col.find_one({'name': {'$eq': template.name}})
    if not doc:
        return None

    return Payload.from_obj(doc, Tmail)
