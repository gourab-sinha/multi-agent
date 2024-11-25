from typing import Dict, Any, Optional
import uuid
from datetime import datetime
from src.agentic.agents.manager import AgentManager
from src.agentic.tools.registry import ToolRegistry
from src.agentic.plugins.registry import PluginRegistry
from src.agentic.memory.base import MemoryProvider
from src.agentic.communication.base import MessageBus
from src.agentic.core.analyzer import TaskAnalyzer
from src.agentic.core.executor import TaskExecutor
from src.agentic.config.settings import Settings

class Orchestrator:
    """Orchestrates task execution and agent management"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.message_bus = MessageBus()
        self.tool_registry = ToolRegistry(settings.tools_config)
        self.plugin_registry = PluginRegistry(settings.plugins_config)
        self.memory = MemoryProvider.create(settings.memory_config)
        
        self.agent_manager = AgentManager(
            self.message_bus,
            self.tool_registry,
            self.plugin_registry,
            self.memory
        )
        
        self.task_analyzer = TaskAnalyzer(settings.llm_config)
        self.executor = TaskExecutor(
            self.agent_manager,
            self.message_bus,
            self.memory
        )

    async def initialize(self):
        """Initialize orchestrator components"""
        await self.plugin_registry.initialize_plugins()
    
    async def process_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        explicit_agents: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process a task with automatic or explicit agent configuration"""
        task_id = str(uuid.uuid4())
        
        try:
            # Store task details
            await self.memory.store(f"task_{task_id}", {
                "task": task,
                "context": context,
                "start_time": datetime.utcnow().isoformat()
            })
            
            # Analyze task if no explicit agents provided
            if not explicit_agents:
                analysis = await self.task_analyzer.analyze_task(task, context)
                agent_config = analysis["required_agents"]
            else:
                agent_config = explicit_agents
            
            # Setup agent network
            network = await self.agent_manager.setup_network(agent_config)
            
            # Execute task
            result = await self.executor.execute(
                task_id=task_id,
                task=task,
                context=context,
                network=network
            )
            
            # Store result
            await self.memory.store(f"result_{task_id}", {
                "result": result,
                "completion_time": datetime.utcnow().isoformat()
            })
            
            return {
                "task_id": task_id,
                "status": "success",
                "result": result
            }
            
        except Exception as e:
            await self.memory.store(f"error_{task_id}", {
                "error": str(e),
                "time": datetime.utcnow().isoformat()
            })
            raise