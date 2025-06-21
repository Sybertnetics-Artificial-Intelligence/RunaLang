"""
Context Manager for Runa Natural Language Parsing
================================================

Tracks parsing context to resolve ambiguities in natural language constructs.
This is essential for Runa's core differentiator - natural language programming.
"""

from typing import Dict, List, Optional, Any, Set
from enum import Enum
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class ContextType(Enum):
    """Types of parsing contexts."""
    GLOBAL = "global"
    FUNCTION_DEFINITION = "function_definition"
    FUNCTION_CALL = "function_call"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    ASSIGNMENT = "assignment"
    EXPRESSION = "expression"
    LLM_COMMUNICATION = "llm_communication"
    AGENT_COORDINATION = "agent_coordination"
    SELF_MODIFICATION = "self_modification"
    KNOWLEDGE_GRAPH = "knowledge_graph"


@dataclass
class ContextFrame:
    """A single context frame with metadata."""
    context_type: ContextType
    parent: Optional['ContextFrame'] = None
    variables: Set[str] = field(default_factory=set)
    functions: Set[str] = field(default_factory=set)
    agents: Set[str] = field(default_factory=set)
    llms: Set[str] = field(default_factory=set)
    knowledge_entities: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.parent:
            # Inherit from parent context
            self.variables.update(self.parent.variables)
            self.functions.update(self.parent.functions)
            self.agents.update(self.parent.agents)
            self.llms.update(self.parent.llms)
            self.knowledge_entities.update(self.parent.knowledge_entities)


class ContextManager:
    """
    Manages parsing context for natural language disambiguation.
    
    Tracks:
    - Current parsing context (function, conditional, etc.)
    - Available variables, functions, agents, LLMs
    - Context-specific disambiguation rules
    - Semantic relationships between entities
    """
    
    def __init__(self):
        self.context_stack: List[ContextFrame] = []
        self.global_context = ContextFrame(ContextType.GLOBAL)
        self.current_frame = self.global_context
        self.disambiguation_cache: Dict[str, Any] = {}
        
    def push_context(self, context_type: ContextType, **metadata) -> ContextFrame:
        """Push a new context frame onto the stack."""
        new_frame = ContextFrame(
            context_type=context_type,
            parent=self.current_frame,
            metadata=metadata
        )
        self.context_stack.append(new_frame)
        self.current_frame = new_frame
        logger.debug(f"Pushed context: {context_type.value}")
        return new_frame
    
    def pop_context(self) -> Optional[ContextFrame]:
        """Pop the current context frame from the stack."""
        if len(self.context_stack) > 0:
            popped = self.context_stack.pop()
            self.current_frame = self.context_stack[-1] if self.context_stack else self.global_context
            logger.debug(f"Popped context: {popped.context_type.value}")
            return popped
        return None
    
    def get_current_context(self) -> ContextFrame:
        """Get the current context frame."""
        return self.current_frame
    
    def add_variable(self, name: str):
        """Add a variable to the current context."""
        self.current_frame.variables.add(name)
        logger.debug(f"Added variable: {name}")
    
    def add_function(self, name: str):
        """Add a function to the current context."""
        self.current_frame.functions.add(name)
        logger.debug(f"Added function: {name}")
    
    def add_agent(self, name: str):
        """Add an agent to the current context."""
        self.current_frame.agents.add(name)
        logger.debug(f"Added agent: {name}")
    
    def add_llm(self, name: str):
        """Add an LLM to the current context."""
        self.current_frame.llms.add(name)
        logger.debug(f"Added LLM: {name}")
    
    def add_knowledge_entity(self, name: str):
        """Add a knowledge entity to the current context."""
        self.current_frame.knowledge_entities.add(name)
        logger.debug(f"Added knowledge entity: {name}")
    
    def resolve_ambiguity(self, token: str, candidates: List[str], 
                         context_hints: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Resolve ambiguity between multiple candidates based on context.
        
        Args:
            token: The ambiguous token
            candidates: List of possible interpretations
            context_hints: Additional context information
            
        Returns:
            The most likely interpretation based on context
        """
        if not candidates:
            return None
            
        if len(candidates) == 1:
            return candidates[0]
        
        # Check cache first
        cache_key = f"{token}:{','.join(sorted(candidates))}"
        if cache_key in self.disambiguation_cache:
            return self.disambiguation_cache[cache_key]
        
        # Score each candidate based on context
        scores = {}
        for candidate in candidates:
            score = self._calculate_context_score(candidate, context_hints)
            scores[candidate] = score
        
        # Return the highest scoring candidate
        best_candidate = max(scores.items(), key=lambda x: x[1])[0]
        
        # Cache the result
        self.disambiguation_cache[cache_key] = best_candidate
        
        logger.debug(f"Resolved ambiguity '{token}' -> '{best_candidate}' (scores: {scores})")
        return best_candidate
    
    def _calculate_context_score(self, candidate: str, 
                                context_hints: Optional[Dict[str, Any]] = None) -> float:
        """Calculate a context score for a candidate interpretation."""
        score = 0.0
        
        # Check if candidate exists in current context
        if candidate in self.current_frame.variables:
            score += 10.0
        if candidate in self.current_frame.functions:
            score += 8.0
        if candidate in self.current_frame.agents:
            score += 6.0
        if candidate in self.current_frame.llms:
            score += 6.0
        if candidate in self.current_frame.knowledge_entities:
            score += 4.0
        
        # Context-specific scoring
        if context_hints:
            # Prefer variables in assignment contexts
            if (self.current_frame.context_type == ContextType.ASSIGNMENT and 
                candidate in self.current_frame.variables):
                score += 5.0
            
            # Prefer functions in function call contexts
            if (self.current_frame.context_type == ContextType.FUNCTION_CALL and 
                candidate in self.current_frame.functions):
                score += 5.0
            
            # Prefer agents in agent coordination contexts
            if (self.current_frame.context_type == ContextType.AGENT_COORDINATION and 
                candidate in self.current_frame.agents):
                score += 5.0
            
            # Prefer LLMs in LLM communication contexts
            if (self.current_frame.context_type == ContextType.LLM_COMMUNICATION and 
                candidate in self.current_frame.llms):
                score += 5.0
        
        return score
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get a summary of the current context for debugging."""
        return {
            "context_type": self.current_frame.context_type.value,
            "variables": list(self.current_frame.variables),
            "functions": list(self.current_frame.functions),
            "agents": list(self.current_frame.agents),
            "llms": list(self.current_frame.llms),
            "knowledge_entities": list(self.current_frame.knowledge_entities),
            "stack_depth": len(self.context_stack),
            "metadata": self.current_frame.metadata
        }
    
    def clear_cache(self):
        """Clear the disambiguation cache."""
        self.disambiguation_cache.clear()
        logger.debug("Cleared disambiguation cache") 