"""
Base Components for Language Toolchains

This module provides base classes and utilities for implementing language-specific
toolchains in the hub-and-spoke system. All 32 languages should extend these
base classes to ensure consistency and proper integration.

Key Features:
- Abstract base classes for parsers, converters, and generators
- Common utilities for all language implementations
- Error handling and logging support
- Metadata and location tracking
- Validation and testing support
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, Set
from dataclasses import dataclass, field
from enum import Enum, auto
import logging
import re
from pathlib import Path

from .runa_ast import ASTNode, SourceLocation, TranslationMetadata


class LanguageTier(Enum):
    """Language tiers for priority and complexity classification."""
    TIER1 = "tier1"  # Core Enterprise/Web: JavaScript, TypeScript, Python, C++, Java, C#, SQL
    TIER2 = "tier2"  # Modern Systems: Rust, Go, Swift, Kotlin, PHP, WebAssembly
    TIER3 = "tier3"  # Configuration/Markup: HTML, CSS, Shell, HCL, YAML, JSON, XML
    TIER4 = "tier4"  # Specialized Domain: R, MATLAB, Julia, Solidity, GraphQL
    TIER5 = "tier5"  # Academic/Functional: LISP, Haskell, Erlang/Elixir, LLVM IR, Assembly
    TIER6 = "tier6"  # Legacy/Niche: Objective-C, VB, COBOL, Ada, Perl, Fortran


@dataclass
class LanguageInfo:
    """Information about a programming language."""
    name: str
    tier: LanguageTier
    file_extensions: List[str]
    mime_types: List[str] = field(default_factory=list)
    description: str = ""
    version: str = "1.0.0"
    documentation_url: str = ""
    
    # Language characteristics
    is_compiled: bool = True
    is_interpreted: bool = False
    is_markup: bool = False
    is_config: bool = False
    is_functional: bool = False
    is_object_oriented: bool = True
    has_static_typing: bool = False
    has_dynamic_typing: bool = True
    
    # Common syntax patterns (regex)
    comment_patterns: List[str] = field(default_factory=list)
    string_patterns: List[str] = field(default_factory=list)
    number_patterns: List[str] = field(default_factory=list)
    identifier_patterns: List[str] = field(default_factory=list)


class ParseError(Exception):
    """Exception raised during parsing."""
    def __init__(self, message: str, location: Optional[SourceLocation] = None):
        self.message = message
        self.location = location
        super().__init__(message)


class ConversionError(Exception):
    """Exception raised during AST conversion."""
    def __init__(self, message: str, node: Optional[ASTNode] = None):
        self.message = message
        self.node = node
        super().__init__(message)


class GenerationError(Exception):
    """Exception raised during code generation."""
    def __init__(self, message: str, node: Optional[ASTNode] = None):
        self.message = message
        self.node = node
        super().__init__(message)


class BaseLanguageParser(ABC):
    """
    Abstract base class for all language-specific parsers.
    
    Parsers are responsible for:
    - Reading source code text
    - Tokenizing and parsing according to language grammar
    - Creating language-specific AST nodes
    - Tracking source locations for debugging
    - Handling parse errors gracefully
    """
    
    def __init__(self, language_info: LanguageInfo):
        self.language_info = language_info
        self.logger = logging.getLogger(f"runa.parser.{language_info.name}")
        self._current_file_path = ""
    
    @abstractmethod
    def parse(self, source_code: str, file_path: str = "") -> ASTNode:
        """
        Parse source code into a language-specific AST.
        
        Args:
            source_code: The source code to parse
            file_path: Path to the source file (for error reporting)
            
        Returns:
            Language-specific AST root node
            
        Raises:
            ParseError: If parsing fails
        """
        pass
    
    def parse_file(self, file_path: str) -> ASTNode:
        """Parse a source file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            return self.parse(source_code, file_path)
        except Exception as e:
            raise ParseError(f"Failed to parse file {file_path}: {e}")
    
    def validate_source_code(self, source_code: str) -> List[str]:
        """
        Validate source code without full parsing.
        Returns list of validation errors.
        """
        errors = []
        
        # Basic validation (can be overridden by subclasses)
        if not source_code.strip():
            errors.append("Empty source code")
        
        return errors
    
    def extract_metadata(self, source_code: str) -> Dict[str, Any]:
        """Extract metadata from source code (comments, annotations, etc.)."""
        metadata = {}
        
        # Extract basic information
        metadata["line_count"] = len(source_code.splitlines())
        metadata["character_count"] = len(source_code)
        metadata["language"] = self.language_info.name
        
        # Extract comments (if patterns are defined)
        if self.language_info.comment_patterns:
            comments = []
            for pattern in self.language_info.comment_patterns:
                matches = re.findall(pattern, source_code, re.MULTILINE)
                comments.extend(matches)
            metadata["comments"] = comments
        
        return metadata
    
    def create_location(self, line: int, column: int, end_line: int = 0, 
                       end_column: int = 0) -> SourceLocation:
        """Create a source location for the current file."""
        return SourceLocation(
            file_path=self._current_file_path,
            line=line,
            column=column,
            end_line=end_line or line,
            end_column=end_column or column
        )


class BaseLanguageConverter(ABC):
    """
    Abstract base class for bidirectional AST converters.
    
    Converters are responsible for:
    - Converting language-specific AST to Runa AST
    - Converting Runa AST to language-specific AST
    - Preserving semantic meaning during conversion
    - Tracking translation metadata
    - Handling conversion errors gracefully
    """
    
    def __init__(self, language_info: LanguageInfo):
        self.language_info = language_info
        self.logger = logging.getLogger(f"runa.converter.{language_info.name}")
    
    @abstractmethod
    def to_runa_ast(self, language_ast: ASTNode) -> ASTNode:
        """
        Convert language-specific AST to Runa AST.
        
        Args:
            language_ast: Language-specific AST root node
            
        Returns:
            Runa AST root node
            
        Raises:
            ConversionError: If conversion fails
        """
        pass
    
    @abstractmethod
    def from_runa_ast(self, runa_ast: ASTNode) -> ASTNode:
        """
        Convert Runa AST to language-specific AST.
        
        Args:
            runa_ast: Runa AST root node
            
        Returns:
            Language-specific AST root node
            
        Raises:
            ConversionError: If conversion fails
        """
        pass
    
    def create_translation_metadata(self, source_language: str = "", 
                                  target_language: str = "") -> TranslationMetadata:
        """Create translation metadata for converted nodes."""
        return TranslationMetadata(
            source_language=source_language or self.language_info.name,
            target_language=target_language,
            confidence_score=1.0  # Can be adjusted based on conversion complexity
        )
    
    def validate_conversion(self, original: ASTNode, converted: ASTNode) -> List[str]:
        """
        Validate that conversion preserves semantic meaning.
        Returns list of validation warnings.
        """
        warnings = []
        
        # Basic validation - can be extended by subclasses
        if not isinstance(converted, ASTNode):
            warnings.append("Converted result is not an ASTNode")
        
        return warnings


class BaseLanguageGenerator(ABC):
    """
    Abstract base class for language-specific code generators.
    
    Generators are responsible for:
    - Converting language-specific AST back to source code
    - Producing well-formatted, idiomatic code
    - Preserving comments and formatting where possible
    - Handling generation errors gracefully
    """
    
    def __init__(self, language_info: LanguageInfo):
        self.language_info = language_info
        self.logger = logging.getLogger(f"runa.generator.{language_info.name}")
        
        # Code formatting settings
        self.indent_size = 4
        self.use_tabs = False
        self.line_ending = "\n"
        self.max_line_length = 100
    
    @abstractmethod
    def generate(self, language_ast: ASTNode) -> str:
        """
        Generate source code from language-specific AST.
        
        Args:
            language_ast: Language-specific AST root node
            
        Returns:
            Generated source code
            
        Raises:
            GenerationError: If generation fails
        """
        pass
    
    def generate_to_file(self, language_ast: ASTNode, file_path: str) -> None:
        """Generate source code and write to file."""
        try:
            source_code = self.generate(language_ast)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(source_code)
        except Exception as e:
            raise GenerationError(f"Failed to generate file {file_path}: {e}")
    
    def format_code(self, source_code: str) -> str:
        """
        Format generated source code.
        Can be overridden by subclasses for language-specific formatting.
        """
        # Basic formatting - remove excessive whitespace
        lines = source_code.splitlines()
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            if line or formatted_lines:  # Avoid leading empty lines
                formatted_lines.append(line)
        
        # Ensure single trailing newline
        return self.line_ending.join(formatted_lines) + self.line_ending
    
    def get_indent(self, level: int) -> str:
        """Get indentation string for the given level."""
        if self.use_tabs:
            return "\t" * level
        else:
            return " " * (self.indent_size * level)


class LanguageToolchainValidator:
    """Validator for language toolchains."""
    
    @staticmethod
    def validate_parser(parser: BaseLanguageParser, test_code: str) -> Dict[str, Any]:
        """Validate a parser with test code."""
        try:
            ast = parser.parse(test_code, "test.code")
            return {
                "success": True,
                "ast_type": type(ast).__name__,
                "node_count": len(ast.get_descendants()) if hasattr(ast, 'get_descendants') else 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    @staticmethod
    def validate_converter(converter: BaseLanguageConverter, test_ast: ASTNode) -> Dict[str, Any]:
        """Validate a converter with test AST."""
        try:
            # Test both directions
            runa_ast = converter.to_runa_ast(test_ast)
            back_to_lang = converter.from_runa_ast(runa_ast)
            
            return {
                "success": True,
                "to_runa_type": type(runa_ast).__name__,
                "from_runa_type": type(back_to_lang).__name__,
                "round_trip_success": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    @staticmethod
    def validate_generator(generator: BaseLanguageGenerator, test_ast: ASTNode) -> Dict[str, Any]:
        """Validate a generator with test AST."""
        try:
            generated_code = generator.generate(test_ast)
            formatted_code = generator.format_code(generated_code)
            
            return {
                "success": True,
                "code_length": len(generated_code),
                "formatted_length": len(formatted_code),
                "line_count": len(generated_code.splitlines())
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }


class LanguageToolchainTemplate:
    """Template generator for new language toolchains."""
    
    @staticmethod
    def generate_parser_template(language_info: LanguageInfo) -> str:
        """Generate a parser template for a language."""
        return f'''"""
{language_info.name} Parser

Parses {language_info.name} source code into language-specific AST.
"""

from typing import List, Optional
from runa.core.base_components import BaseLanguageParser, ParseError
from runa.core.runa_ast import ASTNode, SourceLocation

# Import language-specific AST nodes
from .{language_info.name.lower()}_ast import *


class {language_info.name.title()}Parser(BaseLanguageParser):
    """Parser for {language_info.name} programming language."""
    
    def parse(self, source_code: str, file_path: str = "") -> ASTNode:
        """Parse {language_info.name} source code into AST."""
        self._current_file_path = file_path
        
        try:
            # TODO: Implement actual parsing logic
            # This is a template - replace with real implementation
            
            # 1. Tokenize source code
            tokens = self._tokenize(source_code)
            
            # 2. Parse tokens into AST
            ast = self._parse_tokens(tokens)
            
            return ast
            
        except Exception as e:
            raise ParseError(f"Failed to parse {language_info.name} code: {{e}}")
    
    def _tokenize(self, source_code: str) -> List[str]:
        """Tokenize source code - IMPLEMENT THIS."""
        # TODO: Implement tokenization
        return []
    
    def _parse_tokens(self, tokens: List[str]) -> ASTNode:
        """Parse tokens into AST - IMPLEMENT THIS."""
        # TODO: Implement parsing
        raise NotImplementedError("Parser implementation needed")
'''
    
    @staticmethod
    def generate_converter_template(language_info: LanguageInfo) -> str:
        """Generate a converter template for a language."""
        return f'''"""
{language_info.name} AST Converter

Converts between {language_info.name}-specific AST and Runa AST.
"""

from typing import Dict, Any
from runa.core.base_components import BaseLanguageConverter, ConversionError
from runa.core.runa_ast import ASTNode

# Import language-specific and Runa AST nodes
from .{language_info.name.lower()}_ast import *
from runa.core.runa_ast import *


class {language_info.name.title()}Converter(BaseLanguageConverter):
    """Bidirectional converter for {language_info.name} and Runa ASTs."""
    
    def to_runa_ast(self, language_ast: ASTNode) -> ASTNode:
        """Convert {language_info.name} AST to Runa AST."""
        try:
            # TODO: Implement {language_info.name} -> Runa conversion
            # This should map {language_info.name}-specific nodes to Runa nodes
            
            return self._convert_to_runa(language_ast)
            
        except Exception as e:
            raise ConversionError(f"Failed to convert {language_info.name} AST to Runa: {{e}}")
    
    def from_runa_ast(self, runa_ast: ASTNode) -> ASTNode:
        """Convert Runa AST to {language_info.name} AST."""
        try:
            # TODO: Implement Runa -> {language_info.name} conversion
            # This should map Runa nodes to {language_info.name}-specific nodes
            
            return self._convert_from_runa(runa_ast)
            
        except Exception as e:
            raise ConversionError(f"Failed to convert Runa AST to {language_info.name}: {{e}}")
    
    def _convert_to_runa(self, node: ASTNode) -> ASTNode:
        """Convert a single node to Runa - IMPLEMENT THIS."""
        # TODO: Implement node-by-node conversion logic
        raise NotImplementedError("Converter implementation needed")
    
    def _convert_from_runa(self, node: ASTNode) -> ASTNode:
        """Convert a single Runa node to {language_info.name} - IMPLEMENT THIS."""
        # TODO: Implement node-by-node conversion logic
        raise NotImplementedError("Converter implementation needed")
'''
    
    @staticmethod
    def generate_generator_template(language_info: LanguageInfo) -> str:
        """Generate a generator template for a language."""
        return f'''"""
{language_info.name} Code Generator

Generates {language_info.name} source code from language-specific AST.
"""

from typing import List
from runa.core.base_components import BaseLanguageGenerator, GenerationError
from runa.core.runa_ast import ASTNode

# Import language-specific AST nodes
from .{language_info.name.lower()}_ast import *


class {language_info.name.title()}Generator(BaseLanguageGenerator):
    """Code generator for {language_info.name} programming language."""
    
    def generate(self, language_ast: ASTNode) -> str:
        """Generate {language_info.name} source code from AST."""
        try:
            # TODO: Implement AST -> code generation
            # This should traverse the AST and generate idiomatic {language_info.name} code
            
            code_lines = []
            self._generate_node(language_ast, code_lines, 0)
            
            source_code = self.line_ending.join(code_lines)
            return self.format_code(source_code)
            
        except Exception as e:
            raise GenerationError(f"Failed to generate {language_info.name} code: {{e}}")
    
    def _generate_node(self, node: ASTNode, code_lines: List[str], indent_level: int):
        """Generate code for a single AST node - IMPLEMENT THIS."""
        # TODO: Implement node-by-node code generation
        # This should dispatch to specific methods based on node type
        
        raise NotImplementedError("Generator implementation needed")
'''


# Language registry for tracking all supported languages
LANGUAGE_REGISTRY: Dict[str, LanguageInfo] = {}


def register_language_info(language_info: LanguageInfo) -> None:
    """Register language information."""
    LANGUAGE_REGISTRY[language_info.name.lower()] = language_info


def get_language_info(language_name: str) -> Optional[LanguageInfo]:
    """Get language information by name."""
    return LANGUAGE_REGISTRY.get(language_name.lower())


def list_supported_languages() -> List[str]:
    """Get list of all registered languages."""
    return list(LANGUAGE_REGISTRY.keys())


def get_languages_by_tier(tier: LanguageTier) -> List[LanguageInfo]:
    """Get all languages in a specific tier."""
    return [info for info in LANGUAGE_REGISTRY.values() if info.tier == tier]