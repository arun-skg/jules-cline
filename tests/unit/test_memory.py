import pytest
from core.memory.manager import MemoryManager

def test_memory_store_retrieve():
    manager = MemoryManager()
    manager.store("test_key", "test_value", {"meta": "data"})

    assert manager.retrieve("test_key") == "test_value"
    assert manager.retrieve("non_existent") is None

def test_memory_search_episodic():
    manager = MemoryManager()
    manager.store("task_1", "output_1")
    manager.store("task_2", "output_2")
    manager.store("other", "output_3")

    results = manager.search_episodic("task")
    assert len(results) == 2
    assert results[0].key == "task_1"
    assert results[1].key == "task_2"
