from typing import Dict, Any, List, Optional
from src.agentic.plugins.base import BasePlugin
import re
import json

class ContentOptimizerPlugin(BasePlugin):
    """Plugin for optimizing content quality and readability"""
    
    async def initialize(self) -> bool:
        try:
            self.optimization_rules = {
                "readability": self._optimize_readability,
                "seo": self._optimize_seo,
                "engagement": self._optimize_engagement,
            }
            
            self.metrics = {
                "readability_score": 0.0,
                "seo_score": 0.0,
                "engagement_score": 0.0,
                "clarity_score": 0.0
            }
            
            return True
        except Exception:
            return False
    
    async def execute(
        self,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute content optimization"""
        try:
            content = parameters.get("content", "")
            optimization_types = parameters.get("optimization_types", ["readability", "seo"])
            
            # Initial content analysis
            analysis = await self._analyze_content(content)
            
            # Apply optimizations
            optimized_content = content
            improvements = []
            
            for opt_type in optimization_types:
                if opt_type in self.optimization_rules:
                    result = await self.optimization_rules[opt_type](
                        optimized_content,
                        parameters.get(f"{opt_type}_settings", {})
                    )
                    optimized_content = result["content"]
                    improvements.extend(result["improvements"])
            
            # Final analysis
            final_analysis = await self._analyze_content(optimized_content)
            
            return {
                "status": "success",
                "original_content": content,
                "optimized_content": optimized_content,
                "improvements": improvements,
                "metrics": {
                    "original": analysis,
                    "optimized": final_analysis
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _analyze_content(
        self,
        content: str
    ) -> Dict[str, float]:
        """Analyze content metrics"""
        metrics = {}
        
        # Readability analysis
        metrics["readability_score"] = await self._calculate_readability(content)
        
        # SEO analysis
        metrics["seo_score"] = await self._analyze_seo(content)
        
        # Engagement analysis
        metrics["engagement_score"] = await self._analyze_engagement(content)
        
        return metrics
    
    async def _optimize_readability(
        self,
        content: str,
        settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize content readability"""
        improvements = []
        optimized_content = content
        
        # Sentence length optimization
        max_sentence_length = settings.get("max_sentence_length", 20)
        sentences = re.split(r'[.!?]+', content)
        
        for i, sentence in enumerate(sentences):
            if len(sentence.split()) > max_sentence_length:
                # Use LLM to split long sentences
                improved = await self._llm_improve_sentence(sentence)
                optimized_content = optimized_content.replace(sentence, improved)
                improvements.append({
                    "type": "sentence_length",
                    "original": sentence,
                    "improved": improved
                })
        
        # Paragraph structure
        paragraphs = content.split('\n\n')
        if any(len(p.split()) > settings.get("max_paragraph_words", 100) for p in paragraphs):
            optimized_content = await self._restructure_paragraphs(
                optimized_content,
                settings.get("max_paragraph_words", 100)
            )
            improvements.append({
                "type": "paragraph_structure",
                "message": "Improved paragraph structure for better readability"
            })
        
        return {
            "content": optimized_content,
            "improvements": improvements
        }
    
    async def _optimize_seo(
        self,
        content: str,
        settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize content for SEO"""
        improvements = []
        optimized_content = content
        
        # Keyword optimization
        target_keywords = settings.get("target_keywords", [])
        if target_keywords:
            keyword_analysis = await self._analyze_keyword_usage(
                content,
                target_keywords
            )
            
            if keyword_analysis["needs_improvement"]:
                optimized_content = await self._optimize_keyword_usage(
                    optimized_content,
                    keyword_analysis
                )
                improvements.append({
                    "type": "keyword_optimization",
                    "details": keyword_analysis["details"]
                })
        
        # Header structure
        if not re.search(r'<h1>|#\s', content):
            optimized_content = await self._add_header_structure(optimized_content)
            improvements.append({
                "type": "header_structure",
                "message": "Added proper header hierarchy"
            })
        
        return {
            "content": optimized_content,
            "improvements": improvements
        }
    
    async def _optimize_engagement(
        self,
        content: str,
        settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize content for engagement"""
        improvements = []
        optimized_content = content
        
        # Add hooks and calls to action
        if settings.get("add_hooks", True):
            hook = await self._generate_hook(content)
            optimized_content = f"{hook}\n\n{optimized_content}"
            improvements.append({
                "type": "hook_added",
                "hook": hook
            })
        
        # Add engaging elements
        if settings.get("add_engagement_elements", True):
            optimized_content = await self._add_engagement_elements(
                optimized_content,
                settings.get("engagement_types", ["questions", "examples"])
            )
            improvements.append({
                "type": "engagement_elements",
                "message": "Added engaging elements"
            })
        
        return {
            "content": optimized_content,
            "improvements": improvements
        }