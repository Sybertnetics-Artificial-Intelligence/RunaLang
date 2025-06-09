"""
AI module for the Runa programming language.

This module provides AI-specific functionality for the Runa programming language,
including neural network definitions, training configurations, and integration
with TensorFlow and PyTorch.
"""

import importlib.util

from .models import (
    create_tensorflow_model,
    create_pytorch_model,
    load_model,
    save_model
)

from .training import (
    configure_training,
    train_model,
    evaluate_model
)

from .knowledge import (
    connect_to_neo4j,
    execute_knowledge_query,
    create_knowledge_node,
    create_knowledge_relationship
)

__all__ = [
    # Model creation and management
    'create_tensorflow_model',
    'create_pytorch_model',
    'load_model',
    'save_model',
    
    # Training utilities
    'configure_training',
    'train_model',
    'evaluate_model',
    
    # Knowledge graph integration
    'connect_to_neo4j',
    'execute_knowledge_query',
    'create_knowledge_node',
    'create_knowledge_relationship'
] 