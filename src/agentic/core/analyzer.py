import json
import importlib
import os
import inspect
from typing import Dict, Any, Optional
from src.agentic.llm.base import LLMProvider

class TaskAnalyzer:
    """Analyzes tasks to determine required agent structure"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm = LLMProvider.create(llm_config)
    
    async def analyze_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze task to determine required agents and structure"""
        
        prompt = self._create_analysis_prompt(task, context)
        response = await self.llm.generate(prompt)
        
        # Extract text from LLMResponse
        analysis = self._parse_response(response.text)  # Use the text attribute
        
        return {
            "task_type": analysis["task_type"],
            "required_agents": self._get_required_agents(analysis),
            "workflow_pattern": analysis["workflow_pattern"],
            "tools_required": analysis["tools_required"],
            "plugins_required": analysis["plugins_required"]
        }
    
    def _create_analysis_prompt(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        tools = self._tool_list()
        plugins = self._plugin_list()
        """Create prompt for task analysis"""
        return f"""
        Analyze the following task and determine the optimal agent structure.
        Provide response in JSON format with the following structure:
        {{
            "task_type": string,
            "required_agents": [{{
                "type": string,
                "role": string,
                "capabilities": [string]
            }}],
            "workflow_pattern": string,
            "tools_required": [string],
            "plugins_required": [string]
        }}
        
        Task: {task}
        Context: {json.dumps(context) if context else 'None'}
        Plugins: {plugins}
        Tools: {tools}
        """
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response"""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the response
            try:
                # Look for JSON-like structure in the response
                start_idx = response.find('{')
                end_idx = response.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx + 1]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                # If still fails, return structured format of the text response
                return self._structure_text_response(response)
    
    def _structure_text_response(self, text: str) -> Dict[str, Any]:
        """Convert text response to structured format"""
        try:
            # Default structure
            structured_response = {
                "task_type": "unknown",
                "required_agents": [],
                "workflow_pattern": "sequential",
                "tools_required": [],
                "plugins_required": []
            }
            
            # Extract information from text
            lines = text.strip().split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if "task type" in line.lower():
                    structured_response["task_type"] = line.split(":")[-1].strip()
                elif "agent" in line.lower():
                    agent_info = {
                        "type": line.split(":")[-1].strip(),
                        "role": "general",
                        "capabilities": []
                    }
                    structured_response["required_agents"].append(agent_info)
                elif "tool" in line.lower():
                    tool = line.split(":")[-1].strip()
                    structured_response["tools_required"].append(tool)
                elif "plugin" in line.lower():
                    plugin = line.split(":")[-1].strip()
                    structured_response["plugins_required"].append(plugin)
                elif "workflow" in line.lower():
                    structured_response["workflow_pattern"] = line.split(":")[-1].strip()
            
            return structured_response
            
        except Exception as e:
            # Return basic structure if parsing fails
            return {
                "task_type": "general",
                "required_agents": [{"type": "general", "role": "executor", "capabilities": []}],
                "workflow_pattern": "sequential",
                "tools_required": ["basic_tools"],
                "plugins_required": []
            }
    
    def _get_required_agents(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract required agents from analysis"""
        try:
            if "required_agents" in analysis:
                return analysis["required_agents"]
            
            # If agent information is in a different format
            agents = {}
            for key, value in analysis.items():
                if isinstance(value, dict) and "role" in value:
                    agents[key] = {
                        "type": key,
                        "role": value["role"],
                        "capabilities": value.get("capabilities", [])
                    }
            
            return agents or {
                "general_agent": {
                    "type": "general",
                    "role": "executor",
                    "capabilities": []
                }
            }
            
        except Exception:
            # Return default agent if parsing fails
            return {
                "general_agent": {
                    "type": "general",
                    "role": "executor",
                    "capabilities": []
                }
            }
        
    def _tool_list(self):
        tool_names = []
        # Define the directory path
        directory_path = "src/agentic/tools/implementations"
        base_module_path = directory_path.replace("/", ".")

        # Get all .py files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove '.py' extension
                full_module_path = f"{base_module_path}.{module_name}"

                # Dynamically import each module
                try:
                    module = importlib.import_module(full_module_path)
                except ModuleNotFoundError:
                    print(f"Module {full_module_path} not found.")
                    continue

                # Inspect for classes within each module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Ensure the class is defined in the current module
                    if obj.__module__ == full_module_path:
                        tool_names.append(name)

        return tool_names
    
    def _plugin_list(self):
        tool_names = []
        # Define the directory path
        directory_path = "src/agentic/plugins/implementations"
        base_module_path = directory_path.replace("/", ".")

        # Get all .py files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove '.py' extension
                full_module_path = f"{base_module_path}.{module_name}"

                # Dynamically import each module
                try:
                    module = importlib.import_module(full_module_path)
                except ModuleNotFoundError:
                    print(f"Module {full_module_path} not found.")
                    continue

                # Inspect for classes within each module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Ensure the class is defined in the current module
                    if obj.__module__ == full_module_path:
                        tool_names.append(name)

        return tool_names