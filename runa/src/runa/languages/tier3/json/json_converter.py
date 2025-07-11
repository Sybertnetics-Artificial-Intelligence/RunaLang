#!/usr/bin/env python3
"""
JSON ↔ Runa Bidirectional Converter

Converts between JSON AST and Runa AST in both directions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from .json_ast import *
from ....core.runa_ast import *


class JsonToRunaConverter:
    """Converts JSON AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, json_node: JsonNode) -> ASTNode:
        """Convert JSON AST node to Runa AST node."""
        try:
            if isinstance(json_node, JsonDocument):
                return self._convert_document(json_node)
            elif isinstance(json_node, JsonObject):
                return self._convert_object(json_node)
            elif isinstance(json_node, JsonArray):
                return self._convert_array(json_node)
            elif isinstance(json_node, JsonProperty):
                return self._convert_property(json_node)
            elif isinstance(json_node, JsonString):
                return self._convert_string(json_node)
            elif isinstance(json_node, JsonNumber):
                return self._convert_number(json_node)
            elif isinstance(json_node, JsonBoolean):
                return self._convert_boolean(json_node)
            elif isinstance(json_node, JsonNull):
                return self._convert_null(json_node)
            else:
                return self._create_placeholder(json_node)
        except Exception as e:
            self.logger.error(f"JSON to Runa conversion failed: {e}")
            return self._create_placeholder(json_node)
    
    def _convert_document(self, document: JsonDocument) -> Program:
        """Convert JSON document to Runa program."""
        # Create a program that demonstrates the JSON structure
        statements = []
        
        # Create a variable declaration for the JSON data
        json_data_var = VariableDeclaration(
            name="json_data",
            type_annotation=self._infer_runa_type(document.root),
            initial_value=self._convert_json_value_to_runa_expression(document.root),
            is_mutable=False
        )
        statements.append(json_data_var)
        
        # Add demonstration operations
        statements.extend(self._generate_json_operations(document.root))
        
        return Program(statements=statements)
    
    def _convert_object(self, obj: JsonObject) -> DictionaryLiteral:
        """Convert JSON object to Runa dictionary."""
        pairs = []
        for prop in obj.properties:
            key_expr = StringLiteral(value=prop.key.value)
            value_expr = self._convert_json_value_to_runa_expression(prop.value)
            pairs.append(DictionaryPair(key=key_expr, value=value_expr))
        
        return DictionaryLiteral(pairs=pairs)
    
    def _convert_array(self, array: JsonArray) -> ListLiteral:
        """Convert JSON array to Runa list."""
        elements = []
        for element in array.elements:
            elements.append(self._convert_json_value_to_runa_expression(element))
        
        return ListLiteral(elements=elements)
    
    def _convert_property(self, prop: JsonProperty) -> AssignmentStatement:
        """Convert JSON property to Runa assignment."""
        target = Identifier(name=self._sanitize_identifier(prop.key.value))
        value = self._convert_json_value_to_runa_expression(prop.value)
        return AssignmentStatement(target=target, value=value)
    
    def _convert_string(self, string: JsonString) -> StringLiteral:
        """Convert JSON string to Runa string literal."""
        return StringLiteral(value=string.value)
    
    def _convert_number(self, number: JsonNumber) -> Union[IntegerLiteral, FloatLiteral]:
        """Convert JSON number to Runa number literal."""
        if number.is_integer:
            return IntegerLiteral(value=int(number.value))
        else:
            return FloatLiteral(value=float(number.value))
    
    def _convert_boolean(self, boolean: JsonBoolean) -> BooleanLiteral:
        """Convert JSON boolean to Runa boolean literal."""
        return BooleanLiteral(value=boolean.value)
    
    def _convert_null(self, null: JsonNull) -> NullLiteral:
        """Convert JSON null to Runa null literal."""
        return NullLiteral()
    
    def _convert_json_value_to_runa_expression(self, value: JsonValue) -> Expression:
        """Convert JSON value to Runa expression."""
        if isinstance(value, JsonString):
            return StringLiteral(value=value.value)
        elif isinstance(value, JsonNumber):
            if value.is_integer:
                return IntegerLiteral(value=int(value.value))
            else:
                return FloatLiteral(value=float(value.value))
        elif isinstance(value, JsonBoolean):
            return BooleanLiteral(value=value.value)
        elif isinstance(value, JsonNull):
            return NullLiteral()
        elif isinstance(value, JsonObject):
            return self._convert_object(value)
        elif isinstance(value, JsonArray):
            return self._convert_array(value)
        else:
            return StringLiteral(value="<unknown>")
    
    def _infer_runa_type(self, value: JsonValue) -> TypeAnnotation:
        """Infer Runa type from JSON value."""
        if isinstance(value, JsonString):
            return TypeAnnotation("String")
        elif isinstance(value, JsonNumber):
            if value.is_integer:
                return TypeAnnotation("Integer")
            else:
                return TypeAnnotation("Float")
        elif isinstance(value, JsonBoolean):
            return TypeAnnotation("Boolean")
        elif isinstance(value, JsonNull):
            return TypeAnnotation("Any")
        elif isinstance(value, JsonObject):
            return TypeAnnotation("Dictionary")
        elif isinstance(value, JsonArray):
            # Try to infer element type
            if value.elements:
                first_type = self._infer_runa_type(value.elements[0])
                return TypeAnnotation(f"List[{first_type.name}]")
            else:
                return TypeAnnotation("List")
        else:
            return TypeAnnotation("Any")
    
    def _generate_json_operations(self, root: JsonValue) -> List[Statement]:
        """Generate demonstration operations for JSON data."""
        operations = []
        
        if isinstance(root, JsonObject):
            # Generate property access examples
            for i, prop in enumerate(root.properties[:3]):  # Limit to first 3
                access_expr = FunctionCall(
                    function=Identifier(name="Display"),
                    arguments=[
                        BinaryOperation(
                            left=StringLiteral(value=f"Property '{prop.key.value}': "),
                            operator="concatenated with",
                            right=PropertyAccess(
                                object=Identifier(name="json_data"),
                                property=prop.key.value
                            )
                        )
                    ]
                )
                operations.append(ExpressionStatement(expression=access_expr))
        
        elif isinstance(root, JsonArray):
            # Generate array access examples
            if root.elements:
                access_expr = FunctionCall(
                    function=Identifier(name="Display"),
                    arguments=[
                        BinaryOperation(
                            left=StringLiteral(value="First element: "),
                            operator="concatenated with",
                            right=ArrayAccess(
                                array=Identifier(name="json_data"),
                                index=IntegerLiteral(value=0)
                            )
                        )
                    ]
                )
                operations.append(ExpressionStatement(expression=access_expr))
        
        return operations
    
    def _sanitize_identifier(self, name: str) -> str:
        """Sanitize string to be a valid Runa identifier."""
        # Replace non-alphanumeric characters with underscores
        import re
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Ensure it starts with a letter or underscore
        if sanitized and not sanitized[0].isalpha() and sanitized[0] != '_':
            sanitized = f"_{sanitized}"
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed"
        
        return sanitized
    
    def _create_placeholder(self, node: JsonNode) -> ASTNode:
        """Create placeholder for unsupported nodes."""
        return ExpressionStatement(
            expression=StringLiteral(value=f"JSON_{node.__class__.__name__}")
        )


class RunaToJsonConverter:
    """Converts Runa AST to JSON AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: ASTNode) -> JsonNode:
        """Convert Runa AST node to JSON AST node."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, VariableDeclaration):
                return self._convert_variable_declaration(runa_node)
            elif isinstance(runa_node, DictionaryLiteral):
                return self._convert_dictionary_literal(runa_node)
            elif isinstance(runa_node, ListLiteral):
                return self._convert_list_literal(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return self._convert_string_literal(runa_node)
            elif isinstance(runa_node, IntegerLiteral):
                return self._convert_integer_literal(runa_node)
            elif isinstance(runa_node, FloatLiteral):
                return self._convert_float_literal(runa_node)
            elif isinstance(runa_node, BooleanLiteral):
                return self._convert_boolean_literal(runa_node)
            elif isinstance(runa_node, NullLiteral):
                return self._convert_null_literal(runa_node)
            else:
                return self._create_placeholder(runa_node)
        except Exception as e:
            self.logger.error(f"Runa to JSON conversion failed: {e}")
            return self._create_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> JsonDocument:
        """Convert Runa program to JSON document."""
        # Look for the main data structure in the program
        main_data = None
        
        for stmt in program.statements:
            if isinstance(stmt, VariableDeclaration) and stmt.initial_value:
                # Use the first variable with a complex initial value
                if isinstance(stmt.initial_value, (DictionaryLiteral, ListLiteral)):
                    main_data = self._convert_runa_expression_to_json_value(stmt.initial_value)
                    break
        
        # If no complex data found, create an object with all variables
        if main_data is None:
            properties = []
            for stmt in program.statements:
                if isinstance(stmt, VariableDeclaration) and stmt.initial_value:
                    json_value = self._convert_runa_expression_to_json_value(stmt.initial_value)
                    prop = JsonProperty(
                        key=JsonString(value=stmt.name),
                        value=json_value
                    )
                    properties.append(prop)
            
            main_data = JsonObject(properties=properties)
        
        return JsonDocument(root=main_data)
    
    def _convert_variable_declaration(self, var_decl: VariableDeclaration) -> JsonProperty:
        """Convert Runa variable declaration to JSON property."""
        json_value = JsonNull()
        if var_decl.initial_value:
            json_value = self._convert_runa_expression_to_json_value(var_decl.initial_value)
        
        return JsonProperty(
            key=JsonString(value=var_decl.name),
            value=json_value
        )
    
    def _convert_dictionary_literal(self, dict_lit: DictionaryLiteral) -> JsonObject:
        """Convert Runa dictionary literal to JSON object."""
        properties = []
        
        for pair in dict_lit.pairs:
            # Extract key
            if isinstance(pair.key, StringLiteral):
                key = JsonString(value=pair.key.value)
            else:
                key = JsonString(value=str(pair.key))
            
            # Convert value
            value = self._convert_runa_expression_to_json_value(pair.value)
            
            properties.append(JsonProperty(key=key, value=value))
        
        return JsonObject(properties=properties)
    
    def _convert_list_literal(self, list_lit: ListLiteral) -> JsonArray:
        """Convert Runa list literal to JSON array."""
        elements = []
        
        for element in list_lit.elements:
            json_element = self._convert_runa_expression_to_json_value(element)
            elements.append(json_element)
        
        return JsonArray(elements=elements)
    
    def _convert_string_literal(self, str_lit: StringLiteral) -> JsonString:
        """Convert Runa string literal to JSON string."""
        return JsonString(value=str_lit.value)
    
    def _convert_integer_literal(self, int_lit: IntegerLiteral) -> JsonNumber:
        """Convert Runa integer literal to JSON number."""
        return JsonNumber(value=int_lit.value)
    
    def _convert_float_literal(self, float_lit: FloatLiteral) -> JsonNumber:
        """Convert Runa float literal to JSON number."""
        return JsonNumber(value=float_lit.value)
    
    def _convert_boolean_literal(self, bool_lit: BooleanLiteral) -> JsonBoolean:
        """Convert Runa boolean literal to JSON boolean."""
        return JsonBoolean(value=bool_lit.value)
    
    def _convert_null_literal(self, null_lit: NullLiteral) -> JsonNull:
        """Convert Runa null literal to JSON null."""
        return JsonNull()
    
    def _convert_runa_expression_to_json_value(self, expr: Expression) -> JsonValue:
        """Convert Runa expression to JSON value."""
        if isinstance(expr, StringLiteral):
            return JsonString(value=expr.value)
        elif isinstance(expr, IntegerLiteral):
            return JsonNumber(value=expr.value)
        elif isinstance(expr, FloatLiteral):
            return JsonNumber(value=expr.value)
        elif isinstance(expr, BooleanLiteral):
            return JsonBoolean(value=expr.value)
        elif isinstance(expr, NullLiteral):
            return JsonNull()
        elif isinstance(expr, DictionaryLiteral):
            return self._convert_dictionary_literal(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list_literal(expr)
        elif isinstance(expr, Identifier):
            # Convert identifier to string
            return JsonString(value=expr.name)
        else:
            # Convert unknown expressions to string representation
            return JsonString(value=str(expr))
    
    def _create_placeholder(self, node: ASTNode) -> JsonValue:
        """Create placeholder for unsupported nodes."""
        return JsonString(value=f"Runa_{node.__class__.__name__}")


# Convenience functions
def json_to_runa(json_ast: JsonDocument) -> Program:
    """Convert JSON AST to Runa AST."""
    converter = JsonToRunaConverter()
    return converter.convert(json_ast)


def runa_to_json(runa_ast: Program) -> JsonDocument:
    """Convert Runa AST to JSON AST."""
    converter = RunaToJsonConverter()
    return converter.convert(runa_ast)


def json_value_to_runa_expression(json_value: JsonValue) -> Expression:
    """Convert JSON value to Runa expression."""
    converter = JsonToRunaConverter()
    return converter._convert_json_value_to_runa_expression(json_value)


def runa_expression_to_json_value(runa_expr: Expression) -> JsonValue:
    """Convert Runa expression to JSON value."""
    converter = RunaToJsonConverter()
    return converter._convert_runa_expression_to_json_value(runa_expr)