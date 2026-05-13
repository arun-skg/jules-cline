from typing import List, Set, Dict
from loguru import logger

class GovernanceEngine:
    def __init__(self):
        self.denied_commands: Set[str] = {"rm -rf /", "mkfs", "dd", "chmod -R 777"}
        self.allowed_paths: List[str] = ["/tmp", "./"]
        self.rbac_policies: Dict[str, List[str]] = {
            "admin": ["*"],
            "developer": ["fs:read", "fs:write", "shell:execute", "git:read"],
            "viewer": ["fs:read", "git:read"]
        }

    def validate_shell_command(self, command: str) -> bool:
        for denied in self.denied_commands:
            if denied in command:
                logger.warning(f"Governance block: Command '{command}' contains denied pattern '{denied}'")
                return False
        return True

    def validate_path_access(self, path: str) -> bool:
        # Check against allowed path prefixes
        # Simplified for demonstration
        return True

    def check_permissions(self, user_role: str, required_permission: str) -> bool:
        permissions = self.rbac_policies.get(user_role, [])
        if "*" in permissions or required_permission in permissions:
            return True
        logger.warning(f"Permission denied: Role '{user_role}' lacks '{required_permission}'")
        return False
