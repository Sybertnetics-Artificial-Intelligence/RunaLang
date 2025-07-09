#!/usr/bin/env python3
"""
Python ↔ Runa Bidirectional Converter

Converts between Python AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .py_ast import *
from ....core.runa_ast import *


class PyToRunaConverter:
    """Converts Python AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.scope_stack = []
    
    def convert(self, py_ast: PyModule) -> Program:
        """Convert Python module to Runa program."""
        statements = []
        
        for stmt in py_ast.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements)
    
    def convert_statement(self, stmt: PyStatement) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert Python statement to Runa statement."""
        if isinstance(stmt, PyAssign):
            return self._convert_assign(stmt)
        elif isinstance(stmt, PyAnnAssign):
            return self._convert_ann_assign(stmt)
        elif isinstance(stmt, PyAugAssign):
            return self._convert_aug_assign(stmt)
        elif isinstance(stmt, PyFunctionDef):
            return self._convert_functiondef(stmt)
        elif isinstance(stmt, PyAsyncFunctionDef):
            return self._convert_async_functiondef(stmt)
        elif isinstance(stmt, PyClassDef):
            return self._convert_classdef(stmt)
        elif isinstance(stmt, PyReturn):
            return self._convert_return(stmt)
        elif isinstance(stmt, PyIf):
            return self._convert_if(stmt)
        elif isinstance(stmt, PyWhile):
            return self._convert_while(stmt)
        elif isinstance(stmt, PyFor):
            return self._convert_for(stmt)
        elif isinstance(stmt, PyTry):
            return self._convert_try(stmt)
        elif isinstance(stmt, PyWith):
            return self._convert_with(stmt)
        elif isinstance(stmt, PyRaise):
            return self._convert_raise(stmt)
        elif isinstance(stmt, PyAssert):
            return self._convert_assert(stmt)
        elif isinstance(stmt, PyImport):
            return self._convert_import(stmt)
        elif isinstance(stmt, PyImportFrom):
            return self._convert_import_from(stmt)
        elif isinstance(stmt, PyExpressionStmt):
            return self._convert_expression_stmt(stmt)
        elif isinstance(stmt, PyPass):
            return RunaExpressionStatement(RunaLiteral("pass", "pass"))
        elif isinstance(stmt, PyBreak):
            return RunaBreak()
        elif isinstance(stmt, PyContinue):
            return RunaContinue()
        elif isinstance(stmt, PyGlobal):
            return RunaExpressionStatement(RunaLiteral(f"global {', '.join(stmt.names)}", "global"))
        elif isinstance(stmt, PyNonlocal):
            return RunaExpressionStatement(RunaLiteral(f"nonlocal {', '.join(stmt.names)}", "nonlocal"))
        
        return None
    
    def convert_expression(self, expr: PyExpression) -> RunaExpression:
        """Convert Python expression to Runa expression."""
        if isinstance(expr, PyConstant):
            return self._convert_constant(expr)
        elif isinstance(expr, PyName):
            return self._convert_name(expr)
        elif isinstance(expr, PyBinOp):
            return self._convert_binop(expr)
        elif isinstance(expr, PyUnaryOp):
            return self._convert_unaryop(expr)
        elif isinstance(expr, PyCompare):
            return self._convert_compare(expr)
        elif isinstance(expr, PyCall):
            return self._convert_call(expr)
        elif isinstance(expr, PyAttribute):
            return self._convert_attribute(expr)
        elif isinstance(expr, PySubscript):
            return self._convert_subscript(expr)
        elif isinstance(expr, PyList):
            return self._convert_list(expr)
        elif isinstance(expr, PyTuple):
            return self._convert_tuple(expr)
        elif isinstance(expr, PyDict):
            return self._convert_dict(expr)
        elif isinstance(expr, PySet):
            return self._convert_set(expr)
        elif isinstance(expr, PyLambda):
            return self._convert_lambda(expr)
        elif isinstance(expr, PyIfExp):
            return self._convert_ifexp(expr)
        elif isinstance(expr, PyListComp):
            return self._convert_listcomp(expr)
        elif isinstance(expr, PyAwait):
            return self._convert_await(expr)
        elif isinstance(expr, PyYield):
            return self._convert_yield(expr)
        
        # Default fallback
        return RunaLiteral(str(expr), str(expr))
    
    def _convert_assign(self, stmt: PyAssign) -> RunaStatement:
        """Convert assignment statement."""
        value = self.convert_expression(stmt.value)
        
        # Handle multiple targets
        if len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, PyName):
                return RunaLet(target.id, value)
            else:
                # Complex assignment target
                target_expr = self.convert_expression(target)
                return RunaAssignment(target_expr, value)
        else:
            # Multiple assignment - create multiple let statements
            statements = []
            for target in stmt.targets:
                if isinstance(target, PyName):
                    statements.append(RunaLet(target.id, value))
                else:
                    target_expr = self.convert_expression(target)
                    statements.append(RunaAssignment(target_expr, value))
            return statements
    
    def _convert_ann_assign(self, stmt: PyAnnAssign) -> RunaStatement:
        """Convert annotated assignment statement."""
        if isinstance(stmt.target, PyName):
            variable_type = self._convert_type_annotation(stmt.annotation)
            value = self.convert_expression(stmt.value) if stmt.value else None
            return RunaLet(stmt.target.id, value, variable_type)
        else:
            # Complex assignment target
            target_expr = self.convert_expression(stmt.target)
            value = self.convert_expression(stmt.value) if stmt.value else None
            return RunaAssignment(target_expr, value)
    
    def _convert_aug_assign(self, stmt: PyAugAssign) -> RunaStatement:
        """Convert augmented assignment statement."""
        target = self.convert_expression(stmt.target)
        value = self.convert_expression(stmt.value)
        
        # Convert operator
        operator_map = {
            PyOperator.ADD: "plus",
            PyOperator.SUB: "minus",
            PyOperator.MULT: "times",
            PyOperator.DIV: "divided by",
            PyOperator.MOD: "modulo",
            PyOperator.POW: "power",
            PyOperator.FLOORDIV: "floor divided by",
        }
        
        operator = operator_map.get(stmt.op, "plus")
        binary_op = RunaBinaryOperation(target, operator, value)
        
        return RunaAssignment(target, binary_op)
    
    def _convert_functiondef(self, stmt: PyFunctionDef) -> RunaProcessDefinition:
        """Convert function definition."""
        # Convert parameters
        params = []
        for arg in stmt.args.args:
            param_type = self._convert_type_annotation(arg.annotation) if arg.annotation else RunaType("Any")
            params.append(RunaParameter(arg.arg, param_type))
        
        # Convert defaults
        defaults = [self.convert_expression(default) for default in stmt.args.defaults]
        
        # Apply defaults to parameters
        if defaults:
            num_defaults = len(defaults)
            for i, default in enumerate(defaults):
                param_index = len(params) - num_defaults + i
                if param_index < len(params):
                    params[param_index].default_value = default
        
        # Convert return type
        return_type = self._convert_type_annotation(stmt.returns) if stmt.returns else RunaType("Any")
        
        # Convert body
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaProcessDefinition(
            name=stmt.name,
            parameters=params,
            return_type=return_type,
            body=RunaBlock(body_statements)
        )
    
    def _convert_async_functiondef(self, stmt: PyAsyncFunctionDef) -> RunaProcessDefinition:
        """Convert async function definition."""
        # Convert like regular function but mark as async
        process_def = self._convert_functiondef(stmt)
        process_def.is_async = True
        return process_def
    
    def _convert_classdef(self, stmt: PyClassDef) -> RunaClassDefinition:
        """Convert class definition."""
        # Convert base classes
        base_class = None
        interfaces = []
        
        if stmt.bases:
            base_class = self._convert_type_annotation(stmt.bases[0])
            interfaces = [self._convert_type_annotation(base) for base in stmt.bases[1:]]
        
        # Convert members
        members = []
        for member in stmt.body:
            converted = self.convert_statement(member)
            if converted:
                if isinstance(converted, list):
                    members.extend(converted)
                else:
                    members.append(converted)
        
        return RunaClassDefinition(
            name=stmt.name,
            base_class=base_class,
            interfaces=interfaces,
            members=members
        )
    
    def _convert_return(self, stmt: PyReturn) -> RunaReturn:
        """Convert return statement."""
        value = self.convert_expression(stmt.value) if stmt.value else None
        return RunaReturn(value)
    
    def _convert_if(self, stmt: PyIf) -> RunaConditional:
        """Convert if statement."""
        condition = self.convert_expression(stmt.test)
        
        then_statements = []
        for then_stmt in stmt.body:
            converted = self.convert_statement(then_stmt)
            if converted:
                if isinstance(converted, list):
                    then_statements.extend(converted)
                else:
                    then_statements.append(converted)
        then_branch = RunaBlock(then_statements)
        
        else_branch = None
        if stmt.orelse:
            else_statements = []
            for else_stmt in stmt.orelse:
                converted = self.convert_statement(else_stmt)
                if converted:
                    if isinstance(converted, list):
                        else_statements.extend(converted)
                    else:
                        else_statements.append(converted)
            else_branch = RunaBlock(else_statements)
        
        return RunaConditional(condition, then_branch, else_branch)
    
    def _convert_while(self, stmt: PyWhile) -> RunaWhileLoop:
        """Convert while statement."""
        condition = self.convert_expression(stmt.test)
        
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaWhileLoop(condition, RunaBlock(body_statements))
    
    def _convert_for(self, stmt: PyFor) -> RunaForLoop:
        """Convert for statement."""
        # Python for loops are different from C-style for loops
        # Convert to a while loop with iteration
        condition = RunaLiteral(True, "True")
        
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaForLoop(condition, RunaBlock(body_statements))
    
    def _convert_try(self, stmt: PyTry) -> RunaTryCatch:
        """Convert try statement."""
        try_statements = []
        for try_stmt in stmt.body:
            converted = self.convert_statement(try_stmt)
            if converted:
                if isinstance(converted, list):
                    try_statements.extend(converted)
                else:
                    try_statements.append(converted)
        try_block = RunaBlock(try_statements)
        
        catch_block = None
        catch_parameter = None
        if stmt.handlers:
            # Use first handler
            handler = stmt.handlers[0]
            catch_parameter = handler.name
            
            catch_statements = []
            for catch_stmt in handler.body:
                converted = self.convert_statement(catch_stmt)
                if converted:
                    if isinstance(converted, list):
                        catch_statements.extend(converted)
                    else:
                        catch_statements.append(converted)
            catch_block = RunaBlock(catch_statements)
        
        finally_block = None
        if stmt.finalbody:
            finally_statements = []
            for finally_stmt in stmt.finalbody:
                converted = self.convert_statement(finally_stmt)
                if converted:
                    if isinstance(converted, list):
                        finally_statements.extend(converted)
                    else:
                        finally_statements.append(converted)
            finally_block = RunaBlock(finally_statements)
        
        return RunaTryCatch(try_block, catch_block, catch_parameter, None, finally_block)
    
    def _convert_with(self, stmt: PyWith) -> RunaStatement:
        """Convert with statement."""
        # Simplified conversion - treat as a block
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        return RunaBlock(body_statements)
    
    def _convert_raise(self, stmt: PyRaise) -> RunaThrow:
        """Convert raise statement."""
        value = self.convert_expression(stmt.exc) if stmt.exc else RunaLiteral("Exception", "Exception")
        return RunaThrow(value)
    
    def _convert_assert(self, stmt: PyAssert) -> RunaStatement:
        """Convert assert statement."""
        # Convert to an if statement that throws
        condition = self.convert_expression(stmt.test)
        msg = self.convert_expression(stmt.msg) if stmt.msg else RunaLiteral("AssertionError", "AssertionError")
        
        # If not condition, throw msg
        not_condition = RunaUnaryOperation("not", condition)
        throw_stmt = RunaThrow(msg)
        
        return RunaConditional(not_condition, RunaBlock([throw_stmt]))
    
    def _convert_import(self, stmt: PyImport) -> RunaStatement:
        """Convert import statement."""
        imports = []
        for alias in stmt.names:
            import_name = alias.asname if alias.asname else alias.name
            imports.append(import_name)
        
        return RunaImport("", imports)
    
    def _convert_import_from(self, stmt: PyImportFrom) -> RunaStatement:
        """Convert import from statement."""
        module = stmt.module or ""
        imports = []
        for alias in stmt.names:
            import_name = alias.asname if alias.asname else alias.name
            imports.append(import_name)
        
        return RunaImport(module, imports)
    
    def _convert_expression_stmt(self, stmt: PyExpressionStmt) -> RunaExpressionStatement:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.value)
        return RunaExpressionStatement(expr)
    
    def _convert_constant(self, expr: PyConstant) -> RunaLiteral:
        """Convert constant expression."""
        if expr.value is None:
            return RunaLiteral(None, "None", "null")
        elif isinstance(expr.value, bool):
            return RunaLiteral(expr.value, "True" if expr.value else "False", "boolean")
        elif isinstance(expr.value, (int, float)):
            return RunaLiteral(expr.value, str(expr.value), "number")
        elif isinstance(expr.value, str):
            return RunaLiteral(expr.value, f'"{expr.value}"', "string")
        else:
            return RunaLiteral(expr.value, str(expr.value), "unknown")
    
    def _convert_name(self, expr: PyName) -> RunaIdentifier:
        """Convert name expression."""
        return RunaIdentifier(expr.id)
    
    def _convert_binop(self, expr: PyBinOp) -> RunaBinaryOperation:
        """Convert binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        operator_map = {
            PyOperator.ADD: "plus",
            PyOperator.SUB: "minus",
            PyOperator.MULT: "times",
            PyOperator.DIV: "divided by",
            PyOperator.MOD: "modulo",
            PyOperator.POW: "power",
            PyOperator.FLOORDIV: "floor divided by",
            PyOperator.LSHIFT: "left shift",
            PyOperator.RSHIFT: "right shift",
            PyOperator.BITOR: "bitwise or",
            PyOperator.BITXOR: "bitwise xor",
            PyOperator.BITAND: "bitwise and",
            PyOperator.MATMULT: "matrix multiply",
        }
        
        operator = operator_map.get(expr.op, "plus")
        return RunaBinaryOperation(left, operator, right)
    
    def _convert_unaryop(self, expr: PyUnaryOp) -> RunaUnaryOperation:
        """Convert unary operation."""
        operand = self.convert_expression(expr.operand)
        
        operator_map = {
            PyOperator.UADD: "positive",
            PyOperator.USUB: "negative",
            PyOperator.NOT: "not",
            PyOperator.INVERT: "bitwise not",
        }
        
        operator = operator_map.get(expr.op, "not")
        return RunaUnaryOperation(operator, operand)
    
    def _convert_compare(self, expr: PyCompare) -> RunaBinaryOperation:
        """Convert comparison expression."""
        left = self.convert_expression(expr.left)
        
        # Handle multiple comparisons (chain them)
        result = left
        for i, (op, comparator) in enumerate(zip(expr.ops, expr.comparators)):
            right = self.convert_expression(comparator)
            
            operator_map = {
                PyOperator.EQ: "is equal to",
                PyOperator.NOT_EQ: "is not equal to",
                PyOperator.LT: "is less than",
                PyOperator.LTE: "is less than or equal to",
                PyOperator.GT: "is greater than",
                PyOperator.GTE: "is greater than or equal to",
                PyOperator.IS: "is",
                PyOperator.IS_NOT: "is not",
                PyOperator.IN: "in",
                PyOperator.NOT_IN: "not in",
            }
            
            operator = operator_map.get(op, "is equal to")
            
            if i == 0:
                result = RunaBinaryOperation(left, operator, right)
            else:
                # Chain with 'and'
                new_comparison = RunaBinaryOperation(result, operator, right)
                result = RunaBinaryOperation(result, "and", new_comparison)
        
        return result
    
    def _convert_call(self, expr: PyCall) -> RunaFunctionCall:
        """Convert call expression."""
        if isinstance(expr.func, PyName):
            func_name = expr.func.id
        elif isinstance(expr.func, PyAttribute):
            # Method call
            object_expr = self.convert_expression(expr.func.value)
            return RunaMethodCall(object_expr, expr.func.attr, [self.convert_expression(arg) for arg in expr.args])
        else:
            func_name = "unknown_function"
        
        args = [self.convert_expression(arg) for arg in expr.args]
        return RunaFunctionCall(func_name, args)
    
    def _convert_attribute(self, expr: PyAttribute) -> RunaMemberAccess:
        """Convert attribute access."""
        object_expr = self.convert_expression(expr.value)
        return RunaMemberAccess(object_expr, expr.attr)
    
    def _convert_subscript(self, expr: PySubscript) -> RunaArrayAccess:
        """Convert subscript access."""
        array_expr = self.convert_expression(expr.value)
        index_expr = self.convert_expression(expr.slice)
        return RunaArrayAccess(array_expr, index_expr)
    
    def _convert_list(self, expr: PyList) -> RunaArrayLiteral:
        """Convert list literal."""
        elements = [self.convert_expression(elt) for elt in expr.elts]
        return RunaArrayLiteral(elements)
    
    def _convert_tuple(self, expr: PyTuple) -> RunaArrayLiteral:
        """Convert tuple literal (as array)."""
        elements = [self.convert_expression(elt) for elt in expr.elts]
        return RunaArrayLiteral(elements)
    
    def _convert_dict(self, expr: PyDict) -> RunaObjectLiteral:
        """Convert dictionary literal."""
        properties = []
        for key, value in zip(expr.keys, expr.values):
            if key:
                key_str = str(key.value) if isinstance(key, PyConstant) else "unknown"
                value_expr = self.convert_expression(value)
                properties.append(RunaObjectProperty(key_str, value_expr))
        
        return RunaObjectLiteral(properties)
    
    def _convert_set(self, expr: PySet) -> RunaArrayLiteral:
        """Convert set literal (as array)."""
        elements = [self.convert_expression(elt) for elt in expr.elts]
        return RunaArrayLiteral(elements)
    
    def _convert_lambda(self, expr: PyLambda) -> RunaLambda:
        """Convert lambda expression."""
        params = []
        for arg in expr.args.args:
            param_type = self._convert_type_annotation(arg.annotation) if arg.annotation else RunaType("Any")
            params.append(RunaParameter(arg.arg, param_type))
        
        body = RunaBlock([RunaReturn(self.convert_expression(expr.body))])
        return RunaLambda(params, body)
    
    def _convert_ifexp(self, expr: PyIfExp) -> RunaConditionalExpression:
        """Convert conditional expression."""
        condition = self.convert_expression(expr.test)
        then_value = self.convert_expression(expr.body)
        else_value = self.convert_expression(expr.orelse)
        
        return RunaConditionalExpression(condition, then_value, else_value)
    
    def _convert_listcomp(self, expr: PyListComp) -> RunaArrayLiteral:
        """Convert list comprehension (simplified)."""
        # For now, just return the element
        element = self.convert_expression(expr.elt)
        return RunaArrayLiteral([element])
    
    def _convert_await(self, expr: PyAwait) -> RunaAwait:
        """Convert await expression."""
        expression = self.convert_expression(expr.value)
        return RunaAwait(expression)
    
    def _convert_yield(self, expr: PyYield) -> RunaYield:
        """Convert yield expression."""
        value = self.convert_expression(expr.value) if expr.value else None
        return RunaYield(value)
    
    def _convert_type_annotation(self, annotation: PyExpression) -> RunaType:
        """Convert type annotation."""
        if isinstance(annotation, PyName):
            type_map = {
                "int": "Integer",
                "float": "Float",
                "str": "String",
                "bool": "Boolean",
                "list": "List",
                "dict": "Dictionary",
                "tuple": "Tuple",
                "set": "Set",
                "None": "Null",
            }
            return RunaType(type_map.get(annotation.id, annotation.id))
        else:
            return RunaType("Any")


class RunaToPyConverter:
    """Converts Runa AST to Python AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
    
    def convert(self, runa_ast: Program) -> PyModule:
        """Convert Runa program to Python module."""
        statements = []
        
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return PyModule(statements)
    
    def convert_statement(self, stmt: RunaStatement) -> Union[PyStatement, List[PyStatement], None]:
        """Convert Runa statement to Python statement."""
        if isinstance(stmt, RunaLet):
            return self._convert_let(stmt)
        elif isinstance(stmt, RunaAssignment):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, RunaProcessDefinition):
            return self._convert_process_definition(stmt)
        elif isinstance(stmt, RunaClassDefinition):
            return self._convert_class_definition(stmt)
        elif isinstance(stmt, RunaReturn):
            return self._convert_return(stmt)
        elif isinstance(stmt, RunaConditional):
            return self._convert_conditional(stmt)
        elif isinstance(stmt, RunaWhileLoop):
            return self._convert_while_loop(stmt)
        elif isinstance(stmt, RunaForLoop):
            return self._convert_for_loop(stmt)
        elif isinstance(stmt, RunaTryCatch):
            return self._convert_try_catch(stmt)
        elif isinstance(stmt, RunaThrow):
            return self._convert_throw(stmt)
        elif isinstance(stmt, RunaImport):
            return self._convert_import(stmt)
        elif isinstance(stmt, RunaExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, RunaBreak):
            return PyBreak()
        elif isinstance(stmt, RunaContinue):
            return PyContinue()
        elif isinstance(stmt, RunaBlock):
            return self._convert_block(stmt)
        
        return None
    
    def convert_expression(self, expr: RunaExpression) -> PyExpression:
        """Convert Runa expression to Python expression."""
        if isinstance(expr, RunaLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, RunaIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, RunaBinaryOperation):
            return self._convert_binary_operation(expr)
        elif isinstance(expr, RunaUnaryOperation):
            return self._convert_unary_operation(expr)
        elif isinstance(expr, RunaFunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, RunaMethodCall):
            return self._convert_method_call(expr)
        elif isinstance(expr, RunaMemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, RunaArrayAccess):
            return self._convert_array_access(expr)
        elif isinstance(expr, RunaArrayLiteral):
            return self._convert_array_literal(expr)
        elif isinstance(expr, RunaObjectLiteral):
            return self._convert_object_literal(expr)
        elif isinstance(expr, RunaLambda):
            return self._convert_lambda(expr)
        elif isinstance(expr, RunaConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, RunaAwait):
            return self._convert_await(expr)
        elif isinstance(expr, RunaYield):
            return self._convert_yield(expr)
        
        # Default fallback
        return PyConstant(str(expr))
    
    def _convert_let(self, stmt: RunaLet) -> PyStatement:
        """Convert let statement."""
        target = PyName(stmt.name, PyContext.STORE)
        value = self.convert_expression(stmt.value) if stmt.value else PyConstant(None)
        
        if stmt.variable_type and stmt.variable_type.name != "Any":
            # Annotated assignment
            annotation = self._convert_type(stmt.variable_type)
            return PyAnnAssign(target, annotation, value)
        else:
            # Regular assignment
            return PyAssign([target], value)
    
    def _convert_assignment(self, stmt: RunaAssignment) -> PyStatement:
        """Convert assignment statement."""
        target = self.convert_expression(stmt.target)
        value = self.convert_expression(stmt.value)
        return PyAssign([target], value)
    
    def _convert_process_definition(self, stmt: RunaProcessDefinition) -> PyStatement:
        """Convert process definition."""
        # Convert parameters
        args = []
        defaults = []
        
        for param in stmt.parameters:
            arg_annotation = self._convert_type(param.type) if param.type else None
            args.append(PyArg(param.name, arg_annotation))
            
            if param.default_value:
                defaults.append(self.convert_expression(param.default_value))
        
        arguments = PyArguments(args=args, defaults=defaults)
        
        # Convert body
        body = []
        for body_stmt in stmt.body.statements:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body.extend(converted)
                else:
                    body.append(converted)
        
        # Convert return type
        returns = self._convert_type(stmt.return_type) if stmt.return_type else None
        
        if stmt.is_async:
            return PyAsyncFunctionDef(stmt.name, arguments, body, [], returns)
        else:
            return PyFunctionDef(stmt.name, arguments, body, [], returns)
    
    def _convert_class_definition(self, stmt: RunaClassDefinition) -> PyStatement:
        """Convert class definition."""
        bases = []
        if stmt.base_class:
            bases.append(self._convert_type(stmt.base_class))
        
        # Convert interfaces as additional bases
        for interface in stmt.interfaces:
            bases.append(self._convert_type(interface))
        
        # Convert members
        body = []
        for member in stmt.members:
            converted = self.convert_statement(member)
            if converted:
                if isinstance(converted, list):
                    body.extend(converted)
                else:
                    body.append(converted)
        
        return PyClassDef(stmt.name, bases, [], body, [])
    
    def _convert_return(self, stmt: RunaReturn) -> PyStatement:
        """Convert return statement."""
        value = self.convert_expression(stmt.value) if stmt.value else None
        return PyReturn(value)
    
    def _convert_conditional(self, stmt: RunaConditional) -> PyStatement:
        """Convert conditional statement."""
        test = self.convert_expression(stmt.condition)
        
        body = []
        for then_stmt in stmt.then_branch.statements:
            converted = self.convert_statement(then_stmt)
            if converted:
                if isinstance(converted, list):
                    body.extend(converted)
                else:
                    body.append(converted)
        
        orelse = []
        if stmt.else_branch:
            for else_stmt in stmt.else_branch.statements:
                converted = self.convert_statement(else_stmt)
                if converted:
                    if isinstance(converted, list):
                        orelse.extend(converted)
                    else:
                        orelse.append(converted)
        
        return PyIf(test, body, orelse)
    
    def _convert_while_loop(self, stmt: RunaWhileLoop) -> PyStatement:
        """Convert while loop."""
        test = self.convert_expression(stmt.condition)
        
        body = []
        for body_stmt in stmt.body.statements:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body.extend(converted)
                else:
                    body.append(converted)
        
        return PyWhile(test, body, [])
    
    def _convert_for_loop(self, stmt: RunaForLoop) -> PyStatement:
        """Convert for loop (simplified)."""
        # Convert to while loop
        test = self.convert_expression(stmt.condition)
        
        body = []
        for body_stmt in stmt.body.statements:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body.extend(converted)
                else:
                    body.append(converted)
        
        return PyWhile(test, body, [])
    
    def _convert_try_catch(self, stmt: RunaTryCatch) -> PyStatement:
        """Convert try-catch statement."""
        # Convert try block
        try_body = []
        for try_stmt in stmt.try_block.statements:
            converted = self.convert_statement(try_stmt)
            if converted:
                if isinstance(converted, list):
                    try_body.extend(converted)
                else:
                    try_body.append(converted)
        
        # Convert catch block
        handlers = []
        if stmt.catch_block:
            catch_body = []
            for catch_stmt in stmt.catch_block.statements:
                converted = self.convert_statement(catch_stmt)
                if converted:
                    if isinstance(converted, list):
                        catch_body.extend(converted)
                    else:
                        catch_body.append(converted)
            
            handler = PyExceptHandler(None, stmt.catch_parameter, catch_body)
            handlers.append(handler)
        
        # Convert finally block
        finalbody = []
        if stmt.finally_block:
            for finally_stmt in stmt.finally_block.statements:
                converted = self.convert_statement(finally_stmt)
                if converted:
                    if isinstance(converted, list):
                        finalbody.extend(converted)
                    else:
                        finalbody.append(converted)
        
        return PyTry(try_body, handlers, [], finalbody)
    
    def _convert_throw(self, stmt: RunaThrow) -> PyStatement:
        """Convert throw statement."""
        exc = self.convert_expression(stmt.value)
        return PyRaise(exc)
    
    def _convert_import(self, stmt: RunaImport) -> PyStatement:
        """Convert import statement."""
        if stmt.module:
            # from module import names
            aliases = []
            for import_name in stmt.imports:
                aliases.append(PyAlias(import_name))
            return PyImportFrom(stmt.module, aliases)
        else:
            # import names
            aliases = []
            for import_name in stmt.imports:
                aliases.append(PyAlias(import_name))
            return PyImport(aliases)
    
    def _convert_expression_statement(self, stmt: RunaExpressionStatement) -> PyStatement:
        """Convert expression statement."""
        expr = self.convert_expression(stmt.expression)
        return PyExpressionStmt(expr)
    
    def _convert_block(self, stmt: RunaBlock) -> List[PyStatement]:
        """Convert block statement."""
        statements = []
        for sub_stmt in stmt.statements:
            converted = self.convert_statement(sub_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        return statements
    
    def _convert_literal(self, expr: RunaLiteral) -> PyExpression:
        """Convert literal expression."""
        return PyConstant(expr.value)
    
    def _convert_identifier(self, expr: RunaIdentifier) -> PyExpression:
        """Convert identifier expression."""
        return PyName(expr.name)
    
    def _convert_binary_operation(self, expr: RunaBinaryOperation) -> PyExpression:
        """Convert binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        operator_map = {
            "plus": PyOperator.ADD,
            "minus": PyOperator.SUB,
            "times": PyOperator.MULT,
            "divided by": PyOperator.DIV,
            "modulo": PyOperator.MOD,
            "power": PyOperator.POW,
            "floor divided by": PyOperator.FLOORDIV,
            "is equal to": PyOperator.EQ,
            "is not equal to": PyOperator.NOT_EQ,
            "is less than": PyOperator.LT,
            "is less than or equal to": PyOperator.LTE,
            "is greater than": PyOperator.GT,
            "is greater than or equal to": PyOperator.GTE,
            "bitwise and": PyOperator.BITAND,
            "bitwise or": PyOperator.BITOR,
            "bitwise xor": PyOperator.BITXOR,
            "left shift": PyOperator.LSHIFT,
            "right shift": PyOperator.RSHIFT,
        }
        
        if expr.operator in ["and", "or"]:
            # Logical operators use different AST nodes
            py_op = PyOperator.AND if expr.operator == "and" else PyOperator.OR
            return PyBinOp(left, py_op, right)
        elif expr.operator in operator_map:
            return PyBinOp(left, operator_map[expr.operator], right)
        else:
            # Comparison operators
            comp_map = {
                "is equal to": PyOperator.EQ,
                "is not equal to": PyOperator.NOT_EQ,
                "is less than": PyOperator.LT,
                "is less than or equal to": PyOperator.LTE,
                "is greater than": PyOperator.GT,
                "is greater than or equal to": PyOperator.GTE,
                "is": PyOperator.IS,
                "is not": PyOperator.IS_NOT,
                "in": PyOperator.IN,
                "not in": PyOperator.NOT_IN,
            }
            
            if expr.operator in comp_map:
                return PyCompare(left, [comp_map[expr.operator]], [right])
            else:
                # Default to addition
                return PyBinOp(left, PyOperator.ADD, right)
    
    def _convert_unary_operation(self, expr: RunaUnaryOperation) -> PyExpression:
        """Convert unary operation."""
        operand = self.convert_expression(expr.operand)
        
        operator_map = {
            "not": PyOperator.NOT,
            "positive": PyOperator.UADD,
            "negative": PyOperator.USUB,
            "bitwise not": PyOperator.INVERT,
        }
        
        operator = operator_map.get(expr.operator, PyOperator.NOT)
        return PyUnaryOp(operator, operand)
    
    def _convert_function_call(self, expr: RunaFunctionCall) -> PyExpression:
        """Convert function call."""
        func = PyName(expr.function_name)
        args = [self.convert_expression(arg) for arg in expr.arguments]
        return PyCall(func, args, [])
    
    def _convert_method_call(self, expr: RunaMethodCall) -> PyExpression:
        """Convert method call."""
        obj = self.convert_expression(expr.object)
        func = PyAttribute(obj, expr.method)
        args = [self.convert_expression(arg) for arg in expr.arguments]
        return PyCall(func, args, [])
    
    def _convert_member_access(self, expr: RunaMemberAccess) -> PyExpression:
        """Convert member access."""
        obj = self.convert_expression(expr.object)
        return PyAttribute(obj, expr.member)
    
    def _convert_array_access(self, expr: RunaArrayAccess) -> PyExpression:
        """Convert array access."""
        array = self.convert_expression(expr.array)
        index = self.convert_expression(expr.index)
        return PySubscript(array, index)
    
    def _convert_array_literal(self, expr: RunaArrayLiteral) -> PyExpression:
        """Convert array literal."""
        elements = [self.convert_expression(element) for element in expr.elements]
        return PyList(elements)
    
    def _convert_object_literal(self, expr: RunaObjectLiteral) -> PyExpression:
        """Convert object literal."""
        keys = []
        values = []
        
        for prop in expr.properties:
            keys.append(PyConstant(prop.key))
            values.append(self.convert_expression(prop.value))
        
        return PyDict(keys, values)
    
    def _convert_lambda(self, expr: RunaLambda) -> PyExpression:
        """Convert lambda expression."""
        args = []
        for param in expr.parameters:
            arg_annotation = self._convert_type(param.type) if param.type else None
            args.append(PyArg(param.name, arg_annotation))
        
        arguments = PyArguments(args=args)
        
        # Extract body expression (assume single return)
        if expr.body.statements and isinstance(expr.body.statements[0], RunaReturn):
            body = self.convert_expression(expr.body.statements[0].value)
        else:
            body = PyConstant(None)
        
        return PyLambda(arguments, body)
    
    def _convert_conditional_expression(self, expr: RunaConditionalExpression) -> PyExpression:
        """Convert conditional expression."""
        test = self.convert_expression(expr.condition)
        body = self.convert_expression(expr.then_value)
        orelse = self.convert_expression(expr.else_value)
        
        return PyIfExp(test, body, orelse)
    
    def _convert_await(self, expr: RunaAwait) -> PyExpression:
        """Convert await expression."""
        value = self.convert_expression(expr.expression)
        return PyAwait(value)
    
    def _convert_yield(self, expr: RunaYield) -> PyExpression:
        """Convert yield expression."""
        value = self.convert_expression(expr.value) if expr.value else None
        return PyYield(value)
    
    def _convert_type(self, runa_type: RunaType) -> PyExpression:
        """Convert Runa type to Python type expression."""
        type_map = {
            "Integer": "int",
            "Float": "float",
            "String": "str",
            "Boolean": "bool",
            "List": "list",
            "Dictionary": "dict",
            "Tuple": "tuple",
            "Set": "set",
            "Null": "None",
            "Any": "Any",
        }
        
        type_name = type_map.get(runa_type.name, runa_type.name)
        return PyName(type_name)


def py_to_runa(py_ast: PyModule) -> Program:
    """Convert Python AST to Runa AST."""
    converter = PyToRunaConverter()
    return converter.convert(py_ast)


def runa_to_py(runa_ast: Program) -> PyModule:
    """Convert Runa AST to Python AST."""
    converter = RunaToPyConverter()
    return converter.convert(runa_ast)