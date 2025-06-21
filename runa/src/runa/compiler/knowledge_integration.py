"""
Knowledge Graph Integration for Runa
====================================

Provides knowledge graph operations and syntax for Runa's AI-native constructs.
This enables seamless integration with knowledge bases and semantic reasoning.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import logging
from .ai_constructs import KnowledgeGraphOperation

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntity:
    """Represents a knowledge entity in the graph."""
    name: str
    entity_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    
    def __init__(self, name: str, entity_type: str, properties: Optional[Dict[str, Any]] = None,
                 relationships: Optional[Dict[str, List[str]]] = None):
        self.name = name
        self.entity_type = entity_type
        self.properties = properties or {}
        self.relationships = relationships or {}


@dataclass
class KnowledgeRelationship:
    """Represents a relationship between knowledge entities."""
    source: str
    target: str
    relationship_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, source: str, target: str, relationship_type: str,
                 properties: Optional[Dict[str, Any]] = None):
        self.source = source
        self.target = target
        self.relationship_type = relationship_type
        self.properties = properties or {}


class KnowledgeGraph:
    """
    In-memory knowledge graph for Runa's knowledge integration features.
    
    Features:
    - Entity and relationship management
    - Query operations
    - Semantic search
    - Pattern matching
    """
    
    def __init__(self):
        self.entities: Dict[str, KnowledgeEntity] = {}
        self.relationships: List[KnowledgeRelationship] = []
        self.entity_types: Set[str] = set()
        self.relationship_types: Set[str] = set()
        
    def add_entity(self, name: str, entity_type: str, 
                   properties: Optional[Dict[str, Any]] = None) -> KnowledgeEntity:
        """Add a new entity to the knowledge graph."""
        entity = KnowledgeEntity(name, entity_type, properties)
        self.entities[name] = entity
        self.entity_types.add(entity_type)
        logger.debug(f"Added entity: {name} (type: {entity_type})")
        return entity
    
    def add_relationship(self, source: str, target: str, relationship_type: str,
                        properties: Optional[Dict[str, Any]] = None) -> KnowledgeRelationship:
        """Add a new relationship to the knowledge graph."""
        if source not in self.entities:
            raise ValueError(f"Source entity '{source}' not found")
        if target not in self.entities:
            raise ValueError(f"Target entity '{target}' not found")
        
        relationship = KnowledgeRelationship(source, target, relationship_type, properties)
        self.relationships.append(relationship)
        self.relationship_types.add(relationship_type)
        
        # Update entity relationships
        if relationship_type not in self.entities[source].relationships:
            self.entities[source].relationships[relationship_type] = []
        self.entities[source].relationships[relationship_type].append(target)
        
        logger.debug(f"Added relationship: {source} --{relationship_type}--> {target}")
        return relationship
    
    def query_entities(self, entity_type: Optional[str] = None, 
                      properties: Optional[Dict[str, Any]] = None) -> List[KnowledgeEntity]:
        """Query entities by type and/or properties."""
        results = []
        
        for entity in self.entities.values():
            if entity_type and entity.entity_type != entity_type:
                continue
            
            if properties:
                matches = True
                for key, value in properties.items():
                    if key not in entity.properties or entity.properties[key] != value:
                        matches = False
                        break
                if not matches:
                    continue
            
            results.append(entity)
        
        return results
    
    def query_relationships(self, source: Optional[str] = None, 
                          target: Optional[str] = None,
                          relationship_type: Optional[str] = None) -> List[KnowledgeRelationship]:
        """Query relationships by source, target, and/or type."""
        results = []
        
        for relationship in self.relationships:
            if source and relationship.source != source:
                continue
            if target and relationship.target != target:
                continue
            if relationship_type and relationship.relationship_type != relationship_type:
                continue
            
            results.append(relationship)
        
        return results
    
    def find_path(self, source: str, target: str, 
                  max_depth: int = 3) -> Optional[List[KnowledgeRelationship]]:
        """Find a path between two entities."""
        if source not in self.entities or target not in self.entities:
            return None
        
        # Simple BFS path finding
        visited = set()
        queue = [(source, [])]
        
        while queue:
            current, path = queue.pop(0)
            
            if current == target:
                return path
            
            if current in visited or len(path) >= max_depth:
                continue
            
            visited.add(current)
            
            # Find all relationships from current entity
            for relationship in self.relationships:
                if relationship.source == current:
                    new_path = path + [relationship]
                    queue.append((relationship.target, new_path))
        
        return None
    
    def get_entity_neighbors(self, entity_name: str, 
                           relationship_type: Optional[str] = None) -> List[KnowledgeEntity]:
        """Get neighboring entities of a given entity."""
        if entity_name not in self.entities:
            return []
        
        neighbors = []
        entity = self.entities[entity_name]
        
        for rel_type, targets in entity.relationships.items():
            if relationship_type and rel_type != relationship_type:
                continue
            
            for target in targets:
                if target in self.entities:
                    neighbors.append(self.entities[target])
        
        return neighbors
    
    def remove_entity(self, name: str) -> bool:
        """Remove an entity and all its relationships."""
        if name not in self.entities:
            return False
        
        # Remove all relationships involving this entity
        self.relationships = [
            rel for rel in self.relationships 
            if rel.source != name and rel.target != name
        ]
        
        # Remove entity
        del self.entities[name]
        
        logger.debug(f"Removed entity: {name}")
        return True
    
    def remove_relationship(self, source: str, target: str, 
                          relationship_type: str) -> bool:
        """Remove a specific relationship."""
        for i, relationship in enumerate(self.relationships):
            if (relationship.source == source and 
                relationship.target == target and 
                relationship.relationship_type == relationship_type):
                
                # Remove from relationships list
                del self.relationships[i]
                
                # Remove from entity relationships
                if source in self.entities:
                    entity = self.entities[source]
                    if relationship_type in entity.relationships:
                        if target in entity.relationships[relationship_type]:
                            entity.relationships[relationship_type].remove(target)
                
                logger.debug(f"Removed relationship: {source} --{relationship_type}--> {target}")
                return True
        
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics."""
        return {
            "entity_count": len(self.entities),
            "relationship_count": len(self.relationships),
            "entity_types": list(self.entity_types),
            "relationship_types": list(self.relationship_types)
        }


class KnowledgeGraphManager:
    """
    Manager for knowledge graph operations in Runa.
    
    Provides high-level operations for:
    - Knowledge graph creation and management
    - Query operations
    - Integration with Runa's AI constructs
    """
    
    def __init__(self):
        self.graphs: Dict[str, KnowledgeGraph] = {}
        self.default_graph = "main"
        self.graphs[self.default_graph] = KnowledgeGraph()
        
    def create_graph(self, name: str) -> KnowledgeGraph:
        """Create a new knowledge graph."""
        if name in self.graphs:
            raise ValueError(f"Knowledge graph '{name}' already exists")
        
        graph = KnowledgeGraph()
        self.graphs[name] = graph
        logger.debug(f"Created knowledge graph: {name}")
        return graph
    
    def get_graph(self, name: Optional[str] = None) -> KnowledgeGraph:
        """Get a knowledge graph by name."""
        graph_name = name or self.default_graph
        if graph_name not in self.graphs:
            raise ValueError(f"Knowledge graph '{graph_name}' not found")
        
        return self.graphs[graph_name]
    
    def execute_operation(self, operation: KnowledgeGraphOperation) -> Any:
        """Execute a knowledge graph operation."""
        graph = self.get_graph()
        
        if operation.operation == "query":
            return self._execute_query(graph, operation)
        elif operation.operation == "add":
            return self._execute_add(graph, operation)
        elif operation.operation == "update":
            return self._execute_update(graph, operation)
        elif operation.operation == "remove":
            return self._execute_remove(graph, operation)
        elif operation.operation == "find":
            return self._execute_find(graph, operation)
        else:
            raise ValueError(f"Unknown operation: {operation.operation}")
    
    def _execute_query(self, graph: KnowledgeGraph, operation: KnowledgeGraphOperation) -> List[KnowledgeEntity]:
        """Execute a query operation."""
        entity_type = operation.parameters.get("entity_type") if operation.parameters else None
        properties = operation.parameters.get("properties") if operation.parameters else None
        
        return graph.query_entities(entity_type, properties)
    
    def _execute_add(self, graph: KnowledgeGraph, operation: KnowledgeGraphOperation) -> Any:
        """Execute an add operation."""
        if operation.relationship:
            # Adding a relationship
            source = operation.entity
            target = operation.target
            if not target:
                raise ValueError("Target required for relationship addition")
            
            properties = operation.parameters or {}
            return graph.add_relationship(source, target, operation.relationship, properties)
        else:
            # Adding an entity
            entity_type = operation.parameters.get("entity_type", "unknown") if operation.parameters else "unknown"
            properties = operation.parameters.get("properties") if operation.parameters else None
            
            return graph.add_entity(operation.entity, entity_type, properties)
    
    def _execute_update(self, graph: KnowledgeGraph, operation: KnowledgeGraphOperation) -> bool:
        """Execute an update operation."""
        if operation.entity not in graph.entities:
            return False
        
        entity = graph.entities[operation.entity]
        properties = operation.parameters or {}
        
        for key, value in properties.items():
            entity.properties[key] = value
        
        logger.debug(f"Updated entity: {operation.entity}")
        return True
    
    def _execute_remove(self, graph: KnowledgeGraph, operation: KnowledgeGraphOperation) -> bool:
        """Execute a remove operation."""
        if operation.relationship and operation.target:
            # Removing a relationship
            return graph.remove_relationship(operation.entity, operation.target, operation.relationship)
        else:
            # Removing an entity
            return graph.remove_entity(operation.entity)
    
    def _execute_find(self, graph: KnowledgeGraph, operation: KnowledgeGraphOperation) -> List[KnowledgeEntity]:
        """Execute a find operation (semantic search)."""
        # Simple text-based search for now
        # In production, this would use proper semantic search
        query = operation.entity.lower()
        results = []
        
        for entity in graph.entities.values():
            # Search in entity name
            if query in entity.name.lower():
                results.append(entity)
                continue
            
            # Search in entity type
            if query in entity.entity_type.lower():
                results.append(entity)
                continue
            
            # Search in properties
            for value in entity.properties.values():
                if isinstance(value, str) and query in value.lower():
                    results.append(entity)
                    break
        
        return results
    
    def get_all_graphs(self) -> Dict[str, KnowledgeGraph]:
        """Get all knowledge graphs."""
        return self.graphs.copy()
    
    def delete_graph(self, name: str) -> bool:
        """Delete a knowledge graph."""
        if name == self.default_graph:
            raise ValueError("Cannot delete default graph")
        
        if name in self.graphs:
            del self.graphs[name]
            logger.debug(f"Deleted knowledge graph: {name}")
            return True
        
        return False 