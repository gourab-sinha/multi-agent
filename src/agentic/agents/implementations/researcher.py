from src.agentic.agents.base import BaseAgent
from typing import Dict, Any, Optional

class ResearchAgent(BaseAgent):
    """Agent specialized in research tasks"""
    
    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        step: int
    ) -> Dict[str, Any]:
        try:
            # Use search tool for initial research
            search_results = await self.use_tool(
                "web_search",
                {
                    "query": task,
                    "filters": context.get("filters", {}),
                    "max_results": context.get("max_results", 10)
                }
            )
            
            # Process and analyze results
            processed_results = await self.use_tool(
                "data_analysis",
                {
                    "data": search_results,
                    "type": "research_analysis"
                }
            )
            
            # Store research results
            await self.memory.store(
                f"{self.agent_id}_research_{step}",
                processed_results
            )
            
            # Notify analyst
            await self.send_message(
                "analyst",
                {
                    "type": "research_complete",
                    "data": processed_results,
                    "step": step
                }
            )
            
            return {
                "status": "success",
                "agent_id": self.agent_id,
                "results": processed_results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e)
            }