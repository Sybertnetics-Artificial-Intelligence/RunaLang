"""
Tcl AST (Abstract Syntax Tree) Implementation for Runa Universal Translation Platform

This module provides comprehensive AST node definitions for the Tcl (Tool Command Language),
supporting automation scripting, system administration, and embedded applications.

Tcl is renowned for its simplicity, power, and "everything is a string" philosophy,
making it ideal for:
- System automation and scripting
- Configuration management
- Text processing and manipulation
- Embedded scripting in applications
- Cross-platform automation tasks
- GUI development (with Tk)

Key Tcl Features Supported:
- Simple command-based syntax
- Variable and command substitution
- String manipulation and processing
- Control structures (if, while, for, foreach)
- Procedures and namespaces
- Package system and modules
- List processing and manipulation
- Regular expression support
- File I/O and system interaction
- Error handling (try/catch)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum
import uuid

from ...core.ast_base import ASTNode

class TclNodeType(Enum):
    """Tcl-specific AST node types"""
    # Program structure
    SCRIPT = "script"
    COMMAND = "command"
    WORD = "word"
    
    # Procedures and namespaces
    PROC = "proc"
    NAMESPACE = "namespace"
    PACKAGE = "package"
    
    # Control structures
    IF = "if"
    WHILE = "while"
    FOR = "for"
    FOREACH = "foreach"
    SWITCH = "switch"
    TRY = "try"
    CATCH = "catch"
    
    # Substitutions
    VARIABLE_SUBSTITUTION = "variable_substitution"
    COMMAND_SUBSTITUTION = "command_substitution"
    BACKSLASH_SUBSTITUTION = "backslash_substitution"
    
    # Variables and arrays
    VARIABLE = "variable"
    ARRAY_ELEMENT = "array_element"
    GLOBAL_VAR = "global_var"
    UPVAR = "upvar"
    
    # String and list operations
    STRING_LITERAL = "string_literal"
    QUOTED_STRING = "quoted_string"
    BRACED_STRING = "braced_string"
    LIST = "list"
    LIST_ELEMENT = "list_element"
    
    # File and I/O
    OPEN = "open"
    CLOSE = "close"
    READ = "read"
    PUTS = "puts"
    GETS = "gets"
    
    # Regular expressions
    REGEXP = "regexp"
    REGSUB = "regsub"
    
    # String manipulation
    STRING_MATCH = "string_match"
    STRING_MAP = "string_map"
    STRING_RANGE = "string_range"
    STRING_INDEX = "string_index"
    
    # List manipulation
    LAPPEND = "lappend"
    LINDEX = "lindex"
    LINSERT = "linsert"
    LLENGTH = "llength"
    LRANGE = "lrange"
    LREPLACE = "lreplace"
    LSEARCH = "lsearch"
    LSORT = "lsort"
    
    # System interaction
    EXEC = "exec"
    SOURCE = "source"
    EVAL = "eval"
    
    # Error handling
    ERROR = "error"
    RETURN = "return"
    BREAK = "break"
    CONTINUE = "continue"
    
    # Special constructs
    EXPR = "expr"
    INCR = "incr"
    SET = "set"
    UNSET = "unset"
    INFO = "info"
    
    # Comments
    COMMENT = "comment"

@dataclass
class TclNode(ASTNode):
    """Base class for all Tcl AST nodes"""
    node_type: TclNodeType
    source_location: Optional[Dict[str, int]] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if self.node_id is None:
            self.node_id = str(uuid.uuid4())

@dataclass
class TclScript(TclNode):
    """Tcl script (top-level container)"""
    commands: List['TclCommand'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.SCRIPT

@dataclass
class TclCommand(TclNode):
    """Tcl command"""
    command_name: str
    arguments: List['TclWord'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.COMMAND

@dataclass
class TclWord(TclNode):
    """Tcl word (basic unit)"""
    content: Union[str, List['TclSubstitution']]
    is_quoted: bool = False
    is_braced: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.WORD

@dataclass
class TclSubstitution(TclNode):
    """Base class for Tcl substitutions"""
    pass

@dataclass
class TclVariableSubstitution(TclSubstitution):
    """Variable substitution ($var or ${var})"""
    variable_name: str
    array_index: Optional['TclWord'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.VARIABLE_SUBSTITUTION

@dataclass
class TclCommandSubstitution(TclSubstitution):
    """Command substitution ([command])"""
    command: 'TclCommand'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.COMMAND_SUBSTITUTION

@dataclass
class TclBackslashSubstitution(TclSubstitution):
    """Backslash substitution (\\n, \\t, etc.)"""
    escape_sequence: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.BACKSLASH_SUBSTITUTION

# Procedures and namespaces

@dataclass
class TclProc(TclNode):
    """Tcl procedure definition"""
    name: str
    parameters: List[str] = field(default_factory=list)
    default_values: Dict[str, 'TclWord'] = field(default_factory=dict)
    body: 'TclScript' = field(default_factory=lambda: TclScript())
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.PROC

@dataclass
class TclNamespace(TclNode):
    """Tcl namespace"""
    name: str
    body: 'TclScript' = field(default_factory=lambda: TclScript())
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.NAMESPACE

@dataclass
class TclPackage(TclNode):
    """Tcl package declaration"""
    name: str
    version: str
    requirements: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.PACKAGE

# Control structures

@dataclass
class TclIf(TclNode):
    """Tcl if statement"""
    condition: 'TclWord'
    then_body: 'TclScript'
    elseif_clauses: List['TclElseIf'] = field(default_factory=list)
    else_body: Optional['TclScript'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.IF

@dataclass
class TclElseIf(TclNode):
    """Tcl elseif clause"""
    condition: 'TclWord'
    body: 'TclScript'

@dataclass
class TclWhile(TclNode):
    """Tcl while loop"""
    condition: 'TclWord'
    body: 'TclScript'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.WHILE

@dataclass
class TclFor(TclNode):
    """Tcl for loop"""
    init: 'TclScript'
    condition: 'TclWord'
    increment: 'TclScript'
    body: 'TclScript'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.FOR

@dataclass
class TclForeach(TclNode):
    """Tcl foreach loop"""
    variables: List[str]
    list_expr: 'TclWord'
    body: 'TclScript'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.FOREACH

@dataclass
class TclSwitch(TclNode):
    """Tcl switch statement"""
    expression: 'TclWord'
    patterns: List['TclSwitchPattern'] = field(default_factory=list)
    default_body: Optional['TclScript'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.SWITCH

@dataclass
class TclSwitchPattern(TclNode):
    """Tcl switch pattern"""
    pattern: 'TclWord'
    body: 'TclScript'

@dataclass
class TclTry(TclNode):
    """Tcl try statement"""
    try_body: 'TclScript'
    catch_clauses: List['TclCatch'] = field(default_factory=list)
    finally_body: Optional['TclScript'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.TRY

@dataclass
class TclCatch(TclNode):
    """Tcl catch clause"""
    error_types: List[str] = field(default_factory=list)
    variable_name: Optional[str] = None
    body: 'TclScript' = field(default_factory=lambda: TclScript())
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.CATCH

# Variables and data structures

@dataclass
class TclVariable(TclNode):
    """Tcl variable"""
    name: str
    namespace: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.VARIABLE

@dataclass
class TclArrayElement(TclNode):
    """Tcl array element"""
    array_name: str
    index: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.ARRAY_ELEMENT

@dataclass
class TclSet(TclNode):
    """Tcl set command"""
    variable: Union['TclVariable', 'TclArrayElement']
    value: Optional['TclWord'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.SET

@dataclass
class TclGlobal(TclNode):
    """Tcl global declaration"""
    variables: List[str]
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.GLOBAL_VAR

@dataclass
class TclUpvar(TclNode):
    """Tcl upvar declaration"""
    level: str
    other_var: str
    my_var: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.UPVAR

# String and list operations

@dataclass
class TclStringLiteral(TclNode):
    """Tcl string literal"""
    value: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.STRING_LITERAL

@dataclass
class TclQuotedString(TclNode):
    """Tcl quoted string with substitutions"""
    content: List[Union[str, TclSubstitution]]
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.QUOTED_STRING

@dataclass
class TclBracedString(TclNode):
    """Tcl braced string (no substitutions)"""
    content: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.BRACED_STRING

@dataclass
class TclList(TclNode):
    """Tcl list"""
    elements: List['TclWord'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.LIST

# String manipulation commands

@dataclass
class TclStringMatch(TclNode):
    """string match command"""
    pattern: 'TclWord'
    string: 'TclWord'
    nocase: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.STRING_MATCH

@dataclass
class TclStringMap(TclNode):
    """string map command"""
    mapping: 'TclWord'
    string: 'TclWord'
    nocase: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.STRING_MAP

@dataclass
class TclStringRange(TclNode):
    """string range command"""
    string: 'TclWord'
    first: 'TclWord'
    last: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.STRING_RANGE

@dataclass
class TclStringIndex(TclNode):
    """string index command"""
    string: 'TclWord'
    index: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.STRING_INDEX

# List manipulation commands

@dataclass
class TclLappend(TclNode):
    """lappend command"""
    list_var: str
    values: List['TclWord'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.LAPPEND

@dataclass
class TclLindex(TclNode):
    """lindex command"""
    list_expr: 'TclWord'
    index: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.LINDEX

@dataclass
class TclLlength(TclNode):
    """llength command"""
    list_expr: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.LLENGTH

@dataclass
class TclLrange(TclNode):
    """lrange command"""
    list_expr: 'TclWord'
    first: 'TclWord'
    last: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.LRANGE

@dataclass
class TclLsort(TclNode):
    """lsort command"""
    list_expr: 'TclWord'
    options: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.LSORT

# Regular expressions

@dataclass
class TclRegexp(TclNode):
    """regexp command"""
    pattern: 'TclWord'
    string: 'TclWord'
    match_vars: List[str] = field(default_factory=list)
    options: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.REGEXP

@dataclass
class TclRegsub(TclNode):
    """regsub command"""
    pattern: 'TclWord'
    string: 'TclWord'
    replacement: 'TclWord'
    var_name: Optional[str] = None
    options: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.REGSUB

# File I/O

@dataclass
class TclOpen(TclNode):
    """open command"""
    filename: 'TclWord'
    access: Optional['TclWord'] = None
    permissions: Optional['TclWord'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.OPEN

@dataclass
class TclClose(TclNode):
    """close command"""
    channel: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.CLOSE

@dataclass
class TclPuts(TclNode):
    """puts command"""
    channel: Optional['TclWord'] = None
    string: 'TclWord' = field(default_factory=lambda: TclWord(content=""))
    nonewline: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.PUTS

@dataclass
class TclGets(TclNode):
    """gets command"""
    channel: 'TclWord'
    var_name: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.GETS

@dataclass
class TclRead(TclNode):
    """read command"""
    channel: 'TclWord'
    num_chars: Optional['TclWord'] = None
    nonewline: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.READ

# System interaction

@dataclass
class TclExec(TclNode):
    """exec command"""
    program: 'TclWord'
    arguments: List['TclWord'] = field(default_factory=list)
    options: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.EXEC

@dataclass
class TclSource(TclNode):
    """source command"""
    filename: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.SOURCE

@dataclass
class TclEval(TclNode):
    """eval command"""
    script: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.EVAL

# Error handling and control flow

@dataclass
class TclError(TclNode):
    """error command"""
    message: 'TclWord'
    info: Optional['TclWord'] = None
    code: Optional['TclWord'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.ERROR

@dataclass
class TclReturn(TclNode):
    """return command"""
    value: Optional['TclWord'] = None
    code: Optional['TclWord'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.RETURN

@dataclass
class TclBreak(TclNode):
    """break command"""
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.BREAK

@dataclass
class TclContinue(TclNode):
    """continue command"""
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.CONTINUE

# Special commands

@dataclass
class TclExpr(TclNode):
    """expr command"""
    expression: 'TclWord'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.EXPR

@dataclass
class TclIncr(TclNode):
    """incr command"""
    variable: 'TclVariable'
    increment: Optional['TclWord'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.INCR

@dataclass
class TclUnset(TclNode):
    """unset command"""
    variables: List[str]
    nocomplain: bool = False
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.UNSET

@dataclass
class TclInfo(TclNode):
    """info command"""
    subcommand: str
    arguments: List['TclWord'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.INFO

@dataclass
class TclComment(TclNode):
    """Tcl comment"""
    text: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = TclNodeType.COMMENT

# Utility functions for creating common Tcl constructs

def create_tcl_script() -> TclScript:
    """Create an empty Tcl script"""
    return TclScript()

def create_tcl_command(name: str, *args: str) -> TclCommand:
    """Create a Tcl command with arguments"""
    arguments = [TclWord(content=arg) for arg in args]
    return TclCommand(command_name=name, arguments=arguments)

def create_tcl_proc(name: str, params: List[str], body: str) -> TclProc:
    """Create a Tcl procedure"""
    script = TclScript(commands=[TclCommand(command_name="# body", arguments=[])])
    return TclProc(name=name, parameters=params, body=script)

def create_tcl_if(condition: str, then_body: str, else_body: str = None) -> TclIf:
    """Create a Tcl if statement"""
    then_script = TclScript()
    else_script = TclScript() if else_body else None
    
    return TclIf(
        condition=TclWord(content=condition),
        then_body=then_script,
        else_body=else_script
    )

def create_tcl_while(condition: str, body: str) -> TclWhile:
    """Create a Tcl while loop"""
    body_script = TclScript()
    
    return TclWhile(
        condition=TclWord(content=condition),
        body=body_script
    )

def create_tcl_foreach(var: str, list_expr: str, body: str) -> TclForeach:
    """Create a Tcl foreach loop"""
    body_script = TclScript()
    
    return TclForeach(
        variables=[var],
        list_expr=TclWord(content=list_expr),
        body=body_script
    )

def create_tcl_variable_substitution(var_name: str) -> TclVariableSubstitution:
    """Create a Tcl variable substitution"""
    return TclVariableSubstitution(variable_name=var_name)

def create_tcl_command_substitution(command: str) -> TclCommandSubstitution:
    """Create a Tcl command substitution"""
    cmd = TclCommand(command_name=command, arguments=[])
    return TclCommandSubstitution(command=cmd)

def create_tcl_list(*elements: str) -> TclList:
    """Create a Tcl list"""
    list_elements = [TclWord(content=elem) for elem in elements]
    return TclList(elements=list_elements) 