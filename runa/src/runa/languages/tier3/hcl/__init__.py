#!/usr/bin/env python3
"""
HCL Language Support for Runa Universal Translation System

This package provides comprehensive HCL language support including:
- HashiCorp Configuration Language parsing (HCL 1.0 and 2.0)
- Bidirectional HCL ↔ Runa AST conversion
- Clean HCL code generation with multiple style options
- Round-trip translation verification
- Terraform-specific constructs and validation
- Infrastructure-as-code pattern support
- Complete toolchain integration with Terraform CLI
"""

from .hcl_ast import *
from .hcl_parser import parse_hcl, HCLLexer, HCLParser
from .hcl_converter import hcl_to_runa, runa_to_hcl, HCLToRunaConverter, RunaToHCLConverter
from .hcl_generator import generate_hcl, HCLCodeGenerator, HCLFormatStyle, HCLFormatter
from .hcl_toolchain import (
    HCLToolchain,
    parse_hcl_code,
    generate_hcl_code,
    hcl_round_trip_verify,
    hcl_to_runa_translate,
    runa_to_hcl_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete HCL language toolchain for universal code translation"

# Main toolchain instance
toolchain = HCLToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "HCLToolchain",
    
    # Parser components
    "parse_hcl", "HCLLexer", "HCLParser",
    
    # Converters
    "hcl_to_runa", "runa_to_hcl", "HCLToRunaConverter", "RunaToHCLConverter",
    
    # Generator
    "generate_hcl", "HCLCodeGenerator", "HCLFormatStyle", "HCLFormatter",
    
    # Convenience functions
    "parse_hcl_code", "generate_hcl_code", "hcl_round_trip_verify",
    "hcl_to_runa_translate", "runa_to_hcl_translate",
    
    # AST base classes (main ones)
    "HCLNode", "HCLExpression", "HCLStatement", "HCLBlock", "HCLConfiguration",
]

# Module metadata
__language__ = "hcl"
__tier__ = 3
__file_extensions__ = [".hcl", ".tf", ".tfvars"]
__mime_types__ = ["application/x-hcl", "text/x-terraform"]
