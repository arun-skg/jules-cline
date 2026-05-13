from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class AgentMessage(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class AgentTask(BaseModel):
    task_id: str
    description: str
    context: Optional[Dict[str, Any]] = None

class AgentResult(BaseModel):
    task_id: str
    status: str
    output: Any
    logs: List[str] = []

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name

    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute a given task and return the result."""
        pass

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> AgentMessage:
        """Process an incoming message and return a response."""
        pass
