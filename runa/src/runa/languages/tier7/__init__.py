"""
Tier 7 Languages - Infrastructure & Toolchain Languages

Tier 7 includes build systems, hardware description languages, and development tools
for infrastructure and toolchain development.

Available Languages:
- Nix: Package management and system configuration
- Make: Build automation and dependency management  
- CMake: Cross-platform build system generator
- Bazel: Large-scale build and test system
- CUDA: GPU parallel computing (NVIDIA)
- OpenCL: Cross-platform parallel computing

Usage:
    from runa.languages.tier7 import get_nix_toolchain, get_bazel_toolchain
    
    # Or import specific languages
    from runa.languages.tier7.nix import toolchain as nix_toolchain
"""

# Lazy imports to avoid loading all languages unless needed
def get_nix_toolchain():
    """Get Nix toolchain instance"""
    from .nix import toolchain
    return toolchain

def get_make_toolchain():
    """Get Make toolchain instance"""
    from .make import toolchain
    return toolchain

def get_cmake_toolchain():
    """Get CMake toolchain instance"""
    from .cmake import toolchain
    return toolchain

def get_bazel_toolchain():
    """Get Bazel toolchain instance"""
    from .bazel import toolchain
    return toolchain

def get_cuda_toolchain():
    """Get CUDA toolchain instance"""
    from .cuda import toolchain
    return toolchain

def get_opencl_toolchain():
    """Get OpenCL toolchain instance"""
    from .opencl import toolchain
    return toolchain

# Toolchain registry for dynamic loading
_TOOLCHAIN_REGISTRY = {
    "nix": get_nix_toolchain,
    "make": get_make_toolchain,
    "cmake": get_cmake_toolchain,
    "bazel": get_bazel_toolchain,
    "cuda": get_cuda_toolchain,
    "opencl": get_opencl_toolchain,
}

def get_toolchain(language_name: str):
    """Get toolchain for a specific language"""
    if language_name.lower() in _TOOLCHAIN_REGISTRY:
        return _TOOLCHAIN_REGISTRY[language_name.lower()]()
    raise ValueError(f"Unknown tier 7 language: {language_name}")

def list_languages():
    """List all available tier 7 languages"""
    return list(_TOOLCHAIN_REGISTRY.keys())

__all__ = [
    "get_nix_toolchain",
    "get_make_toolchain", 
    "get_cmake_toolchain",
    "get_bazel_toolchain",
    "get_cuda_toolchain",
    "get_opencl_toolchain",
    "get_toolchain",
    "list_languages",
] 