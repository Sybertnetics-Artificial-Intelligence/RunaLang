#!/usr/bin/env python3
"""
Make AST - Abstract Syntax Tree for Make (GNU Make/POSIX Make)

Comprehensive AST representation supporting:
- Rules and targets (explicit, implicit, pattern, double-colon)
- Variables (simple, recursive, immediate, conditional)
- Dependencies (files, order-only, automatic variables)
- Commands (shell commands, make functions, built-ins)
- Conditionals (ifeq, ifneq, ifdef, ifndef, else, endif)
- Includes and sub-makefiles
- Functions (user-defined and built-in)
- Pattern rules and suffix rules
- VPATH and search paths
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Base AST Node Classes

@dataclass
class MakeNode(ABC):
    """Base class for all Make AST nodes"""
    line_number: int = 0
    column_number: int = 0
    source_file: Optional[str] = None
    
    @abstractmethod
    def accept(self, visitor: 'MakeVisitor') -> Any:
        """Accept visitor for traversal"""
        pass

@dataclass 
class MakeExpression(MakeNode):
    """Base class for Make expressions"""
    pass

@dataclass
class MakeStatement(MakeNode): 
    """Base class for Make statements"""
    pass

# Core AST Node Types

@dataclass
class MakeFile(MakeNode):
    """Root node representing a complete Makefile"""
    statements: List[MakeStatement] = field(default_factory=list)
    variables: Dict[str, 'MakeVariable'] = field(default_factory=dict)
    rules: List['MakeRule'] = field(default_factory=list)
    includes: List['MakeInclude'] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_makefile(self)

# Variable System

@dataclass
class MakeVariable(MakeStatement):
    """Make variable definition"""
    name: str
    value: MakeExpression
    assignment_type: str = "="  # =, :=, ?=, +=, !=
    is_exported: bool = False
    is_override: bool = False
    is_private: bool = False
    target_specific: Optional[str] = None  # Target for target-specific variables
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_variable(self)

@dataclass
class VariableReference(MakeExpression):
    """Variable reference like $(VAR) or ${VAR}"""
    name: str
    bracket_style: str = "$())"  # $() or ${}
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_variable_reference(self)

@dataclass
class AutomaticVariable(MakeExpression):
    """Automatic variables like $@, $<, $?, $^"""
    symbol: str  # @, <, ?, ^, +, *, %, |, etc.
    modifier: Optional[str] = None  # D, F for directory/file parts
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_automatic_variable(self)

# Rules and Targets

@dataclass
class MakeRule(MakeStatement):
    """Make rule definition"""
    targets: List[str]
    dependencies: List[str] = field(default_factory=list)
    order_only_deps: List[str] = field(default_factory=list)  # Dependencies after |
    commands: List['MakeCommand'] = field(default_factory=list)
    is_pattern_rule: bool = False
    is_implicit_rule: bool = False
    is_double_colon: bool = False
    is_phony: bool = False
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_rule(self)

@dataclass
class MakeTarget(MakeExpression):
    """Individual target in a rule"""
    name: str
    is_pattern: bool = False  # Contains % wildcard
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_target(self)

@dataclass
class MakeCommand(MakeNode):
    """Command in a rule recipe"""
    command_line: str
    is_silent: bool = False  # Prefixed with @
    ignore_errors: bool = False  # Prefixed with -
    always_execute: bool = False  # Prefixed with +
    expanded_command: Optional[str] = None  # After variable expansion
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_command(self)

# Functions

@dataclass
class MakeFunction(MakeExpression):
    """Make function call"""
    name: str
    arguments: List[MakeExpression] = field(default_factory=list)
    is_builtin: bool = True
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_function(self)

@dataclass
class UserDefinedFunction(MakeStatement):
    """User-defined function using define/endef"""
    name: str
    parameters: List[str] = field(default_factory=list)
    body: List[MakeStatement] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_user_function(self)

# Built-in Functions (common ones)

@dataclass
class SubstFunction(MakeFunction):
    """$(subst from,to,text) function"""
    from_text: MakeExpression
    to_text: MakeExpression
    source_text: MakeExpression
    
    def __post_init__(self):
        self.name = "subst"
        self.arguments = [self.from_text, self.to_text, self.source_text]

@dataclass
class PatsubstFunction(MakeFunction):
    """$(patsubst pattern,replacement,text) function"""
    pattern: MakeExpression
    replacement: MakeExpression
    text: MakeExpression
    
    def __post_init__(self):
        self.name = "patsubst"
        self.arguments = [self.pattern, self.replacement, self.text]

@dataclass
class WildcardFunction(MakeFunction):
    """$(wildcard pattern) function"""
    pattern: MakeExpression
    
    def __post_init__(self):
        self.name = "wildcard"
        self.arguments = [self.pattern]

@dataclass
class ShellFunction(MakeFunction):
    """$(shell command) function"""
    command: MakeExpression
    
    def __post_init__(self):
        self.name = "shell"
        self.arguments = [self.command]

# Conditionals

@dataclass
class MakeConditional(MakeStatement):
    """Conditional statements (ifeq, ifneq, ifdef, ifndef)"""
    condition_type: str  # ifeq, ifneq, ifdef, ifndef
    condition: MakeExpression
    then_statements: List[MakeStatement] = field(default_factory=list)
    else_statements: List[MakeStatement] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_conditional(self)

@dataclass
class ConditionalExpression(MakeExpression):
    """Conditional expression like (arg1,arg2) or "arg1" "arg2\""""
    left: MakeExpression
    right: MakeExpression
    comparison_type: str  # equals, not_equals, defined, not_defined
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_conditional_expression(self)

# Includes and Directives

@dataclass
class MakeInclude(MakeStatement):
    """Include directive"""
    filenames: List[str]
    is_optional: bool = False  # -include vs include
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_include(self)

@dataclass
class VPathDirective(MakeStatement):
    """VPATH or vpath directive"""
    pattern: Optional[str] = None  # None for VPATH, pattern for vpath
    directories: List[str] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_vpath(self)

@dataclass
class ExportDirective(MakeStatement):
    """Export directive"""
    variables: List[str] = field(default_factory=list)
    is_unexport: bool = False
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_export(self)

# Text and Literals

@dataclass
class TextLiteral(MakeExpression):
    """Plain text literal"""
    value: str
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_text_literal(self)

@dataclass
class ConcatenatedText(MakeExpression):
    """Concatenated text with variables and literals"""
    parts: List[MakeExpression] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_concatenated_text(self)

@dataclass
class MakeComment(MakeStatement):
    """Comment line"""
    text: str
    is_inline: bool = False
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_comment(self)

# Special Targets and Directives

@dataclass
class SpecialTarget(MakeStatement):
    """Special built-in targets like .PHONY, .SUFFIXES, etc."""
    name: str  # .PHONY, .SUFFIXES, .PRECIOUS, .INTERMEDIATE, etc.
    dependencies: List[str] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_special_target(self)

@dataclass
class SuffixRule(MakeStatement):
    """Suffix rule like .c.o:"""
    source_suffix: str
    target_suffix: str
    commands: List[MakeCommand] = field(default_factory=list)
    
    def accept(self, visitor: 'MakeVisitor') -> Any:
        return visitor.visit_suffix_rule(self)

# Visitor Pattern

class MakeVisitor(ABC):
    """Abstract visitor for Make AST traversal"""
    
    @abstractmethod
    def visit_makefile(self, node: MakeFile) -> Any:
        pass
    
    @abstractmethod
    def visit_variable(self, node: MakeVariable) -> Any:
        pass
    
    @abstractmethod
    def visit_variable_reference(self, node: VariableReference) -> Any:
        pass
    
    @abstractmethod
    def visit_automatic_variable(self, node: AutomaticVariable) -> Any:
        pass
    
    @abstractmethod
    def visit_rule(self, node: MakeRule) -> Any:
        pass
    
    @abstractmethod
    def visit_target(self, node: MakeTarget) -> Any:
        pass
    
    @abstractmethod
    def visit_command(self, node: MakeCommand) -> Any:
        pass
    
    @abstractmethod
    def visit_function(self, node: MakeFunction) -> Any:
        pass
    
    @abstractmethod
    def visit_user_function(self, node: UserDefinedFunction) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional(self, node: MakeConditional) -> Any:
        pass
    
    @abstractmethod
    def visit_conditional_expression(self, node: ConditionalExpression) -> Any:
        pass
    
    @abstractmethod
    def visit_include(self, node: MakeInclude) -> Any:
        pass
    
    @abstractmethod
    def visit_vpath(self, node: VPathDirective) -> Any:
        pass
    
    @abstractmethod
    def visit_export(self, node: ExportDirective) -> Any:
        pass
    
    @abstractmethod
    def visit_text_literal(self, node: TextLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_concatenated_text(self, node: ConcatenatedText) -> Any:
        pass
    
    @abstractmethod
    def visit_comment(self, node: MakeComment) -> Any:
        pass
    
    @abstractmethod
    def visit_special_target(self, node: SpecialTarget) -> Any:
        pass
    
    @abstractmethod
    def visit_suffix_rule(self, node: SuffixRule) -> Any:
        pass

# Utility Functions

def create_simple_rule(target: str, dependencies: List[str] = None, commands: List[str] = None) -> MakeRule:
    """Create a simple Make rule"""
    deps = dependencies or []
    cmds = [MakeCommand(cmd) for cmd in (commands or [])]
    return MakeRule(targets=[target], dependencies=deps, commands=cmds)

def create_variable(name: str, value: str, assignment_type: str = "=") -> MakeVariable:
    """Create a simple Make variable"""
    return MakeVariable(name=name, value=TextLiteral(value), assignment_type=assignment_type)

def create_function_call(name: str, *args: str) -> MakeFunction:
    """Create a function call with string arguments"""
    arguments = [TextLiteral(arg) for arg in args]
    return MakeFunction(name=name, arguments=arguments, is_builtin=True)

# AST Builder for common patterns
class MakeASTBuilder:
    """Builder for constructing Make AST nodes"""
    
    def __init__(self):
        self.statements: List[MakeStatement] = []
    
    def add_variable(self, name: str, value: str, assignment_type: str = "=") -> 'MakeASTBuilder':
        """Add a variable definition"""
        var = create_variable(name, value, assignment_type)
        self.statements.append(var)
        return self
    
    def add_rule(self, target: str, dependencies: List[str] = None, commands: List[str] = None) -> 'MakeASTBuilder':
        """Add a rule"""
        rule = create_simple_rule(target, dependencies, commands)
        self.statements.append(rule)
        return self
    
    def add_comment(self, text: str) -> 'MakeASTBuilder':
        """Add a comment"""
        comment = MakeComment(text=text)
        self.statements.append(comment)
        return self
    
    def add_include(self, *filenames: str, optional: bool = False) -> 'MakeASTBuilder':
        """Add an include directive"""
        include = MakeInclude(filenames=list(filenames), is_optional=optional)
        self.statements.append(include)
        return self
    
    def build(self) -> MakeFile:
        """Build the final MakeFile AST"""
        return MakeFile(statements=self.statements)

# Export main classes
__all__ = [
    # Base classes
    'MakeNode', 'MakeExpression', 'MakeStatement', 'MakeVisitor',
    
    # Core nodes
    'MakeFile', 'MakeVariable', 'VariableReference', 'AutomaticVariable',
    'MakeRule', 'MakeTarget', 'MakeCommand', 'MakeFunction', 'UserDefinedFunction',
    
    # Built-in functions
    'SubstFunction', 'PatsubstFunction', 'WildcardFunction', 'ShellFunction',
    
    # Conditionals
    'MakeConditional', 'ConditionalExpression',
    
    # Directives
    'MakeInclude', 'VPathDirective', 'ExportDirective',
    
    # Text and literals
    'TextLiteral', 'ConcatenatedText', 'MakeComment',
    
    # Special constructs
    'SpecialTarget', 'SuffixRule',
    
    # Utilities
    'create_simple_rule', 'create_variable', 'create_function_call', 'MakeASTBuilder'
] 