#!/usr/bin/env python3
"""
CMake AST (Abstract Syntax Tree) Implementation

Complete AST structure for CMake build files including:
- CMakeLists.txt with commands and targets
- Variables and property management
- Functions and macros
- Find modules and package configuration
- Cross-platform build system features
- Modern CMake target-based approach
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class CMakeNodeType(Enum):
    """Enumeration of all CMake AST node types."""
    # File level
    CMAKE_FILE = "cmake_file"
    CMAKE_PROJECT = "cmake_project"
    
    # Commands
    COMMAND_INVOCATION = "command_invocation"
    PROJECT_COMMAND = "project_command"
    ADD_EXECUTABLE = "add_executable"
    ADD_LIBRARY = "add_library"
    TARGET_LINK_LIBRARIES = "target_link_libraries"
    TARGET_INCLUDE_DIRECTORIES = "target_include_directories"
    TARGET_COMPILE_DEFINITIONS = "target_compile_definitions"
    TARGET_COMPILE_OPTIONS = "target_compile_options"
    SET_COMMAND = "set_command"
    FIND_PACKAGE = "find_package"
    INCLUDE = "include"
    
    # Control flow
    IF_STATEMENT = "if_statement"
    WHILE_LOOP = "while_loop"
    FOREACH_LOOP = "foreach_loop"
    FUNCTION_DEF = "function_def"
    MACRO_DEF = "macro_def"
    
    # Expressions
    VARIABLE_REF = "variable_ref"
    GENERATOR_EXPR = "generator_expr"
    STRING_LITERAL = "string_literal"
    LIST_EXPR = "list_expr"
    QUOTED_ARGUMENT = "quoted_argument"
    BRACKET_ARGUMENT = "bracket_argument"
    
    # Advanced features
    CONFIGURE_FILE = "configure_file"
    INSTALL_COMMAND = "install_command"
    CUSTOM_COMMAND = "custom_command"
    CUSTOM_TARGET = "custom_target"
    TEST_COMMAND = "test_command"


@dataclass
class CMakeNode(ABC):
    """Base class for all CMake AST nodes."""
    node_type: CMakeNodeType
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    source_file: Optional[str] = None
    
    @abstractmethod
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        """Accept a visitor for traversal."""
        pass


@dataclass
class CMakeExpression(CMakeNode):
    """Base class for CMake expressions."""
    pass


@dataclass
class CMakeStatement(CMakeNode):
    """Base class for CMake statements."""
    pass


@dataclass
class CMakeCommand(CMakeNode):
    """Base class for CMake commands."""
    pass


# === File Level Nodes ===

@dataclass
class CMakeFile(CMakeNode):
    """Represents a CMakeLists.txt file."""
    file_path: str
    statements: List[CMakeStatement] = field(default_factory=list)
    cmake_minimum_required: Optional[str] = None
    project_name: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.CMAKE_FILE
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_cmake_file(self)


@dataclass
class CMakeProject(CMakeNode):
    """Represents a CMake project."""
    name: str
    version: Optional[str] = None
    languages: List[str] = field(default_factory=list)
    description: Optional[str] = None
    homepage_url: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.CMAKE_PROJECT
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_cmake_project(self)


# === Command Invocations ===

@dataclass
class CommandInvocation(CMakeCommand):
    """Represents a generic command invocation."""
    command_name: str
    arguments: List[CMakeExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.COMMAND_INVOCATION
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_command_invocation(self)


@dataclass
class ProjectCommand(CMakeCommand):
    """Represents project() command."""
    name: str
    version: Optional[str] = None
    languages: List[str] = field(default_factory=list)
    description: Optional[str] = None
    homepage_url: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.PROJECT_COMMAND
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_project_command(self)


@dataclass
class AddExecutable(CMakeCommand):
    """Represents add_executable() command."""
    name: str
    sources: List[str] = field(default_factory=list)
    is_win32: bool = False
    is_macosx_bundle: bool = False
    exclude_from_all: bool = False
    imported: bool = False
    alias_target: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.ADD_EXECUTABLE
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_add_executable(self)


@dataclass
class AddLibrary(CMakeCommand):
    """Represents add_library() command."""
    name: str
    sources: List[str] = field(default_factory=list)
    library_type: str = "STATIC"  # STATIC, SHARED, MODULE, INTERFACE, OBJECT
    exclude_from_all: bool = False
    imported: bool = False
    alias_target: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.ADD_LIBRARY
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_add_library(self)


@dataclass
class TargetLinkLibraries(CMakeCommand):
    """Represents target_link_libraries() command."""
    target: str
    libraries: List[str] = field(default_factory=list)
    scope: str = "PUBLIC"  # PUBLIC, PRIVATE, INTERFACE
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.TARGET_LINK_LIBRARIES
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_target_link_libraries(self)


@dataclass
class TargetIncludeDirectories(CMakeCommand):
    """Represents target_include_directories() command."""
    target: str
    directories: List[str] = field(default_factory=list)
    scope: str = "PUBLIC"  # PUBLIC, PRIVATE, INTERFACE
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.TARGET_INCLUDE_DIRECTORIES
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_target_include_directories(self)


@dataclass
class TargetCompileDefinitions(CMakeCommand):
    """Represents target_compile_definitions() command."""
    target: str
    definitions: List[str] = field(default_factory=list)
    scope: str = "PUBLIC"  # PUBLIC, PRIVATE, INTERFACE
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.TARGET_COMPILE_DEFINITIONS
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_target_compile_definitions(self)


@dataclass
class TargetCompileOptions(CMakeCommand):
    """Represents target_compile_options() command."""
    target: str
    options: List[str] = field(default_factory=list)
    scope: str = "PUBLIC"  # PUBLIC, PRIVATE, INTERFACE
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.TARGET_COMPILE_OPTIONS
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_target_compile_options(self)


@dataclass
class SetCommand(CMakeCommand):
    """Represents set() command."""
    variable: str
    value: Union[str, List[str]]
    cache: bool = False
    cache_type: Optional[str] = None  # BOOL, FILEPATH, PATH, STRING, INTERNAL
    cache_docstring: Optional[str] = None
    force: bool = False
    parent_scope: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.SET_COMMAND
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_set_command(self)


@dataclass
class FindPackage(CMakeCommand):
    """Represents find_package() command."""
    package_name: str
    version: Optional[str] = None
    exact: bool = False
    quiet: bool = False
    required: bool = False
    components: List[str] = field(default_factory=list)
    optional_components: List[str] = field(default_factory=list)
    no_policy_scope: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.FIND_PACKAGE
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_find_package(self)


@dataclass
class Include(CMakeCommand):
    """Represents include() command."""
    file_path: str
    optional: bool = False
    result_variable: Optional[str] = None
    no_policy_scope: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.INCLUDE
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_include(self)


@dataclass
class ConfigureFile(CMakeCommand):
    """Represents configure_file() command."""
    input_file: str
    output_file: str
    copy_only: bool = False
    escape_quotes: bool = False
    at_only: bool = False
    newline_style: Optional[str] = None  # UNIX, DOS, WIN32, LF, CRLF
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.CONFIGURE_FILE
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_configure_file(self)


@dataclass
class InstallCommand(CMakeCommand):
    """Represents install() command."""
    install_type: str  # TARGETS, FILES, PROGRAMS, DIRECTORY, SCRIPT, CODE
    items: List[str] = field(default_factory=list)
    destination: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    configurations: List[str] = field(default_factory=list)
    component: Optional[str] = None
    optional: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.INSTALL_COMMAND
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_install_command(self)


@dataclass
class CustomCommand(CMakeCommand):
    """Represents add_custom_command() command."""
    output: List[str] = field(default_factory=list)
    command: List[str] = field(default_factory=list)
    depends: List[str] = field(default_factory=list)
    working_directory: Optional[str] = None
    comment: Optional[str] = None
    verbatim: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.CUSTOM_COMMAND
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_custom_command(self)


@dataclass
class CustomTarget(CMakeCommand):
    """Represents add_custom_target() command."""
    name: str
    command: List[str] = field(default_factory=list)
    depends: List[str] = field(default_factory=list)
    working_directory: Optional[str] = None
    comment: Optional[str] = None
    all: bool = False
    verbatim: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.CUSTOM_TARGET
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_custom_target(self)


# === Control Flow ===

@dataclass
class IfStatement(CMakeStatement):
    """Represents if() statement."""
    condition: CMakeExpression
    then_body: List[CMakeStatement] = field(default_factory=list)
    elseif_clauses: List[tuple] = field(default_factory=list)  # List of (condition, body) tuples
    else_body: Optional[List[CMakeStatement]] = None
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.IF_STATEMENT
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_if_statement(self)


@dataclass
class WhileLoop(CMakeStatement):
    """Represents while() loop."""
    condition: CMakeExpression
    body: List[CMakeStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.WHILE_LOOP
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_while_loop(self)


@dataclass
class ForeachLoop(CMakeStatement):
    """Represents foreach() loop."""
    variable: str
    items: Union[CMakeExpression, str]  # Can be range, list, or IN LISTS/ITEMS
    body: List[CMakeStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.FOREACH_LOOP
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_foreach_loop(self)


@dataclass
class FunctionDef(CMakeStatement):
    """Represents function() definition."""
    name: str
    parameters: List[str] = field(default_factory=list)
    body: List[CMakeStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.FUNCTION_DEF
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_function_def(self)


@dataclass
class MacroDef(CMakeStatement):
    """Represents macro() definition."""
    name: str
    parameters: List[str] = field(default_factory=list)
    body: List[CMakeStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.MACRO_DEF
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_macro_def(self)


# === Expressions ===

@dataclass
class VariableRef(CMakeExpression):
    """Represents a variable reference ${VAR}."""
    variable: str
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.VARIABLE_REF
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_variable_ref(self)


@dataclass
class GeneratorExpr(CMakeExpression):
    """Represents a generator expression $<...>."""
    expression: str
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.GENERATOR_EXPR
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_generator_expr(self)


@dataclass
class StringLiteral(CMakeExpression):
    """Represents a string literal."""
    value: str
    quoted: bool = False
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.STRING_LITERAL
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_string_literal(self)


@dataclass
class ListExpr(CMakeExpression):
    """Represents a list expression."""
    elements: List[CMakeExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.LIST_EXPR
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_list_expr(self)


@dataclass
class QuotedArgument(CMakeExpression):
    """Represents a quoted argument."""
    content: str
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.QUOTED_ARGUMENT
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_quoted_argument(self)


@dataclass
class BracketArgument(CMakeExpression):
    """Represents a bracket argument [[...]]."""
    content: str
    level: int = 0  # Number of = signs in brackets
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.BRACKET_ARGUMENT
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_bracket_argument(self)


# === Advanced Features ===

@dataclass
class TestCommand(CMakeCommand):
    """Represents add_test() command."""
    name: str
    command: List[str] = field(default_factory=list)
    working_directory: Optional[str] = None
    configurations: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = CMakeNodeType.TEST_COMMAND
    
    def accept(self, visitor: 'CMakeVisitor') -> Any:
        return visitor.visit_test_command(self)


# === Visitor Pattern ===

class CMakeVisitor(ABC):
    """Abstract visitor for traversing CMake AST."""
    
    @abstractmethod
    def visit_cmake_file(self, node: CMakeFile) -> Any:
        pass
    
    @abstractmethod
    def visit_cmake_project(self, node: CMakeProject) -> Any:
        pass
    
    @abstractmethod
    def visit_command_invocation(self, node: CommandInvocation) -> Any:
        pass
    
    @abstractmethod
    def visit_project_command(self, node: ProjectCommand) -> Any:
        pass
    
    @abstractmethod
    def visit_add_executable(self, node: AddExecutable) -> Any:
        pass
    
    @abstractmethod
    def visit_add_library(self, node: AddLibrary) -> Any:
        pass
    
    @abstractmethod
    def visit_target_link_libraries(self, node: TargetLinkLibraries) -> Any:
        pass
    
    @abstractmethod
    def visit_target_include_directories(self, node: TargetIncludeDirectories) -> Any:
        pass
    
    @abstractmethod
    def visit_target_compile_definitions(self, node: TargetCompileDefinitions) -> Any:
        pass
    
    @abstractmethod
    def visit_target_compile_options(self, node: TargetCompileOptions) -> Any:
        pass
    
    @abstractmethod
    def visit_set_command(self, node: SetCommand) -> Any:
        pass
    
    @abstractmethod
    def visit_find_package(self, node: FindPackage) -> Any:
        pass
    
    @abstractmethod
    def visit_include(self, node: Include) -> Any:
        pass
    
    @abstractmethod
    def visit_configure_file(self, node: ConfigureFile) -> Any:
        pass
    
    @abstractmethod
    def visit_install_command(self, node: InstallCommand) -> Any:
        pass
    
    @abstractmethod
    def visit_custom_command(self, node: CustomCommand) -> Any:
        pass
    
    @abstractmethod
    def visit_custom_target(self, node: CustomTarget) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_while_loop(self, node: WhileLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_foreach_loop(self, node: ForeachLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_function_def(self, node: FunctionDef) -> Any:
        pass
    
    @abstractmethod
    def visit_macro_def(self, node: MacroDef) -> Any:
        pass
    
    @abstractmethod
    def visit_variable_ref(self, node: VariableRef) -> Any:
        pass
    
    @abstractmethod
    def visit_generator_expr(self, node: GeneratorExpr) -> Any:
        pass
    
    @abstractmethod
    def visit_string_literal(self, node: StringLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_list_expr(self, node: ListExpr) -> Any:
        pass
    
    @abstractmethod
    def visit_quoted_argument(self, node: QuotedArgument) -> Any:
        pass
    
    @abstractmethod
    def visit_bracket_argument(self, node: BracketArgument) -> Any:
        pass
    
    @abstractmethod
    def visit_test_command(self, node: TestCommand) -> Any:
        pass


# === Utility Functions ===

def create_cmake_minimum_required(version: str) -> CommandInvocation:
    """Create cmake_minimum_required command."""
    return CommandInvocation(
        command_name="cmake_minimum_required",
        arguments=[
            StringLiteral("VERSION"),
            StringLiteral(version)
        ]
    )


def create_variable_reference(variable: str) -> VariableRef:
    """Create a variable reference."""
    return VariableRef(variable=variable)


def create_generator_expression(expression: str) -> GeneratorExpr:
    """Create a generator expression."""
    return GeneratorExpr(expression=expression)


def is_valid_cmake_identifier(name: str) -> bool:
    """Check if a name is a valid CMake identifier."""
    if not name or not name[0].isalpha() and name[0] != '_':
        return False
    return all(c.isalnum() or c == '_' for c in name)


def is_builtin_cmake_command(command: str) -> bool:
    """Check if a command is a built-in CMake command."""
    builtin_commands = {
        'cmake_minimum_required', 'project', 'add_executable', 'add_library',
        'target_link_libraries', 'target_include_directories', 'target_compile_definitions',
        'target_compile_options', 'set', 'find_package', 'include', 'configure_file',
        'install', 'add_custom_command', 'add_custom_target', 'add_test',
        'if', 'elseif', 'else', 'endif', 'while', 'endwhile', 'foreach', 'endforeach',
        'function', 'endfunction', 'macro', 'endmacro', 'return', 'break', 'continue'
    }
    return command.lower() in builtin_commands 