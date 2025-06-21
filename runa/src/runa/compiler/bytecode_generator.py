"""
Runa Bytecode Generator

Generates optimized bytecode from AST nodes with multi-pass optimizations
and performance monitoring for the Runa programming language.
"""

import time
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import sys
from datetime import datetime

from ..error_handler import RunaError, ErrorCode, ErrorCategory, ErrorSeverity, ErrorContext, RunaErrorHandler
from ..performance_monitor import PerformanceMonitor
from .parser import ASTNode, BinaryExpression, UnaryExpression, Literal, Identifier, CallExpression


class Opcode(Enum):
    """Bytecode operation codes."""
    # Stack operations
    LOAD_CONST = "LOAD_CONST"
    LOAD_VAR = "LOAD_VAR"
    STORE_VAR = "STORE_VAR"
    DUP = "DUP"
    POP = "POP"
    SWAP = "SWAP"
    
    # Arithmetic operations
    BINARY_OP = "BINARY_OP"
    UNARY_OP = "UNARY_OP"
    
    # Control flow
    JUMP = "JUMP"
    JUMP_IF_FALSE = "JUMP_IF_FALSE"
    JUMP_IF_TRUE = "JUMP_IF_TRUE"
    RETURN = "RETURN"
    
    # Function calls
    CALL = "CALL"
    CALL_BUILTIN = "CALL_BUILTIN"
    
    # List and dictionary operations
    BUILD_LIST = "BUILD_LIST"
    BUILD_DICT = "BUILD_DICT"
    GET_ITEM = "GET_ITEM"
    SET_ITEM = "SET_ITEM"
    
    # Type operations
    TYPE_CHECK = "TYPE_CHECK"
    TYPE_CAST = "TYPE_CAST"
    
    # AI-specific operations
    AI_THINK = "AI_THINK"
    AI_LEARN = "AI_LEARN"
    AI_COMMUNICATE = "AI_COMMUNICATE"
    AI_TRANSLATE = "AI_TRANSLATE"
    AI_ANALYZE = "AI_ANALYZE"
    
    # Pattern matching
    MATCH_START = "MATCH_START"
    MATCH_CASE = "MATCH_CASE"
    MATCH_END = "MATCH_END"
    
    # Asynchronous operations
    AWAIT = "AWAIT"
    ASYNC_CALL = "ASYNC_CALL"
    
    # Memory management
    ALLOCATE = "ALLOCATE"
    DEALLOCATE = "DEALLOCATE"
    
    # Performance monitoring
    PROFILE_START = "PROFILE_START"
    PROFILE_END = "PROFILE_END"


@dataclass
class Instruction:
    """Represents a single bytecode instruction."""
    opcode: Opcode
    args: Dict[str, Any] = field(default_factory=dict)
    line_number: Optional[int] = None
    source_info: Optional[str] = None


@dataclass
class OptimizationPass:
    """Represents an optimization pass."""
    name: str
    description: str
    enabled: bool = True
    priority: int = 0


class BytecodeGenerator:
    """Generates optimized bytecode from AST nodes."""
    
    def __init__(self):
        self.instructions: List[Instruction] = []
        self.optimization_passes: List[OptimizationPass] = []
        self.performance_monitor = PerformanceMonitor()
        self.error_handler = RunaErrorHandler()
        self.symbol_table: Dict[str, Any] = {}
        self.label_counter = 0
        self.temp_var_counter = 0
        
        self._init_optimization_passes()
    
    def _init_optimization_passes(self) -> None:
        """Initialize optimization passes."""
        self.optimization_passes = [
            OptimizationPass("constant_folding", "Fold constant expressions", True, 1),
            OptimizationPass("dead_code_elimination", "Remove unreachable code", True, 2),
            OptimizationPass("strength_reduction", "Replace expensive operations with cheaper ones", True, 3),
            OptimizationPass("common_subexpression_elimination", "Eliminate redundant computations", True, 4),
            OptimizationPass("loop_optimization", "Optimize loop structures", True, 5),
            OptimizationPass("function_inlining", "Inline small functions", True, 6),
            OptimizationPass("register_allocation", "Optimize variable allocation", True, 7),
            OptimizationPass("ai_pattern_optimization", "Optimize AI-specific patterns", True, 8)
        ]
    
    def generate(self, ast: ASTNode) -> List[Dict[str, Any]]:
        """Generate bytecode from AST with optimizations."""
        start_time = time.time()
        
        try:
            self.instructions.clear()
            self.symbol_table.clear()
            self.label_counter = 0
            self.temp_var_counter = 0
            
            self._generate_node(ast)
            
            bytecode = self._instructions_to_bytecode()
            
            for optimization in sorted(self.optimization_passes, key=lambda x: x.priority):
                if optimization.enabled:
                    bytecode = self._apply_optimization(optimization, bytecode)
            
            generation_time = time.time() - start_time
            self.performance_monitor.record_operation(
                "bytecode_generation", generation_time,
                {"instructions": len(bytecode), "optimizations": len(self.optimization_passes)}
            )
            
            return bytecode
        
        except Exception as e:
            self.performance_monitor.record_error(f"Bytecode generation failed: {e}")
            error_context = ErrorContext(line=0, column=0)
            error = self.error_handler.create_error(
                ErrorCode.COMPILATION_FAILED,
                f"Bytecode generation failed: {e}",
                error_context,
                ErrorSeverity.ERROR
            )
            raise error
    
    def _generate_node(self, node: ASTNode) -> None:
        """Generate bytecode for an AST node."""
        if isinstance(node, Literal):
            self._generate_literal(node)
        elif isinstance(node, Identifier):
            self._generate_variable(node)
        elif isinstance(node, BinaryExpression):
            self._generate_binary_op(node)
        elif isinstance(node, UnaryExpression):
            self._generate_unary_op(node)
        elif isinstance(node, CallExpression):
            self._generate_function_call(node)
        else:
            error_context = ErrorContext(line=0, column=0)
            error = self.error_handler.create_error(
                ErrorCode.COMPILATION_FAILED,
                f"Unsupported node type: {type(node).__name__}",
                error_context,
                ErrorSeverity.ERROR
            )
            raise error
    
    def _generate_literal(self, node: Literal) -> None:
        """Generate bytecode for literal nodes."""
        instruction = Instruction(
            opcode=Opcode.LOAD_CONST,
            args={"value": node.value},
            line_number=node.line,
            source_info=f"literal: {node.value}"
        )
        self.instructions.append(instruction)
    
    def _generate_variable(self, node: Identifier) -> None:
        """Generate bytecode for variable nodes."""
        instruction = Instruction(
            opcode=Opcode.LOAD_VAR,
            args={"name": node.name},
            line_number=node.line,
            source_info=f"variable: {node.name}"
        )
        self.instructions.append(instruction)
    
    def _generate_binary_op(self, node: BinaryExpression) -> None:
        """Generate bytecode for binary operation nodes using Runa operators."""
        self._generate_node(node.left)
        self._generate_node(node.right)
        
        runa_operator = self._convert_to_runa_operator(node.operator)
        
        instruction = Instruction(
            opcode=Opcode.BINARY_OP,
            args={"operator": runa_operator},
            line_number=node.line,
            source_info=f"binary_op: {runa_operator}"
        )
        self.instructions.append(instruction)
    
    def _generate_unary_op(self, node: UnaryExpression) -> None:
        """Generate bytecode for unary operation nodes using Runa operators."""
        self._generate_node(node.operand)
        
        runa_operator = self._convert_to_runa_unary_operator(node.operator)
        
        instruction = Instruction(
            opcode=Opcode.UNARY_OP,
            args={"operator": runa_operator},
            line_number=node.line,
            source_info=f"unary_op: {runa_operator}"
        )
        self.instructions.append(instruction)
    
    def _generate_function_call(self, node: CallExpression) -> None:
        """Generate bytecode for function call nodes."""
        # Generate function expression first
        self._generate_node(node.callee)
        
        # Generate arguments
        for arg in node.arguments:
            self._generate_node(arg)
        
        instruction = Instruction(
            opcode=Opcode.CALL,
            args={"arg_count": len(node.arguments)},
            line_number=node.line,
            source_info=f"function_call: {node.callee}"
        )
        self.instructions.append(instruction)
    
    def _convert_to_runa_operator(self, operator: str) -> str:
        """Convert standard operators to Runa natural language operators."""
        operator_mapping = {
            "+": "plus",
            "-": "minus",
            "*": "multiplied by",
            "/": "divided by",
            "%": "modulo",
            "**": "to the power of",
            "==": "equals",
            "!=": "does not equal",
            "<": "is less than",
            "<=": "is less than or equal to",
            ">": "is greater than",
            ">=": "is greater than or equal to",
            "and": "and",
            "or": "or",
            "not": "not",
            "in": "is in",
            "not in": "is not in",
            "is": "is",
            "is not": "is not"
        }
        return operator_mapping.get(operator, operator)
    
    def _convert_to_runa_unary_operator(self, operator: str) -> str:
        """Convert unary operators to Runa natural language operators."""
        operator_mapping = {
            "+": "positive",
            "-": "negative",
            "not": "not",
            "~": "bitwise not"
        }
        return operator_mapping.get(operator, operator)
    
    def _instructions_to_bytecode(self) -> List[Dict[str, Any]]:
        """Convert instructions to bytecode format."""
        bytecode = []
        for instruction in self.instructions:
            bytecode.append({
                "opcode": instruction.opcode.value,
                "args": instruction.args,
                "line_number": instruction.line_number,
                "source_info": instruction.source_info
            })
        return bytecode
    
    def _apply_optimization(self, optimization: OptimizationPass, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply a specific optimization pass to bytecode."""
        start_time = time.time()
        
        try:
            if optimization.name == "constant_folding":
                optimized_bytecode = self._constant_folding(bytecode)
            elif optimization.name == "dead_code_elimination":
                optimized_bytecode = self._dead_code_elimination(bytecode)
            elif optimization.name == "strength_reduction":
                optimized_bytecode = self._strength_reduction(bytecode)
            elif optimization.name == "common_subexpression_elimination":
                optimized_bytecode = self._common_subexpression_elimination(bytecode)
            elif optimization.name == "loop_optimization":
                optimized_bytecode = self._loop_optimization(bytecode)
            elif optimization.name == "function_inlining":
                optimized_bytecode = self._function_inlining(bytecode)
            elif optimization.name == "register_allocation":
                optimized_bytecode = self._register_allocation(bytecode)
            elif optimization.name == "ai_pattern_optimization":
                optimized_bytecode = self._ai_pattern_optimization(bytecode)
            else:
                optimized_bytecode = bytecode
            
            optimization_time = time.time() - start_time
            self.performance_monitor.record_operation(
                f"optimization_{optimization.name}", optimization_time,
                {"original_instructions": len(bytecode), "optimized_instructions": len(optimized_bytecode)}
            )
            
            return optimized_bytecode
            
        except Exception as e:
            self.performance_monitor.record_error(f"Optimization {optimization.name} failed: {e}")
            return bytecode  # Return original bytecode if optimization fails
    
    def _constant_folding(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fold constant expressions at compile time."""
        optimized = []
        i = 0
        while i < len(bytecode):
            instruction = bytecode[i]
            # Look for constant folding opportunities
            if (
                instruction["opcode"] == "LOAD_CONST"
                and i + 1 < len(bytecode)
                and bytecode[i + 1]["opcode"] == "LOAD_CONST"
                and i + 2 < len(bytecode)
                and bytecode[i + 2]["opcode"] == "BINARY_OP"
            ):
                left = instruction["args"]["value"]
                right = bytecode[i + 1]["args"]["value"]
                operator = bytecode[i + 2]["args"]["operator"]
                try:
                    if operator == "plus":
                        result = left + right
                    elif operator == "minus":
                        result = left - right
                    elif operator == "multiplied by":
                        result = left * right
                    elif operator == "divided by":
                        if right == 0:
                            raise ValueError("Division by zero")
                        result = left / right
                    elif operator == "modulo":
                        result = left % right
                    elif operator == "to the power of":
                        result = left ** right
                    elif operator == "equals":
                        result = left == right
                    elif operator == "does not equal":
                        result = left != right
                    elif operator == "is greater than":
                        result = left > right
                    elif operator == "is less than":
                        result = left < right
                    elif operator == "is greater than or equal to":
                        result = left >= right
                    elif operator == "is less than or equal to":
                        result = left <= right
                    elif operator == "and":
                        result = left and right
                    elif operator == "or":
                        result = left or right
                    elif operator == "is in":
                        result = left in right
                    elif operator == "is not in":
                        result = left not in right
                    elif operator == "is":
                        result = left is right
                    elif operator == "is not":
                        result = left is not right
                    elif operator == "followed by":
                        result = str(left) + str(right)
                    else:
                        optimized.extend(bytecode[i:i+3])
                        i += 3
                        continue
                    optimized.append({
                        "opcode": "LOAD_CONST",
                        "args": {"value": result},
                        "line_number": instruction.get("line_number"),
                        "source_info": f"constant_folded: {left} {operator} {right} = {result}"
                    })
                    i += 3
                    continue
                except (TypeError, ValueError, ZeroDivisionError):
                    optimized.extend(bytecode[i:i+3])
                    i += 3
                    continue
            optimized.append(instruction)
            i += 1
        return optimized
    
    def _dead_code_elimination(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove unreachable code."""
        # Simple dead code elimination - remove unreachable instructions after RETURN
        optimized_bytecode = []
        found_return = False
        
        for instruction in bytecode:
            if instruction["opcode"] == "RETURN":
                found_return = True
                optimized_bytecode.append(instruction)
            elif not found_return:
                optimized_bytecode.append(instruction)
        
        return optimized_bytecode
    
    def _strength_reduction(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Replace expensive operations with cheaper ones."""
        optimized_bytecode = []
        
        for instruction in bytecode:
            if instruction["opcode"] == "BINARY_OP":
                operator = instruction["args"]["operator"]
                
                # Strength reduction optimizations
                if operator == "multiplied by":
                    # Replace multiplication by 2 with left shift (if integers)
                    pass  # Would need type information
                elif operator == "divided by":
                    # Replace division by 2 with right shift (if integers)
                    pass  # Would need type information
                
            optimized_bytecode.append(instruction)
        
        return optimized_bytecode
    
    def _common_subexpression_elimination(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Eliminate redundant computations."""
        # This would require more sophisticated analysis
        return bytecode
    
    def _loop_optimization(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize loop structures."""
        # This would require loop detection and analysis
        return bytecode
    
    def _function_inlining(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Inline small functions."""
        # This would require function analysis
        return bytecode
    
    def _register_allocation(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize variable allocation."""
        # This would require register allocation analysis
        return bytecode
    
    def _ai_pattern_optimization(self, bytecode: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize AI-specific patterns."""
        optimized_bytecode = []
        
        for instruction in bytecode:
            if instruction["opcode"] in ["AI_THINK", "AI_LEARN", "AI_COMMUNICATE", "AI_TRANSLATE", "AI_ANALYZE"]:
                # Add performance monitoring for AI operations
                optimized_bytecode.append({
                    "opcode": "PROFILE_START",
                    "args": {"operation": instruction["opcode"]},
                    "line_number": instruction.get("line_number"),
                    "source_info": f"ai_profile_start: {instruction['opcode']}"
                })
                optimized_bytecode.append(instruction)
                optimized_bytecode.append({
                    "opcode": "PROFILE_END",
                    "args": {"operation": instruction["opcode"]},
                    "line_number": instruction.get("line_number"),
                    "source_info": f"ai_profile_end: {instruction['opcode']}"
                })
            else:
                optimized_bytecode.append(instruction)
        
        return optimized_bytecode
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get statistics about applied optimizations."""
        return {
            "total_optimizations": len(self.optimization_passes),
            "enabled_optimizations": len([opt for opt in self.optimization_passes if opt.enabled]),
            "optimization_passes": [
                {
                    "name": opt.name,
                    "description": opt.description,
                    "enabled": opt.enabled,
                    "priority": opt.priority
                }
                for opt in self.optimization_passes
            ]
        }
    
    def enable_optimization(self, name: str) -> None:
        """Enable a specific optimization pass."""
        for optimization in self.optimization_passes:
            if optimization.name == name:
                optimization.enabled = True
                break
    
    def disable_optimization(self, name: str) -> None:
        """Disable a specific optimization pass."""
        for optimization in self.optimization_passes:
            if optimization.name == name:
                optimization.enabled = False
                break 