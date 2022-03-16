"""
Claims Base Tmail services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.services import IDX_BASE_MAIL, IDX_COMPANY_MAIL
from app0.admin.tmail import MailTemplate, Tmail


async def get_tmails(es, qry: Query = None) -> List[Tmail]:
    """
    Returns a list of queried Tmail
    """
    sort_fld = 'name'
    sort_order = -1
    if qry and qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        cursor = es[IDX_BASE_MAIL].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_BASE_MAIL].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, Tmail) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_tmail(es, oid: str) -> Optional[Tmail]:
    col = es[IDX_BASE_MAIL]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Tmail)


async def save_tmail(es, tmail: Tmail) -> Tmail:
    col = es[IDX_BASE_MAIL]
    await col.replace_one({'_id': ObjectId(tmail.id)}, Payload.to_obj(tmail), upsert=True)
    return tmail


async def get_tmail_by_name(es, template: MailTemplate) -> Optional[Tmail]:
    """Get template mail by collection-name-owner_id"""
    col = es[template.collection]

    if template.owner_id:
        doc = await col.find_one({'$and': [{'owner_id': {'$eq': template.owner_id}},
                                           {'name': {'$eq': template.name}}]})
    else:
        doc = await col.find_one({'name': {'$eq': template.name}})
    if not doc:
        return None

    return Payload.from_obj(doc, Tmail)


async def get_company_tmails(es, qry: Query = None) -> List[Tmail]:
    """
    Returns a list of queried Tmail
    """
    sort_fld = 'name'
    sort_order = -1
    if qry and qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        cursor = es[IDX_COMPANY_MAIL].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_COMPANY_MAIL].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, Tmail) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_company_tmail(es, oid: str) -> Optional[Tmail]:
    col = es[IDX_COMPANY_MAIL]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Tmail)


async def save_company_tmail(es, tmail: Tmail) -> Tmail:
    col = es[IDX_COMPANY_MAIL]
    await col.replace_one({'_id': ObjectId(tmail.id)}, Payload.to_obj(tmail), upsert=True)
    return tmail
