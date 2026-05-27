import asyncio
from typing import Any, Dict, List
from core.skills.base import BaseSkill, SkillMetadata
from core.tools.base import ToolResult

class ShellSkill(BaseSkill):
    def __init__(self):
        super().__init__(SkillMetadata(
            name="shell_execution",
            description="Executes shell commands in a controlled environment",
            version="0.1.0",
            author="Enterprise Agent Core",
            permissions=["shell:execute"]
        ))

    async def execute(self, command: str, args: List[str] = []) -> ToolResult:
        # Use exec for security instead of shell
        process = await asyncio.create_subprocess_exec(
            command,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        return ToolResult(
            output=stdout.decode().strip(),
            error=stderr.decode().strip() if stderr else None,
            exit_code=process.returncode
        )

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [{
            "name": "execute_shell",
            "description": "Execute a shell command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            }
        }]
