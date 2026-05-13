# Security Handbook

## Architecture
- **Sandboxed Execution:** All shell and filesystem operations occur in restricted environments.
- **Governance Engine:** Every tool call is intercepted and validated against RBAC policies.
- **DLP Proxy:** LLM interactions pass through a layer that scans for PII and secrets.

## Access Control (RBAC)
Roles are defined in `core/governance/engine.py`:
- `admin`: Full access to all tools and system settings.
- `developer`: Access to coding tools (fs, git, shell).
- `viewer`: Read-only access to files and git history.

## Audit Logging
All agent actions are logged to `logs/audit.jsonl` in a structured JSON format. This log is intended to be streamed to an immutable storage backend (e.g., CloudWatch, ELK) in production.

## Secure Configuration
- **Secrets:** Never hardcode secrets. Use environment variables or a Secret Vault (Vault/AWS Secrets Manager).
- **JWT:** Tokens are signed using `HS256`. The `SECRET_KEY` must be rotated regularly.
