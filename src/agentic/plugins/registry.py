import asyncio
from typing import Dict, Any, Optional
from src.agentic.plugins.base import BasePlugin
from src.agentic.plugins.seo_optimizer import SEOOptimizerPlugin
from src.agentic.plugins.implementations.content_optimizer import ContentOptimizerPlugin
from src.agentic.plugins.implementations.fact_checker import FactCheckerPlugin

class PluginRegistry:
    """Registry for managing plugins"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plugins: Dict[str, BasePlugin] = {}
        # Initialize default plugins without using asyncio.run
        self._load_default_plugins()
    
    def _load_default_plugins(self):
        """Load default plugins based on configuration"""
        default_plugins = {
            "content_optimizer": ContentOptimizerPlugin,
            "fact_checker": FactCheckerPlugin
        }
        
        for plugin_name, plugin_class in default_plugins.items():
            if self.config.get(plugin_name, {}).get("enabled", True):
                plugin = plugin_class(self.config.get(plugin_name, {}))
                self.plugins[plugin_name] = plugin
    
    async def initialize_plugins(self):
        """Initialize all plugins asynchronously"""
        for plugin_name, plugin in list(self.plugins.items()):
            try:
                is_initialized = await plugin.initialize()
                if not is_initialized:
                    del self.plugins[plugin_name]
            except Exception as e:
                print(f"Failed to initialize plugin {plugin_name}: {str(e)}")
                del self.plugins[plugin_name]
    
    async def register_plugin(self, name: str, plugin: BasePlugin) -> bool:
        """Register a new plugin"""
        if name in self.plugins:
            raise ValueError(f"Plugin already exists: {name}")
        
        try:
            is_initialized = await plugin.initialize()
            if is_initialized:
                self.plugins[name] = plugin
                return True
            return False
        except Exception as e:
            print(f"Failed to register plugin {name}: {str(e)}")
            return False
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get plugin by name"""
        return self.plugins.get(name)