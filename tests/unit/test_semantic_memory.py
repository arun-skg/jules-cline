import asyncio
import pytest
from core.memory.semantic import SemanticMemoryManager

def test_semantic_compression():
    memory = SemanticMemoryManager()

    # Add 11 messages to trigger compression
    for i in range(11):
        memory.add_message("user", f"message {i}")

    # Check if compression happened (short_term should be reduced)
    assert len(memory.short_term) == 3
    assert len(memory.core_facts) == 1
    assert "Semantic insight" in memory.core_facts["fact_0"]

def test_context_prompt_generation():
    memory = SemanticMemoryManager()
    memory.add_message("user", "Hello")
    memory.core_facts["fact1"] = "User wants to build an agent."

    prompt = memory.get_context_prompt()
    assert "User wants to build an agent." in prompt
    assert "user: Hello" in prompt
