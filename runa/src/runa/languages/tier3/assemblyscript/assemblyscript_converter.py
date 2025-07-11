#!/usr/bin/env python3
"""
AssemblyScript to Runa AST Converter

Bidirectional converter between AssemblyScript AST and Runa AST for the universal
translation system.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from ....core.runa_ast import *
from .assemblyscript_ast import *


class AssemblyScriptToRunaConverter:
    """Converts AssemblyScript AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, as_node: AsNode) -> ASTNode:
        """Convert AssemblyScript AST node to Runa AST."""
        try:
            if isinstance(as_node, AsProgram):
                return self._convert_program(as_node)
            elif isinstance(as_node, AsFunction):
                return self._convert_function(as_node)
            elif isinstance(as_node, AsClass):
                return self._convert_class(as_node)
            elif isinstance(as_node, AsVariableDeclaration):
                return self._convert_variable_declaration(as_node)
            elif isinstance(as_node, AsExpression):
                return self._convert_expression(as_node)
            else:
                # Create a simple variable for other node types
                return Variable(identifier="as_node", type_hint=StringType())
        except Exception as e:
            self.logger.error(f"AssemblyScript to Runa conversion failed: {e}")
            raise RuntimeError(f"Failed to convert AssemblyScript to Runa: {e}")
    
    def _convert_program(self, program: AsProgram) -> Program:
        """Convert AssemblyScript program to Runa program."""
        statements = []
        
        # Convert imports
        for import_stmt in program.imports:
            import_var = VariableDeclaration(
                identifier=f"imported module from {import_stmt.source}",
                expression=StringLiteral(import_stmt.source),
                type_hint=StringType()
            )
            statements.append(import_var)
        
        # Convert main statements
        for stmt in program.statements:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        # Add demonstration operations
        demo_stmts = self._create_demo_operations(program)
        statements.extend(demo_stmts)
        
        return Program(statements=statements)
    
    def _convert_statement(self, stmt: AsStatement) -> Optional[Statement]:
        """Convert AssemblyScript statement to Runa statement."""
        if isinstance(stmt, AsFunction):
            return self._convert_function(stmt)
        elif isinstance(stmt, AsClass):
            return self._convert_class(stmt)
        elif isinstance(stmt, AsVariableDeclaration):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, AsReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, AsIfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, AsWhileStatement):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, AsExpressionStatement):
            expr = self._convert_expression(stmt.expression)
            if isinstance(expr, Expression):
                return ExpressionStatement(expression=expr)
        elif isinstance(stmt, AsBlock):
            return self._convert_block(stmt)
        
        return None
    
    def _convert_function(self, func: AsFunction) -> FunctionDeclaration:
        """Convert AssemblyScript function to Runa function."""
        # Convert parameters
        parameters = []
        for param in func.parameters:
            runa_param = Parameter(
                name=param.name,
                type_hint=self._convert_type(param.param_type)
            )
            parameters.append(runa_param)
        
        # Convert body
        body = []
        for stmt in func.body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                body.append(runa_stmt)
        
        return FunctionDeclaration(
            name=func.name,
            parameters=parameters,
            return_type=self._convert_type(func.return_type) if func.return_type else None,
            body=body
        )
    
    def _convert_class(self, cls: AsClass) -> VariableDeclaration:
        """Convert AssemblyScript class to Runa class representation."""
        # Create class dictionary
        class_items = []
        
        # Add class name
        class_items.append(DictionaryItem(
            key=StringLiteral("name"),
            value=StringLiteral(cls.name)
        ))
        
        # Add superclass if present
        if cls.super_class:
            class_items.append(DictionaryItem(
                key=StringLiteral("extends"),
                value=StringLiteral(cls.super_class)
            ))
        
        # Add members
        if cls.members:
            member_items = []
            for member in cls.members:
                member_dict = self._convert_class_member(member)
                if member_dict:
                    member_items.append(member_dict)
            
            if member_items:
                class_items.append(DictionaryItem(
                    key=StringLiteral("members"),
                    value=ListLiteral(elements=member_items)
                ))
        
        # Add export status
        if cls.is_export:
            class_items.append(DictionaryItem(
                key=StringLiteral("exported"),
                value=BooleanLiteral(True)
            ))
        
        return VariableDeclaration(
            identifier=f"class {cls.name}",
            expression=DictionaryLiteral(items=class_items),
            type_hint=DictionaryType(StringType(), StringType())
        )
    
    def _convert_class_member(self, member: AsClassMember) -> Optional[Expression]:
        """Convert class member to dictionary expression."""
        member_items = []
        
        member_items.append(DictionaryItem(
            key=StringLiteral("name"),
            value=StringLiteral(member.name)
        ))
        
        member_items.append(DictionaryItem(
            key=StringLiteral("type"),
            value=StringLiteral(member.member_type)
        ))
        
        member_items.append(DictionaryItem(
            key=StringLiteral("access"),
            value=StringLiteral(member.access_modifier)
        ))
        
        if member.is_static:
            member_items.append(DictionaryItem(
                key=StringLiteral("static"),
                value=BooleanLiteral(True)
            ))
        
        if member.field_type:
            member_items.append(DictionaryItem(
                key=StringLiteral("field_type"),
                value=StringLiteral(member.field_type.full_name)
            ))
        
        return DictionaryLiteral(items=member_items)
    
    def _convert_variable_declaration(self, var_decl: AsVariableDeclaration) -> VariableDeclaration:
        """Convert AssemblyScript variable declaration to Runa."""
        initial_expr = None
        if var_decl.initial_value:
            initial_expr = self._convert_expression(var_decl.initial_value)
        
        return VariableDeclaration(
            identifier=var_decl.name,
            expression=initial_expr,
            type_hint=self._convert_type(var_decl.var_type) if var_decl.var_type else None
        )
    
    def _convert_return_statement(self, ret_stmt: AsReturnStatement) -> ReturnStatement:
        """Convert return statement."""
        value = None
        if ret_stmt.value:
            value = self._convert_expression(ret_stmt.value)
        
        return ReturnStatement(value=value)
    
    def _convert_if_statement(self, if_stmt: AsIfStatement) -> ConditionalStatement:
        """Convert if statement."""
        condition = self._convert_expression(if_stmt.condition)
        then_body = []
        
        if if_stmt.then_statement:
            then_stmt = self._convert_statement(if_stmt.then_statement)
            if then_stmt:
                then_body.append(then_stmt)
        
        else_body = []
        if if_stmt.else_statement:
            else_stmt = self._convert_statement(if_stmt.else_statement)
            if else_stmt:
                else_body.append(else_stmt)
        
        return ConditionalStatement(
            condition=condition,
            if_body=then_body,
            else_body=else_body if else_body else None
        )
    
    def _convert_while_statement(self, while_stmt: AsWhileStatement) -> LoopStatement:
        """Convert while statement."""
        condition = self._convert_expression(while_stmt.condition)
        body = []
        
        if while_stmt.body:
            body_stmt = self._convert_statement(while_stmt.body)
            if body_stmt:
                body.append(body_stmt)
        
        return LoopStatement(
            loop_type="while",
            condition=condition,
            body=body
        )
    
    def _convert_block(self, block: AsBlock) -> List[Statement]:
        """Convert block statement."""
        statements = []
        for stmt in block.statements:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        return statements
    
    def _convert_expression(self, expr: AsExpression) -> Expression:
        """Convert AssemblyScript expression to Runa expression."""
        if isinstance(expr, AsLiteral):
            if expr.literal_type == "number":
                if isinstance(expr.value, int):
                    return IntegerLiteral(expr.value)
                else:
                    return FloatLiteral(float(expr.value))
            elif expr.literal_type == "string":
                return StringLiteral(expr.value)
            elif expr.literal_type == "boolean":
                return BooleanLiteral(expr.value)
            else:
                return StringLiteral(str(expr.value))
        
        elif isinstance(expr, AsIdentifier):
            return Variable(identifier=expr.name)
        
        elif isinstance(expr, AsBinaryExpression):
            left = self._convert_expression(expr.left)
            right = self._convert_expression(expr.right)
            
            # Map operators to Runa
            operator_map = {
                '+': 'plus',
                '-': 'minus', 
                '*': 'multiplied by',
                '/': 'divided by',
                '%': 'modulo',
                '==': 'is equal to',
                '!=': 'is not equal to',
                '<': 'is less than',
                '>': 'is greater than',
                '<=': 'is less than or equal to',
                '>=': 'is greater than or equal to',
                '&&': 'and',
                '||': 'or'
            }
            
            runa_op = operator_map.get(expr.operator, expr.operator)
            return BinaryOperation(left=left, operator=runa_op, right=right)
        
        elif isinstance(expr, AsUnaryExpression):
            operand = self._convert_expression(expr.operand)
            return UnaryOperation(operator=expr.operator, operand=operand)
        
        elif isinstance(expr, AsCallExpression):
            function = self._convert_expression(expr.function)
            arguments = [self._convert_expression(arg) for arg in expr.arguments]
            
            # Extract function name for Runa-style call
            func_name = "function call"
            if isinstance(expr.function, AsIdentifier):
                func_name = expr.function.name
            
            return FunctionCall(function_name=func_name, arguments=arguments)
        
        elif isinstance(expr, AsMemberExpression):
            obj = self._convert_expression(expr.object)
            prop = self._convert_expression(expr.property)
            
            # Convert to Runa member access
            if isinstance(expr.property, AsIdentifier):
                return Variable(identifier=f"{obj}.{expr.property.name}")
            else:
                return Variable(identifier="member access")
        
        elif isinstance(expr, AsArrayExpression):
            elements = [self._convert_expression(elem) for elem in expr.elements if elem]
            return ListLiteral(elements=elements)
        
        elif isinstance(expr, AsObjectExpression):
            items = []
            for prop in expr.properties:
                key = self._convert_expression(prop.key)
                value = self._convert_expression(prop.value)
                
                if isinstance(key, StringLiteral):
                    items.append(DictionaryItem(key=key, value=value))
                else:
                    items.append(DictionaryItem(key=StringLiteral(str(key)), value=value))
            
            return DictionaryLiteral(items=items)
        
        else:
            return StringLiteral(str(expr))
    
    def _convert_type(self, as_type: Optional[AsType]) -> Optional[Type]:
        """Convert AssemblyScript type to Runa type."""
        if not as_type:
            return None
        
        # Map AssemblyScript types to Runa types
        type_map = {
            # Integer types -> Integer
            'i8': IntegerType(), 'u8': IntegerType(), 'i16': IntegerType(), 'u16': IntegerType(),
            'i32': IntegerType(), 'u32': IntegerType(), 'i64': IntegerType(), 'u64': IntegerType(),
            'isize': IntegerType(), 'usize': IntegerType(),
            
            # Float types -> Float
            'f32': FloatType(), 'f64': FloatType(),
            
            # Other types
            'bool': BooleanType(),
            'string': StringType(),
            'void': None,
            
            # Arrays
            'Array': ListType(StringType()),  # Generic array
        }
        
        base_type = type_map.get(as_type.name, StringType())
        
        if as_type.is_array and base_type:
            return ListType(base_type)
        
        return base_type
    
    def _create_demo_operations(self, program: AsProgram) -> List[Statement]:
        """Create demonstration operations for AssemblyScript processing."""
        statements = []
        
        # Find functions and create calls
        for stmt in program.statements:
            if isinstance(stmt, AsFunction):
                # Create function call demonstration
                call_stmt = VariableDeclaration(
                    identifier=f"result of {stmt.name}",
                    expression=FunctionCall(
                        function_name=stmt.name,
                        arguments=[StringLiteral("example input")]
                    ),
                    type_hint=self._convert_type(stmt.return_type) if stmt.return_type else StringType()
                )
                statements.append(call_stmt)
        
        # Find classes and create instantiation examples
        for stmt in program.statements:
            if isinstance(stmt, AsClass):
                # Create class instantiation
                instance_stmt = VariableDeclaration(
                    identifier=f"instance of {stmt.name}",
                    expression=FunctionCall(
                        function_name="create instance",
                        arguments=[StringLiteral(stmt.name)]
                    ),
                    type_hint=StringType()
                )
                statements.append(instance_stmt)
        
        # Add type conversion examples
        if any(isinstance(stmt, AsVariableDeclaration) for stmt in program.statements):
            conversion_stmt = VariableDeclaration(
                identifier="type conversion example",
                expression=FunctionCall(
                    function_name="convert to WebAssembly type",
                    arguments=[
                        StringLiteral("i32"),
                        IntegerLiteral(42)
                    ]
                ),
                type_hint=IntegerType()
            )
            statements.append(conversion_stmt)
        
        return statements


class RunaToAssemblyScriptConverter:
    """Converts Runa AST to AssemblyScript AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: ASTNode) -> AsNode:
        """Convert Runa AST node to AssemblyScript AST."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, FunctionDeclaration):
                return self._convert_function(runa_node)
            elif isinstance(runa_node, VariableDeclaration):
                return self._convert_variable_declaration(runa_node)
            else:
                # Create a simple identifier for other types
                return AsIdentifier(name="runa_node")
        except Exception as e:
            self.logger.error(f"Runa to AssemblyScript conversion failed: {e}")
            raise RuntimeError(f"Failed to convert Runa to AssemblyScript: {e}")
    
    def _convert_program(self, program: Program) -> AsProgram:
        """Convert Runa program to AssemblyScript program."""
        statements = []
        imports = []
        exports = []
        
        for stmt in program.statements:
            if isinstance(stmt, FunctionDeclaration):
                as_func = self._convert_function(stmt)
                statements.append(as_func)
            elif isinstance(stmt, VariableDeclaration):
                # Check if this represents a class
                if stmt.identifier.startswith("class ") and isinstance(stmt.expression, DictionaryLiteral):
                    as_class = self._convert_class_from_dict(stmt)
                    if as_class:
                        statements.append(as_class)
                else:
                    as_var = self._convert_variable_declaration(stmt)
                    statements.append(as_var)
        
        return AsProgram(statements=statements, imports=imports, exports=exports)
    
    def _convert_function(self, func: FunctionDeclaration) -> AsFunction:
        """Convert Runa function to AssemblyScript function."""
        # Convert parameters
        parameters = []
        for param in func.parameters:
            as_param = AsParameter(
                name=param.name,
                param_type=self._convert_type_to_as(param.type_hint)
            )
            parameters.append(as_param)
        
        # Convert body
        body = []
        for stmt in func.body:
            as_stmt = self._convert_statement(stmt)
            if as_stmt:
                body.append(as_stmt)
        
        return AsFunction(
            name=func.name,
            parameters=parameters,
            return_type=self._convert_type_to_as(func.return_type),
            body=body
        )
    
    def _convert_class_from_dict(self, var_decl: VariableDeclaration) -> Optional[AsClass]:
        """Convert dictionary representation back to AssemblyScript class."""
        if not isinstance(var_decl.expression, DictionaryLiteral):
            return None
        
        class_name = var_decl.identifier.replace("class ", "")
        super_class = None
        members = []
        
        # Extract class properties from dictionary
        for item in var_decl.expression.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "extends" and isinstance(item.value, StringLiteral):
                    super_class = item.value.value
                elif key == "members" and isinstance(item.value, ListLiteral):
                    for member_expr in item.value.elements:
                        if isinstance(member_expr, DictionaryLiteral):
                            member = self._convert_class_member_from_dict(member_expr)
                            if member:
                                members.append(member)
        
        return AsClass(name=class_name, super_class=super_class, members=members)
    
    def _convert_class_member_from_dict(self, member_dict: DictionaryLiteral) -> Optional[AsClassMember]:
        """Convert dictionary representation to class member."""
        name = ""
        member_type = "field"
        access_modifier = "public"
        field_type = None
        
        for item in member_dict.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "name" and isinstance(item.value, StringLiteral):
                    name = item.value.value
                elif key == "type" and isinstance(item.value, StringLiteral):
                    member_type = item.value.value
                elif key == "access" and isinstance(item.value, StringLiteral):
                    access_modifier = item.value.value
                elif key == "field_type" and isinstance(item.value, StringLiteral):
                    field_type = string_to_as_type(item.value.value)
        
        if name:
            return AsClassMember(
                name=name,
                member_type=member_type,
                access_modifier=access_modifier,
                field_type=field_type
            )
        
        return None
    
    def _convert_variable_declaration(self, var_decl: VariableDeclaration) -> AsVariableDeclaration:
        """Convert Runa variable declaration to AssemblyScript."""
        initial_value = None
        if var_decl.expression:
            initial_value = self._convert_expression(var_decl.expression)
        
        return AsVariableDeclaration(
            name=var_decl.identifier,
            var_type=self._convert_type_to_as(var_decl.type_hint),
            initial_value=initial_value,
            is_const=False,  # Default to let
            is_let=True
        )
    
    def _convert_statement(self, stmt: Statement) -> Optional[AsStatement]:
        """Convert Runa statement to AssemblyScript statement."""
        if isinstance(stmt, ReturnStatement):
            value = None
            if stmt.value:
                value = self._convert_expression(stmt.value)
            return AsReturnStatement(value=value)
        
        elif isinstance(stmt, ConditionalStatement):
            condition = self._convert_expression(stmt.condition)
            
            then_stmt = None
            if stmt.if_body:
                if len(stmt.if_body) == 1:
                    then_stmt = self._convert_statement(stmt.if_body[0])
                else:
                    block_stmts = [self._convert_statement(s) for s in stmt.if_body if s]
                    then_stmt = AsBlock(statements=[s for s in block_stmts if s])
            
            else_stmt = None
            if stmt.else_body:
                if len(stmt.else_body) == 1:
                    else_stmt = self._convert_statement(stmt.else_body[0])
                else:
                    block_stmts = [self._convert_statement(s) for s in stmt.else_body if s]
                    else_stmt = AsBlock(statements=[s for s in block_stmts if s])
            
            return AsIfStatement(condition=condition, then_statement=then_stmt, else_statement=else_stmt)
        
        elif isinstance(stmt, VariableDeclaration):
            return self._convert_variable_declaration(stmt)
        
        elif isinstance(stmt, ExpressionStatement):
            expr = self._convert_expression(stmt.expression)
            return AsExpressionStatement(expression=expr)
        
        return None
    
    def _convert_expression(self, expr: Expression) -> AsExpression:
        """Convert Runa expression to AssemblyScript expression."""
        if isinstance(expr, IntegerLiteral):
            return AsLiteral(value=expr.value, literal_type="number")
        
        elif isinstance(expr, FloatLiteral):
            return AsLiteral(value=expr.value, literal_type="number")
        
        elif isinstance(expr, StringLiteral):
            return AsLiteral(value=expr.value, literal_type="string")
        
        elif isinstance(expr, BooleanLiteral):
            return AsLiteral(value=expr.value, literal_type="boolean")
        
        elif isinstance(expr, Variable):
            return AsIdentifier(name=expr.identifier)
        
        elif isinstance(expr, BinaryOperation):
            left = self._convert_expression(expr.left)
            right = self._convert_expression(expr.right)
            
            # Map Runa operators to AssemblyScript
            operator_map = {
                'plus': '+',
                'minus': '-',
                'multiplied by': '*',
                'divided by': '/',
                'modulo': '%',
                'is equal to': '==',
                'is not equal to': '!=',
                'is less than': '<',
                'is greater than': '>',
                'is less than or equal to': '<=',
                'is greater than or equal to': '>=',
                'and': '&&',
                'or': '||'
            }
            
            as_op = operator_map.get(expr.operator, expr.operator)
            return AsBinaryExpression(left=left, operator=as_op, right=right)
        
        elif isinstance(expr, FunctionCall):
            function = AsIdentifier(name=expr.function_name)
            arguments = [self._convert_expression(arg) for arg in expr.arguments]
            return AsCallExpression(function=function, arguments=arguments)
        
        elif isinstance(expr, ListLiteral):
            elements = [self._convert_expression(elem) for elem in expr.elements]
            return AsArrayExpression(elements=elements)
        
        elif isinstance(expr, DictionaryLiteral):
            properties = []
            for item in expr.items:
                key = self._convert_expression(item.key)
                value = self._convert_expression(item.value)
                properties.append(AsProperty(key=key, value=value))
            return AsObjectExpression(properties=properties)
        
        else:
            return AsIdentifier(name="unknown")
    
    def _convert_type_to_as(self, runa_type: Optional[Type]) -> AsType:
        """Convert Runa type to AssemblyScript type."""
        if not runa_type:
            return create_as_type("any")
        
        if isinstance(runa_type, IntegerType):
            return create_as_type("i32")  # Default integer type
        elif isinstance(runa_type, FloatType):
            return create_as_type("f64")  # Default float type
        elif isinstance(runa_type, BooleanType):
            return create_as_type("bool")
        elif isinstance(runa_type, StringType):
            return create_as_type("string")
        elif isinstance(runa_type, ListType):
            element_type = self._convert_type_to_as(runa_type.element_type)
            return create_as_type("Array", [element_type])
        elif isinstance(runa_type, DictionaryType):
            return create_as_type("Map")  # Simplified mapping
        else:
            return create_as_type("any")


# Convenience functions
def assemblyscript_to_runa(as_node: AsNode) -> ASTNode:
    """Convert AssemblyScript AST to Runa AST."""
    converter = AssemblyScriptToRunaConverter()
    return converter.convert(as_node)


def runa_to_assemblyscript(runa_node: ASTNode) -> AsNode:
    """Convert Runa AST to AssemblyScript AST."""
    converter = RunaToAssemblyScriptConverter()
    return converter.convert(runa_node)


def assemblyscript_program_to_runa_program(program: AsProgram) -> Program:
    """Convert AssemblyScript program to Runa program."""
    converter = AssemblyScriptToRunaConverter()
    return converter.convert(program)


def runa_program_to_assemblyscript_program(program: Program) -> AsProgram:
    """Convert Runa program to AssemblyScript program."""
    converter = RunaToAssemblyScriptConverter()
    result = converter.convert(program)
    if isinstance(result, AsProgram):
        return result
    else:
        # Wrap in program
        return AsProgram(statements=[result] if isinstance(result, AsStatement) else [])