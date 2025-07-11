"""
Tier 2 Languages - Systems & Modern Backend Languages

Tier 2 includes systems programming and performant server-side development languages
that are essential for modern development workflows.

Available Languages:
- Rust: Memory-safe systems programming
- Go: Cloud services, microservices, DevOps tools
- Swift: iOS/macOS development, systems programming
- Kotlin: Android development, multiplatform applications
- PHP: Web development, server-side scripting
- WebAssembly: High-performance web applications
- Scala: JVM-based functional programming

Usage:
    from runa.languages.tier2 import get_rust_toolchain, get_go_toolchain
    
    # Or import specific languages
    from runa.languages.tier2.rust import toolchain as rust_toolchain
"""

# Lazy imports to avoid loading all languages unless needed
def get_rust_toolchain():
    """Get Rust toolchain instance"""
    from .rust import toolchain
    return toolchain

def get_go_toolchain():
    """Get Go toolchain instance"""
    from .go import toolchain
    return toolchain

def get_swift_toolchain():
    """Get Swift toolchain instance"""
    from .swift import toolchain
    return toolchain

def get_kotlin_toolchain():
    """Get Kotlin toolchain instance"""
    from .kotlin import toolchain
    return toolchain

def get_php_toolchain():
    """Get PHP toolchain instance"""
    from .php import toolchain
    return toolchain

def get_webassembly_toolchain():
    """Get WebAssembly toolchain instance"""
    from .webassembly import toolchain
    return toolchain

def get_scala_toolchain():
    """Get Scala toolchain instance"""
    from .scala import toolchain
    return toolchain

# Toolchain registry for dynamic loading
_TOOLCHAIN_REGISTRY = {
    "rust": get_rust_toolchain,
    "go": get_go_toolchain,
    "swift": get_swift_toolchain,
    "kotlin": get_kotlin_toolchain,
    "php": get_php_toolchain,
    "webassembly": get_webassembly_toolchain,
    "scala": get_scala_toolchain,
}

def get_toolchain(language_name: str):
    """Get toolchain for a specific language"""
    if language_name.lower() in _TOOLCHAIN_REGISTRY:
        return _TOOLCHAIN_REGISTRY[language_name.lower()]()
    raise ValueError(f"Unknown tier 2 language: {language_name}")

def list_languages():
    """List all available tier 2 languages"""
    return list(_TOOLCHAIN_REGISTRY.keys())

__all__ = [
    "get_rust_toolchain",
    "get_go_toolchain",
    "get_swift_toolchain", 
    "get_kotlin_toolchain",
    "get_php_toolchain",
    "get_webassembly_toolchain",
    "get_scala_toolchain",
    "get_toolchain",
    "list_languages",
]
