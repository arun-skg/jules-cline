import asyncio
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from core.tools.base import ToolResult, ToolDefinition
from core.governance.engine import GovernanceEngine
from loguru import logger

class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    user_context: Optional[Dict[str, Any]] = None

class ToolService:
    def __init__(self):
        self.governance = GovernanceEngine()
        self.tools: Dict[str, Any] = {}

    def register_tool(self, tool_name: str, tool_instance: Any):
        self.tools[tool_name] = tool_instance
        logger.debug(f"Tool registered: {tool_name}")

    async def execute_tool(self, request: ToolExecutionRequest) -> ToolResult:
        logger.info(f"Executing tool: {request.tool_name}")

        if request.tool_name not in self.tools:
            return ToolResult(output="", error=f"Tool {request.tool_name} not found", exit_code=1)

        # 1. Governance Check
        is_allowed = self.governance.validate_path_access(request.arguments.get("path", "."))
        if request.tool_name == "execute_shell":
             is_allowed = is_allowed and self.governance.validate_shell_command(request.arguments.get("command", ""))

        if not is_allowed:
            return ToolResult(output="", error="Action blocked by governance policy", exit_code=1)

        # 2. Execution (Simulating sandbox for now, Phase 6 will use Docker)
        try:
            tool = self.tools[request.tool_name]
            # If it's a skill, call execute
            if hasattr(tool, 'execute'):
                return await tool.execute(**request.arguments)
            return await tool.run(**request.arguments)
        except Exception as e:
            logger.exception(f"Error executing tool {request.tool_name}")
            return ToolResult(output="", error=str(e), exit_code=1)
