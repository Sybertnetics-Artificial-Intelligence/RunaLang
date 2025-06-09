"""
Bytecode generation and representation for the Runa VM.

This module provides the bytecode generator that translates AST to bytecode,
and the bytecode module representation for serialization and execution.
"""

from typing import List, Dict, Optional, Set, Union, Any, Tuple
from dataclasses import dataclass, field
import struct
import os
import time
from enum import Enum, auto
import json

from ..ast import (
    Node, BinaryOp, UnaryOp, Literal, Identifier, Assignment,
    CallExpr, IfExpr, Block, FunctionDecl, VarDecl, ReturnStmt,
    ForLoop, WhileLoop, MethodCall, PropertyAccess, ListExpr,
    DictionaryExpr, IndexAccess, TryCatchStatement, IfStatement,
    MatchStatement, Pattern, LiteralPattern, VariablePattern, WildcardPattern,
    ListPattern, DictionaryPattern, TypePattern, FunctionExpression,
    Program, Declaration, ImportStatement, ExportStatement
)
from .instructions import Instruction, OpCode


class BytecodeModule:
    """
    Represents a compiled Runa module containing bytecode and metadata.
    
    Attributes:
        name: The name of the module
        instructions: The list of instructions
        constants: The constant pool
        global_names: The names of global variables
        import_names: The names of imported modules
        export_names: The names of exported symbols
        source_map: Mapping from bytecode offsets to source positions
        filename: The source filename
        timestamp: The compilation timestamp
    """
    
    MAGIC_NUMBER = b'RUNA'
    VERSION = 1
    
    def __init__(self, name: str):
        """
        Initialize a new BytecodeModule.
        
        Args:
            name: The name of the module
        """
        self.name = name
        self.instructions: List[Instruction] = []
        self.constants: List[Any] = []
        self.string_pool: List[str] = []
        self.global_names: List[str] = []
        self.import_names: List[str] = []
        self.export_names: List[str] = []
        self.source_map: Dict[int, Tuple[int, int]] = {}  # offset -> (line, column)
        self.filename: str = ""
        self.timestamp: float = time.time()
        
        # Function and type definitions
        self.functions: Dict[str, Tuple[int, int]] = {}  # name -> (start_offset, end_offset)
        self.types: Dict[str, Dict[str, Any]] = {}  # name -> type_definition
    
    def add_instruction(self, instruction: Instruction) -> int:
        """
        Add an instruction to the module.
        
        Args:
            instruction: The instruction to add
            
        Returns:
            The offset of the added instruction
        """
        offset = len(self.instructions)
        self.instructions.append(instruction)
        return offset
    
    def add_constant(self, value: Any) -> int:
        """
        Add a constant to the constant pool.
        
        Args:
            value: The constant value to add
            
        Returns:
            The index of the added constant
        """
        # Check if the constant already exists
        if value in self.constants:
            return self.constants.index(value)
        
        # Add the constant
        index = len(self.constants)
        self.constants.append(value)
        return index
    
    def add_string(self, string: str) -> int:
        """
        Add a string to the string pool.
        
        Args:
            string: The string to add
            
        Returns:
            The index of the added string
        """
        # Check if the string already exists
        if string in self.string_pool:
            return self.string_pool.index(string)
        
        # Add the string
        index = len(self.string_pool)
        self.string_pool.append(string)
        return index
    
    def add_global(self, name: str) -> int:
        """
        Add a global variable to the module.
        
        Args:
            name: The name of the global variable
            
        Returns:
            The index of the added global
        """
        # Check if the global already exists
        if name in self.global_names:
            return self.global_names.index(name)
        
        # Add the global
        index = len(self.global_names)
        self.global_names.append(name)
        return index
    
    def add_import(self, name: str) -> int:
        """
        Add an import to the module.
        
        Args:
            name: The name of the imported module
            
        Returns:
            The index of the added import
        """
        # Check if the import already exists
        if name in self.import_names:
            return self.import_names.index(name)
        
        # Add the import
        index = len(self.import_names)
        self.import_names.append(name)
        return index
    
    def add_export(self, name: str) -> int:
        """
        Add an export to the module.
        
        Args:
            name: The name of the exported symbol
            
        Returns:
            The index of the added export
        """
        # Check if the export already exists
        if name in self.export_names:
            return self.export_names.index(name)
        
        # Add the export
        index = len(self.export_names)
        self.export_names.append(name)
        return index
    
    def add_function(self, name: str, start_offset: int, end_offset: int) -> None:
        """
        Add a function definition to the module.
        
        Args:
            name: The name of the function
            start_offset: The start offset of the function in the bytecode
            end_offset: The end offset of the function in the bytecode
        """
        self.functions[name] = (start_offset, end_offset)
    
    def add_type(self, name: str, type_definition: Dict[str, Any]) -> None:
        """
        Add a type definition to the module.
        
        Args:
            name: The name of the type
            type_definition: The type definition
        """
        self.types[name] = type_definition
    
    def encode(self) -> bytes:
        """
        Encode the module as bytes.
        
        Returns:
            The encoded module
        """
        # Magic number + version
        result = self.MAGIC_NUMBER + struct.pack(">I", self.VERSION)
        
        # Module name
        name_bytes = self.name.encode('utf-8')
        result += struct.pack(">I", len(name_bytes)) + name_bytes
        
        # Timestamp
        result += struct.pack(">d", self.timestamp)
        
        # Filename
        filename_bytes = self.filename.encode('utf-8')
        result += struct.pack(">I", len(filename_bytes)) + filename_bytes
        
        # Constants
        result += struct.pack(">I", len(self.constants))
        for constant in self.constants:
            # Encode constant based on type
            if isinstance(constant, int):
                result += b'i' + struct.pack(">q", constant)
            elif isinstance(constant, float):
                result += b'f' + struct.pack(">d", constant)
            elif isinstance(constant, str):
                string_bytes = constant.encode('utf-8')
                result += b's' + struct.pack(">I", len(string_bytes)) + string_bytes
            elif constant is None:
                result += b'n'
            elif isinstance(constant, bool):
                result += b'b' + struct.pack(">?", constant)
            elif isinstance(constant, list):
                # Encode list as JSON
                json_bytes = json.dumps(constant).encode('utf-8')
                result += b'l' + struct.pack(">I", len(json_bytes)) + json_bytes
            elif isinstance(constant, dict):
                # Encode dictionary as JSON
                json_bytes = json.dumps(constant).encode('utf-8')
                result += b'd' + struct.pack(">I", len(json_bytes)) + json_bytes
            else:
                # Unsupported type
                raise ValueError(f"Unsupported constant type: {type(constant)}")
        
        # String pool
        result += struct.pack(">I", len(self.string_pool))
        for string in self.string_pool:
            string_bytes = string.encode('utf-8')
            result += struct.pack(">I", len(string_bytes)) + string_bytes
        
        # Global names
        result += struct.pack(">I", len(self.global_names))
        for name in self.global_names:
            name_bytes = name.encode('utf-8')
            result += struct.pack(">I", len(name_bytes)) + name_bytes
        
        # Import names
        result += struct.pack(">I", len(self.import_names))
        for name in self.import_names:
            name_bytes = name.encode('utf-8')
            result += struct.pack(">I", len(name_bytes)) + name_bytes
        
        # Export names
        result += struct.pack(">I", len(self.export_names))
        for name in self.export_names:
            name_bytes = name.encode('utf-8')
            result += struct.pack(">I", len(name_bytes)) + name_bytes
        
        # Functions
        result += struct.pack(">I", len(self.functions))
        for name, (start_offset, end_offset) in self.functions.items():
            name_bytes = name.encode('utf-8')
            result += struct.pack(">I", len(name_bytes)) + name_bytes
            result += struct.pack(">II", start_offset, end_offset)
        
        # Types
        result += struct.pack(">I", len(self.types))
        for name, type_definition in self.types.items():
            name_bytes = name.encode('utf-8')
            result += struct.pack(">I", len(name_bytes)) + name_bytes
            type_json = json.dumps(type_definition).encode('utf-8')
            result += struct.pack(">I", len(type_json)) + type_json
        
        # Instructions
        result += struct.pack(">I", len(self.instructions))
        for instruction in self.instructions:
            result += instruction.encode()
        
        # Source map
        result += struct.pack(">I", len(self.source_map))
        for offset, (line, column) in self.source_map.items():
            result += struct.pack(">III", offset, line, column)
        
        return result
    
    @classmethod
    def decode(cls, data: bytes) -> 'BytecodeModule':
        """
        Decode a module from bytes.
        
        Args:
            data: The encoded data
            
        Returns:
            The decoded module
        """
        # Check magic number
        magic = data[:4]
        if magic != cls.MAGIC_NUMBER:
            raise ValueError("Invalid magic number")
        
        # Check version
        version = struct.unpack(">I", data[4:8])[0]
        if version != cls.VERSION:
            raise ValueError(f"Unsupported version: {version}")
        
        offset = 8
        
        # Module name
        name_length = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        name = data[offset:offset+name_length].decode('utf-8')
        offset += name_length
        
        module = cls(name)
        
        # Timestamp
        module.timestamp = struct.unpack(">d", data[offset:offset+8])[0]
        offset += 8
        
        # Filename
        filename_length = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        module.filename = data[offset:offset+filename_length].decode('utf-8')
        offset += filename_length
        
        # Constants
        constant_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(constant_count):
            constant_type = data[offset:offset+1]
            offset += 1
            if constant_type == b'i':
                value = struct.unpack(">q", data[offset:offset+8])[0]
                offset += 8
            elif constant_type == b'f':
                value = struct.unpack(">d", data[offset:offset+8])[0]
                offset += 8
            elif constant_type == b's':
                string_length = struct.unpack(">I", data[offset:offset+4])[0]
                offset += 4
                value = data[offset:offset+string_length].decode('utf-8')
                offset += string_length
            elif constant_type == b'n':
                value = None
            elif constant_type == b'b':
                value = bool(struct.unpack(">?", data[offset:offset+1])[0])
                offset += 1
            elif constant_type == b'l':
                json_length = struct.unpack(">I", data[offset:offset+4])[0]
                offset += 4
                value = json.loads(data[offset:offset+json_length].decode('utf-8'))
                offset += json_length
            elif constant_type == b'd':
                json_length = struct.unpack(">I", data[offset:offset+4])[0]
                offset += 4
                value = json.loads(data[offset:offset+json_length].decode('utf-8'))
                offset += json_length
            else:
                raise ValueError(f"Unsupported constant type: {constant_type}")
            module.constants.append(value)
        
        # String pool
        string_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(string_count):
            string_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            string = data[offset:offset+string_length].decode('utf-8')
            offset += string_length
            module.string_pool.append(string)
        
        # Global names
        global_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(global_count):
            name_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            module.global_names.append(name)
        
        # Import names
        import_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(import_count):
            name_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            module.import_names.append(name)
        
        # Export names
        export_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(export_count):
            name_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            module.export_names.append(name)
        
        # Functions
        function_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(function_count):
            name_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            start_offset, end_offset = struct.unpack(">II", data[offset:offset+8])
            offset += 8
            module.functions[name] = (start_offset, end_offset)
        
        # Types
        type_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(type_count):
            name_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            name = data[offset:offset+name_length].decode('utf-8')
            offset += name_length
            type_json_length = struct.unpack(">I", data[offset:offset+4])[0]
            offset += 4
            type_json = data[offset:offset+type_json_length].decode('utf-8')
            offset += type_json_length
            module.types[name] = json.loads(type_json)
        
        # Instructions
        instruction_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(instruction_count):
            instruction, offset = Instruction.decode(data, offset)
            module.instructions.append(instruction)
        
        # Source map
        source_map_count = struct.unpack(">I", data[offset:offset+4])[0]
        offset += 4
        for _ in range(source_map_count):
            instr_offset, line, column = struct.unpack(">III", data[offset:offset+12])
            offset += 12
            module.source_map[instr_offset] = (line, column)
        
        return module
    
    def save(self, filename: str) -> None:
        """
        Save the module to a file.
        
        Args:
            filename: The filename to save to
        """
        with open(filename, 'wb') as f:
            f.write(self.encode())
    
    @classmethod
    def load(cls, filename: str) -> 'BytecodeModule':
        """
        Load a module from a file.
        
        Args:
            filename: The filename to load from
            
        Returns:
            The loaded module
        """
        with open(filename, 'rb') as f:
            data = f.read()
        return cls.decode(data)
    
    def __str__(self) -> str:
        """Return a string representation of the module."""
        lines = [f"Module: {self.name}"]
        lines.append(f"Filename: {self.filename}")
        lines.append(f"Timestamp: {time.ctime(self.timestamp)}")
        
        lines.append("\nConstants:")
        for i, constant in enumerate(self.constants):
            lines.append(f"  {i}: {constant}")
        
        lines.append("\nString Pool:")
        for i, string in enumerate(self.string_pool):
            lines.append(f"  {i}: {string}")
        
        lines.append("\nGlobals:")
        for i, name in enumerate(self.global_names):
            lines.append(f"  {i}: {name}")
        
        lines.append("\nImports:")
        for i, name in enumerate(self.import_names):
            lines.append(f"  {i}: {name}")
        
        lines.append("\nExports:")
        for i, name in enumerate(self.export_names):
            lines.append(f"  {i}: {name}")
        
        lines.append("\nFunctions:")
        for name, (start, end) in self.functions.items():
            lines.append(f"  {name}: {start}-{end}")
        
        lines.append("\nTypes:")
        for name in self.types:
            lines.append(f"  {name}")
        
        lines.append("\nInstructions:")
        for i, instruction in enumerate(self.instructions):
            line_info = ""
            if i in self.source_map:
                line, column = self.source_map[i]
                line_info = f" (line {line}, col {column})"
            lines.append(f"  {i}: {instruction}{line_info}")
        
        return "\n".join(lines)


class BytecodeGenerator:
    """
    Generates bytecode from AST.
    
    This class converts an AST representation of a Runa program
    into bytecode instructions for the Runa VM.
    
    Attributes:
        module: The bytecode module being generated
    """
    
    def __init__(self, module_name: str, filename: str = ""):
        """
        Initialize a new BytecodeGenerator.
        
        Args:
            module_name: The name of the module
            filename: The source filename
        """
        self.module = BytecodeModule(module_name)
        self.module.filename = filename
        
        # Compilation state
        self.loop_starts: List[int] = []  # Stack of loop start offsets
        self.loop_ends: List[int] = []    # Stack of loop end offsets
        self.break_offsets: List[List[int]] = []  # Stack of lists of break offsets
        self.continue_offsets: List[List[int]] = []  # Stack of lists of continue offsets
        
        # Scope state
        self.locals: List[Dict[str, int]] = [{}]  # Stack of local variable name -> index
        self.local_count = 0  # Total number of local variables
        
        # Function state
        self.current_function: Optional[str] = None
        self.function_starts: Dict[str, int] = {}  # Function name -> start offset
        
        # Constant pool
        self.constants: Dict[Any, int] = {}  # Constant -> index
    
    def generate(self, ast: Node) -> BytecodeModule:
        """
        Generate bytecode from AST.
        
        Args:
            ast: The AST to generate bytecode from
            
        Returns:
            The generated bytecode module
        """
        self._generate_node(ast)
        
        # Add explicit return if not already present
        if not self.module.instructions or self.module.instructions[-1].opcode != OpCode.RET:
            self.module.add_instruction(Instruction(OpCode.PUSH_NULL))
            self.module.add_instruction(Instruction(OpCode.RET))
        
        return self.module
    
    def _generate_node(self, node: Node) -> None:
        """
        Generate bytecode for a node.
        
        Args:
            node: The node to generate bytecode for
        """
        if isinstance(node, Program):
            self._generate_program(node)
        elif isinstance(node, Block):
            self._generate_block(node)
        elif isinstance(node, Declaration):
            self._generate_declaration(node)
        elif isinstance(node, VarDecl):
            self._generate_var_decl(node)
        elif isinstance(node, Assignment):
            self._generate_assignment(node)
        elif isinstance(node, FunctionDecl):
            self._generate_function_decl(node)
        elif isinstance(node, ReturnStmt):
            self._generate_return_stmt(node)
        elif isinstance(node, IfExpr):
            self._generate_if_expr(node)
        elif isinstance(node, IfStatement):
            self._generate_if_statement(node)
        elif isinstance(node, ForLoop):
            self._generate_for_loop(node)
        elif isinstance(node, WhileLoop):
            self._generate_while_loop(node)
        elif isinstance(node, MatchStatement):
            self._generate_match_statement(node)
        elif isinstance(node, ImportStatement):
            self._generate_import_statement(node)
        elif isinstance(node, ExportStatement):
            self._generate_export_statement(node)
        elif isinstance(node, CallExpr):
            self._generate_call_expr(node)
        elif isinstance(node, MethodCall):
            self._generate_method_call(node)
        elif isinstance(node, PropertyAccess):
            self._generate_property_access(node)
        elif isinstance(node, IndexAccess):
            self._generate_index_access(node)
        elif isinstance(node, ListExpr):
            self._generate_list_expr(node)
        elif isinstance(node, DictionaryExpr):
            self._generate_dict_expr(node)
        elif isinstance(node, FunctionExpression):
            self._generate_function_expression(node)
        elif isinstance(node, BinaryOp):
            self._generate_binary_op(node)
        elif isinstance(node, UnaryOp):
            self._generate_unary_op(node)
        elif isinstance(node, Literal):
            self._generate_literal(node)
        elif isinstance(node, Identifier):
            self._generate_identifier(node)
        elif isinstance(node, TryCatchStatement):
            self._generate_try_catch_statement(node)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")
    
    def _generate_literal(self, node: Literal) -> None:
        """
        Generate bytecode for a literal.
        
        Args:
            node: The literal node
        """
        value = node.value
        
        # Handle different literal types
        if value is None:
            self.module.add_instruction(Instruction(OpCode.PUSH_NULL, line=node.line))
        elif value is True:
            self.module.add_instruction(Instruction(OpCode.PUSH_TRUE, line=node.line))
        elif value is False:
            self.module.add_instruction(Instruction(OpCode.PUSH_FALSE, line=node.line))
        elif isinstance(value, int):
            self.module.add_instruction(Instruction(OpCode.PUSH_INT, [value], node.line))
        elif isinstance(value, float):
            self.module.add_instruction(Instruction(OpCode.PUSH_FLOAT, [value], node.line))
        elif isinstance(value, str):
            self.module.add_instruction(Instruction(OpCode.PUSH_STRING, [value], node.line))
        else:
            # Add to constant pool
            const_idx = self.module.add_constant(value)
            self.module.add_instruction(Instruction(OpCode.LOAD_CONST, [const_idx], node.line))
    
    def _generate_binary_op(self, node: BinaryOp) -> None:
        """
        Generate bytecode for a binary operation.
        
        Args:
            node: The binary operation node
        """
        # Special handling for short-circuit logical operators
        if node.op == "&&":
            self._generate_logical_and(node)
            return
        elif node.op == "||":
            self._generate_logical_or(node)
            return
        
        # For non-short-circuit operators, evaluate both operands
        node.left.accept(self)
        node.right.accept(self)
        
        # Generate the appropriate instruction for the operator
        if node.op == "+":
            self.module.add_instruction(Instruction(OpCode.ADD, line=node.line))
        elif node.op == "-":
            self.module.add_instruction(Instruction(OpCode.SUB, line=node.line))
        elif node.op == "*":
            self.module.add_instruction(Instruction(OpCode.MUL, line=node.line))
        elif node.op == "/":
            self.module.add_instruction(Instruction(OpCode.DIV, line=node.line))
        elif node.op == "%":
            self.module.add_instruction(Instruction(OpCode.MOD, line=node.line))
        elif node.op == "**":
            self.module.add_instruction(Instruction(OpCode.POW, line=node.line))
        elif node.op == "==":
            self.module.add_instruction(Instruction(OpCode.EQ, line=node.line))
        elif node.op == "!=":
            self.module.add_instruction(Instruction(OpCode.NE, line=node.line))
        elif node.op == "<":
            self.module.add_instruction(Instruction(OpCode.LT, line=node.line))
        elif node.op == "<=":
            self.module.add_instruction(Instruction(OpCode.LE, line=node.line))
        elif node.op == ">":
            self.module.add_instruction(Instruction(OpCode.GT, line=node.line))
        elif node.op == ">=":
            self.module.add_instruction(Instruction(OpCode.GE, line=node.line))
        elif node.op == "is":
            self.module.add_instruction(Instruction(OpCode.IS, line=node.line))
        else:
            raise ValueError(f"Unsupported binary operator: {node.op}")
    
    def _generate_logical_and(self, node: BinaryOp) -> None:
        """
        Generate bytecode for a logical AND operation with short-circuit evaluation.
        
        Args:
            node: The binary operation node
        """
        # Create a label for short-circuit evaluation
        end_label = self.create_label()
        
        # Evaluate the left operand
        node.left.accept(self)
        
        # Duplicate the left result for the final result if short-circuited
        self.emit(OpCode.DUP)
        
        # If the left operand is false, skip the right operand evaluation
        self.emit(OpCode.JZ, [0])  # Placeholder for end_label
        
        # Pop the duplicate of the left operand if we're evaluating the right
        self.emit(OpCode.POP)
        
        # Evaluate the right operand
        node.right.accept(self)
        
        # Define the end label
        self.define_label(end_label)
    
    def _generate_logical_or(self, node: BinaryOp) -> None:
        """
        Generate bytecode for a logical OR operation with short-circuit evaluation.
        
        Args:
            node: The binary operation node
        """
        # Create a label for short-circuit evaluation
        end_label = self.create_label()
        
        # Evaluate the left operand
        node.left.accept(self)
        
        # Duplicate the left result for the final result if short-circuited
        self.emit(OpCode.DUP)
        
        # If the left operand is true, skip the right operand evaluation
        self.emit(OpCode.JNZ, [0])  # Placeholder for end_label
        
        # Pop the duplicate of the left operand if we're evaluating the right
        self.emit(OpCode.POP)
        
        # Evaluate the right operand
        node.right.accept(self)
        
        # Define the end label
        self.define_label(end_label)
    
    def _generate_try_catch_statement(self, node: TryCatchStatement) -> None:
        """
        Generate bytecode for a try-catch statement.
        
        Args:
            node: The try-catch statement node
        """
        # Create labels for the try, catch, and end blocks
        try_start_label = self.create_label()
        catch_start_label = self.create_label()
        end_label = self.create_label()
        
        # Generate TRY_BEGIN instruction with placeholder for catch block address
        try_begin_idx = len(self.module.instructions)
        self.emit(OpCode.TRY_BEGIN, [0])  # Placeholder for catch_start_label
        
        # Mark the start of the try block
        self.define_label(try_start_label)
        
        # Generate code for the try block
        node.try_block.accept(self)
        
        # Generate TRY_END instruction with placeholder for end of catch block
        try_end_idx = len(self.module.instructions)
        self.emit(OpCode.TRY_END, [0])  # Placeholder for end_label
        
        # Jump to the end of the catch block
        self.emit(OpCode.JMP, [0])  # Placeholder for end_label
        
        # Mark the start of the catch block
        self.define_label(catch_start_label)
        
        # Generate CATCH_BEGIN instruction
        self.emit(OpCode.CATCH_BEGIN)
        
        # Store the error in the error variable
        error_idx = self._get_or_declare_local(node.error_variable)
        self.emit(OpCode.STORE_LOCAL, [error_idx])
        
        # Generate code for the catch block
        node.catch_block.accept(self)
        
        # Generate CATCH_END instruction
        self.emit(OpCode.CATCH_END)
        
        # Mark the end of the catch block
        self.define_label(end_label)
        
        # Update the TRY_BEGIN instruction with the catch block address
        try_begin_instr = self.module.instructions[try_begin_idx]
        try_begin_instr.operands[0] = self.get_label_offset(catch_start_label)
        
        # Update the TRY_END instruction with the end of catch block address
        try_end_instr = self.module.instructions[try_end_idx]
        try_end_instr.operands[0] = self.get_label_offset(end_label)
        
        # Update the JMP instruction after TRY_END
        jmp_instr = self.module.instructions[try_end_idx + 1]
        jmp_instr.operands[0] = self.get_label_offset(end_label)

    def _generate_import_statement(self, node: ImportStatement) -> None:
        """
        Generate bytecode for an import statement.
        
        Args:
            node: The import statement node
        """
        # Push the module name onto the stack
        self.emit(OpCode.PUSH_STRING, [node.module])
        
        # Create a list of items to import, or empty list for importing everything
        if node.items:
            # Build a list of item names
            for item in node.items:
                self.emit(OpCode.PUSH_STRING, [item])
            self.emit(OpCode.BUILD_LIST, [len(node.items)])
            
            # Call import_from function
            self.emit(OpCode.LOAD_GLOBAL, [self.module.add_global("runa.module.import_from")])
            self.emit(OpCode.SWAP)  # Swap module and items
            self.emit(OpCode.SWAP)  # Swap function and module
            self.emit(OpCode.CALL, [2])  # Call with 2 arguments
        else:
            # Call import_module function
            self.emit(OpCode.LOAD_GLOBAL, [self.module.add_global("runa.module.import_module")])
            self.emit(OpCode.SWAP)  # Swap function and module
            self.emit(OpCode.CALL, [1])  # Call with 1 argument
        
        # Store the result in the module's namespace
        if not node.items:
            # If importing the whole module, store it in a variable with the module name
            module_parts = node.module.split('.')
            module_name = module_parts[-1]
            module_idx = self._get_or_declare_local(module_name)
            self.emit(OpCode.STORE_LOCAL, [module_idx])
        else:
            # If importing specific items, store each item in a variable
            for item in node.items:
                # Get the value from the imported dict
                self.emit(OpCode.DUP)
                self.emit(OpCode.PUSH_STRING, [item])
                self.emit(OpCode.DICT_GET)
                
                # Store in a local variable
                item_idx = self._get_or_declare_local(item)
                self.emit(OpCode.STORE_LOCAL, [item_idx])
            
            # Pop the imported dict
            self.emit(OpCode.POP)

    def _generate_export_statement(self, node: ExportStatement) -> None:
        """
        Generate bytecode for an export statement.
        
        Args:
            node: The export statement node
        """
        # Create a dictionary to hold the exports
        self.emit(OpCode.BUILD_DICT, [0])
        
        # Add each exported item to the dictionary
        for item_name in node.items:
            # Load the variable value
            var_idx = self._get_local(item_name)
            self.emit(OpCode.LOAD_LOCAL, [var_idx])
            
            # Add to the exports dictionary
            self.emit(OpCode.DUP_X1)  # Duplicate dict below value
            self.emit(OpCode.PUSH_STRING, [item_name])  # Push key
            self.emit(OpCode.SWAP)  # Swap key and value
            self.emit(OpCode.DICT_SET)  # Set key/value in dict
        
        # Register the exports with the module system
        self.emit(OpCode.LOAD_GLOBAL, [self.module.add_global("runa.module.register_exports")])
        self.emit(OpCode.SWAP)  # Swap function and exports dict
        self.emit(OpCode.CALL, [1])  # Call with 1 argument
        
        # Pop the result of register_exports
        self.emit(OpCode.POP)
        
        # Record exports in the module metadata
        for item_name in node.items:
            self.module.add_export(item_name)

    def _generate_function_expression(self, node: FunctionExpression) -> None:
        """
        Generate bytecode for a function expression (closure).
        
        Args:
            node: The function expression node
        """
        # Create a unique name for the anonymous function
        func_name = f"_lambda_{self.get_next_lambda_id()}"
        
        # Save the current locals
        old_locals = self.locals.copy()
        
        # Create a new locals scope for the function
        self.locals.append({})
        
        # Add parameters to the locals
        for i, param in enumerate(node.parameters):
            self.locals[-1][param.name] = self.local_count
            self.local_count += 1
        
        # Record function start
        func_start = len(self.module.instructions)
        self.function_starts[func_name] = func_start
        
        # Create a closure environment for captured variables
        closure_env = []
        
        # Capture variables from outer scopes
        for var_name in node.captured_variables:
            # Find the variable in the outer scopes
            for scope in reversed(old_locals):
                if var_name in scope:
                    closure_env.append((var_name, scope[var_name]))
                    break
        
        # Generate code for the function body
        node.body.accept(self)
        
        # If the function doesn't end with a return, add an implicit return null
        if not (node.body.statements and isinstance(node.body.statements[-1], ReturnStmt)):
            self.emit(OpCode.PUSH_NULL)
            self.emit(OpCode.RET)
        
        # Create a closure object
        self.emit(OpCode.CREATE_CLOSURE, [func_name, len(closure_env)])
        
        # Add captured variables to the closure
        for var_name, var_idx in closure_env:
            self.emit(OpCode.CAPTURE_VAR, [var_idx])
        
        # Restore the old locals
        self.locals = old_locals

    def get_next_lambda_id(self) -> int:
        """
        Get the next unique ID for a lambda function.
        
        Returns:
            The next lambda ID
        """
        if not hasattr(self, '_lambda_counter'):
            self._lambda_counter = 0
        
        lambda_id = self._lambda_counter
        self._lambda_counter += 1
        
        return lambda_id

    # The remaining node type generators would be implemented here 