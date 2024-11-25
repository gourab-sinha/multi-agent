from src.agentic.agents.base import BaseAgent
from typing import Optional, Dict, Any


class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis"""
    
    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        step: int
    ) -> Dict[str, Any]:
        try:
            # Wait for research data
            research_data = await self.receive_message()
            if not research_data:
                return {
                    "status": "waiting",
                    "agent_id": self.agent_id
                }
            
            # Analyze data
            analysis = await self.use_tool(
                "data_analysis",
                {
                    "data": research_data["data"],
                    "type": "deep_analysis",
                    "metrics": context.get("metrics", ["trends", "patterns"])
                }
            )
            
            # Generate visualizations
            visualizations = await self.use_tool(
                "visualization",
                {
                    "data": analysis,
                    "types": context.get("visualization_types", ["charts"])
                }
            )
            
            results = {
                "analysis": analysis,
                "visualizations": visualizations
            }
            
            # Store results
            await self.memory.store(
                f"{self.agent_id}_analysis_{step}",
                results
            )
            
            # Notify writer
            await self.send_message(
                "writer",
                {
                    "type": "analysis_complete",
                    "data": results,
                    "step": step
                }
            )
            
            return {
                "status": "success",
                "agent_id": self.agent_id,
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e)
            }