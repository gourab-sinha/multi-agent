import google.generativeai as genai
from typing import Dict, Any, List
from ..base import LLMProvider, LLMResponse

class GeminiProvider(LLMProvider):
    """Google Gemini API provider"""
    
    def __init__(self, config: Dict[str, Any]):
        genai.configure(api_key=config["api_key"])
        self.model = genai.GenerativeModel('gemini-pro')
        self.max_tokens = config.get("max_tokens", 2000)
        self.temperature = config.get("temperature", 0.7)
    
    async def generate(
        self,
        prompt: str,
        **kwargs: Any
    ) -> LLMResponse:
        try:
            response = await self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature)
                }
            )
            
            return LLMResponse(
                text=response.text,
                tokens_used=0,  # Gemini doesn't provide token count
                model="gemini-pro",
                metadata={
                    "prompt_feedback": response.prompt_feedback,
                    "candidates": len(response.candidates)
                }
            )
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def embed(
        self,
        text: str,
        **kwargs: Any
    ) -> List[float]:
        raise NotImplementedError("Embedding not supported for Gemini")