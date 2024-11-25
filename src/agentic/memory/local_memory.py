from typing import Dict, Any, Optional
import time
from src.agentic.memory.base import MemoryProvider


class LocalMemoryProvider(MemoryProvider):
    """Local in-memory storage provider"""
    
    def __init__(self, config: Dict[str, Any]):
        self.storage: Dict[str, Dict[str, Any]] = {}
        self.max_size = config.get("max_size", 1000)
    
    async def store(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        try:
            if len(self.storage) >= self.max_size:
                self._cleanup()
                
            self.storage[key] = {
                "value": value,
                "timestamp": time.time(),
                "ttl": ttl
            }
            return True
        except Exception:
            return False
    
    async def retrieve(
        self,
        key: str
    ) -> Optional[Any]:
        try:
            data = self.storage.get(key)
            if not data:
                return None
                
            if self._is_expired(data):
                await self.delete(key)
                return None
                
            return data["value"]
        except Exception:
            return None
    
    async def delete(
        self,
        key: str
    ) -> bool:
        try:
            if key in self.storage:
                del self.storage[key]
            return True
        except Exception:
            return False
    
    async def exists(
        self,
        key: str
    ) -> bool:
        try:
            data = self.storage.get(key)
            if not data:
                return False
            
            if self._is_expired(data):
                await self.delete(key)
                return False
                
            return True
        except Exception:
            return False
    
    def _is_expired(self, data: Dict[str, Any]) -> bool:
        """Check if data is expired"""
        if not data.get("ttl"):
            return False
            
        return time.time() - data["timestamp"] > data["ttl"]
    
    def _cleanup(self):
        """Clean up expired entries"""
        current_time = time.time()
        keys_to_delete = []
        
        for key, data in self.storage.items():
            if data.get("ttl") and current_time - data["timestamp"] > data["ttl"]:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.storage[key]