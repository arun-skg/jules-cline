from core.agents.base import BaseAgent, AgentTask, AgentResult, AgentMessage
from core.skills.shell import ShellSkill
from core.skills.filesystem import FileSystemSkill
from core.tools.service import ToolService, ToolExecutionRequest
from loguru import logger

class ExecutorAgent(BaseAgent):
    def __init__(self, agent_id: str = "executor-001"):
        super().__init__(agent_id, "Executor Agent")
        self.tool_service = ToolService()

        # Register core skills
        self.tool_service.register_tool("execute_shell", ShellSkill())
        self.tool_service.register_tool("manage_filesystem", FileSystemSkill())
        logger.info("ExecutorAgent initialized with core tools")

    async def execute_task(self, task: AgentTask) -> AgentResult:
        logger.info(f"Executor performing task: {task.description}")

        # In a real LLM scenario, the LLM would choose which tool to call.
        # Here we demonstrate the routing via simple keyword matching.

        logs = []
        output = None

        if "list files" in task.description.lower() or "read file" in task.description.lower():
            action = "list" if "list" in task.description.lower() else "read"
            path = task.context.get("path", ".") if task.context else "."

            res = await self.tool_service.execute_tool(ToolExecutionRequest(
                tool_name="manage_filesystem",
                arguments={"action": action, "path": path}
            ))
            output = res.output if not res.error else res.error
            logs.append(f"FileSystem tool executed: {action}")

        elif "run" in task.description.lower() and "command" in task.description.lower():
            command = task.context.get("command", "ls") if task.context else "ls"
            res = await self.tool_service.execute_tool(ToolExecutionRequest(
                tool_name="execute_shell",
                arguments={"command": command}
            ))
            output = res.output if not res.error else res.error
            logs.append(f"Shell tool executed: {command}")
        else:
            output = f"Successfully executed: {task.description}"
            logs.append(f"Mock execution for: {task.description}")

        status = "completed" if output and "error" not in str(output).lower() else "failed"

        return AgentResult(
            task_id=task.task_id,
            status=status,
            output=output,
            logs=logs
        )

    async def process_message(self, message: AgentMessage) -> AgentMessage:
        return AgentMessage(role="assistant", content=f"Executor received: {message.content}")
