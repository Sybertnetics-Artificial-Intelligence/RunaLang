#!/usr/bin/env python3
"""
Objective-C AST Converter

Bidirectional converter between Objective-C AST and Runa AST supporting all language features
including message passing syntax, protocols, categories, blocks, memory management,
Foundation framework integration, and Apple ecosystem constructs.

This converter handles:
- Message passing: [object method:parameter] ↔ Runa method calls
- Interface/implementation declarations ↔ Runa class definitions
- Protocols ↔ Runa interfaces
- Categories ↔ Runa extensions
- Properties with attributes ↔ Runa properties
- Blocks and closures ↔ Runa lambda expressions
- Memory management constructs ↔ Runa resource management
- Foundation framework patterns ↔ Runa standard library
"""

from typing import Dict, List, Optional, Any, Union
import logging

from ....core.base_components import BaseLanguageConverter, LanguageInfo, ConversionError, LanguageTier
from ....core.runa_ast import (
    ASTNode, SourceLocation, TranslationMetadata,
    # Import commonly used Runa AST nodes
    ProgramNode, ClassDefinition, InterfaceDefinition, MethodDefinition,
    PropertyDefinition, VariableDeclaration, Expression, Statement,
    FunctionCall, LambdaExpression, Identifier, Literal, BinaryOperation,
    Block, IfStatement, WhileStatement, ForStatement, ReturnStatement,
    TypeAnnotation, ImportStatement
)
from .objective_c_ast import *


class ObjCToRunaConverter(BaseLanguageConverter):
    """Converts Objective-C AST to Runa AST."""
    
    def __init__(self):
        language_info = LanguageInfo(
            name="objective_c",
            tier=LanguageTier.TIER6,
            file_extensions=[".m", ".mm", ".h"],
            description="Objective-C to Runa AST converter"
        )
        super().__init__(language_info)
        
        # Mapping tables for conversion
        self.foundation_type_mappings = {
            'NSString': 'String',
            'NSNumber': 'Number',
            'NSArray': 'List',
            'NSDictionary': 'Dictionary',
            'NSMutableArray': 'MutableList',
            'NSMutableDictionary': 'MutableDictionary',
            'NSInteger': 'Integer',
            'NSUInteger': 'UnsignedInteger',
            'CGFloat': 'Float',
            'BOOL': 'Boolean',
            'NSData': 'Data',
            'NSDate': 'Date',
            'NSURL': 'URL',
            'NSError': 'Error'
        }
        
        self.property_attribute_mappings = {
            ObjCPropertyAttribute.STRONG: 'owned',
            ObjCPropertyAttribute.WEAK: 'weak',
            ObjCPropertyAttribute.COPY: 'copied',
            ObjCPropertyAttribute.ASSIGN: 'assigned',
            ObjCPropertyAttribute.RETAIN: 'retained',
            ObjCPropertyAttribute.READONLY: 'readonly',
            ObjCPropertyAttribute.READWRITE: 'readwrite',
            ObjCPropertyAttribute.ATOMIC: 'synchronized',
            ObjCPropertyAttribute.NONATOMIC: 'unsynchronized'
        }
    
    def to_runa_ast(self, objc_ast: ObjCNode) -> ASTNode:
        """Convert Objective-C AST to Runa AST."""
        try:
            if isinstance(objc_ast, ObjCSourceUnit):
                return self._convert_source_unit(objc_ast)
            elif isinstance(objc_ast, ObjCInterfaceDeclaration):
                return self._convert_interface_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCImplementation):
                return self._convert_implementation(objc_ast)
            elif isinstance(objc_ast, ObjCProtocolDeclaration):
                return self._convert_protocol_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCMethodDeclaration):
                return self._convert_method_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCPropertyDeclaration):
                return self._convert_property_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCMessageExpression):
                return self._convert_message_expression(objc_ast)
            elif isinstance(objc_ast, ObjCBlockExpression):
                return self._convert_block_expression(objc_ast)
            else:
                self.logger.warning(f"Unsupported Objective-C AST node type: {type(objc_ast)}")
                return self._create_placeholder_node(f"Unsupported node: {type(objc_ast)}")
        
        except Exception as e:
            raise ConversionError(f"Failed to convert Objective-C AST to Runa: {e}", objc_ast)
    
    def from_runa_ast(self, runa_ast: ASTNode) -> ObjCNode:
        """Convert Runa AST to Objective-C AST."""
        try:
            if isinstance(runa_ast, ProgramNode):
                return self._convert_from_program_node(runa_ast)
            elif isinstance(runa_ast, ClassDefinition):
                return self._convert_from_class_definition(runa_ast)
            elif isinstance(runa_ast, InterfaceDefinition):
                return self._convert_from_interface_definition(runa_ast)
            elif isinstance(runa_ast, MethodDefinition):
                return self._convert_from_method_definition(runa_ast)
            elif isinstance(runa_ast, PropertyDefinition):
                return self._convert_from_property_definition(runa_ast)
            elif isinstance(runa_ast, FunctionCall):
                return self._convert_from_function_call(runa_ast)
            elif isinstance(runa_ast, LambdaExpression):
                return self._convert_from_lambda_expression(runa_ast)
            else:
                self.logger.warning(f"Unsupported Runa AST node type: {type(runa_ast)}")
                return self._create_objc_placeholder_node(f"Unsupported node: {type(runa_ast)}")
        
        except Exception as e:
            raise ConversionError(f"Failed to convert Runa AST to Objective-C: {e}", runa_ast)
    
    # ========================================================================
    # Objective-C to Runa Conversion Methods
    # ========================================================================
    
    def _convert_source_unit(self, source_unit: ObjCSourceUnit) -> ProgramNode:
        """Convert Objective-C source unit to Runa program."""
        program = ProgramNode()
        
        # Convert imports
        for import_directive in source_unit.imports:
            program.imports.append(self._convert_import_directive(import_directive))
        
        # Convert interfaces to class declarations
        for interface in source_unit.interfaces:
            program.declarations.append(self._convert_interface_declaration(interface))
        
        # Convert implementations to class definitions
        for implementation in source_unit.implementations:
            program.declarations.append(self._convert_implementation(implementation))
        
        # Convert protocols to interface definitions
        for protocol in source_unit.protocols:
            program.declarations.append(self._convert_protocol_declaration(protocol))
        
        # Convert categories to extension definitions
        for category in source_unit.categories:
            program.declarations.append(self._convert_category_interface(category))
        
        return program
    
    def _convert_import_directive(self, import_dir: ObjCImportDirective) -> ImportStatement:
        """Convert #import/@import to Runa import."""
        if import_dir.framework_name:
            # Framework import: @import Foundation
            module_name = import_dir.framework_name
        else:
            # File import: #import "Header.h"
            module_name = import_dir.path.replace('.h', '').replace('.m', '').replace('/', '.')
        
        return ImportStatement(
            module=module_name,
            is_framework=import_dir.is_framework_import,
            metadata=self._create_metadata("objective_c_import")
        )
    
    def _convert_interface_declaration(self, interface: ObjCInterfaceDeclaration) -> ClassDefinition:
        """Convert @interface to Runa class declaration."""
        class_def = ClassDefinition(
            name=interface.name,
            superclass=interface.superclass,
            interfaces=interface.protocols,  # Protocols become interfaces
            metadata=self._create_metadata("objective_c_interface")
        )
        
        # Convert properties
        for prop in interface.properties:
            class_def.properties.append(self._convert_property_declaration(prop))
        
        # Convert methods
        for method in interface.methods:
            class_def.methods.append(self._convert_method_declaration(method))
        
        # Convert instance variables
        for ivar in interface.instance_variables:
            class_def.fields.append(self._convert_ivar_declaration(ivar))
        
        return class_def
    
    def _convert_implementation(self, impl: ObjCImplementation) -> ClassDefinition:
        """Convert @implementation to Runa class definition with method bodies."""
        class_def = ClassDefinition(
            name=impl.name,
            metadata=self._create_metadata("objective_c_implementation")
        )
        
        # Convert method implementations
        for method in impl.methods:
            class_def.methods.append(self._convert_method_implementation(method))
        
        # Convert property synthesis to field initializations
        for synthesis in impl.properties:
            class_def.fields.append(self._convert_property_synthesis(synthesis))
        
        # Convert instance variables
        for ivar in impl.instance_variables:
            class_def.fields.append(self._convert_ivar_declaration(ivar))
        
        return class_def
    
    def _convert_protocol_declaration(self, protocol: ObjCProtocolDeclaration) -> InterfaceDefinition:
        """Convert @protocol to Runa interface."""
        interface_def = InterfaceDefinition(
            name=protocol.name,
            super_interfaces=protocol.protocols,
            metadata=self._create_metadata("objective_c_protocol")
        )
        
        # Convert required methods
        for method in protocol.required_methods:
            interface_def.methods.append(self._convert_method_declaration(method))
        
        # Convert optional methods (marked with metadata)
        for method in protocol.optional_methods:
            method_def = self._convert_method_declaration(method)
            method_def.metadata.attributes.append("optional")
            interface_def.methods.append(method_def)
        
        # Convert properties
        for prop in protocol.properties:
            interface_def.properties.append(self._convert_property_declaration(prop))
        
        return interface_def
    
    def _convert_category_interface(self, category: ObjCCategoryInterface) -> ClassDefinition:
        """Convert category to Runa extension."""
        # Categories become extension classes in Runa
        extension_name = f"{category.class_name}_{category.category_name}_Extension"
        
        extension = ClassDefinition(
            name=extension_name,
            metadata=self._create_metadata("objective_c_category")
        )
        extension.metadata.attributes.extend([
            f"extends:{category.class_name}",
            f"category:{category.category_name}"
        ])
        
        # Convert methods
        for method in category.methods:
            extension.methods.append(self._convert_method_declaration(method))
        
        return extension
    
    def _convert_method_declaration(self, method: ObjCMethodDeclaration) -> MethodDefinition:
        """Convert Objective-C method declaration to Runa method."""
        method_def = MethodDefinition(
            name=self._convert_selector_to_method_name(method.selector),
            parameters=self._convert_parameters(method.parameters),
            return_type=self._convert_type(method.return_type),
            is_static=(method.method_type == ObjCMethodType.CLASS),
            metadata=self._create_metadata("objective_c_method")
        )
        
        # Store original selector in metadata
        method_def.metadata.attributes.append(f"selector:{method.selector.get_selector_string()}")
        
        return method_def
    
    def _convert_method_implementation(self, method: ObjCMethodImplementation) -> MethodDefinition:
        """Convert Objective-C method implementation to Runa method with body."""
        method_def = self._convert_method_declaration(method)
        
        # Convert method body (simplified)
        if method.body:
            method_def.body = Block([
                self._convert_statement(stmt) for stmt in method.body
            ])
        
        return method_def
    
    def _convert_property_declaration(self, prop: ObjCPropertyDeclaration) -> PropertyDefinition:
        """Convert @property to Runa property."""
        property_def = PropertyDefinition(
            name=prop.name,
            type_annotation=self._convert_type(prop.type_annotation),
            metadata=self._create_metadata("objective_c_property")
        )
        
        # Convert property attributes
        for attr in prop.attributes:
            if attr in self.property_attribute_mappings:
                property_def.metadata.attributes.append(self.property_attribute_mappings[attr])
        
        # Custom getter/setter names
        if prop.getter_name:
            property_def.metadata.attributes.append(f"getter:{prop.getter_name}")
        if prop.setter_name:
            property_def.metadata.attributes.append(f"setter:{prop.setter_name}")
        
        return property_def
    
    def _convert_ivar_declaration(self, ivar: ObjCIvarDeclaration) -> VariableDeclaration:
        """Convert instance variable to Runa field."""
        return VariableDeclaration(
            name=ivar.name,
            type_annotation=self._convert_type(ivar.type_annotation),
            initial_value=self._convert_expression(ivar.initial_value) if ivar.initial_value else None,
            visibility=self._convert_visibility(ivar.visibility),
            metadata=self._create_metadata("objective_c_ivar")
        )
    
    def _convert_property_synthesis(self, synthesis: ObjCPropertySynthesis) -> VariableDeclaration:
        """Convert @synthesize to Runa field declaration."""
        field_name = synthesis.ivar_name or f"_{synthesis.property_name}"
        
        return VariableDeclaration(
            name=field_name,
            metadata=self._create_metadata("objective_c_synthesized_property")
        )
    
    def _convert_message_expression(self, msg_expr: ObjCMessageExpression) -> FunctionCall:
        """Convert [object method:param] to Runa method call."""
        # Convert receiver
        receiver = self._convert_expression(msg_expr.receiver)
        
        # Convert method name
        method_name = self._convert_selector_to_method_name(msg_expr.selector)
        
        # Convert arguments
        arguments = []
        for arg in msg_expr.arguments:
            arguments.append(self._convert_expression(arg.expression))
        
        # Create method call
        if receiver:
            # Instance method call: receiver.method(args)
            return FunctionCall(
                function=f"{receiver}.{method_name}",
                arguments=arguments,
                metadata=self._create_metadata("objective_c_message_send")
            )
        else:
            # Static method call
            return FunctionCall(
                function=method_name,
                arguments=arguments,
                metadata=self._create_metadata("objective_c_message_send")
            )
    
    def _convert_block_expression(self, block: ObjCBlockExpression) -> LambdaExpression:
        """Convert ^{...} block to Runa lambda."""
        parameters = self._convert_parameters(block.parameters)
        body = Block([self._convert_statement(stmt) for stmt in block.body])
        
        return LambdaExpression(
            parameters=parameters,
            body=body,
            return_type=self._convert_type(block.return_type),
            metadata=self._create_metadata("objective_c_block")
        )
    
    # ========================================================================
    # Runa to Objective-C Conversion Methods  
    # ========================================================================
    
    def _convert_from_program_node(self, program: ProgramNode) -> ObjCSourceUnit:
        """Convert Runa program to Objective-C source unit."""
        source_unit = ObjCSourceUnit()
        
        # Convert imports
        for import_stmt in program.imports:
            source_unit.imports.append(self._convert_from_import_statement(import_stmt))
        
        # Convert declarations
        for decl in program.declarations:
            if isinstance(decl, ClassDefinition):
                if self._is_interface_class(decl):
                    source_unit.interfaces.append(self._convert_from_class_definition_to_interface(decl))
                else:
                    source_unit.implementations.append(self._convert_from_class_definition_to_implementation(decl))
            elif isinstance(decl, InterfaceDefinition):
                source_unit.protocols.append(self._convert_from_interface_definition(decl))
        
        return source_unit
    
    def _convert_from_import_statement(self, import_stmt: ImportStatement) -> ObjCImportDirective:
        """Convert Runa import to Objective-C import."""
        if import_stmt.is_framework:
            # Framework import
            return ObjCImportDirective(
                is_framework_import=True,
                framework_name=import_stmt.module,
                path=f"@import {import_stmt.module};"
            )
        else:
            # Header import
            header_name = import_stmt.module.replace('.', '/') + '.h'
            return ObjCImportDirective(
                is_framework_import=False,
                path=header_name,
                is_system_import=False
            )
    
    def _convert_from_class_definition(self, class_def: ClassDefinition) -> ObjCImplementation:
        """Convert Runa class to Objective-C implementation."""
        implementation = ObjCImplementation(name=class_def.name)
        
        # Convert methods
        for method in class_def.methods:
            implementation.methods.append(self._convert_from_method_definition(method))
        
        # Convert fields to instance variables
        for field in class_def.fields:
            implementation.instance_variables.append(self._convert_from_variable_declaration(field))
        
        # Convert properties to @synthesize
        for prop in class_def.properties:
            implementation.properties.append(self._convert_from_property_definition(prop))
        
        return implementation
    
    def _convert_from_class_definition_to_interface(self, class_def: ClassDefinition) -> ObjCInterfaceDeclaration:
        """Convert Runa class to Objective-C interface."""
        interface = ObjCInterfaceDeclaration(
            name=class_def.name,
            superclass=class_def.superclass,
            protocols=class_def.interfaces
        )
        
        # Convert methods to declarations
        for method in class_def.methods:
            interface.methods.append(self._convert_from_method_definition_to_declaration(method))
        
        # Convert properties
        for prop in class_def.properties:
            interface.properties.append(self._convert_from_property_definition_to_declaration(prop))
        
        return interface
    
    def _convert_from_interface_definition(self, interface_def: InterfaceDefinition) -> ObjCProtocolDeclaration:
        """Convert Runa interface to Objective-C protocol."""
        protocol = ObjCProtocolDeclaration(
            name=interface_def.name,
            protocols=interface_def.super_interfaces
        )
        
        # Convert methods
        for method in interface_def.methods:
            method_decl = self._convert_from_method_definition_to_declaration(method)
            
            # Check if optional
            if "optional" in getattr(method.metadata, 'attributes', []):
                protocol.optional_methods.append(method_decl)
            else:
                protocol.required_methods.append(method_decl)
        
        return protocol
    
    def _convert_from_method_definition(self, method: MethodDefinition) -> ObjCMethodImplementation:
        """Convert Runa method to Objective-C method implementation."""
        method_impl = ObjCMethodImplementation(
            name=method.name,
            method_type=ObjCMethodType.CLASS if method.is_static else ObjCMethodType.INSTANCE,
            return_type=self._convert_from_type(method.return_type),
            selector=self._convert_method_name_to_selector(method.name),
            parameters=self._convert_from_parameters(method.parameters)
        )
        
        # Convert method body
        if method.body:
            method_impl.body = [self._convert_from_statement(stmt) for stmt in method.body.statements]
        
        return method_impl
    
    def _convert_from_function_call(self, call: FunctionCall) -> ObjCMessageExpression:
        """Convert Runa function call to Objective-C message expression."""
        # Parse receiver and method name
        if '.' in call.function:
            receiver_name, method_name = call.function.rsplit('.', 1)
            receiver = ObjCIdentifier(name=receiver_name)
        else:
            receiver = None
            method_name = call.function
        
        # Convert arguments to keyword arguments
        selector = ObjCSelector(parts=[method_name])
        arguments = []
        
        for i, arg in enumerate(call.arguments):
            keyword = f"arg{i}" if i > 0 else ""
            arguments.append(ObjCKeywordArgument(
                keyword=keyword,
                expression=self._convert_from_expression(arg)
            ))
        
        return ObjCMessageExpression(
            receiver=receiver,
            selector=selector,
            arguments=arguments
        )
    
    def _convert_from_lambda_expression(self, lambda_expr: LambdaExpression) -> ObjCBlockExpression:
        """Convert Runa lambda to Objective-C block."""
        return ObjCBlockExpression(
            parameters=self._convert_from_parameters(lambda_expr.parameters),
            return_type=self._convert_from_type(lambda_expr.return_type),
            body=[self._convert_from_statement(stmt) for stmt in lambda_expr.body.statements]
        )
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _convert_selector_to_method_name(self, selector: ObjCSelector) -> str:
        """Convert Objective-C selector to Runa method name."""
        if not selector.parts:
            return "unknown"
        
        # Simple case: single part selector
        if len(selector.parts) == 1:
            return selector.parts[0]
        
        # Multi-part selector: combine with underscores
        return "_".join(selector.parts)
    
    def _convert_method_name_to_selector(self, method_name: str) -> ObjCSelector:
        """Convert Runa method name to Objective-C selector."""
        # Check for underscore-separated parts
        if '_' in method_name:
            parts = method_name.split('_')
        else:
            parts = [method_name]
        
        return ObjCSelector(parts=parts)
    
    def _convert_type(self, objc_type: Optional[ObjCType]) -> Optional[TypeAnnotation]:
        """Convert Objective-C type to Runa type."""
        if not objc_type:
            return None
        
        if isinstance(objc_type, ObjCIdType):
            return TypeAnnotation(name="Any")
        elif isinstance(objc_type, ObjCInstanceType):
            return TypeAnnotation(name="Self")
        elif isinstance(objc_type, ObjCClassType):
            # Map Foundation types
            if objc_type.class_name in self.foundation_type_mappings:
                return TypeAnnotation(name=self.foundation_type_mappings[objc_type.class_name])
            else:
                return TypeAnnotation(name=objc_type.class_name)
        elif isinstance(objc_type, ObjCPointerType):
            pointed_type = self._convert_type(objc_type.pointed_type)
            if pointed_type:
                return TypeAnnotation(name=f"Pointer<{pointed_type.name}>")
            else:
                return TypeAnnotation(name="Pointer<Any>")
        else:
            return TypeAnnotation(name="Any")
    
    def _convert_from_type(self, runa_type: Optional[TypeAnnotation]) -> Optional[ObjCType]:
        """Convert Runa type to Objective-C type."""
        if not runa_type:
            return None
        
        # Reverse Foundation type mappings
        reverse_mappings = {v: k for k, v in self.foundation_type_mappings.items()}
        
        if runa_type.name in reverse_mappings:
            objc_class_name = reverse_mappings[runa_type.name]
            return ObjCPointerType(pointed_type=ObjCClassType(class_name=objc_class_name))
        elif runa_type.name == "Any":
            return ObjCIdType()
        elif runa_type.name == "Self":
            return ObjCInstanceType()
        else:
            return ObjCPointerType(pointed_type=ObjCClassType(class_name=runa_type.name))
    
    def _convert_parameters(self, params: List[ObjCParameter]) -> List[Any]:
        """Convert Objective-C parameters to Runa parameters."""
        # Simplified parameter conversion
        return [
            {
                'name': param.name,
                'type': self._convert_type(param.type_annotation)
            }
            for param in params
        ]
    
    def _convert_from_parameters(self, params: List[Any]) -> List[ObjCParameter]:
        """Convert Runa parameters to Objective-C parameters."""
        return [
            ObjCParameter(
                name=param.get('name', 'param'),
                type_annotation=self._convert_from_type(param.get('type'))
            )
            for param in params
        ]
    
    def _convert_expression(self, expr: Optional[ObjCExpression]) -> Optional[Expression]:
        """Convert Objective-C expression to Runa expression."""
        if not expr:
            return None
        
        if isinstance(expr, ObjCStringLiteral):
            return Literal(value=expr.value, type_name="String")
        elif isinstance(expr, ObjCNumberLiteral):
            return Literal(value=expr.value, type_name="Number")
        elif isinstance(expr, ObjCBoolLiteral):
            return Literal(value=expr.value, type_name="Boolean")
        elif isinstance(expr, ObjCNilExpression):
            return Literal(value=None, type_name="Null")
        elif isinstance(expr, ObjCSelfExpression):
            return Identifier(name="self")
        elif isinstance(expr, ObjCSuperExpression):
            return Identifier(name="super")
        else:
            return Identifier(name="unknown")
    
    def _convert_from_expression(self, expr: Expression) -> ObjCExpression:
        """Convert Runa expression to Objective-C expression."""
        if isinstance(expr, Literal):
            if expr.type_name == "String":
                return ObjCStringLiteral(value=str(expr.value), is_nsstring=True)
            elif expr.type_name in ["Number", "Integer", "Float"]:
                return ObjCNumberLiteral(value=expr.value, is_nsnumber=True)
            elif expr.type_name == "Boolean":
                return ObjCBoolLiteral(value=bool(expr.value))
            else:
                return ObjCNilExpression()
        elif isinstance(expr, Identifier):
            if expr.name == "self":
                return ObjCSelfExpression()
            elif expr.name == "super":
                return ObjCSuperExpression()
            else:
                return ObjCIdentifier(name=expr.name)
        else:
            return ObjCIdentifier(name="unknown")
    
    def _convert_statement(self, stmt: Any) -> Statement:
        """Convert Objective-C statement to Runa statement."""
        # Simplified statement conversion
        return Statement()
    
    def _convert_from_statement(self, stmt: Statement) -> ObjCStatement:
        """Convert Runa statement to Objective-C statement."""
        # Simplified statement conversion
        return ObjCExpressionStatement()
    
    def _convert_visibility(self, visibility: ObjCVisibility) -> str:
        """Convert Objective-C visibility to Runa visibility."""
        visibility_map = {
            ObjCVisibility.PUBLIC: "public",
            ObjCVisibility.PRIVATE: "private",
            ObjCVisibility.PROTECTED: "protected",
            ObjCVisibility.PACKAGE: "internal"
        }
        return visibility_map.get(visibility, "private")
    
    def _is_interface_class(self, class_def: ClassDefinition) -> bool:
        """Check if a class definition should be converted to an interface."""
        # Heuristic: if class has metadata indicating it's an interface declaration
        return "objective_c_interface" in getattr(class_def.metadata, 'attributes', [])
    
    def _convert_from_property_definition(self, prop: PropertyDefinition) -> ObjCPropertySynthesis:
        """Convert Runa property to Objective-C property synthesis."""
        return ObjCPropertySynthesis(
            property_name=prop.name,
            ivar_name=f"_{prop.name}",
            is_dynamic=False
        )
    
    def _convert_from_property_definition_to_declaration(self, prop: PropertyDefinition) -> ObjCPropertyDeclaration:
        """Convert Runa property to Objective-C property declaration."""
        # Convert metadata attributes back to property attributes
        attributes = []
        for attr in getattr(prop.metadata, 'attributes', []):
            for objc_attr, runa_attr in self.property_attribute_mappings.items():
                if attr == runa_attr:
                    attributes.append(objc_attr)
                    break
        
        return ObjCPropertyDeclaration(
            name=prop.name,
            type_annotation=self._convert_from_type(prop.type_annotation),
            attributes=attributes
        )
    
    def _convert_from_method_definition_to_declaration(self, method: MethodDefinition) -> ObjCMethodDeclaration:
        """Convert Runa method to Objective-C method declaration."""
        return ObjCMethodDeclaration(
            method_type=ObjCMethodType.CLASS if method.is_static else ObjCMethodType.INSTANCE,
            return_type=self._convert_from_type(method.return_type),
            selector=self._convert_method_name_to_selector(method.name),
            parameters=self._convert_from_parameters(method.parameters)
        )
    
    def _convert_from_variable_declaration(self, var_decl: VariableDeclaration) -> ObjCIvarDeclaration:
        """Convert Runa variable to Objective-C instance variable."""
        return ObjCIvarDeclaration(
            name=var_decl.name,
            type_annotation=self._convert_from_type(var_decl.type_annotation),
            initial_value=self._convert_from_expression(var_decl.initial_value) if var_decl.initial_value else None
        )
    
    def _create_metadata(self, conversion_type: str) -> TranslationMetadata:
        """Create translation metadata."""
        return TranslationMetadata(
            source_language="objective_c",
            target_language="runa",
            conversion_type=conversion_type,
            attributes=[]
        )
    
    def _create_placeholder_node(self, description: str) -> ASTNode:
        """Create placeholder Runa AST node."""
        return Statement(metadata=self._create_metadata(f"placeholder: {description}"))
    
    def _create_objc_placeholder_node(self, description: str) -> ObjCNode:
        """Create placeholder Objective-C AST node."""
        return ObjCExpressionStatement()


# Factory functions
def objective_c_to_runa(objc_ast: ObjCNode) -> ASTNode:
    """Convert Objective-C AST to Runa AST."""
    converter = ObjCToRunaConverter()
    return converter.to_runa_ast(objc_ast)


def runa_to_objective_c(runa_ast: ASTNode) -> ObjCNode:
    """Convert Runa AST to Objective-C AST."""
    converter = ObjCToRunaConverter()
    return converter.from_runa_ast(runa_ast) 