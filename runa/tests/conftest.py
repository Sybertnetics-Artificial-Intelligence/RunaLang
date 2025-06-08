"""
Pytest configuration file for Runa tests.

This module contains fixtures and configuration for running the Runa test suite.
"""

import os
import sys
import pytest
from pathlib import Path

# Add the parent directory to the Python path so we can import the Runa modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def example_program():
    """
    Fixture that provides a simple Runa program for testing.
    
    Returns:
        A string containing a simple Runa program
    """
    return """
# This is a sample Runa program
Let user name be "John"
Let user age be 30

If user age is greater than 18:
    Display "Hello, " followed by user name
    Display "You are an adult."
Otherwise:
    Display "Hello, " followed by user name
    Display "You are not yet an adult."
"""


@pytest.fixture
def complex_program():
    """
    Fixture that provides a more complex Runa program for testing.
    
    Returns:
        A string containing a complex Runa program with various language features
    """
    return """
# A more complex Runa program with multiple features

# Define a function
Process called "Calculate Tax" that takes amount and tax rate (Number):
    Let tax be amount multiplied by tax rate
    Return tax

# Create a list
Let items be list containing "apple", "banana", "orange"

# Create a dictionary
Let prices be dictionary with:
    "apple" as 1.0
    "banana" as 0.5
    "orange" as 0.75

# Use a loop
Let total cost be 0

For each item in items:
    Let price be prices at index item
    Let item tax be Calculate Tax with:
        amount as price
        tax rate as 0.1
    Let item total be price plus item tax
    Set total cost to total cost plus item total
    Display item followed by " costs " followed by item total

Display "Total cost: " followed by total cost

# Error handling
Try:
    Let invalid item be prices at index "grape"
Catch error:
    Display "Error: " followed by error
"""


@pytest.fixture
def temp_dir(tmpdir):
    """
    Fixture that provides a temporary directory for file operations.
    
    Args:
        tmpdir: Pytest's tmpdir fixture
        
    Returns:
        A Path object representing the temporary directory
    """
    return Path(tmpdir)


@pytest.fixture
def create_runa_file(temp_dir):
    """
    Fixture that creates a Runa file with given content.
    
    Args:
        temp_dir: The temporary directory fixture
        
    Returns:
        A function that creates a Runa file with the given content
    """
    def _create_file(filename, content):
        file_path = temp_dir / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    return _create_file 