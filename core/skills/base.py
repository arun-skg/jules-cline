from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class SkillMetadata(BaseModel):
    name: str
    description: str
    version: str
    author: str
    permissions: List[str] = []

class BaseSkill(ABC):
    def __init__(self, metadata: SkillMetadata):
        self.metadata = metadata

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the skill's primary logic."""
        pass

    @abstractmethod
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return the tool definitions for this skill (e.g., for LLM function calling)."""
        pass
