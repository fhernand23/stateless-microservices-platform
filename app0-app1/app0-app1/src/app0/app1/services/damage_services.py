"""
Damage Services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.damage import Damage
from app0.app1.services import IDX_DAMAGE
from app0.admin.db import Query


async def get_damages(es, query: Optional[Query] = None) -> List[Damage]:
    assert query
    if query.flts:
        cursor = es[IDX_DAMAGE].find(query.find_qry())
    else:
        cursor = es[IDX_DAMAGE].find()
    return [Payload.from_obj(doc, Damage) for doc in await cursor.to_list(length=query.max_items)]


async def get_damage(es, obj_id: str) -> Optional[Damage]:
    col = es[IDX_DAMAGE]

    doc = await col.find_one(ObjectId(obj_id))

    return Payload.from_obj(doc, Damage)


async def save_damage(es, damage: Damage) -> Damage:
    col = es[IDX_DAMAGE]
    await col.replace_one({'_id': ObjectId(damage.id)}, Payload.to_obj(damage), upsert=True)

    return damage


async def delete_damage(es, obj_id) -> dict:
    col = es[IDX_DAMAGE]

    return await col.delete_many({'_id': ObjectId(obj_id)})
