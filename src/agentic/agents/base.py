from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from src.agentic.communication.base import MessageBus
from src.agentic.tools.registry import ToolRegistry
from src.agentic.plugins.registry import PluginRegistry
from src.agentic.memory.base import MemoryProvider

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(
        self,
        agent_id: str,
        config: Dict[str, Any],
        message_bus: MessageBus,
        tool_registry: ToolRegistry,
        plugin_registry: PluginRegistry,
        memory: MemoryProvider
    ):
        self.agent_id = agent_id
        self.config = config
        self.message_bus = message_bus
        self.tool_registry = tool_registry
        self.plugin_registry = plugin_registry
        self.memory = memory
        self.state = {}
    
    @abstractmethod
    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        step: int
    ) -> Dict[str, Any]:
        """Execute agent's task"""
        pass
    
    async def send_message(
        self,
        to_agent: str,
        message: Dict[str, Any],
        priority: int = 0
    ):
        """Send message to another agent"""
        await self.message_bus.send(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message=message,
            priority=priority
        )
    
    async def receive_message(
        self,
        timeout: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """Receive message from message bus"""
        return await self.message_bus.receive(
            self.agent_id,
            timeout=timeout
        )
    
    async def use_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use registered tool"""
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        return await tool.execute(parameters)
    
    async def use_plugin(
        self,
        plugin_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use registered plugin"""
        plugin = self.plugin_registry.get_plugin(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin not found: {plugin_name}")
        return await plugin.execute(parameters)