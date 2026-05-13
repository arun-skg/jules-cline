# Contributing to Enterprise AI Agent Platform

Thank you for your interest in contributing! This project aims to build a robust, secure, and extensible AI agent platform for enterprise use.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Reporting Bugs](#reporting-bugs)

## 🤝 How Can I Contribute?
- **Skills:** Implement new skills in `core/skills/`.
- **Agents:** Improve reasoning or multi-agent orchestration in `core/agents/`.
- **Infrastructure:** Enhance the sandboxing or observability layers.
- **Documentation:** Improve README, SPECIFICATION, or RESEARCH_REPORT.

## 🛠️ Development Workflow
1. **Setup:** Use `uv sync` to install dependencies.
2. **Branching:** Create a descriptive branch: `feat/new-skill` or `fix/reasoning-loop`.
3. **Testing:** Ensure all tests pass with `uv run pytest`.
4. **Linting:** Use `black` and `isort` for formatting.
5. **PR:** Submit a detailed Pull Request.

## 📏 Style Guidelines
- Use Type Hints for all function signatures.
- Follow Pydantic best practices for data models.
- Use `loguru` for logging and `opentelemetry` for tracing.
- Keep agents stateless where possible.

## 🐛 Reporting Bugs
Use GitHub Issues to report bugs. Include:
- A clear description of the issue.
- Steps to reproduce.
- Expected vs Actual behavior.
- Logs and environment details.
