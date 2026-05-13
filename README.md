# Enterprise Python AI Agent Platform

[![CI](https://github.com/your-org/enterprise-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/enterprise-agent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-3120/)

## 🚀 Overview
An enterprise-grade, autonomous AI agent platform designed for complex engineering workflows and automation. Built with **Python 3.12+**, this platform provides a secure, scalable, and extensible environment for AI-driven development.

Inspired by `Roo-Code`, `Cline`, and `everything-claude-code`.

## 🏗️ Architecture
- **Multi-Agent Orchestration:** Specialized agents (Planner, Executor, Reviewer) collaborate via a central Orchestrator.
- **Async-First Runtime:** High-concurrency agent loops built on FastAPI and Python's `asyncio`.
- **Secure Sandbox:** Tool execution isolated in ephemeral environments with strict governance.
- **Memory/RAG Service:** Hybrid memory combining short-term context, episodic task history, and long-term vector storage (Qdrant).
- **Observability:** Native OpenTelemetry integration for full-stack tracing and metrics.

---

## 🛠️ Setup & Installation

### Prerequisites
- **Python 3.12+**
- **[uv](https://github.com/astral-sh/uv):** Extremely fast Python package manager.
- **Docker & Docker Compose:** For running isolated services.

### Local Development Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/enterprise-agent.git
   cd enterprise-agent
   ```

2. **Install dependencies:**
   ```bash
   uv sync --all-groups
   ```

3. **Configure Environment:**
   Create a `.env` file in the root:
   ```env
   SECRET_KEY=your-secure-secret-key
   REDIS_URL=redis://localhost:6379/0
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   ```

---

## 🏃 Running the Platform

### Using Docker Compose (Recommended)
Start the entire stack (API, Redis, Qdrant):
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.

### Manual Start (for development)
1. **Start dependencies:**
   ```bash
   docker run -p 6379:6379 -d redis:7-alpine
   docker run -p 6333:6333 -d qdrant/qdrant:latest
   ```

2. **Start the API:**
   ```bash
   PYTHONPATH=. uv run python apps/api/main.py
   ```

---

## 🤖 Using the Agent

### Authentication
Obtain a JWT token:
```bash
curl -X POST http://localhost:8000/token \
     -F "username=admin" \
     -F "password=password"
```

### Executing a Task
Send a task description to the agent:
```bash
curl -X POST http://localhost:8000/agent/execute \
     -H "Authorization: Bearer <your_token>" \
     -d "task_description=List files in the current directory and explain their purpose"
```

---

## 🧩 Extending Capabilities (Skills)

The platform is designed to be extensible. You can add new "Skills" to give the agent more capabilities.

### Creating a New Skill
1. Create a new file in `core/skills/`:
   ```python
   # core/skills/my_new_skill.py
   from core.skills.base import BaseSkill, SkillMetadata

   class MyNewSkill(BaseSkill):
       def __init__(self):
           super().__init__(SkillMetadata(
               name="custom_skill",
               description="Does something awesome",
               version="0.1.0",
               author="You",
               permissions=["custom:permission"]
           ))

       async def execute(self, param1: str):
           # Your logic here
           return f"Executed with {param1}"
   ```

2. Register it in `core/agents/executor.py` or through a dynamic plugin loader.

---

## 🧪 Testing

Run the full test suite:
```bash
PYTHONPATH=. uv run pytest
```

Run specific test layers:
```bash
uv run pytest tests/unit          # Unit tests
uv run pytest tests/test_agent_flow.py  # Integration tests
```

---

## 🛡️ Governance & Security
- **RBAC:** Defined in `core/governance/engine.py`. Roles (admin, developer, viewer) control tool access.
- **Audit Logs:** Every agent action is cryptographically recorded in `logs/audit.jsonl`.
- **Command Sanitization:** Shell commands are validated against a denied list (e.g., `rm -rf /`).

---

## 📖 Documentation
- [**SPECIFICATION.md**](SPECIFICATION.md): Master system prompt and technical spec.
- [**RESEARCH_REPORT.md**](RESEARCH_REPORT.md): Competitive analysis and reverse engineering findings.
- [**CONTRIBUTING.md**](CONTRIBUTING.md): Guidelines for developing the platform.
