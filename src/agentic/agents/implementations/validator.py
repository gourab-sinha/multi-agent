from typing import Dict, Any, List, Optional
from datetime import datetime
from src.agentic.agents.base import BaseAgent

class ValidatorAgent(BaseAgent):
    """Agent responsible for content validation, fact checking, and quality assurance"""
    
    async def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        step: int
    ) -> Dict[str, Any]:
        try:
            # Wait for content to validate
            content_data = await self.receive_message()
            if not content_data:
                return {
                    "status": "waiting",
                    "agent_id": self.agent_id
                }
            
            # Validate based on content type
            content_type = content_data.get("type", "general")
            validation_results = await self._validate_content(
                content_data.get("data", {}),
                content_type,
                context
            )
            
            # Store validation results
            await self.store_memory(
                f"validation_results_{step}",
                validation_results,
                ttl=3600
            )
            
            if validation_results["passed"]:
                # Content passed validation
                return {
                    "status": "success",
                    "agent_id": self.agent_id,
                    "validation": validation_results,
                    "content": content_data["data"]
                }
            else:
                # Request revisions
                await self._request_revisions(
                    content_data,
                    validation_results
                )
                return {
                    "status": "revision_requested",
                    "agent_id": self.agent_id,
                    "validation": validation_results
                }
                
        except Exception as e:
            return {
                "status": "error",
                "agent_id": self.agent_id,
                "error": str(e)
            }
    
    async def _validate_content(
        self,
        content: Dict[str, Any],
        content_type: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate content based on type and requirements"""
        validation_results = {
            "passed": True,
            "checks": [],
            "issues": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # 1. Basic validation
        basic_checks = await self._perform_basic_validation(content, context)
        validation_results["checks"].extend(basic_checks)
        
        # 2. Content type specific validation
        if content_type == "research":
            type_checks = await self._validate_research_content(content)
        elif content_type == "analysis":
            type_checks = await self._validate_analysis_content(content)
        elif content_type == "report":
            type_checks = await self._validate_report_content(content)
        else:
            type_checks = await self._validate_general_content(content)
            
        validation_results["checks"].extend(type_checks)
        
        # 3. Fact checking if required
        if context and context.get("fact_checking", True):
            fact_checks = await self._perform_fact_checking(content)
            validation_results["checks"].extend(fact_checks)
        
        # 4. Quality checks
        quality_checks = await self._perform_quality_checks(content, context)
        validation_results["checks"].extend(quality_checks)
        
        # Collect issues
        validation_results["issues"] = [
            check for check in validation_results["checks"]
            if not check["passed"]
        ]
        
        # Update overall status
        validation_results["passed"] = len(validation_results["issues"]) == 0
        
        return validation_results
    
    async def _perform_basic_validation(
        self,
        content: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Perform basic content validation"""
        checks = []
        
        # Check content structure
        checks.append({
            "type": "structure",
            "passed": self._validate_structure(content),
            "message": "Content structure validation"
        })
        
        # Check content length
        if context and "min_length" in context:
            length_check = self._validate_length(
                content,
                context["min_length"],
                context.get("max_length")
            )
            checks.append({
                "type": "length",
                "passed": length_check["passed"],
                "message": length_check["message"]
            })
        
        return checks
    
    async def _validate_research_content(
        self,
        content: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Validate research content"""
        checks = []
        
        # Check citations
        citations_check = await self._validate_citations(content)
        checks.append({
            "type": "citations",
            "passed": citations_check["passed"],
            "message": citations_check["message"]
        })
        
        # Check methodology
        if "methodology" in content:
            methodology_check = self._validate_methodology(content["methodology"])
            checks.append({
                "type": "methodology",
                "passed": methodology_check["passed"],
                "message": methodology_check["message"]
            })
        
        return checks
    
    async def _validate_analysis_content(
        self,
        content: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Validate analysis content"""
        checks = []
        
        # Check data support
        data_check = self._validate_data_support(content)
        checks.append({
            "type": "data_support",
            "passed": data_check["passed"],
            "message": data_check["message"]
        })
        
        # Check analysis depth
        depth_check = self._validate_analysis_depth(content)
        checks.append({
            "type": "analysis_depth",
            "passed": depth_check["passed"],
            "message": depth_check["message"]
        })
        
        return checks
    
    async def _perform_fact_checking(
        self,
        content: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Perform fact checking using validation tools"""
        checks = []
        
        try:
            # Use fact checking tool
            fact_check_results = await self.use_tool(
                "fact_checker",
                {
                    "content": content,
                    "confidence_threshold": 0.8
                }
            )
            
            checks.append({
                "type": "fact_check",
                "passed": fact_check_results["passed"],
                "message": "Fact checking validation",
                "details": fact_check_results.get("details", {})
            })
            
        except Exception as e:
            checks.append({
                "type": "fact_check",
                "passed": False,
                "message": f"Fact checking failed: {str(e)}"
            })
        
        return checks
    
    async def _perform_quality_checks(
        self,
        content: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Perform quality assurance checks"""
        checks = []
        
        # Use quality checker tool
        try:
            quality_results = await self.use_tool(
                "quality_checker",
                {
                    "content": content,
                    "requirements": context.get("quality_requirements", {})
                }
            )
            
            checks.extend([
                {
                    "type": f"quality_{check['type']}",
                    "passed": check["passed"],
                    "message": check["message"],
                    "score": check.get("score")
                }
                for check in quality_results["checks"]
            ])
            
        except Exception as e:
            checks.append({
                "type": "quality",
                "passed": False,
                "message": f"Quality check failed: {str(e)}"
            })
        
        return checks
    
    async def _request_revisions(
        self,
        content_data: Dict[str, Any],
        validation_results: Dict[str, Any]
    ):
        """Request content revisions from appropriate agent"""
        await self.send_message(
            content_data["source_agent"],
            {
                "type": "revision_request",
                "content_id": content_data.get("content_id"),
                "validation_results": validation_results,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

# Example usage:
"""
# Initialize validator agent
validator = ValidatorAgent(
    agent_id="validator_1",
    config={
        "validation_requirements": {
            "min_length": 1000,
            "fact_checking": True,
            "quality_threshold": 0.8
        }
    },
    message_bus=message_bus,
    tool_registry=tool_registry,
    plugin_registry=plugin_registry,
    memory=memory
)

# Execute validation
result = await validator.execute(
    task="Validate research report",
    context={
        "content_type": "research",
        "fact_checking": True,
        "quality_requirements": {
            "clarity": 0.8,
            "coherence": 0.8,
            "support": 0.8
        }
    },
    step=1
)
"""