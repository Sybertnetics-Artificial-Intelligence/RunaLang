"""
Symbol Table Implementation for Runa Programming Language.

This module provides a comprehensive symbol table system with nested scoping
support for variable tracking, type information, and semantic analysis.

Features:
- Nested scoping with proper scope resolution
- Symbol binding and lookup
- Type information storage
- Function parameter tracking
- Variable mutability tracking
- Scope chain navigation
"""

from typing import Dict, List, Optional, Any, Set, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod

from .errors import SourcePosition, RunaSemanticError, semantic_error
from .ast_nodes import TypeAnnotation


class SymbolType(Enum):
    """Types of symbols that can be stored in the symbol table."""
    VARIABLE = auto()
    FUNCTION = auto()
    PARAMETER = auto()
    CONSTANT = auto()
    CLASS = auto()
    MODULE = auto()
    TYPE = auto()


class SymbolVisibility(Enum):
    """Visibility levels for symbols."""
    PUBLIC = auto()
    PRIVATE = auto()
    PROTECTED = auto()


@dataclass
class Symbol:
    """
    Represents a symbol in the symbol table.
    
    Contains all information about a declared identifier including
    its type, value, mutability, and source location.
    """
    name: str
    symbol_type: SymbolType
    data_type: Optional[TypeAnnotation]
    position: SourcePosition
    is_mutable: bool = True
    is_initialized: bool = False
    visibility: SymbolVisibility = SymbolVisibility.PUBLIC
    value: Optional[Any] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"Symbol({self.name}, {self.symbol_type.name}, {self.data_type})"
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class FunctionSymbol(Symbol):
    """Extended symbol for function definitions."""
    parameters: List[Symbol] = field(default_factory=list)
    return_type: Optional[TypeAnnotation] = None
    is_builtin: bool = False
    overloads: List['FunctionSymbol'] = field(default_factory=list)
    
    def __post_init__(self):
        self.symbol_type = SymbolType.FUNCTION


@dataclass
class ClassSymbol(Symbol):
    """Extended symbol for class definitions."""
    base_classes: List[str] = field(default_factory=list)
    methods: Dict[str, FunctionSymbol] = field(default_factory=dict)
    fields: Dict[str, Symbol] = field(default_factory=dict)
    
    def __post_init__(self):
        self.symbol_type = SymbolType.CLASS


class ScopeType(Enum):
    """Types of scopes in the program."""
    GLOBAL = auto()
    FUNCTION = auto()
    BLOCK = auto()
    CLASS = auto()
    MODULE = auto()
    LOOP = auto()
    CONDITIONAL = auto()


class Scope:
    """
    Represents a single scope level in the symbol table.
    
    Each scope maintains its own symbol dictionary and provides
    methods for symbol management within that scope.
    """
    
    def __init__(
        self, 
        scope_type: ScopeType, 
        name: str = "",
        parent: Optional['Scope'] = None
    ):
        self.scope_type = scope_type
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
        self.children: List['Scope'] = []
        self.level = 0 if parent is None else parent.level + 1
        
        if parent:
            parent.children.append(self)
    
    def define(self, symbol: Symbol) -> None:
        """
        Define a new symbol in this scope.
        
        Raises:
            RunaSemanticError: If symbol is already defined in this scope.
        """
        if symbol.name in self.symbols:
            existing = self.symbols[symbol.name]
            raise semantic_error(
                f"Symbol '{symbol.name}' is already defined in this scope",
                symbol.position,
                f"Previously defined at {existing.position}"
            )
        
        self.symbols[symbol.name] = symbol
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in this scope only."""
        return self.symbols.get(name)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in this scope and parent scopes.
        
        Follows the scope chain upward until the symbol is found
        or the global scope is reached.
        """
        symbol = self.lookup_local(name)
        if symbol is not None:
            return symbol
        
        if self.parent is not None:
            return self.parent.lookup(name)
        
        return None
    
    def is_defined(self, name: str) -> bool:
        """Check if a symbol is defined in this scope."""
        return name in self.symbols
    
    def is_defined_anywhere(self, name: str) -> bool:
        """Check if a symbol is defined in this scope or any parent scope."""
        return self.lookup(name) is not None
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Get all symbols defined in this scope."""
        return self.symbols.copy()
    
    def get_symbol_names(self) -> Set[str]:
        """Get all symbol names defined in this scope."""
        return set(self.symbols.keys())
    
    def update_symbol(self, name: str, **kwargs) -> None:
        """
        Update properties of an existing symbol.
        
        Raises:
            RunaSemanticError: If symbol is not found.
        """
        symbol = self.lookup(name)
        if symbol is None:
            raise semantic_error(
                f"Symbol '{name}' is not defined",
                SourcePosition(0, 0)  # Position would come from parser context
            )
        
        for key, value in kwargs.items():
            if hasattr(symbol, key):
                setattr(symbol, key, value)
    
    def __str__(self) -> str:
        """String representation for debugging."""
        symbols_str = ", ".join(self.symbols.keys()) if self.symbols else "empty"
        return f"Scope({self.scope_type.name}, {self.name}, symbols=[{symbols_str}])"
    
    def __repr__(self) -> str:
        return self.__str__()


class SymbolTable:
    """
    Main symbol table implementation with nested scoping support.
    
    Manages the scope stack and provides high-level operations for
    symbol definition, lookup, and scope management.
    """
    
    def __init__(self):
        """Initialize the symbol table with a global scope."""
        self.global_scope = Scope(ScopeType.GLOBAL, "global")
        self.current_scope = self.global_scope
        self.scope_stack: List[Scope] = [self.global_scope]
        self._initialize_builtins()
    
    def _initialize_builtins(self) -> None:
        """Initialize built-in symbols and functions."""
        # Built-in types
        builtin_types = [
            "integer", "string", "boolean", "float", "list", "dictionary"
        ]
        
        for type_name in builtin_types:
            type_symbol = Symbol(
                name=type_name,
                symbol_type=SymbolType.TYPE,
                data_type=None,
                position=SourcePosition(0, 0, "<builtin>"),
                is_mutable=False
            )
            self.global_scope.define(type_symbol)
        
        # Built-in functions
        builtin_functions = [
            ("display", [], None),
            ("input", [("prompt", "string")], "string"),
            ("length", [("obj", "any")], "integer"),
            ("type_of", [("obj", "any")], "string"),
        ]
        
        for func_name, params, return_type in builtin_functions:
            param_symbols = []
            for param_name, param_type in params:
                param_symbol = Symbol(
                    name=param_name,
                    symbol_type=SymbolType.PARAMETER,
                    data_type=TypeAnnotation(
                        position=SourcePosition(0, 0, "<builtin>"),
                        node_type=None,
                        type_name=param_type,
                        generic_args=None
                    ),
                    position=SourcePosition(0, 0, "<builtin>"),
                    is_mutable=True
                )
                param_symbols.append(param_symbol)
            
            func_symbol = FunctionSymbol(
                name=func_name,
                symbol_type=SymbolType.FUNCTION,
                data_type=None,
                position=SourcePosition(0, 0, "<builtin>"),
                is_mutable=False,
                parameters=param_symbols,
                return_type=TypeAnnotation(
                    position=SourcePosition(0, 0, "<builtin>"),
                    node_type=None,
                    type_name=return_type or "void",
                    generic_args=None
                ) if return_type else None,
                is_builtin=True
            )
            self.global_scope.define(func_symbol)
    
    def enter_scope(self, scope_type: ScopeType, name: str = "") -> Scope:
        """
        Enter a new scope.
        
        Creates a new scope as a child of the current scope and
        pushes it onto the scope stack.
        """
        new_scope = Scope(scope_type, name, self.current_scope)
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self) -> Optional[Scope]:
        """
        Exit the current scope.
        
        Pops the current scope from the stack and returns to the parent scope.
        
        Returns:
            The exited scope, or None if already at global scope.
        """
        if len(self.scope_stack) <= 1:
            # Can't exit global scope
            return None
        
        exited_scope = self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
        return exited_scope
    
    def define(self, symbol: Symbol) -> None:
        """Define a symbol in the current scope."""
        self.current_scope.define(symbol)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol starting from the current scope."""
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in the current scope only."""
        return self.current_scope.lookup_local(name)
    
    def is_defined(self, name: str) -> bool:
        """Check if a symbol is defined in the current scope."""
        return self.current_scope.is_defined(name)
    
    def is_defined_anywhere(self, name: str) -> bool:
        """Check if a symbol is defined in any accessible scope."""
        return self.current_scope.is_defined_anywhere(name)
    
    def get_current_scope_type(self) -> ScopeType:
        """Get the type of the current scope."""
        return self.current_scope.scope_type
    
    def get_scope_level(self) -> int:
        """Get the nesting level of the current scope."""
        return self.current_scope.level
    
    def get_all_symbols_in_scope(self) -> Dict[str, Symbol]:
        """Get all symbols defined in the current scope."""
        return self.current_scope.get_all_symbols()
    
    def get_all_accessible_symbols(self) -> Dict[str, Symbol]:
        """
        Get all symbols accessible from the current scope.
        
        Returns symbols from current scope and all parent scopes,
        with current scope symbols taking precedence.
        """
        symbols = {}
        scope = self.current_scope
        
        while scope is not None:
            for name, symbol in scope.symbols.items():
                if name not in symbols:  # Current scope takes precedence
                    symbols[name] = symbol
            scope = scope.parent
        
        return symbols
    
    def update_symbol(self, name: str, **kwargs) -> None:
        """Update properties of an existing symbol."""
        self.current_scope.update_symbol(name, **kwargs)
    
    def create_function_scope(self, function_name: str, parameters: List[Symbol]) -> Scope:
        """
        Create a new function scope with parameters.
        
        Enters a function scope and defines all parameters as local symbols.
        """
        func_scope = self.enter_scope(ScopeType.FUNCTION, function_name)
        
        # Define parameters in the function scope
        for param in parameters:
            param.symbol_type = SymbolType.PARAMETER
            func_scope.define(param)
        
        return func_scope
    
    def create_block_scope(self, block_name: str = "") -> Scope:
        """Create a new block scope (for control structures)."""
        return self.enter_scope(ScopeType.BLOCK, block_name)
    
    def create_class_scope(self, class_name: str) -> Scope:
        """Create a new class scope."""
        return self.enter_scope(ScopeType.CLASS, class_name)
    
    def create_module_scope(self, module_name: str) -> Scope:
        """Create a new module scope."""
        return self.enter_scope(ScopeType.MODULE, module_name)
    
    def get_scope_chain(self) -> List[Scope]:
        """Get the current scope chain from global to current."""
        return self.scope_stack.copy()
    
    def get_scope_info(self) -> Dict[str, Any]:
        """Get debugging information about the current scope state."""
        return {
            'current_scope': str(self.current_scope),
            'scope_level': self.get_scope_level(),
            'scope_stack_size': len(self.scope_stack),
            'symbols_in_current_scope': len(self.current_scope.symbols),
            'total_accessible_symbols': len(self.get_all_accessible_symbols()),
            'scope_chain': [str(scope) for scope in self.scope_stack]
        }
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"SymbolTable(current={self.current_scope}, level={self.get_scope_level()})"
    
    def __repr__(self) -> str:
        return self.__str__()


# Export all public classes and functions
__all__ = [
    'Symbol',
    'FunctionSymbol', 
    'ClassSymbol',
    'SymbolType',
    'SymbolVisibility',
    'Scope',
    'ScopeType',
    'SymbolTable',
] 