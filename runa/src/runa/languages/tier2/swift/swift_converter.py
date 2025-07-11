#!/usr/bin/env python3
"""
Swift ↔ Runa Bidirectional Converter

Converts between Swift AST and Runa AST in both directions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from .swift_ast import *
from ....core.runa_ast import *


class SwiftToRunaConverter:
    """Converts Swift AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'Int': 'Integer',
            'Float': 'Float',
            'Double': 'Float',
            'String': 'String',
            'Bool': 'Boolean',
            'Array': 'List',
            'Dictionary': 'Dictionary',
            'Optional': 'Optional',
        }
    
    def convert(self, swift_node: SwiftNode) -> ASTNode:
        """Convert Swift AST node to Runa AST node."""
        try:
            if isinstance(swift_node, SwiftSourceFile):
                return self._convert_source_file(swift_node)
            elif isinstance(swift_node, SwiftClassDeclaration):
                return self._convert_class_declaration(swift_node)
            elif isinstance(swift_node, SwiftStructDeclaration):
                return self._convert_struct_declaration(swift_node)
            elif isinstance(swift_node, SwiftEnumDeclaration):
                return self._convert_enum_declaration(swift_node)
            elif isinstance(swift_node, SwiftFunctionDeclaration):
                return self._convert_function_declaration(swift_node)
            elif isinstance(swift_node, SwiftVariableDeclaration):
                return self._convert_variable_declaration(swift_node)
            elif isinstance(swift_node, SwiftIdentifierExpression):
                return self._convert_identifier_expression(swift_node)
            elif isinstance(swift_node, SwiftLiteralExpression):
                return self._convert_literal_expression(swift_node)
            else:
                return self._create_placeholder(swift_node)
        except Exception as e:
            self.logger.error(f"Failed to convert Swift node: {e}")
            return self._create_placeholder(swift_node)
    
    def _convert_source_file(self, source_file: SwiftSourceFile) -> Program:
        """Convert Swift source file to Runa program."""
        statements = []
        
        # Convert imports
        for import_decl in source_file.imports:
            statements.append(ImportStatement(
                module_name=import_decl.module_name,
                imported_names=["*"]
            ))
        
        # Convert declarations
        for decl in source_file.declarations:
            converted = self.convert(decl)
            if converted:
                statements.append(converted)
        
        return Program(statements=statements)
    
    def _convert_class_declaration(self, class_decl: SwiftClassDeclaration) -> StructDefinition:
        """Convert Swift class to Runa struct."""
        fields = []
        
        for member in class_decl.members:
            if isinstance(member, SwiftVariableDeclaration):
                field = FieldDefinition(
                    name=member.name,
                    type_annotation=self._convert_type(member.type_annotation),
                    annotations={"swift_access": member.access_level.value}
                )
                fields.append(field)
        
        return StructDefinition(
            name=class_decl.name,
            fields=fields,
            annotations={"swift_type": "class"}
        )
    
    def _convert_struct_declaration(self, struct_decl: SwiftStructDeclaration) -> StructDefinition:
        """Convert Swift struct to Runa struct."""
        fields = []
        
        for member in struct_decl.members:
            if isinstance(member, SwiftVariableDeclaration):
                field = FieldDefinition(
                    name=member.name,
                    type_annotation=self._convert_type(member.type_annotation),
                    annotations={"swift_access": member.access_level.value}
                )
                fields.append(field)
        
        return StructDefinition(
            name=struct_decl.name,
            fields=fields,
            annotations={"swift_type": "struct"}
        )
    
    def _convert_enum_declaration(self, enum_decl: SwiftEnumDeclaration) -> UnionType:
        """Convert Swift enum to Runa union type."""
        types = []
        
        for case in enum_decl.cases:
            types.append(BasicType(name=case.name))
        
        return UnionType(
            types=types,
            annotations={"swift_enum": enum_decl.name}
        )
    
    def _convert_function_declaration(self, func_decl: SwiftFunctionDeclaration) -> ProcessDeclaration:
        """Convert Swift function to Runa process."""
        parameters = []
        
        for param in func_decl.parameters:
            field = FieldDefinition(
                name=param.internal_name,
                type_annotation=self._convert_type(param.type_annotation)
            )
            parameters.append(field)
        
        return ProcessDeclaration(
            name=func_decl.name,
            parameters=parameters,
            return_type=self._convert_type(func_decl.return_type),
            is_async=func_decl.is_async,
            annotations={"swift_throws": func_decl.is_throws}
        )
    
    def _convert_variable_declaration(self, var_decl: SwiftVariableDeclaration) -> LetStatement:
        """Convert Swift variable to Runa let statement."""
        return LetStatement(
            name=var_decl.name,
            type_annotation=self._convert_type(var_decl.type_annotation),
            value=self.convert(var_decl.initializer) if var_decl.initializer else None,
            annotations={"swift_mutability": var_decl.mutability.value}
        )
    
    def _convert_identifier_expression(self, identifier: SwiftIdentifierExpression) -> Identifier:
        """Convert Swift identifier to Runa identifier."""
        return Identifier(name=identifier.name)
    
    def _convert_literal_expression(self, literal: SwiftLiteralExpression) -> Expression:
        """Convert Swift literal to Runa literal."""
        if literal.literal_type == "int":
            return IntegerLiteral(value=int(literal.value))
        elif literal.literal_type == "float":
            return FloatLiteral(value=float(literal.value))
        elif literal.literal_type == "string":
            return StringLiteral(value=str(literal.value))
        elif literal.literal_type == "bool":
            return BooleanLiteral(value=bool(literal.value))
        else:
            return StringLiteral(value=str(literal.value))
    
    def _convert_type(self, swift_type: Optional[SwiftType]) -> Optional[TypeExpression]:
        """Convert Swift type to Runa type."""
        if not swift_type:
            return None
        
        if isinstance(swift_type, SwiftTypeIdentifier):
            runa_type_name = self.type_mapping.get(swift_type.name, swift_type.name)
            return BasicType(name=runa_type_name)
        elif isinstance(swift_type, SwiftOptionalType):
            inner_type = self._convert_type(swift_type.wrapped_type)
            return OptionalType(inner_type=inner_type)
        elif isinstance(swift_type, SwiftArrayType):
            element_type = self._convert_type(swift_type.element_type)
            return GenericType(
                base_type=BasicType(name="List"),
                type_arguments=[element_type] if element_type else []
            )
        else:
            return BasicType(name="Any")
    
    def _create_placeholder(self, swift_node: SwiftNode) -> Expression:
        """Create placeholder for unconverted nodes."""
        return Identifier(name=f"swift_{type(swift_node).__name__.lower()}")


class RunaToSwiftConverter:
    """Converts Runa AST to Swift AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'Integer': 'Int',
            'Float': 'Double',
            'String': 'String',
            'Boolean': 'Bool',
            'List': 'Array',
            'Dictionary': 'Dictionary',
            'Optional': 'Optional',
        }
    
    def convert(self, runa_node: ASTNode) -> SwiftNode:
        """Convert Runa AST node to Swift AST node."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, StructDefinition):
                return self._convert_struct_definition(runa_node)
            elif isinstance(runa_node, ProcessDeclaration):
                return self._convert_process_declaration(runa_node)
            elif isinstance(runa_node, LetStatement):
                return self._convert_let_statement(runa_node)
            elif isinstance(runa_node, Identifier):
                return self._convert_identifier(runa_node)
            elif isinstance(runa_node, IntegerLiteral):
                return self._convert_integer_literal(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return self._convert_string_literal(runa_node)
            elif isinstance(runa_node, BooleanLiteral):
                return self._convert_boolean_literal(runa_node)
            else:
                return self._create_swift_placeholder(runa_node)
        except Exception as e:
            self.logger.error(f"Failed to convert Runa node: {e}")
            return self._create_swift_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> SwiftSourceFile:
        """Convert Runa program to Swift source file."""
        imports = []
        declarations = []
        
        for stmt in program.statements:
            if isinstance(stmt, ImportStatement):
                imports.append(SwiftImportDeclaration(module_name=stmt.module_name))
            else:
                converted = self.convert(stmt)
                if converted and isinstance(converted, SwiftDeclaration):
                    declarations.append(converted)
        
        return SwiftSourceFile(imports=imports, declarations=declarations)
    
    def _convert_struct_definition(self, struct_def: StructDefinition) -> Union[SwiftStructDeclaration, SwiftClassDeclaration]:
        """Convert Runa struct to Swift struct or class."""
        members = []
        
        for field in struct_def.fields:
            var_decl = SwiftVariableDeclaration(
                name=field.name,
                type_annotation=self._convert_runa_type(field.type_annotation),
                mutability=SwiftMutabilityKind.MUTABLE
            )
            members.append(var_decl)
        
        annotations = struct_def.annotations or {}
        swift_type = annotations.get("swift_type", "struct")
        
        if swift_type == "class":
            return SwiftClassDeclaration(name=struct_def.name, members=members)
        else:
            return SwiftStructDeclaration(name=struct_def.name, members=members)
    
    def _convert_process_declaration(self, process: ProcessDeclaration) -> SwiftFunctionDeclaration:
        """Convert Runa process to Swift function."""
        parameters = []
        
        for param in process.parameters:
            swift_param = SwiftParameter(
                internal_name=param.name,
                type_annotation=self._convert_runa_type(param.type_annotation)
            )
            parameters.append(swift_param)
        
        annotations = process.annotations or {}
        
        return SwiftFunctionDeclaration(
            name=process.name,
            parameters=parameters,
            return_type=self._convert_runa_type(process.return_type),
            is_async=process.is_async,
            is_throws=annotations.get("swift_throws", False)
        )
    
    def _convert_let_statement(self, let_stmt: LetStatement) -> SwiftVariableDeclaration:
        """Convert Runa let statement to Swift variable."""
        annotations = let_stmt.annotations or {}
        mutability_str = annotations.get("swift_mutability", "let")
        mutability = SwiftMutabilityKind.MUTABLE if mutability_str == "var" else SwiftMutabilityKind.IMMUTABLE
        
        return SwiftVariableDeclaration(
            name=let_stmt.name,
            type_annotation=self._convert_runa_type(let_stmt.type_annotation),
            initializer=self.convert(let_stmt.value) if let_stmt.value else None,
            mutability=mutability
        )
    
    def _convert_identifier(self, identifier: Identifier) -> SwiftIdentifierExpression:
        """Convert Runa identifier to Swift identifier."""
        return SwiftIdentifierExpression(name=identifier.name)
    
    def _convert_integer_literal(self, literal: IntegerLiteral) -> SwiftLiteralExpression:
        """Convert Runa integer literal to Swift literal."""
        return SwiftLiteralExpression(value=literal.value, literal_type="int")
    
    def _convert_string_literal(self, literal: StringLiteral) -> SwiftLiteralExpression:
        """Convert Runa string literal to Swift literal."""
        return SwiftLiteralExpression(value=literal.value, literal_type="string")
    
    def _convert_boolean_literal(self, literal: BooleanLiteral) -> SwiftLiteralExpression:
        """Convert Runa boolean literal to Swift literal."""
        return SwiftLiteralExpression(value=literal.value, literal_type="bool")
    
    def _convert_runa_type(self, runa_type: Optional[TypeExpression]) -> Optional[SwiftType]:
        """Convert Runa type to Swift type."""
        if not runa_type:
            return None
        
        if isinstance(runa_type, BasicType):
            swift_type_name = self.type_mapping.get(runa_type.name, runa_type.name)
            return SwiftTypeIdentifier(name=swift_type_name)
        elif isinstance(runa_type, OptionalType):
            inner_type = self._convert_runa_type(runa_type.inner_type)
            return SwiftOptionalType(wrapped_type=inner_type)
        elif isinstance(runa_type, GenericType):
            base_name = runa_type.base_type.name if isinstance(runa_type.base_type, BasicType) else "Generic"
            swift_base_name = self.type_mapping.get(base_name, base_name)
            
            if swift_base_name == "Array":
                element_type = self._convert_runa_type(runa_type.type_arguments[0]) if runa_type.type_arguments else None
                return SwiftArrayType(element_type=element_type)
            else:
                return SwiftTypeIdentifier(name=swift_base_name)
        else:
            return SwiftTypeIdentifier(name="Any")
    
    def _create_swift_placeholder(self, runa_node: ASTNode) -> SwiftExpression:
        """Create Swift placeholder for unconverted nodes."""
        return SwiftIdentifierExpression(name=f"runa_{type(runa_node).__name__.lower()}")


# Convenience functions
def swift_to_runa(swift_ast: SwiftNode) -> ASTNode:
    """Convert Swift AST to Runa AST."""
    converter = SwiftToRunaConverter()
    return converter.convert(swift_ast)


def runa_to_swift(runa_ast: ASTNode) -> SwiftNode:
    """Convert Runa AST to Swift AST."""
    converter = RunaToSwiftConverter()
    return converter.convert(runa_ast)