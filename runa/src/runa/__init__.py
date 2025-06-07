"""
Runa Programming Language

A natural language programming language designed as AI agents' native thought language.
Runa bridges human thought patterns with machine execution through pseudocode-like
syntax that resembles natural language while maintaining computational precision.
"""

from ._version import __version__, __version_info__, get_version, get_version_info

# Week 1 completed components
from .lexer import RunaLexer, Token, TokenType
from .errors import RunaError, RunaSyntaxError, ErrorReporter, SourcePosition

__all__ = [
    # Version information
    "__version__",
    "__version_info__", 
    "get_version",
    "get_version_info",
    
    # Week 1 components
    "RunaLexer",
    "Token", 
    "TokenType",
    "RunaError",
    "RunaSyntaxError",
    "ErrorReporter",
    "SourcePosition",
]

# Package metadata
__author__ = "SyberSuite AI Development Team"
__email__ = "dev@sybersuite.ai" 
__license__ = "MIT"
__description__ = "Runa Programming Language - Natural language programming for AI agents"
__url__ = "https://github.com/sybersuite/runa"
