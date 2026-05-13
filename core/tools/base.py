from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolResult(BaseModel):
    output: str
    error: Optional[str] = None
    exit_code: int = 0

class BaseTool(ABC):
    def __init__(self, definition: ToolDefinition):
        self.definition = definition

    @abstractmethod
    async def run(self, **kwargs) -> ToolResult:
        """Run the tool and return the result."""
        pass
