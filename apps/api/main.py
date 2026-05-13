from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from apps.api.auth import create_access_token, Token
from core.orchestration.engine import Orchestrator
from core.telemetry.setup import setup_telemetry

# Initialize Telemetry
setup_telemetry("enterprise-agent-api")

app = FastAPI(
    title="Enterprise AI Agent API",
    description="Backend API for the Enterprise AI Agent Platform",
    version="0.1.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
orchestrator = Orchestrator()

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Foundation phase: Simple hardcoded admin
    if form_data.username == "admin" and form_data.password == "password":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/agent/execute")
async def execute_agent_task(task_description: str, token: str = Depends(oauth2_scheme)):
    logger.info(f"API Execution request: {task_description}")
    try:
        results = await orchestrator.run_complex_task(task_description)
        return {"results": results}
    except Exception as e:
        logger.exception("Error during agent execution")
        raise HTTPException(status_code=500, detail=str(e))

# Instrumentation
FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
