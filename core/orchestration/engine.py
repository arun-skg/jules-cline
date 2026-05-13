import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from core.agents.base import BaseAgent, AgentTask, AgentResult
from core.agents.planner import PlannerAgent
from core.agents.executor import ExecutorAgent
from core.agents.reviewer import ReviewerAgent
from core.telemetry.setup import tracer
from loguru import logger

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        logger.debug("Orchestrator agents (Planner, Executor, Reviewer) initialized")

    async def run_complex_task(self, description: str, context: Optional[Dict[str, Any]] = None) -> List[AgentResult]:
        with tracer.start_as_current_span("run_complex_task") as span:
            logger.info(f"Starting complex task orchestration: {description}")

            # 1. Plan
            plan_task = AgentTask(task_id="plan-initial", description=description, context=context)
            plan_result = await self.planner.execute_task(plan_task)

            all_results = [plan_result]
            if plan_result.status != "completed":
                logger.error("Planning failed")
                return all_results

            sub_tasks = plan_result.output.get("sub_tasks", [])
            logger.info(f"Generated {len(sub_tasks)} sub-tasks")

            # 2. Execute and Review
            for i, sub_desc in enumerate(sub_tasks):
                # Execution
                exec_task = AgentTask(task_id=f"exec-{i}", description=sub_desc, context=context)
                exec_result = await self.executor.execute_task(exec_task)
                all_results.append(exec_result)

                if exec_result.status != "completed":
                    logger.warning(f"Sub-task {i} failed. Attempting autonomous repair...")
                    # Phase 4 repair placeholder
                    continue

                # Review
                review_task = AgentTask(
                    task_id=f"review-{i}",
                    description=f"Review result of: {sub_desc}",
                    context={"result_to_review": exec_result.output}
                )
                review_result = await self.reviewer.execute_task(review_task)
                all_results.append(review_result)

            return all_results
