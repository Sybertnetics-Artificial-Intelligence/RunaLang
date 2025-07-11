#!/usr/bin/env python3
"""
PHP ↔ Runa Bidirectional Converter

Converts between PHP AST and Runa AST in both directions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from .php_ast import *
from ....core.runa_ast import *


class PhpToRunaConverter:
    """Converts PHP AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'int': 'Integer',
            'float': 'Float',
            'string': 'String',
            'bool': 'Boolean',
            'array': 'List',
            'object': 'Object',
            'mixed': 'Any',
            'void': 'Void',
            'null': 'Null',
        }
    
    def convert(self, php_node: PhpNode) -> ASTNode:
        """Convert PHP AST node to Runa AST node."""
        try:
            if isinstance(php_node, PhpSourceFile):
                return self._convert_source_file(php_node)
            elif isinstance(php_node, PhpClassDeclaration):
                return self._convert_class_declaration(php_node)
            elif isinstance(php_node, PhpInterfaceDeclaration):
                return self._convert_interface_declaration(php_node)
            elif isinstance(php_node, PhpTraitDeclaration):
                return self._convert_trait_declaration(php_node)
            elif isinstance(php_node, PhpEnumDeclaration):
                return self._convert_enum_declaration(php_node)
            elif isinstance(php_node, PhpFunctionDeclaration):
                return self._convert_function_declaration(php_node)
            elif isinstance(php_node, PhpMethodDeclaration):
                return self._convert_method_declaration(php_node)
            elif isinstance(php_node, PhpVariable):
                return self._convert_variable(php_node)
            elif isinstance(php_node, PhpLiteral):
                return self._convert_literal(php_node)
            elif isinstance(php_node, PhpIdentifier):
                return self._convert_identifier(php_node)
            else:
                return self._create_placeholder(php_node)
        except Exception as e:
            self.logger.error(f"Failed to convert PHP node: {e}")
            return self._create_placeholder(php_node)
    
    def _convert_source_file(self, source_file: PhpSourceFile) -> Program:
        """Convert PHP source file to Runa program."""
        statements = []
        
        # Convert namespace declarations
        for decl in source_file.declarations:
            if isinstance(decl, PhpNamespaceDeclaration):
                # Add namespace as import
                statements.append(ImportStatement(
                    module_name=decl.name,
                    imported_names=["*"]
                ))
            elif isinstance(decl, PhpUseDeclaration):
                # Convert use declarations to imports
                statements.append(ImportStatement(
                    module_name=decl.name,
                    imported_names=[decl.alias] if decl.alias else ["*"]
                ))
            else:
                converted = self.convert(decl)
                if converted:
                    statements.append(converted)
        
        # Convert statements
        for stmt in source_file.statements:
            converted = self.convert(stmt)
            if converted:
                statements.append(converted)
        
        return Program(statements=statements)
    
    def _convert_class_declaration(self, class_decl: PhpClassDeclaration) -> StructDefinition:
        """Convert PHP class to Runa struct."""
        fields = []
        
        for member in class_decl.members:
            if isinstance(member, PhpPropertyDeclaration):
                field = FieldDefinition(
                    name=member.name,
                    type_annotation=self._convert_type(member.type_hint),
                    annotations={
                        "php_visibility": member.visibility.value if member.visibility else "public",
                        "php_static": member.is_static,
                        "php_readonly": member.is_readonly
                    }
                )
                fields.append(field)
        
        return StructDefinition(
            name=class_decl.name,
            fields=fields,
            annotations={
                "php_type": "class",
                "php_extends": class_decl.extends,
                "php_implements": class_decl.implements,
                "php_abstract": class_decl.is_abstract,
                "php_final": class_decl.is_final,
                "php_readonly": class_decl.is_readonly
            }
        )
    
    def _convert_interface_declaration(self, interface_decl: PhpInterfaceDeclaration) -> StructDefinition:
        """Convert PHP interface to Runa struct."""
        return StructDefinition(
            name=interface_decl.name,
            fields=[],
            annotations={
                "php_type": "interface",
                "php_extends": interface_decl.extends
            }
        )
    
    def _convert_trait_declaration(self, trait_decl: PhpTraitDeclaration) -> StructDefinition:
        """Convert PHP trait to Runa struct."""
        return StructDefinition(
            name=trait_decl.name,
            fields=[],
            annotations={"php_type": "trait"}
        )
    
    def _convert_enum_declaration(self, enum_decl: PhpEnumDeclaration) -> UnionType:
        """Convert PHP enum to Runa union type."""
        types = []
        
        for case in enum_decl.cases:
            types.append(BasicType(name=case.name))
        
        return UnionType(
            types=types,
            annotations={
                "php_enum": enum_decl.name,
                "php_backed_type": enum_decl.backed_type.name if enum_decl.backed_type else None
            }
        )
    
    def _convert_function_declaration(self, func_decl: PhpFunctionDeclaration) -> ProcessDeclaration:
        """Convert PHP function to Runa process."""
        parameters = []
        
        for param in func_decl.parameters:
            field = FieldDefinition(
                name=param.name.lstrip('$'),  # Remove $ prefix
                type_annotation=self._convert_type(param.type_hint),
                annotations={
                    "php_reference": param.is_reference,
                    "php_variadic": param.is_variadic
                }
            )
            parameters.append(field)
        
        return ProcessDeclaration(
            name=func_decl.name,
            parameters=parameters,
            return_type=self._convert_type(func_decl.return_type),
            annotations={
                "php_generator": func_decl.is_generator
            }
        )
    
    def _convert_method_declaration(self, method_decl: PhpMethodDeclaration) -> ProcessDeclaration:
        """Convert PHP method to Runa process."""
        parameters = []
        
        for param in method_decl.parameters:
            field = FieldDefinition(
                name=param.name.lstrip('$'),  # Remove $ prefix
                type_annotation=self._convert_type(param.type_hint),
                annotations={
                    "php_reference": param.is_reference,
                    "php_variadic": param.is_variadic
                }
            )
            parameters.append(field)
        
        return ProcessDeclaration(
            name=method_decl.name,
            parameters=parameters,
            return_type=self._convert_type(method_decl.return_type),
            annotations={
                "php_visibility": method_decl.visibility.value if method_decl.visibility else "public",
                "php_static": method_decl.is_static,
                "php_abstract": method_decl.is_abstract,
                "php_final": method_decl.is_final
            }
        )
    
    def _convert_variable(self, variable: PhpVariable) -> Identifier:
        """Convert PHP variable to Runa identifier."""
        # Remove $ prefix
        name = variable.name.lstrip('$')
        return Identifier(name=name)
    
    def _convert_literal(self, literal: PhpLiteral) -> Expression:
        """Convert PHP literal to Runa literal."""
        if literal.literal_type == "int":
            return IntegerLiteral(value=int(literal.value))
        elif literal.literal_type == "float":
            return FloatLiteral(value=float(literal.value))
        elif literal.literal_type == "string":
            return StringLiteral(value=str(literal.value))
        elif literal.literal_type == "bool":
            return BooleanLiteral(value=bool(literal.value))
        elif literal.literal_type == "null":
            return NullLiteral()
        else:
            return StringLiteral(value=str(literal.value))
    
    def _convert_identifier(self, identifier: PhpIdentifier) -> Identifier:
        """Convert PHP identifier to Runa identifier."""
        return Identifier(name=identifier.name)
    
    def _convert_type(self, php_type: Optional[PhpType]) -> Optional[TypeExpression]:
        """Convert PHP type to Runa type."""
        if not php_type:
            return None
        
        if isinstance(php_type, PhpTypeDeclaration):
            runa_type_name = self.type_mapping.get(php_type.name.lower(), php_type.name)
            return BasicType(name=runa_type_name)
        elif isinstance(php_type, PhpNullableType):
            inner_type = self._convert_type(php_type.inner_type)
            return OptionalType(inner_type=inner_type)
        elif isinstance(php_type, PhpUnionType):
            types = [self._convert_type(t) for t in php_type.types if t]
            return UnionType(types=[t for t in types if t])
        else:
            return BasicType(name="Any")
    
    def _create_placeholder(self, php_node: PhpNode) -> Expression:
        """Create placeholder for unconverted nodes."""
        return Identifier(name=f"php_{type(php_node).__name__.lower()}")


class RunaToPhpConverter:
    """Converts Runa AST to PHP AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'Integer': 'int',
            'Float': 'float',
            'String': 'string',
            'Boolean': 'bool',
            'List': 'array',
            'Object': 'object',
            'Any': 'mixed',
            'Void': 'void',
            'Null': 'null',
        }
    
    def convert(self, runa_node: ASTNode) -> PhpNode:
        """Convert Runa AST node to PHP AST node."""
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
            elif isinstance(runa_node, NullLiteral):
                return self._convert_null_literal(runa_node)
            else:
                return self._create_php_placeholder(runa_node)
        except Exception as e:
            self.logger.error(f"Failed to convert Runa node: {e}")
            return self._create_php_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> PhpSourceFile:
        """Convert Runa program to PHP source file."""
        declarations = []
        statements = []
        
        for stmt in program.statements:
            if isinstance(stmt, ImportStatement):
                declarations.append(PhpUseDeclaration(name=stmt.module_name))
            elif isinstance(stmt, StructDefinition):
                converted = self.convert(stmt)
                if isinstance(converted, PhpDeclaration):
                    declarations.append(converted)
            elif isinstance(stmt, ProcessDeclaration):
                converted = self.convert(stmt)
                if isinstance(converted, PhpDeclaration):
                    declarations.append(converted)
            else:
                converted = self.convert(stmt)
                if isinstance(converted, PhpStatement):
                    statements.append(converted)
        
        return PhpSourceFile(declarations=declarations, statements=statements)
    
    def _convert_struct_definition(self, struct_def: StructDefinition) -> PhpClassDeclaration:
        """Convert Runa struct to PHP class/interface/trait."""
        annotations = struct_def.annotations or {}
        php_type = annotations.get("php_type", "class")
        
        if php_type == "interface":
            return PhpInterfaceDeclaration(
                name=struct_def.name,
                extends=annotations.get("php_extends", [])
            )
        elif php_type == "trait":
            return PhpTraitDeclaration(name=struct_def.name)
        else:
            # Convert to class
            members = []
            
            for field in struct_def.fields:
                field_annotations = field.annotations or {}
                prop = PhpPropertyDeclaration(
                    name=field.name,
                    type_hint=self._convert_runa_type(field.type_annotation),
                    visibility=self._get_php_visibility(field_annotations.get("php_visibility", "public")),
                    is_static=field_annotations.get("php_static", False),
                    is_readonly=field_annotations.get("php_readonly", False)
                )
                members.append(prop)
            
            return PhpClassDeclaration(
                name=struct_def.name,
                extends=annotations.get("php_extends"),
                implements=annotations.get("php_implements", []),
                members=members,
                is_abstract=annotations.get("php_abstract", False),
                is_final=annotations.get("php_final", False),
                is_readonly=annotations.get("php_readonly", False)
            )
    
    def _convert_process_declaration(self, process: ProcessDeclaration) -> PhpFunctionDeclaration:
        """Convert Runa process to PHP function."""
        parameters = []
        
        for param in process.parameters:
            param_annotations = param.annotations or {}
            php_param = PhpParameter(
                name=f"${param.name}",  # Add $ prefix
                type_hint=self._convert_runa_type(param.type_annotation),
                is_reference=param_annotations.get("php_reference", False),
                is_variadic=param_annotations.get("php_variadic", False)
            )
            parameters.append(php_param)
        
        annotations = process.annotations or {}
        
        # Check if it should be a method
        if "php_visibility" in annotations:
            return PhpMethodDeclaration(
                name=process.name,
                parameters=parameters,
                return_type=self._convert_runa_type(process.return_type),
                visibility=self._get_php_visibility(annotations.get("php_visibility", "public")),
                is_static=annotations.get("php_static", False),
                is_abstract=annotations.get("php_abstract", False),
                is_final=annotations.get("php_final", False)
            )
        else:
            return PhpFunctionDeclaration(
                name=process.name,
                parameters=parameters,
                return_type=self._convert_runa_type(process.return_type),
                is_generator=annotations.get("php_generator", False)
            )
    
    def _convert_let_statement(self, let_stmt: LetStatement) -> PhpExpressionStatement:
        """Convert Runa let statement to PHP assignment."""
        target = PhpVariable(name=f"${let_stmt.name}")  # Add $ prefix
        value = self.convert(let_stmt.value) if let_stmt.value else PhpLiteral(value=None, literal_type="null")
        
        assignment = PhpAssignmentExpression(
            target=target,
            value=value
        )
        
        return PhpExpressionStatement(expression=assignment)
    
    def _convert_identifier(self, identifier: Identifier) -> PhpIdentifier:
        """Convert Runa identifier to PHP identifier."""
        return PhpIdentifier(name=identifier.name)
    
    def _convert_integer_literal(self, literal: IntegerLiteral) -> PhpLiteral:
        """Convert Runa integer literal to PHP literal."""
        return PhpLiteral(value=literal.value, literal_type="int")
    
    def _convert_string_literal(self, literal: StringLiteral) -> PhpLiteral:
        """Convert Runa string literal to PHP literal."""
        return PhpLiteral(value=literal.value, literal_type="string")
    
    def _convert_boolean_literal(self, literal: BooleanLiteral) -> PhpLiteral:
        """Convert Runa boolean literal to PHP literal."""
        return PhpLiteral(value=literal.value, literal_type="bool")
    
    def _convert_null_literal(self, literal: NullLiteral) -> PhpLiteral:
        """Convert Runa null literal to PHP literal."""
        return PhpLiteral(value=None, literal_type="null")
    
    def _convert_runa_type(self, runa_type: Optional[TypeExpression]) -> Optional[PhpType]:
        """Convert Runa type to PHP type."""
        if not runa_type:
            return None
        
        if isinstance(runa_type, BasicType):
            php_type_name = self.type_mapping.get(runa_type.name, runa_type.name.lower())
            return PhpTypeDeclaration(name=php_type_name)
        elif isinstance(runa_type, OptionalType):
            inner_type = self._convert_runa_type(runa_type.inner_type)
            return PhpNullableType(inner_type=inner_type)
        elif isinstance(runa_type, UnionType):
            types = [self._convert_runa_type(t) for t in runa_type.types if t]
            return PhpUnionType(types=[t for t in types if t])
        else:
            return PhpTypeDeclaration(name="mixed")
    
    def _get_php_visibility(self, visibility_str: str) -> PhpVisibility:
        """Convert visibility string to PHP visibility enum."""
        visibility_map = {
            "public": PhpVisibility.PUBLIC,
            "protected": PhpVisibility.PROTECTED,
            "private": PhpVisibility.PRIVATE
        }
        return visibility_map.get(visibility_str.lower(), PhpVisibility.PUBLIC)
    
    def _create_php_placeholder(self, runa_node: ASTNode) -> PhpExpression:
        """Create PHP placeholder for unconverted nodes."""
        return PhpIdentifier(name=f"runa_{type(runa_node).__name__.lower()}")


# Convenience functions
def php_to_runa(php_ast: PhpNode) -> ASTNode:
    """Convert PHP AST to Runa AST."""
    converter = PhpToRunaConverter()
    return converter.convert(php_ast)


def runa_to_php(runa_ast: ASTNode) -> PhpNode:
    """Convert Runa AST to PHP AST."""
    converter = RunaToPhpConverter()
    return converter.convert(runa_ast)