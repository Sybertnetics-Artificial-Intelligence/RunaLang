"""
Tier 5 Languages - Academic & Functional Languages

Tier 5 includes research, functional programming, and low-level system languages
for academic applications and specialized development.

Available Languages:
- LISP: Symbolic computation and AI research
- Haskell: Pure functional programming
- Erlang/Elixir: Actor-based concurrent systems
- OCaml: Functional programming with objects
- Clojure: Lisp dialect on the JVM
- Assembly: Low-level processor instruction programming
- LLVM IR: Low-level intermediate representation
- Starlark: Configuration language (Bazel, Copybara)
- Rholang: RChain blockchain language

Usage:
    from runa.languages.tier5 import get_haskell_toolchain, get_lisp_toolchain
    
    # Or import specific languages
    from runa.languages.tier5.haskell import toolchain as haskell_toolchain
"""

# Lazy imports to avoid loading all languages unless needed
def get_lisp_toolchain():
    """Get LISP toolchain instance"""
    from .lisp import toolchain
    return toolchain

def get_haskell_toolchain():
    """Get Haskell toolchain instance"""
    from .haskell import toolchain
    return toolchain

def get_erlang_toolchain():
    """Get Erlang toolchain instance"""
    from .erlang import toolchain
    return toolchain

def get_elixir_toolchain():
    """Get Elixir toolchain instance"""
    from .elixir import toolchain
    return toolchain

def get_ocaml_toolchain():
    """Get OCaml toolchain instance"""
    from .ocaml import toolchain
    return toolchain

def get_clojure_toolchain():
    """Get Clojure toolchain instance"""
    from .clojure import toolchain
    return toolchain

def get_assembly_toolchain():
    """Get Assembly toolchain instance"""
    from .assembly import toolchain
    return toolchain

def get_llvm_ir_toolchain():
    """Get LLVM IR toolchain instance"""
    from .llvm_ir import toolchain
    return toolchain

def get_starlark_toolchain():
    """Get Starlark toolchain instance"""
    from .starlark import toolchain
    return toolchain

def get_rholang_toolchain():
    """Get Rholang toolchain instance"""
    from .rholang import toolchain
    return toolchain

# Toolchain registry for dynamic loading
_TOOLCHAIN_REGISTRY = {
    "lisp": get_lisp_toolchain,
    "haskell": get_haskell_toolchain,
    "erlang": get_erlang_toolchain,
    "elixir": get_elixir_toolchain,
    "ocaml": get_ocaml_toolchain,
    "clojure": get_clojure_toolchain,
    "assembly": get_assembly_toolchain,
    "llvm_ir": get_llvm_ir_toolchain,
    "starlark": get_starlark_toolchain,
    "rholang": get_rholang_toolchain,
}

def get_toolchain(language_name: str):
    """Get toolchain for a specific language"""
    if language_name.lower() in _TOOLCHAIN_REGISTRY:
        return _TOOLCHAIN_REGISTRY[language_name.lower()]()
    raise ValueError(f"Unknown tier 5 language: {language_name}")

def list_languages():
    """List all available tier 5 languages"""
    return list(_TOOLCHAIN_REGISTRY.keys())

__all__ = [
    "get_lisp_toolchain",
    "get_haskell_toolchain",
    "get_erlang_toolchain",
    "get_elixir_toolchain",
    "get_ocaml_toolchain",
    "get_clojure_toolchain",
    "get_assembly_toolchain",
    "get_llvm_ir_toolchain",
    "get_starlark_toolchain",
    "get_rholang_toolchain",
    "get_toolchain",
    "list_languages",
]
