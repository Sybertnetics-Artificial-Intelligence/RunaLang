"""
Tier 6 Languages - Legacy & Enterprise Languages

Tier 6 includes legacy and enterprise programming languages that are critical
for maintaining compatibility with older systems, government applications,
and specialized enterprise environments.

Available Languages:
- Objective-C: Legacy iOS/macOS development and Apple ecosystem integration
- Visual Basic: Microsoft legacy applications and enterprise systems
- COBOL: Mainframe and legacy enterprise business systems
- Ada: Safety-critical and defense systems requiring high reliability
- Perl: Text processing and legacy web development systems
- Fortran: Scientific computing and engineering legacy systems
- Tcl: Tool command language, automation, and scripting systems

Usage:
    from runa.languages.tier6 import get_objective_c_toolchain, get_cobol_toolchain
    
    # Or import specific languages
    from runa.languages.tier6.objective_c import toolchain as objc_toolchain
    from runa.languages.tier6.cobol import toolchain as cobol_toolchain
"""

# Lazy imports to avoid loading all languages unless needed
def get_objective_c_toolchain():
    """Get Objective-C language toolchain."""
    from .objective_c import toolchain
    return toolchain

def get_visual_basic_toolchain():
    """Get Visual Basic language toolchain."""
    from .visual_basic import toolchain
    return toolchain

def get_cobol_toolchain():
    """Get COBOL language toolchain."""
    from .cobol import toolchain
    return toolchain

def get_ada_toolchain():
    """Get Ada language toolchain."""
    from .ada import toolchain
    return toolchain

def get_perl_toolchain():
    """Get Perl language toolchain."""
    from .perl import toolchain
    return toolchain

def get_fortran_toolchain():
    """Get Fortran language toolchain."""
    from .fortran import toolchain
    return toolchain

def get_tcl_toolchain():
    """Get Tcl language toolchain."""
    from .tcl import toolchain
    return toolchain

# Direct toolchain access (lazy-loaded)
class _ToolchainProxy:
    """Proxy that lazy-loads toolchains on first access."""
    
    @property
    def objective_c(self):
        return get_objective_c_toolchain()
    
    @property 
    def visual_basic(self):
        return get_visual_basic_toolchain()
        
    @property
    def cobol(self):
        return get_cobol_toolchain()
        
    @property
    def ada(self):
        return get_ada_toolchain()
        
    @property
    def perl(self):
        return get_perl_toolchain()
    
    @property
    def fortran(self):
        return get_fortran_toolchain()
    
    @property
    def tcl(self):
        return get_tcl_toolchain()

# Main toolchain collection
toolchains = _ToolchainProxy()

# Convenience exports
__all__ = [
    "toolchains",
    "get_objective_c_toolchain",
    "get_visual_basic_toolchain", 
    "get_cobol_toolchain",
    "get_ada_toolchain",
    "get_perl_toolchain",
    "get_fortran_toolchain",
    "get_tcl_toolchain",
]

# Metadata
__tier__ = 6
__description__ = "Legacy and enterprise languages for critical system maintenance and modernization"
__languages__ = ["objective_c", "visual_basic", "cobol", "ada", "perl", "fortran", "tcl"]
