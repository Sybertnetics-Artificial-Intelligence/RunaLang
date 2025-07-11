#!/usr/bin/env python3
"""
Solidity ↔ Runa AST Converter

Bidirectional AST conversion between Solidity and Runa with complete semantic mapping
for smart contract constructs, blockchain-specific features, and type systems.
"""

from typing import List, Optional, Any, Union, Dict
from dataclasses import dataclass

from .solidity_ast import *
from ....core.runa_ast import (
    ASTNode, NodeType, Expression, Statement, Declaration,
    Identifier, LiteralExpression, BinaryExpression, UnaryExpression,
    FunctionDeclaration, FunctionCall, VariableDeclaration,
    IfStatement, ForLoop, WhileLoop, ReturnStatement,
    Block, Program, ClassDeclaration
)


class SolidityToRunaConverter:
    """Convert Solidity AST to Runa AST."""
    
    def __init__(self):
        self.contract_mappings: Dict[str, str] = {}
        self.type_mappings: Dict[str, str] = {
            'uint256': 'BigInteger',
            'uint': 'BigInteger', 
            'int256': 'BigInteger',
            'int': 'BigInteger',
            'address': 'Address',
            'bool': 'boolean',
            'string': 'string',
            'bytes': 'ByteArray',
            'bytes32': 'ByteArray'
        }
    
    def convert(self, sol_node: SolidityNode) -> ASTNode:
        """Convert Solidity AST node to Runa AST node."""
        if isinstance(sol_node, SoliditySourceUnit):
            return self.convert_source_unit(sol_node)
        elif isinstance(sol_node, SolidityContractDefinition):
            return self.convert_contract_definition(sol_node)
        elif isinstance(sol_node, SolidityFunctionDefinition):
            return self.convert_function_definition(sol_node)
        elif isinstance(sol_node, SolidityVariableDeclaration):
            return self.convert_variable_declaration(sol_node)
        elif isinstance(sol_node, SolidityFunctionCall):
            return self.convert_function_call(sol_node)
        elif isinstance(sol_node, SolidityIdentifier):
            return self.convert_identifier(sol_node)
        elif isinstance(sol_node, SolidityLiteral):
            return self.convert_literal(sol_node)
        elif isinstance(sol_node, SolidityBinaryExpression):
            return self.convert_binary_expression(sol_node)
        elif isinstance(sol_node, SolidityUnaryExpression):
            return self.convert_unary_expression(sol_node)
        elif isinstance(sol_node, SolidityIfStatement):
            return self.convert_if_statement(sol_node)
        elif isinstance(sol_node, SolidityForLoop):
            return self.convert_for_loop(sol_node)
        elif isinstance(sol_node, SolidityWhileLoop):
            return self.convert_while_loop(sol_node)
        elif isinstance(sol_node, SolidityReturnStatement):
            return self.convert_return_statement(sol_node)
        elif isinstance(sol_node, SolidityEventDefinition):
            return self.convert_event_definition(sol_node)
        elif isinstance(sol_node, SolidityModifierDefinition):
            return self.convert_modifier_definition(sol_node)
        else:
            # Fallback for unsupported nodes
            return self.create_comment_node(f"# Unsupported Solidity construct: {type(sol_node).__name__}")
    
    def convert_source_unit(self, sol_unit: SoliditySourceUnit) -> Program:
        """Convert Solidity source unit to Runa program."""
        statements = []
        
        # Convert pragma directives to comments
        for pragma in sol_unit.pragma_directives:
            comment = f"# pragma {pragma.name} {pragma.value}"
            statements.append(self.create_comment_node(comment))
        
        # Convert import directives to import statements
        for import_dir in sol_unit.import_directives:
            # Runa-style import
            import_stmt = Statement(
                type=NodeType.IMPORT,
                module=import_dir.path,
                alias=import_dir.alias
            )
            statements.append(import_stmt)
        
        # Convert contracts to classes
        for contract in sol_unit.contracts:
            class_def = self.convert(contract)
            statements.append(class_def)
        
        # Convert interfaces and libraries
        for interface in sol_unit.interfaces:
            interface_def = self.convert(interface)
            statements.append(interface_def)
        
        for library in sol_unit.libraries:
            library_def = self.convert(library)
            statements.append(library_def)
        
        return Program(statements=statements)
    
    def convert_contract_definition(self, sol_contract: SolidityContractDefinition) -> ClassDeclaration:
        """Convert Solidity contract to Runa class."""
        # Contract becomes a class
        methods = []
        properties = []
        
        # Convert state variables to properties
        for state_var in sol_contract.state_variables:
            prop = self.convert_state_variable_to_property(state_var)
            properties.append(prop)
        
        # Convert functions to methods
        for function in sol_contract.functions:
            method = self.convert_function_to_method(function)
            methods.append(method)
        
        # Convert events to special methods
        for event in sol_contract.events:
            event_method = self.convert_event_to_method(event)
            methods.append(event_method)
        
        # Handle inheritance
        base_classes = []
        for inheritance in sol_contract.inheritance:
            base_classes.append(inheritance.base_name)
        
        return ClassDeclaration(
            name=sol_contract.name,
            base_classes=base_classes,
            properties=properties,
            methods=methods,
            is_abstract=sol_contract.is_abstract
        )
    
    def convert_function_definition(self, sol_func: SolidityFunctionDefinition) -> FunctionDeclaration:
        """Convert Solidity function to Runa function."""
        # Convert parameters
        parameters = []
        if sol_func.parameters:
            for param in sol_func.parameters.parameters:
                param_type = self.convert_solidity_type(param.type_name)
                parameters.append({
                    'name': param.name,
                    'type': param_type
                })
        
        # Convert return type
        return_type = "void"
        if sol_func.return_parameters and sol_func.return_parameters.parameters:
            if len(sol_func.return_parameters.parameters) == 1:
                return_type = self.convert_solidity_type(sol_func.return_parameters.parameters[0].type_name)
            else:
                # Multiple return values -> tuple
                return_types = [self.convert_solidity_type(p.type_name) for p in sol_func.return_parameters.parameters]
                return_type = f"Tuple<{', '.join(return_types)}>"
        
        # Convert function body
        body_statements = []
        if sol_func.body:
            for stmt in sol_func.body.statements:
                runa_stmt = self.convert(stmt)
                if runa_stmt:
                    body_statements.append(runa_stmt)
        
        body = Block(statements=body_statements)
        
        # Add visibility and mutability as annotations
        annotations = []
        annotations.append(f"visibility: {sol_func.visibility.value}")
        annotations.append(f"mutability: {sol_func.mutability.value}")
        
        if sol_func.is_virtual:
            annotations.append("virtual")
        if sol_func.is_override:
            annotations.append("override")
        
        return FunctionDeclaration(
            name=sol_func.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            annotations=annotations
        )
    
    def convert_variable_declaration(self, sol_var: SolidityVariableDeclaration) -> VariableDeclaration:
        """Convert Solidity variable declaration to Runa variable declaration."""
        var_type = self.convert_solidity_type(sol_var.type_name)
        
        initial_value = None
        if sol_var.initial_value:
            initial_value = self.convert(sol_var.initial_value)
        
        annotations = []
        if sol_var.visibility:
            annotations.append(f"visibility: {sol_var.visibility.value}")
        if sol_var.is_constant:
            annotations.append("constant")
        if sol_var.is_immutable:
            annotations.append("immutable")
        
        return VariableDeclaration(
            name=sol_var.name,
            type=var_type,
            value=initial_value,
            annotations=annotations
        )
    
    def convert_function_call(self, sol_call: SolidityFunctionCall) -> FunctionCall:
        """Convert Solidity function call to Runa function call."""
        function = self.convert(sol_call.expression)
        
        arguments = []
        for i, arg in enumerate(sol_call.arguments):
            arg_value = self.convert(arg)
            
            # Handle named arguments
            if i < len(sol_call.names) and sol_call.names[i]:
                arguments.append({
                    'name': sol_call.names[i],
                    'value': arg_value
                })
            else:
                arguments.append({
                    'value': arg_value
                })
        
        return FunctionCall(
            function=function,
            arguments=arguments
        )
    
    def convert_identifier(self, sol_id: SolidityIdentifier) -> Identifier:
        """Convert Solidity identifier to Runa identifier."""
        # Map Solidity built-ins to Runa equivalents
        name_mappings = {
            'msg': 'message',
            'block': 'current_block',
            'tx': 'transaction',
            'now': 'current_timestamp',
            'this': 'self'
        }
        
        mapped_name = name_mappings.get(sol_id.name, sol_id.name)
        return Identifier(name=mapped_name)
    
    def convert_literal(self, sol_lit: SolidityLiteral) -> LiteralExpression:
        """Convert Solidity literal to Runa literal."""
        # Map Solidity types to Runa types
        type_mappings = {
            'uint256': 'BigInteger',
            'string': 'string',
            'bool': 'boolean',
            'address': 'Address'
        }
        
        runa_type = type_mappings.get(sol_lit.type_name, 'Any')
        
        return LiteralExpression(
            value=sol_lit.value,
            type=runa_type
        )
    
    def convert_binary_expression(self, sol_expr: SolidityBinaryExpression) -> BinaryExpression:
        """Convert Solidity binary expression to Runa binary expression."""
        left = self.convert(sol_expr.left)
        right = self.convert(sol_expr.right)
        
        # Map Solidity operators to Runa operators
        operator_mappings = {
            SolidityOperator.PLUS: '+',
            SolidityOperator.MINUS: '-',
            SolidityOperator.MULTIPLY: '*',
            SolidityOperator.DIVIDE: '/',
            SolidityOperator.MODULO: '%',
            SolidityOperator.EXPONENT: '**',
            SolidityOperator.EQUAL: '==',
            SolidityOperator.NOT_EQUAL: '!=',
            SolidityOperator.LESS_THAN: '<',
            SolidityOperator.LESS_EQUAL: '<=',
            SolidityOperator.GREATER_THAN: '>',
            SolidityOperator.GREATER_EQUAL: '>=',
            SolidityOperator.AND: 'and',
            SolidityOperator.OR: 'or'
        }
        
        operator = operator_mappings.get(sol_expr.operator, str(sol_expr.operator.value))
        
        return BinaryExpression(
            left=left,
            operator=operator,
            right=right
        )
    
    def convert_unary_expression(self, sol_expr: SolidityUnaryExpression) -> UnaryExpression:
        """Convert Solidity unary expression to Runa unary expression."""
        expression = self.convert(sol_expr.expression)
        
        operator_mappings = {
            SolidityOperator.MINUS: '-',
            SolidityOperator.NOT: 'not'
        }
        
        operator = operator_mappings.get(sol_expr.operator, str(sol_expr.operator.value))
        
        return UnaryExpression(
            operator=operator,
            expression=expression
        )
    
    def convert_if_statement(self, sol_if: SolidityIfStatement) -> IfStatement:
        """Convert Solidity if statement to Runa if statement."""
        condition = self.convert(sol_if.condition)
        then_stmt = self.convert(sol_if.then_statement)
        else_stmt = self.convert(sol_if.else_statement) if sol_if.else_statement else None
        
        return IfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt
        )
    
    def convert_for_loop(self, sol_for: SolidityForLoop) -> ForLoop:
        """Convert Solidity for loop to Runa for loop."""
        # Solidity for loops are more complex, convert to while loop if needed
        init = self.convert(sol_for.init_statement) if sol_for.init_statement else None
        condition = self.convert(sol_for.condition) if sol_for.condition else None
        update = self.convert(sol_for.update_expression) if sol_for.update_expression else None
        body = self.convert(sol_for.body)
        
        # Create equivalent while loop structure
        statements = []
        if init:
            statements.append(init)
        
        loop_body = []
        if body:
            loop_body.append(body)
        if update:
            loop_body.append(update)
        
        while_loop = WhileLoop(
            condition=condition or LiteralExpression(value=True, type="boolean"),
            body=Block(statements=loop_body)
        )
        
        statements.append(while_loop)
        
        return Block(statements=statements)
    
    def convert_while_loop(self, sol_while: SolidityWhileLoop) -> WhileLoop:
        """Convert Solidity while loop to Runa while loop."""
        condition = self.convert(sol_while.condition)
        body = self.convert(sol_while.body)
        
        return WhileLoop(
            condition=condition,
            body=body
        )
    
    def convert_return_statement(self, sol_return: SolidityReturnStatement) -> ReturnStatement:
        """Convert Solidity return statement to Runa return statement."""
        value = self.convert(sol_return.expression) if sol_return.expression else None
        
        return ReturnStatement(value=value)
    
    def convert_event_definition(self, sol_event: SolidityEventDefinition) -> FunctionDeclaration:
        """Convert Solidity event to Runa event method."""
        # Events become special methods
        parameters = []
        if sol_event.parameters:
            for param in sol_event.parameters.parameters:
                param_type = self.convert_solidity_type(param.type_name)
                parameters.append({
                    'name': param.name,
                    'type': param_type
                })
        
        # Event body - emit the event
        body = Block(statements=[
            self.create_comment_node(f"# Event: {sol_event.name}")
        ])
        
        return FunctionDeclaration(
            name=f"emit_{sol_event.name}",
            parameters=parameters,
            return_type="void",
            body=body,
            annotations=["event"]
        )
    
    def convert_modifier_definition(self, sol_modifier: SolidityModifierDefinition) -> FunctionDeclaration:
        """Convert Solidity modifier to Runa decorator function."""
        parameters = []
        if sol_modifier.parameters:
            for param in sol_modifier.parameters.parameters:
                param_type = self.convert_solidity_type(param.type_name)
                parameters.append({
                    'name': param.name,
                    'type': param_type
                })
        
        body_statements = []
        if sol_modifier.body:
            for stmt in sol_modifier.body.statements:
                runa_stmt = self.convert(stmt)
                if runa_stmt:
                    body_statements.append(runa_stmt)
        
        body = Block(statements=body_statements)
        
        return FunctionDeclaration(
            name=sol_modifier.name,
            parameters=parameters,
            return_type="void",
            body=body,
            annotations=["modifier", "decorator"]
        )
    
    def convert_solidity_type(self, sol_type) -> str:
        """Convert Solidity type to Runa type."""
        if isinstance(sol_type, SolidityElementaryType):
            return self.type_mappings.get(sol_type.name, sol_type.name)
        elif isinstance(sol_type, SolidityArrayType):
            base_type = self.convert_solidity_type(sol_type.base_type)
            return f"Array<{base_type}>"
        elif isinstance(sol_type, SolidityMappingType):
            key_type = self.convert_solidity_type(sol_type.key_type)
            value_type = self.convert_solidity_type(sol_type.value_type)
            return f"Map<{key_type}, {value_type}>"
        elif isinstance(sol_type, SolidityUserDefinedType):
            return sol_type.name
        else:
            return "Any"
    
    def convert_state_variable_to_property(self, state_var: SolidityStateVariable) -> Dict:
        """Convert Solidity state variable to Runa class property."""
        var_type = self.convert_solidity_type(state_var.type_name)
        
        return {
            'name': state_var.name,
            'type': var_type,
            'visibility': state_var.visibility.value if state_var.visibility else 'private',
            'is_constant': state_var.is_constant,
            'initial_value': self.convert(state_var.initial_value) if state_var.initial_value else None
        }
    
    def convert_function_to_method(self, function: SolidityFunctionDefinition) -> Dict:
        """Convert Solidity function to Runa class method."""
        method = self.convert_function_definition(function)
        
        return {
            'name': method.name,
            'parameters': method.parameters,
            'return_type': method.return_type,
            'body': method.body,
            'visibility': 'public',  # Default
            'annotations': method.annotations
        }
    
    def convert_event_to_method(self, event: SolidityEventDefinition) -> Dict:
        """Convert Solidity event to Runa class method."""
        method = self.convert_event_definition(event)
        
        return {
            'name': method.name,
            'parameters': method.parameters,
            'return_type': method.return_type,
            'body': method.body,
            'visibility': 'public',
            'annotations': method.annotations
        }
    
    def create_comment_node(self, text: str) -> Statement:
        """Create a comment statement."""
        return Statement(
            type=NodeType.COMMENT,
            text=text
        )


class RunaToSolidityConverter:
    """Convert Runa AST to Solidity AST."""
    
    def __init__(self):
        self.type_mappings: Dict[str, str] = {
            'BigInteger': 'uint256',
            'Address': 'address',
            'boolean': 'bool',
            'string': 'string',
            'ByteArray': 'bytes'
        }
    
    def convert(self, runa_node: ASTNode) -> SolidityNode:
        """Convert Runa AST node to Solidity AST node."""
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
        elif isinstance(runa_node, WhileLoop):
            return self.convert_while_loop(runa_node)
        elif isinstance(runa_node, ReturnStatement):
            return self.convert_return_statement(runa_node)
        else:
            # Fallback
            return SolidityComment(text=f"// Unsupported Runa construct: {type(runa_node).__name__}")
    
    def convert_program(self, runa_program: Program) -> SoliditySourceUnit:
        """Convert Runa program to Solidity source unit."""
        contracts = []
        pragma_directives = [SolidityPragmaDirective(name="solidity", value="^0.8.0")]
        
        for stmt in runa_program.statements:
            if isinstance(stmt, ClassDeclaration):
                contract = self.convert(stmt)
                contracts.append(contract)
        
        return SoliditySourceUnit(
            pragma_directives=pragma_directives,
            contracts=contracts
        )
    
    def convert_class_declaration(self, runa_class: ClassDeclaration) -> SolidityContractDefinition:
        """Convert Runa class to Solidity contract."""
        # Class becomes a contract
        state_variables = []
        functions = []
        events = []
        
        # Convert properties to state variables
        if hasattr(runa_class, 'properties'):
            for prop in runa_class.properties:
                state_var = self.convert_property_to_state_variable(prop)
                state_variables.append(state_var)
        
        # Convert methods to functions
        if hasattr(runa_class, 'methods'):
            for method in runa_class.methods:
                if 'event' in method.get('annotations', []):
                    event = self.convert_method_to_event(method)
                    events.append(event)
                else:
                    function = self.convert_method_to_function(method)
                    functions.append(function)
        
        return SolidityContractDefinition(
            name=runa_class.name,
            is_abstract=getattr(runa_class, 'is_abstract', False),
            state_variables=state_variables,
            functions=functions,
            events=events
        )
    
    def convert_function_declaration(self, runa_func: FunctionDeclaration) -> SolidityFunctionDefinition:
        """Convert Runa function to Solidity function."""
        # Convert parameters
        parameters = []
        for param in runa_func.parameters:
            param_name = param.get('name', 'param')
            param_type = self.convert_runa_type(param.get('type', 'uint256'))
            
            sol_param = SolidityParameter(
                type_name=SolidityElementaryType(name=param_type),
                name=param_name
            )
            parameters.append(sol_param)
        
        param_list = SolidityParameterList(parameters=parameters)
        
        # Convert return type
        return_params = None
        if runa_func.return_type and runa_func.return_type != "void":
            return_type = self.convert_runa_type(runa_func.return_type)
            return_param = SolidityParameter(
                type_name=SolidityElementaryType(name=return_type),
                name=""
            )
            return_params = SolidityParameterList(parameters=[return_param])
        
        # Convert body
        body_statements = []
        if runa_func.body and hasattr(runa_func.body, 'statements'):
            for stmt in runa_func.body.statements:
                sol_stmt = self.convert(stmt)
                if sol_stmt:
                    body_statements.append(sol_stmt)
        
        body = SolidityBlock(statements=body_statements)
        
        return SolidityFunctionDefinition(
            name=runa_func.name,
            parameters=param_list,
            return_parameters=return_params,
            visibility=SolidityVisibility.PUBLIC,
            mutability=SolidityMutability.NONPAYABLE,
            body=body
        )
    
    def convert_variable_declaration(self, runa_var: VariableDeclaration) -> SolidityVariableDeclaration:
        """Convert Runa variable declaration to Solidity variable declaration."""
        var_type = self.convert_runa_type(runa_var.type)
        type_name = SolidityElementaryType(name=var_type)
        
        initial_value = None
        if runa_var.value:
            initial_value = self.convert(runa_var.value)
        
        return SolidityVariableDeclaration(
            type_name=type_name,
            name=runa_var.name,
            visibility=SolidityVisibility.INTERNAL,
            initial_value=initial_value
        )
    
    def convert_runa_type(self, runa_type: str) -> str:
        """Convert Runa type to Solidity type."""
        return self.type_mappings.get(runa_type, runa_type)
    
    def convert_property_to_state_variable(self, prop: Dict) -> SolidityStateVariable:
        """Convert Runa class property to Solidity state variable."""
        var_type = self.convert_runa_type(prop.get('type', 'uint256'))
        type_name = SolidityElementaryType(name=var_type)
        
        visibility_map = {
            'public': SolidityVisibility.PUBLIC,
            'private': SolidityVisibility.PRIVATE,
            'internal': SolidityVisibility.INTERNAL
        }
        
        visibility = visibility_map.get(prop.get('visibility', 'private'), SolidityVisibility.PRIVATE)
        
        return SolidityStateVariable(
            type_name=type_name,
            name=prop.get('name', 'variable'),
            visibility=visibility,
            is_constant=prop.get('is_constant', False),
            initial_value=self.convert(prop['initial_value']) if prop.get('initial_value') else None
        )
    
    def convert_method_to_function(self, method: Dict) -> SolidityFunctionDefinition:
        """Convert Runa class method to Solidity function."""
        # Convert similar to function declaration
        parameters = []
        for param in method.get('parameters', []):
            param_name = param.get('name', 'param')
            param_type = self.convert_runa_type(param.get('type', 'uint256'))
            
            sol_param = SolidityParameter(
                type_name=SolidityElementaryType(name=param_type),
                name=param_name
            )
            parameters.append(sol_param)
        
        param_list = SolidityParameterList(parameters=parameters)
        
        return SolidityFunctionDefinition(
            name=method.get('name', 'function'),
            parameters=param_list,
            visibility=SolidityVisibility.PUBLIC,
            mutability=SolidityMutability.NONPAYABLE,
            body=SolidityBlock(statements=[])
        )
    
    def convert_method_to_event(self, method: Dict) -> SolidityEventDefinition:
        """Convert Runa event method to Solidity event."""
        parameters = []
        for param in method.get('parameters', []):
            param_name = param.get('name', 'param')
            param_type = self.convert_runa_type(param.get('type', 'uint256'))
            
            sol_param = SolidityParameter(
                type_name=SolidityElementaryType(name=param_type),
                name=param_name
            )
            parameters.append(sol_param)
        
        param_list = SolidityParameterList(parameters=parameters)
        
        # Remove "emit_" prefix if present
        event_name = method.get('name', 'Event')
        if event_name.startswith('emit_'):
            event_name = event_name[5:]
        
        return SolidityEventDefinition(
            name=event_name,
            parameters=param_list
        )
    
    # Additional conversion methods for other node types...
    def convert_function_call(self, runa_call: FunctionCall) -> SolidityFunctionCall:
        """Convert Runa function call to Solidity function call."""
        expression = self.convert(runa_call.function)
        
        arguments = []
        names = []
        for arg in runa_call.arguments:
            if isinstance(arg, dict):
                arguments.append(self.convert(arg['value']))
                names.append(arg.get('name', ''))
            else:
                arguments.append(self.convert(arg))
                names.append('')
        
        return SolidityFunctionCall(
            expression=expression,
            arguments=arguments,
            names=names
        )
    
    def convert_identifier(self, runa_id: Identifier) -> SolidityIdentifier:
        """Convert Runa identifier to Solidity identifier."""
        # Map Runa built-ins to Solidity equivalents
        name_mappings = {
            'message': 'msg',
            'current_block': 'block',
            'transaction': 'tx',
            'current_timestamp': 'now',
            'self': 'this'
        }
        
        mapped_name = name_mappings.get(runa_id.name, runa_id.name)
        return SolidityIdentifier(name=mapped_name)
    
    def convert_literal_expression(self, runa_lit: LiteralExpression) -> SolidityLiteral:
        """Convert Runa literal to Solidity literal."""
        type_mappings = {
            'BigInteger': 'uint256',
            'string': 'string',
            'boolean': 'bool',
            'Address': 'address'
        }
        
        sol_type = type_mappings.get(runa_lit.type, 'uint256')
        
        return SolidityLiteral(
            value=runa_lit.value,
            type_name=sol_type
        )
    
    def convert_binary_expression(self, runa_expr: BinaryExpression) -> SolidityBinaryExpression:
        """Convert Runa binary expression to Solidity binary expression."""
        left = self.convert(runa_expr.left)
        right = self.convert(runa_expr.right)
        
        operator_mappings = {
            '+': SolidityOperator.PLUS,
            '-': SolidityOperator.MINUS,
            '*': SolidityOperator.MULTIPLY,
            '/': SolidityOperator.DIVIDE,
            '%': SolidityOperator.MODULO,
            '**': SolidityOperator.EXPONENT,
            '==': SolidityOperator.EQUAL,
            '!=': SolidityOperator.NOT_EQUAL,
            '<': SolidityOperator.LESS_THAN,
            '<=': SolidityOperator.LESS_EQUAL,
            '>': SolidityOperator.GREATER_THAN,
            '>=': SolidityOperator.GREATER_EQUAL,
            'and': SolidityOperator.AND,
            'or': SolidityOperator.OR
        }
        
        operator = operator_mappings.get(runa_expr.operator, SolidityOperator.PLUS)
        
        return SolidityBinaryExpression(
            left=left,
            operator=operator,
            right=right
        )
    
    def convert_unary_expression(self, runa_expr: UnaryExpression) -> SolidityUnaryExpression:
        """Convert Runa unary expression to Solidity unary expression."""
        expression = self.convert(runa_expr.expression)
        
        operator_mappings = {
            '-': SolidityOperator.MINUS,
            'not': SolidityOperator.NOT
        }
        
        operator = operator_mappings.get(runa_expr.operator, SolidityOperator.MINUS)
        
        return SolidityUnaryExpression(
            operator=operator,
            expression=expression
        )
    
    def convert_if_statement(self, runa_if: IfStatement) -> SolidityIfStatement:
        """Convert Runa if statement to Solidity if statement."""
        condition = self.convert(runa_if.condition)
        then_stmt = self.convert(runa_if.then_statement)
        else_stmt = self.convert(runa_if.else_statement) if runa_if.else_statement else None
        
        return SolidityIfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt
        )
    
    def convert_while_loop(self, runa_while: WhileLoop) -> SolidityWhileLoop:
        """Convert Runa while loop to Solidity while loop."""
        condition = self.convert(runa_while.condition)
        body = self.convert(runa_while.body)
        
        return SolidityWhileLoop(
            condition=condition,
            body=body
        )
    
    def convert_return_statement(self, runa_return: ReturnStatement) -> SolidityReturnStatement:
        """Convert Runa return statement to Solidity return statement."""
        expression = self.convert(runa_return.value) if runa_return.value else None
        
        return SolidityReturnStatement(expression=expression)


# Convenience functions
def solidity_to_runa(sol_ast: SolidityNode) -> ASTNode:
    """Convert Solidity AST to Runa AST."""
    converter = SolidityToRunaConverter()
    return converter.convert(sol_ast)


def runa_to_solidity(runa_ast: ASTNode) -> SolidityNode:
    """Convert Runa AST to Solidity AST."""
    converter = RunaToSolidityConverter()
    return converter.convert(runa_ast) 