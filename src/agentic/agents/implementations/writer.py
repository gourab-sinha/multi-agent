from src.agentic.agents.base import BaseAgent
from typing import Dict, Any, Optional

class WriterAgent(BaseAgent):
    """Agent specialized in content generation"""
    
    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        step: int
    ) -> Dict[str, Any]:
        try:
            # Wait for analysis data
            analysis_data = await self.receive_message()
            if not analysis_data:
                return {
                    "status": "waiting",
                    "agent_id": self.agent_id
                }
            
            # Generate content
            content = await self.use_tool(
                "content_generator",
                {
                    "task": task,
                    "data": analysis_data["data"],
                    "style": context.get("style", "professional"),
                    "format": context.get("format", "report"),
                    "max_length": context.get("max_length", 2000)
                }
            )
            
            # Optimize content if needed
            if context.get("optimize_content", True):
                content = await self.use_plugin(
                    "content_optimizer",
                    {
                        "content": content,
                        "target_metrics": ["readability", "engagement"]
                    }
                )
            
            # Store content
            await self.memory.store(
                f"{self.agent_id}_content_{step}",
                content
            )
            
            # Notify validator
            await self.send_message(
                "validator",
                {
                    "type": "content_ready",
                    "data": content,
                    "step": step
                }
            )
            
            return {
                "status": "success",
                "agent_id": self.agent_id,
                "results": content
            }
            
        except Exception as e:
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e)
            }