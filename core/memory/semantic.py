from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from loguru import logger
import json

class MemoryEntry(BaseModel):
    key: str
    value: Any
    metadata: Optional[Dict[str, Any]] = None

class SemanticMemoryManager:
    def __init__(self):
        self.short_term: List[Dict[str, Any]] = []
        self.episodic: List[MemoryEntry] = []
        self.core_facts: Dict[str, str] = {} # Summarized context

    def add_message(self, role: str, content: str):
        self.short_term.append({"role": role, "content": content})
        if len(self.short_term) > 10:
            # Trigger semantic compression (placeholder for LLM call)
            self._compress_context()

    def _compress_context(self):
        logger.info("Triggering semantic context compression...")

        # Combine messages to summarize
        to_summarize = "\n".join([f"{m['role']}: {m['content']}" for m in self.short_term])

        # Simulated logic for "Token Friendly" semantic extraction
        # This reduces 10 messages (potentially thousands of tokens) into a few core facts.
        core_fact = f"Semantic insight from interaction: Focused on enhancing {self.short_term[0]['content'][:50]}..."

        fact_id = f"fact_{len(self.core_facts)}"
        self.core_facts[fact_id] = core_fact

        # Evict old short-term memory to save tokens in prompt
        self.short_term = self.short_term[-3:]
        logger.info(f"Context compressed. Saved approx {len(to_summarize) // 4} tokens. Core facts count: {len(self.core_facts)}")

    def get_context_prompt(self) -> str:
        facts = "\n".join([f"- {v}" for v in self.core_facts.values()])
        recent = "\n".join([f"{m['role']}: {m['content']}" for m in self.short_term])
        return f"Core Facts:\n{facts}\n\nRecent Conversation:\n{recent}"

    def store(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None):
        self.episodic.append(MemoryEntry(key=key, value=value, metadata=metadata))

    def search_episodic(self, query: str) -> List[MemoryEntry]:
        return [entry for entry in self.episodic if query.lower() in entry.key.lower()]
