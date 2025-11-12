
import asyncio
import json
from typing import Optional

try:
    import redis.asyncio as redis
except Exception:
    redis = None

class MemoryStore:
    def __init__(self):
        self._mem = {}

    async def get_session(self, session_id: str) -> Optional[dict]:
        return self._mem.get(session_id)

    async def set_session(self, session_id: str, data: dict):
        self._mem[session_id] = data

class RedisStore:
    def __init__(self, url: str):
        self.client = redis.from_url(url, decode_responses=True)

    async def get_session(self, session_id: str):
        raw = await self.client.get(f"session:{session_id}")
        return json.loads(raw) if raw else None

    async def set_session(self, session_id: str, data: dict):
        await self.client.set(f"session:{session_id}", json.dumps(data))

def get_store(url: str | None):
    if url and redis:
        return RedisStore(url)
    return MemoryStore()
