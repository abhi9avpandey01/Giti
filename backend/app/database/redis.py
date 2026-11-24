import json
from typing import Any, Optional
import redis.asyncio as aioredis
from app.config import settings

_redis_client: Optional[aioredis.Redis] = None


async def get_redis_client() -> Optional[aioredis.Redis]:
    """Get async Redis client singleton."""
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception:
            _redis_client = None
    return _redis_client


async def cache_get(key: str) -> Optional[Any]:
    """Retrieve JSON-deserialized value from Redis."""
    try:
        client = await get_redis_client()
        if not client:
            return None
        val = await client.get(key)
        return json.loads(val) if val else None
    except Exception:
        return None


async def cache_set(key: str, value: Any, expire_seconds: int = 3600) -> bool:
    """Store JSON-serialized value into Redis with TTL."""
    try:
        client = await get_redis_client()
        if not client:
            return False
        await client.set(key, json.dumps(value), ex=expire_seconds)
        return True
    except Exception:
        return False
