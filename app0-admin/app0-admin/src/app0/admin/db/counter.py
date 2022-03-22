"""
Counter Module
"""
import os

import aioredis


async def incr(key: str) -> int:
    """
    Save and return next number for a certain key.
    This function store data in redis.
    """
    redis_url = os.getenv('REDIS_URL')

    assert redis_url is not None, "Cannot get value from OS environment var: REDIS_URL"
    redis = aioredis.from_url(redis_url)
    async with redis.client() as conn:
        return await conn.incr(key)
