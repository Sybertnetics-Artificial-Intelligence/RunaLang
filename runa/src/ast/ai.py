"""
AI-specific AST nodes for the Runa programming language.

This module defines the AST nodes for AI-specific features such as neural
network definitions, training configurations, and knowledge graph queries.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union, Set

from . import Node, NodeType, SourceLocation, Expression, Block
from .visitor import ASTVisitor


@dataclass
class ModelDefinition(Node):
    """
    Represents a neural network model definition.
    
    Attributes:
        name: The model name (as a string literal)
        body: The model definition body containing model statements
    """
    
    name: str
    body: 'ModelBlock'
    
    def __init__(
        self,
        name: str,
        body: 'ModelBlock',
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ModelDefinition node.
        
        Args:
            name: The model name
            body: The model definition body
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MODEL_DEFINITION, location)
        self.name = name
        self.body = body
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_model_definition(self)


@dataclass
class ModelBlock(Block):
    """
    Represents a block of model statements.
    
    Attributes:
        statements: The list of model statements
    """
    
    statements: List['ModelStatement']
    
    def __init__(
        self,
        statements: List['ModelStatement'],
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ModelBlock node.
        
        Args:
            statements: The list of model statements
            location: The source location of the node (optional)
        """
        super().__init__(statements, location)


@dataclass
class ModelStatement(Node):
    """
    Base class for all model statements.
    
    This is an abstract class that should not be instantiated directly.
    """
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_model_statement(self)


@dataclass
class InputLayerStatement(ModelStatement):
    """
    Represents an input layer definition in a neural network model.
    
    Attributes:
        shape_expr: Expression defining the input shape
    """
    
    shape_expr: Expression
    
    def __init__(
        self,
        shape_expr: Expression,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new InputLayerStatement node.
        
        Args:
            shape_expr: Expression defining the input shape
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MODEL_STATEMENT, location)
        self.shape_expr = shape_expr


@dataclass
class ConvolutionalLayerStatement(ModelStatement):
    """
    Represents a convolutional layer definition in a neural network model.
    
    Attributes:
        filters: Number of filters to start with
    """
    
    filters: int
    
    def __init__(
        self,
        filters: int,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ConvolutionalLayerStatement node.
        
        Args:
            filters: Number of filters to start with
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MODEL_STATEMENT, location)
        self.filters = filters


@dataclass
class DownsamplingStatement(ModelStatement):
    """
    Represents a downsampling configuration in a neural network model.
    """
    
    def __init__(
        self,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new DownsamplingStatement node.
        
        Args:
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MODEL_STATEMENT, location)


@dataclass
class ResidualConnectionStatement(ModelStatement):
    """
    Represents a residual connection configuration in a neural network model.
    """
    
    def __init__(
        self,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new ResidualConnectionStatement node.
        
        Args:
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MODEL_STATEMENT, location)


@dataclass
class OutputLayerStatement(ModelStatement):
    """
    Represents an output layer definition in a neural network model.
    
    Attributes:
        classes: Number of output classes
        activation: Activation function name
    """
    
    classes: int
    activation: str
    
    def __init__(
        self,
        classes: int,
        activation: str,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new OutputLayerStatement node.
        
        Args:
            classes: Number of output classes
            activation: Activation function name
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.MODEL_STATEMENT, location)
        self.classes = classes
        self.activation = activation


@dataclass
class TrainingConfig(Node):
    """
    Represents a training configuration for a neural network model.
    
    Attributes:
        model_name: The name of the model to train
        body: The training configuration body
    """
    
    model_name: str
    body: 'TrainingBlock'
    
    def __init__(
        self,
        model_name: str,
        body: 'TrainingBlock',
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new TrainingConfig node.
        
        Args:
            model_name: The name of the model to train
            body: The training configuration body
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRAINING_CONFIG, location)
        self.model_name = model_name
        self.body = body
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_training_config(self)


@dataclass
class TrainingBlock(Block):
    """
    Represents a block of training statements.
    
    Attributes:
        statements: The list of training statements
    """
    
    statements: List['TrainingStatement']
    
    def __init__(
        self,
        statements: List['TrainingStatement'],
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new TrainingBlock node.
        
        Args:
            statements: The list of training statements
            location: The source location of the node (optional)
        """
        super().__init__(statements, location)


@dataclass
class TrainingStatement(Node):
    """
    Base class for all training statements.
    
    This is an abstract class that should not be instantiated directly.
    """
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_training_statement(self)


@dataclass
class DatasetStatement(TrainingStatement):
    """
    Represents a dataset definition in a training configuration.
    
    Attributes:
        path: Path to the dataset
        config_expr: Expression for dataset configuration
    """
    
    path: str
    config_expr: Expression
    
    def __init__(
        self,
        path: str,
        config_expr: Expression,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new DatasetStatement node.
        
        Args:
            path: Path to the dataset
            config_expr: Expression for dataset configuration
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRAINING_STATEMENT, location)
        self.path = path
        self.config_expr = config_expr


@dataclass
class AugmentationStatement(TrainingStatement):
    """
    Represents a data augmentation configuration in a training configuration.
    
    Attributes:
        augmentation_expr: Expression defining the augmentation
    """
    
    augmentation_expr: Expression
    
    def __init__(
        self,
        augmentation_expr: Expression,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new AugmentationStatement node.
        
        Args:
            augmentation_expr: Expression defining the augmentation
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRAINING_STATEMENT, location)
        self.augmentation_expr = augmentation_expr


@dataclass
class OptimizerStatement(TrainingStatement):
    """
    Represents an optimizer configuration in a training configuration.
    
    Attributes:
        optimizer_name: Name of the optimizer
        learning_rate: Learning rate value
    """
    
    optimizer_name: str
    learning_rate: float
    
    def __init__(
        self,
        optimizer_name: str,
        learning_rate: float,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new OptimizerStatement node.
        
        Args:
            optimizer_name: Name of the optimizer
            learning_rate: Learning rate value
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRAINING_STATEMENT, location)
        self.optimizer_name = optimizer_name
        self.learning_rate = learning_rate


@dataclass
class TrainStatement(TrainingStatement):
    """
    Represents a training loop configuration in a training configuration.
    
    Attributes:
        epochs: Number of epochs to train for
        early_stopping_expr: Optional expression for early stopping condition
    """
    
    epochs: int
    early_stopping_expr: Optional[Expression] = None
    
    def __init__(
        self,
        epochs: int,
        early_stopping_expr: Optional[Expression] = None,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new TrainStatement node.
        
        Args:
            epochs: Number of epochs to train for
            early_stopping_expr: Optional expression for early stopping condition
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRAINING_STATEMENT, location)
        self.epochs = epochs
        self.early_stopping_expr = early_stopping_expr


@dataclass
class SaveModelStatement(TrainingStatement):
    """
    Represents a model saving configuration in a training configuration.
    
    Attributes:
        metric_expr: Expression defining the metric to use for saving the best model
    """
    
    metric_expr: Expression
    
    def __init__(
        self,
        metric_expr: Expression,
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new SaveModelStatement node.
        
        Args:
            metric_expr: Expression defining the metric to use for saving the best model
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.TRAINING_STATEMENT, location)
        self.metric_expr = metric_expr


@dataclass
class KnowledgeQuery(Node):
    """
    Represents a knowledge graph query.
    
    Attributes:
        method: The query method name (e.g., "query", "find", "relate", etc.)
        arguments: The arguments to the query
    """
    
    method: str
    arguments: List[Expression]
    
    def __init__(
        self,
        method: str,
        arguments: List[Expression],
        location: Optional[SourceLocation] = None
    ):
        """
        Initialize a new KnowledgeQuery node.
        
        Args:
            method: The query method name
            arguments: The arguments to the query
            location: The source location of the node (optional)
        """
        super().__init__(NodeType.KNOWLEDGE_QUERY, location)
        self.method = method
        self.arguments = arguments
    
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accept a visitor to process this node."""
        return visitor.visit_knowledge_query(self) 