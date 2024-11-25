from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class LLMResponse(BaseModel):
    """Standardized LLM response"""
    text: str
    tokens_used: int
    model: str
    metadata: Optional[Dict[str, Any]] = None

class LLMProvider(ABC):
    """Base class for LLM providers"""
    
    @classmethod
    def create(cls, config: Dict[str, Any]) -> 'LLMProvider':
        """Create appropriate LLM provider"""
        provider = config.get("provider", "openai")
        
        if provider == "openai":
            from .providers.async_openai import AsyncOpenAIProvider
            return AsyncOpenAIProvider(config)
        elif provider == "anthropic":
            from .providers.anthropic import AnthropicProvider
            return AnthropicProvider(config)
        elif provider == "gemini":
            from .providers.gemini import GeminiProvider
            return GeminiProvider(config)
        elif provider == "azure":
            from .providers.azure import AzureOpenAIProvider
            return AzureOpenAIProvider(config)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        **kwargs: Any
    ) -> LLMResponse:
        """Generate text completion"""
        pass
    
    @abstractmethod
    async def embed(
        self,
        text: str,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings"""
        pass