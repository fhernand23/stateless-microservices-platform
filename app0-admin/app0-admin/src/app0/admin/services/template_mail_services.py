"""
App0 Admin TemplateMail services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.services import IDX_TEMPLATE_MAIL
from app0.admin.template_mail import TemplateMail


async def get_template_mails(es, qry: Query = None) -> List[TemplateMail]:
    """
    Returns a list of queried TemplateMail
    """
    sort_fld = 'name'
    sort_order = -1
    if qry and qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        cursor = es[IDX_TEMPLATE_MAIL].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_TEMPLATE_MAIL].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, TemplateMail) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_template_mail(es, oid: str) -> Optional[TemplateMail]:
    col = es[IDX_TEMPLATE_MAIL]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, TemplateMail)


async def save_template_mail(es, tmail: TemplateMail) -> TemplateMail:
    col = es[IDX_TEMPLATE_MAIL]
    await col.replace_one({'_id': ObjectId(tmail.id)}, Payload.to_obj(tmail), upsert=True)
    return tmail


async def get_template_mail_by_name(es, template: str) -> Optional[TemplateMail]:
    """Get template mail by name"""
    col = es[IDX_TEMPLATE_MAIL]
    doc = await col.find_one({'name': {'$eq': template}})
    if not doc:
        return None

    return Payload.from_obj(doc, TemplateMail)
