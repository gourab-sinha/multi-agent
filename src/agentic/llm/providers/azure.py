from typing import Dict, Any, List
import openai
from ..base import LLMProvider, LLMResponse

class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI API provider"""
    
    def __init__(self, config: Dict[str, Any]):
        openai.api_type = "azure"
        openai.api_base = config["api_base"]
        openai.api_version = config["api_version"]
        openai.api_key = config["api_key"]
        
        self.deployment_id = config["deployment_id"]
        self.max_tokens = config.get("max_tokens", 2000)
        self.temperature = config.get("temperature", 0.7)
    
    async def generate(
        self,
        prompt: str,
        **kwargs: Any
    ) -> LLMResponse:
        try:
            response = await openai.ChatCompletion.create(
                engine=self.deployment_id,
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
                model=self.deployment_id,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "created": response.created
                }
            )
            
        except Exception as e:
            raise Exception(f"Azure OpenAI API error: {str(e)}")
    
    async def embed(
        self,
        text: str,
        **kwargs: Any
    ) -> List[float]:
        try:
            response = await openai.Embedding.create(
                input=text,
                engine=self.deployment_id
            )
            return response.data[0].embedding
            
        except Exception as e:
            raise Exception(f"Azure OpenAI Embedding error: {str(e)}")