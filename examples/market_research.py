from src.agentic import AgentFlow

async def market_research_example():
    """Example of market research task"""
    framework = AgentFlow()
    
    task = """
    Create a comprehensive market research report for the AI chip industry:
    - Market size and growth trends
    - Key players and their market share
    - Technology comparison
    - Future outlook
    """
    
    context = {
        "required_sections": [
            "executive_summary",
            "market_analysis",
            "competitive_landscape",
            "technology_assessment",
            "future_predictions"
        ],
        "data_sources": [
            "industry_reports",
            "company_financials",
            "news_articles",
            "research_papers"
        ],
        "output_formats": [
            "detailed_report",
            "executive_summary",
            "presentation"
        ]
    }
    
    result = await framework.execute(task, context)
    return result