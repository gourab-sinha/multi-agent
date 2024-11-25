import asyncio
from typing import Dict, Any, List
from src.agentic.agent_flow import AgentFlow
from examples.market_research import market_research_example
from examples.content_creation import content_creation_example
async def data_analysis_example():
    """Example of data analysis task"""
    framework = AgentFlow()
    
    task = """
    Analyze customer feedback data to identify key insights:
    - Sentiment analysis
    - Common issues
    - Improvement opportunities
    - Trend analysis
    """
    
    context = {
        "data_source": "customer_feedback.csv",
        "analysis_types": [
            "sentiment_analysis",
            "topic_modeling",
            "trend_analysis",
            "statistical_analysis"
        ],
        "visualizations": [
            "sentiment_trends",
            "issue_distribution",
            "keyword_cloud"
        ],
        "output_requirements": {
            "format": "dashboard",
            "include_raw_data": True,
            "confidence_scores": True
        }
    }
    
    result = await framework.execute(task, context)
    return result

# Custom Tool Example
class CustomDataAnalysisTool:
    """Custom tool for specialized data analysis"""
    
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        data = parameters.get("data", [])
        analysis_type = parameters.get("type", "basic")
        
        if analysis_type == "basic":
            return await self._basic_analysis(data)
        elif analysis_type == "advanced":
            return await self._advanced_analysis(data)
        
        raise ValueError(f"Unknown analysis type: {analysis_type}")
    
    async def _basic_analysis(self, data: List[Any]) -> Dict[str, Any]:
        # Implement basic analysis
        pass
    
    async def _advanced_analysis(self, data: List[Any]) -> Dict[str, Any]:
        # Implement advanced analysis
        pass

# Custom Plugin Example
class CustomSEOPlugin:
    """Custom plugin for SEO optimization"""
    
    async def initialize(self) -> bool:
        # Initialize plugin
        return True
    
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        content = parameters.get("content", "")
        keywords = parameters.get("keywords", [])
        
        # Implement SEO optimization
        optimized_content = await self._optimize_content(content, keywords)
        seo_score = await self._calculate_seo_score(optimized_content)
        
        return {
            "optimized_content": optimized_content,
            "seo_score": seo_score,
            "improvements": await self._get_improvements(content, optimized_content)
        }

# Integration Example
async def main():
    # Initialize framework
    framework = AgentFlow()
    
    # Register custom components
    await framework.register_tool(
        "custom_analysis",
        CustomDataAnalysisTool()
    )
    
    await framework.register_plugin(
        "custom_seo",
        CustomSEOPlugin()
    )
    
    # Execute tasks
    market_result = await market_research_example()
    content_result = await content_creation_example()
    analysis_result = await data_analysis_example()
    
    return {
        "market_research": market_result,
        "content_creation": content_result,
        "data_analysis": analysis_result
    }

if __name__ == "__main__":
    asyncio.run(main())