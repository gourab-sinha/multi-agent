from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time


class MemoryProvider(ABC):
    """Base class for memory providers"""
    
    @classmethod
    def create(cls, config: Dict[str, Any]) -> 'MemoryProvider':
        """Create appropriate memory provider"""
        provider_type = config.get("provider", "local")
        
        if provider_type == "redis":
            from src.agentic.memory.redis_store import RedisMemoryProvider
            return RedisMemoryProvider(config)
        else:
            from src.agentic.memory.local_memory import LocalMemoryProvider
            return LocalMemoryProvider(config)
    
    @abstractmethod
    async def store(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Store value in memory"""
        pass
    
    @abstractmethod
    async def retrieve(
        self,
        key: str
    ) -> Optional[Any]:
        """Retrieve value from memory"""
        pass
    
    @abstractmethod
    async def delete(
        self,
        key: str
    ) -> bool:
        """Delete value from memory"""
        pass
    
    @abstractmethod
    async def exists(
        self,
        key: str
    ) -> bool:
        """Check if key exists"""
        pass