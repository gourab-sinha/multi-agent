from typing import Dict, Any, Optional
import os
import yaml
from pydantic import BaseModel
from .defaults import DEFAULT_CONFIG

class Settings(BaseModel):
    """Framework settings management"""
    
    config: Dict[str, Any]
    
    def __init__(self, config_path: Optional[str] = None):
        config = DEFAULT_CONFIG.copy()
        
        # Load from config file if provided
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
                config.update(file_config)
        
        # Override with environment variables
        config = self._update_from_env(config)
        
        super().__init__(config=config)
    
    def _update_from_env(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update configuration with environment variables"""
        env_mapping = {
            "OPENAI_API_KEY": ("llm", "api_key"),
            "ANTHROPIC_API_KEY": ("llm", "api_key"),
            "GOOGLE_API_KEY": ("llm", "api_key"),
            "REDIS_URL": ("memory", "url")
        }
        
        for env_var, config_path in env_mapping.items():
            if env_var in os.environ:
                current = config
                for key in config_path[:-1]:
                    current = current.setdefault(key, {})
                current[config_path[-1]] = os.environ[env_var]
        
        return config
    
    @property
    def llm_config(self) -> Dict[str, Any]:
        return self.config["llm"]
    
    @property
    def memory_config(self) -> Dict[str, Any]:
        return self.config["memory"]
    
    @property
    def tools_config(self) -> Dict[str, Any]:
        return self.config["tools"]
    
    @property
    def plugins_config(self) -> Dict[str, Any]:
        return self.config["plugins"]