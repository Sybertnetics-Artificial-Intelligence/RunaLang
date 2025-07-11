#!/usr/bin/env python3
"""
LISP Converter

Bidirectional converter between LISP AST and Runa universal AST.
Handles functional programming constructs, S-expressions, and LISP-specific features.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from ...shared.base_toolchain import BaseConverter
from ....core.ast_nodes import (
    Node, NodeType, Expression, Statement, Declaration,
    Literal, Identifier, BinaryOp, UnaryOp, FunctionCall,
    VariableDeclaration, FunctionDeclaration, Parameter,
    Block, IfStatement, WhileLoop, ReturnStatement,
    Assignment, ListLiteral, DictLiteral
)

from .lisp_ast import (
    LispNode, LispExpression, LispForm, LispAtom, LispSymbol, LispList,
    LispCons, LispQuote, LispDefun, LispLambda, LispLet, LispSetq, LispIf,
    LispCond, LispProgn, LispWhen, LispUnless, LispCar, LispCdr, LispConsFunc,
    LispEq, LispEqual, LispAtomFunc, LispListp, LispLoop, LispReturn,
    LispDefmacro, LispMacroCall, LispApplication, LispProgram,
    LispNodeType, lisp_nil, lisp_t, lisp_number, lisp_string, lisp_symbol,
    lisp_list, lisp_application
)


class LispToRunaConverter(BaseConverter):
    """Converts LISP AST to Runa universal AST."""
    
    def __init__(self):
        super().__init__()
        self.symbol_map: Dict[str, str] = {}
        self.lambda_counter = 0
    
    def convert(self, lisp_node: LispNode) -> Node:
        """Convert LISP AST node to Runa AST node."""
        return self._convert_node(lisp_node)
    
    def _convert_node(self, node: LispNode) -> Node:
        """Convert any LISP node to Runa node."""
        if isinstance(node, LispProgram):
            return self._convert_program(node)
        elif isinstance(node, LispAtom):
            return self._convert_atom(node)
        elif isinstance(node, LispSymbol):
            return self._convert_symbol(node)
        elif isinstance(node, LispList):
            return self._convert_list(node)
        elif isinstance(node, LispCons):
            return self._convert_cons(node)
        elif isinstance(node, LispQuote):
            return self._convert_quote(node)
        elif isinstance(node, LispDefun):
            return self._convert_defun(node)
        elif isinstance(node, LispLambda):
            return self._convert_lambda(node)
        elif isinstance(node, LispLet):
            return self._convert_let(node)
        elif isinstance(node, LispSetq):
            return self._convert_setq(node)
        elif isinstance(node, LispIf):
            return self._convert_if(node)
        elif isinstance(node, LispCond):
            return self._convert_cond(node)
        elif isinstance(node, LispProgn):
            return self._convert_progn(node)
        elif isinstance(node, LispWhen):
            return self._convert_when(node)
        elif isinstance(node, LispUnless):
            return self._convert_unless(node)
        elif isinstance(node, LispApplication):
            return self._convert_application(node)
        elif isinstance(node, (LispCar, LispCdr, LispConsFunc, LispEq, LispEqual,
                               LispAtomFunc, LispListp)):
            return self._convert_builtin_function(node)
        elif isinstance(node, LispLoop):
            return self._convert_loop(node)
        elif isinstance(node, LispReturn):
            return self._convert_return(node)
        elif isinstance(node, LispDefmacro):
            return self._convert_defmacro(node)
        else:
            raise ValueError(f"Unknown LISP node type: {type(node)}")
    
    def _convert_program(self, node: LispProgram) -> Block:
        """Convert LISP program to Runa block."""
        statements = []
        for form in node.forms:
            stmt = self._convert_node(form)
            if isinstance(stmt, Expression):
                # Wrap expression in statement
                statements.append(stmt)
            else:
                statements.append(stmt)
        
        return Block(statements)
    
    def _convert_atom(self, node: LispAtom) -> Literal:
        """Convert LISP atom to Runa literal."""
        if node.atom_type == "nil":
            return Literal(None, "null")
        elif node.atom_type == "t":
            return Literal(True, "boolean")
        elif node.atom_type == "number":
            if isinstance(node.value, float):
                return Literal(node.value, "float")
            else:
                return Literal(node.value, "integer")
        elif node.atom_type == "string":
            return Literal(node.value, "string")
        else:
            return Literal(node.value, "unknown")
    
    def _convert_symbol(self, node: LispSymbol) -> Identifier:
        """Convert LISP symbol to Runa identifier."""
        return Identifier(node.name)
    
    def _convert_list(self, node: LispList) -> ListLiteral:
        """Convert LISP list to Runa list literal."""
        elements = [self._convert_node(elem) for elem in node.elements]
        return ListLiteral(elements)
    
    def _convert_cons(self, node: LispCons) -> FunctionCall:
        """Convert LISP cons to Runa function call."""
        car = self._convert_node(node.car)
        cdr = self._convert_node(node.cdr)
        return FunctionCall(
            Identifier("cons"),
            [car, cdr]
        )
    
    def _convert_quote(self, node: LispQuote) -> FunctionCall:
        """Convert LISP quote to Runa function call."""
        expr = self._convert_node(node.expression)
        return FunctionCall(
            Identifier("quote"),
            [expr]
        )
    
    def _convert_defun(self, node: LispDefun) -> FunctionDeclaration:
        """Convert LISP defun to Runa function declaration."""
        name = node.name.name
        parameters = [Parameter(param.name, None) for param in node.parameters]
        
        # Convert body
        body_statements = [self._convert_node(expr) for expr in node.body]
        body = Block(body_statements)
        
        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            return_type=None,
            body=body,
            annotations=[]
        )
    
    def _convert_lambda(self, node: LispLambda) -> FunctionDeclaration:
        """Convert LISP lambda to Runa function declaration."""
        self.lambda_counter += 1
        name = f"__lambda_{self.lambda_counter}"
        
        parameters = [Parameter(param.name, None) for param in node.parameters]
        
        # Convert body
        body_statements = [self._convert_node(expr) for expr in node.body]
        body = Block(body_statements)
        
        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            return_type=None,
            body=body,
            annotations=["lambda"]
        )
    
    def _convert_let(self, node: LispLet) -> Block:
        """Convert LISP let to Runa block with variable declarations."""
        statements = []
        
        # Create variable declarations for bindings
        for symbol, value in node.bindings:
            var_name = symbol.name
            init_value = self._convert_node(value)
            var_decl = VariableDeclaration(var_name, None, init_value)
            statements.append(var_decl)
        
        # Add body statements
        for expr in node.body:
            stmt = self._convert_node(expr)
            statements.append(stmt)
        
        return Block(statements)
    
    def _convert_setq(self, node: LispSetq) -> Assignment:
        """Convert LISP setq to Runa assignment."""
        target = self._convert_node(node.symbol)
        value = self._convert_node(node.value)
        return Assignment(target, value)
    
    def _convert_if(self, node: LispIf) -> IfStatement:
        """Convert LISP if to Runa if statement."""
        condition = self._convert_node(node.test)
        then_stmt = self._convert_node(node.then_expr)
        
        else_stmt = None
        if node.else_expr:
            else_stmt = self._convert_node(node.else_expr)
        
        return IfStatement(condition, then_stmt, else_stmt)
    
    def _convert_cond(self, node: LispCond) -> IfStatement:
        """Convert LISP cond to nested Runa if statements."""
        if not node.clauses:
            return Block([])
        
        # Build nested if-else chain
        result = None
        for test, expr in reversed(node.clauses):
            condition = self._convert_node(test)
            then_stmt = self._convert_node(expr)
            
            if result is None:
                result = IfStatement(condition, then_stmt, None)
            else:
                result = IfStatement(condition, then_stmt, result)
        
        return result
    
    def _convert_progn(self, node: LispProgn) -> Block:
        """Convert LISP progn to Runa block."""
        statements = [self._convert_node(expr) for expr in node.expressions]
        return Block(statements)
    
    def _convert_when(self, node: LispWhen) -> IfStatement:
        """Convert LISP when to Runa if statement."""
        condition = self._convert_node(node.test)
        body_statements = [self._convert_node(expr) for expr in node.body]
        body = Block(body_statements)
        
        return IfStatement(condition, body, None)
    
    def _convert_unless(self, node: LispUnless) -> IfStatement:
        """Convert LISP unless to Runa if statement with negated condition."""
        condition = self._convert_node(node.test)
        negated_condition = UnaryOp("not", condition)
        
        body_statements = [self._convert_node(expr) for expr in node.body]
        body = Block(body_statements)
        
        return IfStatement(negated_condition, body, None)
    
    def _convert_application(self, node: LispApplication) -> FunctionCall:
        """Convert LISP function application to Runa function call."""
        function = self._convert_node(node.function)
        arguments = [self._convert_node(arg) for arg in node.arguments]
        
        return FunctionCall(function, arguments)
    
    def _convert_builtin_function(self, node: LispExpression) -> FunctionCall:
        """Convert LISP built-in function to Runa function call."""
        if isinstance(node, LispCar):
            return FunctionCall(Identifier("car"), [self._convert_node(node.expression)])
        elif isinstance(node, LispCdr):
            return FunctionCall(Identifier("cdr"), [self._convert_node(node.expression)])
        elif isinstance(node, LispConsFunc):
            return FunctionCall(
                Identifier("cons"),
                [self._convert_node(node.car), self._convert_node(node.cdr)]
            )
        elif isinstance(node, LispEq):
            return BinaryOp(
                self._convert_node(node.left),
                "eq",
                self._convert_node(node.right)
            )
        elif isinstance(node, LispEqual):
            return BinaryOp(
                self._convert_node(node.left),
                "equal",
                self._convert_node(node.right)
            )
        elif isinstance(node, LispAtomFunc):
            return FunctionCall(Identifier("atom"), [self._convert_node(node.expression)])
        elif isinstance(node, LispListp):
            return FunctionCall(Identifier("listp"), [self._convert_node(node.expression)])
        else:
            raise ValueError(f"Unknown built-in function: {type(node)}")
    
    def _convert_loop(self, node: LispLoop) -> WhileLoop:
        """Convert LISP loop to Runa while loop."""
        # LISP loop is infinite, so use true condition
        condition = Literal(True, "boolean")
        body_statements = [self._convert_node(expr) for expr in node.body]
        body = Block(body_statements)
        
        return WhileLoop(condition, body)
    
    def _convert_return(self, node: LispReturn) -> ReturnStatement:
        """Convert LISP return to Runa return statement."""
        value = None
        if node.value:
            value = self._convert_node(node.value)
        
        return ReturnStatement(value)
    
    def _convert_defmacro(self, node: LispDefmacro) -> FunctionDeclaration:
        """Convert LISP defmacro to Runa function declaration with macro annotation."""
        name = node.name.name
        parameters = [Parameter(param.name, None) for param in node.parameters]
        
        # Convert body
        body_statements = [self._convert_node(expr) for expr in node.body]
        body = Block(body_statements)
        
        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            return_type=None,
            body=body,
            annotations=["macro"]
        )


class RunaToLispConverter(BaseConverter):
    """Converts Runa universal AST to LISP AST."""
    
    def __init__(self):
        super().__init__()
        self.function_counter = 0
    
    def convert(self, runa_node: Node) -> LispNode:
        """Convert Runa AST node to LISP AST node."""
        return self._convert_node(runa_node)
    
    def _convert_node(self, node: Node) -> LispNode:
        """Convert any Runa node to LISP node."""
        if isinstance(node, Block):
            return self._convert_block(node)
        elif isinstance(node, Literal):
            return self._convert_literal(node)
        elif isinstance(node, Identifier):
            return self._convert_identifier(node)
        elif isinstance(node, BinaryOp):
            return self._convert_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self._convert_unary_op(node)
        elif isinstance(node, FunctionCall):
            return self._convert_function_call(node)
        elif isinstance(node, VariableDeclaration):
            return self._convert_variable_declaration(node)
        elif isinstance(node, FunctionDeclaration):
            return self._convert_function_declaration(node)
        elif isinstance(node, IfStatement):
            return self._convert_if_statement(node)
        elif isinstance(node, WhileLoop):
            return self._convert_while_loop(node)
        elif isinstance(node, ReturnStatement):
            return self._convert_return_statement(node)
        elif isinstance(node, Assignment):
            return self._convert_assignment(node)
        elif isinstance(node, ListLiteral):
            return self._convert_list_literal(node)
        else:
            # Default: try to convert as expression
            return self._convert_expression(node)
    
    def _convert_block(self, node: Block) -> LispProgram:
        """Convert Runa block to LISP program."""
        forms = []
        for stmt in node.statements:
            lisp_form = self._convert_node(stmt)
            forms.append(lisp_form)
        
        return LispProgram(forms)
    
    def _convert_literal(self, node: Literal) -> LispAtom:
        """Convert Runa literal to LISP atom."""
        if node.value is None:
            return lisp_nil()
        elif isinstance(node.value, bool):
            return lisp_t() if node.value else lisp_nil()
        elif isinstance(node.value, (int, float)):
            return lisp_number(node.value)
        elif isinstance(node.value, str):
            return lisp_string(node.value)
        else:
            return lisp_string(str(node.value))
    
    def _convert_identifier(self, node: Identifier) -> LispSymbol:
        """Convert Runa identifier to LISP symbol."""
        return lisp_symbol(node.name)
    
    def _convert_binary_op(self, node: BinaryOp) -> LispApplication:
        """Convert Runa binary operation to LISP function application."""
        left = self._convert_node(node.left)
        right = self._convert_node(node.right)
        
        # Map operators to LISP functions
        op_map = {
            "eq": "eq",
            "equal": "equal",
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "==": "equal",
            "!=": "not-equal"
        }
        
        func_name = op_map.get(node.operator, node.operator)
        return lisp_application(lisp_symbol(func_name), left, right)
    
    def _convert_unary_op(self, node: UnaryOp) -> LispApplication:
        """Convert Runa unary operation to LISP function application."""
        operand = self._convert_node(node.operand)
        
        # Map operators to LISP functions
        op_map = {
            "not": "not",
            "-": "minus",
            "+": "plus"
        }
        
        func_name = op_map.get(node.operator, node.operator)
        return lisp_application(lisp_symbol(func_name), operand)
    
    def _convert_function_call(self, node: FunctionCall) -> LispApplication:
        """Convert Runa function call to LISP function application."""
        function = self._convert_node(node.function)
        arguments = [self._convert_node(arg) for arg in node.arguments]
        
        return lisp_application(function, *arguments)
    
    def _convert_variable_declaration(self, node: VariableDeclaration) -> LispSetq:
        """Convert Runa variable declaration to LISP setq."""
        symbol = lisp_symbol(node.name)
        value = self._convert_node(node.value) if node.value else lisp_nil()
        
        return LispSetq(symbol, value)
    
    def _convert_function_declaration(self, node: FunctionDeclaration) -> LispDefun:
        """Convert Runa function declaration to LISP defun."""
        name = lisp_symbol(node.name)
        parameters = [lisp_symbol(param.name) for param in node.parameters]
        
        # Convert body
        body = []
        if isinstance(node.body, Block):
            for stmt in node.body.statements:
                body.append(self._convert_node(stmt))
        else:
            body.append(self._convert_node(node.body))
        
        # Check for lambda annotation
        if "lambda" in (node.annotations or []):
            return LispLambda(parameters, body)
        elif "macro" in (node.annotations or []):
            return LispDefmacro(name, parameters, body)
        else:
            return LispDefun(name, parameters, body)
    
    def _convert_if_statement(self, node: IfStatement) -> LispIf:
        """Convert Runa if statement to LISP if."""
        test = self._convert_node(node.condition)
        then_expr = self._convert_node(node.then_statement)
        
        else_expr = None
        if node.else_statement:
            else_expr = self._convert_node(node.else_statement)
        
        return LispIf(test, then_expr, else_expr)
    
    def _convert_while_loop(self, node: WhileLoop) -> LispLoop:
        """Convert Runa while loop to LISP loop."""
        # Convert body
        body = []
        if isinstance(node.body, Block):
            for stmt in node.body.statements:
                body.append(self._convert_node(stmt))
        else:
            body.append(self._convert_node(node.body))
        
        return LispLoop(body)
    
    def _convert_return_statement(self, node: ReturnStatement) -> LispReturn:
        """Convert Runa return statement to LISP return."""
        value = None
        if node.value:
            value = self._convert_node(node.value)
        
        return LispReturn(value)
    
    def _convert_assignment(self, node: Assignment) -> LispSetq:
        """Convert Runa assignment to LISP setq."""
        if isinstance(node.target, Identifier):
            symbol = lisp_symbol(node.target.name)
            value = self._convert_node(node.value)
            return LispSetq(symbol, value)
        else:
            raise ValueError("LISP only supports simple variable assignments")
    
    def _convert_list_literal(self, node: ListLiteral) -> LispList:
        """Convert Runa list literal to LISP list."""
        elements = [self._convert_node(elem) for elem in node.elements]
        return lisp_list(*elements)
    
    def _convert_expression(self, node: Node) -> LispExpression:
        """Convert generic Runa expression to LISP expression."""
        # Default behavior for unknown nodes
        if hasattr(node, 'name'):
            return lisp_symbol(str(node.name))
        else:
            return lisp_symbol("unknown")


# Convenience functions
def lisp_to_runa(lisp_ast: LispNode) -> Node:
    """Convert LISP AST to Runa AST."""
    converter = LispToRunaConverter()
    return converter.convert(lisp_ast)


def runa_to_lisp(runa_ast: Node) -> LispNode:
    """Convert Runa AST to LISP AST."""
    converter = RunaToLispConverter()
    return converter.convert(runa_ast) 