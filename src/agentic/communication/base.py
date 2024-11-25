from typing import Dict, Any, Optional, List
import asyncio
from collections import defaultdict
from datetime import datetime
import uuid

class Message:
    """Represents a message in the system"""
    
    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        content: Dict[str, Any],
        priority: int = 0
    ):
        self.id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.priority = priority
        self.timestamp = datetime.utcnow().isoformat()

class MessageBus:
    """Handles inter-agent communication"""
    
    def __init__(self):
        self.queues: Dict[str, asyncio.PriorityQueue] = defaultdict(asyncio.PriorityQueue)
        self.subscriptions: Dict[str, List[str]] = defaultdict(list)
        self.history: List[Message] = []
    
    async def send(
        self,
        from_agent: str,
        to_agent: str,
        message: Dict[str, Any],
        priority: int = 0
    ):
        """Send message to specific agent"""
        msg = Message(from_agent, to_agent, message, priority)
        await self.queues[to_agent].put((-priority, msg))
        self.history.append(msg)
    
    async def receive(
        self,
        agent_id: str,
        timeout: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """Receive message for specific agent"""
        try:
            if timeout:
                priority, msg = await asyncio.wait_for(
                    self.queues[agent_id].get(),
                    timeout=timeout
                )
            else:
                priority, msg = await self.queues[agent_id].get()
            
            return {
                "id": msg.id,
                "from": msg.from_agent,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
        except asyncio.TimeoutError:
            return None
    
    async def broadcast(
        self,
        from_agent: str,
        message: Dict[str, Any],
        priority: int = 0
    ):
        """Broadcast message to all subscribers"""
        tasks = [
            self.send(from_agent, subscriber, message, priority)
            for subscriber in self.subscriptions[from_agent]
        ]
        await asyncio.gather(*tasks)
    
    def subscribe(
        self,
        subscriber: str,
        publisher: str
    ):
        """Subscribe to messages from publisher"""
        if subscriber not in self.subscriptions[publisher]:
            self.subscriptions[publisher].append(subscriber)
    
    def unsubscribe(
        self,
        subscriber: str,
        publisher: str
    ):
        """Unsubscribe from publisher"""
        if subscriber in self.subscriptions[publisher]:
            self.subscriptions[publisher].remove(subscriber)
    
    def get_history(
        self,
        agent_id: Optional[str] = None,
        start_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get message history"""
        filtered_history = self.history
        
        if agent_id:
            filtered_history = [
                msg for msg in filtered_history
                if msg.from_agent == agent_id or msg.to_agent == agent_id
            ]
        
        if start_time:
            filtered_history = [
                msg for msg in filtered_history
                if msg.timestamp >= start_time
            ]
        
        return [
            {
                "id": msg.id,
                "from": msg.from_agent,
                "to": msg.to_agent,
                "content": msg.content,
                "priority": msg.priority,
                "timestamp": msg.timestamp
            }
            for msg in filtered_history
        ]