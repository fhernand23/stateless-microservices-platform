"""
Claims Base App services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.app import AppDef, AppRole
from app0.admin.services import IDX_APP, IDX_ROLE


# apps services
async def get_apps(es) -> List[AppDef]:
    cursor = es[IDX_APP].find()
    return [Payload.from_obj(doc, AppDef) for doc in await cursor.to_list(length=100)]


async def get_app_by_name(es, name) -> Optional[AppDef]:
    if name:
        doc = await es[IDX_APP].find_one({'name': {'$eq': name}})
        return Payload.from_obj(doc, AppDef) if doc else None
    return None


async def get_app(es, oid: str) -> Optional[AppDef]:
    col = es[IDX_APP]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, AppDef)


async def get_apps_by_roles(es, roles: List[str]) -> List[AppDef]:
    if roles:
        cursor = es[IDX_APP].find({'default_role': {'$in': roles}})
        return [Payload.from_obj(doc, AppDef) for doc in await cursor.to_list(length=100)]
    return []


async def save_app(es, app_def: AppDef) -> AppDef:
    col = es[IDX_APP]
    await col.replace_one({'_id': ObjectId(app_def.id)}, Payload.to_obj(app_def), upsert=True)
    return app_def


async def delete_app(es, oid: str) -> dict:
    col = es[IDX_APP]
    return await col.delete_many({'_id': ObjectId(oid)})


# role services
async def get_roles(es) -> List[AppRole]:
    cursor = es[IDX_ROLE].find()
    return [Payload.from_obj(doc, AppRole) for doc in await cursor.to_list(length=100)]


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
