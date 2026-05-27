import asyncio
import pytest
from core.orchestration.strategic import StrategicOrchestrator
from core.telemetry.setup import setup_telemetry

@pytest.mark.asyncio
async def test_strategic_orchestrator_flow():
    setup_telemetry("test-strategic")
    orchestrator = StrategicOrchestrator()

    results = await orchestrator.run_task("Analyze and refactor the auth system")

    # Verify we have plan, execution and review results
    assert len(results) >= 3
    assert results[0].task_id == "plan-1"
    assert "review" in results[2].task_id
    assert results[2].output["review_score"] > 0.9
