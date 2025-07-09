"""
Tier 1 Languages - Core Programming Languages

Tier 1 includes the most important and widely-used programming languages
that form the foundation of modern software development.

Available Languages:
- Python: Modern Python with type hints and async support
- Java: Enterprise Java with modern features  
- JavaScript: Modern ECMAScript with ES6+ features
- TypeScript: TypeScript with advanced type system
- C++: Modern C++ with C++11/14/17/20 features
- C#: Modern C# with .NET features and nullable types
- SQL: Multi-dialect SQL with ANSI compliance

Usage:
    from runa.languages.tier1 import PythonToolchain, JavaToolchain
    
    # Or import specific languages
    from runa.languages.tier1.python import toolchain as python_toolchain
"""

# Lazy imports to avoid loading all languages unless needed
def get_python_toolchain():
    """Get Python language toolchain."""
    from .python import toolchain
    return toolchain

def get_java_toolchain():
    """Get Java language toolchain."""
    from .java import toolchain
    return toolchain

def get_javascript_toolchain():
    """Get JavaScript language toolchain."""
    from .javascript import toolchain
    return toolchain

def get_typescript_toolchain():
    """Get TypeScript language toolchain."""
    from .typescript import toolchain
    return toolchain

def get_cpp_toolchain():
    """Get C++ language toolchain."""
    from .cpp import toolchain
    return toolchain

def get_csharp_toolchain():
    """Get C# language toolchain."""
    from .csharp import toolchain
    return toolchain

def get_sql_toolchain():
    """Get SQL language toolchain."""
    from .sql import toolchain
    return toolchain

# Direct toolchain access (lazy-loaded)
class _ToolchainProxy:
    """Proxy that lazy-loads toolchains on first access."""
    
    @property
    def python(self):
        return get_python_toolchain()
    
    @property 
    def java(self):
        return get_java_toolchain()
        
    @property
    def javascript(self):
        return get_javascript_toolchain()
        
    @property
    def typescript(self):
        return get_typescript_toolchain()
        
    @property
    def cpp(self):
        return get_cpp_toolchain()
        
    @property
    def csharp(self):
        return get_csharp_toolchain()
        
    @property
    def sql(self):
        return get_sql_toolchain()

# Main toolchain collection
toolchains = _ToolchainProxy()

# Convenience exports
__all__ = [
    "toolchains",
    "get_python_toolchain",
    "get_java_toolchain", 
    "get_javascript_toolchain",
    "get_typescript_toolchain",
    "get_cpp_toolchain",
    "get_csharp_toolchain",
    "get_sql_toolchain",
]

# Metadata
__tier__ = 1
__description__ = "Core programming languages - the foundation of modern software development"
__languages__ = ["python", "java", "javascript", "typescript", "cpp", "csharp", "sql"]
