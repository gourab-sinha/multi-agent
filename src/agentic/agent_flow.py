from typing import Dict, Any, Optional
from src.agentic.core.orchestrator import Orchestrator
from src.agentic.config.settings import Settings
from src.agentic.utils.logger import setup_logger

class AgentFlow:
    """Main entry point for the framework"""
    
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        config_path: Optional[str] = None
    ):
        self.logger = setup_logger(__name__)
        self.settings = Settings(config_path)
        if config:
            self.settings.config.update(config)
        
        self.orchestrator = Orchestrator(self.settings)
        self.initialized = False
        self.logger.info(f"Framework initialized with LLM provider: {self.settings.llm_config['provider']}")
    
    async def initialize(self):
        """Initialize the framework"""
        if not self.initialized:
            await self.orchestrator.initialize()
            self.initialized = True

            
    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        agents: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a task with automatic or explicit agent configuration"""
        try:
            return await self.orchestrator.process_task(task, context, agents)
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def register_tool(self, name: str, tool: Any) -> bool:
        """Register a custom tool"""
        return await self.orchestrator.tool_registry.register_tool(name, tool)
    
    async def register_plugin(self, name: str, plugin: Any) -> bool:
        """Register a custom plugin"""
        return await self.orchestrator.plugin_registry.register_plugin(name, plugin)
