from typing import Dict,Any, Optional

from src.agentic.agents.manager import AgentManager, AgentNetwork
from src.agentic.communication.base import MessageBus
from src.agentic.memory.base import MemoryProvider

class TaskExecutor:
    """Executes tasks using agent network"""
    
    def __init__(
        self,
        agent_manager: AgentManager,
        message_bus: MessageBus,
        memory: MemoryProvider
    ):
        self.agent_manager = agent_manager
        self.message_bus = message_bus
        self.memory = memory
    
    async def execute(
        self,
        task_id: str,
        task: str,
        context: Optional[Dict[str, Any]],
        network: AgentNetwork
    ) -> Dict[str, Any]:
        """Execute task using agent network"""
        
        try:
            # Initialize execution
            await self._initialize_execution(task_id, network)
            
            # Execute task steps
            result = await self._execute_steps(task_id, task, context, network)
            
            # Finalize execution
            final_result = await self._finalize_execution(task_id, result)
            
            return final_result
            
        except Exception as e:
            await self._handle_execution_error(task_id, e)
            raise
    
    async def _initialize_execution(
        self,
        task_id: str,
        network: AgentNetwork
    ):
        """Initialize task execution"""
        await self.message_bus.broadcast(
            "system",
            {
                "type": "execution_start",
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    async def _execute_steps(
        self,
        task_id: str,
        task: str,
        context: Optional[Dict[str, Any]],
        network: AgentNetwork
    ) -> Dict[str, Any]:
        """Execute task steps"""
        current_step = 0
        results = {}
        
        while not network.is_complete():
            # Get next executable agents
            executable = network.get_executable_agents()
            
            # Execute agents in parallel
            step_results = await asyncio.gather(*[
                agent.execute(task, context, current_step)
                for agent in executable
            ])
            
            # Store step results
            results[f"step_{current_step}"] = step_results
            
            # Update network state
            network.update_state(step_results)
            current_step += 1
        
        return results
    
    async def _finalize_execution(
        self,
        task_id: str,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Finalize task execution"""
        # Consolidate results
        final_result = self._consolidate_results(results)
        
        # Notify completion
        await self.message_bus.broadcast(
            "system",
            {
                "type": "execution_complete",
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return final_result
    
    async def _handle_execution_error(
        self,
        task_id: str,
        error: Exception
    ):
        """Handle execution error"""
        await self.message_bus.broadcast(
            "system",
            {
                "type": "execution_error",
                "task_id": task_id,
                "error": str(error),
                "timestamp": datetime.utcnow().isoformat()
            }
        )