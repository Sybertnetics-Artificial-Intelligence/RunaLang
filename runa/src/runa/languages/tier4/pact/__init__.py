"""
Pact language support for the Runa Universal Translation Pipeline.

Pact is Kadena's smart contract language designed for high-level programming 
with formal verification capabilities. It features LISP-like syntax with
built-in support for capabilities, keysets, and human-readable contracts.

Key Features:
- LISP-like syntax with S-expressions
- Formal verification and theorem proving
- Capability-based security model
- Human-readable contract code
- Built-in testing framework
- Multi-sig and keyset management

This module provides:
- PactAST: Complete AST representation for Pact smart contracts
- PactParser: Parser for LISP-like Pact syntax
- PactConverter: Bidirectional conversion between Pact and Runa AST
- PactGenerator: Code generation for idiomatic Pact contracts
- PactToolchain: Integrated development and deployment tools
"""

from .pact_ast import PactAST
from .pact_parser import PactParser
from .pact_converter import PactConverter
from .pact_generator import PactGenerator  
from .pact_toolchain import PactToolchain

__all__ = [
    'PactAST',
    'PactParser', 
    'PactConverter',
    'PactGenerator',
    'PactToolchain'
]

# Language metadata
LANGUAGE_NAME = "pact"
LANGUAGE_VERSION = "4.9"
LANGUAGE_DESCRIPTION = "Kadena's formal verification smart contract language"
SUPPORTED_FEATURES = [
    "smart_contracts",
    "formal_verification", 
    "capabilities",
    "keysets",
    "lisp_syntax",
    "testing_framework",
    "multi_sig"
]
