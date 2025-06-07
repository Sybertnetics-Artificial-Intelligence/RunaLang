"""
Comprehensive Symbol Table Tests for Runa Programming Language.

This module contains extensive tests for the symbol table implementation,
covering symbol management, scoping, and error handling.

Test Categories:
- Basic symbol operations
- Scope management
- Symbol lookup and resolution
- Error handling
- Built-in symbols
- Complex scoping scenarios
"""

import pytest
from typing import List, Any

from runa.symbol_table import (
    SymbolTable, Symbol, FunctionSymbol, ClassSymbol,
    SymbolType, SymbolVisibility, ScopeType, Scope
)
from runa.ast_nodes import TypeAnnotation
from runa.errors import SourcePosition, RunaSemanticError


class TestSymbolBasics:
    """Test basic symbol functionality."""
    
    def test_symbol_creation(self):
        """Test creating a basic symbol."""
        position = SourcePosition(1, 1)
        symbol = Symbol(
            name="test_var",
            symbol_type=SymbolType.VARIABLE,
            data_type=None,
            position=position,
            is_mutable=True,
            is_initialized=True
        )
        
        assert symbol.name == "test_var"
        assert symbol.symbol_type == SymbolType.VARIABLE
        assert symbol.is_mutable
        assert symbol.is_initialized
        assert symbol.position == position
    
    def test_function_symbol_creation(self):
        """Test creating a function symbol."""
        position = SourcePosition(1, 1)
        param1 = Symbol("x", SymbolType.PARAMETER, None, position)
        param2 = Symbol("y", SymbolType.PARAMETER, None, position)
        
        func_symbol = FunctionSymbol(
            name="test_func",
            symbol_type=SymbolType.FUNCTION,
            data_type=None,
            position=position,
            parameters=[param1, param2],
            return_type=None
        )
        
        assert func_symbol.name == "test_func"
        assert func_symbol.symbol_type == SymbolType.FUNCTION
        assert len(func_symbol.parameters) == 2
        assert func_symbol.parameters[0].name == "x"
        assert func_symbol.parameters[1].name == "y"
    
    def test_class_symbol_creation(self):
        """Test creating a class symbol."""
        position = SourcePosition(1, 1)
        class_symbol = ClassSymbol(
            name="TestClass",
            symbol_type=SymbolType.CLASS,
            data_type=None,
            position=position
        )
        
        assert class_symbol.name == "TestClass"
        assert class_symbol.symbol_type == SymbolType.CLASS
        assert len(class_symbol.methods) == 0
        assert len(class_symbol.fields) == 0


class TestScopeBasics:
    """Test basic scope functionality."""
    
    def test_scope_creation(self):
        """Test creating a scope."""
        scope = Scope(ScopeType.GLOBAL, "global")
        
        assert scope.scope_type == ScopeType.GLOBAL
        assert scope.name == "global"
        assert scope.parent is None
        assert scope.level == 0
        assert len(scope.symbols) == 0
    
    def test_nested_scope_creation(self):
        """Test creating nested scopes."""
        global_scope = Scope(ScopeType.GLOBAL, "global")
        function_scope = Scope(ScopeType.FUNCTION, "test_func", global_scope)
        
        assert function_scope.parent == global_scope
        assert function_scope.level == 1
        assert global_scope in function_scope.parent.children
    
    def test_symbol_definition_in_scope(self):
        """Test defining symbols in a scope."""
        scope = Scope(ScopeType.GLOBAL, "global")
        position = SourcePosition(1, 1)
        symbol = Symbol("test_var", SymbolType.VARIABLE, None, position)
        
        scope.define(symbol)
        
        assert "test_var" in scope.symbols
        assert scope.lookup_local("test_var") == symbol
    
    def test_symbol_redefinition_error(self):
        """Test error on symbol redefinition in same scope."""
        scope = Scope(ScopeType.GLOBAL, "global")
        position = SourcePosition(1, 1)
        symbol1 = Symbol("test_var", SymbolType.VARIABLE, None, position)
        symbol2 = Symbol("test_var", SymbolType.VARIABLE, None, position)
        
        scope.define(symbol1)
        
        with pytest.raises(RunaSemanticError):
            scope.define(symbol2)
    
    def test_symbol_lookup_chain(self):
        """Test symbol lookup through scope chain."""
        global_scope = Scope(ScopeType.GLOBAL, "global")
        function_scope = Scope(ScopeType.FUNCTION, "test_func", global_scope)
        
        position = SourcePosition(1, 1)
        global_symbol = Symbol("global_var", SymbolType.VARIABLE, None, position)
        local_symbol = Symbol("local_var", SymbolType.VARIABLE, None, position)
        
        global_scope.define(global_symbol)
        function_scope.define(local_symbol)
        
        # Local lookup should find local symbol
        assert function_scope.lookup_local("local_var") == local_symbol
        assert function_scope.lookup_local("global_var") is None
        
        # Chain lookup should find both
        assert function_scope.lookup("local_var") == local_symbol
        assert function_scope.lookup("global_var") == global_symbol


class TestSymbolTable:
    """Test symbol table functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.symbol_table = SymbolTable()
    
    def test_symbol_table_initialization(self):
        """Test symbol table initialization."""
        assert self.symbol_table.global_scope is not None
        assert self.symbol_table.current_scope == self.symbol_table.global_scope
        assert len(self.symbol_table.scope_stack) == 1
        
        # Check built-in symbols are present
        assert self.symbol_table.lookup("print") is not None
        assert self.symbol_table.lookup("string") is not None
        assert self.symbol_table.lookup("number") is not None
    
    def test_symbol_definition(self):
        """Test defining symbols in symbol table."""
        position = SourcePosition(1, 1)
        symbol = Symbol("test_var", SymbolType.VARIABLE, None, position)
        
        self.symbol_table.define(symbol)
        
        assert self.symbol_table.lookup("test_var") == symbol
        assert self.symbol_table.is_defined("test_var")
        assert self.symbol_table.is_defined_anywhere("test_var")
    
    def test_scope_management(self):
        """Test scope creation and management."""
        # Start in global scope
        assert self.symbol_table.get_current_scope_type() == ScopeType.GLOBAL
        assert self.symbol_table.get_scope_level() == 0
        
        # Enter function scope
        func_scope = self.symbol_table.enter_scope(ScopeType.FUNCTION, "test_func")
        assert self.symbol_table.get_current_scope_type() == ScopeType.FUNCTION
        assert self.symbol_table.get_scope_level() == 1
        assert self.symbol_table.current_scope == func_scope
        
        # Exit scope
        exited_scope = self.symbol_table.exit_scope()
        assert exited_scope == func_scope
        assert self.symbol_table.get_current_scope_type() == ScopeType.GLOBAL
        assert self.symbol_table.get_scope_level() == 0
    
    def test_nested_scoping(self):
        """Test nested scope behavior."""
        position = SourcePosition(1, 1)
        
        # Define global variable
        global_var = Symbol("x", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(global_var)
        
        # Enter function scope
        self.symbol_table.enter_scope(ScopeType.FUNCTION, "test_func")
        
        # Define local variable with same name
        local_var = Symbol("x", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(local_var)
        
        # Local lookup should find local variable
        assert self.symbol_table.lookup_local("x") == local_var
        assert self.symbol_table.lookup("x") == local_var  # Shadows global
        
        # Exit scope
        self.symbol_table.exit_scope()
        
        # Should now find global variable
        assert self.symbol_table.lookup("x") == global_var
    
    def test_function_scope_creation(self):
        """Test creating function scope with parameters."""
        position = SourcePosition(1, 1)
        param1 = Symbol("x", SymbolType.PARAMETER, None, position)
        param2 = Symbol("y", SymbolType.PARAMETER, None, position)
        
        func_scope = self.symbol_table.create_function_scope("test_func", [param1, param2])
        
        assert self.symbol_table.current_scope == func_scope
        assert self.symbol_table.lookup("x") == param1
        assert self.symbol_table.lookup("y") == param2
    
    def test_block_scope_creation(self):
        """Test creating block scope."""
        block_scope = self.symbol_table.create_block_scope("test_block")
        
        assert self.symbol_table.current_scope == block_scope
        assert block_scope.scope_type == ScopeType.BLOCK
        assert block_scope.name == "test_block"
    
    def test_symbol_update(self):
        """Test updating symbol properties."""
        position = SourcePosition(1, 1)
        symbol = Symbol("test_var", SymbolType.VARIABLE, None, position, is_initialized=False)
        
        self.symbol_table.define(symbol)
        assert not symbol.is_initialized
        
        self.symbol_table.update_symbol("test_var", is_initialized=True)
        assert symbol.is_initialized
    
    def test_symbol_update_nonexistent(self):
        """Test error when updating nonexistent symbol."""
        with pytest.raises(RunaSemanticError):
            self.symbol_table.update_symbol("nonexistent", is_initialized=True)


class TestBuiltinSymbols:
    """Test built-in symbol functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.symbol_table = SymbolTable()
    
    def test_builtin_types_present(self):
        """Test that built-in types are present."""
        builtin_types = ["string", "number", "boolean", "list", "dict", "auto"]
        
        for type_name in builtin_types:
            symbol = self.symbol_table.lookup(type_name)
            assert symbol is not None
            assert symbol.symbol_type == SymbolType.TYPE
    
    def test_builtin_functions_present(self):
        """Test that built-in functions are present."""
        builtin_functions = ["print", "input", "len", "str", "int", "float", "bool"]
        
        for func_name in builtin_functions:
            symbol = self.symbol_table.lookup(func_name)
            assert symbol is not None
            assert symbol.symbol_type == SymbolType.FUNCTION
            assert isinstance(symbol, FunctionSymbol)
            assert symbol.is_builtin


class TestComplexScenarios:
    """Test complex scoping scenarios."""
    
    def setup_method(self):
        """Set up test environment."""
        self.symbol_table = SymbolTable()
    
    def test_deeply_nested_scopes(self):
        """Test deeply nested scope scenarios."""
        position = SourcePosition(1, 1)
        
        # Global variable
        global_var = Symbol("x", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(global_var)
        
        # Function scope
        self.symbol_table.enter_scope(ScopeType.FUNCTION, "outer_func")
        func_var = Symbol("y", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(func_var)
        
        # Block scope within function
        self.symbol_table.enter_scope(ScopeType.BLOCK, "if_block")
        block_var = Symbol("z", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(block_var)
        
        # All variables should be accessible
        assert self.symbol_table.lookup("x") == global_var
        assert self.symbol_table.lookup("y") == func_var
        assert self.symbol_table.lookup("z") == block_var
        
        # Exit block scope
        self.symbol_table.exit_scope()
        assert self.symbol_table.lookup("z") is None  # Block variable no longer accessible
        assert self.symbol_table.lookup("y") == func_var  # Function variable still accessible
        
        # Exit function scope
        self.symbol_table.exit_scope()
        assert self.symbol_table.lookup("y") is None  # Function variable no longer accessible
        assert self.symbol_table.lookup("x") == global_var  # Global variable still accessible
    
    def test_multiple_function_scopes(self):
        """Test multiple function scopes."""
        position = SourcePosition(1, 1)
        
        # First function
        self.symbol_table.enter_scope(ScopeType.FUNCTION, "func1")
        var1 = Symbol("local_var", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(var1)
        self.symbol_table.exit_scope()
        
        # Second function
        self.symbol_table.enter_scope(ScopeType.FUNCTION, "func2")
        var2 = Symbol("local_var", SymbolType.VARIABLE, None, position)  # Same name, different scope
        self.symbol_table.define(var2)
        
        # Should find the second variable
        assert self.symbol_table.lookup("local_var") == var2
        
        self.symbol_table.exit_scope()
        
        # Should not find any local_var in global scope
        assert self.symbol_table.lookup("local_var") is None
    
    def test_scope_chain_info(self):
        """Test scope chain information retrieval."""
        # Start with global scope
        chain = self.symbol_table.get_scope_chain()
        assert len(chain) == 1
        assert chain[0].scope_type == ScopeType.GLOBAL
        
        # Add function scope
        self.symbol_table.enter_scope(ScopeType.FUNCTION, "test_func")
        chain = self.symbol_table.get_scope_chain()
        assert len(chain) == 2
        assert chain[0].scope_type == ScopeType.GLOBAL
        assert chain[1].scope_type == ScopeType.FUNCTION
        
        # Add block scope
        self.symbol_table.enter_scope(ScopeType.BLOCK, "test_block")
        chain = self.symbol_table.get_scope_chain()
        assert len(chain) == 3
        assert chain[2].scope_type == ScopeType.BLOCK
    
    def test_scope_info_retrieval(self):
        """Test scope information retrieval."""
        info = self.symbol_table.get_scope_info()
        
        assert "current_scope" in info
        assert "scope_level" in info
        assert "scope_type" in info
        assert "symbol_count" in info
        
        assert info["scope_type"] == "GLOBAL"
        assert info["scope_level"] == 0
        assert info["symbol_count"] > 0  # Built-in symbols


class TestErrorHandling:
    """Test error handling in symbol table."""
    
    def setup_method(self):
        """Set up test environment."""
        self.symbol_table = SymbolTable()
    
    def test_exit_scope_at_global(self):
        """Test exiting scope when already at global level."""
        # Should return None when trying to exit global scope
        result = self.symbol_table.exit_scope()
        assert result is None
        assert self.symbol_table.current_scope == self.symbol_table.global_scope
    
    def test_symbol_visibility(self):
        """Test symbol visibility handling."""
        position = SourcePosition(1, 1)
        
        # Public symbol (default)
        public_symbol = Symbol("public_var", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(public_symbol)
        
        # Private symbol
        private_symbol = Symbol(
            "private_var", SymbolType.VARIABLE, None, position,
            visibility=SymbolVisibility.PRIVATE
        )
        self.symbol_table.define(private_symbol)
        
        # Both should be findable (visibility enforcement would be in semantic analyzer)
        assert self.symbol_table.lookup("public_var") == public_symbol
        assert self.symbol_table.lookup("private_var") == private_symbol
    
    def test_get_all_symbols(self):
        """Test retrieving all symbols in current scope."""
        position = SourcePosition(1, 1)
        
        # Add some symbols
        var1 = Symbol("var1", SymbolType.VARIABLE, None, position)
        var2 = Symbol("var2", SymbolType.VARIABLE, None, position)
        
        self.symbol_table.define(var1)
        self.symbol_table.define(var2)
        
        symbols = self.symbol_table.get_all_symbols_in_scope()
        
        assert "var1" in symbols
        assert "var2" in symbols
        assert symbols["var1"] == var1
        assert symbols["var2"] == var2
    
    def test_get_all_accessible_symbols(self):
        """Test retrieving all accessible symbols."""
        position = SourcePosition(1, 1)
        
        # Global symbol
        global_var = Symbol("global_var", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(global_var)
        
        # Enter function scope and add local symbol
        self.symbol_table.enter_scope(ScopeType.FUNCTION, "test_func")
        local_var = Symbol("local_var", SymbolType.VARIABLE, None, position)
        self.symbol_table.define(local_var)
        
        accessible = self.symbol_table.get_all_accessible_symbols()
        
        # Should include both global and local symbols, plus built-ins
        assert "global_var" in accessible
        assert "local_var" in accessible
        assert "print" in accessible  # Built-in function
        assert accessible["global_var"] == global_var
        assert accessible["local_var"] == local_var 