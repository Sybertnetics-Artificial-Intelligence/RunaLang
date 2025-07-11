#!/usr/bin/env python3
"""
WebAssembly AST Node Definitions

Complete WebAssembly Abstract Syntax Tree node definitions for the Runa
universal translation system. Supports WebAssembly MVP and extensions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class WasmValueType(Enum):
    """WebAssembly value types."""
    I32 = "i32"
    I64 = "i64"
    F32 = "f32"
    F64 = "f64"
    V128 = "v128"
    FUNCREF = "funcref"
    EXTERNREF = "externref"


class WasmMutability(Enum):
    """WebAssembly mutability types."""
    CONST = "const"
    VAR = "var"


class WasmOpcode(Enum):
    """WebAssembly instruction opcodes."""
    # Control flow
    UNREACHABLE = "unreachable"
    NOP = "nop"
    BLOCK = "block"
    LOOP = "loop"
    IF = "if"
    ELSE = "else"
    END = "end"
    BR = "br"
    BR_IF = "br_if"
    BR_TABLE = "br_table"
    RETURN = "return"
    CALL = "call"
    CALL_INDIRECT = "call_indirect"
    
    # Parametric
    DROP = "drop"
    SELECT = "select"
    SELECT_T = "select_t"
    
    # Variable
    LOCAL_GET = "local.get"
    LOCAL_SET = "local.set"
    LOCAL_TEE = "local.tee"
    GLOBAL_GET = "global.get"
    GLOBAL_SET = "global.set"
    
    # Table
    TABLE_GET = "table.get"
    TABLE_SET = "table.set"
    TABLE_INIT = "table.init"
    ELEM_DROP = "elem.drop"
    TABLE_COPY = "table.copy"
    TABLE_GROW = "table.grow"
    TABLE_SIZE = "table.size"
    TABLE_FILL = "table.fill"
    
    # Memory
    I32_LOAD = "i32.load"
    I64_LOAD = "i64.load"
    F32_LOAD = "f32.load"
    F64_LOAD = "f64.load"
    I32_LOAD8_S = "i32.load8_s"
    I32_LOAD8_U = "i32.load8_u"
    I32_LOAD16_S = "i32.load16_s"
    I32_LOAD16_U = "i32.load16_u"
    I64_LOAD8_S = "i64.load8_s"
    I64_LOAD8_U = "i64.load8_u"
    I64_LOAD16_S = "i64.load16_s"
    I64_LOAD16_U = "i64.load16_u"
    I64_LOAD32_S = "i64.load32_s"
    I64_LOAD32_U = "i64.load32_u"
    I32_STORE = "i32.store"
    I64_STORE = "i64.store"
    F32_STORE = "f32.store"
    F64_STORE = "f64.store"
    I32_STORE8 = "i32.store8"
    I32_STORE16 = "i32.store16"
    I64_STORE8 = "i64.store8"
    I64_STORE16 = "i64.store16"
    I64_STORE32 = "i64.store32"
    MEMORY_SIZE = "memory.size"
    MEMORY_GROW = "memory.grow"
    
    # Constants
    I32_CONST = "i32.const"
    I64_CONST = "i64.const"
    F32_CONST = "f32.const"
    F64_CONST = "f64.const"
    
    # Comparison
    I32_EQZ = "i32.eqz"
    I32_EQ = "i32.eq"
    I32_NE = "i32.ne"
    I32_LT_S = "i32.lt_s"
    I32_LT_U = "i32.lt_u"
    I32_GT_S = "i32.gt_s"
    I32_GT_U = "i32.gt_u"
    I32_LE_S = "i32.le_s"
    I32_LE_U = "i32.le_u"
    I32_GE_S = "i32.ge_s"
    I32_GE_U = "i32.ge_u"
    
    # Arithmetic
    I32_CLZ = "i32.clz"
    I32_CTZ = "i32.ctz"
    I32_POPCNT = "i32.popcnt"
    I32_ADD = "i32.add"
    I32_SUB = "i32.sub"
    I32_MUL = "i32.mul"
    I32_DIV_S = "i32.div_s"
    I32_DIV_U = "i32.div_u"
    I32_REM_S = "i32.rem_s"
    I32_REM_U = "i32.rem_u"
    I32_AND = "i32.and"
    I32_OR = "i32.or"
    I32_XOR = "i32.xor"
    I32_SHL = "i32.shl"
    I32_SHR_S = "i32.shr_s"
    I32_SHR_U = "i32.shr_u"
    I32_ROTL = "i32.rotl"
    I32_ROTR = "i32.rotr"
    
    # Conversion
    I32_WRAP_I64 = "i32.wrap_i64"
    I32_TRUNC_F32_S = "i32.trunc_f32_s"
    I32_TRUNC_F32_U = "i32.trunc_f32_u"
    I32_TRUNC_F64_S = "i32.trunc_f64_s"
    I32_TRUNC_F64_U = "i32.trunc_f64_u"
    I64_EXTEND_I32_S = "i64.extend_i32_s"
    I64_EXTEND_I32_U = "i64.extend_i32_u"
    F32_CONVERT_I32_S = "f32.convert_i32_s"
    F32_CONVERT_I32_U = "f32.convert_i32_u"
    F32_CONVERT_I64_S = "f32.convert_i64_s"
    F32_CONVERT_I64_U = "f32.convert_i64_u"
    F32_DEMOTE_F64 = "f32.demote_f64"
    F64_CONVERT_I32_S = "f64.convert_i32_s"
    F64_CONVERT_I32_U = "f64.convert_i32_u"
    F64_CONVERT_I64_S = "f64.convert_i64_s"
    F64_CONVERT_I64_U = "f64.convert_i64_u"
    F64_PROMOTE_F32 = "f64.promote_f32"
    I32_REINTERPRET_F32 = "i32.reinterpret_f32"
    I64_REINTERPRET_F64 = "i64.reinterpret_f64"
    F32_REINTERPRET_I32 = "f32.reinterpret_i32"
    F64_REINTERPRET_I64 = "f64.reinterpret_i64"


class WasmVisitor(ABC):
    """Visitor interface for WebAssembly AST nodes."""
    
    @abstractmethod
    def visit_wasm_module(self, node: 'WasmModule'): pass
    
    @abstractmethod
    def visit_wasm_function(self, node: 'WasmFunction'): pass
    
    @abstractmethod
    def visit_wasm_instruction(self, node: 'WasmInstruction'): pass
    
    @abstractmethod
    def visit_wasm_type(self, node: 'WasmType'): pass
    
    @abstractmethod
    def visit_wasm_import(self, node: 'WasmImport'): pass
    
    @abstractmethod
    def visit_wasm_export(self, node: 'WasmExport'): pass
    
    @abstractmethod
    def visit_wasm_table(self, node: 'WasmTable'): pass
    
    @abstractmethod
    def visit_wasm_memory(self, node: 'WasmMemory'): pass
    
    @abstractmethod
    def visit_wasm_global(self, node: 'WasmGlobal'): pass
    
    @abstractmethod
    def visit_wasm_data(self, node: 'WasmData'): pass
    
    @abstractmethod
    def visit_wasm_element(self, node: 'WasmElement'): pass


class WasmNode(ABC):
    """Base class for all WebAssembly AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: WasmVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class WasmModule(WasmNode):
    """WebAssembly module."""
    types: List['WasmType'] = field(default_factory=list)
    imports: List['WasmImport'] = field(default_factory=list)
    functions: List['WasmFunction'] = field(default_factory=list)
    tables: List['WasmTable'] = field(default_factory=list)
    memories: List['WasmMemory'] = field(default_factory=list)
    globals: List['WasmGlobal'] = field(default_factory=list)
    exports: List['WasmExport'] = field(default_factory=list)
    start: Optional[int] = None
    elements: List['WasmElement'] = field(default_factory=list)
    data: List['WasmData'] = field(default_factory=list)
    custom_sections: List['WasmCustomSection'] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_module(self)


@dataclass
class WasmType(WasmNode):
    """WebAssembly function type."""
    parameters: List[WasmValueType] = field(default_factory=list)
    results: List[WasmValueType] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_type(self)


@dataclass
class WasmImport(WasmNode):
    """WebAssembly import."""
    module: str
    name: str
    kind: str  # func, table, memory, global
    type_index: Optional[int] = None
    type_info: Optional[Any] = None
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_import(self)


@dataclass
class WasmExport(WasmNode):
    """WebAssembly export."""
    name: str
    kind: str  # func, table, memory, global
    index: int
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_export(self)


@dataclass
class WasmFunction(WasmNode):
    """WebAssembly function."""
    type_index: int
    locals: List[WasmValueType] = field(default_factory=list)
    body: List['WasmInstruction'] = field(default_factory=list)
    name: Optional[str] = None
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_function(self)


@dataclass
class WasmTable(WasmNode):
    """WebAssembly table."""
    element_type: WasmValueType
    limits: 'WasmLimits'
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_table(self)


@dataclass
class WasmMemory(WasmNode):
    """WebAssembly memory."""
    limits: 'WasmLimits'
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_memory(self)


@dataclass
class WasmGlobal(WasmNode):
    """WebAssembly global variable."""
    value_type: WasmValueType
    mutability: WasmMutability
    init: List['WasmInstruction'] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_global(self)


@dataclass
class WasmData(WasmNode):
    """WebAssembly data segment."""
    memory_index: int
    offset: List['WasmInstruction'] = field(default_factory=list)
    data: bytes = b''
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_data(self)


@dataclass
class WasmElement(WasmNode):
    """WebAssembly element segment."""
    table_index: int
    offset: List['WasmInstruction'] = field(default_factory=list)
    init: List[int] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_element(self)


@dataclass
class WasmCustomSection(WasmNode):
    """WebAssembly custom section."""
    name: str
    data: bytes
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_custom_section(self)


@dataclass
class WasmLimits(WasmNode):
    """WebAssembly limits."""
    min: int
    max: Optional[int] = None
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_limits(self)


@dataclass
class WasmInstruction(WasmNode):
    """WebAssembly instruction."""
    opcode: WasmOpcode
    args: List[Any] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_instruction(self)


@dataclass
class WasmBlock(WasmNode):
    """WebAssembly block structure."""
    label: Optional[str] = None
    result_type: Optional[WasmValueType] = None
    instructions: List[WasmInstruction] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_block(self)


@dataclass
class WasmLoop(WasmNode):
    """WebAssembly loop structure."""
    label: Optional[str] = None
    result_type: Optional[WasmValueType] = None
    instructions: List[WasmInstruction] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_loop(self)


@dataclass
class WasmIf(WasmNode):
    """WebAssembly if structure."""
    label: Optional[str] = None
    result_type: Optional[WasmValueType] = None
    then_instructions: List[WasmInstruction] = field(default_factory=list)
    else_instructions: List[WasmInstruction] = field(default_factory=list)
    
    def accept(self, visitor: WasmVisitor) -> Any:
        return visitor.visit_wasm_if(self)


# Utility functions
def create_wasm_module(types: List[WasmType] = None,
                      imports: List[WasmImport] = None,
                      functions: List[WasmFunction] = None,
                      tables: List[WasmTable] = None,
                      memories: List[WasmMemory] = None,
                      globals: List[WasmGlobal] = None,
                      exports: List[WasmExport] = None,
                      start: int = None,
                      elements: List[WasmElement] = None,
                      data: List[WasmData] = None) -> WasmModule:
    """Create a WebAssembly module with specified components."""
    return WasmModule(
        types=types or [],
        imports=imports or [],
        functions=functions or [],
        tables=tables or [],
        memories=memories or [],
        globals=globals or [],
        exports=exports or [],
        start=start,
        elements=elements or [],
        data=data or []
    )


def create_wasm_function(type_index: int,
                        locals: List[WasmValueType] = None,
                        body: List[WasmInstruction] = None,
                        name: str = None) -> WasmFunction:
    """Create a WebAssembly function."""
    return WasmFunction(
        type_index=type_index,
        locals=locals or [],
        body=body or [],
        name=name
    )


def create_wasm_instruction(opcode: WasmOpcode, *args) -> WasmInstruction:
    """Create a WebAssembly instruction."""
    return WasmInstruction(opcode=opcode, args=list(args))


def create_wasm_type(parameters: List[WasmValueType] = None,
                    results: List[WasmValueType] = None) -> WasmType:
    """Create a WebAssembly function type."""
    return WasmType(
        parameters=parameters or [],
        results=results or []
    )


def create_wasm_limits(min_val: int, max_val: int = None) -> WasmLimits:
    """Create WebAssembly limits."""
    return WasmLimits(min=min_val, max=max_val)


def create_wasm_memory(min_pages: int, max_pages: int = None) -> WasmMemory:
    """Create WebAssembly memory."""
    return WasmMemory(limits=create_wasm_limits(min_pages, max_pages))


def create_wasm_table(element_type: WasmValueType,
                     min_size: int,
                     max_size: int = None) -> WasmTable:
    """Create WebAssembly table."""
    return WasmTable(
        element_type=element_type,
        limits=create_wasm_limits(min_size, max_size)
    )


def create_wasm_global(value_type: WasmValueType,
                      mutability: WasmMutability,
                      init_instructions: List[WasmInstruction] = None) -> WasmGlobal:
    """Create WebAssembly global variable."""
    return WasmGlobal(
        value_type=value_type,
        mutability=mutability,
        init=init_instructions or []
    )


def create_wasm_import(module: str, name: str, kind: str,
                      type_index: int = None, type_info: Any = None) -> WasmImport:
    """Create WebAssembly import."""
    return WasmImport(
        module=module,
        name=name,
        kind=kind,
        type_index=type_index,
        type_info=type_info
    )


def create_wasm_export(name: str, kind: str, index: int) -> WasmExport:
    """Create WebAssembly export."""
    return WasmExport(name=name, kind=kind, index=index)


def create_wasm_data(memory_index: int,
                    offset_instructions: List[WasmInstruction] = None,
                    data: bytes = b'') -> WasmData:
    """Create WebAssembly data segment."""
    return WasmData(
        memory_index=memory_index,
        offset=offset_instructions or [],
        data=data
    )


def create_wasm_element(table_index: int,
                       offset_instructions: List[WasmInstruction] = None,
                       init: List[int] = None) -> WasmElement:
    """Create WebAssembly element segment."""
    return WasmElement(
        table_index=table_index,
        offset=offset_instructions or [],
        init=init or []
    )


# Extended visitor for more nodes
class WasmVisitorExtended(WasmVisitor):
    """Extended visitor with additional node types."""
    
    def visit_wasm_custom_section(self, node: WasmCustomSection): pass
    def visit_wasm_limits(self, node: WasmLimits): pass
    def visit_wasm_block(self, node: WasmBlock): pass
    def visit_wasm_loop(self, node: WasmLoop): pass
    def visit_wasm_if(self, node: WasmIf): pass