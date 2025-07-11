#!/usr/bin/env python3
"""
Shell Language Support for Runa Universal Translation System

This package provides comprehensive Shell script language support including:
- POSIX sh, Bash, Zsh, Fish shell parsing and validation
- Bidirectional Shell ↔ Runa AST conversion
- Multi-dialect shell code generation with formatting options
- Round-trip translation verification
- Shell script linting and security analysis
- Cross-shell portability checking
- Complete toolchain integration with ShellCheck, shfmt, and shell interpreters
- Shell testing and execution frameworks
"""

from .shell_ast import *
from .shell_parser import parse_shell, ShellLexer, ShellParser, validate_shell_syntax
from .shell_converter import shell_to_runa, runa_to_shell, ShellToRunaConverter, RunaToShellConverter
from .shell_generator import generate_shell, ShellCodeGenerator, ShellDialect, ShellFormatStyle, ShellFormatter
from .shell_toolchain import (
    ShellToolchain,
    parse_shell_code,
    generate_shell_code,
    shell_round_trip_verify,
    shell_to_runa_translate,
    runa_to_shell_translate
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "Complete Shell script language toolchain for universal code translation"

# Main toolchain instance
toolchain = ShellToolchain()

# Convenience functions for external use
__all__ = [
    # Core components
    "toolchain", "ShellToolchain",
    
    # Parser components
    "parse_shell", "ShellLexer", "ShellParser", "validate_shell_syntax",
    
    # Converters
    "shell_to_runa", "runa_to_shell", "ShellToRunaConverter", "RunaToShellConverter",
    
    # Generator
    "generate_shell", "ShellCodeGenerator", "ShellDialect", "ShellFormatStyle", "ShellFormatter",
    
    # Convenience functions
    "parse_shell_code", "generate_shell_code", "shell_round_trip_verify",
    "shell_to_runa_translate", "runa_to_shell_translate",
    
    # AST base classes (main ones)
    "ShellNode", "ShellStatement", "ShellScript", "ShellCommand", "ShellPipeline",
    "ShellCompoundCommand", "ShellFunctionDefinition", "ShellVariableAssignment",
    "ShellConditional", "ShellLoop", "ShellRedirection", "ShellExpansion",
    "ShellParameterExpansion", "ShellCommandSubstitution", "ShellArithmeticExpansion",
    "ShellComment", "ShellGlob", "ShellProcess",
    
    # Enums and types
    "ShellNodeType", "ShellDialect", "ShellFormatStyle", "ShellTokenType",
    
    # Helper functions
    "create_shell_script", "create_shell_command", "create_shell_pipeline",
    "create_shell_function", "create_shell_variable_assignment", "create_shell_if",
    "create_shell_for_loop", "create_shell_while_loop", "create_shell_redirection",
    "create_shell_comment", "parse_shell_command_line", "is_shell_special_character",
    "escape_shell_string", "get_shell_builtin_commands", "get_shell_reserved_words",
    "normalize_shell_command", "shell_to_dict", "dict_to_shell",
    
    # Visitor pattern
    "ShellVisitor", "ShellVisitorExtended",
]

# Module metadata
__language__ = "shell"
__tier__ = 3
__file_extensions__ = [".sh", ".bash", ".zsh", ".fish"]
__mime_types__ = ["application/x-sh", "application/x-shellscript", "text/x-shellscript"]
__dialects__ = ["sh", "bash", "zsh", "fish", "dash"]
