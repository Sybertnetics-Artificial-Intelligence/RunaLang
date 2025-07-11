#!/usr/bin/env python3
"""
Shell Script AST Node Definitions

Complete Shell Script Abstract Syntax Tree node definitions for the Runa
universal translation system supporting POSIX shell, Bash, and modern shell features.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


class ShellNodeType(Enum):
    """Shell node types."""
    SCRIPT = "script"
    COMMAND = "command"
    PIPELINE = "pipeline"
    COMPOUND_COMMAND = "compound_command"
    FUNCTION_DEFINITION = "function_definition"
    VARIABLE_ASSIGNMENT = "variable_assignment"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    REDIRECTION = "redirection"
    PARAMETER_EXPANSION = "parameter_expansion"
    COMMAND_SUBSTITUTION = "command_substitution"
    ARITHMETIC_EXPANSION = "arithmetic_expansion"
    COMMENT = "comment"


class ShellVisitor(ABC):
    """Visitor interface for Shell AST nodes."""
    
    @abstractmethod
    def visit_shell_script(self, node: 'ShellScript'): pass
    
    @abstractmethod
    def visit_shell_command(self, node: 'ShellCommand'): pass
    
    @abstractmethod
    def visit_shell_pipeline(self, node: 'ShellPipeline'): pass
    
    @abstractmethod
    def visit_shell_compound_command(self, node: 'ShellCompoundCommand'): pass
    
    @abstractmethod
    def visit_shell_function_definition(self, node: 'ShellFunctionDefinition'): pass
    
    @abstractmethod
    def visit_shell_variable_assignment(self, node: 'ShellVariableAssignment'): pass
    
    @abstractmethod
    def visit_shell_conditional(self, node: 'ShellConditional'): pass
    
    @abstractmethod
    def visit_shell_loop(self, node: 'ShellLoop'): pass
    
    @abstractmethod
    def visit_shell_redirection(self, node: 'ShellRedirection'): pass
    
    @abstractmethod
    def visit_shell_expansion(self, node: 'ShellExpansion'): pass
    
    @abstractmethod
    def visit_shell_comment(self, node: 'ShellComment'): pass


class ShellNode(ABC):
    """Base class for all Shell AST nodes."""
    
    @abstractmethod
    def accept(self, visitor: ShellVisitor) -> Any:
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class ShellScript(ShellNode):
    """Shell script root."""
    statements: List['ShellStatement'] = field(default_factory=list)
    shebang: Optional[str] = None
    comments: List['ShellComment'] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    functions: List['ShellFunctionDefinition'] = field(default_factory=list)
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_script(self)
    
    def add_statement(self, statement: 'ShellStatement'):
        """Add a statement to the script."""
        self.statements.append(statement)
    
    def add_comment(self, comment: 'ShellComment'):
        """Add a comment to the script."""
        self.comments.append(comment)
    
    def add_function(self, function: 'ShellFunctionDefinition'):
        """Add a function definition."""
        self.functions.append(function)
    
    def find_function(self, name: str) -> Optional['ShellFunctionDefinition']:
        """Find function by name."""
        for func in self.functions:
            if func.name == name:
                return func
        return None
    
    def get_variable_assignments(self) -> List['ShellVariableAssignment']:
        """Get all variable assignments in script."""
        assignments = []
        for stmt in self.statements:
            if isinstance(stmt, ShellVariableAssignment):
                assignments.append(stmt)
        return assignments


class ShellStatement(ShellNode):
    """Base class for shell statements."""
    pass


@dataclass
class ShellCommand(ShellStatement):
    """Shell command (simple command)."""
    command: str
    arguments: List[str] = field(default_factory=list)
    redirections: List['ShellRedirection'] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    background: bool = False
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_command(self)
    
    def add_argument(self, arg: str):
        """Add an argument to the command."""
        self.arguments.append(arg)
    
    def add_redirection(self, redirection: 'ShellRedirection'):
        """Add a redirection to the command."""
        self.redirections.append(redirection)
    
    def get_full_command(self) -> str:
        """Get full command with arguments."""
        parts = [self.command] + self.arguments
        return " ".join(parts)
    
    @property
    def is_builtin(self) -> bool:
        """Check if command is a shell builtin."""
        builtins = {
            'echo', 'printf', 'cd', 'pwd', 'ls', 'cp', 'mv', 'rm', 'mkdir', 'rmdir',
            'cat', 'grep', 'sed', 'awk', 'sort', 'uniq', 'head', 'tail', 'wc',
            'find', 'which', 'type', 'alias', 'unalias', 'history', 'jobs', 'fg', 'bg',
            'kill', 'killall', 'ps', 'top', 'nohup', 'screen', 'tmux',
            'export', 'unset', 'set', 'readonly', 'local', 'declare', 'typeset',
            'test', '[', 'true', 'false', 'exit', 'return', 'break', 'continue',
            'source', '.', 'exec', 'eval', 'shift', 'getopts', 'read', 'trap'
        }
        return self.command in builtins


@dataclass
class ShellPipeline(ShellStatement):
    """Shell pipeline (command1 | command2 | ...)."""
    commands: List[ShellCommand] = field(default_factory=list)
    negated: bool = False
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_pipeline(self)
    
    def add_command(self, command: ShellCommand):
        """Add a command to the pipeline."""
        self.commands.append(command)
    
    def get_pipeline_string(self) -> str:
        """Get pipeline as string."""
        cmd_strings = [cmd.get_full_command() for cmd in self.commands]
        pipeline = " | ".join(cmd_strings)
        if self.negated:
            pipeline = "! " + pipeline
        return pipeline


@dataclass
class ShellCompoundCommand(ShellStatement):
    """Shell compound command (subshell, command group, etc.)."""
    command_type: str  # "subshell", "group", "arithmetic", "conditional"
    body: List[ShellStatement] = field(default_factory=list)
    test_expression: Optional[str] = None
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_compound_command(self)
    
    def add_statement(self, statement: ShellStatement):
        """Add a statement to the compound command."""
        self.body.append(statement)
    
    @property
    def is_subshell(self) -> bool:
        """Check if this is a subshell command."""
        return self.command_type == "subshell"
    
    @property
    def is_group(self) -> bool:
        """Check if this is a command group."""
        return self.command_type == "group"


@dataclass
class ShellFunctionDefinition(ShellStatement):
    """Shell function definition."""
    name: str
    body: List[ShellStatement] = field(default_factory=list)
    parameters: List[str] = field(default_factory=list)
    local_variables: Dict[str, str] = field(default_factory=dict)
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_function_definition(self)
    
    def add_statement(self, statement: ShellStatement):
        """Add a statement to the function body."""
        self.body.append(statement)
    
    def add_parameter(self, param: str):
        """Add a parameter to the function."""
        self.parameters.append(param)


@dataclass
class ShellVariableAssignment(ShellStatement):
    """Shell variable assignment."""
    variable: str
    value: str
    export: bool = False
    readonly: bool = False
    local: bool = False
    array: bool = False
    array_values: List[str] = field(default_factory=list)
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_variable_assignment(self)
    
    def get_assignment_string(self) -> str:
        """Get assignment as string."""
        if self.array:
            values = " ".join(f'"{val}"' for val in self.array_values)
            assignment = f"{self.variable}=({values})"
        else:
            assignment = f'{self.variable}="{self.value}"'
        
        if self.export:
            assignment = "export " + assignment
        elif self.readonly:
            assignment = "readonly " + assignment
        elif self.local:
            assignment = "local " + assignment
        
        return assignment


@dataclass
class ShellConditional(ShellStatement):
    """Shell conditional statement (if, case, etc.)."""
    conditional_type: str  # "if", "case", "test"
    condition: str
    then_body: List[ShellStatement] = field(default_factory=list)
    else_body: List[ShellStatement] = field(default_factory=list)
    elif_clauses: List[Tuple[str, List[ShellStatement]]] = field(default_factory=list)
    case_patterns: List[Tuple[str, List[ShellStatement]]] = field(default_factory=list)
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_conditional(self)
    
    def add_then_statement(self, statement: ShellStatement):
        """Add statement to then body."""
        self.then_body.append(statement)
    
    def add_else_statement(self, statement: ShellStatement):
        """Add statement to else body."""
        self.else_body.append(statement)
    
    def add_elif_clause(self, condition: str, body: List[ShellStatement]):
        """Add elif clause."""
        self.elif_clauses.append((condition, body))
    
    def add_case_pattern(self, pattern: str, body: List[ShellStatement]):
        """Add case pattern."""
        self.case_patterns.append((pattern, body))
    
    @property
    def is_if_statement(self) -> bool:
        """Check if this is an if statement."""
        return self.conditional_type == "if"
    
    @property
    def is_case_statement(self) -> bool:
        """Check if this is a case statement."""
        return self.conditional_type == "case"


@dataclass
class ShellLoop(ShellStatement):
    """Shell loop statement (for, while, until)."""
    loop_type: str  # "for", "while", "until"
    condition: str
    body: List[ShellStatement] = field(default_factory=list)
    variable: Optional[str] = None
    iterable: Optional[str] = None
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_loop(self)
    
    def add_statement(self, statement: ShellStatement):
        """Add statement to loop body."""
        self.body.append(statement)
    
    @property
    def is_for_loop(self) -> bool:
        """Check if this is a for loop."""
        return self.loop_type == "for"
    
    @property
    def is_while_loop(self) -> bool:
        """Check if this is a while loop."""
        return self.loop_type == "while"
    
    @property
    def is_until_loop(self) -> bool:
        """Check if this is an until loop."""
        return self.loop_type == "until"


@dataclass
class ShellRedirection(ShellNode):
    """Shell I/O redirection."""
    redirection_type: str  # ">", ">>", "<", "<<", "2>", "2>>", "&>", etc.
    target: str
    file_descriptor: Optional[int] = None
    here_document: bool = False
    here_string: bool = False
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_redirection(self)
    
    def get_redirection_string(self) -> str:
        """Get redirection as string."""
        if self.file_descriptor is not None:
            return f"{self.file_descriptor}{self.redirection_type}{self.target}"
        return f"{self.redirection_type}{self.target}"
    
    @property
    def is_output_redirection(self) -> bool:
        """Check if this is output redirection."""
        return self.redirection_type in (">", ">>", "2>", "2>>", "&>", "&>>")
    
    @property
    def is_input_redirection(self) -> bool:
        """Check if this is input redirection."""
        return self.redirection_type in ("<", "<<", "<<<")


class ShellExpansion(ShellNode):
    """Base class for shell expansions."""
    pass


@dataclass
class ShellParameterExpansion(ShellExpansion):
    """Shell parameter expansion (${var}, etc.)."""
    parameter: str
    expansion_type: str = "simple"  # "simple", "default", "assign", "error", "substring", etc.
    modifier: Optional[str] = None
    default_value: Optional[str] = None
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_expansion(self)
    
    def get_expansion_string(self) -> str:
        """Get expansion as string."""
        if self.expansion_type == "simple":
            return f"${{{self.parameter}}}"
        elif self.expansion_type == "default" and self.default_value:
            return f"${{{self.parameter}:-{self.default_value}}}"
        elif self.expansion_type == "assign" and self.default_value:
            return f"${{{self.parameter}:={self.default_value}}}"
        elif self.expansion_type == "error" and self.default_value:
            return f"${{{self.parameter}:?{self.default_value}}}"
        elif self.expansion_type == "substring" and self.modifier:
            return f"${{{self.parameter}:{self.modifier}}}"
        else:
            return f"${{{self.parameter}}}"


@dataclass
class ShellCommandSubstitution(ShellExpansion):
    """Shell command substitution ($(...) or `...`)."""
    command: str
    backtick_style: bool = False
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_expansion(self)
    
    def get_substitution_string(self) -> str:
        """Get substitution as string."""
        if self.backtick_style:
            return f"`{self.command}`"
        return f"$({self.command})"


@dataclass
class ShellArithmeticExpansion(ShellExpansion):
    """Shell arithmetic expansion ($((expr)))."""
    expression: str
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_expansion(self)
    
    def get_expansion_string(self) -> str:
        """Get expansion as string."""
        return f"$(({self.expression}))"


@dataclass
class ShellComment(ShellNode):
    """Shell comment."""
    text: str
    inline: bool = False
    
    def accept(self, visitor: ShellVisitor) -> Any:
        return visitor.visit_shell_comment(self)


# Shell-specific utility classes
@dataclass
class ShellGlob:
    """Shell glob pattern."""
    pattern: str
    case_insensitive: bool = False
    
    def matches(self, text: str) -> bool:
        """Check if pattern matches text (simplified)."""
        import fnmatch
        return fnmatch.fnmatch(text, self.pattern)


@dataclass
class ShellProcess:
    """Shell process information."""
    pid: Optional[int] = None
    command: str = ""
    exit_code: Optional[int] = None
    background: bool = False


# Utility functions
def create_shell_script(shebang: str = "#!/bin/bash") -> ShellScript:
    """Create an empty shell script."""
    return ShellScript(shebang=shebang)


def create_shell_command(command: str, *args: str) -> ShellCommand:
    """Create a shell command."""
    return ShellCommand(command=command, arguments=list(args))


def create_shell_pipeline(*commands: ShellCommand) -> ShellPipeline:
    """Create a shell pipeline."""
    return ShellPipeline(commands=list(commands))


def create_shell_function(name: str, *statements: ShellStatement) -> ShellFunctionDefinition:
    """Create a shell function."""
    return ShellFunctionDefinition(name=name, body=list(statements))


def create_shell_variable_assignment(variable: str, value: str, **kwargs) -> ShellVariableAssignment:
    """Create a variable assignment."""
    return ShellVariableAssignment(variable=variable, value=value, **kwargs)


def create_shell_if(condition: str, then_body: List[ShellStatement], 
                   else_body: Optional[List[ShellStatement]] = None) -> ShellConditional:
    """Create an if statement."""
    return ShellConditional(
        conditional_type="if",
        condition=condition,
        then_body=then_body,
        else_body=else_body or []
    )


def create_shell_for_loop(variable: str, iterable: str, body: List[ShellStatement]) -> ShellLoop:
    """Create a for loop."""
    return ShellLoop(
        loop_type="for",
        condition=f"{variable} in {iterable}",
        variable=variable,
        iterable=iterable,
        body=body
    )


def create_shell_while_loop(condition: str, body: List[ShellStatement]) -> ShellLoop:
    """Create a while loop."""
    return ShellLoop(
        loop_type="while",
        condition=condition,
        body=body
    )


def create_shell_redirection(redirection_type: str, target: str, **kwargs) -> ShellRedirection:
    """Create a redirection."""
    return ShellRedirection(redirection_type=redirection_type, target=target, **kwargs)


def create_shell_comment(text: str, inline: bool = False) -> ShellComment:
    """Create a comment."""
    return ShellComment(text=text, inline=inline)


def parse_shell_command_line(command_line: str) -> ShellCommand:
    """Parse command line into command and arguments (simplified)."""
    parts = command_line.strip().split()
    if not parts:
        return ShellCommand(command="")
    
    command = parts[0]
    arguments = parts[1:] if len(parts) > 1 else []
    
    return ShellCommand(command=command, arguments=arguments)


def is_shell_special_character(char: str) -> bool:
    """Check if character is a shell special character."""
    special_chars = {'|', '&', ';', '(', ')', '<', '>', ' ', '\t', '\n', '$', '`', '\\', '"', "'", '?', '*', '[', ']', '{', '}'}
    return char in special_chars


def escape_shell_string(text: str, quote_style: str = "double") -> str:
    """Escape string for shell."""
    if quote_style == "single":
        # Single quotes preserve everything literally
        return f"'{text.replace(\"'\", \"'\\\"'\\\"'\")}'"
    else:
        # Double quotes allow variable expansion but escape special chars
        escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
        return f'"{escaped}"'


def get_shell_builtin_commands() -> List[str]:
    """Get list of common shell builtin commands."""
    return [
        'echo', 'printf', 'read', 'cd', 'pwd', 'pushd', 'popd', 'dirs',
        'export', 'unset', 'set', 'unalias', 'alias', 'type', 'which',
        'history', 'fc', 'jobs', 'fg', 'bg', 'kill', 'wait', 'sleep',
        'test', '[', 'true', 'false', 'exit', 'return', 'break', 'continue',
        'source', '.', 'exec', 'eval', 'shift', 'getopts', 'trap', 'ulimit',
        'umask', 'times', 'help', 'bind', 'builtin', 'command', 'enable',
        'hash', 'readonly', 'local', 'declare', 'typeset', 'let', 'caller'
    ]


def get_shell_reserved_words() -> List[str]:
    """Get list of shell reserved words."""
    return [
        'if', 'then', 'else', 'elif', 'fi', 'case', 'esac', 'for', 'select',
        'while', 'until', 'do', 'done', 'function', 'time', 'coproc',
        'in', '!', '{', '}', '[[', ']]', '(', ')'
    ]


def normalize_shell_command(command: str) -> str:
    """Normalize shell command."""
    return command.strip().lower()


def shell_to_dict(script: ShellScript) -> Dict[str, Any]:
    """Convert shell script to dictionary representation."""
    result = {
        "type": "script",
        "shebang": script.shebang,
        "statements": len(script.statements),
        "functions": len(script.functions),
        "variables": len(script.variables),
        "comments": len(script.comments)
    }
    
    return result


def dict_to_shell(data: Dict[str, Any]) -> ShellScript:
    """Convert dictionary to shell script (basic implementation)."""
    script = ShellScript()
    
    if "shebang" in data:
        script.shebang = data["shebang"]
    
    return script


# Extended visitor for additional functionality
class ShellVisitorExtended(ShellVisitor):
    """Extended visitor with additional methods."""
    pass