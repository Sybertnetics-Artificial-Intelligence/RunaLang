#!/usr/bin/env python3
"""
XML Language Support for Runa

Complete XML toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .xml_ast import *
from .xml_parser import parse_xml, parse_xml_file, parse_xml_fragment, XmlLexer, XmlParser
from .xml_converter import xml_to_runa, runa_to_xml, XmlToRunaConverter, RunaToXmlConverter
from .xml_generator import generate_xml_code, XmlCodeGenerator, XmlCodeStyle, XmlFormatter
from .xml_toolchain import (
    XmlToolchain,
    create_xml_toolchain,
    xml_to_runa_translation,
    runa_to_xml_translation,
    verify_xml_round_trip,
    parse_xml_code,
    generate_xml_code_from_ast
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete XML language toolchain for universal code translation"

# Main toolchain instance
toolchain = XmlToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "XmlToolchain",
    
    # Parser components
    "parse_xml", "parse_xml_file", "parse_xml_fragment", "XmlLexer", "XmlParser",
    
    # Converters
    "xml_to_runa", "runa_to_xml", "XmlToRunaConverter", "RunaToXmlConverter",
    
    # Generator
    "generate_xml_code", "XmlCodeGenerator", "XmlCodeStyle", "XmlFormatter",
    
    # Convenience functions
    "create_xml_toolchain", "xml_to_runa_translation", "runa_to_xml_translation",
    "verify_xml_round_trip", "parse_xml_code", "generate_xml_code_from_ast",
    
    # AST base classes (main ones)
    "XmlNode", "XmlDocument", "XmlElement", "XmlText", "XmlComment", "XmlCData",
]

# Module metadata
__language__ = "xml"
__tier__ = 3
__file_extensions__ = [".xml", ".xhtml", ".svg", ".xsl", ".xslt"]
__mime_types__ = ["application/xml", "text/xml", "application/xhtml+xml"]