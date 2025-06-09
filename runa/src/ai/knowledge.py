"""
Knowledge graph integration for the Runa programming language.

This module provides functionality for integrating with Neo4j knowledge graphs,
enabling knowledge-based queries and reasoning in Runa programs.
"""

import os
import json
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
import importlib.util

# Check if Neo4j is available
neo4j_available = importlib.util.find_spec("neo4j") is not None
if neo4j_available:
    from neo4j import GraphDatabase


class KnowledgeGraphError(Exception):
    """Exception raised when a knowledge graph operation fails."""
    pass


def check_neo4j_available():
    """Check if Neo4j is available, raise an error if not."""
    if not neo4j_available:
        raise KnowledgeGraphError(
            "Neo4j is not installed. Please install neo4j package to use "
            "knowledge graph features in Runa."
        )


class Neo4jConnection:
    """
    A connection to a Neo4j database.
    
    This class manages the connection to a Neo4j database and provides
    methods for executing queries and transactions.
    """
    
    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
        database: str = "neo4j"
    ):
        """
        Initialize a connection to a Neo4j database.
        
        Args:
            uri: The URI of the Neo4j database
            user: The username for authentication
            password: The password for authentication
            database: The name of the database to connect to
        
        Raises:
            KnowledgeGraphError: If Neo4j is not installed
        """
        check_neo4j_available()
        
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database
        self.driver = None
        
        try:
            self.driver = GraphDatabase.driver(
                uri,
                auth=(user, password)
            )
        except Exception as e:
            raise KnowledgeGraphError(f"Failed to connect to Neo4j: {str(e)}")
    
    def close(self):
        """Close the connection to the Neo4j database."""
        if self.driver:
            self.driver.close()
    
    def execute_query(
        self,
        query: str,
        parameters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query against the Neo4j database.
        
        Args:
            query: The Cypher query to execute
            parameters: Parameters for the query
        
        Returns:
            A list of dictionaries containing the query results
        
        Raises:
            KnowledgeGraphError: If the query fails
        """
        if parameters is None:
            parameters = {}
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            raise KnowledgeGraphError(f"Query execution failed: {str(e)}")
    
    def execute_write_transaction(
        self,
        tx_function: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute a write transaction against the Neo4j database.
        
        Args:
            tx_function: The transaction function to execute
            *args: Positional arguments for the transaction function
            **kwargs: Keyword arguments for the transaction function
        
        Returns:
            The result of the transaction
        
        Raises:
            KnowledgeGraphError: If the transaction fails
        """
        try:
            with self.driver.session(database=self.database) as session:
                return session.execute_write(tx_function, *args, **kwargs)
        except Exception as e:
            raise KnowledgeGraphError(f"Transaction execution failed: {str(e)}")


# Global connection object for Neo4j
_neo4j_connection = None


def connect_to_neo4j(
    uri: str,
    user: str,
    password: str,
    database: str = "neo4j"
) -> None:
    """
    Connect to a Neo4j database.
    
    Args:
        uri: The URI of the Neo4j database
        user: The username for authentication
        password: The password for authentication
        database: The name of the database to connect to
    
    Raises:
        KnowledgeGraphError: If the connection fails
    """
    global _neo4j_connection
    
    try:
        _neo4j_connection = Neo4jConnection(
            uri=uri,
            user=user,
            password=password,
            database=database
        )
    except Exception as e:
        raise KnowledgeGraphError(f"Failed to connect to Neo4j: {str(e)}")


def get_neo4j_connection() -> Neo4jConnection:
    """
    Get the current Neo4j connection.
    
    Returns:
        The current Neo4j connection
    
    Raises:
        KnowledgeGraphError: If no connection has been established
    """
    global _neo4j_connection
    
    if _neo4j_connection is None:
        raise KnowledgeGraphError(
            "No Neo4j connection has been established. "
            "Call connect_to_neo4j() first."
        )
    
    return _neo4j_connection


def execute_knowledge_query(
    query: str,
    parameters: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Execute a knowledge query against the Neo4j database.
    
    Args:
        query: The Cypher query to execute
        parameters: Parameters for the query
    
    Returns:
        A list of dictionaries containing the query results
    
    Raises:
        KnowledgeGraphError: If the query fails or no connection exists
    """
    connection = get_neo4j_connection()
    return connection.execute_query(query, parameters)


def create_knowledge_node(
    label: str,
    properties: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a node in the knowledge graph.
    
    Args:
        label: The label for the node
        properties: The properties for the node
    
    Returns:
        A dictionary containing the created node
    
    Raises:
        KnowledgeGraphError: If the operation fails or no connection exists
    """
    def create_node_tx(tx, label, properties):
        # Construct Cypher query
        property_keys = list(properties.keys())
        property_values = [properties[key] for key in property_keys]
        
        # Convert property keys to Cypher parameter placeholders
        property_placeholders = ", ".join([f"{key}: ${key}" for key in property_keys])
        
        # Build query
        query = f"CREATE (n:{label} {{{property_placeholders}}}) RETURN n"
        
        # Build parameters
        params = {key: value for key, value in zip(property_keys, property_values)}
        
        # Execute query
        result = tx.run(query, params)
        return result.single()["n"]
    
    connection = get_neo4j_connection()
    return connection.execute_write_transaction(create_node_tx, label, properties)


def create_knowledge_relationship(
    start_node_label: str,
    start_node_properties: Dict[str, Any],
    relationship_type: str,
    relationship_properties: Dict[str, Any],
    end_node_label: str,
    end_node_properties: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a relationship between two nodes in the knowledge graph.
    
    Args:
        start_node_label: The label for the start node
        start_node_properties: Properties to identify the start node
        relationship_type: The type of the relationship
        relationship_properties: Properties for the relationship
        end_node_label: The label for the end node
        end_node_properties: Properties to identify the end node
    
    Returns:
        A dictionary containing the created relationship
    
    Raises:
        KnowledgeGraphError: If the operation fails or no connection exists
    """
    def create_relationship_tx(tx, start_label, start_props, rel_type, rel_props, end_label, end_props):
        # Construct start node match clause
        start_props_str = " AND ".join([f"a.{key} = ${key}" for key in start_props.keys()])
        start_params = {key: value for key, value in start_props.items()}
        
        # Construct end node match clause
        end_props_str = " AND ".join([f"b.{key} = ${key}" for key in end_props.keys()])
        end_params = {f"end_{key}": value for key, value in end_props.items()}
        end_props_str = end_props_str.replace("$", "$end_")
        
        # Construct relationship properties
        rel_props_str = ", ".join([f"{key}: ${key}" for key in rel_props.keys()])
        rel_params = {f"rel_{key}": value for key, value in rel_props.items()}
        rel_props_str = rel_props_str.replace("$", "$rel_")
        
        # Build query
        query = f"""
        MATCH (a:{start_label})
        WHERE {start_props_str}
        MATCH (b:{end_label})
        WHERE {end_props_str}
        CREATE (a)-[r:{rel_type} {{{rel_props_str}}}]->(b)
        RETURN r
        """
        
        # Combine parameters
        params = {**start_params, **end_params, **rel_params}
        
        # Execute query
        result = tx.run(query, params)
        return result.single()["r"]
    
    connection = get_neo4j_connection()
    return connection.execute_write_transaction(
        create_relationship_tx,
        start_node_label,
        start_node_properties,
        relationship_type,
        relationship_properties,
        end_node_label,
        end_node_properties
    ) 