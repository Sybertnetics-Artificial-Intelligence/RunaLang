#!/usr/bin/env python3
"""
TypeScript ↔ Runa Bidirectional Converter

Converts between TypeScript AST and Runa AST in both directions,
preserving type information and enabling round-trip translation.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .ts_ast import *
from ....core.runa_ast import *


class TSToRunaConverter:
    """Converts TypeScript AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.scope_stack = []
        self.converted_functions = {}
    
    def convert(self, ts_ast: TSProgram) -> Program:
        """Convert TypeScript program to Runa program."""
        statements = []
        
        for stmt in ts_ast.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements)
    
    def convert_statement(self, stmt: TSNode) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert TypeScript statement to Runa statement."""
        if isinstance(stmt, TSVariableDeclaration):
            return self._convert_variable_declaration(stmt)
        
        elif isinstance(stmt, TSFunctionDeclaration):
            return self._convert_function_declaration(stmt)
        
        elif isinstance(stmt, TSInterfaceDeclaration):
            return self._convert_interface_declaration(stmt)
        
        elif isinstance(stmt, TSTypeAliasDeclaration):
            return self._convert_type_alias_declaration(stmt)
        
        elif isinstance(stmt, TSEnumDeclaration):
            return self._convert_enum_declaration(stmt)
        
        elif isinstance(stmt, TSClassDeclaration):
            return self._convert_class_declaration(stmt)
        
        elif isinstance(stmt, TSNamespaceDeclaration):
            return self._convert_namespace_declaration(stmt)
        
        elif isinstance(stmt, TSBlockStatement):
            return self._convert_block_statement(stmt)
        
        # Handle expressions as statements
        elif isinstance(stmt, TSNode):
            expr = self.convert_expression(stmt)
            if expr:
                return RunaExpressionStatement(expr)
        
        return None
    
    def convert_expression(self, expr: TSNode) -> Optional[RunaExpression]:
        """Convert TypeScript expression to Runa expression."""
        if isinstance(expr, TSLiteral):
            return self._convert_literal(expr)
        
        elif isinstance(expr, TSIdentifier):
            return self._convert_identifier(expr)
        
        elif isinstance(expr, TSTypeAssertion):
            return self._convert_type_assertion(expr)
        
        # Add more expression conversions as needed
        return None
    
    def convert_type(self, ts_type: TSType) -> RunaType:
        """Convert TypeScript type to Runa type."""
        if isinstance(ts_type, TSTypeReference):
            return self._convert_type_reference(ts_type)
        
        elif isinstance(ts_type, TSUnionType):
            return self._convert_union_type(ts_type)
        
        elif isinstance(ts_type, TSIntersectionType):
            return self._convert_intersection_type(ts_type)
        
        elif isinstance(ts_type, TSArrayType):
            return self._convert_array_type(ts_type)
        
        elif isinstance(ts_type, TSTupleType):
            return self._convert_tuple_type(ts_type)
        
        elif isinstance(ts_type, TSFunctionType):
            return self._convert_function_type(ts_type)
        
        elif isinstance(ts_type, TSTypeLiteral):
            return self._convert_type_literal(ts_type)
        
        # Default to Any type
        return RunaType("Any")
    
    def _convert_variable_declaration(self, stmt: TSVariableDeclaration) -> List[RunaStatement]:
        """Convert variable declaration to Runa Let statements."""
        statements = []
        
        for declarator in stmt.declarations:
            if isinstance(declarator, TSVariableDeclarator):
                name = declarator.id.name if isinstance(declarator.id, TSIdentifier) else "temp_var"
                
                # Determine mutability based on declaration kind
                mutable = stmt.kind != TSVariableKind.CONST
                
                # Convert type annotation
                variable_type = None
                if declarator.type_annotation:
                    variable_type = self.convert_type(declarator.type_annotation.type_annotation)
                
                # Convert initial value
                if declarator.init:
                    value = self.convert_expression(declarator.init)
                    let_stmt = RunaLet(name, value, variable_type, mutable)
                else:
                    let_stmt = RunaLet(name, RunaLiteral(None, "undefined"), variable_type, mutable)
                
                statements.append(let_stmt)
        
        return statements
    
    def _convert_function_declaration(self, stmt: TSFunctionDeclaration) -> RunaProcessDefinition:
        """Convert function declaration to Runa Process definition."""
        func_name = stmt.name.name
        
        # Convert parameters
        params = []
        for param in stmt.parameters:
            if isinstance(param, TSParameter):
                param_name = param.name.name
                param_type = RunaType("Any")
                
                if param.type_annotation:
                    param_type = self.convert_type(param.type_annotation.type_annotation)
                
                # Handle default values
                default_value = None
                if param.default_value:
                    default_value = self.convert_expression(param.default_value)
                
                runa_param = RunaParameter(param_name, param_type, default_value)
                params.append(runa_param)
        
        # Convert return type
        return_type = RunaType("Any")
        if stmt.return_type:
            return_type = self.convert_type(stmt.return_type.type_annotation)
        
        # Convert body
        body_statements = []
        for body_stmt in stmt.body.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaProcessDefinition(
            name=func_name,
            parameters=params,
            return_type=return_type,
            body=RunaBlock(body_statements),
            is_async=stmt.async_,
            type_parameters=self._convert_type_parameters(stmt.type_parameters)
        )
    
    def _convert_interface_declaration(self, stmt: TSInterfaceDeclaration) -> RunaInterfaceDefinition:
        """Convert interface declaration to Runa interface definition."""
        interface_name = stmt.name.name
        
        # Convert extends clause
        extends = []
        for extend_type in stmt.extends_clause:
            extends.append(self.convert_type(extend_type))
        
        # Convert members
        members = []
        for member in stmt.body:
            converted_member = self.convert_statement(member)
            if converted_member:
                if isinstance(converted_member, list):
                    members.extend(converted_member)
                else:
                    members.append(converted_member)
        
        return RunaInterfaceDefinition(
            name=interface_name,
            extends=extends,
            type_parameters=self._convert_type_parameters(stmt.type_parameters),
            members=members
        )
    
    def _convert_type_alias_declaration(self, stmt: TSTypeAliasDeclaration) -> RunaStatement:
        """Convert type alias declaration to Runa equivalent."""
        # For now, convert to a comment or documentation
        alias_name = stmt.name.name
        type_def = self.convert_type(stmt.type_annotation)
        
        # Create a process that returns the type (simplified representation)
        return RunaExpressionStatement(
            RunaLiteral(f"Type alias: {alias_name}", f"// Type {alias_name}")
        )
    
    def _convert_enum_declaration(self, stmt: TSEnumDeclaration) -> RunaStatement:
        """Convert enum declaration to Runa equivalent."""
        enum_name = stmt.name.name
        
        # Convert to a series of let statements
        statements = []
        for i, member in enumerate(stmt.members):
            member_name = f"{enum_name}_{member.name.name}"
            
            if member.initializer:
                value = self.convert_expression(member.initializer)
            else:
                value = RunaLiteral(i, str(i))
            
            statements.append(RunaLet(member_name, value, RunaType("Integer"), False))
        
        # Return the first statement or a block
        return statements[0] if statements else RunaExpressionStatement(
            RunaLiteral(f"Empty enum: {enum_name}", f"// Empty enum {enum_name}")
        )
    
    def _convert_class_declaration(self, stmt: TSClassDeclaration) -> RunaClassDefinition:
        """Convert class declaration to Runa class definition."""
        class_name = stmt.name.name
        
        # Convert super class
        base_class = None
        if stmt.super_class:
            base_class = self.convert_type(stmt.super_class)
        
        # Convert implements clause
        interfaces = []
        for interface_type in stmt.implements_clause:
            interfaces.append(self.convert_type(interface_type))
        
        # Convert members
        members = []
        for member in stmt.body:
            converted_member = self.convert_statement(member)
            if converted_member:
                if isinstance(converted_member, list):
                    members.extend(converted_member)
                else:
                    members.append(converted_member)
        
        return RunaClassDefinition(
            name=class_name,
            base_class=base_class,
            interfaces=interfaces,
            type_parameters=self._convert_type_parameters(stmt.type_parameters),
            members=members
        )
    
    def _convert_namespace_declaration(self, stmt: TSNamespaceDeclaration) -> RunaStatement:
        """Convert namespace declaration to Runa equivalent."""
        namespace_name = stmt.name.name
        
        # Convert body statements
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        # For now, just return a block with a comment
        return RunaBlock([
            RunaExpressionStatement(RunaLiteral(f"Namespace: {namespace_name}", f"// Namespace {namespace_name}")),
            *body_statements
        ])
    
    def _convert_block_statement(self, stmt: TSBlockStatement) -> RunaBlock:
        """Convert block statement."""
        statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return RunaBlock(statements)
    
    def _convert_literal(self, expr: TSLiteral) -> RunaLiteral:
        """Convert literal expression."""
        if expr.literal_type == TSLiteralType.NULL:
            return RunaLiteral(None, "null", "null")
        elif expr.literal_type == TSLiteralType.UNDEFINED:
            return RunaLiteral(None, "undefined", "undefined")
        elif expr.literal_type == TSLiteralType.BOOLEAN:
            return RunaLiteral(expr.value, "true" if expr.value else "false", "boolean")
        elif expr.literal_type == TSLiteralType.NUMBER:
            return RunaLiteral(expr.value, str(expr.value), "number")
        elif expr.literal_type == TSLiteralType.STRING:
            return RunaLiteral(expr.value, f'"{expr.value}"', "string")
        elif expr.literal_type == TSLiteralType.BIGINT:
            return RunaLiteral(expr.value, str(expr.value), "bigint")
        else:
            return RunaLiteral(expr.value, expr.raw, "unknown")
    
    def _convert_identifier(self, expr: TSIdentifier) -> RunaIdentifier:
        """Convert identifier expression."""
        return RunaIdentifier(expr.name)
    
    def _convert_type_assertion(self, expr: TSTypeAssertion) -> RunaTypeAssertion:
        """Convert type assertion."""
        target_type = self.convert_type(expr.type_annotation)
        expression = self.convert_expression(expr.expression)
        
        return RunaTypeAssertion(expression, target_type)
    
    def _convert_type_reference(self, ts_type: TSTypeReference) -> RunaType:
        """Convert type reference."""
        type_name = ts_type.type_name.name
        
        # Convert generic arguments
        generic_args = []
        for arg in ts_type.type_arguments:
            generic_args.append(self.convert_type(arg))
        
        return RunaType(type_name, generic_args)
    
    def _convert_union_type(self, ts_type: TSUnionType) -> RunaType:
        """Convert union type to Runa type."""
        # For now, use the first type in the union
        if ts_type.types:
            return self.convert_type(ts_type.types[0])
        return RunaType("Any")
    
    def _convert_intersection_type(self, ts_type: TSIntersectionType) -> RunaType:
        """Convert intersection type to Runa type."""
        # For now, use the first type in the intersection
        if ts_type.types:
            return self.convert_type(ts_type.types[0])
        return RunaType("Any")
    
    def _convert_array_type(self, ts_type: TSArrayType) -> RunaType:
        """Convert array type."""
        element_type = self.convert_type(ts_type.element_type)
        return RunaType("List", [element_type])
    
    def _convert_tuple_type(self, ts_type: TSTupleType) -> RunaType:
        """Convert tuple type."""
        # For now, convert to array of first element type
        if ts_type.element_types:
            element_type = self.convert_type(ts_type.element_types[0])
            return RunaType("List", [element_type])
        return RunaType("List", [RunaType("Any")])
    
    def _convert_function_type(self, ts_type: TSFunctionType) -> RunaType:
        """Convert function type."""
        # For now, just return a Function type
        return RunaType("Function")
    
    def _convert_type_literal(self, ts_type: TSTypeLiteral) -> RunaType:
        """Convert type literal."""
        # For now, convert to Object type
        return RunaType("Object")
    
    def _convert_type_parameters(self, type_params: List[TSTypeParameter]) -> List[str]:
        """Convert type parameters."""
        return [param.name.name for param in type_params]


class RunaToTSConverter:
    """Converts Runa AST to TypeScript AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
    
    def convert(self, runa_ast: Program) -> TSProgram:
        """Convert Runa program to TypeScript program."""
        statements = []
        
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return TSProgram(statements, "module")
    
    def convert_statement(self, stmt: RunaStatement) -> Union[TSNode, List[TSNode], None]:
        """Convert Runa statement to TypeScript statement."""
        if isinstance(stmt, RunaLet):
            return self._convert_let_statement(stmt)
        
        elif isinstance(stmt, RunaProcessDefinition):
            return self._convert_process_definition(stmt)
        
        elif isinstance(stmt, RunaInterfaceDefinition):
            return self._convert_interface_definition(stmt)
        
        elif isinstance(stmt, RunaClassDefinition):
            return self._convert_class_definition(stmt)
        
        elif isinstance(stmt, RunaExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        elif isinstance(stmt, RunaBlock):
            return self._convert_block(stmt)
        
        return None
    
    def convert_expression(self, expr: RunaExpression) -> TSNode:
        """Convert Runa expression to TypeScript expression."""
        if isinstance(expr, RunaLiteral):
            return self._convert_literal(expr)
        
        elif isinstance(expr, RunaIdentifier):
            return self._convert_identifier(expr)
        
        elif isinstance(expr, RunaTypeAssertion):
            return self._convert_type_assertion(expr)
        
        # Add more expression conversions as needed
        return TSIdentifier("unknown")
    
    def convert_type(self, runa_type: RunaType) -> TSType:
        """Convert Runa type to TypeScript type."""
        # Map basic types
        type_map = {
            "Any": "any",
            "String": "string",
            "Integer": "number",
            "Float": "number",
            "Boolean": "boolean",
            "Void": "void",
            "Object": "object",
            "Function": "Function",
        }
        
        base_type = type_map.get(runa_type.name, runa_type.name)
        
        # Handle generic types
        if runa_type.generic_args:
            if runa_type.name == "List":
                element_type = self.convert_type(runa_type.generic_args[0])
                return TSArrayType(element_type)
            else:
                # Generic type reference
                type_args = [self.convert_type(arg) for arg in runa_type.generic_args]
                return TSTypeReference(TSIdentifier(base_type), type_args)
        
        return TSTypeReference(TSIdentifier(base_type))
    
    def _convert_let_statement(self, stmt: RunaLet) -> TSVariableDeclaration:
        """Convert Let statement to variable declaration."""
        id_node = TSIdentifier(stmt.name)
        
        # Convert type annotation
        type_annotation = None
        if stmt.variable_type:
            type_annotation = TSTypeAnnotation(self.convert_type(stmt.variable_type))
        
        # Convert initial value
        init = None
        if stmt.value:
            init = self.convert_expression(stmt.value)
        
        declarator = TSVariableDeclarator(id_node, type_annotation, init)
        
        # Choose appropriate variable kind
        kind = TSVariableKind.CONST if not stmt.mutable else TSVariableKind.LET
        
        return TSVariableDeclaration([declarator], kind)
    
    def _convert_process_definition(self, stmt: RunaProcessDefinition) -> TSFunctionDeclaration:
        """Convert Process definition to function declaration."""
        name_node = TSIdentifier(stmt.name)
        
        # Convert parameters
        params = []
        for param in stmt.parameters:
            param_name = TSIdentifier(param.name)
            
            param_type_annotation = None
            if param.type:
                param_type_annotation = TSTypeAnnotation(self.convert_type(param.type))
            
            default_value = None
            if param.default_value:
                default_value = self.convert_expression(param.default_value)
            
            ts_param = TSParameter(param_name, param_type_annotation, default_value)
            params.append(ts_param)
        
        # Convert return type
        return_type = None
        if stmt.return_type:
            return_type = TSTypeAnnotation(self.convert_type(stmt.return_type))
        
        # Convert body
        body_statements = []
        for body_stmt in stmt.body.statements:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = TSBlockStatement(body_statements)
        
        # Convert type parameters
        type_parameters = []
        for type_param in stmt.type_parameters:
            type_parameters.append(TSTypeParameter(TSIdentifier(type_param)))
        
        return TSFunctionDeclaration(
            name_node, 
            params, 
            body, 
            return_type, 
            type_parameters,
            stmt.is_generator,
            stmt.is_async
        )
    
    def _convert_interface_definition(self, stmt: RunaInterfaceDefinition) -> TSInterfaceDeclaration:
        """Convert interface definition to TypeScript interface."""
        name_node = TSIdentifier(stmt.name)
        
        # Convert extends clause
        extends_clause = []
        for extend_type in stmt.extends:
            extends_clause.append(TSTypeReference(TSIdentifier(extend_type.name)))
        
        # Convert type parameters
        type_parameters = []
        for type_param in stmt.type_parameters:
            type_parameters.append(TSTypeParameter(TSIdentifier(type_param)))
        
        # Convert members
        body = []
        for member in stmt.members:
            converted_member = self.convert_statement(member)
            if converted_member:
                if isinstance(converted_member, list):
                    body.extend(converted_member)
                else:
                    body.append(converted_member)
        
        return TSInterfaceDeclaration(name_node, type_parameters, extends_clause, body)
    
    def _convert_class_definition(self, stmt: RunaClassDefinition) -> TSClassDeclaration:
        """Convert class definition to TypeScript class."""
        name_node = TSIdentifier(stmt.name)
        
        # Convert super class
        super_class = None
        if stmt.base_class:
            super_class = TSTypeReference(TSIdentifier(stmt.base_class.name))
        
        # Convert implements clause
        implements_clause = []
        for interface_type in stmt.interfaces:
            implements_clause.append(TSTypeReference(TSIdentifier(interface_type.name)))
        
        # Convert type parameters
        type_parameters = []
        for type_param in stmt.type_parameters:
            type_parameters.append(TSTypeParameter(TSIdentifier(type_param)))
        
        # Convert members
        body = []
        for member in stmt.members:
            converted_member = self.convert_statement(member)
            if converted_member:
                if isinstance(converted_member, list):
                    body.extend(converted_member)
                else:
                    body.append(converted_member)
        
        return TSClassDeclaration(
            name_node,
            type_parameters,
            super_class,
            implements_clause,
            body
        )
    
    def _convert_expression_statement(self, stmt: RunaExpressionStatement) -> TSNode:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.expression)
        return expr
    
    def _convert_block(self, stmt: RunaBlock) -> TSBlockStatement:
        """Convert block statement."""
        statements = []
        for sub_stmt in stmt.statements:
            converted = self.convert_statement(sub_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return TSBlockStatement(statements)
    
    def _convert_literal(self, expr: RunaLiteral) -> TSLiteral:
        """Convert literal expression."""
        if expr.value is None:
            if expr.literal_type == "null":
                return TSLiteral(None, "null", TSLiteralType.NULL)
            else:
                return TSLiteral(None, "undefined", TSLiteralType.UNDEFINED)
        elif isinstance(expr.value, bool):
            return TSLiteral(expr.value, str(expr.value).lower(), TSLiteralType.BOOLEAN)
        elif isinstance(expr.value, (int, float)):
            return TSLiteral(expr.value, str(expr.value), TSLiteralType.NUMBER)
        elif isinstance(expr.value, str):
            return TSLiteral(expr.value, f'"{expr.value}"', TSLiteralType.STRING)
        else:
            return TSLiteral(expr.value, str(expr.value), TSLiteralType.STRING)
    
    def _convert_identifier(self, expr: RunaIdentifier) -> TSIdentifier:
        """Convert identifier expression."""
        return TSIdentifier(expr.name)
    
    def _convert_type_assertion(self, expr: RunaTypeAssertion) -> TSTypeAssertion:
        """Convert type assertion."""
        type_annotation = self.convert_type(expr.target_type)
        expression = self.convert_expression(expr.expression)
        
        return TSTypeAssertion(type_annotation, expression)


def ts_to_runa(ts_ast: TSProgram) -> Program:
    """Convert TypeScript AST to Runa AST."""
    converter = TSToRunaConverter()
    return converter.convert(ts_ast)


def runa_to_ts(runa_ast: Program) -> TSProgram:
    """Convert Runa AST to TypeScript AST."""
    converter = RunaToTSConverter()
    return converter.convert(runa_ast)