#!/usr/bin/env python3
"""
Rholang Converter Implementation

This module provides bidirectional conversion between Rholang AST and Runa Universal AST.
It handles all Rholang language constructs including process calculus, channels, and
blockchain-specific features, mapping them to equivalent Runa representations.

Key conversion features:
- Process-oriented constructs to Runa concurrent patterns
- Channel communication to message passing abstractions
- Pattern matching preservation
- Blockchain contract mapping to Runa smart contract constructs
- Concurrency and parallelism preservation
"""

from typing import Any, List, Optional, Dict, Union, Set
from dataclasses import dataclass

from ...runa.runa_ast import *
from .rholang_ast import *


@dataclass
class RholangConversionContext:
    """Context for tracking Rholang conversion state."""
    
    scope_stack: List[Dict[str, Any]]
    channel_mappings: Dict[str, str]
    process_mappings: Dict[str, str]
    metadata: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    
    def __post_init__(self):
        if not self.scope_stack:
            self.scope_stack = [{}]
        if not self.channel_mappings:
            self.channel_mappings = {}
        if not self.process_mappings:
            self.process_mappings = {}
        if not self.metadata:
            self.metadata = {}
        if not self.errors:
            self.errors = []
        if not self.warnings:
            self.warnings = []


class RholangToRunaConverter:
    """Converts Rholang AST to Runa Universal AST."""
    
    def __init__(self):
        self.context = RholangConversionContext(
            scope_stack=[{}],
            channel_mappings={},
            process_mappings={},
            metadata={},
            errors=[],
            warnings=[]
        )
    
    def convert(self, rholang_node: RholangNode) -> RunaNode:
        """Convert a Rholang AST node to Runa Universal AST."""
        return rholang_node.accept(self)
    
    def visit_module(self, node: RholangModule) -> RunaModule:
        """Convert Rholang module to Runa module."""
        runa_statements = []
        
        for process in node.body:
            try:
                runa_stmt = process.accept(self)
                if runa_stmt:
                    runa_statements.append(runa_stmt)
            except Exception as e:
                self.context.errors.append(f"Failed to convert process: {e}")
        
        metadata = {
            "original_language": "rholang",
            "process_oriented": True,
            "blockchain_platform": "rchain",
            "conversion_context": {
                "errors": self.context.errors,
                "warnings": self.context.warnings,
                "channel_mappings": self.context.channel_mappings
            }
        }
        
        return RunaModule(
            statements=runa_statements,
            metadata=metadata
        )
    
    def visit_par(self, node: RholangPar) -> RunaConcurrentBlock:
        """Convert Rholang parallel composition to Runa concurrent block."""
        concurrent_processes = []
        
        for process in node.processes:
            runa_process = process.accept(self)
            concurrent_processes.append(runa_process)
        
        return RunaConcurrentBlock(
            processes=concurrent_processes,
            synchronization_type="parallel",
            metadata={"rholang_par": True}
        )
    
    def visit_new(self, node: RholangNew) -> RunaChannelDeclaration:
        """Convert Rholang new construct to Runa channel declaration."""
        channels = []
        
        for name in node.names:
            channel = RunaChannel(
                name=name,
                channel_type="private",
                metadata={"rholang_new": True}
            )
            channels.append(channel)
            self.context.channel_mappings[name] = name
        
        body = node.process.accept(self)
        
        return RunaChannelDeclaration(
            channels=channels,
            scope=body,
            metadata={"rholang_new": True, "uri_patterns": node.uri_patterns}
        )
    
    def visit_send(self, node: RholangSend) -> RunaMessageSend:
        """Convert Rholang send to Runa message send."""
        channel = node.channel.accept(self)
        
        data = []
        for item in node.data:
            runa_item = item.accept(self)
            data.append(runa_item)
        
        return RunaMessageSend(
            channel=channel,
            message=data[0] if len(data) == 1 else RunaTuple(elements=data),
            persistent=node.persistent,
            metadata={
                "rholang_send": True,
                "peek": node.peek,
                "data_count": len(data)
            }
        )
    
    def visit_receive(self, node: RholangReceive) -> RunaMessageReceive:
        """Convert Rholang receive to Runa message receive."""
        patterns = []
        
        for receive_pattern in node.receives:
            channel = receive_pattern.channel.accept(self)
            
            # Convert patterns to Runa patterns
            runa_patterns = []
            for pattern in receive_pattern.patterns:
                runa_pattern = self._convert_pattern(pattern)
                runa_patterns.append(runa_pattern)
            
            receive_case = RunaReceiveCase(
                channel=channel,
                patterns=runa_patterns,
                condition=receive_pattern.condition.accept(self) if receive_pattern.condition else None
            )
            patterns.append(receive_case)
        
        continuation = node.continuation.accept(self)
        
        return RunaMessageReceive(
            cases=patterns,
            continuation=continuation,
            persistent=node.persistent,
            metadata={
                "rholang_receive": True,
                "peek": node.peek
            }
        )
    
    def visit_contract(self, node: RholangContract) -> RunaContractDefinition:
        """Convert Rholang contract to Runa contract definition."""
        name = node.name.accept(self)
        
        parameters = []
        for pattern in node.parameters:
            param = self._convert_pattern_to_parameter(pattern)
            parameters.append(param)
        
        body = node.body.accept(self)
        
        return RunaContractDefinition(
            name=name,
            parameters=parameters,
            body=body,
            blockchain_platform="rchain",
            metadata={"rholang_contract": True}
        )
    
    def visit_match(self, node: RholangMatch) -> RunaMatchExpression:
        """Convert Rholang match to Runa match expression."""
        target = node.target.accept(self)
        
        cases = []
        for case in node.cases:
            pattern = self._convert_pattern(case.pattern)
            body = case.body.accept(self)
            condition = case.condition.accept(self) if case.condition else None
            
            match_case = RunaMatchCase(
                pattern=pattern,
                body=body,
                condition=condition
            )
            cases.append(match_case)
        
        return RunaMatchExpression(
            target=target,
            cases=cases,
            metadata={"rholang_match": True}
        )
    
    def visit_if(self, node: RholangIf) -> IfStatement:
        """Convert Rholang if to Runa if statement."""
        condition = node.condition.accept(self)
        then_body = [node.then_process.accept(self)]
        else_body = [node.else_process.accept(self)] if node.else_process else []
        
        return IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            metadata={"rholang_if": True}
        )
    
    def visit_for(self, node: RholangFor) -> RunaForComprehension:
        """Convert Rholang for to Runa for comprehension."""
        variables = []
        iterables = []
        
        for var, gen in zip(node.variables, node.generators):
            var_name = self._extract_pattern_name(var)
            variables.append(var_name)
            iterable = gen.accept(self)
            iterables.append(iterable)
        
        body = node.body.accept(self)
        
        return RunaForComprehension(
            variables=variables,
            iterables=iterables,
            body=body,
            metadata={"rholang_for": True}
        )
    
    def visit_literal(self, node: RholangLiteral) -> StringLiteral:
        """Convert Rholang literal to Runa literal."""
        type_mapping = {
            "int": "Int",
            "string": "String",
            "bool": "Bool",
            "bytes": "Bytes",
            "uri": "URI"
        }
        
        return StringLiteral(
            value=node.value,
            data_type=type_mapping.get(node.literal_type, "Any"),
            metadata={"rholang_type": node.literal_type}
        )
    
    def visit_name(self, node: RholangName) -> Identifier:
        """Convert Rholang name to Runa identifier."""
        if node.is_wildcard:
            return RunaWildcard(metadata={"rholang_wildcard": True})
        
        return Identifier(
            name=node.name,
            data_type="Any",
            metadata={"rholang_name": True}
        )
    
    def visit_quote(self, node: RholangQuote) -> RunaQuotedExpression:
        """Convert Rholang quote to Runa quoted expression."""
        quoted_process = node.process.accept(self)
        
        return RunaQuotedExpression(
            expression=quoted_process,
            metadata={"rholang_quote": True}
        )
    
    def visit_list(self, node: RholangList) -> ListLiteral:
        """Convert Rholang list to Runa list."""
        elements = [elem.accept(self) for elem in node.elements]
        
        return ListLiteral(
            elements=elements,
            element_type="Any",
            metadata={"rholang_list": True}
        )
    
    def visit_tuple(self, node: RholangTuple) -> RunaTuple:
        """Convert Rholang tuple to Runa tuple."""
        elements = [elem.accept(self) for elem in node.elements]
        
        return RunaTuple(
            elements=elements,
            metadata={"rholang_tuple": True}
        )
    
    def visit_set(self, node: RholangSet) -> SetStatement:
        """Convert Rholang set to Runa set."""
        elements = [elem.accept(self) for elem in node.elements]
        
        return SetStatement(
            elements=elements,
            element_type="Any",
            metadata={"rholang_set": True}
        )
    
    def visit_map(self, node: RholangMap) -> RunaDictionary:
        """Convert Rholang map to Runa dictionary."""
        pairs = []
        for pair in node.pairs:
            key = pair.key.accept(self)
            value = pair.value.accept(self)
            pairs.append(RunaKeyValuePair(key=key, value=value))
        
        return RunaDictionary(
            pairs=pairs,
            key_type="Any",
            value_type="Any",
            metadata={"rholang_map": True}
        )
    
    def visit_binary_op(self, node: RholangBinaryOp) -> RunaBinaryOp:
        """Convert Rholang binary operation to Runa binary operation."""
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        operator_mapping = {
            RholangOperator.ADD: "+",
            RholangOperator.SUB: "-",
            RholangOperator.MUL: "*",
            RholangOperator.DIV: "/",
            RholangOperator.MOD: "%",
            RholangOperator.POW: "**",
            RholangOperator.EQ: "==",
            RholangOperator.NE: "!=",
            RholangOperator.LT: "<",
            RholangOperator.LE: "<=",
            RholangOperator.GT: ">",
            RholangOperator.GE: ">=",
            RholangOperator.AND: "and",
            RholangOperator.OR: "or",
        }
        
        runa_operator = operator_mapping.get(node.operator, node.operator.value)
        
        return RunaBinaryOp(
            left=left,
            operator=runa_operator,
            right=right,
            metadata={"rholang_operator": node.operator.value}
        )
    
    def visit_unary_op(self, node: RholangUnaryOp) -> RunaUnaryOp:
        """Convert Rholang unary operation to Runa unary operation."""
        operand = node.operand.accept(self)
        
        operator_mapping = {
            RholangOperator.NOT: "not",
            RholangOperator.UADD: "+",
            RholangOperator.USUB: "-",
        }
        
        runa_operator = operator_mapping.get(node.operator, node.operator.value)
        
        return RunaUnaryOp(
            operator=runa_operator,
            operand=operand,
            metadata={"rholang_operator": node.operator.value}
        )
    
    def visit_method_call(self, node: RholangMethodCall) -> RunaMethodCall:
        """Convert Rholang method call to Runa method call."""
        target = node.target.accept(self)
        arguments = [arg.accept(self) for arg in node.arguments]
        
        return RunaMethodCall(
            target=target,
            method=node.method,
            arguments=arguments,
            metadata={"rholang_method_call": True}
        )
    
    def visit_pattern(self, node: RholangPattern) -> Pattern:
        """Convert Rholang pattern to Runa pattern."""
        return self._convert_pattern(node)
    
    def visit_nil(self, node: RholangNil) -> RunaNilProcess:
        """Convert Rholang nil to Runa nil process."""
        return RunaNilProcess(metadata={"rholang_nil": True})
    
    def visit_bundle(self, node: RholangBundle) -> RunaCapabilityWrapper:
        """Convert Rholang bundle to Runa capability wrapper."""
        process = node.process.accept(self)
        
        return RunaCapabilityWrapper(
            capability_type=node.bundle_type,
            wrapped_expression=process,
            metadata={"rholang_bundle": True}
        )
    
    def _convert_pattern(self, pattern: RholangPattern) -> Pattern:
        """Convert a Rholang pattern to Runa pattern."""
        if isinstance(pattern, RholangVarPattern):
            return RunaVariablePattern(name=pattern.name)
        elif isinstance(pattern, RholangWildcardPattern):
            return WildcardPattern()
        elif isinstance(pattern, RholangListPattern):
            patterns = [self._convert_pattern(p) for p in pattern.patterns]
            return ListPattern(patterns=patterns)
        elif isinstance(pattern, RholangTuplePattern):
            patterns = [self._convert_pattern(p) for p in pattern.patterns]
            return RunaTuplePattern(patterns=patterns)
        else:
            return WildcardPattern()
    
    def _convert_pattern_to_parameter(self, pattern: RholangPattern) -> Parameter:
        """Convert a Rholang pattern to a Runa parameter."""
        if isinstance(pattern, RholangVarPattern):
            return Parameter(name=pattern.name, data_type="Any")
        else:
            return Parameter(name="_", data_type="Any")
    
    def _extract_pattern_name(self, pattern: RholangPattern) -> str:
        """Extract variable name from pattern."""
        if isinstance(pattern, RholangVarPattern):
            return pattern.name
        else:
            return "_"


class RunaToRholangConverter:
    """Converts Runa Universal AST to Rholang AST."""
    
    def __init__(self):
        self.context = RholangConversionContext(
            scope_stack=[{}],
            channel_mappings={},
            process_mappings={},
            metadata={},
            errors=[],
            warnings=[]
        )
    
    def convert(self, runa_node: RunaNode) -> RholangNode:
        """Convert a Runa Universal AST node to Rholang AST."""
        return self._convert_node(runa_node)
    
    def _convert_node(self, node: RunaNode) -> RholangNode:
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
        elif isinstance(node, ListLiteral):
            return self._convert_list(node)
        elif isinstance(node, RunaTuple):
            return self._convert_tuple(node)
        elif isinstance(node, RunaDictionary):
            return self._convert_dictionary(node)
        elif isinstance(node, RunaConcurrentBlock):
            return self._convert_concurrent_block(node)
        elif isinstance(node, RunaMessageSend):
            return self._convert_message_send(node)
        elif isinstance(node, RunaMessageReceive):
            return self._convert_message_receive(node)
        elif isinstance(node, RunaContractDefinition):
            return self._convert_contract_definition(node)
        elif isinstance(node, RunaMatchExpression):
            return self._convert_match_expression(node)
        elif isinstance(node, IfStatement):
            return self._convert_if_statement(node)
        else:
            self.context.warnings.append(f"Unsupported Runa node type: {type(node).__name__}")
            return rho_nil()
    
    def _convert_module(self, node: RunaModule) -> RholangModule:
        """Convert Runa module to Rholang module."""
        processes = []
        
        for stmt in node.statements:
            try:
                rholang_process = self._convert_node(stmt)
                if isinstance(rholang_process, RholangProcess):
                    processes.append(rholang_process)
            except Exception as e:
                self.context.errors.append(f"Failed to convert statement: {e}")
        
        return RholangModule(body=processes)
    
    def _convert_literal(self, node: StringLiteral) -> RholangLiteral:
        """Convert Runa literal to Rholang literal."""
        type_mapping = {
            "Int": "int",
            "String": "string",
            "Bool": "bool",
            "Bytes": "bytes",
            "URI": "uri"
        }
        
        literal_type = type_mapping.get(node.data_type, "string")
        
        return RholangLiteral(value=node.value, literal_type=literal_type)
    
    def _convert_identifier(self, node: Identifier) -> RholangName:
        """Convert Runa identifier to Rholang name."""
        return RholangName(name=node.name)
    
    def _convert_binary_op(self, node: RunaBinaryOp) -> RholangBinaryOp:
        """Convert Runa binary operation to Rholang binary operation."""
        left = self._convert_node(node.left)
        right = self._convert_node(node.right)
        
        operator_mapping = {
            "+": RholangOperator.ADD,
            "-": RholangOperator.SUB,
            "*": RholangOperator.MUL,
            "/": RholangOperator.DIV,
            "%": RholangOperator.MOD,
            "**": RholangOperator.POW,
            "==": RholangOperator.EQ,
            "!=": RholangOperator.NE,
            "<": RholangOperator.LT,
            "<=": RholangOperator.LE,
            ">": RholangOperator.GT,
            ">=": RholangOperator.GE,
            "and": RholangOperator.AND,
            "or": RholangOperator.OR,
        }
        
        operator = operator_mapping.get(node.operator, RholangOperator.ADD)
        
        return RholangBinaryOp(left=left, operator=operator, right=right)
    
    def _convert_unary_op(self, node: RunaUnaryOp) -> RholangUnaryOp:
        """Convert Runa unary operation to Rholang unary operation."""
        operand = self._convert_node(node.operand)
        
        operator_mapping = {
            "not": RholangOperator.NOT,
            "+": RholangOperator.UADD,
            "-": RholangOperator.USUB,
        }
        
        operator = operator_mapping.get(node.operator, RholangOperator.NOT)
        
        return RholangUnaryOp(operator=operator, operand=operand)
    
    def _convert_list(self, node: ListLiteral) -> RholangList:
        """Convert Runa list to Rholang list."""
        elements = [self._convert_node(elem) for elem in node.elements]
        return RholangList(elements=elements)
    
    def _convert_tuple(self, node: RunaTuple) -> RholangTuple:
        """Convert Runa tuple to Rholang tuple."""
        elements = [self._convert_node(elem) for elem in node.elements]
        return RholangTuple(elements=elements)
    
    def _convert_dictionary(self, node: RunaDictionary) -> RholangMap:
        """Convert Runa dictionary to Rholang map."""
        pairs = []
        for pair in node.pairs:
            key = self._convert_node(pair.key)
            value = self._convert_node(pair.value)
            pairs.append(RholangMapPair(key=key, value=value))
        
        return RholangMap(pairs=pairs)
    
    def _convert_concurrent_block(self, node: RunaConcurrentBlock) -> RholangPar:
        """Convert Runa concurrent block to Rholang parallel composition."""
        processes = []
        for process in node.processes:
            rholang_process = self._convert_node(process)
            if isinstance(rholang_process, RholangProcess):
                processes.append(rholang_process)
        
        return RholangPar(processes=processes)
    
    def _convert_message_send(self, node: RunaMessageSend) -> RholangSend:
        """Convert Runa message send to Rholang send."""
        channel = self._convert_node(node.channel)
        
        if isinstance(node.message, RunaTuple):
            data = [self._convert_node(elem) for elem in node.message.elements]
        else:
            data = [self._convert_node(node.message)]
        
        return RholangSend(channel=channel, data=data, persistent=node.persistent)
    
    def _convert_message_receive(self, node: RunaMessageReceive) -> RholangReceive:
        """Convert Runa message receive to Rholang receive."""
        receives = []
        
        for case in node.cases:
            channel = self._convert_node(case.channel)
            patterns = [self._convert_runa_pattern(p) for p in case.patterns]
            condition = self._convert_node(case.condition) if case.condition else None
            
            receive_pattern = RholangReceivePattern(
                channel=channel,
                patterns=patterns,
                condition=condition
            )
            receives.append(receive_pattern)
        
        continuation = self._convert_node(node.continuation)
        
        return RholangReceive(
            receives=receives,
            continuation=continuation,
            persistent=node.persistent
        )
    
    def _convert_contract_definition(self, node: RunaContractDefinition) -> RholangContract:
        """Convert Runa contract definition to Rholang contract."""
        name = self._convert_node(node.name)
        
        parameters = []
        for param in node.parameters:
            pattern = rho_var_pattern(param.name)
            parameters.append(pattern)
        
        body = self._convert_node(node.body)
        
        return RholangContract(name=name, parameters=parameters, body=body)
    
    def _convert_match_expression(self, node: RunaMatchExpression) -> RholangMatch:
        """Convert Runa match expression to Rholang match."""
        target = self._convert_node(node.target)
        
        cases = []
        for case in node.cases:
            pattern = self._convert_runa_pattern(case.pattern)
            body = self._convert_node(case.body)
            condition = self._convert_node(case.condition) if case.condition else None
            
            rholang_case = RholangMatchCase(pattern=pattern, condition=condition, body=body)
            cases.append(rholang_case)
        
        return RholangMatch(target=target, cases=cases)
    
    def _convert_if_statement(self, node: IfStatement) -> RholangIf:
        """Convert Runa if statement to Rholang if."""
        condition = self._convert_node(node.condition)
        then_process = self._convert_node(node.then_body[0]) if node.then_body else rho_nil()
        else_process = self._convert_node(node.else_body[0]) if node.else_body else None
        
        return RholangIf(condition=condition, then_process=then_process, else_process=else_process)
    
    def _convert_runa_pattern(self, pattern: Pattern) -> RholangPattern:
        """Convert Runa pattern to Rholang pattern."""
        if isinstance(pattern, RunaVariablePattern):
            return rho_var_pattern(pattern.name)
        elif isinstance(pattern, WildcardPattern):
            return rho_wildcard_pattern()
        elif isinstance(pattern, ListPattern):
            patterns = [self._convert_runa_pattern(p) for p in pattern.patterns]
            return rho_list_pattern(patterns)
        elif isinstance(pattern, RunaTuplePattern):
            patterns = [self._convert_runa_pattern(p) for p in pattern.patterns]
            return rho_tuple_pattern(patterns)
        else:
            return rho_wildcard_pattern()


# Main conversion functions

def rholang_to_runa(rholang_ast: RholangNode) -> RunaNode:
    """Convert Rholang AST to Runa Universal AST."""
    converter = RholangToRunaConverter()
    return converter.convert(rholang_ast)


def runa_to_rholang(runa_ast: RunaNode) -> RholangNode:
    """Convert Runa Universal AST to Rholang AST."""
    converter = RunaToRholangConverter()
    return converter.convert(runa_ast)


__all__ = [
    "RholangConversionContext",
    "RholangToRunaConverter",
    "RunaToRholangConverter",
    "rholang_to_runa",
    "runa_to_rholang"
] 