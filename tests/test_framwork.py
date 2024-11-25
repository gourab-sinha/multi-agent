import pytest
from agentic import AgentFlow

class TestFramework:
    @pytest.mark.asyncio
    async def test_basic_execution(self, framework):
        """Test basic task execution"""
        result = await framework.execute(
            task="Summarize the main features of Python programming language",
            context={"max_length": 500}
        )
        
        assert result["status"] == "success"
        assert "result" in result
    
    @pytest.mark.asyncio
    async def test_multi_agent_execution(self, framework):
        """Test execution with multiple agents"""
        result = await framework.execute(
            task="Create a market analysis report for electric vehicles",
            context={
                "focus_areas": ["technology", "market_size", "trends"],
                "output_format": "report"
            }
        )
        
        assert result["status"] == "success"
        assert "result" in result
        assert isinstance(result["result"], dict)
    
    @pytest.mark.asyncio
    async def test_tool_registration(self, framework):
        """Test custom tool registration"""
        class CustomTool:
            async def execute(self, parameters):
                return {"result": "custom tool output"}
        
        success = await framework.register_tool("custom_tool", CustomTool())
        assert success
        
        result = await framework.execute(
            task="Test custom tool",
            context={"tools": ["custom_tool"]}
        )
        assert result["status"] == "success"