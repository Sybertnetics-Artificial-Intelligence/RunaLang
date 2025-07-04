"""
Code Generation Package for Runa Compiler

This package contains code generators for different target languages.
Currently supports:
- Python (primary target for MVP)

Future targets planned:
- JavaScript/TypeScript
- WebAssembly
- C/C++
"""

from .python_generator import PythonCodeGenerator

__all__ = ['PythonCodeGenerator'] 