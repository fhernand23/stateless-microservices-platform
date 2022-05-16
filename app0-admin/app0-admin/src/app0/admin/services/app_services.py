"""
App0 Admin App services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.app import AppDef, AppRole
from app0.admin.services import IDX_APP, IDX_ROLE


# apps services
async def get_apps(es, query: Query) -> List[AppDef]:
    sort_field = query.sort.field if query.sort else 'name'
    sort_order = query.sort.order if query.sort else 1

    if query.flts:
        cursor = es[IDX_APP].find(query.find_qry()).sort(sort_field, sort_order)
    else:
        cursor = es[IDX_APP].find().sort(sort_field, sort_order)
    return [Payload.from_obj(doc, AppDef) for doc in await cursor.to_list(length=query.max_items)]


async def get_app_by_name(es, name) -> Optional[AppDef]:
    if name:
        doc = await es[IDX_APP].find_one({'name': {'$eq': name}})
        return Payload.from_obj(doc, AppDef) if doc else None
    return None


async def get_app(es, oid: str) -> Optional[AppDef]:
    col = es[IDX_APP]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, AppDef)


async def save_app(es, app_def: AppDef) -> AppDef:
    col = es[IDX_APP]
    await col.replace_one({'_id': ObjectId(app_def.id)}, Payload.to_obj(app_def), upsert=True)
    return app_def


async def delete_app(es, oid: str) -> dict:
    col = es[IDX_APP]
    return await col.delete_many({'_id': ObjectId(oid)})


# role services
async def get_roles(es, query: Query) -> List[AppRole]:
    sort_field = query.sort.field if query.sort else 'name'
    sort_order = query.sort.order if query.sort else 1

    if query.flts:
        cursor = es[IDX_ROLE].find(query.find_qry()).sort(sort_field, sort_order)
    else:
        cursor = es[IDX_ROLE].find().sort(sort_field, sort_order)
    return [Payload.from_obj(doc, AppRole) for doc in await cursor.to_list(length=query.max_items)]


async def get_role_by_name(es, name) -> Optional[AppRole]:
    if name:
        col = es[IDX_ROLE]
        doc = await col.find_one({'name': {'$eq': name}})
        if doc:
            return Payload.from_obj(doc, AppRole)
    return None


async def get_role(es, oid: str) -> Optional[AppRole]:
    col = es[IDX_ROLE]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, AppRole)


async def save_role(es, app_role: AppRole) -> AppRole:
    col = es[IDX_ROLE]
    await col.replace_one({'_id': ObjectId(app_role.id)}, Payload.to_obj(app_role), upsert=True)
    return app_role


async def delete_role(es, oid) -> dict:
    col = es[IDX_ROLE]
    return await col.delete_many({'_id': ObjectId(oid)})
