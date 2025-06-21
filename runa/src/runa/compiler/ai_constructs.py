"""
AI-Specific AST Nodes for Runa
==============================

AST nodes for AI-native constructs including:
- LLM communication protocol syntax
- AI agent coordination patterns
- Self-modification language constructs
- Knowledge graph integration syntax
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .ast_base import ASTNode, Expression, Statement


@dataclass
class LLMCommunication(ASTNode):
    """AST node for LLM-to-LLM communication."""
    operation: str  # "ask", "tell", "query", "instruct"
    target_llm: str
    content: str
    parameters: Optional[Dict[str, Any]] = None
    
    def __init__(self, operation: str, target_llm: str, content: str, 
                 parameters: Optional[Dict[str, Any]] = None):
        self.operation = operation
        self.target_llm = target_llm
        self.content = content
        self.parameters = parameters or {}


@dataclass
class AgentCoordination(ASTNode):
    """AST node for AI agent coordination."""
    operation: str  # "delegate", "wait", "broadcast", "coordinate"
    target_agent: Optional[str] = None
    task: str = ""
    parameters: Optional[Dict[str, Any]] = None
    
    def __init__(self, operation: str, task: str, target_agent: Optional[str] = None,
                 parameters: Optional[Dict[str, Any]] = None):
        self.operation = operation
        self.task = task
        self.target_agent = target_agent
        self.parameters = parameters or {}


@dataclass
class SelfModification(ASTNode):
    """AST node for safe self-modification constructs."""
    operation: str  # "modify", "add", "update", "remove"
    target: str
    modification: str
    safety_constraints: Optional[List[str]] = None
    
    def __init__(self, operation: str, target: str, modification: str,
                 safety_constraints: Optional[List[str]] = None):
        self.operation = operation
        self.target = target
        self.modification = modification
        self.safety_constraints = safety_constraints or []


@dataclass
class KnowledgeGraphOperation(ASTNode):
    """AST node for knowledge graph operations."""
    operation: str  # "query", "add", "update", "remove", "find"
    entity: str
    relationship: Optional[str] = None
    target: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    
    def __init__(self, operation: str, entity: str, relationship: Optional[str] = None,
                 target: Optional[str] = None, parameters: Optional[Dict[str, Any]] = None):
        self.operation = operation
        self.entity = entity
        self.relationship = relationship
        self.target = target
        self.parameters = parameters or {}


@dataclass
class AIContext(ASTNode):
    """AST node for AI context information."""
    context_type: str  # "llm", "agent", "knowledge", "modification"
    context_data: Dict[str, Any]
    
    def __init__(self, context_type: str, context_data: Dict[str, Any]):
        self.context_type = context_type
        self.context_data = context_data


@dataclass
class AIPattern(ASTNode):
    """AST node for AI pattern matching and recognition."""
    pattern_type: str  # "semantic", "structural", "behavioral"
    pattern: str
    confidence: float
    alternatives: Optional[List[str]] = None
    
    def __init__(self, pattern_type: str, pattern: str, confidence: float,
                 alternatives: Optional[List[str]] = None):
        self.pattern_type = pattern_type
        self.pattern = pattern
        self.confidence = confidence
        self.alternatives = alternatives or []


@dataclass
class AILearning(ASTNode):
    """AST node for AI learning and adaptation."""
    learning_type: str  # "supervised", "unsupervised", "reinforcement"
    data_source: str
    learning_parameters: Optional[Dict[str, Any]] = None
    
    def __init__(self, learning_type: str, data_source: str,
                 learning_parameters: Optional[Dict[str, Any]] = None):
        self.learning_type = learning_type
        self.data_source = data_source
        self.learning_parameters = learning_parameters or {}


@dataclass
class AICapability(ASTNode):
    """AST node for AI capability definitions."""
    capability_name: str
    capability_type: str  # "function", "knowledge", "skill", "tool"
    description: str
    parameters: Optional[Dict[str, Any]] = None
    
    def __init__(self, capability_name: str, capability_type: str, description: str,
                 parameters: Optional[Dict[str, Any]] = None):
        self.capability_name = capability_name
        self.capability_type = capability_type
        self.description = description
        self.parameters = parameters or {}


@dataclass
class AISafety(ASTNode):
    """AST node for AI safety constraints and validation."""
    constraint_type: str  # "ethical", "security", "performance", "privacy"
    constraint: str
    validation_rules: Optional[List[str]] = None
    
    def __init__(self, constraint_type: str, constraint: str,
                 validation_rules: Optional[List[str]] = None):
        self.constraint_type = constraint_type
        self.constraint = constraint
        self.validation_rules = validation_rules or []


@dataclass
class AICoordination(ASTNode):
    """AST node for complex AI coordination scenarios."""
    coordination_type: str  # "sequential", "parallel", "hierarchical", "distributed"
    agents: List[str]
    tasks: List[str]
    coordination_rules: Optional[Dict[str, Any]] = None
    
    def __init__(self, coordination_type: str, agents: List[str], tasks: List[str],
                 coordination_rules: Optional[Dict[str, Any]] = None):
        self.coordination_type = coordination_type
        self.agents = agents
        self.tasks = tasks
        self.coordination_rules = coordination_rules or {}


@dataclass
class AIDecision(ASTNode):
    """AST node for AI decision-making constructs."""
    decision_type: str  # "conditional", "probabilistic", "multi-criteria", "consensus"
    criteria: List[str]
    options: List[str]
    decision_parameters: Optional[Dict[str, Any]] = None
    
    def __init__(self, decision_type: str, criteria: List[str], options: List[str],
                 decision_parameters: Optional[Dict[str, Any]] = None):
        self.decision_type = decision_type
        self.criteria = criteria
        self.options = options
        self.decision_parameters = decision_parameters or {}


@dataclass
class AIIntegration(ASTNode):
    """AST node for AI system integration."""
    integration_type: str  # "api", "database", "service", "protocol"
    target_system: str
    integration_method: str
    configuration: Optional[Dict[str, Any]] = None
    
    def __init__(self, integration_type: str, target_system: str, integration_method: str,
                 configuration: Optional[Dict[str, Any]] = None):
        self.integration_type = integration_type
        self.target_system = target_system
        self.integration_method = integration_method
        self.configuration = configuration or {}


# AI-specific statement types
@dataclass
class LLMCommunicationStatement(Statement):
    """Statement for LLM communication."""
    communication: LLMCommunication
    
    def __init__(self, communication: LLMCommunication):
        self.communication = communication


@dataclass
class AgentCoordinationStatement(Statement):
    """Statement for agent coordination."""
    coordination: AgentCoordination
    
    def __init__(self, coordination: AgentCoordination):
        self.coordination = coordination


@dataclass
class SelfModificationStatement(Statement):
    """Statement for self-modification."""
    modification: SelfModification
    
    def __init__(self, modification: SelfModification):
        self.modification = modification


@dataclass
class KnowledgeGraphStatement(Statement):
    """Statement for knowledge graph operations."""
    operation: KnowledgeGraphOperation
    
    def __init__(self, operation: KnowledgeGraphOperation):
        self.operation = operation


@dataclass
class AIContextStatement(Statement):
    """Statement for AI context."""
    context: AIContext
    
    def __init__(self, context: AIContext):
        self.context = context


@dataclass
class AIPatternStatement(Statement):
    """Statement for AI patterns."""
    pattern: AIPattern
    
    def __init__(self, pattern: AIPattern):
        self.pattern = pattern


@dataclass
class AILearningStatement(Statement):
    """Statement for AI learning."""
    learning: AILearning
    
    def __init__(self, learning: AILearning):
        self.learning = learning


@dataclass
class AICapabilityStatement(Statement):
    """Statement for AI capabilities."""
    capability: AICapability
    
    def __init__(self, capability: AICapability):
        self.capability = capability


@dataclass
class AISafetyStatement(Statement):
    """Statement for AI safety."""
    safety: AISafety
    
    def __init__(self, safety: AISafety):
        self.safety = safety


@dataclass
class AICoordinationStatement(Statement):
    """Statement for AI coordination."""
    coordination: AICoordination
    
    def __init__(self, coordination: AICoordination):
        self.coordination = coordination


@dataclass
class AIDecisionStatement(Statement):
    """Statement for AI decisions."""
    decision: AIDecision
    
    def __init__(self, decision: AIDecision):
        self.decision = decision


@dataclass
class AIIntegrationStatement(Statement):
    """Statement for AI integration."""
    integration: AIIntegration
    
    def __init__(self, integration: AIIntegration):
        self.integration = integration


# AI-specific expression types
@dataclass
class LLMCommunicationExpression(Expression):
    """Expression for LLM communication."""
    communication: LLMCommunication
    
    def __init__(self, communication: LLMCommunication):
        self.communication = communication


@dataclass
class AgentCoordinationExpression(Expression):
    """Expression for agent coordination."""
    coordination: AgentCoordination
    
    def __init__(self, coordination: AgentCoordination):
        self.coordination = coordination


@dataclass
class KnowledgeGraphExpression(Expression):
    """Expression for knowledge graph operations."""
    operation: KnowledgeGraphOperation
    
    def __init__(self, operation: KnowledgeGraphOperation):
        self.operation = operation


@dataclass
class AIPatternExpression(Expression):
    """Expression for AI patterns."""
    pattern: AIPattern
    
    def __init__(self, pattern: AIPattern):
        self.pattern = pattern


@dataclass
class AIDecisionExpression(Expression):
    """Expression for AI decisions."""
    decision: AIDecision
    
    def __init__(self, decision: AIDecision):
        self.decision = decision 