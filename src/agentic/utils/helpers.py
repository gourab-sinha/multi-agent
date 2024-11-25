import uuid
import time
from datetime import datetime
from typing import Dict, Any, Optional, Callable, TypeVar, Awaitable
import asyncio
import json

T = TypeVar('T')

def generate_id(prefix: str = "") -> str:
    """Generate unique identifier"""
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def format_timestamp(
    timestamp: Optional[float] = None,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """Format timestamp to string"""
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime(format)

def validate_config(
    config: Dict[str, Any],
    required_fields: Dict[str, type]
) -> bool:
    """Validate configuration dictionary"""
    try:
        for field, field_type in required_fields.items():
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(config[field], field_type):
                raise TypeError(
                    f"Field {field} must be of type {field_type.__name__}"
                )
        return True
    except (ValueError, TypeError) as e:
        raise ConfigurationError(str(e))

def deep_merge(
    dict1: Dict[str, Any],
    dict2: Dict[str, Any]
) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result

async def retry_with_backoff(
    func: Callable[..., Awaitable[T]],
    *args,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    **kwargs
) -> T:
    """Retry async function with exponential backoff"""
    delay = initial_delay
    last_exception = None
    
    for retry in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if retry == max_retries - 1:
                raise
            
            await asyncio.sleep(delay)
            delay = min(delay * exponential_base, max_delay)
    
    raise last_exception

class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass

# Example usage:
"""
# Setup logging
logger = setup_logger(
    "agentic",
    level="DEBUG",
    log_file="logs/agentic.log",
    json_format=True
)

# Generate ID
task_id = generate_id("task_")

# Validate config
config = {
    "llm": {
        "provider": "openai",
        "api_key": "..."
    }
}

required_fields = {
    "llm": dict,
    "llm.provider": str,
    "llm.api_key": str
}

try:
    validate_config(config, required_fields)
except ConfigurationError as e:
    logger.error(f"Configuration error: {str(e)}")

# Retry function
async def api_call():
    # API call implementation
    pass

result = await retry_with_backoff(
    api_call,
    max_retries=3,
    initial_delay=1.0
)
"""