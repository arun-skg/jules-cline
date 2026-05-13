# Enterprise AI Agent Platform

## Overview
This is a production-grade, autonomous AI agent platform designed for enterprise engineering and workflow automation. It is inspired by `everything-claude-code`, `Roo-Code`, and `cline`.

## Architecture
- **Python 3.12+ Async Core:** High-performance, type-safe implementation.
- **Multi-Agent Orchestration:** Specialized agents (Planner, Executor, Reviewer) for complex task execution.
- **Secure Sandboxing:** Tool execution occurs in isolated Docker/Firecracker environments.
- **Enterprise Governance:** RBAC/ABAC and immutable audit logs.
- **Modular Skills:** Extensible plugin system for rapid capability growth.

## Getting Started

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Docker & Docker Compose

### Installation
```bash
uv sync
```

### Running the API
```bash
docker-compose up
```

## Documentation
- [SPECIFICATION.md](SPECIFICATION.md)
- [RESEARCH_REPORT.md](RESEARCH_REPORT.md)
- [Architecture Details](docs/research/intelligence_report.md)
