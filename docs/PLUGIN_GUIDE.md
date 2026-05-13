# Plugin & Skill Development Guide

The Enterprise AI Agent platform is designed to be extensible through **Skills**. A skill is a encapsulated unit of capability that an agent can utilize.

## Skill Structure
Each skill must inherit from `BaseSkill` and define `SkillMetadata`.

```python
from core.skills.base import BaseSkill, SkillMetadata

class MySkill(BaseSkill):
    def __init__(self):
        super().__init__(SkillMetadata(
            name="unique_skill_name",
            description="Clear description of what the skill does",
            version="1.0.0",
            author="Author Name",
            permissions=["required:permission"]
        ))

    async def execute(self, **kwargs):
        # Implementation logic
        return "Result"

    def get_tool_definitions(self):
        # Definitions for LLM function calling
        return [...]
```

## Tool Orchestration
Skills are executed through the `ToolService`, which handles:
1. **Governance Check:** Validating permissions and command safety.
2. **Execution:** Running the logic in a sandboxed environment.
3. **Audit:** Logging the execution details.

## Best Practices
- **Statelessness:** Skills should ideally be stateless.
- **Error Handling:** Return descriptive errors in the `ToolResult`.
- **Validation:** Use Pydantic for input validation where possible.
