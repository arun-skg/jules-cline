from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from core.orchestration.strategic import StrategicOrchestrator
from core.memory.semantic import SemanticMemoryManager

app = FastAPI(title="OpenClaw Intelligence Bridge")
orchestrator = StrategicOrchestrator()

class IntelligenceRequest(BaseModel):
    prompt: str
    context: Optional[Dict[str, Any]] = None

class MemoryIngestRequest(BaseModel):
    role: str
    content: str

@app.post("/reason")
async def strategic_reasoning(request: IntelligenceRequest):
    """Provides high-thinking strategic reasoning for OpenClaw."""
    try:
        results = await orchestrator.run_task(request.prompt, request.context)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/ingest")
async def ingest_memory(request: MemoryIngestRequest):
    """Ingests conversation into semantic memory for long-term context."""
    orchestrator.memory.add_message(request.role, request.content)
    return {"status": "ingested"}

@app.get("/memory/context")
async def get_memory_context():
    """Returns the summarized semantic context."""
    return {"context": orchestrator.memory.get_context_prompt()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
