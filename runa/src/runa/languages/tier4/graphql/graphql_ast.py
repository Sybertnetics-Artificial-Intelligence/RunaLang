#!/usr/bin/env python3
"""
GraphQL AST Node Definitions

Comprehensive Abstract Syntax Tree nodes for GraphQL language covering all GraphQL features
including schema definitions, type systems, queries, mutations, subscriptions, and directives.

This module provides complete AST representation for:
- Schema definitions and type systems
- Object, interface, union, enum, and input types
- Queries, mutations, and subscriptions
- Field definitions with arguments and directives
- Scalar types and custom scalars
- Fragments and inline fragments
- Variables and input values
- Introspection system
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata


class GraphQLNodeType(Enum):
    """GraphQL-specific AST node types."""
    # Document structure
    DOCUMENT = auto()
    
    # Definitions
    SCHEMA_DEFINITION = auto()
    TYPE_DEFINITION = auto()
    SCALAR_TYPE_DEFINITION = auto()
    OBJECT_TYPE_DEFINITION = auto()
    INTERFACE_TYPE_DEFINITION = auto()
    UNION_TYPE_DEFINITION = auto()
    ENUM_TYPE_DEFINITION = auto()
    INPUT_OBJECT_TYPE_DEFINITION = auto()
    DIRECTIVE_DEFINITION = auto()
    
    # Type extensions
    SCHEMA_EXTENSION = auto()
    TYPE_EXTENSION = auto()
    SCALAR_TYPE_EXTENSION = auto()
    OBJECT_TYPE_EXTENSION = auto()
    INTERFACE_TYPE_EXTENSION = auto()
    UNION_TYPE_EXTENSION = auto()
    ENUM_TYPE_EXTENSION = auto()
    INPUT_OBJECT_TYPE_EXTENSION = auto()
    
    # Operations
    OPERATION_DEFINITION = auto()
    FRAGMENT_DEFINITION = auto()
    
    # Fields and selections
    FIELD = auto()
    INLINE_FRAGMENT = auto()
    FRAGMENT_SPREAD = auto()
    SELECTION_SET = auto()
    
    # Types
    NAMED_TYPE = auto()
    LIST_TYPE = auto()
    NON_NULL_TYPE = auto()
    
    # Arguments and variables
    ARGUMENT = auto()
    VARIABLE_DEFINITION = auto()
    VARIABLE = auto()
    
    # Values
    INT_VALUE = auto()
    FLOAT_VALUE = auto()
    STRING_VALUE = auto()
    BOOLEAN_VALUE = auto()
    NULL_VALUE = auto()
    ENUM_VALUE = auto()
    LIST_VALUE = auto()
    OBJECT_VALUE = auto()
    OBJECT_FIELD = auto()
    
    # Field and input definitions
    FIELD_DEFINITION = auto()
    INPUT_VALUE_DEFINITION = auto()
    ENUM_VALUE_DEFINITION = auto()
    
    # Directives
    DIRECTIVE = auto()
    
    # Names and descriptions
    NAME = auto()
    DESCRIPTION = auto()


class GraphQLOperationType(Enum):
    """GraphQL operation types."""
    QUERY = "query"
    MUTATION = "mutation"
    SUBSCRIPTION = "subscription"


class GraphQLDirectiveLocation(Enum):
    """GraphQL directive locations."""
    # Executable directive locations
    QUERY = "QUERY"
    MUTATION = "MUTATION"
    SUBSCRIPTION = "SUBSCRIPTION"
    FIELD = "FIELD"
    FRAGMENT_DEFINITION = "FRAGMENT_DEFINITION"
    FRAGMENT_SPREAD = "FRAGMENT_SPREAD"
    INLINE_FRAGMENT = "INLINE_FRAGMENT"
    VARIABLE_DEFINITION = "VARIABLE_DEFINITION"
    
    # Type system directive locations
    SCHEMA = "SCHEMA"
    SCALAR = "SCALAR"
    OBJECT = "OBJECT"
    FIELD_DEFINITION = "FIELD_DEFINITION"
    ARGUMENT_DEFINITION = "ARGUMENT_DEFINITION"
    INTERFACE = "INTERFACE"
    UNION = "UNION"
    ENUM = "ENUM"
    ENUM_VALUE = "ENUM_VALUE"
    INPUT_OBJECT = "INPUT_OBJECT"
    INPUT_FIELD_DEFINITION = "INPUT_FIELD_DEFINITION"


@dataclass
class GraphQLNode(ASTNode):
    """Base class for all GraphQL AST nodes."""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.DOCUMENT
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for AST traversal."""
        pass


# ============================================================================
# Document and Top-Level Definitions
# ============================================================================

@dataclass
class GraphQLDocument(GraphQLNode):
    """GraphQL document containing definitions"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.DOCUMENT
    definitions: List['GraphQLDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_document(self)


@dataclass
class GraphQLDefinition(GraphQLNode):
    """Base class for top-level definitions"""
    pass


# ============================================================================
# Schema Definition
# ============================================================================

@dataclass
class GraphQLSchemaDefinition(GraphQLDefinition):
    """Schema definition: schema { query: Query mutation: Mutation }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.SCHEMA_DEFINITION
    description: Optional[str] = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    operation_types: List['GraphQLOperationTypeDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_schema_definition(self)


@dataclass
class GraphQLOperationTypeDefinition(GraphQLNode):
    """Operation type definition: query: Query"""
    operation: GraphQLOperationType = GraphQLOperationType.QUERY
    type: 'GraphQLNamedType' = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_operation_type_definition(self)


# ============================================================================
# Type Definitions
# ============================================================================

@dataclass
class GraphQLTypeDefinition(GraphQLDefinition):
    """Base class for type definitions"""
    name: str = ""
    description: Optional[str] = None
    directives: List['GraphQLDirective'] = field(default_factory=list)


@dataclass
class GraphQLScalarTypeDefinition(GraphQLTypeDefinition):
    """Scalar type definition: scalar DateTime"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.SCALAR_TYPE_DEFINITION
    
    def accept(self, visitor):
        return visitor.visit_graphql_scalar_type_definition(self)


@dataclass
class GraphQLObjectTypeDefinition(GraphQLTypeDefinition):
    """Object type definition: type User implements Node { id: ID! }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.OBJECT_TYPE_DEFINITION
    interfaces: List['GraphQLNamedType'] = field(default_factory=list)
    fields: List['GraphQLFieldDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_object_type_definition(self)


@dataclass
class GraphQLInterfaceTypeDefinition(GraphQLTypeDefinition):
    """Interface type definition: interface Node { id: ID! }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.INTERFACE_TYPE_DEFINITION
    interfaces: List['GraphQLNamedType'] = field(default_factory=list)
    fields: List['GraphQLFieldDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_interface_type_definition(self)


@dataclass
class GraphQLUnionTypeDefinition(GraphQLTypeDefinition):
    """Union type definition: union SearchResult = User | Post"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.UNION_TYPE_DEFINITION
    types: List['GraphQLNamedType'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_union_type_definition(self)


@dataclass
class GraphQLEnumTypeDefinition(GraphQLTypeDefinition):
    """Enum type definition: enum Color { RED GREEN BLUE }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.ENUM_TYPE_DEFINITION
    values: List['GraphQLEnumValueDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_enum_type_definition(self)


@dataclass
class GraphQLInputObjectTypeDefinition(GraphQLTypeDefinition):
    """Input object type definition: input UserInput { name: String! }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.INPUT_OBJECT_TYPE_DEFINITION
    fields: List['GraphQLInputValueDefinition'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_input_object_type_definition(self)


@dataclass
class GraphQLDirectiveDefinition(GraphQLDefinition):
    """Directive definition: directive @auth(role: String!) on FIELD_DEFINITION"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.DIRECTIVE_DEFINITION
    name: str = ""
    description: Optional[str] = None
    arguments: List['GraphQLInputValueDefinition'] = field(default_factory=list)
    repeatable: bool = False
    locations: List[GraphQLDirectiveLocation] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_directive_definition(self)


# ============================================================================
# Field and Input Definitions
# ============================================================================

@dataclass
class GraphQLFieldDefinition(GraphQLNode):
    """Field definition: name(arg: Type): Type @directive"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.FIELD_DEFINITION
    name: str = ""
    description: Optional[str] = None
    arguments: List['GraphQLInputValueDefinition'] = field(default_factory=list)
    type: 'GraphQLType' = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_field_definition(self)


@dataclass
class GraphQLInputValueDefinition(GraphQLNode):
    """Input value definition: name: Type = defaultValue @directive"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.INPUT_VALUE_DEFINITION
    name: str = ""
    description: Optional[str] = None
    type: 'GraphQLType' = None
    default_value: Optional['GraphQLValue'] = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_input_value_definition(self)


@dataclass
class GraphQLEnumValueDefinition(GraphQLNode):
    """Enum value definition: RED @deprecated(reason: "Use CRIMSON")"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.ENUM_VALUE_DEFINITION
    name: str = ""
    description: Optional[str] = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_enum_value_definition(self)


# ============================================================================
# Operations
# ============================================================================

@dataclass
class GraphQLOperationDefinition(GraphQLDefinition):
    """Operation definition: query GetUser($id: ID!) { user(id: $id) { name } }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.OPERATION_DEFINITION
    operation: GraphQLOperationType = GraphQLOperationType.QUERY
    name: Optional[str] = None
    variable_definitions: List['GraphQLVariableDefinition'] = field(default_factory=list)
    directives: List['GraphQLDirective'] = field(default_factory=list)
    selection_set: 'GraphQLSelectionSet' = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_operation_definition(self)


@dataclass
class GraphQLFragmentDefinition(GraphQLDefinition):
    """Fragment definition: fragment UserInfo on User { name email }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.FRAGMENT_DEFINITION
    name: str = ""
    type_condition: 'GraphQLNamedType' = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    selection_set: 'GraphQLSelectionSet' = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_fragment_definition(self)


@dataclass
class GraphQLVariableDefinition(GraphQLNode):
    """Variable definition: $id: ID! = "default" @directive"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.VARIABLE_DEFINITION
    variable: 'GraphQLVariable' = None
    type: 'GraphQLType' = None
    default_value: Optional['GraphQLValue'] = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_variable_definition(self)


# ============================================================================
# Selections
# ============================================================================

@dataclass
class GraphQLSelectionSet(GraphQLNode):
    """Selection set: { field1 field2 }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.SELECTION_SET
    selections: List['GraphQLSelection'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_selection_set(self)


@dataclass
class GraphQLSelection(GraphQLNode):
    """Base class for selections"""
    pass


@dataclass
class GraphQLField(GraphQLSelection):
    """Field selection: name(arg: value) { subfield }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.FIELD
    alias: Optional[str] = None
    name: str = ""
    arguments: List['GraphQLArgument'] = field(default_factory=list)
    directives: List['GraphQLDirective'] = field(default_factory=list)
    selection_set: Optional['GraphQLSelectionSet'] = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_field(self)


@dataclass
class GraphQLInlineFragment(GraphQLSelection):
    """Inline fragment: ... on Type @directive { field }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.INLINE_FRAGMENT
    type_condition: Optional['GraphQLNamedType'] = None
    directives: List['GraphQLDirective'] = field(default_factory=list)
    selection_set: 'GraphQLSelectionSet' = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_inline_fragment(self)


@dataclass
class GraphQLFragmentSpread(GraphQLSelection):
    """Fragment spread: ...fragmentName @directive"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.FRAGMENT_SPREAD
    name: str = ""
    directives: List['GraphQLDirective'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_fragment_spread(self)


# ============================================================================
# Arguments and Variables
# ============================================================================

@dataclass
class GraphQLArgument(GraphQLNode):
    """Argument: name: value"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.ARGUMENT
    name: str = ""
    value: 'GraphQLValue' = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_argument(self)


@dataclass
class GraphQLVariable(GraphQLNode):
    """Variable: $variableName"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.VARIABLE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_graphql_variable(self)


# ============================================================================
# Types
# ============================================================================

@dataclass
class GraphQLType(GraphQLNode):
    """Base class for GraphQL types"""
    pass


@dataclass
class GraphQLNamedType(GraphQLType):
    """Named type: String, User, etc."""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.NAMED_TYPE
    name: str = ""
    
    def accept(self, visitor):
        return visitor.visit_graphql_named_type(self)


@dataclass
class GraphQLListType(GraphQLType):
    """List type: [String]"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.LIST_TYPE
    type: GraphQLType = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_list_type(self)


@dataclass
class GraphQLNonNullType(GraphQLType):
    """Non-null type: String!"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.NON_NULL_TYPE
    type: GraphQLType = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_non_null_type(self)


# ============================================================================
# Values
# ============================================================================

@dataclass
class GraphQLValue(GraphQLNode):
    """Base class for GraphQL values"""
    pass


@dataclass
class GraphQLIntValue(GraphQLValue):
    """Integer value: 42"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.INT_VALUE
    value: int = 0
    
    def accept(self, visitor):
        return visitor.visit_graphql_int_value(self)


@dataclass
class GraphQLFloatValue(GraphQLValue):
    """Float value: 3.14"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.FLOAT_VALUE
    value: float = 0.0
    
    def accept(self, visitor):
        return visitor.visit_graphql_float_value(self)


@dataclass
class GraphQLStringValue(GraphQLValue):
    """String value: "hello" or '''block string'''"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.STRING_VALUE
    value: str = ""
    block: bool = False  # True for block strings (""")
    
    def accept(self, visitor):
        return visitor.visit_graphql_string_value(self)


@dataclass
class GraphQLBooleanValue(GraphQLValue):
    """Boolean value: true or false"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.BOOLEAN_VALUE
    value: bool = False
    
    def accept(self, visitor):
        return visitor.visit_graphql_boolean_value(self)


@dataclass
class GraphQLNullValue(GraphQLValue):
    """Null value: null"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.NULL_VALUE
    
    def accept(self, visitor):
        return visitor.visit_graphql_null_value(self)


@dataclass
class GraphQLEnumValue(GraphQLValue):
    """Enum value: RED, ACTIVE, etc."""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.ENUM_VALUE
    value: str = ""
    
    def accept(self, visitor):
        return visitor.visit_graphql_enum_value(self)


@dataclass
class GraphQLListValue(GraphQLValue):
    """List value: [1, 2, 3]"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.LIST_VALUE
    values: List[GraphQLValue] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_list_value(self)


@dataclass
class GraphQLObjectValue(GraphQLValue):
    """Object value: { name: "John", age: 30 }"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.OBJECT_VALUE
    fields: List['GraphQLObjectField'] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_object_value(self)


@dataclass
class GraphQLObjectField(GraphQLNode):
    """Object field: name: value"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.OBJECT_FIELD
    name: str = ""
    value: GraphQLValue = None
    
    def accept(self, visitor):
        return visitor.visit_graphql_object_field(self)


# ============================================================================
# Directives
# ============================================================================

@dataclass
class GraphQLDirective(GraphQLNode):
    """Directive: @include(if: true)"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.DIRECTIVE
    name: str = ""
    arguments: List[GraphQLArgument] = field(default_factory=list)
    
    def accept(self, visitor):
        return visitor.visit_graphql_directive(self)


# ============================================================================
# Names and Descriptions
# ============================================================================

@dataclass
class GraphQLName(GraphQLNode):
    """GraphQL name identifier"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.NAME
    value: str = ""
    
    def accept(self, visitor):
        return visitor.visit_graphql_name(self)


@dataclass
class GraphQLDescription(GraphQLNode):
    """GraphQL description (string literal used as description)"""
    graphql_node_type: GraphQLNodeType = GraphQLNodeType.DESCRIPTION
    value: str = ""
    block: bool = False
    
    def accept(self, visitor):
        return visitor.visit_graphql_description(self)


# ============================================================================
# Utility Functions
# ============================================================================

def create_graphql_named_type(name: str) -> GraphQLNamedType:
    """Create a GraphQL named type node."""
    return GraphQLNamedType(name=name)


def create_graphql_list_type(item_type: GraphQLType) -> GraphQLListType:
    """Create a GraphQL list type node."""
    return GraphQLListType(type=item_type)


def create_graphql_non_null_type(type_: GraphQLType) -> GraphQLNonNullType:
    """Create a GraphQL non-null type node."""
    return GraphQLNonNullType(type=type_)


def create_graphql_field(name: str, type_: GraphQLType, args: List[GraphQLInputValueDefinition] = None) -> GraphQLFieldDefinition:
    """Create a GraphQL field definition node."""
    return GraphQLFieldDefinition(
        name=name,
        type=type_,
        arguments=args or []
    )


def create_graphql_argument(name: str, value: GraphQLValue) -> GraphQLArgument:
    """Create a GraphQL argument node."""
    return GraphQLArgument(name=name, value=value)


def create_graphql_variable(name: str) -> GraphQLVariable:
    """Create a GraphQL variable node."""
    return GraphQLVariable(name=name)


def create_graphql_string_value(value: str, block: bool = False) -> GraphQLStringValue:
    """Create a GraphQL string value node."""
    return GraphQLStringValue(value=value, block=block)


def create_graphql_int_value(value: int) -> GraphQLIntValue:
    """Create a GraphQL integer value node."""
    return GraphQLIntValue(value=value)


def create_graphql_boolean_value(value: bool) -> GraphQLBooleanValue:
    """Create a GraphQL boolean value node."""
    return GraphQLBooleanValue(value=value)


def create_graphql_object_type(name: str, fields: List[GraphQLFieldDefinition] = None, interfaces: List[GraphQLNamedType] = None) -> GraphQLObjectTypeDefinition:
    """Create a GraphQL object type definition node."""
    return GraphQLObjectTypeDefinition(
        name=name,
        fields=fields or [],
        interfaces=interfaces or []
    )


def create_graphql_operation(operation_type: GraphQLOperationType, selection_set: GraphQLSelectionSet, name: str = None) -> GraphQLOperationDefinition:
    """Create a GraphQL operation definition node."""
    return GraphQLOperationDefinition(
        operation=operation_type,
        name=name,
        selection_set=selection_set
    )


def create_graphql_selection_set(selections: List[GraphQLSelection]) -> GraphQLSelectionSet:
    """Create a GraphQL selection set node."""
    return GraphQLSelectionSet(selections=selections)


def create_graphql_field_selection(name: str, alias: str = None, args: List[GraphQLArgument] = None, selection_set: GraphQLSelectionSet = None) -> GraphQLField:
    """Create a GraphQL field selection node."""
    return GraphQLField(
        name=name,
        alias=alias,
        arguments=args or [],
        selection_set=selection_set
    ) 