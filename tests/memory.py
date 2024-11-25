import pytest

@pytest.mark.asyncio
async def test_memory_operations(framework):
    """Test memory operations"""
    memory = framework.orchestrator.memory
    
    # Store
    await memory.store("test_key", {"data": "test_value"})
    
    # Retrieve
    value = await memory.retrieve("test_key")
    assert value["data"] == "test_value"
    
    # Delete
    await memory.delete("test_key")
    value = await memory.retrieve("test_key")
    assert value is None