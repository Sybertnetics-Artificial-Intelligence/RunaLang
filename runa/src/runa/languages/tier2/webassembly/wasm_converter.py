#!/usr/bin/env python3
"""
WebAssembly ↔ Runa Bidirectional Converter

Converts between WebAssembly AST and Runa AST in both directions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from .wasm_ast import *
from ....core.runa_ast import *


class WasmToRunaConverter:
    """Converts WebAssembly AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'i32': 'Integer',
            'i64': 'Integer',
            'f32': 'Float',
            'f64': 'Float',
            'v128': 'Vector',
            'funcref': 'FunctionReference',
            'externref': 'ExternalReference',
        }
        
        self.opcode_mapping = {
            # Arithmetic
            'i32.add': 'plus',
            'i32.sub': 'minus',
            'i32.mul': 'times',
            'i32.div_s': 'divided by',
            'i32.div_u': 'divided by',
            'i64.add': 'plus',
            'i64.sub': 'minus',
            'i64.mul': 'times',
            'i64.div_s': 'divided by',
            'i64.div_u': 'divided by',
            'f32.add': 'plus',
            'f32.sub': 'minus',
            'f32.mul': 'times',
            'f32.div': 'divided by',
            'f64.add': 'plus',
            'f64.sub': 'minus',
            'f64.mul': 'times',
            'f64.div': 'divided by',
            
            # Comparison
            'i32.eq': 'is equal to',
            'i32.ne': 'is not equal to',
            'i32.lt_s': 'is less than',
            'i32.lt_u': 'is less than',
            'i32.gt_s': 'is greater than',
            'i32.gt_u': 'is greater than',
            'i32.le_s': 'is less than or equal to',
            'i32.le_u': 'is less than or equal to',
            'i32.ge_s': 'is greater than or equal to',
            'i32.ge_u': 'is greater than or equal to',
            
            # Logical
            'i32.and': 'and',
            'i32.or': 'or',
            'i32.xor': 'xor',
            
            # Constants
            'i32.const': 'constant',
            'i64.const': 'constant',
            'f32.const': 'constant',
            'f64.const': 'constant',
        }
    
    def convert(self, wasm_node: WasmNode) -> ASTNode:
        """Convert WebAssembly AST node to Runa AST node."""
        try:
            if isinstance(wasm_node, WasmModule):
                return self._convert_module(wasm_node)
            elif isinstance(wasm_node, WasmFunction):
                return self._convert_function(wasm_node)
            elif isinstance(wasm_node, WasmType):
                return self._convert_type(wasm_node)
            elif isinstance(wasm_node, WasmInstruction):
                return self._convert_instruction(wasm_node)
            elif isinstance(wasm_node, WasmGlobal):
                return self._convert_global(wasm_node)
            elif isinstance(wasm_node, WasmImport):
                return self._convert_import(wasm_node)
            elif isinstance(wasm_node, WasmExport):
                return self._convert_export(wasm_node)
            elif isinstance(wasm_node, WasmTable):
                return self._convert_table(wasm_node)
            elif isinstance(wasm_node, WasmMemory):
                return self._convert_memory(wasm_node)
            elif isinstance(wasm_node, WasmData):
                return self._convert_data(wasm_node)
            elif isinstance(wasm_node, WasmElement):
                return self._convert_element(wasm_node)
            else:
                return self._create_placeholder(wasm_node)
        except Exception as e:
            self.logger.error(f"WebAssembly to Runa conversion failed: {e}")
            return self._create_placeholder(wasm_node)
    
    def _convert_module(self, module: WasmModule) -> Program:
        """Convert WebAssembly module to Runa program."""
        statements = []
        
        # Convert functions
        for func in module.functions:
            statements.append(self._convert_function(func))
        
        # Convert globals
        for global_var in module.globals:
            statements.append(self._convert_global(global_var))
        
        # Convert imports (as external declarations)
        for import_decl in module.imports:
            statements.append(self._convert_import(import_decl))
        
        # Convert exports (as export statements)
        for export in module.exports:
            statements.append(self._convert_export(export))
        
        return Program(statements=statements)
    
    def _convert_function(self, func: WasmFunction) -> FunctionDeclaration:
        """Convert WebAssembly function to Runa function."""
        # Create function name
        name = func.name or f"function_{func.type_index}"
        
        # Convert parameters (simplified)
        parameters = []
        for i, local_type in enumerate(func.locals):
            param_name = f"param_{i}"
            param_type = self._convert_value_type(local_type)
            parameters.append(Parameter(name=param_name, type_annotation=param_type))
        
        # Convert body
        body_statements = []
        for instruction in func.body:
            stmt = self._convert_instruction(instruction)
            if stmt:
                body_statements.append(stmt)
        
        body = Block(statements=body_statements)
        
        return FunctionDeclaration(
            name=name,
            parameters=parameters,
            body=body,
            return_type=TypeAnnotation("Any")  # Simplified
        )
    
    def _convert_instruction(self, instruction: WasmInstruction) -> Optional[ASTNode]:
        """Convert WebAssembly instruction to Runa statement/expression."""
        opcode_str = instruction.opcode.value
        
        # Handle constants
        if opcode_str.endswith('.const'):
            if len(instruction.args) > 0:
                value = instruction.args[0]
                if opcode_str.startswith('i32') or opcode_str.startswith('i64'):
                    return IntegerLiteral(value=int(value))
                elif opcode_str.startswith('f32') or opcode_str.startswith('f64'):
                    return FloatLiteral(value=float(value))
        
        # Handle arithmetic operations
        if opcode_str in self.opcode_mapping:
            operator = self.opcode_mapping[opcode_str]
            # This would need stack-based evaluation context
            # For now, create a placeholder
            return ExpressionStatement(
                expression=Identifier(name=f"wasm_{opcode_str}")
            )
        
        # Handle control flow
        if opcode_str == 'if':
            # Would need to parse the if structure
            return IfStatement(
                condition=Identifier(name="condition"),
                then_block=Block(statements=[]),
                else_block=None
            )
        elif opcode_str == 'loop':
            return WhileStatement(
                condition=BooleanLiteral(value=True),
                body=Block(statements=[])
            )
        elif opcode_str == 'return':
            return ReturnStatement(value=None)
        
        # Handle function calls
        if opcode_str == 'call':
            if len(instruction.args) > 0:
                func_index = instruction.args[0]
                return ExpressionStatement(
                    expression=FunctionCall(
                        function=Identifier(name=f"function_{func_index}"),
                        arguments=[]
                    )
                )
        
        # Handle local variables
        if opcode_str == 'local.get':
            if len(instruction.args) > 0:
                local_index = instruction.args[0]
                return ExpressionStatement(
                    expression=Identifier(name=f"local_{local_index}")
                )
        elif opcode_str == 'local.set':
            if len(instruction.args) > 0:
                local_index = instruction.args[0]
                return AssignmentStatement(
                    target=Identifier(name=f"local_{local_index}"),
                    value=Identifier(name="value")  # Simplified
                )
        
        # Handle global variables
        if opcode_str == 'global.get':
            if len(instruction.args) > 0:
                global_index = instruction.args[0]
                return ExpressionStatement(
                    expression=Identifier(name=f"global_{global_index}")
                )
        elif opcode_str == 'global.set':
            if len(instruction.args) > 0:
                global_index = instruction.args[0]
                return AssignmentStatement(
                    target=Identifier(name=f"global_{global_index}"),
                    value=Identifier(name="value")  # Simplified
                )
        
        # Default: create placeholder
        return ExpressionStatement(
            expression=Identifier(name=f"wasm_{opcode_str}")
        )
    
    def _convert_global(self, global_var: WasmGlobal) -> VariableDeclaration:
        """Convert WebAssembly global to Runa variable."""
        name = f"global_var"
        type_annotation = self._convert_value_type(global_var.value_type)
        
        # Handle initial value
        initial_value = None
        if global_var.init:
            # Simplified - just use first instruction
            first_init = global_var.init[0]
            if first_init.opcode.value.endswith('.const') and first_init.args:
                value = first_init.args[0]
                if first_init.opcode.value.startswith('i32') or first_init.opcode.value.startswith('i64'):
                    initial_value = IntegerLiteral(value=int(value))
                elif first_init.opcode.value.startswith('f32') or first_init.opcode.value.startswith('f64'):
                    initial_value = FloatLiteral(value=float(value))
        
        is_mutable = global_var.mutability == WasmMutability.VAR
        
        return VariableDeclaration(
            name=name,
            type_annotation=type_annotation,
            initial_value=initial_value,
            is_mutable=is_mutable
        )
    
    def _convert_import(self, import_decl: WasmImport) -> ImportStatement:
        """Convert WebAssembly import to Runa import."""
        module_name = import_decl.module
        import_name = import_decl.name
        
        return ImportStatement(
            module=module_name,
            imported_names=[import_name]
        )
    
    def _convert_export(self, export: WasmExport) -> ExpressionStatement:
        """Convert WebAssembly export to Runa export-like statement."""
        # Runa doesn't have explicit exports, so create a placeholder
        return ExpressionStatement(
            expression=Identifier(name=f"export_{export.name}")
        )
    
    def _convert_table(self, table: WasmTable) -> VariableDeclaration:
        """Convert WebAssembly table to Runa variable."""
        return VariableDeclaration(
            name="table",
            type_annotation=TypeAnnotation("Table"),
            initial_value=None
        )
    
    def _convert_memory(self, memory: WasmMemory) -> VariableDeclaration:
        """Convert WebAssembly memory to Runa variable."""
        return VariableDeclaration(
            name="memory",
            type_annotation=TypeAnnotation("Memory"),
            initial_value=None
        )
    
    def _convert_data(self, data: WasmData) -> VariableDeclaration:
        """Convert WebAssembly data segment to Runa variable."""
        return VariableDeclaration(
            name="data_segment",
            type_annotation=TypeAnnotation("Bytes"),
            initial_value=StringLiteral(value=data.data.decode('utf-8', errors='ignore'))
        )
    
    def _convert_element(self, element: WasmElement) -> VariableDeclaration:
        """Convert WebAssembly element segment to Runa variable."""
        return VariableDeclaration(
            name="element_segment",
            type_annotation=TypeAnnotation("List"),
            initial_value=None
        )
    
    def _convert_type(self, wasm_type: WasmType) -> TypeAnnotation:
        """Convert WebAssembly type to Runa type."""
        # For function types, create a function type annotation
        if wasm_type.parameters or wasm_type.results:
            return TypeAnnotation("Function")
        
        return TypeAnnotation("Any")
    
    def _convert_value_type(self, value_type: WasmValueType) -> TypeAnnotation:
        """Convert WebAssembly value type to Runa type."""
        runa_type = self.type_mapping.get(value_type.value, "Any")
        return TypeAnnotation(runa_type)
    
    def _create_placeholder(self, node: WasmNode) -> ASTNode:
        """Create placeholder for unsupported nodes."""
        return ExpressionStatement(
            expression=Identifier(name=f"wasm_{node.__class__.__name__}")
        )


class RunaToWasmConverter:
    """Converts Runa AST to WebAssembly AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'Integer': WasmValueType.I32,
            'Float': WasmValueType.F32,
            'Boolean': WasmValueType.I32,  # WebAssembly uses i32 for booleans
            'String': WasmValueType.I32,   # String as pointer
            'Any': WasmValueType.I32,
        }
        
        self.operator_mapping = {
            'plus': 'i32.add',
            'minus': 'i32.sub',
            'times': 'i32.mul',
            'divided by': 'i32.div_s',
            'is equal to': 'i32.eq',
            'is not equal to': 'i32.ne',
            'is less than': 'i32.lt_s',
            'is greater than': 'i32.gt_s',
            'is less than or equal to': 'i32.le_s',
            'is greater than or equal to': 'i32.ge_s',
            'and': 'i32.and',
            'or': 'i32.or',
        }
    
    def convert(self, runa_node: ASTNode) -> WasmNode:
        """Convert Runa AST node to WebAssembly AST node."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, FunctionDeclaration):
                return self._convert_function_declaration(runa_node)
            elif isinstance(runa_node, VariableDeclaration):
                return self._convert_variable_declaration(runa_node)
            elif isinstance(runa_node, IfStatement):
                return self._convert_if_statement(runa_node)
            elif isinstance(runa_node, WhileStatement):
                return self._convert_while_statement(runa_node)
            elif isinstance(runa_node, ReturnStatement):
                return self._convert_return_statement(runa_node)
            elif isinstance(runa_node, ExpressionStatement):
                return self._convert_expression_statement(runa_node)
            elif isinstance(runa_node, BinaryOperation):
                return self._convert_binary_operation(runa_node)
            elif isinstance(runa_node, FunctionCall):
                return self._convert_function_call(runa_node)
            elif isinstance(runa_node, IntegerLiteral):
                return self._convert_integer_literal(runa_node)
            elif isinstance(runa_node, FloatLiteral):
                return self._convert_float_literal(runa_node)
            elif isinstance(runa_node, BooleanLiteral):
                return self._convert_boolean_literal(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return self._convert_string_literal(runa_node)
            elif isinstance(runa_node, Identifier):
                return self._convert_identifier(runa_node)
            else:
                return self._create_placeholder(runa_node)
        except Exception as e:
            self.logger.error(f"Runa to WebAssembly conversion failed: {e}")
            return self._create_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> WasmModule:
        """Convert Runa program to WebAssembly module."""
        module = WasmModule()
        
        # Create basic function type for void -> void
        void_type = WasmType(parameters=[], results=[])
        module.types.append(void_type)
        
        # Convert statements
        for stmt in program.statements:
            if isinstance(stmt, FunctionDeclaration):
                wasm_func = self._convert_function_declaration(stmt)
                module.functions.append(wasm_func)
            elif isinstance(stmt, VariableDeclaration):
                wasm_global = self._convert_variable_declaration(stmt)
                if isinstance(wasm_global, WasmGlobal):
                    module.globals.append(wasm_global)
        
        # Add basic memory
        module.memories.append(WasmMemory(limits=WasmLimits(min=1)))
        
        return module
    
    def _convert_function_declaration(self, func: FunctionDeclaration) -> WasmFunction:
        """Convert Runa function to WebAssembly function."""
        # Create function type
        param_types = []
        for param in func.parameters:
            if param.type_annotation:
                wasm_type = self._convert_type_annotation(param.type_annotation)
                param_types.append(wasm_type)
            else:
                param_types.append(WasmValueType.I32)
        
        result_types = []
        if func.return_type:
            result_type = self._convert_type_annotation(func.return_type)
            result_types.append(result_type)
        
        # Convert body
        body_instructions = []
        if func.body:
            for stmt in func.body.statements:
                instructions = self._convert_statement_to_instructions(stmt)
                body_instructions.extend(instructions)
        
        return WasmFunction(
            type_index=0,  # Simplified
            locals=[],
            body=body_instructions
        )
    
    def _convert_variable_declaration(self, var_decl: VariableDeclaration) -> WasmGlobal:
        """Convert Runa variable to WebAssembly global."""
        value_type = WasmValueType.I32
        if var_decl.type_annotation:
            value_type = self._convert_type_annotation(var_decl.type_annotation)
        
        mutability = WasmMutability.VAR if var_decl.is_mutable else WasmMutability.CONST
        
        # Convert initial value
        init_instructions = []
        if var_decl.initial_value:
            init_instructions = self._convert_expression_to_instructions(var_decl.initial_value)
        else:
            # Default initialization
            if value_type == WasmValueType.I32:
                init_instructions = [WasmInstruction(opcode=WasmOpcode.I32_CONST, args=[0])]
            elif value_type == WasmValueType.F32:
                init_instructions = [WasmInstruction(opcode=WasmOpcode.F32_CONST, args=[0.0])]
            elif value_type == WasmValueType.F64:
                init_instructions = [WasmInstruction(opcode=WasmOpcode.F64_CONST, args=[0.0])]
            else:
                init_instructions = [WasmInstruction(opcode=WasmOpcode.I32_CONST, args=[0])]
        
        return WasmGlobal(
            value_type=value_type,
            mutability=mutability,
            init=init_instructions
        )
    
    def _convert_if_statement(self, if_stmt: IfStatement) -> WasmIf:
        """Convert Runa if statement to WebAssembly if."""
        # Convert condition
        condition_instructions = self._convert_expression_to_instructions(if_stmt.condition)
        
        # Convert then block
        then_instructions = []
        if if_stmt.then_block:
            for stmt in if_stmt.then_block.statements:
                then_instructions.extend(self._convert_statement_to_instructions(stmt))
        
        # Convert else block
        else_instructions = []
        if if_stmt.else_block:
            for stmt in if_stmt.else_block.statements:
                else_instructions.extend(self._convert_statement_to_instructions(stmt))
        
        return WasmIf(
            then_instructions=then_instructions,
            else_instructions=else_instructions
        )
    
    def _convert_while_statement(self, while_stmt: WhileStatement) -> WasmLoop:
        """Convert Runa while statement to WebAssembly loop."""
        # Convert condition
        condition_instructions = self._convert_expression_to_instructions(while_stmt.condition)
        
        # Convert body
        body_instructions = []
        if while_stmt.body:
            for stmt in while_stmt.body.statements:
                body_instructions.extend(self._convert_statement_to_instructions(stmt))
        
        # Create loop with branch
        loop_instructions = condition_instructions + body_instructions
        loop_instructions.append(WasmInstruction(opcode=WasmOpcode.BR, args=[0]))
        
        return WasmLoop(instructions=loop_instructions)
    
    def _convert_return_statement(self, return_stmt: ReturnStatement) -> WasmInstruction:
        """Convert Runa return statement to WebAssembly return."""
        return WasmInstruction(opcode=WasmOpcode.RETURN)
    
    def _convert_expression_statement(self, expr_stmt: ExpressionStatement) -> List[WasmInstruction]:
        """Convert Runa expression statement to WebAssembly instructions."""
        return self._convert_expression_to_instructions(expr_stmt.expression)
    
    def _convert_binary_operation(self, binary_op: BinaryOperation) -> List[WasmInstruction]:
        """Convert Runa binary operation to WebAssembly instructions."""
        instructions = []
        
        # Generate left operand
        instructions.extend(self._convert_expression_to_instructions(binary_op.left))
        
        # Generate right operand
        instructions.extend(self._convert_expression_to_instructions(binary_op.right))
        
        # Generate operation
        wasm_op = self.operator_mapping.get(binary_op.operator, 'i32.add')
        try:
            opcode = WasmOpcode(wasm_op)
            instructions.append(WasmInstruction(opcode=opcode))
        except ValueError:
            # Unknown operation, use add as default
            instructions.append(WasmInstruction(opcode=WasmOpcode.I32_ADD))
        
        return instructions
    
    def _convert_function_call(self, func_call: FunctionCall) -> List[WasmInstruction]:
        """Convert Runa function call to WebAssembly call."""
        instructions = []
        
        # Generate arguments
        for arg in func_call.arguments:
            instructions.extend(self._convert_expression_to_instructions(arg))
        
        # Generate call
        # For now, assume function index 0
        instructions.append(WasmInstruction(opcode=WasmOpcode.CALL, args=[0]))
        
        return instructions
    
    def _convert_integer_literal(self, int_lit: IntegerLiteral) -> List[WasmInstruction]:
        """Convert Runa integer literal to WebAssembly const."""
        return [WasmInstruction(opcode=WasmOpcode.I32_CONST, args=[int_lit.value])]
    
    def _convert_float_literal(self, float_lit: FloatLiteral) -> List[WasmInstruction]:
        """Convert Runa float literal to WebAssembly const."""
        return [WasmInstruction(opcode=WasmOpcode.F32_CONST, args=[float_lit.value])]
    
    def _convert_boolean_literal(self, bool_lit: BooleanLiteral) -> List[WasmInstruction]:
        """Convert Runa boolean literal to WebAssembly const."""
        value = 1 if bool_lit.value else 0
        return [WasmInstruction(opcode=WasmOpcode.I32_CONST, args=[value])]
    
    def _convert_string_literal(self, str_lit: StringLiteral) -> List[WasmInstruction]:
        """Convert Runa string literal to WebAssembly const."""
        # Simplified: return pointer to string data
        return [WasmInstruction(opcode=WasmOpcode.I32_CONST, args=[0])]
    
    def _convert_identifier(self, identifier: Identifier) -> List[WasmInstruction]:
        """Convert Runa identifier to WebAssembly get instruction."""
        # Simplified: assume it's a local variable
        return [WasmInstruction(opcode=WasmOpcode.LOCAL_GET, args=[0])]
    
    def _convert_type_annotation(self, type_ann: TypeAnnotation) -> WasmValueType:
        """Convert Runa type annotation to WebAssembly value type."""
        return self.type_mapping.get(type_ann.name, WasmValueType.I32)
    
    def _convert_statement_to_instructions(self, stmt: ASTNode) -> List[WasmInstruction]:
        """Convert Runa statement to WebAssembly instructions."""
        if isinstance(stmt, ExpressionStatement):
            return self._convert_expression_to_instructions(stmt.expression)
        elif isinstance(stmt, ReturnStatement):
            return [self._convert_return_statement(stmt)]
        elif isinstance(stmt, VariableDeclaration):
            # Variable declarations become global sets
            return [WasmInstruction(opcode=WasmOpcode.GLOBAL_SET, args=[0])]
        else:
            return []
    
    def _convert_expression_to_instructions(self, expr: ASTNode) -> List[WasmInstruction]:
        """Convert Runa expression to WebAssembly instructions."""
        if isinstance(expr, IntegerLiteral):
            return self._convert_integer_literal(expr)
        elif isinstance(expr, FloatLiteral):
            return self._convert_float_literal(expr)
        elif isinstance(expr, BooleanLiteral):
            return self._convert_boolean_literal(expr)
        elif isinstance(expr, StringLiteral):
            return self._convert_string_literal(expr)
        elif isinstance(expr, Identifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, BinaryOperation):
            return self._convert_binary_operation(expr)
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call(expr)
        else:
            return []
    
    def _create_placeholder(self, node: ASTNode) -> WasmInstruction:
        """Create placeholder for unsupported nodes."""
        return WasmInstruction(opcode=WasmOpcode.NOP)


# Convenience functions
def wasm_to_runa(wasm_ast: WasmModule) -> Program:
    """Convert WebAssembly AST to Runa AST."""
    converter = WasmToRunaConverter()
    return converter.convert(wasm_ast)


def runa_to_wasm(runa_ast: Program) -> WasmModule:
    """Convert Runa AST to WebAssembly AST."""
    converter = RunaToWasmConverter()
    return converter.convert(runa_ast)