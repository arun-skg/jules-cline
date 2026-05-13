import asyncio
import pytest
from core.orchestration.engine import Orchestrator
from core.telemetry.setup import setup_telemetry
from loguru import logger

@pytest.mark.asyncio
async def test_multi_agent_flow():
    setup_telemetry("test-flow")
    orchestrator = Orchestrator()

    logger.info("Starting test multi-agent flow")
    results = await orchestrator.run_complex_task("Build a new Python microservice")

    for result in results:
        logger.info(f"Result: {result.task_id} - {result.status}")
        logger.info(f"Output: {result.output}")

if __name__ == "__main__":
    asyncio.run(test_multi_agent_flow())
