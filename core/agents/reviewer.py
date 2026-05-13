from core.agents.base import BaseAgent, AgentTask, AgentResult, AgentMessage
from loguru import logger

class ReviewerAgent(BaseAgent):
    def __init__(self, agent_id: str = "reviewer-001"):
        super().__init__(agent_id, "Reviewer Agent")

    async def execute_task(self, task: AgentTask) -> AgentResult:
        logger.info(f"Reviewer analyzing results for: {task.description}")

        # Simulated review logic
        logs = ["Analyzed output for security violations", "Checked for code regressions"]
        output = task.context.get("result_to_review", "") if task.context else ""

        # Simulate a pass
        return AgentResult(
            task_id=task.task_id,
            status="completed",
            output={"review_score": 0.95, "comments": "Output looks safe and correct"},
            logs=logs
        )

    async def process_message(self, message: AgentMessage) -> AgentMessage:
        return AgentMessage(role="assistant", content=f"Reviewer received: {message.content}")
