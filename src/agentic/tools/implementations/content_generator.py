from typing import Dict, Any, List, Optional
from src.agentic.tools.base import BaseTool
import asyncio

class ContentGeneratorTool(BaseTool):
    """Tool for generating various types of content"""
    
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        content_type = parameters.get("type", "text")
        try:
            if content_type == "text":
                return await self._generate_text(parameters)
            elif content_type == "report":
                return await self._generate_report(parameters)
            elif content_type == "blog":
                return await self._generate_blog(parameters)
            elif content_type == "technical":
                return await self._generate_technical_content(parameters)
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _generate_text(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate regular text content"""
        prompt = parameters.get("prompt", "")
        style = parameters.get("style", "professional")
        max_length = parameters.get("max_length", 1000)
        
        try:
            # Use LLM for text generation
            generated_text = await self._llm_generate(
                prompt=prompt,
                style=style,
                max_length=max_length
            )
            
            # Apply formatting and enhancements
            formatted_text = await self._format_content(
                generated_text,
                parameters.get("formatting", {})
            )
            
            return {
                "status": "success",
                "content": formatted_text,
                "metadata": {
                    "type": "text",
                    "style": style,
                    "length": len(formatted_text)
                }
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def _generate_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured report"""
        try:
            # Generate different sections in parallel
            sections = parameters.get("sections", ["introduction", "body", "conclusion"])
            tasks = [
                self._generate_section(section, parameters)
                for section in sections
            ]
            
            section_contents = await asyncio.gather(*tasks)
            
            # Combine sections
            report = await self._combine_sections(
                sections,
                section_contents,
                parameters.get("formatting", {})
            )
            
            return {
                "status": "success",
                "content": report,
                "metadata": {
                    "type": "report",
                    "sections": sections,
                    "length": len(report)
                }
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def _generate_technical_content(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical content with code examples"""
        try:
            # Generate technical explanation
            explanation = await self._llm_generate(
                prompt=parameters.get("prompt", ""),
                style="technical",
                max_length=parameters.get("max_length", 2000)
            )
            
            # Generate code examples if required
            if parameters.get("include_code", True):
                code_examples = await self._generate_code_examples(
                    parameters.get("programming_language", "python"),
                    parameters.get("complexity", "medium")
                )
            else:
                code_examples = []
            
            return {
                "status": "success",
                "content": {
                    "explanation": explanation,
                    "code_examples": code_examples
                },
                "metadata": {
                    "type": "technical",
                    "includes_code": bool(code_examples)
                }
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}