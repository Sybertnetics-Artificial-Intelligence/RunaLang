"""
Tier 4 Languages - Domain-Specific Languages

Tier 4 includes specialized domain-specific languages for specific use cases
like data analysis, smart contracts, and API definitions.

Available Languages:
- R: Statistical computing and data analysis
- Julia: Scientific computing and high-performance numerical analysis
- Matlab: Matrix operations and mathematical computing
- GraphQL: API query language and schema definition
- Solidity: Smart contract development for Ethereum

Blockchain/Smart Contract Languages:
- Vyper: Python-like smart contract language for Ethereum
- Move: Resource-oriented programming language for blockchains (Facebook/Diem)
- Michelson: Stack-based smart contract language for Tezos
- Scilla: Functional smart contract language for Zilliqa
- SmartPy: Python-based smart contract language for Tezos
- LIGO: High-level smart contract language for Tezos
- Plutus: Haskell-based smart contract language for Cardano
- Pact: Human-readable smart contract language for Kadena
- Scrypto: Asset-oriented smart contract language for Radix DLT

Usage:
    from runa.languages.tier4 import get_r_toolchain, get_solidity_toolchain, get_scrypto_toolchain
    
    # Or import specific languages
    from runa.languages.tier4.r import toolchain as r_toolchain
    from runa.languages.tier4.scrypto import toolchain as scrypto_toolchain
"""

# Lazy imports to avoid loading all languages unless needed

# Original Tier 4 languages
def get_r_toolchain():
    """Get R language toolchain."""
    from .r import toolchain
    return toolchain

def get_julia_toolchain():
    """Get Julia language toolchain."""
    from .julia import toolchain
    return toolchain

def get_matlab_toolchain():
    """Get Matlab language toolchain."""
    from .matlab import toolchain
    return toolchain

def get_graphql_toolchain():
    """Get GraphQL language toolchain."""
    from .graphql import toolchain
    return toolchain

def get_solidity_toolchain():
    """Get Solidity language toolchain."""
    from .solidity import toolchain
    return toolchain

# Blockchain/Smart Contract languages
def get_vyper_toolchain():
    """Get Vyper language toolchain."""
    from .vyper import toolchain
    return toolchain

def get_move_toolchain():
    """Get Move language toolchain."""
    from .move import toolchain
    return toolchain

def get_michelson_toolchain():
    """Get Michelson language toolchain."""
    from .michelson import toolchain
    return toolchain

def get_scilla_toolchain():
    """Get Scilla language toolchain."""
    from .scilla import toolchain
    return toolchain

def get_smartpy_toolchain():
    """Get SmartPy language toolchain."""
    from .smartpy import toolchain
    return toolchain

def get_ligo_toolchain():
    """Get LIGO language toolchain."""
    from .ligo import toolchain
    return toolchain

def get_plutus_toolchain():
    """Get Plutus language toolchain."""
    from .plutus import toolchain
    return toolchain

def get_pact_toolchain():
    """Get Pact language toolchain."""
    from .pact import toolchain
    return toolchain

def get_scrypto_toolchain():
    """Get Scrypto language toolchain."""
    from .scrypto import toolchain
    return toolchain

# Direct toolchain access (lazy-loaded)
class _ToolchainProxy:
    """Proxy that lazy-loads toolchains on first access."""
    
    # Original languages
    @property
    def r(self):
        return get_r_toolchain()
    
    @property 
    def julia(self):
        return get_julia_toolchain()
        
    @property
    def matlab(self):
        return get_matlab_toolchain()
        
    @property
    def graphql(self):
        return get_graphql_toolchain()
        
    @property
    def solidity(self):
        return get_solidity_toolchain()
    
    # Blockchain languages
    @property
    def vyper(self):
        return get_vyper_toolchain()
    
    @property
    def move(self):
        return get_move_toolchain()
    
    @property
    def michelson(self):
        return get_michelson_toolchain()
    
    @property
    def scilla(self):
        return get_scilla_toolchain()
    
    @property
    def smartpy(self):
        return get_smartpy_toolchain()
    
    @property
    def ligo(self):
        return get_ligo_toolchain()
    
    @property
    def plutus(self):
        return get_plutus_toolchain()
    
    @property
    def pact(self):
        return get_pact_toolchain()
    
    @property
    def scrypto(self):
        return get_scrypto_toolchain()

# Main toolchain collection
toolchains = _ToolchainProxy()

# Convenience exports
__all__ = [
    "toolchains",
    # Original languages
    "get_r_toolchain",
    "get_julia_toolchain", 
    "get_matlab_toolchain",
    "get_graphql_toolchain",
    "get_solidity_toolchain",
    # Blockchain languages
    "get_vyper_toolchain",
    "get_move_toolchain",
    "get_michelson_toolchain",
    "get_scilla_toolchain",
    "get_smartpy_toolchain",
    "get_ligo_toolchain",
    "get_plutus_toolchain",
    "get_pact_toolchain",
    "get_scrypto_toolchain",
]

# Metadata
__tier__ = 4
__description__ = "Domain-specific languages for specialized computing and blockchain development"
__languages__ = [
    # Original languages
    "r", "julia", "matlab", "graphql", "solidity",
    # Blockchain/Smart Contract languages  
    "vyper", "move", "michelson", "scilla", "smartpy", 
    "ligo", "plutus", "pact", "scrypto"
]
