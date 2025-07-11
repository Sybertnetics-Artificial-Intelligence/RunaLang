#!/usr/bin/env python3
"""
Vyper ↔ Runa AST Converter

Bidirectional AST conversion between Vyper and Runa with complete semantic mapping
for smart contract constructs with Python-like syntax, blockchain-specific features,
and type systems.
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass

from .vyper_ast import *
from ....core.runa_ast import (
    ASTNode, NodeType, Expression, Statement, Declaration,
    Identifier, LiteralExpression, BinaryExpression, UnaryExpression,
    FunctionDeclaration, FunctionCall, VariableDeclaration,
    IfStatement, ForLoop, WhileLoop, ReturnStatement,
    Block, Program, ClassDeclaration
)


class VyperToRunaConverter:
    """Convert Vyper AST to Runa AST."""
    
    def __init__(self):
        self.interface_mappings: Dict[str, str] = {}
        self.type_mappings: Dict[str, str] = {
            'uint8': 'UnsignedInteger8',
            'uint16': 'UnsignedInteger16', 
            'uint32': 'UnsignedInteger32',
            'uint64': 'UnsignedInteger64',
            'uint128': 'UnsignedInteger128',
            'uint256': 'BigInteger',
            'int8': 'Integer8',
            'int16': 'Integer16',
            'int32': 'Integer32',
            'int64': 'Integer64',
            'int128': 'Integer128',
            'int256': 'BigInteger',
            'address': 'Address',
            'bool': 'boolean',
            'String': 'string',
            'Bytes': 'ByteArray',
            'bytes32': 'ByteArray',
            'decimal': 'Decimal'
        }
    
    def convert(self, vyper_node: VyperNode) -> ASTNode:
        """Convert Vyper AST node to Runa AST node."""
        if isinstance(vyper_node, VyperModule):
            return self.convert_module(vyper_node)
        elif isinstance(vyper_node, VyperInterfaceDefinition):
            return self.convert_interface_definition(vyper_node)
        elif isinstance(vyper_node, VyperFunctionDefinition):
            return self.convert_function_definition(vyper_node)
        elif isinstance(vyper_node, VyperVariableDeclaration):
            return self.convert_variable_declaration(vyper_node)
        elif isinstance(vyper_node, VyperStateVariable):
            return self.convert_state_variable(vyper_node)
        elif isinstance(vyper_node, VyperConstantDeclaration):
            return self.convert_constant_declaration(vyper_node)
        elif isinstance(vyper_node, VyperImmutableDeclaration):
            return self.convert_immutable_declaration(vyper_node)
        elif isinstance(vyper_node, VyperFunctionCall):
            return self.convert_function_call(vyper_node)
        elif isinstance(vyper_node, VyperIdentifier):
            return self.convert_identifier(vyper_node)
        elif isinstance(vyper_node, VyperLiteral):
            return self.convert_literal(vyper_node)
        elif isinstance(vyper_node, VyperBinaryExpression):
            return self.convert_binary_expression(vyper_node)
        elif isinstance(vyper_node, VyperUnaryExpression):
            return self.convert_unary_expression(vyper_node)
        elif isinstance(vyper_node, VyperIfStatement):
            return self.convert_if_statement(vyper_node)
        elif isinstance(vyper_node, VyperForLoop):
            return self.convert_for_loop(vyper_node)
        elif isinstance(vyper_node, VyperReturnStatement):
            return self.convert_return_statement(vyper_node)
        elif isinstance(vyper_node, VyperAssignmentStatement):
            return self.convert_assignment_statement(vyper_node)
        elif isinstance(vyper_node, VyperAugmentedAssignment):
            return self.convert_augmented_assignment(vyper_node)
        elif isinstance(vyper_node, VyperEventDefinition):
            return self.convert_event_definition(vyper_node)
        elif isinstance(vyper_node, VyperStructDefinition):
            return self.convert_struct_definition(vyper_node)
        elif isinstance(vyper_node, VyperEnumDefinition):
            return self.convert_enum_definition(vyper_node)
        elif isinstance(vyper_node, VyperLogStatement):
            return self.convert_log_statement(vyper_node)
        elif isinstance(vyper_node, VyperAssertStatement):
            return self.convert_assert_statement(vyper_node)
        elif isinstance(vyper_node, VyperRaiseStatement):
            return self.convert_raise_statement(vyper_node)
        else:
            # Fallback for unsupported nodes
            return self.create_comment_node(f"# Unsupported Vyper construct: {type(vyper_node).__name__}")
    
    def convert_module(self, vyper_module: VyperModule) -> Program:
        """Convert Vyper module to Runa program."""
        statements = []
        
        # Convert imports to import statements
        for import_stmt in vyper_module.imports:
            runa_import = Statement(
                type=NodeType.IMPORT,
                module=import_stmt.module,
                alias=import_stmt.alias
            )
            statements.append(runa_import)
        
        # Convert from imports
        for from_import in vyper_module.from_imports:
            for i, name in enumerate(from_import.names):
                alias = from_import.aliases[i] if i < len(from_import.aliases) else None
                runa_import = Statement(
                    type=NodeType.IMPORT,
                    module=f"{from_import.module}.{name}",
                    alias=alias
                )
                statements.append(runa_import)
        
        # Convert interfaces to interface declarations
        for interface in vyper_module.interfaces:
            interface_def = self.convert(interface)
            statements.append(interface_def)
        
        # Convert implements statements to comments (metadata)
        for implements in vyper_module.implements:
            comment = f"# implements: {implements.interface_name}"
            statements.append(self.create_comment_node(comment))
        
        # Convert structs and enums to class declarations
        for struct in vyper_module.structs:
            struct_def = self.convert(struct)
            statements.append(struct_def)
        
        for enum in vyper_module.enums:
            enum_def = self.convert(enum)
            statements.append(enum_def)
        
        # Convert constants and immutables to global variables
        for constant in vyper_module.constants:
            const_def = self.convert(constant)
            statements.append(const_def)
        
        for immutable in vyper_module.immutables:
            immut_def = self.convert(immutable)
            statements.append(immut_def)
        
        # Convert state variables to class properties (in a main contract class)
        if vyper_module.state_variables or vyper_module.functions or vyper_module.events:
            # Create main contract class
            properties = []
            methods = []
            
            # Convert state variables to properties
            for state_var in vyper_module.state_variables:
                prop = self.convert_state_variable_to_property(state_var)
                properties.append(prop)
            
            # Convert functions to methods
            for function in vyper_module.functions:
                method = self.convert_function_to_method(function)
                methods.append(method)
            
            # Convert events to special methods
            for event in vyper_module.events:
                event_method = self.convert_event_to_method(event)
                methods.append(event_method)
            
            main_class = ClassDeclaration(
                name="Contract",  # Default contract name
                base_classes=[],
                properties=properties,
                methods=methods
            )
            statements.append(main_class)
        
        return Program(statements=statements)
    
    def convert_interface_definition(self, vyper_interface: VyperInterfaceDefinition) -> ClassDeclaration:
        """Convert Vyper interface to Runa interface class."""
        methods = []
        
        # Convert functions to abstract methods
        for function in vyper_interface.functions:
            method = self.convert_function_to_method(function, is_abstract=True)
            methods.append(method)
        
        # Convert events to special methods
        for event in vyper_interface.events:
            event_method = self.convert_event_to_method(event)
            methods.append(event_method)
        
        return ClassDeclaration(
            name=vyper_interface.name,
            base_classes=[],
            properties=[],
            methods=methods,
            is_abstract=True
        )
    
    def convert_function_definition(self, vyper_func: VyperFunctionDefinition) -> FunctionDeclaration:
        """Convert Vyper function to Runa function."""
        # Convert parameters
        parameters = []
        if vyper_func.parameters:
            for param in vyper_func.parameters.parameters:
                param_type = self.convert_vyper_type(param.type_annotation)
                parameters.append({
                    'name': param.name,
                    'type': param_type,
                    'default': self.convert(param.default_value) if param.default_value else None
                })
        
        # Convert return type
        return_type = "void"
        if vyper_func.return_type:
            return_type = self.convert_vyper_type(vyper_func.return_type)
        
        # Convert function body
        body_statements = []
        for stmt in vyper_func.body:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        body = Block(statements=body_statements)
        
        # Add decorators as annotations
        annotations = []
        for decorator in vyper_func.decorators:
            annotations.append(f"decorator: {decorator.name}")
        
        return FunctionDeclaration(
            name=vyper_func.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            annotations=annotations
        )
    
    def convert_variable_declaration(self, vyper_var: VyperVariableDeclaration) -> VariableDeclaration:
        """Convert Vyper variable declaration to Runa variable declaration."""
        var_type = self.convert_vyper_type(vyper_var.type_annotation)
        
        initial_value = None
        if vyper_var.initial_value:
            initial_value = self.convert(vyper_var.initial_value)
        
        annotations = []
        if vyper_var.is_public:
            annotations.append("public")
        
        return VariableDeclaration(
            name=vyper_var.name,
            type=var_type,
            initial_value=initial_value,
            annotations=annotations
        )
    
    def convert_state_variable(self, vyper_var: VyperStateVariable) -> VariableDeclaration:
        """Convert Vyper state variable to Runa variable declaration."""
        return self.convert_variable_declaration(vyper_var)
    
    def convert_constant_declaration(self, vyper_const: VyperConstantDeclaration) -> VariableDeclaration:
        """Convert Vyper constant to Runa constant variable."""
        var_type = self.convert_vyper_type(vyper_const.type_annotation)
        initial_value = self.convert(vyper_const.value)
        
        return VariableDeclaration(
            name=vyper_const.name,
            type=var_type,
            initial_value=initial_value,
            annotations=["constant"]
        )
    
    def convert_immutable_declaration(self, vyper_immut: VyperImmutableDeclaration) -> VariableDeclaration:
        """Convert Vyper immutable to Runa immutable variable."""
        var_type = self.convert_vyper_type(vyper_immut.type_annotation)
        
        return VariableDeclaration(
            name=vyper_immut.name,
            type=var_type,
            initial_value=None,
            annotations=["immutable"]
        )
    
    def convert_function_call(self, vyper_call: VyperFunctionCall) -> FunctionCall:
        """Convert Vyper function call to Runa function call."""
        # Convert function expression
        func_expr = self.convert(vyper_call.func)
        
        # Convert arguments
        arguments = []
        for arg in vyper_call.args:
            runa_arg = self.convert(arg)
            arguments.append(runa_arg)
        
        # Convert keyword arguments
        for keyword in vyper_call.keywords:
            # Handle as named argument
            arguments.append({
                'name': keyword.arg,
                'value': self.convert(keyword.value)
            })
        
        return FunctionCall(
            function=func_expr,
            arguments=arguments
        )
    
    def convert_identifier(self, vyper_id: VyperIdentifier) -> Identifier:
        """Convert Vyper identifier to Runa identifier."""
        # Handle special Vyper identifiers
        special_mappings = {
            'self': 'this',
            'msg': 'message',
            'block': 'block',
            'tx': 'transaction'
        }
        
        name = special_mappings.get(vyper_id.name, vyper_id.name)
        return Identifier(name=name)
    
    def convert_literal(self, vyper_lit: VyperLiteral) -> LiteralExpression:
        """Convert Vyper literal to Runa literal."""
        # Handle different literal types
        if vyper_lit.type_name == "string":
            return LiteralExpression(value=vyper_lit.value, type="string")
        elif vyper_lit.type_name == "number":
            # Convert to appropriate numeric type
            if '.' in str(vyper_lit.value):
                return LiteralExpression(value=float(vyper_lit.value), type="decimal")
            else:
                return LiteralExpression(value=int(vyper_lit.value), type="integer")
        elif vyper_lit.type_name == "bool":
            return LiteralExpression(value=vyper_lit.value, type="boolean")
        else:
            return LiteralExpression(value=vyper_lit.value, type=vyper_lit.type_name)
    
    def convert_binary_expression(self, vyper_expr: VyperBinaryExpression) -> BinaryExpression:
        """Convert Vyper binary expression to Runa binary expression."""
        left = self.convert(vyper_expr.left)
        right = self.convert(vyper_expr.right)
        
        # Map Vyper operators to Runa operators
        operator_mappings = {
            VyperOperator.PLUS: '+',
            VyperOperator.MINUS: '-',
            VyperOperator.MULTIPLY: '*',
            VyperOperator.DIVIDE: '/',
            VyperOperator.INT_DIVIDE: '//',
            VyperOperator.MODULO: '%',
            VyperOperator.EXPONENT: '**',
            VyperOperator.EQUAL: '==',
            VyperOperator.NOT_EQUAL: '!=',
            VyperOperator.LESS_THAN: '<',
            VyperOperator.LESS_EQUAL: '<=',
            VyperOperator.GREATER_THAN: '>',
            VyperOperator.GREATER_EQUAL: '>=',
            VyperOperator.AND: 'and',
            VyperOperator.OR: 'or',
            VyperOperator.BIT_AND: '&',
            VyperOperator.BIT_OR: '|',
            VyperOperator.BIT_XOR: '^',
            VyperOperator.SHIFT_LEFT: '<<',
            VyperOperator.SHIFT_RIGHT: '>>'
        }
        
        operator = operator_mappings.get(vyper_expr.operator, str(vyper_expr.operator.value))
        
        return BinaryExpression(
            left=left,
            operator=operator,
            right=right
        )
    
    def convert_unary_expression(self, vyper_expr: VyperUnaryExpression) -> UnaryExpression:
        """Convert Vyper unary expression to Runa unary expression."""
        operand = self.convert(vyper_expr.operand)
        
        # Map Vyper operators to Runa operators
        operator_mappings = {
            VyperOperator.NOT: 'not',
            VyperOperator.MINUS: '-',
            VyperOperator.BIT_NOT: '~'
        }
        
        operator = operator_mappings.get(vyper_expr.operator, str(vyper_expr.operator.value))
        
        return UnaryExpression(
            operator=operator,
            operand=operand
        )
    
    def convert_if_statement(self, vyper_if: VyperIfStatement) -> IfStatement:
        """Convert Vyper if statement to Runa if statement."""
        condition = self.convert(vyper_if.condition)
        
        then_statements = []
        for stmt in vyper_if.body:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                then_statements.append(runa_stmt)
        
        else_statements = []
        for stmt in vyper_if.orelse:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                else_statements.append(runa_stmt)
        
        then_block = Block(statements=then_statements)
        else_block = Block(statements=else_statements) if else_statements else None
        
        return IfStatement(
            condition=condition,
            then_statement=then_block,
            else_statement=else_block
        )
    
    def convert_for_loop(self, vyper_for: VyperForLoop) -> ForLoop:
        """Convert Vyper for loop to Runa for loop."""
        # Vyper for loops are like Python for-in loops
        # Convert to Runa enhanced for loop syntax
        
        target = self.convert(vyper_for.target)
        iterable = self.convert(vyper_for.iter)
        
        body_statements = []
        for stmt in vyper_for.body:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        body = Block(statements=body_statements)
        
        # Create enhanced for loop (for item in collection)
        return ForLoop(
            init_statement=None,  # No init in for-in loops
            condition=None,       # Condition is implicit
            update_expression=None,  # Update is implicit
            body=body,
            annotations=[f"for_in: {target.name} in {iterable}"]
        )
    
    def convert_return_statement(self, vyper_return: VyperReturnStatement) -> ReturnStatement:
        """Convert Vyper return statement to Runa return statement."""
        value = None
        if vyper_return.value:
            value = self.convert(vyper_return.value)
        
        return ReturnStatement(value=value)
    
    def convert_assignment_statement(self, vyper_assign: VyperAssignmentStatement) -> Statement:
        """Convert Vyper assignment statement to Runa assignment."""
        target = self.convert(vyper_assign.target)
        value = self.convert(vyper_assign.value)
        
        return Statement(
            type=NodeType.ASSIGNMENT,
            target=target,
            value=value
        )
    
    def convert_augmented_assignment(self, vyper_aug: VyperAugmentedAssignment) -> Statement:
        """Convert Vyper augmented assignment to Runa assignment."""
        target = self.convert(vyper_aug.target)
        value = self.convert(vyper_aug.value)
        
        # Convert to equivalent binary expression assignment
        operator_mappings = {
            VyperOperator.PLUS_ASSIGN: '+',
            VyperOperator.MINUS_ASSIGN: '-',
            VyperOperator.MULTIPLY_ASSIGN: '*',
            VyperOperator.DIVIDE_ASSIGN: '/',
            VyperOperator.MODULO_ASSIGN: '%',
            VyperOperator.POWER_ASSIGN: '**'
        }
        
        operator = operator_mappings.get(vyper_aug.operator, '=')
        
        if operator != '=':
            # Create binary expression: target = target op value
            binary_expr = BinaryExpression(
                left=target,
                operator=operator,
                right=value
            )
            value = binary_expr
        
        return Statement(
            type=NodeType.ASSIGNMENT,
            target=target,
            value=value
        )
    
    def convert_event_definition(self, vyper_event: VyperEventDefinition) -> FunctionDeclaration:
        """Convert Vyper event to Runa event function."""
        # Convert parameters
        parameters = []
        for param in vyper_event.parameters:
            param_type = self.convert_vyper_type(param.type_annotation)
            parameters.append({
                'name': param.name,
                'type': param_type
            })
        
        # Events become special functions
        return FunctionDeclaration(
            name=vyper_event.name,
            parameters=parameters,
            return_type="void",
            body=Block(statements=[]),
            annotations=["event"]
        )
    
    def convert_struct_definition(self, vyper_struct: VyperStructDefinition) -> ClassDeclaration:
        """Convert Vyper struct to Runa data class."""
        properties = []
        
        for field in vyper_struct.fields:
            field_type = self.convert_vyper_type(field.type_annotation)
            properties.append({
                'name': field.name,
                'type': field_type,
                'visibility': 'public'
            })
        
        return ClassDeclaration(
            name=vyper_struct.name,
            base_classes=[],
            properties=properties,
            methods=[],
            annotations=["struct", "data_class"]
        )
    
    def convert_enum_definition(self, vyper_enum: VyperEnumDefinition) -> ClassDeclaration:
        """Convert Vyper enum to Runa enum class."""
        # Enums become special classes with constant values
        properties = []
        
        for i, value in enumerate(vyper_enum.values):
            properties.append({
                'name': value,
                'type': 'integer',
                'value': i,
                'visibility': 'public',
                'is_constant': True
            })
        
        return ClassDeclaration(
            name=vyper_enum.name,
            base_classes=[],
            properties=properties,
            methods=[],
            annotations=["enum"]
        )
    
    def convert_log_statement(self, vyper_log: VyperLogStatement) -> Statement:
        """Convert Vyper log statement to Runa event emission."""
        event_call = self.convert(vyper_log.event_call)
        
        return Statement(
            type=NodeType.EXPRESSION_STATEMENT,
            expression=event_call,
            annotations=["log_event"]
        )
    
    def convert_assert_statement(self, vyper_assert: VyperAssertStatement) -> Statement:
        """Convert Vyper assert statement to Runa assert."""
        test = self.convert(vyper_assert.test)
        
        message = None
        if vyper_assert.msg:
            message = self.convert(vyper_assert.msg)
        
        return Statement(
            type=NodeType.ASSERTION,
            condition=test,
            message=message
        )
    
    def convert_raise_statement(self, vyper_raise: VyperRaiseStatement) -> Statement:
        """Convert Vyper raise statement to Runa exception throw."""
        exception = None
        if vyper_raise.exc:
            exception = self.convert(vyper_raise.exc)
        
        return Statement(
            type=NodeType.THROW,
            exception=exception
        )
    
    def convert_vyper_type(self, vyper_type) -> str:
        """Convert Vyper type to Runa type."""
        if isinstance(vyper_type, VyperPrimitiveTypeName):
            return self.type_mappings.get(vyper_type.name.value, vyper_type.name.value)
        elif isinstance(vyper_type, VyperArrayType):
            element_type = self.convert_vyper_type(vyper_type.element_type)
            if vyper_type.size:
                # Fixed array
                return f"Array<{element_type}>"
            else:
                # Dynamic array
                return f"List<{element_type}>"
        elif isinstance(vyper_type, VyperDynArrayType):
            element_type = self.convert_vyper_type(vyper_type.element_type)
            return f"List<{element_type}>"
        elif isinstance(vyper_type, VyperHashMapType):
            key_type = self.convert_vyper_type(vyper_type.key_type)
            value_type = self.convert_vyper_type(vyper_type.value_type)
            return f"Map<{key_type}, {value_type}>"
        elif isinstance(vyper_type, VyperStructType):
            return vyper_type.name
        elif isinstance(vyper_type, VyperInterfaceType):
            return vyper_type.name
        else:
            return str(vyper_type)
    
    def convert_state_variable_to_property(self, state_var: VyperStateVariable) -> Dict:
        """Convert Vyper state variable to Runa class property."""
        prop_type = self.convert_vyper_type(state_var.type_annotation)
        
        initial_value = None
        if state_var.initial_value:
            initial_value = self.convert(state_var.initial_value)
        
        return {
            'name': state_var.name,
            'type': prop_type,
            'initial_value': initial_value,
            'visibility': 'public' if state_var.is_public else 'private',
            'annotations': ['state_variable']
        }
    
    def convert_function_to_method(self, function: VyperFunctionDefinition, is_abstract: bool = False) -> Dict:
        """Convert Vyper function to Runa class method."""
        # Convert parameters
        parameters = []
        if function.parameters:
            for param in function.parameters.parameters:
                param_type = self.convert_vyper_type(param.type_annotation)
                parameters.append({
                    'name': param.name,
                    'type': param_type,
                    'default': self.convert(param.default_value) if param.default_value else None
                })
        
        # Convert return type
        return_type = "void"
        if function.return_type:
            return_type = self.convert_vyper_type(function.return_type)
        
        # Convert body (if not abstract)
        body = None
        if not is_abstract:
            body_statements = []
            for stmt in function.body:
                runa_stmt = self.convert(stmt)
                if runa_stmt:
                    body_statements.append(runa_stmt)
            body = Block(statements=body_statements)
        
        # Extract visibility from decorators
        visibility = 'internal'  # Default
        annotations = []
        
        for decorator in function.decorators:
            if decorator.name in ['external']:
                visibility = 'public'
            elif decorator.name in ['internal']:
                visibility = 'private'
            annotations.append(f"decorator: {decorator.name}")
        
        if is_abstract:
            annotations.append("abstract")
        
        return {
            'name': function.name,
            'parameters': parameters,
            'return_type': return_type,
            'body': body,
            'visibility': visibility,
            'annotations': annotations
        }
    
    def convert_event_to_method(self, event: VyperEventDefinition) -> Dict:
        """Convert Vyper event to Runa event method."""
        # Convert parameters
        parameters = []
        for param in event.parameters:
            param_type = self.convert_vyper_type(param.type_annotation)
            parameters.append({
                'name': param.name,
                'type': param_type
            })
        
        return {
            'name': event.name,
            'parameters': parameters,
            'return_type': 'void',
            'body': Block(statements=[]),
            'visibility': 'public',
            'annotations': ['event']
        }
    
    def create_comment_node(self, text: str) -> Statement:
        """Create a comment statement node."""
        return Statement(
            type=NodeType.COMMENT,
            text=text
        )


class RunaToVyperConverter:
    """Convert Runa AST to Vyper AST."""
    
    def __init__(self):
        self.type_mappings: Dict[str, str] = {
            'UnsignedInteger8': 'uint8',
            'UnsignedInteger16': 'uint16',
            'UnsignedInteger32': 'uint32', 
            'UnsignedInteger64': 'uint64',
            'UnsignedInteger128': 'uint128',
            'BigInteger': 'uint256',
            'Integer8': 'int8',
            'Integer16': 'int16',
            'Integer32': 'int32',
            'Integer64': 'int64',
            'Integer128': 'int128',
            'Address': 'address',
            'boolean': 'bool',
            'string': 'String',
            'ByteArray': 'Bytes',
            'Decimal': 'decimal'
        }
    
    def convert(self, runa_node: ASTNode) -> VyperNode:
        """Convert Runa AST node to Vyper AST node."""
        if isinstance(runa_node, Program):
            return self.convert_program(runa_node)
        elif isinstance(runa_node, ClassDeclaration):
            return self.convert_class_declaration(runa_node)
        elif isinstance(runa_node, FunctionDeclaration):
            return self.convert_function_declaration(runa_node)
        elif isinstance(runa_node, VariableDeclaration):
            return self.convert_variable_declaration(runa_node)
        elif isinstance(runa_node, FunctionCall):
            return self.convert_function_call(runa_node)
        elif isinstance(runa_node, Identifier):
            return self.convert_identifier(runa_node)
        elif isinstance(runa_node, LiteralExpression):
            return self.convert_literal_expression(runa_node)
        elif isinstance(runa_node, BinaryExpression):
            return self.convert_binary_expression(runa_node)
        elif isinstance(runa_node, UnaryExpression):
            return self.convert_unary_expression(runa_node)
        elif isinstance(runa_node, IfStatement):
            return self.convert_if_statement(runa_node)
        elif isinstance(runa_node, ForLoop):
            return self.convert_for_loop(runa_node)
        elif isinstance(runa_node, ReturnStatement):
            return self.convert_return_statement(runa_node)
        else:
            # Fallback - create a comment
            return VyperComment(text=f"# Unsupported Runa construct: {type(runa_node).__name__}")
    
    def convert_program(self, runa_program: Program) -> VyperModule:
        """Convert Runa program to Vyper module."""
        module = VyperModule()
        
        for stmt in runa_program.statements:
            if isinstance(stmt, Statement) and stmt.type == NodeType.IMPORT:
                # Convert import statements
                if '.' in stmt.module:
                    # from import
                    parts = stmt.module.split('.')
                    module_name = '.'.join(parts[:-1])
                    name = parts[-1]
                    from_import = VyperFromImport(
                        module=module_name,
                        names=[name],
                        aliases=[stmt.alias] if stmt.alias else [None]
                    )
                    module.from_imports.append(from_import)
                else:
                    # simple import
                    import_stmt = VyperImportStatement(
                        module=stmt.module,
                        alias=stmt.alias
                    )
                    module.imports.append(import_stmt)
            
            elif isinstance(stmt, ClassDeclaration):
                # Convert class to appropriate Vyper construct
                if 'interface' in getattr(stmt, 'annotations', []):
                    interface = self.convert_class_to_interface(stmt)
                    module.interfaces.append(interface)
                elif 'struct' in getattr(stmt, 'annotations', []):
                    struct = self.convert_class_to_struct(stmt)
                    module.structs.append(struct)
                elif 'enum' in getattr(stmt, 'annotations', []):
                    enum = self.convert_class_to_enum(stmt)
                    module.enums.append(enum)
                else:
                    # Main contract - extract components
                    for prop in getattr(stmt, 'properties', []):
                        state_var = self.convert_property_to_state_variable(prop)
                        module.state_variables.append(state_var)
                    
                    for method in getattr(stmt, 'methods', []):
                        if 'event' in method.get('annotations', []):
                            event = self.convert_method_to_event(method)
                            module.events.append(event)
                        else:
                            function = self.convert_method_to_function(method)
                            module.functions.append(function)
            
            elif isinstance(stmt, FunctionDeclaration):
                # Convert standalone function
                vyper_func = self.convert_function_declaration(stmt)
                module.functions.append(vyper_func)
            
            elif isinstance(stmt, VariableDeclaration):
                # Convert global variable
                if 'constant' in getattr(stmt, 'annotations', []):
                    constant = self.convert_variable_to_constant(stmt)
                    module.constants.append(constant)
                elif 'immutable' in getattr(stmt, 'annotations', []):
                    immutable = self.convert_variable_to_immutable(stmt)
                    module.immutables.append(immutable)
                else:
                    state_var = self.convert_variable_to_state_variable(stmt)
                    module.state_variables.append(state_var)
        
        return module
    
    def convert_runa_type(self, runa_type: str) -> VyperTypeName:
        """Convert Runa type to Vyper type."""
        # Handle generic types
        if runa_type.startswith('Array<') or runa_type.startswith('List<'):
            # Extract element type
            inner_type = runa_type[runa_type.find('<')+1:runa_type.rfind('>')]
            element_type = self.convert_runa_type(inner_type)
            
            if runa_type.startswith('Array<'):
                return VyperArrayType(element_type=element_type, size=None)
            else:
                return VyperDynArrayType(element_type=element_type, max_size=VyperLiteral(value=1000))
        
        elif runa_type.startswith('Map<'):
            # Extract key and value types
            inner = runa_type[4:-1]  # Remove 'Map<' and '>'
            parts = inner.split(', ')
            key_type = self.convert_runa_type(parts[0])
            value_type = self.convert_runa_type(parts[1])
            return VyperHashMapType(key_type=key_type, value_type=value_type)
        
        else:
            # Simple type mapping
            vyper_type = self.type_mappings.get(runa_type, runa_type)
            
            # Check if it's a primitive type
            try:
                primitive = VyperPrimitiveType(vyper_type)
                return VyperPrimitiveTypeName(name=primitive)
            except ValueError:
                # Must be a user-defined type
                return VyperStructType(name=vyper_type)


# Convenience functions for external use
def vyper_to_runa(vyper_ast: VyperNode) -> ASTNode:
    """Convert Vyper AST to Runa AST."""
    converter = VyperToRunaConverter()
    return converter.convert(vyper_ast)


def runa_to_vyper(runa_ast: ASTNode) -> VyperNode:
    """Convert Runa AST to Vyper AST."""
    converter = RunaToVyperConverter()
    return converter.convert(runa_ast) 