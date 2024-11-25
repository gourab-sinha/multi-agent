from typing import Dict, Any, Optional
from src.agentic.tools.base import BaseTool
from src.agentic.tools.implementations.web_search import WebSearchTool
from src.agentic.tools.implementations.data_analysis import DataAnalysisTool
from src.agentic.tools.implementations.content_generator import ContentGeneratorTool
from src.agentic.tools.implementations.content_generator import ContentGeneratorTool

class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.tools: Dict[str, BaseTool] = {}
        self._load_default_tools()
    
    def _load_default_tools(self):
        """Load default tools based on configuration"""
        default_tools = {
            "web_search": WebSearchTool,
            "data_analysis": DataAnalysisTool,
            "content_generator": ContentGeneratorTool,
            # "visualization": VisualizationTool
        }
        
        for tool_name, tool_class in default_tools.items():
            if self.config.get(tool_name, {}).get("enabled", True):
                self.tools[tool_name] = tool_class(
                    self.config.get(tool_name, {})
                )
    
    async def register_tool(
        self,
        name: str,
        tool: BaseTool
    ) -> bool:
        """Register a new tool"""
        if name in self.tools:
            raise ValueError(f"Tool already exists: {name}")
            
        self.tools[name] = tool
        return True
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        return self.tools.get(name)