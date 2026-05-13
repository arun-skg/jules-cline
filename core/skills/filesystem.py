import os
import pathlib
from typing import Any, Dict, List
from core.skills.base import BaseSkill, SkillMetadata
from core.tools.base import ToolResult

class FileSystemSkill(BaseSkill):
    def __init__(self, base_path: str = "."):
        super().__init__(SkillMetadata(
            name="filesystem_management",
            description="Manages files and directories",
            version="0.1.0",
            author="Enterprise Agent Core",
            permissions=["fs:read", "fs:write"]
        ))
        self.base_path = pathlib.Path(base_path).resolve()

    async def execute(self, action: str, path: str, content: str = None) -> ToolResult:
        target_path = (self.base_path / path).resolve()

        # Security check: Ensure target_path is within base_path
        if not str(target_path).startswith(str(self.base_path)):
            return ToolResult(output="", error="Access denied: outside of base path", exit_code=1)

        try:
            if action == "read":
                with open(target_path, "r") as f:
                    return ToolResult(output=f.read())
            elif action == "write":
                os.makedirs(target_path.parent, exist_ok=True)
                with open(target_path, "w") as f:
                    f.write(content)
                return ToolResult(output=f"Successfully wrote to {path}")
            elif action == "list":
                items = os.listdir(target_path)
                return ToolResult(output="\n".join(items))
            else:
                return ToolResult(output="", error=f"Unknown action: {action}", exit_code=1)
        except Exception as e:
            return ToolResult(output="", error=str(e), exit_code=1)

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [{
            "name": "manage_filesystem",
            "description": "Read, write, or list files and directories",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["read", "write", "list"]},
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["action", "path"]
            }
        }]
