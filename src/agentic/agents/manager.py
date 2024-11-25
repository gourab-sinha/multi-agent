import uuid
from typing import Dict, Any, List
from src.agentic.agents.base import BaseAgent
from src.agentic.communication.base import MessageBus
from src.agentic.tools.registry import ToolRegistry
from src.agentic.plugins.registry import PluginRegistry
from src.agentic.memory.base import MemoryProvider

from src.agentic.agents.implementations.researcher import ResearchAgent
from src.agentic.agents.implementations.writer import WriterAgent
from src.agentic.agents.implementations.analyst import AnalystAgent
from src.agentic.agents.implementations.validator import ValidatorAgent


class AgentNetwork:
    """Represents a network of collaborating agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.completed_agents: set = set()
    
    def add_agent(self, agent: BaseAgent):
        """Add agent to network"""
        self.agents[agent.agent_id] = agent
    
    def set_dependencies(self, dependencies: Dict[str, List[str]]):
        """Set agent dependencies"""
        self.dependencies = dependencies
    
    def get_executable_agents(self) -> List[BaseAgent]:
        """Get agents that can be executed"""
        executable = []
        
        for agent_id, agent in self.agents.items():
            if agent_id not in self.completed_agents:
                dependencies = self.dependencies.get(agent_id, [])
                if all(dep in self.completed_agents for dep in dependencies):
                    executable.append(agent)
        
        return executable
    
    def update_state(self, results: List[Dict[str, Any]]):
        """Update network state based on execution results"""
        for result in results:
            if result.get("status") == "success":
                self.completed_agents.add(result["agent_id"])
    
    def is_complete(self) -> bool:
        """Check if all agents have completed"""
        return len(self.completed_agents) == len(self.agents)

class AgentManager:
    """Manages agent lifecycle and coordination"""
    
    def __init__(
        self,
        message_bus: MessageBus,
        tool_registry: ToolRegistry,
        plugin_registry: PluginRegistry,
        memory: MemoryProvider
    ):
        self.message_bus = message_bus
        self.tool_registry = tool_registry
        self.plugin_registry = plugin_registry
        self.memory = memory
        self.agent_types = self._load_agent_types()
    
    def _load_agent_types(self) -> Dict[str, type]:
        """Load available agent types"""
        return {
            "researcher": ResearchAgent,
            "analyst": AnalystAgent,
            "writer": WriterAgent,
            "validator": ValidatorAgent
        }
    
    async def setup_network(
        self,
        config: Dict[str, Any]
    ) -> AgentNetwork:
        """Setup agent network from configuration"""
        network = AgentNetwork()
        
        # Create agents
        for agent_config in config:
            agent = await self._create_agent(agent_type=agent_config["type"],config=agent_config)
            network.add_agent(agent)
        
        # Setup dependencies
        dependencies = self._create_dependencies(config)
        network.set_dependencies(dependencies)
        
        return network
    
    async def _create_agent(
        self,
        agent_type: str,
        config: Dict[str, Any]
    ) -> BaseAgent:
        """Create agent instance"""
        if agent_type not in self.agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        agent_class = self.agent_types[agent_type]
        agent_id = f"{agent_type}_{str(uuid.uuid4())[:8]}"
        
        return agent_class(
            agent_id=agent_id,
            config=config,
            message_bus=self.message_bus,
            tool_registry=self.tool_registry,
            plugin_registry=self.plugin_registry,
            memory=self.memory
        )
    
    def _create_dependencies(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Create agent dependencies based on configuration"""
        dependencies = {}
        
        for agent_id, agent_config in config:
            if "depends_on" in agent_config:
                dependencies[agent_id] = agent_config["depends_on"]
        
        return dependencies