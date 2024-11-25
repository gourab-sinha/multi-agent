import click
import asyncio
import yaml
import json
from typing import Dict, Any
from src.agentic.agent_flow import AgentFlow

@click.group()
def cli():
    """Agentic Framework CLI"""
    pass

@cli.command()
@click.argument('task')
@click.option('--context', '-c', help='Context in JSON format')
@click.option('--config', '-f', help='Configuration file path')
@click.option('--output', '-o', help='Output file path')
def execute(task: str, context: str = None, config: str = None, output: str = None):
    """Execute a task"""
    try:
        # Load configuration
        if config:
            with open(config, 'r') as f:
                config_data = yaml.safe_load(f)
        else:
            config_data = None
        
        # Parse context
        context_data = json.loads(context) if context else None
        
        # Execute task
        result = asyncio.run(_execute_task(task, context_data, config_data))
        
        # Handle output
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
        else:
            click.echo(json.dumps(result, indent=2))
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

async def _execute_task(
    task: str,
    context: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute task using framework"""
    framework = AgentFlow(config)
    return await framework.execute(task, context)

@cli.command()
@click.argument('tool_path')
@click.option('--name', '-n', required=True, help='Tool name')
@click.option('--config', '-c', help='Tool configuration in JSON format')
def register_tool(tool_path: str, name: str, config: str = None):
    """Register a custom tool"""
    try:
        # Import tool class
        module_path, class_name = tool_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        tool_class = getattr(module, class_name)
        
        # Parse configuration
        config_data = json.loads(config) if config else {}
        
        # Register tool
        framework = AgentFlow()
        asyncio.run(framework.register_tool(name, tool_class(config_data)))
        
        click.echo(f"Tool '{name}' registered successfully")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)