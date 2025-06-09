"""
Input/Output module for Runa Standard Library.

This module provides functions for file operations, streaming, and 
other input/output capabilities.
"""

from .file import register_file_functions
from .stream import register_stream_functions

__all__ = [
    'register_file_functions',
    'register_stream_functions'
] 