from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class MemoryEntry(BaseModel):
    key: str
    value: Any
    metadata: Optional[Dict[str, Any]] = None

class MemoryManager:
    def __init__(self):
        self.short_term: Dict[str, Any] = {}
        self.episodic: List[MemoryEntry] = []

    def store(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None):
        self.short_term[key] = value
        self.episodic.append(MemoryEntry(key=key, value=value, metadata=metadata))

    def retrieve(self, key: str) -> Optional[Any]:
        return self.short_term.get(key)

    def search_episodic(self, query: str) -> List[MemoryEntry]:
        # Simple string matching for now; will be replaced with Vector search in Phase 6
        return [entry for entry in self.episodic if query.lower() in entry.key.lower()]
