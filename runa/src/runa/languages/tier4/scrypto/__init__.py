"""
Scrypto language support for the Runa Universal Translation Pipeline.

Scrypto is Radix DLT's asset-oriented smart contract language designed for
building secure and scalable decentralized finance (DeFi) applications.
Built on Rust with native asset handling and component-based architecture.

Key Features:
- Asset-oriented programming paradigm
- Component-based smart contract architecture  
- Blueprint system for reusable contract templates
- Native resource management (tokens, NFTs, badges)
- Bucket and Vault system for safe asset handling
- Badge-based authentication and authorization
- SBOR (Structured Binary Object Representation) encoding
- Radix Engine integration for optimal performance
- Formal verification capabilities

This module provides:
- ScryptoAST: Complete AST representation for Scrypto smart contracts
- ScryptoParser: Parser for Rust-based Scrypto syntax with asset extensions
- ScryptoConverter: Bidirectional conversion between Scrypto and Runa AST
- ScryptoGenerator: Code generation for idiomatic Scrypto contracts
- ScryptoToolchain: Integrated development, testing, and deployment tools
"""

from .scrypto_ast import ScryptoAST
from .scrypto_parser import ScryptoParser
from .scrypto_converter import ScryptoConverter
from .scrypto_generator import ScryptoGenerator
from .scrypto_toolchain import ScryptoToolchain

__all__ = [
    'ScryptoAST',
    'ScryptoParser',
    'ScryptoConverter', 
    'ScryptoGenerator',
    'ScryptoToolchain'
]

# Language metadata
LANGUAGE_NAME = "scrypto"
LANGUAGE_VERSION = "1.3.0"
LANGUAGE_DESCRIPTION = "Radix DLT's asset-oriented smart contract language"
SUPPORTED_FEATURES = [
    "smart_contracts",
    "asset_oriented_programming",
    "component_architecture",
    "blueprint_system",
    "native_resources",
    "bucket_vault_system", 
    "badge_authentication",
    "sbor_encoding",
    "radix_engine_integration",
    "formal_verification",
    "rust_based"
]
