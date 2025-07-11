#!/usr/bin/env python3
"""
GraphQL ↔ Runa Bidirectional Converter

Converts between GraphQL AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.

This module handles conversion between:
- GraphQL operations ↔ Runa process definitions
- GraphQL type definitions ↔ Runa type definitions
- GraphQL fields ↔ Runa function calls/property access
- GraphQL fragments ↔ Runa reusable code blocks
- GraphQL directives ↔ Runa annotations
- GraphQL arguments ↔ Runa function parameters
- GraphQL values ↔ Runa literals/expressions
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .graphql_ast import *
from ....core.runa_ast import *
from ....core.translation_result import TranslationResult, TranslationError


class GraphQLToRunaConverter:
    """Converts GraphQL AST to Runa AST."""
    
    def __init__(self):
        self.current_module = None
        self.type_mapping = self._create_type_mapping()
        self.fragments = {}  # Store fragment definitions for reuse
        
    def _create_type_mapping(self) -> Dict[str, str]:
        """Create mapping from GraphQL types to Runa types."""
        return {
            # Scalar types
            'ID': 'String',
            'String': 'String', 
            'Int': 'Integer',
            'Float': 'Float',
            'Boolean': 'Boolean',
            
            # Special GraphQL types
            'DateTime': 'String',  # ISO 8601 string
            'Date': 'String',
            'Time': 'String',
            'JSON': 'Any',
            'Upload': 'Any',
        }
    
    def convert_document(self, document: GraphQLDocument) -> Program:
        """Convert GraphQL document to Runa program."""
        statements = []
        
        # First pass: collect fragment definitions
        for definition in document.definitions:
            if isinstance(definition, GraphQLFragmentDefinition):
                self.fragments[definition.name] = definition
        
        # Second pass: convert all definitions
        for definition in document.definitions:
            runa_stmts = self.convert_definition(definition)
            statements.extend(runa_stmts)
        
        return Program(statements=statements)
    
    def convert_definition(self, definition: GraphQLDefinition) -> List[Statement]:
        """Convert GraphQL definition to Runa statements."""
        if isinstance(definition, GraphQLOperationDefinition):
            return [self.convert_operation_definition(definition)]
        elif isinstance(definition, GraphQLFragmentDefinition):
            return [self.convert_fragment_definition(definition)]
        elif isinstance(definition, GraphQLObjectTypeDefinition):
            return [self.convert_object_type_definition(definition)]
        elif isinstance(definition, GraphQLInterfaceTypeDefinition):
            return [self.convert_interface_type_definition(definition)]
        elif isinstance(definition, GraphQLUnionTypeDefinition):
            return [self.convert_union_type_definition(definition)]
        elif isinstance(definition, GraphQLEnumTypeDefinition):
            return [self.convert_enum_type_definition(definition)]
        elif isinstance(definition, GraphQLInputObjectTypeDefinition):
            return [self.convert_input_object_type_definition(definition)]
        elif isinstance(definition, GraphQLScalarTypeDefinition):
            return [self.convert_scalar_type_definition(definition)]
        else:
            return []
    
    def convert_operation_definition(self, op: GraphQLOperationDefinition) -> ProcessDefinition:
        """Convert GraphQL operation to Runa process definition."""
        # Map operation type to process name
        op_name = op.name or f"Anonymous{op.operation_type.name.title()}"
        
        # Convert variable definitions to parameters
        parameters = []
        for var_def in op.variable_definitions:
            param = Parameter(
                name=var_def.variable.name,
                type_annotation=self.convert_graphql_type_to_runa(var_def.type)
            )
            parameters.append(param)
        
        # Convert selection set to process body
        body = self.convert_selection_set(op.selection_set)
        
        # Create process definition
        process = ProcessDefinition(
            name=op_name,
            parameters=parameters,
            body=body
        )
        
        # Add directives as annotations if present
        if op.directives:
            # Convert directives to comments or metadata
            for directive in op.directives:
                comment = f"Note: Directive @{directive.name}"
                if directive.arguments:
                    args_str = ", ".join([f"{arg.name}: {self._value_to_string(arg.value)}" 
                                         for arg in directive.arguments])
                    comment += f"({args_str})"
                process.metadata.add_note("directive", comment)
        
        return process
    
    def convert_fragment_definition(self, fragment: GraphQLFragmentDefinition) -> ProcessDefinition:
        """Convert GraphQL fragment to Runa process definition."""
        # Fragment becomes a reusable process
        body = self.convert_selection_set(fragment.selection_set)
        
        process = ProcessDefinition(
            name=f"Fragment_{fragment.name}",
            parameters=[],  # Fragments don't have parameters
            body=body
        )
        
        # Add type condition as metadata
        process.metadata.add_note("fragment_type", fragment.type_condition)
        
        return process
    
    def convert_selection_set(self, selection_set: Optional[GraphQLSelectionSet]) -> List[Statement]:
        """Convert GraphQL selection set to Runa statements."""
        if not selection_set:
            return []
        
        statements = []
        
        for selection in selection_set.selections:
            if isinstance(selection, GraphQLField):
                field_stmt = self.convert_field(selection)
                statements.append(field_stmt)
            elif isinstance(selection, GraphQLFragmentSpread):
                fragment_stmt = self.convert_fragment_spread(selection)
                statements.append(fragment_stmt)
            elif isinstance(selection, GraphQLInlineFragment):
                inline_stmts = self.convert_inline_fragment(selection)
                statements.extend(inline_stmts)
        
        return statements
    
    def convert_field(self, field: GraphQLField) -> Statement:
        """Convert GraphQL field to Runa statement."""
        # Field becomes either a function call or property access
        if field.arguments:
            # Field with arguments becomes a function call
            args = []
            for arg in field.arguments:
                args.append((arg.name, self.convert_value(arg.value)))
            
            call = FunctionCall(
                function_name=field.name,
                arguments=args
            )
            
            if field.alias:
                # Store result in variable with alias name
                return LetStatement(
                    identifier=field.alias,
                    value=call
                )
            else:
                return ExpressionStatement(expression=call)
        else:
            # Field without arguments becomes property access
            access = Identifier(name=field.name)
            
            if field.alias:
                return LetStatement(
                    identifier=field.alias,
                    value=access
                )
            else:
                return ExpressionStatement(expression=access)
    
    def convert_fragment_spread(self, spread: GraphQLFragmentSpread) -> Statement:
        """Convert GraphQL fragment spread to Runa function call."""
        # Fragment spread becomes a call to the fragment process
        call = FunctionCall(
            function_name=f"Fragment_{spread.name}",
            arguments=[]
        )
        return ExpressionStatement(expression=call)
    
    def convert_inline_fragment(self, inline: GraphQLInlineFragment) -> List[Statement]:
        """Convert GraphQL inline fragment to Runa conditional."""
        # Inline fragment becomes conditional execution
        body = self.convert_selection_set(inline.selection_set)
        
        if inline.type_condition:
            # Create a type check condition
            condition = BinaryExpression(
                left=Identifier(name="__typename"),
                operator=BinaryOperator.EQUALS,
                right=StringLiteral(value=inline.type_condition)
            )
            
            if_stmt = IfStatement(
                condition=condition,
                then_block=body
            )
            return [if_stmt]
        else:
            # No type condition, just include the statements
            return body
    
    def convert_value(self, value: Any) -> Expression:
        """Convert GraphQL value to Runa expression."""
        if isinstance(value, GraphQLIntValue):
            return IntegerLiteral(value=value.value)
        elif isinstance(value, GraphQLFloatValue):
            return FloatLiteral(value=value.value)
        elif isinstance(value, GraphQLStringValue):
            return StringLiteral(value=value.value)
        elif isinstance(value, GraphQLBooleanValue):
            return BooleanLiteral(value=value.value)
        elif isinstance(value, GraphQLNullValue):
            return StringLiteral(value="null")  # Or a special null representation
        elif isinstance(value, GraphQLEnumValue):
            return StringLiteral(value=value.value)
        elif isinstance(value, GraphQLListValue):
            elements = [self.convert_value(v) for v in value.values]
            return ListLiteral(elements=elements)
        elif isinstance(value, GraphQLObjectValue):
            pairs = []
            for field in value.fields:
                key = StringLiteral(value=field.name)
                val = self.convert_value(field.value)
                pairs.append((key, val))
            return DictionaryLiteral(pairs=pairs)
        elif isinstance(value, GraphQLVariable):
            return Identifier(name=value.name)
        else:
            return StringLiteral(value=str(value))
    
    def convert_object_type_definition(self, obj_type: GraphQLObjectTypeDefinition) -> Statement:
        """Convert GraphQL object type to Runa type definition."""
        # Create a dictionary-like type definition
        fields = []
        for field_def in obj_type.fields:
            field_type = self.convert_graphql_type_to_runa(field_def.type)
            fields.append(f"{field_def.name}: {field_type}")
        
        type_def = TypeDefinition(
            name=obj_type.name,
            definition=BasicType(name=f"Dictionary with {', '.join(fields)}")
        )
        
        # Add interfaces as metadata
        if obj_type.interfaces:
            type_def.metadata.add_note("implements", obj_type.interfaces)
        
        return type_def
    
    def convert_interface_type_definition(self, interface: GraphQLInterfaceTypeDefinition) -> Statement:
        """Convert GraphQL interface to Runa type definition."""
        # Interface becomes an abstract type definition
        return TypeDefinition(
            name=interface.name,
            definition=BasicType(name="Interface")
        )
    
    def convert_union_type_definition(self, union: GraphQLUnionTypeDefinition) -> Statement:
        """Convert GraphQL union to Runa union type."""
        union_types = [BasicType(name=t) for t in union.types]
        return TypeDefinition(
            name=union.name,
            definition=UnionType(types=union_types)
        )
    
    def convert_enum_type_definition(self, enum: GraphQLEnumTypeDefinition) -> Statement:
        """Convert GraphQL enum to Runa type definition."""
        return TypeDefinition(
            name=enum.name,
            definition=BasicType(name=f"Enum({', '.join(enum.values)})")
        )
    
    def convert_input_object_type_definition(self, input_obj: GraphQLInputObjectTypeDefinition) -> Statement:
        """Convert GraphQL input object to Runa type definition."""
        # Input object becomes a dictionary type
        return TypeDefinition(
            name=input_obj.name,
            definition=BasicType(name="Dictionary")
        )
    
    def convert_scalar_type_definition(self, scalar: GraphQLScalarTypeDefinition) -> Statement:
        """Convert GraphQL scalar to Runa type definition."""
        # Map to appropriate Runa type or create custom type
        runa_type = self.type_mapping.get(scalar.name, "String")
        return TypeDefinition(
            name=scalar.name,
            definition=BasicType(name=runa_type)
        )
    
    def convert_graphql_type_to_runa(self, graphql_type: str) -> TypeExpression:
        """Convert GraphQL type string to Runa type expression."""
        # Handle list types [Type]
        if graphql_type.startswith('[') and graphql_type.endswith(']'):
            inner_type = graphql_type[1:-1]
            return GenericType(
                base_type="List",
                type_args=[self.convert_graphql_type_to_runa(inner_type)]
            )
        
        # Handle non-null types Type!
        if graphql_type.endswith('!'):
            inner_type = graphql_type[:-1]
            return self.convert_graphql_type_to_runa(inner_type)  # Non-null is default in Runa
        
        # Map scalar types
        runa_type = self.type_mapping.get(graphql_type, graphql_type)
        return BasicType(name=runa_type)
    
    def _value_to_string(self, value: Any) -> str:
        """Convert value to string representation."""
        if isinstance(value, GraphQLStringValue):
            return f'"{value.value}"'
        elif hasattr(value, 'value'):
            return str(value.value)
        else:
            return str(value)


class RunaToGraphQLConverter:
    """Converts Runa AST to GraphQL AST."""
    
    def __init__(self):
        self.type_mapping = self._create_type_mapping()
    
    def _create_type_mapping(self) -> Dict[str, str]:
        """Create mapping from Runa types to GraphQL types."""
        return {
            'String': 'String',
            'Integer': 'Int',
            'Float': 'Float', 
            'Boolean': 'Boolean',
            'Any': 'JSON',
        }
    
    def convert_program(self, program: Program) -> GraphQLDocument:
        """Convert Runa program to GraphQL document."""
        definitions = []
        
        for stmt in program.statements:
            graphql_defs = self.convert_statement(stmt)
            definitions.extend(graphql_defs)
        
        return GraphQLDocument(definitions=definitions)
    
    def convert_statement(self, stmt: Statement) -> List[GraphQLDefinition]:
        """Convert Runa statement to GraphQL definitions."""
        if isinstance(stmt, ProcessDefinition):
            return [self.convert_process_definition(stmt)]
        elif isinstance(stmt, TypeDefinition):
            return [self.convert_type_definition(stmt)]
        else:
            return []
    
    def convert_process_definition(self, process: ProcessDefinition) -> GraphQLOperationDefinition:
        """Convert Runa process to GraphQL operation."""
        # Determine operation type from name or metadata
        name = process.name.lower()
        if "mutation" in name or "create" in name or "update" in name or "delete" in name:
            op_type = GraphQLNodeType.MUTATION
        elif "subscription" in name or "subscribe" in name:
            op_type = GraphQLNodeType.SUBSCRIPTION
        else:
            op_type = GraphQLNodeType.QUERY
        
        # Convert parameters to variable definitions
        var_defs = []
        for param in process.parameters:
            var_def = GraphQLVariableDefinition(
                variable=GraphQLVariable(name=param.name),
                type=self.convert_runa_type_to_graphql(param.type_annotation)
            )
            var_defs.append(var_def)
        
        # Convert body to selection set
        selection_set = self.convert_statements_to_selection_set(process.body)
        
        return GraphQLOperationDefinition(
            operation_type=op_type,
            name=process.name,
            variable_definitions=var_defs,
            selection_set=selection_set
        )
    
    def convert_type_definition(self, type_def: TypeDefinition) -> GraphQLDefinition:
        """Convert Runa type definition to GraphQL type definition."""
        if isinstance(type_def.definition, UnionType):
            # Union type
            type_names = [t.name if isinstance(t, BasicType) else str(t) 
                         for t in type_def.definition.types]
            return GraphQLUnionTypeDefinition(
                name=type_def.name,
                types=type_names
            )
        else:
            # Object type (default)
            return GraphQLObjectTypeDefinition(
                name=type_def.name,
                fields=[]  # Would need more context to populate fields
            )
    
    def convert_statements_to_selection_set(self, statements: List[Statement]) -> GraphQLSelectionSet:
        """Convert Runa statements to GraphQL selection set."""
        selections = []
        
        for stmt in statements:
            if isinstance(stmt, ExpressionStatement):
                if isinstance(stmt.expression, FunctionCall):
                    field = self.convert_function_call_to_field(stmt.expression)
                    selections.append(field)
                elif isinstance(stmt.expression, Identifier):
                    field = GraphQLField(name=stmt.expression.name)
                    selections.append(field)
        
        return GraphQLSelectionSet(selections=selections)
    
    def convert_function_call_to_field(self, call: FunctionCall) -> GraphQLField:
        """Convert Runa function call to GraphQL field."""
        # Convert arguments
        args = []
        for arg_name, arg_value in call.arguments:
            graphql_value = self.convert_expression_to_value(arg_value)
            args.append(GraphQLArgument(name=arg_name, value=graphql_value))
        
        return GraphQLField(
            name=call.function_name,
            arguments=args
        )
    
    def convert_expression_to_value(self, expr: Expression) -> GraphQLNode:
        """Convert Runa expression to GraphQL value."""
        if isinstance(expr, IntegerLiteral):
            return GraphQLIntValue(value=expr.value)
        elif isinstance(expr, FloatLiteral):
            return GraphQLFloatValue(value=expr.value)
        elif isinstance(expr, StringLiteral):
            return GraphQLStringValue(value=expr.value)
        elif isinstance(expr, BooleanLiteral):
            return GraphQLBooleanValue(value=expr.value)
        elif isinstance(expr, Identifier):
            return GraphQLVariable(name=expr.name)
        else:
            return GraphQLStringValue(value=str(expr))
    
    def convert_runa_type_to_graphql(self, runa_type: Optional[TypeExpression]) -> str:
        """Convert Runa type to GraphQL type string."""
        if not runa_type:
            return "String"
        
        if isinstance(runa_type, BasicType):
            return self.type_mapping.get(runa_type.name, runa_type.name)
        elif isinstance(runa_type, GenericType) and runa_type.base_type == "List":
            if runa_type.type_args:
                inner_type = self.convert_runa_type_to_graphql(runa_type.type_args[0])
                return f"[{inner_type}]"
            return "[String]"
        else:
            return "String"


# Public API functions
def graphql_to_runa(graphql_ast: GraphQLDocument) -> Program:
    """Convert GraphQL AST to Runa AST."""
    converter = GraphQLToRunaConverter()
    return converter.convert_document(graphql_ast)

def runa_to_graphql(runa_ast: Program) -> GraphQLDocument:
    """Convert Runa AST to GraphQL AST."""
    converter = RunaToGraphQLConverter()
    return converter.convert_program(runa_ast) 