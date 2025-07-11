"""
Tier 3 Languages - Scripting & Interface Languages

Tier 3 includes markup, configuration, shell scripting, and automation languages
that are critical for DevOps and web development.

Available Languages:
- HTML: Web markup and structure
- CSS: Web styling and presentation
- Shell: Unix/Linux shell scripting (Bash, Zsh)
- HCL: HashiCorp Configuration Language (Terraform)
- YAML: Configuration files and data serialization
- JSON: Data interchange and configuration
- XML: Structured data and configuration
- Lua: Embedded scripting and configuration
- TOML: Configuration file format
- INI: Simple configuration files
- AssemblyScript: TypeScript-to-WebAssembly compiler

Usage:
    from runa.languages.tier3 import get_html_toolchain, get_yaml_toolchain
    
    # Or import specific languages
    from runa.languages.tier3.html import toolchain as html_toolchain
"""

# Lazy imports to avoid loading all languages unless needed
def get_html_toolchain():
    """Get HTML toolchain instance"""
    from .html import toolchain
    return toolchain

def get_css_toolchain():
    """Get CSS toolchain instance"""
    from .css import toolchain
    return toolchain

def get_shell_toolchain():
    """Get Shell toolchain instance"""
    from .shell import toolchain
    return toolchain

def get_hcl_toolchain():
    """Get HCL toolchain instance"""
    from .hcl import toolchain
    return toolchain

def get_yaml_toolchain():
    """Get YAML toolchain instance"""
    from .yaml import toolchain
    return toolchain

def get_json_toolchain():
    """Get JSON toolchain instance"""
    from .json import toolchain
    return toolchain

def get_xml_toolchain():
    """Get XML toolchain instance"""
    from .xml import toolchain
    return toolchain

def get_lua_toolchain():
    """Get Lua toolchain instance"""
    from .lua import toolchain
    return toolchain

def get_toml_toolchain():
    """Get TOML toolchain instance"""
    from .toml import toolchain
    return toolchain

def get_ini_toolchain():
    """Get INI toolchain instance"""
    from .ini import toolchain
    return toolchain

def get_assemblyscript_toolchain():
    """Get AssemblyScript toolchain instance"""
    from .assemblyscript import toolchain
    return toolchain

# Toolchain registry for dynamic loading
_TOOLCHAIN_REGISTRY = {
    "html": get_html_toolchain,
    "css": get_css_toolchain,
    "shell": get_shell_toolchain,
    "hcl": get_hcl_toolchain,
    "yaml": get_yaml_toolchain,
    "json": get_json_toolchain,
    "xml": get_xml_toolchain,
    "lua": get_lua_toolchain,
    "toml": get_toml_toolchain,
    "ini": get_ini_toolchain,
    "assemblyscript": get_assemblyscript_toolchain,
}

def get_toolchain(language_name: str):
    """Get toolchain for a specific language"""
    if language_name.lower() in _TOOLCHAIN_REGISTRY:
        return _TOOLCHAIN_REGISTRY[language_name.lower()]()
    raise ValueError(f"Unknown tier 3 language: {language_name}")

def list_languages():
    """List all available tier 3 languages"""
    return list(_TOOLCHAIN_REGISTRY.keys())

__all__ = [
    "get_html_toolchain",
    "get_css_toolchain",
    "get_shell_toolchain",
    "get_hcl_toolchain",
    "get_yaml_toolchain",
    "get_json_toolchain",
    "get_xml_toolchain",
    "get_lua_toolchain",
    "get_toml_toolchain",
    "get_ini_toolchain",
    "get_assemblyscript_toolchain",
    "get_toolchain",
    "list_languages",
]
