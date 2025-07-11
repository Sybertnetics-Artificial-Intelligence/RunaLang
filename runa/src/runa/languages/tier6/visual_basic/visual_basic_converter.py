#!/usr/bin/env python3
"""
Visual Basic Converter Implementation

Bidirectional converter between Runa AST and Visual Basic AST with comprehensive
type mappings, .NET Framework integration, and Visual Basic-specific constructs.
"""

from typing import List, Dict, Optional, Any, Union
import logging
from dataclasses import dataclass

from .visual_basic_ast import *
from ....core.runa_ast import *
from ....core.semantic_analyzer import TypeInformation
from ....core.error_handler import ErrorHandler, ErrorType
from ....core.translation_context import TranslationContext

# Type mapping configurations
VB_TO_RUNA_TYPE_MAP = {
    # Primitive types
    'Integer': 'Integer',
    'Long': 'Long',
    'Short': 'Short',
    'Byte': 'Byte',
    'Single': 'Float',
    'Double': 'Double',
    'Decimal': 'Decimal',
    'Boolean': 'Boolean',
    'Char': 'Character',
    'String': 'String',
    'Date': 'DateTime',
    'Object': 'Any',
    
    # .NET Framework types
    'System.String': 'String',
    'System.Int32': 'Integer',
    'System.Int64': 'Long',
    'System.Boolean': 'Boolean',
    'System.Double': 'Double',
    'System.DateTime': 'DateTime',
    'System.Object': 'Any',
    'System.Collections.Generic.List': 'List',
    'System.Collections.Generic.Dictionary': 'Dictionary',
    
    # Collections
    'List(Of T)': 'List<T>',
    'Dictionary(Of K, V)': 'Dictionary<K, V>',
    'Array': 'Array',
    
    # Special types
    'Nothing': 'None',
    'DBNull': 'None',
}

RUNA_TO_VB_TYPE_MAP = {v: k for k, v in VB_TO_RUNA_TYPE_MAP.items()}
RUNA_TO_VB_TYPE_MAP.update({
    'None': 'Nothing',
    'List': 'List(Of T)',
    'Dictionary': 'Dictionary(Of K, V)',
    'Character': 'Char',
})

# Access modifier mappings
VB_TO_RUNA_ACCESS = {
    VBAccessModifier.PUBLIC: AccessModifier.PUBLIC,
    VBAccessModifier.PRIVATE: AccessModifier.PRIVATE,
    VBAccessModifier.PROTECTED: AccessModifier.PROTECTED,
    VBAccessModifier.FRIEND: AccessModifier.INTERNAL,
    VBAccessModifier.PROTECTED_FRIEND: AccessModifier.PROTECTED_INTERNAL,
}

RUNA_TO_VB_ACCESS = {v: k for k, v in VB_TO_RUNA_ACCESS.items()}

# Operator mappings
VB_TO_RUNA_OPERATORS = {
    VBOperator.PLUS: BinaryOperator.ADD,
    VBOperator.MINUS: BinaryOperator.SUBTRACT,
    VBOperator.MULTIPLY: BinaryOperator.MULTIPLY,
    VBOperator.DIVIDE: BinaryOperator.DIVIDE,
    VBOperator.MOD: BinaryOperator.MODULO,
    VBOperator.EXPONENT: BinaryOperator.POWER,
    VBOperator.EQUALS: BinaryOperator.EQUALS,
    VBOperator.NOT_EQUALS: BinaryOperator.NOT_EQUALS,
    VBOperator.LESS_THAN: BinaryOperator.LESS_THAN,
    VBOperator.LESS_EQUAL: BinaryOperator.LESS_EQUAL,
    VBOperator.GREATER_THAN: BinaryOperator.GREATER_THAN,
    VBOperator.GREATER_EQUAL: BinaryOperator.GREATER_EQUAL,
    VBOperator.AND: BinaryOperator.LOGICAL_AND,
    VBOperator.OR: BinaryOperator.LOGICAL_OR,
    VBOperator.ANDALSO: BinaryOperator.LOGICAL_AND,
    VBOperator.ORELSE: BinaryOperator.LOGICAL_OR,
    VBOperator.CONCATENATE: BinaryOperator.STRING_CONCAT,
}

RUNA_TO_VB_OPERATORS = {v: k for k, v in VB_TO_RUNA_OPERATORS.items()}

class VBToRunaConverter:
    """Converts Visual Basic AST to Runa AST."""
    
    def __init__(self, error_handler: ErrorHandler, context: TranslationContext):
        self.error_handler = error_handler
        self.context = context
        self.logger = logging.getLogger(__name__)
    
    def convert(self, vb_node: VBNode) -> RunaNode:
        """Convert VB AST node to Runa AST node."""
        try:
            return vb_node.accept(self)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.CONVERSION_ERROR,
                f"Failed to convert VB node: {e}",
                getattr(vb_node, 'source_location', SourceLocation()).line,
                getattr(vb_node, 'source_location', SourceLocation()).column
            )
            return EmptyStatement()
    
    # Visitor methods for VB AST nodes
    def visit_vb_source_unit(self, node: VBSourceUnit) -> CompilationUnit:
        """Convert VB source unit to Runa compilation unit."""
        compilation_unit = CompilationUnit()
        
        # Convert imports
        for imports in node.imports_statements:
            import_stmt = self.convert(imports)
            if isinstance(import_stmt, ImportStatement):
                compilation_unit.imports.append(import_stmt)
        
        # Convert namespaces and types
        for namespace in node.namespace_declarations:
            ns_decl = self.convert(namespace)
            if isinstance(ns_decl, NamespaceDeclaration):
                compilation_unit.declarations.append(ns_decl)
        
        for type_decl in node.type_declarations:
            decl = self.convert(type_decl)
            compilation_unit.declarations.append(decl)
        
        return compilation_unit
    
    def visit_vb_namespace(self, node: VBNamespace) -> NamespaceDeclaration:
        """Convert VB namespace to Runa namespace."""
        namespace = NamespaceDeclaration(name=node.name)
        
        for type_decl in node.type_declarations:
            decl = self.convert(type_decl)
            namespace.declarations.append(decl)
        
        return namespace
    
    def visit_vb_imports_statement(self, node: VBImportsStatement) -> ImportStatement:
        """Convert VB imports to Runa import."""
        return ImportStatement(
            module_path=node.namespace,
            alias=node.alias
        )
    
    def visit_vb_class_declaration(self, node: VBClassDeclaration) -> ClassDeclaration:
        """Convert VB class to Runa class."""
        class_decl = ClassDeclaration(
            name=node.name,
            access_modifier=VB_TO_RUNA_ACCESS.get(node.access_modifier, AccessModifier.PUBLIC)
        )
        
        # Convert inheritance
        if node.inherits_from:
            class_decl.base_class = node.inherits_from
        
        class_decl.interfaces = node.implements.copy()
        
        # Convert members
        for member in node.members:
            member_decl = self.convert(member)
            if isinstance(member_decl, (MethodDeclaration, PropertyDeclaration, FieldDeclaration)):
                class_decl.members.append(member_decl)
        
        return class_decl
    
    def visit_vb_module_declaration(self, node: VBModuleDeclaration) -> ClassDeclaration:
        """Convert VB module to Runa static class."""
        class_decl = ClassDeclaration(
            name=node.name,
            access_modifier=VB_TO_RUNA_ACCESS.get(node.access_modifier, AccessModifier.PUBLIC),
            is_static=True
        )
        
        # Convert members
        for member in node.members:
            member_decl = self.convert(member)
            if isinstance(member_decl, (MethodDeclaration, PropertyDeclaration, FieldDeclaration)):
                class_decl.members.append(member_decl)
        
        return class_decl
    
    def visit_vb_method_declaration(self, node: VBMethodDeclaration) -> MethodDeclaration:
        """Convert VB method to Runa method."""
        method = MethodDeclaration(
            name=node.name,
            access_modifier=VB_TO_RUNA_ACCESS.get(node.access_modifier, AccessModifier.PUBLIC),
            is_static=VBMemberModifier.SHARED in node.member_modifiers
        )
        
        # Convert parameters
        for param in node.parameters:
            runa_param = self.convert(param)
            if isinstance(runa_param, Parameter):
                method.parameters.append(runa_param)
        
        # Convert return type
        if node.return_type and node.is_function:
            method.return_type = self._convert_type(node.return_type)
        
        # Convert body
        for stmt in node.body:
            runa_stmt = self.convert(stmt)
            method.body.statements.append(runa_stmt)
        
        return method
    
    def visit_vb_property_declaration(self, node: VBPropertyDeclaration) -> PropertyDeclaration:
        """Convert VB property to Runa property."""
        prop = PropertyDeclaration(
            name=node.name,
            access_modifier=VB_TO_RUNA_ACCESS.get(node.access_modifier, AccessModifier.PUBLIC),
            property_type=self._convert_type(node.property_type)
        )
        
        # Convert getter
        if node.getter:
            prop.getter = self._convert_accessor(node.getter)
        
        # Convert setter
        if node.setter:
            prop.setter = self._convert_accessor(node.setter)
        
        return prop
    
    def visit_vb_field_declaration(self, node: VBFieldDeclaration) -> FieldDeclaration:
        """Convert VB field to Runa field."""
        field = FieldDeclaration(
            name=node.name,
            access_modifier=VB_TO_RUNA_ACCESS.get(node.access_modifier, AccessModifier.PUBLIC),
            field_type=self._convert_type(node.field_type),
            is_static=VBMemberModifier.SHARED in node.member_modifiers,
            is_readonly=VBMemberModifier.READONLY in node.member_modifiers
        )
        
        if node.initial_value:
            field.initializer = self.convert(node.initial_value)
        
        return field
    
    def visit_vb_binary_expression(self, node: VBBinaryExpression) -> BinaryExpression:
        """Convert VB binary expression to Runa binary expression."""
        return BinaryExpression(
            left=self.convert(node.left),
            operator=VB_TO_RUNA_OPERATORS.get(node.operator, BinaryOperator.ADD),
            right=self.convert(node.right)
        )
    
    def visit_vb_literal_expression(self, node: VBLiteralExpression) -> LiteralExpression:
        """Convert VB literal to Runa literal."""
        value = node.value
        
        # Handle VB-specific literals
        if node.literal_type == "Nothing":
            value = None
        elif node.literal_type == "Boolean":
            value = str(value).lower() == "true"
        
        return LiteralExpression(value=value)
    
    def visit_vb_identifier_expression(self, node: VBIdentifierExpression) -> IdentifierExpression:
        """Convert VB identifier to Runa identifier."""
        return IdentifierExpression(name=node.name)
    
    def _convert_type(self, vb_type: VBType) -> Optional[TypeExpression]:
        """Convert VB type to Runa type."""
        if isinstance(vb_type, VBNamedType):
            runa_type_name = VB_TO_RUNA_TYPE_MAP.get(vb_type.name, vb_type.name)
            return TypeExpression(name=runa_type_name)
        elif isinstance(vb_type, VBArrayType):
            element_type = self._convert_type(vb_type.element_type)
            return ArrayTypeExpression(element_type=element_type, dimensions=vb_type.rank)
        return None
    
    def _convert_accessor(self, accessor: VBAccessorDeclaration) -> AccessorDeclaration:
        """Convert VB accessor to Runa accessor."""
        runa_accessor = AccessorDeclaration(
            is_getter=accessor.is_getter,
            access_modifier=VB_TO_RUNA_ACCESS.get(accessor.access_modifier, AccessModifier.PUBLIC)
        )
        
        for stmt in accessor.body:
            runa_stmt = self.convert(stmt)
            runa_accessor.body.statements.append(runa_stmt)
        
        return runa_accessor

class RunaToVBConverter:
    """Converts Runa AST to Visual Basic AST."""
    
    def __init__(self, error_handler: ErrorHandler, context: TranslationContext):
        self.error_handler = error_handler
        self.context = context
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: RunaNode) -> VBNode:
        """Convert Runa AST node to VB AST node."""
        try:
            return self._convert_node(runa_node)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.CONVERSION_ERROR,
                f"Failed to convert Runa node: {e}",
                getattr(runa_node, 'source_location', SourceLocation()).line,
                getattr(runa_node, 'source_location', SourceLocation()).column
            )
            return VBComment(text=f"// Conversion error: {e}")
    
    def _convert_node(self, node: RunaNode) -> VBNode:
        """Convert specific Runa node types."""
        if isinstance(node, CompilationUnit):
            return self._convert_compilation_unit(node)
        elif isinstance(node, ClassDeclaration):
            return self._convert_class_declaration(node)
        elif isinstance(node, MethodDeclaration):
            return self._convert_method_declaration(node)
        elif isinstance(node, PropertyDeclaration):
            return self._convert_property_declaration(node)
        elif isinstance(node, FieldDeclaration):
            return self._convert_field_declaration(node)
        elif isinstance(node, BinaryExpression):
            return self._convert_binary_expression(node)
        elif isinstance(node, LiteralExpression):
            return self._convert_literal_expression(node)
        elif isinstance(node, IdentifierExpression):
            return self._convert_identifier_expression(node)
        else:
            return VBComment(text=f"' Unsupported node type: {type(node).__name__}")
    
    def _convert_compilation_unit(self, node: CompilationUnit) -> VBSourceUnit:
        """Convert Runa compilation unit to VB source unit."""
        source_unit = VBSourceUnit()
        
        # Convert imports
        for import_stmt in node.imports:
            vb_import = VBImportsStatement(
                namespace=import_stmt.module_path,
                alias=import_stmt.alias
            )
            source_unit.imports_statements.append(vb_import)
        
        # Convert declarations
        for decl in node.declarations:
            if isinstance(decl, NamespaceDeclaration):
                vb_namespace = self._convert_namespace_declaration(decl)
                source_unit.namespace_declarations.append(vb_namespace)
            elif isinstance(decl, ClassDeclaration):
                vb_class = self._convert_class_declaration(decl)
                source_unit.type_declarations.append(vb_class)
        
        return source_unit
    
    def _convert_namespace_declaration(self, node: NamespaceDeclaration) -> VBNamespace:
        """Convert Runa namespace to VB namespace."""
        namespace = VBNamespace(name=node.name)
        
        for decl in node.declarations:
            if isinstance(decl, ClassDeclaration):
                vb_class = self._convert_class_declaration(decl)
                namespace.type_declarations.append(vb_class)
        
        return namespace
    
    def _convert_class_declaration(self, node: ClassDeclaration) -> Union[VBClassDeclaration, VBModuleDeclaration]:
        """Convert Runa class to VB class or module."""
        if node.is_static:
            # Convert to VB Module
            module = VBModuleDeclaration(
                name=node.name,
                access_modifier=RUNA_TO_VB_ACCESS.get(node.access_modifier, VBAccessModifier.PUBLIC)
            )
            
            for member in node.members:
                vb_member = self._convert_node(member)
                if isinstance(vb_member, VBMemberDeclaration):
                    module.members.append(vb_member)
            
            return module
        else:
            # Convert to VB Class
            class_decl = VBClassDeclaration(
                name=node.name,
                access_modifier=RUNA_TO_VB_ACCESS.get(node.access_modifier, VBAccessModifier.PUBLIC)
            )
            
            if node.base_class:
                class_decl.inherits_from = node.base_class
            
            class_decl.implements = node.interfaces.copy()
            
            for member in node.members:
                vb_member = self._convert_node(member)
                if isinstance(vb_member, VBMemberDeclaration):
                    class_decl.members.append(vb_member)
            
            return class_decl
    
    def _convert_method_declaration(self, node: MethodDeclaration) -> VBMethodDeclaration:
        """Convert Runa method to VB method."""
        method = VBMethodDeclaration(
            name=node.name,
            access_modifier=RUNA_TO_VB_ACCESS.get(node.access_modifier, VBAccessModifier.PUBLIC),
            is_function=node.return_type is not None
        )
        
        # Add Shared modifier if static
        if node.is_static:
            method.member_modifiers.append(VBMemberModifier.SHARED)
        
        # Convert parameters
        for param in node.parameters:
            vb_param = self._convert_parameter(param)
            method.parameters.append(vb_param)
        
        # Convert return type
        if node.return_type:
            method.return_type = self._convert_type_to_vb(node.return_type)
        
        # Convert body
        for stmt in node.body.statements:
            vb_stmt = self._convert_node(stmt)
            if isinstance(vb_stmt, VBStatement):
                method.body.append(vb_stmt)
        
        return method
    
    def _convert_property_declaration(self, node: PropertyDeclaration) -> VBPropertyDeclaration:
        """Convert Runa property to VB property."""
        prop = VBPropertyDeclaration(
            name=node.name,
            access_modifier=RUNA_TO_VB_ACCESS.get(node.access_modifier, VBAccessModifier.PUBLIC),
            property_type=self._convert_type_to_vb(node.property_type)
        )
        
        # Convert getter
        if node.getter:
            prop.getter = self._convert_accessor_to_vb(node.getter)
        
        # Convert setter
        if node.setter:
            prop.setter = self._convert_accessor_to_vb(node.setter)
        
        return prop
    
    def _convert_field_declaration(self, node: FieldDeclaration) -> VBFieldDeclaration:
        """Convert Runa field to VB field."""
        field = VBFieldDeclaration(
            name=node.name,
            access_modifier=RUNA_TO_VB_ACCESS.get(node.access_modifier, VBAccessModifier.PUBLIC),
            field_type=self._convert_type_to_vb(node.field_type)
        )
        
        # Add modifiers
        if node.is_static:
            field.member_modifiers.append(VBMemberModifier.SHARED)
        if node.is_readonly:
            field.member_modifiers.append(VBMemberModifier.READONLY)
        
        # Convert initializer
        if node.initializer:
            field.initial_value = self._convert_node(node.initializer)
        
        return field
    
    def _convert_binary_expression(self, node: BinaryExpression) -> VBBinaryExpression:
        """Convert Runa binary expression to VB binary expression."""
        return VBBinaryExpression(
            left=self._convert_node(node.left),
            operator=RUNA_TO_VB_OPERATORS.get(node.operator, VBOperator.PLUS),
            right=self._convert_node(node.right)
        )
    
    def _convert_literal_expression(self, node: LiteralExpression) -> VBLiteralExpression:
        """Convert Runa literal to VB literal."""
        value = node.value
        literal_type = "Object"
        
        if value is None:
            literal_type = "Nothing"
        elif isinstance(value, bool):
            literal_type = "Boolean"
            value = "True" if value else "False"
        elif isinstance(value, int):
            literal_type = "Integer"
        elif isinstance(value, float):
            literal_type = "Double"
        elif isinstance(value, str):
            literal_type = "String"
        
        return VBLiteralExpression(value=value, literal_type=literal_type)
    
    def _convert_identifier_expression(self, node: IdentifierExpression) -> VBIdentifierExpression:
        """Convert Runa identifier to VB identifier."""
        return VBIdentifierExpression(name=node.name)
    
    def _convert_parameter(self, param: Parameter) -> VBParameter:
        """Convert Runa parameter to VB parameter."""
        return VBParameter(
            name=param.name,
            parameter_type=self._convert_type_to_vb(param.parameter_type),
            is_byref=param.is_ref,
            is_optional=param.default_value is not None,
            default_value=self._convert_node(param.default_value) if param.default_value else None
        )
    
    def _convert_type_to_vb(self, runa_type: Optional[TypeExpression]) -> Optional[VBType]:
        """Convert Runa type to VB type."""
        if not runa_type:
            return None
        
        if isinstance(runa_type, TypeExpression):
            vb_type_name = RUNA_TO_VB_TYPE_MAP.get(runa_type.name, runa_type.name)
            return VBNamedType(name=vb_type_name)
        elif isinstance(runa_type, ArrayTypeExpression):
            element_type = self._convert_type_to_vb(runa_type.element_type)
            return VBArrayType(element_type=element_type, rank=runa_type.dimensions or 1)
        
        return VBNamedType(name="Object")
    
    def _convert_accessor_to_vb(self, accessor: AccessorDeclaration) -> VBAccessorDeclaration:
        """Convert Runa accessor to VB accessor."""
        vb_accessor = VBAccessorDeclaration(
            is_getter=accessor.is_getter,
            access_modifier=RUNA_TO_VB_ACCESS.get(accessor.access_modifier)
        )
        
        for stmt in accessor.body.statements:
            vb_stmt = self._convert_node(stmt)
            if isinstance(vb_stmt, VBStatement):
                vb_accessor.body.append(vb_stmt)
        
        return vb_accessor

def convert_vb_to_runa(vb_ast: VBNode, error_handler: ErrorHandler, 
                      context: TranslationContext) -> RunaNode:
    """Convert Visual Basic AST to Runa AST."""
    converter = VBToRunaConverter(error_handler, context)
    return converter.convert(vb_ast)

def convert_runa_to_vb(runa_ast: RunaNode, error_handler: ErrorHandler,
                      context: TranslationContext) -> VBNode:
    """Convert Runa AST to Visual Basic AST.""" 
    converter = RunaToVBConverter(error_handler, context)
    return converter.convert(runa_ast) 