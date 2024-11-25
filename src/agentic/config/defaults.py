from typing import Dict, Any
DEFAULT_CONFIG: Dict[str, Any] = {
    "llm": {
        "provider": "openai",
        "model": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    "memory": {
        "provider": "local",
        "ttl": 3600,
        "max_size": 1000
    },
    "tools": {
        "web_search": {
            "enabled": True,
            "max_results": 10
        },
        "data_analysis": {
            "enabled": True,
            "max_rows": 100000
        },
        "content_generation": {
            "enabled": True,
            "max_length": 4000
        }
    },
    "plugins": {
        "market_research": {
            "enabled": True,
            "update_frequency": 86400
        },
        "content_pipeline": {
            "enabled": True,
            "seo_optimization": True
        }
    },
    "execution": {
        "max_parallel_tasks": 5,
        "timeout": 300,
        "retry_attempts": 3
    }
}