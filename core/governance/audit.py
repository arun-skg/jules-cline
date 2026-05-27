import datetime
import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from loguru import logger

class AuditEntry(BaseModel):
    timestamp: str
    user_id: str
    tenant_id: str
    agent_id: str
    action: str
    details: Dict[str, Any]
    status: str

class AuditLogger:
    def __init__(self, storage_path: str = "logs/audit.jsonl"):
        self.storage_path = storage_path

    def log_action(self, user_id: str, tenant_id: str, agent_id: str, action: str, details: Dict[str, Any], status: str):
        entry = AuditEntry(
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            user_id=user_id,
            tenant_id=tenant_id,
            agent_id=agent_id,
            action=action,
            details=details,
            status=status
        )

        logger.info(f"AUDIT | {tenant_id} | {user_id} | {agent_id} | {action} | {status}")

        with open(self.storage_path, "a") as f:
            f.write(entry.model_dump_json() + "\n")

# Global Audit instance
audit = AuditLogger()
