#!/usr/bin/env python3
"""
YAML ↔ Runa Bidirectional Converter

Converts between YAML AST and Runa AST in both directions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from .yaml_ast import *
from ....core.runa_ast import *


class YamlToRunaConverter:
    """Converts YAML AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, yaml_node: YamlNode) -> ASTNode:
        """Convert YAML AST node to Runa AST node."""
        try:
            if isinstance(yaml_node, YamlStream):
                return self._convert_stream(yaml_node)
            elif isinstance(yaml_node, YamlDocument):
                return self._convert_document(yaml_node)
            elif isinstance(yaml_node, YamlMapping):
                return self._convert_mapping(yaml_node)
            elif isinstance(yaml_node, YamlSequence):
                return self._convert_sequence(yaml_node)
            elif isinstance(yaml_node, YamlScalar):
                return self._convert_scalar(yaml_node)
            elif isinstance(yaml_node, YamlMappingItem):
                return self._convert_mapping_item(yaml_node)
            elif isinstance(yaml_node, YamlAlias):
                return self._convert_alias(yaml_node)
            elif isinstance(yaml_node, YamlAnchor):
                return self._convert_anchor(yaml_node)
            else:
                return self._create_placeholder(yaml_node)
        except Exception as e:
            self.logger.error(f"YAML to Runa conversion failed: {e}")
            return self._create_placeholder(yaml_node)
    
    def _convert_stream(self, stream: YamlStream) -> Program:
        """Convert YAML stream to Runa program."""
        statements = []
        
        if not stream.documents:
            return Program(statements=statements)
        
        # If single document, convert directly
        if len(stream.documents) == 1:
            doc_content = self._convert_yaml_value_to_runa_expression(stream.documents[0].content)
            yaml_data_var = VariableDeclaration(
                name="yaml_data",
                type_annotation=self._infer_runa_type(stream.documents[0].content),
                initial_value=doc_content,
                is_mutable=False
            )
            statements.append(yaml_data_var)
        else:
            # Multiple documents - create array
            documents = []
            for doc in stream.documents:
                doc_expr = self._convert_yaml_value_to_runa_expression(doc.content)
                documents.append(doc_expr)
            
            documents_var = VariableDeclaration(
                name="yaml_documents",
                type_annotation=TypeAnnotation("List"),
                initial_value=ListLiteral(elements=documents),
                is_mutable=False
            )
            statements.append(documents_var)
        
        # Add demonstration operations
        statements.extend(self._generate_yaml_operations(stream))
        
        return Program(statements=statements)
    
    def _convert_document(self, document: YamlDocument) -> Program:
        """Convert YAML document to Runa program."""
        statements = []
        
        # Create main data variable
        yaml_data_var = VariableDeclaration(
            name="yaml_data",
            type_annotation=self._infer_runa_type(document.content),
            initial_value=self._convert_yaml_value_to_runa_expression(document.content),
            is_mutable=False
        )
        statements.append(yaml_data_var)
        
        # Add demonstration operations
        statements.extend(self._generate_yaml_operations_from_value(document.content))
        
        return Program(statements=statements)
    
    def _convert_mapping(self, mapping: YamlMapping) -> DictionaryLiteral:
        """Convert YAML mapping to Runa dictionary."""
        pairs = []
        for item in mapping.items:
            key_expr = self._convert_yaml_value_to_runa_expression(item.key)
            value_expr = self._convert_yaml_value_to_runa_expression(item.value)
            pairs.append(DictionaryPair(key=key_expr, value=value_expr))
        
        return DictionaryLiteral(pairs=pairs)
    
    def _convert_sequence(self, sequence: YamlSequence) -> ListLiteral:
        """Convert YAML sequence to Runa list."""
        elements = []
        for item in sequence.items:
            elements.append(self._convert_yaml_value_to_runa_expression(item))
        
        return ListLiteral(elements=elements)
    
    def _convert_scalar(self, scalar: YamlScalar) -> Expression:
        """Convert YAML scalar to Runa expression."""
        if scalar.value is None:
            return NullLiteral()
        elif isinstance(scalar.value, bool):
            return BooleanLiteral(value=scalar.value)
        elif isinstance(scalar.value, int):
            return IntegerLiteral(value=scalar.value)
        elif isinstance(scalar.value, float):
            return FloatLiteral(value=scalar.value)
        elif isinstance(scalar.value, str):
            return StringLiteral(value=scalar.value)
        elif isinstance(scalar.value, bytes):
            # Convert bytes to string representation
            return StringLiteral(value=scalar.value.decode('utf-8', errors='replace'))
        else:
            return StringLiteral(value=str(scalar.value))
    
    def _convert_mapping_item(self, item: YamlMappingItem) -> AssignmentStatement:
        """Convert YAML mapping item to Runa assignment."""
        # Create variable name from key
        key_str = self._extract_key_string(item.key)
        target = Identifier(name=self._sanitize_identifier(key_str))
        value = self._convert_yaml_value_to_runa_expression(item.value)
        return AssignmentStatement(target=target, value=value)
    
    def _convert_alias(self, alias: YamlAlias) -> Identifier:
        """Convert YAML alias to Runa identifier."""
        return Identifier(name=f"anchor_{alias.name}")
    
    def _convert_anchor(self, anchor: YamlAnchor) -> VariableDeclaration:
        """Convert YAML anchor to Runa variable declaration."""
        return VariableDeclaration(
            name=f"anchor_{anchor.name}",
            type_annotation=self._infer_runa_type(anchor.value),
            initial_value=self._convert_yaml_value_to_runa_expression(anchor.value),
            is_mutable=False
        )
    
    def _convert_yaml_value_to_runa_expression(self, value: YamlValue) -> Expression:
        """Convert YAML value to Runa expression."""
        if isinstance(value, YamlScalar):
            return self._convert_scalar(value)
        elif isinstance(value, YamlMapping):
            return self._convert_mapping(value)
        elif isinstance(value, YamlSequence):
            return self._convert_sequence(value)
        elif isinstance(value, YamlAlias):
            return Identifier(name=f"anchor_{value.name}")
        elif isinstance(value, YamlAnchor):
            return self._convert_yaml_value_to_runa_expression(value.value)
        else:
            return StringLiteral(value="<unknown>")
    
    def _infer_runa_type(self, value: YamlValue) -> TypeAnnotation:
        """Infer Runa type from YAML value."""
        if isinstance(value, YamlScalar):
            if value.value is None:
                return TypeAnnotation("Any")
            elif isinstance(value.value, bool):
                return TypeAnnotation("Boolean")
            elif isinstance(value.value, int):
                return TypeAnnotation("Integer")
            elif isinstance(value.value, float):
                return TypeAnnotation("Float")
            elif isinstance(value.value, (str, bytes)):
                return TypeAnnotation("String")
            else:
                return TypeAnnotation("Any")
        elif isinstance(value, YamlMapping):
            return TypeAnnotation("Dictionary")
        elif isinstance(value, YamlSequence):
            if value.items:
                first_type = self._infer_runa_type(value.items[0])
                return TypeAnnotation(f"List[{first_type.name}]")
            else:
                return TypeAnnotation("List")
        elif isinstance(value, (YamlAlias, YamlAnchor)):
            return TypeAnnotation("Any")
        else:
            return TypeAnnotation("Any")
    
    def _generate_yaml_operations(self, stream: YamlStream) -> List[Statement]:
        """Generate demonstration operations for YAML stream."""
        operations = []
        
        if stream.documents:
            if len(stream.documents) == 1:
                operations.extend(self._generate_yaml_operations_from_value(stream.documents[0].content))
            else:
                # Multiple documents
                for i, doc in enumerate(stream.documents[:3]):  # Limit to first 3
                    access_expr = FunctionCall(
                        function=Identifier(name="Display"),
                        arguments=[
                            BinaryOperation(
                                left=StringLiteral(value=f"Document {i + 1}: "),
                                operator="concatenated with",
                                right=ArrayAccess(
                                    array=Identifier(name="yaml_documents"),
                                    index=IntegerLiteral(value=i)
                                )
                            )
                        ]
                    )
                    operations.append(ExpressionStatement(expression=access_expr))
        
        return operations
    
    def _generate_yaml_operations_from_value(self, value: YamlValue) -> List[Statement]:
        """Generate demonstration operations for YAML value."""
        operations = []
        
        if isinstance(value, YamlMapping):
            # Generate property access examples
            for i, item in enumerate(value.items[:3]):  # Limit to first 3
                key_str = self._extract_key_string(item.key)
                access_expr = FunctionCall(
                    function=Identifier(name="Display"),
                    arguments=[
                        BinaryOperation(
                            left=StringLiteral(value=f"Property '{key_str}': "),
                            operator="concatenated with",
                            right=PropertyAccess(
                                object=Identifier(name="yaml_data"),
                                property=key_str
                            )
                        )
                    ]
                )
                operations.append(ExpressionStatement(expression=access_expr))
        
        elif isinstance(value, YamlSequence):
            # Generate array access examples
            if value.items:
                access_expr = FunctionCall(
                    function=Identifier(name="Display"),
                    arguments=[
                        BinaryOperation(
                            left=StringLiteral(value="First element: "),
                            operator="concatenated with",
                            right=ArrayAccess(
                                array=Identifier(name="yaml_data"),
                                index=IntegerLiteral(value=0)
                            )
                        )
                    ]
                )
                operations.append(ExpressionStatement(expression=access_expr))
        
        return operations
    
    def _extract_key_string(self, key: YamlValue) -> str:
        """Extract string representation of key."""
        if isinstance(key, YamlScalar):
            return str(key.value) if key.value is not None else ""
        else:
            return str(key)
    
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
    
    def _create_placeholder(self, node: YamlNode) -> ASTNode:
        """Create placeholder for unsupported nodes."""
        return ExpressionStatement(
            expression=StringLiteral(value=f"YAML_{node.__class__.__name__}")
        )


class RunaToYamlConverter:
    """Converts Runa AST to YAML AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: ASTNode) -> YamlNode:
        """Convert Runa AST node to YAML AST node."""
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
            self.logger.error(f"Runa to YAML conversion failed: {e}")
            return self._create_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> YamlDocument:
        """Convert Runa program to YAML document."""
        # Look for the main data structure in the program
        main_data = None
        
        for stmt in program.statements:
            if isinstance(stmt, VariableDeclaration) and stmt.initial_value:
                # Use the first variable with a complex initial value
                if isinstance(stmt.initial_value, (DictionaryLiteral, ListLiteral)):
                    main_data = self._convert_runa_expression_to_yaml_value(stmt.initial_value)
                    break
        
        # If no complex data found, create a mapping with all variables
        if main_data is None:
            items = []
            for stmt in program.statements:
                if isinstance(stmt, VariableDeclaration) and stmt.initial_value:
                    yaml_value = self._convert_runa_expression_to_yaml_value(stmt.initial_value)
                    key = YamlScalar(value=stmt.name)
                    items.append(YamlMappingItem(key=key, value=yaml_value))
            
            main_data = YamlMapping(items=items)
        
        return YamlDocument(content=main_data)
    
    def _convert_variable_declaration(self, var_decl: VariableDeclaration) -> YamlMappingItem:
        """Convert Runa variable declaration to YAML mapping item."""
        yaml_value = YamlScalar(value=None)
        if var_decl.initial_value:
            yaml_value = self._convert_runa_expression_to_yaml_value(var_decl.initial_value)
        
        return YamlMappingItem(
            key=YamlScalar(value=var_decl.name),
            value=yaml_value
        )
    
    def _convert_dictionary_literal(self, dict_lit: DictionaryLiteral) -> YamlMapping:
        """Convert Runa dictionary literal to YAML mapping."""
        items = []
        
        for pair in dict_lit.pairs:
            # Extract key
            if isinstance(pair.key, StringLiteral):
                key = YamlScalar(value=pair.key.value)
            else:
                key = YamlScalar(value=str(pair.key))
            
            # Convert value
            value = self._convert_runa_expression_to_yaml_value(pair.value)
            
            items.append(YamlMappingItem(key=key, value=value))
        
        return YamlMapping(items=items)
    
    def _convert_list_literal(self, list_lit: ListLiteral) -> YamlSequence:
        """Convert Runa list literal to YAML sequence."""
        items = []
        
        for element in list_lit.elements:
            yaml_element = self._convert_runa_expression_to_yaml_value(element)
            items.append(yaml_element)
        
        return YamlSequence(items=items)
    
    def _convert_string_literal(self, str_lit: StringLiteral) -> YamlScalar:
        """Convert Runa string literal to YAML scalar."""
        return YamlScalar(value=str_lit.value)
    
    def _convert_integer_literal(self, int_lit: IntegerLiteral) -> YamlScalar:
        """Convert Runa integer literal to YAML scalar."""
        return YamlScalar(value=int_lit.value)
    
    def _convert_float_literal(self, float_lit: FloatLiteral) -> YamlScalar:
        """Convert Runa float literal to YAML scalar."""
        return YamlScalar(value=float_lit.value)
    
    def _convert_boolean_literal(self, bool_lit: BooleanLiteral) -> YamlScalar:
        """Convert Runa boolean literal to YAML scalar."""
        return YamlScalar(value=bool_lit.value)
    
    def _convert_null_literal(self, null_lit: NullLiteral) -> YamlScalar:
        """Convert Runa null literal to YAML scalar."""
        return YamlScalar(value=None)
    
    def _convert_runa_expression_to_yaml_value(self, expr: Expression) -> YamlValue:
        """Convert Runa expression to YAML value."""
        if isinstance(expr, StringLiteral):
            return YamlScalar(value=expr.value)
        elif isinstance(expr, IntegerLiteral):
            return YamlScalar(value=expr.value)
        elif isinstance(expr, FloatLiteral):
            return YamlScalar(value=expr.value)
        elif isinstance(expr, BooleanLiteral):
            return YamlScalar(value=expr.value)
        elif isinstance(expr, NullLiteral):
            return YamlScalar(value=None)
        elif isinstance(expr, DictionaryLiteral):
            return self._convert_dictionary_literal(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list_literal(expr)
        elif isinstance(expr, Identifier):
            # Convert identifier to string
            return YamlScalar(value=expr.name)
        else:
            # Convert unknown expressions to string representation
            return YamlScalar(value=str(expr))
    
    def _create_placeholder(self, node: ASTNode) -> YamlValue:
        """Create placeholder for unsupported nodes."""
        return YamlScalar(value=f"Runa_{node.__class__.__name__}")


# Convenience functions
def yaml_to_runa(yaml_ast: YamlDocument) -> Program:
    """Convert YAML AST to Runa AST."""
    converter = YamlToRunaConverter()
    return converter.convert(yaml_ast)


def runa_to_yaml(runa_ast: Program) -> YamlDocument:
    """Convert Runa AST to YAML AST."""
    converter = RunaToYamlConverter()
    return converter.convert(runa_ast)


def yaml_value_to_runa_expression(yaml_value: YamlValue) -> Expression:
    """Convert YAML value to Runa expression."""
    converter = YamlToRunaConverter()
    return converter._convert_yaml_value_to_runa_expression(yaml_value)


def runa_expression_to_yaml_value(runa_expr: Expression) -> YamlValue:
    """Convert Runa expression to YAML value."""
    converter = RunaToYamlConverter()
    return converter._convert_runa_expression_to_yaml_value(runa_expr)