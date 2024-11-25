import pytest
import asyncio
from typing import Dict, Any
from agentic import AgentFlow

@pytest.fixture
async def framework():
    """Fixture for framework instance"""
    config = {
        "llm": {
            "provider": "openai",
            "api_key": "test-key",
            "model": "gpt-4"
        },
        "memory": {
            "provider": "local",
            "max_size": 1000
        }
    }
    
    framework = AgentFlow(config)
    yield framework

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()