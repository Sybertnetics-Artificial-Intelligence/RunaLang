#!/usr/bin/env python3
"""
Runa Universal Translation Platform - Language System

This module provides unified access to the complete Runa Universal Translation Platform
supporting 65+ programming languages across 7 tiers.

## Language Tiers

**Tier 1 - Core Programming Languages (7 languages)**
Python, Java, JavaScript, TypeScript, C++, C#, SQL

**Tier 2 - Systems & Modern Backend Languages (7 languages)**  
Rust, Go, Swift, Kotlin, PHP, WebAssembly, Scala

**Tier 3 - Scripting & Interface Languages (11 languages)**
HTML, CSS, Shell, HCL, YAML, JSON, XML, Lua, TOML, INI, AssemblyScript

**Tier 4 - Domain-Specific Languages (14 languages)**
R, Julia, Matlab, GraphQL, Solidity + 9 blockchain languages

**Tier 5 - Academic & Functional Languages (10 languages)**
LISP, Haskell, Erlang, Elixir, OCaml, Clojure, Assembly, LLVM IR, Starlark, Rholang

**Tier 6 - Legacy & Enterprise Languages (7 languages)**
Objective-C, Visual Basic, COBOL, Ada, Perl, Fortran, Tcl

**Tier 7 - Infrastructure & Toolchain Languages (6 languages)**
Nix, Make, CMake, Bazel, CUDA, OpenCL

## Usage

    # Access by tier
    from runa.languages import tier1, tier4
    python_toolchain = tier1.toolchains.python
    solidity_toolchain = tier4.toolchains.solidity
    
    # Direct tier access
    from runa.languages import get_tier1, get_tier4
    tier1_module = get_tier1()
    tier4_module = get_tier4()

Total: 387 implementation files across 65 programming languages
"""

# Lazy tier imports to avoid loading unnecessary modules
def get_tier1():
    """Get Tier 1 (Core Programming Languages) module."""
    from . import tier1
    return tier1

def get_tier2():
    """Get Tier 2 (Systems & Modern Backend) module."""
    from . import tier2
    return tier2

def get_tier3():
    """Get Tier 3 (Scripting & Interface) module."""
    from . import tier3
    return tier3

def get_tier4():
    """Get Tier 4 (Domain-Specific) module."""
    from . import tier4
    return tier4

def get_tier5():
    """Get Tier 5 (Academic & Functional) module."""
    from . import tier5
    return tier5

def get_tier6():
    """Get Tier 6 (Legacy & Enterprise) module."""
    from . import tier6
    return tier6

def get_tier7():
    """Get Tier 7 (Infrastructure & Toolchain) module."""
    from . import tier7
    return tier7

def get_runa():
    """Get Runa language module."""
    from . import runa
    return runa

def get_shared():
    """Get shared utilities module."""
    from . import shared
    return shared

# Tier proxy for convenient access
class _TierProxy:
    """Proxy for convenient tier access."""
    
    @property
    def tier1(self):
        """Access Tier 1 languages."""
        return get_tier1()
    
    @property
    def tier2(self):
        """Access Tier 2 languages."""
        return get_tier2()
    
    @property
    def tier3(self):
        """Access Tier 3 languages."""
        return get_tier3()
    
    @property
    def tier4(self):
        """Access Tier 4 languages."""
        return get_tier4()
    
    @property
    def tier5(self):
        """Access Tier 5 languages."""
        return get_tier5()
    
    @property
    def tier6(self):
        """Access Tier 6 languages."""
        return get_tier6()
    
    @property
    def tier7(self):
        """Access Tier 7 languages."""
        return get_tier7()
    
    @property
    def runa(self):
        """Access Runa language."""
        return get_runa()
    
    @property
    def shared(self):
        """Access shared utilities."""
        return get_shared()

# Main interface objects
tiers = _TierProxy()

# Convenience aliases for direct access
tier1 = tiers.tier1
tier2 = tiers.tier2  
tier3 = tiers.tier3
tier4 = tiers.tier4
tier5 = tiers.tier5
tier6 = tiers.tier6
tier7 = tiers.tier7
runa = tiers.runa
shared = tiers.shared

# Main exports
__all__ = [
    # Tier access
    "tiers", "tier1", "tier2", "tier3", "tier4", "tier5", "tier6", "tier7",
    "runa", "shared",
    
    # Tier getters
    "get_tier1", "get_tier2", "get_tier3", "get_tier4", 
    "get_tier5", "get_tier6", "get_tier7", "get_runa", "get_shared"
]

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Universal Programming Language Translation Platform"
__languages_count__ = 65
__tiers_count__ = 7
__files_count__ = 387