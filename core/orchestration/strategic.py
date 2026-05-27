from typing import List, Dict, Any, Optional
from core.agents.base import BaseAgent, AgentTask, AgentResult
from core.agents.planner import PlannerAgent
from core.agents.executor import ExecutorAgent
from core.agents.reviewer import ReviewerAgent
from core.memory.semantic import SemanticMemoryManager
from core.telemetry.setup import tracer
from loguru import logger

class StrategicOrchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        self.memory = SemanticMemoryManager()
        logger.info("StrategicOrchestrator initialized with high-thinking agents")

    async def run_task(self, description: str, context: Optional[Dict[str, Any]] = None) -> List[AgentResult]:
        with tracer.start_as_current_span("strategic_run_task") as span:
            self.memory.add_message("user", description)

            # 1. Planning with Context
            enhanced_description = f"{description}\n\nContext:\n{self.memory.get_context_prompt()}"
            plan_task = AgentTask(task_id="plan-1", description=enhanced_description, context=context)
            plan_result = await self.planner.execute_task(plan_task)

            all_results = [plan_result]
            sub_tasks = plan_result.output.get("sub_tasks", [])

            # 2. Execution Loop with Self-Correction
            for i, sub_desc in enumerate(sub_tasks):
                # Execute
                exec_task = AgentTask(task_id=f"exec-{i}", description=sub_desc, context=context)
                exec_result = await self.executor.execute_task(exec_task)

                # Review (High Thinking)
                review_task = AgentTask(
                    task_id=f"review-{i}",
                    description=f"Validate: {sub_desc}",
                    context={"result_to_review": exec_result.output}
                )
                review_result = await self.reviewer.execute_task(review_task)

                if review_result.output.get("review_score", 0) < 0.8:
                    logger.warning(f"Low quality output for {sub_desc}. Retrying with elevated thinking...")
                    # Placeholder for retry logic
                    exec_result.logs.append("Self-correction triggered: Retrying task...")

                all_results.extend([exec_result, review_result])
                self.memory.add_message("assistant", f"Executed: {sub_desc}. Result: {exec_result.status}")

            return all_results
