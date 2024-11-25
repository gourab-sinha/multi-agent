from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseTool(ABC):
    """Base class for all tools"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute tool functionality"""
        pass
    
    async def validate_parameters(
        self,
        parameters: Dict[str, Any]
    ) -> bool:
        """Validate input parameters"""
        return True