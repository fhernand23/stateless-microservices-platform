"""
App0 Admin User services
"""
from typing import List, Optional

from bson.objectid import ObjectId  # type: ignore
from hopeit.dataobjects.payload import Payload

from app0.admin.db import Query
from app0.admin.services import IDX_USER, IDX_USER_ROLE
from app0.admin.user import User, UserAppRole


async def get_users(es, search: str = None) -> List[User]:
    if search:
        cursor = es[IDX_USER].find({'$text': {'$search': search}})
    else:
        cursor = es[IDX_USER].find()
    return [Payload.from_obj(doc, User) for doc in await cursor.to_list(length=100)]


async def get_user_by_username(es, username: str) -> Optional[User]:
    col = es[IDX_USER]

    doc = await col.find_one({'username': {'$eq': username}})
    if not doc:
        return None

    return Payload.from_obj(doc, User)


async def get_user_by_employee(es, employee_id: str) -> Optional[User]:
    col = es[IDX_USER]
    doc = await col.find_one({'employee_id': {'$eq': employee_id}})
    if not doc:
        return None
    return Payload.from_obj(doc, User)


async def get_user(es, oid: str) -> Optional[User]:
    col = es[IDX_USER]
    doc = await col.find_one(ObjectId(oid))
    return Payload.from_obj(doc, User)


async def save_user(es, user: User) -> User:
    col = es[IDX_USER]
    await col.replace_one({'_id': ObjectId(user.id)}, Payload.to_obj(user), upsert=True)
    return user


async def delete_user(es, oid) -> dict:
    col = es[IDX_USER]
    return await col.delete_many({'_id': ObjectId(oid)})


async def get_user_roles_by_username(es, username) -> List[UserAppRole]:
    col = es[IDX_USER_ROLE]
    cursor = col.find({'username': {'$eq': username}})
    return [Payload.from_obj(doc, UserAppRole) for doc in await cursor.to_list(length=100)]


async def save_user_role(es, user_app_role: UserAppRole) -> UserAppRole:
    col = es[IDX_USER_ROLE]
    await col.replace_one({'_id': ObjectId(user_app_role.id)}, Payload.to_obj(user_app_role), upsert=True)
    return user_app_role


async def get_user_roles(es, query: Query) -> List[UserAppRole]:
    if query.flts:
        cursor = es[IDX_USER_ROLE].find(query.find_qry())
    else:
        cursor = es[IDX_USER_ROLE].find()
    return [Payload.from_obj(doc, UserAppRole) for doc in await cursor.to_list(length=query.max_items)]
