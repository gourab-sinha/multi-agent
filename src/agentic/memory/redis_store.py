import json
import redis.asyncio as redis
from typing import Dict, Any, Optional
from src.agentic.memory.base import MemoryProvider

class RedisMemoryProvider(MemoryProvider):
    """Redis-based memory provider"""
    
    def __init__(self, config: Dict[str, Any]):
        self.redis = redis.Redis(
            host=config.get("host", "localhost"),
            port=config.get("port", 6379),
            password=config.get("password"),
            db=config.get("db", 0)
        )
    
    async def store(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        try:
            serialized = json.dumps(value)
            await self.redis.set(key, serialized, ex=ttl)
            return True
        except Exception as e:
            print(f"Redis store error: {str(e)}")
            return False
    
    async def retrieve(
        self,
        key: str
    ) -> Optional[Any]:
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis retrieve error: {str(e)}")
            return None
    
    async def delete(
        self,
        key: str
    ) -> bool:
        try:
            await self.redis.delete(key)
            return True
        except Exception:
            return False
    
    async def exists(
        self,
        key: str
    ) -> bool:
        try:
            return await self.redis.exists(key) > 0
        except Exception:
            return False