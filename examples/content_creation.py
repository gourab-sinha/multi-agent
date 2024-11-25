from src.agentic import AgentFlow

async def content_creation_example():
    """Example of content creation task"""
    framework = AgentFlow()
    
    task = """
    Create a series of technical blog posts about quantum computing:
    - Fundamental principles
    - Current applications
    - Future possibilities
    Include code examples and visualizations.
    """
    
    context = {
        "target_audience": "technical_professionals",
        "style": "technical_but_accessible",
        "series_length": 3,
        "posts_structure": [
            {
                "title": "Quantum Computing Basics",
                "sections": ["principles", "qubits", "superposition"]
            },
            {
                "title": "Quantum Algorithms",
                "sections": ["grover", "shor", "quantum_gates"]
            },
            {
                "title": "Quantum Future",
                "sections": ["challenges", "opportunities", "timeline"]
            }
        ]
    }
    
    result = await framework.execute(task, context)
    return result