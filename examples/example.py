# example.py
import asyncio
import os
from dotenv import load_dotenv
from src.agentic.agent_flow import AgentFlow

# Load environment variables
load_dotenv()

async def main():
    # Configuration
    config = {
        "llm": {
            "provider": "openai",
            "api_key": os.getenv("OPENAI_API_KEY"),  # Get API key from environment
            "model": "gpt-4",
            "temperature": 0.7
        },
        "memory": {
            "provider": "local",  # Use local memory for this example
            "ttl": 3600
        }
    }
    
    # Initialize framework
    framework = AgentFlow(config)
    
    # Example task
    task = "Create a comprehensive analysis of electric vehicles market trends"
    context = {
        "focus_areas": [
            "market_size",
            "key_players",
            "technology_trends",
            "future_outlook"
        ],
        "output_format": "report",
        "depth": "comprehensive"
    }
    try:
        # Execute task
        result = await framework.execute(task, context)
        
        # Print results
        print("\nTask Result:")
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print("\nAnalysis:")
            print(result['result'])
        else:
            print(f"Error: {result.get('error')}")
            
    except Exception as e:
        print(f"Execution failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

# .env
# OPENAI_API_KEY=your-openai-api-key