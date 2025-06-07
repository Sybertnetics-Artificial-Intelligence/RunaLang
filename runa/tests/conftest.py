"""
PyTest configuration and shared fixtures for Runa testing.

This module provides comprehensive testing infrastructure including:
- Sample code fixtures
- VM state fixtures  
- Performance benchmarking setup
- Integration test helpers
"""

import pytest
from typing import Any, Dict, List
from pathlib import Path

# Sample Runa code for testing
SAMPLE_RUNA_PROGRAMS = {
    "hello_world": '''
Display "Hello, World!"
''',
    
    "variables": '''
Let user name be "Alex"
Let age be 30
Set user name to "Alexandra"
Display user name with message "is" and age and "years old"
''',
    
    "control_flow": '''
Let score be 85

If score is greater than 90:
    Display "Excellent!"
Otherwise if score is greater than 80:
    Display "Good job!"
Otherwise:
    Display "Keep trying!"
''',
    
    "loops": '''
Define colors as list containing "red", "blue", "green"

For each color in colors:
    Display color with message "is a beautiful color"
''',
    
    "functions": '''
Process called "Calculate Area" that takes width and height:
    Let area be width multiplied by height
    Return area

Let room area be Calculate Area with width as 10 and height as 12
Display room area
''',
    
    "ai_model": '''
Define neural network "SimpleClassifier":
    Input layer accepts 784 features
    Hidden layer with 128 neurons using ReLU activation
    Output layer with 10 classes using softmax activation

Configure training for SimpleClassifier:
    Use dataset "mnist" with 80/20 train/validation split
    Use Adam optimizer with learning rate 0.001
    Train for 10 epochs
''',
}

@pytest.fixture
def sample_programs() -> Dict[str, str]:
    """Provide sample Runa programs for testing."""
    return SAMPLE_RUNA_PROGRAMS

@pytest.fixture
def hello_world_program() -> str:
    """Simple hello world program."""
    return SAMPLE_RUNA_PROGRAMS["hello_world"]

@pytest.fixture
def variables_program() -> str:
    """Program demonstrating variable operations."""
    return SAMPLE_RUNA_PROGRAMS["variables"]

@pytest.fixture
def control_flow_program() -> str:
    """Program demonstrating control flow."""
    return SAMPLE_RUNA_PROGRAMS["control_flow"]

@pytest.fixture
def loops_program() -> str:
    """Program demonstrating loops."""
    return SAMPLE_RUNA_PROGRAMS["loops"]

@pytest.fixture
def functions_program() -> str:
    """Program demonstrating function definition and calls."""
    return SAMPLE_RUNA_PROGRAMS["functions"]

@pytest.fixture
def ai_model_program() -> str:
    """Program demonstrating AI model definition."""
    return SAMPLE_RUNA_PROGRAMS["ai_model"]

@pytest.fixture
def temp_runa_file(tmp_path: Path) -> Path:
    """Create a temporary .runa file for testing."""
    runa_file = tmp_path / "test.runa"
    runa_file.write_text(SAMPLE_RUNA_PROGRAMS["hello_world"])
    return runa_file

@pytest.fixture
def runa_project_dir(tmp_path: Path) -> Path:
    """Create a temporary Runa project directory structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create main.runa
    main_file = project_dir / "main.runa"
    main_file.write_text(SAMPLE_RUNA_PROGRAMS["hello_world"])
    
    # Create lib directory with a module
    lib_dir = project_dir / "lib"
    lib_dir.mkdir()
    
    utils_file = lib_dir / "utils.runa"
    utils_file.write_text('''
Process called "Add Numbers" that takes a and b:
    Return a plus b
''')
    
    return project_dir

@pytest.fixture
def mock_vm_state() -> Dict[str, Any]:
    """Provide a mock VM state for testing."""
    return {
        "stack": [],
        "heap": {},
        "variables": {},
        "call_stack": [],
        "pc": 0,  # program counter
        "status": "ready",
    }

@pytest.fixture
def performance_threshold() -> Dict[str, float]:
    """Performance thresholds for benchmarking."""
    return {
        "lexer_tokens_per_second": 10000,
        "parser_statements_per_second": 1000,
        "vm_instructions_per_second": 100000,
        "compilation_time_ms": 100,
    }

# Test markers for different test categories
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests across components"  
    )
    config.addinivalue_line(
        "markers", "benchmark: Performance benchmark tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to run"
    )
    config.addinivalue_line(
        "markers", "ai: Tests for AI-specific features"
    )

# Helper functions for testing
def assert_tokens_equal(actual_tokens: List[Any], expected_tokens: List[Any]) -> None:
    """Assert that two token lists are equal with helpful error messages."""
    assert len(actual_tokens) == len(expected_tokens), (
        f"Token count mismatch: expected {len(expected_tokens)}, "
        f"got {len(actual_tokens)}"
    )
    
    for i, (actual, expected) in enumerate(zip(actual_tokens, expected_tokens)):
        assert actual == expected, (
            f"Token {i} mismatch: expected {expected}, got {actual}"
        )

def assert_ast_structure(node: Any, expected_type: type, **expected_attrs) -> None:
    """Assert AST node structure with detailed error messages."""
    assert isinstance(node, expected_type), (
        f"Node type mismatch: expected {expected_type.__name__}, "
        f"got {type(node).__name__}"
    )
    
    for attr_name, expected_value in expected_attrs.items():
        actual_value = getattr(node, attr_name, None)
        assert actual_value == expected_value, (
            f"Node attribute '{attr_name}' mismatch: "
            f"expected {expected_value}, got {actual_value}"
        )

# Test data for edge cases
ERROR_TEST_CASES = {
    "syntax_errors": [
        "Let be 5",  # Missing variable name
        "Display",   # Missing arguments
        "If true",   # Missing colon
        "For each in colors:",  # Missing variable name
    ],
    
    "type_errors": [
        "Let x be 5\nLet y be x plus \"hello\"",  # Type mismatch
        "Let colors be list containing 1, 2, 3\nDisplay colors at index \"first\"",  # Invalid index type
    ],
    
    "runtime_errors": [
        "Let x be 10 divided by 0",  # Division by zero
        "Let colors be list containing \"red\"\nDisplay colors at index 5",  # Index out of bounds
    ],
}

@pytest.fixture
def error_test_cases() -> Dict[str, List[str]]:
    """Provide test cases for various error conditions."""
    return ERROR_TEST_CASES 