from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize plugin"""
        pass
    
    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute plugin functionality"""
        pass