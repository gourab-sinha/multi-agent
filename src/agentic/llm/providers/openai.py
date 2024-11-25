from openai import OpenAI
from typing import Dict, Any, List
from src.agentic.llm.base import LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    """OpenAI API provider using the new 1.0.0+ client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.client = OpenAI(api_key=config["api_key"])
        self.model = config.get("model", "gpt-4")
        self.max_tokens = config.get("max_tokens", 2000)
        self.temperature = config.get("temperature", 0.7)
    
    async def generate(
        self,
        prompt: str,
        **kwargs: Any
    ) -> LLMResponse:
        try:
            # The new OpenAI client is synchronous
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                n=1
            )
            
            return LLMResponse(
                text=response.choices[0].message.content,
                tokens_used=response.usage.total_tokens,
                model=response.model,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "created": response.created
                }
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def embed(
        self,
        text: str,
        **kwargs: Any
    ) -> List[float]:
        try:
            # The new OpenAI client is synchronous
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            raise Exception(f"OpenAI Embedding error: {str(e)}")