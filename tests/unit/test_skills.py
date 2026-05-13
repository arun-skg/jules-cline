import pytest
import os
import shutil
from core.skills.filesystem import FileSystemSkill

@pytest.fixture
def temp_fs():
    base_dir = "/tmp/test_agent_fs"
    os.makedirs(base_dir, exist_ok=True)
    yield base_dir
    shutil.rmtree(base_dir)

@pytest.mark.asyncio
async def test_fs_skill_write_read(temp_fs):
    skill = FileSystemSkill(base_path=temp_fs)

    # Test Write
    write_result = await skill.execute(action="write", path="test.txt", content="hello world")
    assert "Successfully wrote" in write_result.output

    # Test Read
    read_result = await skill.execute(action="read", path="test.txt")
    assert read_result.output == "hello world"

@pytest.mark.asyncio
async def test_fs_skill_security(temp_fs):
    skill = FileSystemSkill(base_path=temp_fs)

    # Try to access outside base path
    result = await skill.execute(action="read", path="../../../../etc/passwd")
    assert "Access denied" in result.error
