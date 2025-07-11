"""
Tcl Language Support for Runa Universal Translation Platform

This package provides comprehensive support for the Tcl (Tool Command Language),
enabling bidirectional translation between Runa and Tcl for automation scripting,
text processing, and system administration tasks.

Tcl Features Supported:
- Simple command-based syntax
- Variable and command substitution  
- String manipulation and processing
- Control structures (if, while, for, foreach)
- Procedures and namespaces
- List processing and manipulation
- Regular expressions
- File I/O and system interaction
- Error handling (try/catch)
- Package system
- Automation scripting
- Text processing workflows
"""

# Core components
from .tcl_ast import (
    # Node types and enums
    TclNodeType, TclNode,
    
    # Program structure
    TclScript, TclCommand, TclWord,
    
    # Procedures and namespaces
    TclProc, TclNamespace, TclPackage,
    
    # Control structures
    TclIf, TclElseIf, TclWhile, TclFor, TclForeach,
    TclSwitch, TclSwitchPattern, TclTry, TclCatch,
    
    # Substitutions
    TclVariableSubstitution, TclCommandSubstitution, TclBackslashSubstitution,
    
    # Variables and arrays
    TclVariable, TclArrayElement, TclSet, TclGlobal, TclUpvar,
    
    # String and list operations
    TclStringLiteral, TclQuotedString, TclBracedString, TclList,
    TclStringMatch, TclStringMap, TclStringRange, TclStringIndex,
    TclLappend, TclLindex, TclLlength, TclLrange, TclLsort,
    
    # Regular expressions
    TclRegexp, TclRegsub,
    
    # File and I/O
    TclOpen, TclClose, TclPuts, TclGets, TclRead,
    
    # System interaction
    TclExec, TclSource, TclEval,
    
    # Error handling and control
    TclError, TclReturn, TclBreak, TclContinue,
    
    # Special constructs
    TclExpr, TclIncr, TclUnset, TclInfo, TclComment,
    
    # Utility functions
    create_tcl_script, create_tcl_command, create_tcl_proc,
    create_tcl_if, create_tcl_while, create_tcl_foreach,
    create_tcl_variable_substitution, create_tcl_command_substitution,
    create_tcl_list
)

from .tcl_parser import TclParser, TclParsingContext
from .tcl_converter import TclConverter, TclConversionContext  
from .tcl_generator import TclGenerator, TclGenerationContext
from .tcl_toolchain import TclToolchain, TclToolchainConfig, TclExecutionResult

# Package metadata
LANGUAGE_NAME = "tcl"
LANGUAGE_VERSION = "8.6"
TIER = 6
CATEGORY = "automation_scripting"

# Supported features
FEATURES = {
    "automation_scripting": True,
    "text_processing": True,
    "string_manipulation": True,
    "command_substitution": True,
    "variable_substitution": True,
    "list_processing": True,
    "regular_expressions": True,
    "file_io": True,
    "control_structures": True,
    "procedures": True,
    "namespaces": True,
    "error_handling": True,
    "system_interaction": True,
    "package_system": True,
    "gui_development": True,  # via Tk
    "expect_automation": True  # via Expect
}

# Export list for convenience
__all__ = [
    # Core classes
    'TclParser', 'TclConverter', 'TclGenerator', 'TclToolchain',
    
    # AST nodes - Program structure
    'TclScript', 'TclCommand', 'TclWord',
    
    # AST nodes - Procedures and namespaces  
    'TclProc', 'TclNamespace', 'TclPackage',
    
    # AST nodes - Control structures
    'TclIf', 'TclElseIf', 'TclWhile', 'TclFor', 'TclForeach',
    'TclSwitch', 'TclSwitchPattern', 'TclTry', 'TclCatch',
    
    # AST nodes - Substitutions
    'TclVariableSubstitution', 'TclCommandSubstitution', 'TclBackslashSubstitution',
    
    # AST nodes - Variables and data
    'TclVariable', 'TclArrayElement', 'TclSet', 'TclGlobal', 'TclUpvar',
    'TclStringLiteral', 'TclQuotedString', 'TclBracedString', 'TclList',
    
    # AST nodes - String operations
    'TclStringMatch', 'TclStringMap', 'TclStringRange', 'TclStringIndex',
    
    # AST nodes - List operations
    'TclLappend', 'TclLindex', 'TclLlength', 'TclLrange', 'TclLsort',
    
    # AST nodes - Regular expressions
    'TclRegexp', 'TclRegsub',
    
    # AST nodes - File I/O
    'TclOpen', 'TclClose', 'TclPuts', 'TclGets', 'TclRead',
    
    # AST nodes - System interaction
    'TclExec', 'TclSource', 'TclEval',
    
    # AST nodes - Control flow
    'TclError', 'TclReturn', 'TclBreak', 'TclContinue',
    
    # AST nodes - Special constructs
    'TclExpr', 'TclIncr', 'TclUnset', 'TclInfo', 'TclComment',
    
    # Configuration and context
    'TclParsingContext', 'TclConversionContext', 'TclGenerationContext',
    'TclToolchainConfig', 'TclExecutionResult',
    
    # Utility functions
    'create_tcl_script', 'create_tcl_command', 'create_tcl_proc',
    'create_tcl_if', 'create_tcl_while', 'create_tcl_foreach',
    'create_tcl_variable_substitution', 'create_tcl_command_substitution',
    'create_tcl_list',
    
    # High-level functions
    'parse_tcl', 'generate_tcl', 'runa_to_tcl', 'tcl_to_runa',
    'create_tcl_toolchain', 'execute_tcl_script', 'validate_tcl_syntax',
    
    # Metadata
    'LANGUAGE_NAME', 'LANGUAGE_VERSION', 'TIER', 'CATEGORY', 'FEATURES'
]

# Convenience functions for common operations

def parse_tcl(source_code: str, context: TclParsingContext = None) -> TclScript:
    """Parse Tcl source code into AST"""
    parser = TclParser(context or TclParsingContext())
    return parser.parse(source_code)

def generate_tcl(ast_node: TclNode, context: TclGenerationContext = None) -> str:
    """Generate Tcl code from AST"""
    generator = TclGenerator()
    if context:
        generator.context = context
    return generator.generate(ast_node)

def runa_to_tcl(runa_ast, context: TclConversionContext = None):
    """Convert Runa AST to Tcl AST"""
    converter = TclConverter()
    if context:
        converter.context = context
    return converter.runa_to_tcl(runa_ast)

def tcl_to_runa(tcl_ast: TclNode, context: TclConversionContext = None):
    """Convert Tcl AST to Runa AST"""
    converter = TclConverter()
    if context:
        converter.context = context
    return converter.tcl_to_runa(tcl_ast)

def create_tcl_toolchain(config: TclToolchainConfig = None) -> TclToolchain:
    """Create a configured Tcl toolchain"""
    return TclToolchain(config or TclToolchainConfig())

def execute_tcl_script(script_path: str, args: list = None, 
                      toolchain: TclToolchain = None) -> TclExecutionResult:
    """Execute a Tcl script with optional arguments"""
    if toolchain is None:
        toolchain = create_tcl_toolchain()
    return toolchain.execute_script(script_path, args or [])

def validate_tcl_syntax(script_path: str, toolchain: TclToolchain = None) -> tuple:
    """Validate Tcl script syntax"""
    if toolchain is None:
        toolchain = create_tcl_toolchain()
    return toolchain.validate_syntax(script_path)

# Automation and scripting utilities

def create_automation_script(commands: list, output_file: str = None) -> TclScript:
    """Create a Tcl automation script from a list of commands"""
    script = TclScript()
    
    # Add header comment
    script.commands.append(TclComment(text="Automation script generated by Runa"))
    
    for cmd in commands:
        if isinstance(cmd, str):
            # Simple command string
            script.commands.append(TclCommand(command_name=cmd))
        elif isinstance(cmd, dict):
            # Command with arguments
            command_name = cmd.get('command', '')
            args = cmd.get('args', [])
            tcl_args = [TclWord(content=str(arg)) for arg in args]
            script.commands.append(TclCommand(command_name=command_name, arguments=tcl_args))
        elif isinstance(cmd, TclCommand):
            # Already a Tcl command
            script.commands.append(cmd)
    
    if output_file:
        # Generate and save to file
        generator = TclGenerator()
        code = generator.generate(script)
        with open(output_file, 'w') as f:
            f.write(code)
    
    return script

def create_text_processing_script(input_file: str, output_file: str, 
                                operations: list) -> TclScript:
    """Create a Tcl script for text processing operations"""
    script = TclScript()
    
    # Open input file
    script.commands.append(TclCommand(
        command_name="set",
        arguments=[
            TclWord(content="infile"),
            TclWord(content=f'[open "{input_file}" r]')
        ]
    ))
    
    # Open output file
    script.commands.append(TclCommand(
        command_name="set", 
        arguments=[
            TclWord(content="outfile"),
            TclWord(content=f'[open "{output_file}" w]')
        ]
    ))
    
    # Process operations
    for op in operations:
        if op.get('type') == 'replace':
            # String replacement operation
            pattern = op.get('pattern', '')
            replacement = op.get('replacement', '')
            script.commands.append(TclRegsub(
                pattern=TclWord(content=pattern),
                string=TclWord(content="$line"),
                replacement=TclWord(content=replacement),
                options=["-all"]
            ))
    
    # Close files
    script.commands.append(TclCommand(command_name="close", arguments=[TclWord(content="$infile")]))
    script.commands.append(TclCommand(command_name="close", arguments=[TclWord(content="$outfile")]))
    
    return script

def create_system_admin_script(tasks: list) -> TclScript:
    """Create a Tcl script for system administration tasks"""
    script = TclScript()
    
    # Add safety header
    script.commands.append(TclComment(text="System administration script - use with caution"))
    
    for task in tasks:
        task_type = task.get('type', '')
        
        if task_type == 'backup':
            source = task.get('source', '')
            destination = task.get('destination', '')
            script.commands.append(TclExec(
                program=TclWord(content="cp"),
                arguments=[
                    TclWord(content="-r"),
                    TclWord(content=source),
                    TclWord(content=destination)
                ]
            ))
        elif task_type == 'log_rotate':
            log_file = task.get('file', '')
            script.commands.append(TclExec(
                program=TclWord(content="logrotate"),
                arguments=[TclWord(content=log_file)]
            ))
        elif task_type == 'cleanup':
            directory = task.get('directory', '')
            pattern = task.get('pattern', '*.tmp')
            script.commands.append(TclExec(
                program=TclWord(content="find"),
                arguments=[
                    TclWord(content=directory),
                    TclWord(content="-name"),
                    TclWord(content=pattern),
                    TclWord(content="-delete")
                ]
            ))
    
    return script

# Package information for introspection
def get_package_info() -> dict:
    """Get comprehensive package information"""
    return {
        "name": LANGUAGE_NAME,
        "version": LANGUAGE_VERSION,
        "tier": TIER,
        "category": CATEGORY,
        "features": FEATURES,
        "description": "Tcl (Tool Command Language) support for automation scripting and text processing",
        "use_cases": [
            "System administration automation",
            "Text processing and manipulation", 
            "Configuration management",
            "Scripting and glue code",
            "GUI applications (with Tk)",
            "Network automation (with Expect)",
            "Build system scripting",
            "Testing and validation scripts"
        ],
        "strengths": [
            "Simple, consistent syntax",
            "Powerful string processing",
            "Excellent for automation tasks", 
            "Cross-platform compatibility",
            "Extensive standard library",
            "Easy integration with other tools",
            "Mature and stable language"
        ],
        "common_patterns": [
            "Command-line processing",
            "File manipulation",
            "Regular expression operations",
            "System command execution",
            "Configuration file parsing",
            "Log file processing",
            "Network protocol scripting"
        ]
    } 