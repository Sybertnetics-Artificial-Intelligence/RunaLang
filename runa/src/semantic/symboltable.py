"""
Symbol table implementation for Runa programming language.

This module provides a symbol table for tracking variable declarations,
function definitions, and types during semantic analysis.
"""

from typing import Dict, Optional, List, Any, Set
from enum import Enum, auto


class SymbolType(Enum):
    """Type of symbol in the symbol table."""
    
    VARIABLE = auto()
    FUNCTION = auto()
    TYPE = auto()
    PARAMETER = auto()


class Symbol:
    """
    Represents a symbol in the symbol table.
    
    Attributes:
        name: The name of the symbol
        symbol_type: The type of symbol (variable, function, etc.)
        data_type: The data type of the symbol (if applicable)
        defined: Whether the symbol has been defined
        initialized: Whether the symbol has been initialized
        position: The position of the symbol in the source code
        scope_level: The scope level where the symbol is defined
    """
    
    def __init__(
        self,
        name: str,
        symbol_type: SymbolType,
        data_type: Optional[str] = None,
        defined: bool = True,
        initialized: bool = False,
        position: Optional[tuple[int, int]] = None,
        scope_level: int = 0
    ):
        """
        Initialize a new Symbol.
        
        Args:
            name: The name of the symbol
            symbol_type: The type of symbol (variable, function, etc.)
            data_type: The data type of the symbol (if applicable)
            defined: Whether the symbol has been defined
            initialized: Whether the symbol has been initialized
            position: The position of the symbol in the source code
            scope_level: The scope level where the symbol is defined
        """
        self.name = name
        self.symbol_type = symbol_type
        self.data_type = data_type
        self.defined = defined
        self.initialized = initialized
        self.position = position
        self.scope_level = scope_level
        # Additional attributes for functions
        self.parameters: List[Symbol] = []
        self.return_type: Optional[str] = None
        # Additional attributes for types
        self.fields: Dict[str, Symbol] = {}
    
    def __str__(self) -> str:
        """Return a string representation of the symbol."""
        return f"{self.name} ({self.symbol_type.name}): {self.data_type or 'unknown'}"


class Scope:
    """
    Represents a scope in the symbol table.
    
    A scope contains a set of symbols defined in that scope.
    
    Attributes:
        level: The nesting level of the scope
        symbols: Dictionary of symbols in this scope
        parent: The parent scope (None for global scope)
    """
    
    def __init__(self, level: int, parent: Optional['Scope'] = None):
        """
        Initialize a new Scope.
        
        Args:
            level: The nesting level of the scope
            parent: The parent scope (None for global scope)
        """
        self.level = level
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent
    
    def define(self, symbol: Symbol) -> None:
        """
        Define a symbol in this scope.
        
        Args:
            symbol: The symbol to define
        """
        self.symbols[symbol.name] = symbol
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """
        Resolve a symbol in this scope.
        
        Args:
            name: The name of the symbol to resolve
            
        Returns:
            The resolved symbol or None if not found in this scope
        """
        return self.symbols.get(name)
    
    def __str__(self) -> str:
        """Return a string representation of the scope."""
        return f"Scope(level={self.level}, symbols={list(self.symbols.keys())})"


class SymbolTable:
    """
    Symbol table for tracking variable declarations, function definitions, and types.
    
    The symbol table maintains a hierarchy of scopes for nested blocks.
    
    Attributes:
        scopes: Stack of scopes, with the global scope at the bottom
        current_scope: The current scope being populated
    """
    
    def __init__(self):
        """Initialize a new SymbolTable with a global scope."""
        self.global_scope = Scope(0)
        self.scopes: List[Scope] = [self.global_scope]
        self.current_scope = self.global_scope
    
    def enter_scope(self) -> None:
        """Enter a new scope."""
        new_scope = Scope(len(self.scopes), self.current_scope)
        self.scopes.append(new_scope)
        self.current_scope = new_scope
    
    def exit_scope(self) -> None:
        """Exit the current scope and return to the parent scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope = self.scopes[-1]
    
    def define(self, symbol: Symbol) -> None:
        """
        Define a symbol in the current scope.
        
        Args:
            symbol: The symbol to define
        """
        symbol.scope_level = self.current_scope.level
        self.current_scope.define(symbol)
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """
        Resolve a symbol by searching in the current scope and parent scopes.
        
        Args:
            name: The name of the symbol to resolve
            
        Returns:
            The resolved symbol or None if not found
        """
        # Start with the current scope
        scope = self.current_scope
        
        # Traverse up the scope chain
        while scope:
            symbol = scope.resolve(name)
            if symbol:
                return symbol
            
            scope = scope.parent
        
        return None
    
    def resolve_local(self, name: str) -> Optional[Symbol]:
        """
        Resolve a symbol in the current scope only.
        
        Args:
            name: The name of the symbol to resolve
            
        Returns:
            The resolved symbol or None if not found in the current scope
        """
        return self.current_scope.resolve(name)
    
    def define_variable(
        self,
        name: str,
        data_type: Optional[str] = None,
        initialized: bool = False,
        position: Optional[tuple[int, int]] = None
    ) -> Symbol:
        """
        Define a variable in the current scope.
        
        Args:
            name: The name of the variable
            data_type: The data type of the variable
            initialized: Whether the variable has been initialized
            position: The position of the variable in the source code
            
        Returns:
            The created Symbol
        """
        symbol = Symbol(
            name,
            SymbolType.VARIABLE,
            data_type,
            True,
            initialized,
            position,
            self.current_scope.level
        )
        self.define(symbol)
        return symbol
    
    def define_function(
        self,
        name: str,
        return_type: Optional[str] = None,
        parameters: Optional[List[Symbol]] = None,
        position: Optional[tuple[int, int]] = None
    ) -> Symbol:
        """
        Define a function in the current scope.
        
        Args:
            name: The name of the function
            return_type: The return type of the function
            parameters: List of parameter symbols
            position: The position of the function in the source code
            
        Returns:
            The created Symbol
        """
        symbol = Symbol(
            name,
            SymbolType.FUNCTION,
            None,
            True,
            True,
            position,
            self.current_scope.level
        )
        symbol.return_type = return_type
        symbol.parameters = parameters or []
        self.define(symbol)
        return symbol
    
    def define_type(
        self,
        name: str,
        fields: Optional[Dict[str, Symbol]] = None,
        position: Optional[tuple[int, int]] = None
    ) -> Symbol:
        """
        Define a type in the current scope.
        
        Args:
            name: The name of the type
            fields: Dictionary of field symbols
            position: The position of the type in the source code
            
        Returns:
            The created Symbol
        """
        symbol = Symbol(
            name,
            SymbolType.TYPE,
            name,
            True,
            True,
            position,
            self.current_scope.level
        )
        symbol.fields = fields or {}
        self.define(symbol)
        return symbol
    
    def __str__(self) -> str:
        """Return a string representation of the symbol table."""
        result = []
        for i, scope in enumerate(self.scopes):
            scope_symbols = ", ".join(scope.symbols.keys())
            result.append(f"Scope {i}: {scope_symbols}")
        
        return "\n".join(result) 