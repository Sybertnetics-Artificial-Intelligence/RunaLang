#!/usr/bin/env python3
"""
Test file for Runa type definition parsing.

This file tests the parse_type_definition method to ensure it correctly
handles various forms of type definitions in Runa's natural language syntax.
"""

import pytest
from src.runa.languages.runa.lexer import RunaLexer
from src.runa.languages.runa.runa_parser import RunaParser
from src.runa.core.runa_ast import (
    TypeDefinition, BasicType, GenericType, UnionType, 
    Program
)


class TestTypeDefinitionParsing:
    """Test suite for type definition parsing."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.lexer = RunaLexer()
        self.parser = RunaParser()
    
    def parse_type_definition(self, source: str) -> TypeDefinition:
        """Helper method to parse a type definition from source code."""
        tokens = self.lexer.tokenize(source)
        self.parser.tokens = tokens
        self.parser.current = 0
        program = self.parser.parse_program()
        assert len(program.statements) == 1, f"Expected 1 statement, got {len(program.statements)}"
        assert isinstance(program.statements[0], TypeDefinition), "Expected TypeDefinition"
        return program.statements[0]
    
    def test_simple_type_alias(self):
        """Test simple type alias like 'Type UserId is Integer'."""
        source = "Type UserId is Integer"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "UserId"
        assert isinstance(type_def.definition, BasicType)
        assert type_def.definition.name == "Integer"
    
    def test_builtin_type_alias(self):
        """Test type alias with built-in types."""
        test_cases = [
            ("Type MyInt is Integer", "Integer"),
            ("Type MyFloat is Float", "Float"),
            ("Type MyString is String", "String"),
            ("Type MyBool is Boolean", "Boolean"),
        ]
        
        for source, expected_type in test_cases:
            type_def = self.parse_type_definition(source)
            assert type_def.definition.name == expected_type
    
    def test_generic_type_alias(self):
        """Test generic type alias like 'Type MyList is List[Integer]'."""
        source = "Type MyList is List[Integer]"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "MyList"
        assert isinstance(type_def.definition, GenericType)
        assert type_def.definition.base_type == "List"
        assert len(type_def.definition.type_args) == 1
        assert isinstance(type_def.definition.type_args[0], BasicType)
        assert type_def.definition.type_args[0].name == "Integer"
    
    def test_multiple_generic_parameters(self):
        """Test generic type with multiple parameters like 'Type MyDict is Dictionary[String, Integer]'."""
        source = "Type MyDict is Dictionary[String, Integer]"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "MyDict"
        assert isinstance(type_def.definition, GenericType)
        assert type_def.definition.base_type == "Dictionary"
        assert len(type_def.definition.type_args) == 2
        
        # Check first type argument (String)
        assert isinstance(type_def.definition.type_args[0], BasicType)
        assert type_def.definition.type_args[0].name == "String"
        
        # Check second type argument (Integer)
        assert isinstance(type_def.definition.type_args[1], BasicType)
        assert type_def.definition.type_args[1].name == "Integer"
    
    def test_union_type(self):
        """Test union type like 'Type Result is Integer OR String'."""
        source = "Type Result is Integer OR String"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "Result"
        assert isinstance(type_def.definition, UnionType)
        assert len(type_def.definition.types) == 2
        
        # Check union members
        assert isinstance(type_def.definition.types[0], BasicType)
        assert type_def.definition.types[0].name == "Integer"
        assert isinstance(type_def.definition.types[1], BasicType)
        assert type_def.definition.types[1].name == "String"
    
    def test_multiple_union_types(self):
        """Test union type with multiple alternatives."""
        source = "Type Status is Integer OR String OR Boolean"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "Status"
        assert isinstance(type_def.definition, UnionType)
        assert len(type_def.definition.types) == 3
        
        # Check all union members
        expected_types = ["Integer", "String", "Boolean"]
        for i, expected in enumerate(expected_types):
            assert isinstance(type_def.definition.types[i], BasicType)
            assert type_def.definition.types[i].name == expected
    
    def test_string_literal_type(self):
        """Test type with string literal like 'Type Status is \"active\"'."""
        source = 'Type Status is "active"'
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "Status"
        assert isinstance(type_def.definition, BasicType)
        assert type_def.definition.name == '"active"'
    
    def test_custom_type_reference(self):
        """Test type definition referencing another custom type."""
        source = "Type NewUserId is UserId"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "NewUserId"
        assert isinstance(type_def.definition, BasicType)
        assert type_def.definition.name == "UserId"
    
    def test_nested_generic_types(self):
        """Test nested generic types like 'Type Complex is List[Dictionary[String, Integer]]'."""
        source = "Type Complex is List[Dictionary[String, Integer]]"
        type_def = self.parse_type_definition(source)
        
        assert type_def.name == "Complex"
        assert isinstance(type_def.definition, GenericType)
        assert type_def.definition.base_type == "List"
        assert len(type_def.definition.type_args) == 1
        
        # Check nested Dictionary type
        nested_type = type_def.definition.type_args[0]
        assert isinstance(nested_type, GenericType)
        assert nested_type.base_type == "Dictionary"
        assert len(nested_type.type_args) == 2
        assert nested_type.type_args[0].name == "String"
        assert nested_type.type_args[1].name == "Integer"

    def test_error_cases(self):
        """Test various error cases in type definitions."""
        error_cases = [
            "Type",  # Missing name and definition
            "Type UserId",  # Missing 'is' and definition
            "Type UserId is",  # Missing type definition
            "UserId is Integer",  # Missing 'Type' keyword
        ]
        
        for source in error_cases:
            with pytest.raises(Exception):  # Could be ParseError or other parsing exception
                self.parse_type_definition(source)


if __name__ == "__main__":
    # Simple standalone test
    lexer = RunaLexer()
    parser = RunaParser()
    
    test_source = "Type UserId is Integer"
    print(f"Testing: {test_source}")
    
    tokens = lexer.tokenize(test_source)
    parser.tokens = tokens
    parser.current = 0
    
    try:
        program = parser.parse_program()
        type_def = program.statements[0]
        print(f"✅ Successfully parsed type definition: {type_def.name} -> {type_def.definition.name}")
    except Exception as e:
        print(f"❌ Parse error: {e}")
    
    print("\nType definition parsing implementation complete!") 