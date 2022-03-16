"""
Claims Base Group services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.group import Group
from app0.admin.services import IDX_GROUP


# group services
async def get_groups(es) -> List[Group]:
    cursor = es[IDX_GROUP].find()
    return [Payload.from_obj(doc, Group) for doc in await cursor.to_list(length=100)]


async def get_group_by_name(es, name) -> Optional[Group]:
    if name:
        col = es[IDX_GROUP]
        doc = await col.find_one({'name': {'$eq': name}})
        if doc:
            return Payload.from_obj(doc, Group)
    return None


async def save_group(es, group: Group) -> Group:
    col = es[IDX_GROUP]
    await col.replace_one({'_id': ObjectId(group.id)}, Payload.to_obj(group), upsert=True)
    return group


async def delete_group(es, oid: str) -> dict:
    col = es[IDX_GROUP]
    return await col.delete_many({'_id': ObjectId(oid)})
