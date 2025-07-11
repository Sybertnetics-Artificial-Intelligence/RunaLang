#!/usr/bin/env python3
"""
Starlark Converter Implementation

This module provides bidirectional conversion between Starlark AST and Runa Universal AST.
It handles all Starlark language constructs and maps them to equivalent Runa representations.

Key conversion features:
- Complete Starlark syntax mapping to Runa Universal AST
- Starlark-specific constructs (load, rule, aspect, provider) to Runa extensions
- Type preservation and inference
- Metadata preservation for round-trip fidelity
- Error handling and validation during conversion

The converter maintains semantic equivalence while handling the differences between
Starlark's Python-like syntax and Runa's universal representation.
"""

from typing import Any, List, Optional, Dict, Union, Set
import json
from dataclasses import dataclass

from ...runa.runa_ast import *
from .starlark_ast import *


@dataclass
class ConversionContext:
    """Context for tracking conversion state."""
    
    scope_stack: List[Dict[str, Any]]
    type_hints: Dict[str, str]
    metadata: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    
    def __post_init__(self):
        if not self.scope_stack:
            self.scope_stack = [{}]
        if not self.type_hints:
            self.type_hints = {}
        if not self.metadata:
            self.metadata = {}
        if not self.errors:
            self.errors = []
        if not self.warnings:
            self.warnings = []
    
    def enter_scope(self) -> None:
        """Enter a new scope."""
        self.scope_stack.append({})
    
    def exit_scope(self) -> None:
        """Exit current scope."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
    
    def declare_variable(self, name: str, var_type: str = "any") -> None:
        """Declare a variable in current scope."""
        self.scope_stack[-1][name] = var_type
        self.type_hints[name] = var_type
    
    def lookup_variable(self, name: str) -> Optional[str]:
        """Look up a variable type."""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return self.type_hints.get(name)
    
    def add_error(self, message: str) -> None:
        """Add a conversion error."""
        self.errors.append(message)
    
    def add_warning(self, message: str) -> None:
        """Add a conversion warning."""
        self.warnings.append(message)


class StarlarkToRunaConverter:
    """Converts Starlark AST to Runa Universal AST."""
    
    def __init__(self):
        self.context = ConversionContext(
            scope_stack=[{}],
            type_hints={},
            metadata={},
            errors=[],
            warnings=[]
        )
    
    def convert(self, starlark_node: StarlarkNode) -> RunaNode:
        """Convert a Starlark AST node to Runa Universal AST."""
        return starlark_node.accept(self)
    
    def visit_module(self, node: StarlarkModule) -> RunaModule:
        """Convert Starlark module to Runa module."""
        runa_statements = []
        
        for stmt in node.body:
            try:
                runa_stmt = stmt.accept(self)
                if runa_stmt:
                    runa_statements.append(runa_stmt)
            except Exception as e:
                self.context.add_error(f"Failed to convert statement: {e}")
        
        metadata = {
            "original_language": "starlark",
            "docstring": node.docstring,
            "conversion_context": {
                "errors": self.context.errors,
                "warnings": self.context.warnings,
                "type_hints": self.context.type_hints
            }
        }
        
        return RunaModule(
            statements=runa_statements,
            metadata=metadata
        )
    
    def visit_literal(self, node: StarlarkLiteral) -> StringLiteral:
        """Convert Starlark literal to Runa literal."""
        type_mapping = {
            "int": "Int",
            "float": "Float", 
            "string": "String",
            "bool": "Bool",
            "none": "None"
        }
        
        return StringLiteral(
            value=node.value,
            data_type=type_mapping.get(node.literal_type, "Any"),
            metadata={"starlark_type": node.literal_type}
        )
    
    def visit_identifier(self, node: StarlarkIdentifier) -> Identifier:
        """Convert Starlark identifier to Runa identifier."""
        var_type = self.context.lookup_variable(node.name) or "Any"
        
        return Identifier(
            name=node.name,
            data_type=var_type,
            metadata={"original_name": node.name}
        )
    
    def visit_binary_op(self, node: StarlarkBinaryOp) -> RunaBinaryOp:
        """Convert Starlark binary operation to Runa binary operation."""
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        operator_mapping = {
            StarlarkOperator.ADD: "+",
            StarlarkOperator.SUB: "-",
            StarlarkOperator.MUL: "*",
            StarlarkOperator.DIV: "/",
            StarlarkOperator.FLOOR_DIV: "//",
            StarlarkOperator.MOD: "%",
            StarlarkOperator.POW: "**",
            StarlarkOperator.BIT_OR: "|",
            StarlarkOperator.BIT_XOR: "^",
            StarlarkOperator.BIT_AND: "&",
            StarlarkOperator.LEFT_SHIFT: "<<",
            StarlarkOperator.RIGHT_SHIFT: ">>",
        }
        
        runa_operator = operator_mapping.get(node.operator, node.operator.value)
        
        return RunaBinaryOp(
            left=left,
            operator=runa_operator,
            right=right,
            metadata={"starlark_operator": node.operator.value}
        )
    
    def visit_unary_op(self, node: StarlarkUnaryOp) -> RunaUnaryOp:
        """Convert Starlark unary operation to Runa unary operation."""
        operand = node.operand.accept(self)
        
        operator_mapping = {
            StarlarkOperator.UADD: "+",
            StarlarkOperator.USUB: "-",
            StarlarkOperator.NOT: "not",
            StarlarkOperator.INVERT: "~"
        }
        
        runa_operator = operator_mapping.get(node.operator, node.operator.value)
        
        return RunaUnaryOp(
            operator=runa_operator,
            operand=operand,
            metadata={"starlark_operator": node.operator.value}
        )
    
    def visit_comparison(self, node: StarlarkComparison) -> Expression:
        """Convert Starlark comparison to Runa comparison."""
        left = node.left.accept(self)
        
        if len(node.operators) == 1:
            operator_mapping = {
                StarlarkOperator.EQ: "==",
                StarlarkOperator.NE: "!=",
                StarlarkOperator.LT: "<",
                StarlarkOperator.LE: "<=",
                StarlarkOperator.GT: ">",
                StarlarkOperator.GE: ">=",
                StarlarkOperator.IN: "in",
                StarlarkOperator.NOT_IN: "not in",
                StarlarkOperator.IS: "is",
                StarlarkOperator.IS_NOT: "is not"
            }
            
            right = node.comparators[0].accept(self)
            operator = operator_mapping.get(node.operators[0], node.operators[0].value)
            
            return RunaBinaryOp(
                left=left,
                operator=operator,
                right=right,
                metadata={"starlark_comparison": True}
            )
        else:
            # Chain comparisons using 'and'
            comparisons = []
            current_left = left
            
            for i, (op, comp) in enumerate(zip(node.operators, node.comparators)):
                operator_mapping = {
                    StarlarkOperator.EQ: "==",
                    StarlarkOperator.NE: "!=",
                    StarlarkOperator.LT: "<",
                    StarlarkOperator.LE: "<=",
                    StarlarkOperator.GT: ">",
                    StarlarkOperator.GE: ">=",
                    StarlarkOperator.IN: "in",
                    StarlarkOperator.NOT_IN: "not in"
                }
                
                right = comp.accept(self)
                operator = operator_mapping.get(op, op.value)
                
                comparison = RunaBinaryOp(
                    left=current_left,
                    operator=operator,
                    right=right
                )
                
                comparisons.append(comparison)
                current_left = right
            
            # Chain with 'and'
            result = comparisons[0]
            for comp in comparisons[1:]:
                result = RunaBinaryOp(
                    left=result,
                    operator="and",
                    right=comp
                )
            
            return result
    
    def visit_bool_op(self, node: StarlarkBoolOp) -> Expression:
        """Convert Starlark boolean operation to Runa boolean operation."""
        if len(node.values) < 2:
            return node.values[0].accept(self) if node.values else StringLiteral(value=True, data_type="Bool")
        
        operator = "and" if node.operator == StarlarkOperator.AND else "or"
        
        result = node.values[0].accept(self)
        for value in node.values[1:]:
            right = value.accept(self)
            result = RunaBinaryOp(
                left=result,
                operator=operator,
                right=right
            )
        
        return result
    
    def visit_attribute(self, node: StarlarkAttribute) -> RunaAttributeAccess:
        """Convert Starlark attribute access to Runa attribute access."""
        obj = node.value.accept(self)
        
        return RunaAttributeAccess(
            object=obj,
            attribute=node.attr,
            metadata={"starlark_attribute": True}
        )
    
    def visit_index(self, node: StarlarkIndex) -> IndexAccess:
        """Convert Starlark index access to Runa index access."""
        obj = node.value.accept(self)
        index = node.index.accept(self)
        
        return IndexAccess(
            object=obj,
            index=index,
            metadata={"starlark_index": True}
        )
    
    def visit_slice(self, node: StarlarkSlice) -> RunaSliceAccess:
        """Convert Starlark slice access to Runa slice access."""
        obj = node.value.accept(self)
        start = node.start.accept(self) if node.start else None
        end = node.end.accept(self) if node.end else None
        step = node.step.accept(self) if node.step else None
        
        return RunaSliceAccess(
            object=obj,
            start=start,
            end=end,
            step=step,
            metadata={"starlark_slice": True}
        )
    
    def visit_list(self, node: StarlarkList) -> ListLiteral:
        """Convert Starlark list to Runa list."""
        elements = [elem.accept(self) for elem in node.elements]
        
        return ListLiteral(
            elements=elements,
            element_type="Any",
            metadata={"starlark_list": True}
        )
    
    def visit_tuple(self, node: StarlarkTuple) -> RunaTuple:
        """Convert Starlark tuple to Runa tuple."""
        elements = [elem.accept(self) for elem in node.elements]
        
        return RunaTuple(
            elements=elements,
            metadata={"starlark_tuple": True}
        )
    
    def visit_dict(self, node: StarlarkDict) -> RunaDictionary:
        """Convert Starlark dictionary to Runa dictionary."""
        pairs = []
        for key, value in zip(node.keys, node.values):
            runa_key = key.accept(self)
            runa_value = value.accept(self)
            pairs.append(RunaKeyValuePair(key=runa_key, value=runa_value))
        
        return RunaDictionary(
            pairs=pairs,
            key_type="Any",
            value_type="Any",
            metadata={"starlark_dict": True}
        )
    
    def visit_call(self, node: StarlarkCall) -> FunctionCall:
        """Convert Starlark function call to Runa function call."""
        func = node.func.accept(self)
        args = [arg.accept(self) for arg in node.args]
        
        kwargs = []
        for kw in node.keywords:
            value = kw.value.accept(self)
            kwargs.append(RunaKeywordArgument(name=kw.arg, value=value))
        
        return FunctionCall(
            function=func,
            arguments=args,
            keyword_arguments=kwargs,
            metadata={"starlark_call": True}
        )
    
    def visit_keyword(self, node: StarlarkKeyword) -> RunaKeywordArgument:
        """Convert Starlark keyword argument to Runa keyword argument."""
        value = node.value.accept(self)
        
        return RunaKeywordArgument(
            name=node.arg,
            value=value,
            metadata={"starlark_keyword": True}
        )
    
    def visit_lambda(self, node: StarlarkLambda) -> ProcessDefinitionExpression:
        """Convert Starlark lambda to Runa lambda expression."""
        self.context.enter_scope()
        
        parameters = []
        for arg in node.args:
            param = Parameter(name=arg, data_type="Any")
            parameters.append(param)
            self.context.declare_variable(arg, "Any")
        
        body = node.body.accept(self)
        
        self.context.exit_scope()
        
        return ProcessDefinitionExpression(
            parameters=parameters,
            body=body,
            metadata={"starlark_lambda": True}
        )
    
    def visit_conditional_expr(self, node: StarlarkConditionalExpr) -> IfStatementExpression:
        """Convert Starlark conditional expression to Runa conditional expression."""
        condition = node.test.accept(self)
        then_expr = node.body.accept(self)
        else_expr = node.orelse.accept(self)
        
        return IfStatementExpression(
            condition=condition,
            then_expression=then_expr,
            else_expression=else_expr,
            metadata={"starlark_conditional": True}
        )
    
    def visit_list_comp(self, node: StarlarkListComp) -> ListLiteralComprehension:
        """Convert Starlark list comprehension to Runa list comprehension."""
        self.context.enter_scope()
        self.context.declare_variable(node.target, "Any")
        
        element = node.element.accept(self)
        iterable = node.iter.accept(self)
        
        conditions = [cond.accept(self) for cond in node.ifs]
        
        self.context.exit_scope()
        
        return ListLiteralComprehension(
            element=element,
            variable=node.target,
            iterable=iterable,
            conditions=conditions,
            metadata={"starlark_list_comp": True}
        )
    
    def visit_dict_comp(self, node: StarlarkDictComp) -> RunaDictionaryComprehension:
        """Convert Starlark dictionary comprehension to Runa dictionary comprehension."""
        self.context.enter_scope()
        self.context.declare_variable(node.target, "Any")
        
        key = node.key.accept(self)
        value = node.value.accept(self)
        iterable = node.iter.accept(self)
        
        conditions = [cond.accept(self) for cond in node.ifs]
        
        self.context.exit_scope()
        
        return RunaDictionaryComprehension(
            key=key,
            value=value,
            variable=node.target,
            iterable=iterable,
            conditions=conditions,
            metadata={"starlark_dict_comp": True}
        )
    
    def visit_assign(self, node: StarlarkAssign) -> SetStatement:
        """Convert Starlark assignment to Runa assignment."""
        value = node.value.accept(self)
        
        if len(node.targets) == 1:
            target = node.targets[0].accept(self)
            
            # Track variable declaration
            if isinstance(node.targets[0], StarlarkIdentifier):
                self.context.declare_variable(node.targets[0].name, "Any")
            
            return SetStatement(
                target=target,
                value=value,
                metadata={"starlark_assign": True}
            )
        else:
            # Multiple assignment - convert to tuple unpacking
            targets = [target.accept(self) for target in node.targets]
            
            return RunaTupleUnpacking(
                targets=targets,
                value=value,
                metadata={"starlark_multiple_assign": True}
            )
    
    def visit_aug_assign(self, node: StarlarkAugAssign) -> RunaAugmentedAssignment:
        """Convert Starlark augmented assignment to Runa augmented assignment."""
        target = node.target.accept(self)
        value = node.value.accept(self)
        
        operator_mapping = {
            StarlarkOperator.ADD: "+",
            StarlarkOperator.SUB: "-",
            StarlarkOperator.MUL: "*",
            StarlarkOperator.DIV: "/",
            StarlarkOperator.FLOOR_DIV: "//",
            StarlarkOperator.MOD: "%"
        }
        
        operator = operator_mapping.get(node.operator, node.operator.value)
        
        return RunaAugmentedAssignment(
            target=target,
            operator=operator,
            value=value,
            metadata={"starlark_aug_assign": True}
        )
    
    def visit_function_def(self, node: StarlarkFunctionDef) -> RunaFunctionDefinition:
        """Convert Starlark function definition to Runa function definition."""
        self.context.enter_scope()
        
        parameters = []
        for i, arg in enumerate(node.args):
            default_value = None
            if i >= len(node.args) - len(node.defaults):
                default_index = i - (len(node.args) - len(node.defaults))
                default_value = node.defaults[default_index].accept(self)
            
            param = Parameter(
                name=arg,
                data_type="Any",
                default_value=default_value
            )
            parameters.append(param)
            self.context.declare_variable(arg, "Any")
        
        body = []
        for stmt in node.body:
            runa_stmt = stmt.accept(self)
            if runa_stmt:
                body.append(runa_stmt)
        
        self.context.exit_scope()
        
        return RunaFunctionDefinition(
            name=node.name,
            parameters=parameters,
            body=body,
            return_type="Any",
            metadata={"starlark_function": True}
        )
    
    def visit_return(self, node: StarlarkReturn) -> ReturnStatementStatement:
        """Convert Starlark return statement to Runa return statement."""
        value = node.value.accept(self) if node.value else None
        
        return ReturnStatementStatement(
            value=value,
            metadata={"starlark_return": True}
        )
    
    def visit_if(self, node: StarlarkIf) -> IfStatement:
        """Convert Starlark if statement to Runa if statement."""
        condition = node.test.accept(self)
        
        then_body = []
        for stmt in node.body:
            runa_stmt = stmt.accept(self)
            if runa_stmt:
                then_body.append(runa_stmt)
        
        else_body = []
        for stmt in node.orelse:
            runa_stmt = stmt.accept(self)
            if runa_stmt:
                else_body.append(runa_stmt)
        
        return IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            metadata={"starlark_if": True}
        )
    
    def visit_for(self, node: StarlarkFor) -> RunaForLoop:
        """Convert Starlark for loop to Runa for loop."""
        self.context.enter_scope()
        self.context.declare_variable(node.target, "Any")
        
        iterable = node.iter.accept(self)
        
        body = []
        for stmt in node.body:
            runa_stmt = stmt.accept(self)
            if runa_stmt:
                body.append(runa_stmt)
        
        self.context.exit_scope()
        
        return RunaForLoop(
            variable=node.target,
            iterable=iterable,
            body=body,
            metadata={"starlark_for": True}
        )
    
    def visit_break(self, node: StarlarkBreak) -> BreakStatementStatement:
        """Convert Starlark break statement to Runa break statement."""
        return BreakStatementStatement(metadata={"starlark_break": True})
    
    def visit_continue(self, node: StarlarkContinue) -> ContinueStatementStatement:
        """Convert Starlark continue statement to Runa continue statement."""
        return ContinueStatementStatement(metadata={"starlark_continue": True})
    
    def visit_pass(self, node: StarlarkPass) -> RunaPassStatement:
        """Convert Starlark pass statement to Runa pass statement."""
        return RunaPassStatement(metadata={"starlark_pass": True})
    
    def visit_load(self, node: StarlarkLoad) -> ImportStatement:
        """Convert Starlark load statement to Runa import statement."""
        # Convert load to specialized import
        imports = []
        for symbol in node.symbols:
            alias = node.aliases.get(symbol, symbol)
            imports.append(RunaImportItem(name=symbol, alias=alias if alias != symbol else None))
        
        return ImportStatement(
            module=node.module,
            imports=imports,
            metadata={
                "starlark_load": True,
                "original_module": node.module,
                "aliases": node.aliases
            }
        )
    
    def visit_rule(self, node: StarlarkRule) -> RunaExtensionConstruct:
        """Convert Starlark rule to Runa extension construct."""
        implementation = node.implementation.accept(self)
        
        attrs_dict = {}
        for name, value in node.attrs.items():
            attrs_dict[name] = value.accept(self)
        
        return RunaExtensionConstruct(
            construct_type="starlark_rule",
            name=node.name,
            parameters={
                "implementation": implementation,
                "attrs": attrs_dict,
                "doc": node.doc
            },
            metadata={
                "starlark_rule": True,
                "original_name": node.name
            }
        )
    
    def visit_aspect(self, node: StarlarkAspect) -> RunaExtensionConstruct:
        """Convert Starlark aspect to Runa extension construct."""
        implementation = node.implementation.accept(self)
        
        attrs_dict = {}
        for name, value in node.attrs.items():
            attrs_dict[name] = value.accept(self)
        
        return RunaExtensionConstruct(
            construct_type="starlark_aspect",
            name=node.name,
            parameters={
                "implementation": implementation,
                "attr_aspects": node.attr_aspects,
                "attrs": attrs_dict
            },
            metadata={
                "starlark_aspect": True,
                "original_name": node.name
            }
        )
    
    def visit_provider(self, node: StarlarkProvider) -> RunaExtensionConstruct:
        """Convert Starlark provider to Runa extension construct."""
        return RunaExtensionConstruct(
            construct_type="starlark_provider",
            name=node.name,
            parameters={
                "fields": node.fields,
                "doc": node.doc
            },
            metadata={
                "starlark_provider": True,
                "original_name": node.name
            }
        )


class RunaToStarlarkConverter:
    """Converts Runa Universal AST to Starlark AST."""
    
    def __init__(self):
        self.context = ConversionContext(
            scope_stack=[{}],
            type_hints={},
            metadata={},
            errors=[],
            warnings=[]
        )
    
    def convert(self, runa_node: RunaNode) -> StarlarkNode:
        """Convert a Runa Universal AST node to Starlark AST."""
        return self._convert_node(runa_node)
    
    def _convert_node(self, node: RunaNode) -> StarlarkNode:
        """Internal method to convert nodes based on type."""
        if isinstance(node, RunaModule):
            return self._convert_module(node)
        elif isinstance(node, StringLiteral):
            return self._convert_literal(node)
        elif isinstance(node, Identifier):
            return self._convert_identifier(node)
        elif isinstance(node, RunaBinaryOp):
            return self._convert_binary_op(node)
        elif isinstance(node, RunaUnaryOp):
            return self._convert_unary_op(node)
        elif isinstance(node, FunctionCall):
            return self._convert_function_call(node)
        elif isinstance(node, ListLiteral):
            return self._convert_list(node)
        elif isinstance(node, RunaDictionary):
            return self._convert_dictionary(node)
        elif isinstance(node, SetStatement):
            return self._convert_assignment(node)
        elif isinstance(node, RunaFunctionDefinition):
            return self._convert_function_definition(node)
        elif isinstance(node, IfStatement):
            return self._convert_if_statement(node)
        elif isinstance(node, RunaForLoop):
            return self._convert_for_loop(node)
        elif isinstance(node, ReturnStatementStatement):
            return self._convert_return_statement(node)
        elif isinstance(node, ImportStatement):
            return self._convert_import_statement(node)
        elif isinstance(node, RunaExtensionConstruct):
            return self._convert_extension_construct(node)
        else:
            self.context.add_warning(f"Unsupported Runa node type: {type(node).__name__}")
            return starlark_none()
    
    def _convert_module(self, node: RunaModule) -> StarlarkModule:
        """Convert Runa module to Starlark module."""
        statements = []
        
        for stmt in node.statements:
            try:
                starlark_stmt = self._convert_node(stmt)
                if starlark_stmt and isinstance(starlark_stmt, StarlarkStatement):
                    statements.append(starlark_stmt)
            except Exception as e:
                self.context.add_error(f"Failed to convert statement: {e}")
        
        docstring = node.metadata.get("docstring") if node.metadata else None
        
        return StarlarkModule(body=statements, docstring=docstring)
    
    def _convert_literal(self, node: StringLiteral) -> StarlarkLiteral:
        """Convert Runa literal to Starlark literal."""
        type_mapping = {
            "Int": "int",
            "Float": "float",
            "String": "string", 
            "Bool": "bool",
            "None": "none"
        }
        
        literal_type = type_mapping.get(node.data_type, "string")
        
        return StarlarkLiteral(value=node.value, literal_type=literal_type)
    
    def _convert_identifier(self, node: Identifier) -> StarlarkIdentifier:
        """Convert Runa identifier to Starlark identifier."""
        return StarlarkIdentifier(name=node.name)
    
    def _convert_binary_op(self, node: RunaBinaryOp) -> StarlarkExpression:
        """Convert Runa binary operation to Starlark binary operation."""
        left = self._convert_node(node.left)
        right = self._convert_node(node.right)
        
        operator_mapping = {
            "+": StarlarkOperator.ADD,
            "-": StarlarkOperator.SUB,
            "*": StarlarkOperator.MUL,
            "/": StarlarkOperator.DIV,
            "//": StarlarkOperator.FLOOR_DIV,
            "%": StarlarkOperator.MOD,
            "**": StarlarkOperator.POW,
            "|": StarlarkOperator.BIT_OR,
            "^": StarlarkOperator.BIT_XOR,
            "&": StarlarkOperator.BIT_AND,
            "<<": StarlarkOperator.LEFT_SHIFT,
            ">>": StarlarkOperator.RIGHT_SHIFT,
            "==": StarlarkOperator.EQ,
            "!=": StarlarkOperator.NE,
            "<": StarlarkOperator.LT,
            "<=": StarlarkOperator.LE,
            ">": StarlarkOperator.GT,
            ">=": StarlarkOperator.GE,
            "in": StarlarkOperator.IN,
            "not in": StarlarkOperator.NOT_IN,
            "is": StarlarkOperator.IS,
            "is not": StarlarkOperator.IS_NOT
        }
        
        if node.operator in ["and", "or"]:
            operator = StarlarkOperator.AND if node.operator == "and" else StarlarkOperator.OR
            return StarlarkBoolOp(operator=operator, values=[left, right])
        
        operator = operator_mapping.get(node.operator)
        if operator in [StarlarkOperator.EQ, StarlarkOperator.NE, StarlarkOperator.LT, 
                       StarlarkOperator.LE, StarlarkOperator.GT, StarlarkOperator.GE,
                       StarlarkOperator.IN, StarlarkOperator.NOT_IN]:
            return StarlarkComparison(left=left, operators=[operator], comparators=[right])
        
        if operator:
            return StarlarkBinaryOp(left=left, operator=operator, right=right)
        
        self.context.add_warning(f"Unknown binary operator: {node.operator}")
        return StarlarkBinaryOp(left=left, operator=StarlarkOperator.ADD, right=right)
    
    def _convert_unary_op(self, node: RunaUnaryOp) -> StarlarkUnaryOp:
        """Convert Runa unary operation to Starlark unary operation."""
        operand = self._convert_node(node.operand)
        
        operator_mapping = {
            "+": StarlarkOperator.UADD,
            "-": StarlarkOperator.USUB,
            "not": StarlarkOperator.NOT,
            "~": StarlarkOperator.INVERT
        }
        
        operator = operator_mapping.get(node.operator, StarlarkOperator.NOT)
        
        return StarlarkUnaryOp(operator=operator, operand=operand)
    
    def _convert_function_call(self, node: FunctionCall) -> StarlarkCall:
        """Convert Runa function call to Starlark call."""
        func = self._convert_node(node.function)
        args = [self._convert_node(arg) for arg in node.arguments]
        
        keywords = []
        for kw in node.keyword_arguments:
            value = self._convert_node(kw.value)
            keywords.append(StarlarkKeyword(arg=kw.name, value=value))
        
        return StarlarkCall(func=func, args=args, keywords=keywords)
    
    def _convert_list(self, node: ListLiteral) -> StarlarkList:
        """Convert Runa list to Starlark list."""
        elements = [self._convert_node(elem) for elem in node.elements]
        return StarlarkList(elements=elements)
    
    def _convert_dictionary(self, node: RunaDictionary) -> StarlarkDict:
        """Convert Runa dictionary to Starlark dictionary."""
        keys = []
        values = []
        
        for pair in node.pairs:
            keys.append(self._convert_node(pair.key))
            values.append(self._convert_node(pair.value))
        
        return StarlarkDict(keys=keys, values=values)
    
    def _convert_assignment(self, node: SetStatement) -> StarlarkAssign:
        """Convert Runa assignment to Starlark assignment."""
        target = self._convert_node(node.target)
        value = self._convert_node(node.value)
        
        return StarlarkAssign(targets=[target], value=value)
    
    def _convert_function_definition(self, node: RunaFunctionDefinition) -> StarlarkFunctionDef:
        """Convert Runa function definition to Starlark function definition."""
        args = [param.name for param in node.parameters]
        defaults = []
        
        for param in node.parameters:
            if param.default_value:
                defaults.append(self._convert_node(param.default_value))
        
        body = []
        for stmt in node.body:
            starlark_stmt = self._convert_node(stmt)
            if isinstance(starlark_stmt, StarlarkStatement):
                body.append(starlark_stmt)
        
        return StarlarkFunctionDef(name=node.name, args=args, defaults=defaults, body=body)
    
    def _convert_if_statement(self, node: IfStatement) -> StarlarkIf:
        """Convert Runa if statement to Starlark if statement."""
        test = self._convert_node(node.condition)
        
        body = []
        for stmt in node.then_body:
            starlark_stmt = self._convert_node(stmt)
            if isinstance(starlark_stmt, StarlarkStatement):
                body.append(starlark_stmt)
        
        orelse = []
        for stmt in node.else_body:
            starlark_stmt = self._convert_node(stmt)
            if isinstance(starlark_stmt, StarlarkStatement):
                orelse.append(starlark_stmt)
        
        return StarlarkIf(test=test, body=body, orelse=orelse)
    
    def _convert_for_loop(self, node: RunaForLoop) -> StarlarkFor:
        """Convert Runa for loop to Starlark for loop."""
        iter_expr = self._convert_node(node.iterable)
        
        body = []
        for stmt in node.body:
            starlark_stmt = self._convert_node(stmt)
            if isinstance(starlark_stmt, StarlarkStatement):
                body.append(starlark_stmt)
        
        return StarlarkFor(target=node.variable, iter=iter_expr, body=body)
    
    def _convert_return_statement(self, node: ReturnStatementStatement) -> StarlarkReturn:
        """Convert Runa return statement to Starlark return statement."""
        value = self._convert_node(node.value) if node.value else None
        return StarlarkReturn(value=value)
    
    def _convert_import_statement(self, node: ImportStatement) -> StarlarkLoad:
        """Convert Runa import statement to Starlark load statement."""
        symbols = []
        aliases = {}
        
        for import_item in node.imports:
            symbols.append(import_item.name)
            if import_item.alias:
                aliases[import_item.name] = import_item.alias
        
        return StarlarkLoad(module=node.module, symbols=symbols, aliases=aliases)
    
    def _convert_extension_construct(self, node: RunaExtensionConstruct) -> StarlarkStatement:
        """Convert Runa extension construct to Starlark construct."""
        if node.construct_type == "starlark_rule":
            implementation = self._convert_node(node.parameters["implementation"])
            attrs = {}
            for name, value in node.parameters["attrs"].items():
                attrs[name] = self._convert_node(value)
            
            return StarlarkRule(
                name=node.name,
                implementation=implementation,
                attrs=attrs,
                doc=node.parameters.get("doc")
            )
        
        elif node.construct_type == "starlark_aspect":
            implementation = self._convert_node(node.parameters["implementation"])
            attrs = {}
            for name, value in node.parameters["attrs"].items():
                attrs[name] = self._convert_node(value)
            
            return StarlarkAspect(
                name=node.name,
                implementation=implementation,
                attr_aspects=node.parameters["attr_aspects"],
                attrs=attrs
            )
        
        elif node.construct_type == "starlark_provider":
            return StarlarkProvider(
                name=node.name,
                fields=node.parameters["fields"],
                doc=node.parameters.get("doc")
            )
        
        self.context.add_warning(f"Unknown extension construct type: {node.construct_type}")
        return StarlarkPass()


# Main conversion functions

def starlark_to_runa(starlark_ast: StarlarkNode) -> RunaNode:
    """Convert Starlark AST to Runa Universal AST."""
    converter = StarlarkToRunaConverter()
    return converter.convert(starlark_ast)


def runa_to_starlark(runa_ast: RunaNode) -> StarlarkNode:
    """Convert Runa Universal AST to Starlark AST.""" 
    converter = RunaToStarlarkConverter()
    return converter.convert(runa_ast)


__all__ = [
    "ConversionContext",
    "StarlarkToRunaConverter", 
    "RunaToStarlarkConverter",
    "starlark_to_runa",
    "runa_to_starlark"
] 