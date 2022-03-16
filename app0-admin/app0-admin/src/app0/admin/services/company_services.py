"""
Claims Base Company services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.company import Company
from app0.admin.services import IDX_COMPANY


async def get_companies(es, qry: Optional[Query] = None) -> List[Company]:
    """
    Returns a list of queried Companies
    """
    sort_fld = 'name'
    sort_order = 1
    assert qry
    if qry.sort:
        sort_fld = qry.sort.fld
        sort_order = qry.sort.rdr
    if qry and qry.flts:
        cursor = es[IDX_COMPANY].find(qry.find_qry()).sort(sort_fld, sort_order)
    else:
        cursor = es[IDX_COMPANY].find().sort(sort_fld, sort_order)
    return [Payload.from_obj(doc, Company) for doc in await cursor.to_list(length=qry.max_items if qry else 100)]


async def get_company_by_name(es, name) -> Optional[Company]:
    if name:
        doc = await es[IDX_COMPANY].find_one({'name': {'$eq': name}})
        if doc:
            return Payload.from_obj(doc, Company)
    return None


async def get_company(es, oid: str) -> Optional[Company]:
    col = es[IDX_COMPANY]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, Company)


async def save_company(es, company: Company) -> Company:
    col = es[IDX_COMPANY]
    await col.replace_one({'_id': ObjectId(company.id)}, Payload.to_obj(company), upsert=True)
    return company


async def delete_company(es, oid) -> dict:
    col = es[IDX_COMPANY]
    return await col.delete_many({'_id': ObjectId(oid)})
