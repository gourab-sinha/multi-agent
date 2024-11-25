from anthropic import Anthropic, CLAUDE_3_OPUS_20240229
from typing import Dict, Any, List
from ..base import LLMProvider, LLMResponse

class AnthropicProvider(LLMProvider):
    """Anthropic API provider"""
    
    def __init__(self, config: Dict[str, Any]):
        self.client = Anthropic(api_key=config["api_key"])
        self.model = config.get("model", CLAUDE_3_OPUS_20240229)
        self.max_tokens = config.get("max_tokens", 2000)
    
    async def generate(
        self,
        prompt: str,
        **kwargs: Any
    ) -> LLMResponse:
        try:
            response = await self.client.messages.create(
                model=kwargs.get("model", self.model),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return LLMResponse(
                text=response.content[0].text,
                tokens_used=response.usage.total_tokens,
                model=response.model,
                metadata={
                    "stop_reason": response.stop_reason,
                    "stop_sequence": response.stop_sequence
                }
            )
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def embed(
        self,
        text: str,
        **kwargs: Any
    ) -> List[float]:
        raise NotImplementedError("Embedding not supported for Anthropic")