"""
Perl AST (Abstract Syntax Tree) Implementation for Runa Universal Translation Platform

This module provides comprehensive AST node definitions for the Perl programming language,
supporting Perl 5 with its powerful text processing, regular expressions, and flexible syntax.

Perl is renowned for its text processing capabilities and "There's More Than One Way To Do It"
(TMTOWTDI) philosophy, making it ideal for system administration, bioinformatics, web development,
and data munging tasks.

Key Perl Features Supported:
- Scalars, arrays, hashes, and typeglobs
- Regular expressions with advanced pattern matching
- References and complex data structures
- Subroutines with flexible parameter handling
- Object-oriented programming (blessing)
- Modules and packages (namespaces)
- Context-sensitive operations (scalar vs list context)
- Special variables ($_, @_, %ENV, etc.)
- File handles and I/O operations
- CPAN module system integration

Text Processing Features:
- Powerful regex engine with backreferences
- String interpolation and here documents
- Pattern matching and substitution operators
- Text splitting and joining operations
- Format statements for report generation
- Locale and Unicode support

Advanced Features:
- Dynamic symbol table manipulation
- Eval for runtime code execution
- Tie mechanisms for magic variables
- Source filters and code modification
- XS interface for C integration
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from enum import Enum
import uuid

from ...core.ast_base import ASTNode

class PerlNodeType(Enum):
    """Perl-specific AST node types"""
    # Program structure
    PROGRAM = "program"
    PACKAGE = "package"
    MODULE = "module"
    USE_STATEMENT = "use_statement"
    REQUIRE_STATEMENT = "require_statement"
    
    # Variable declarations and types
    SCALAR_VARIABLE = "scalar_variable"
    ARRAY_VARIABLE = "array_variable"
    HASH_VARIABLE = "hash_variable"
    TYPEGLOB = "typeglob"
    REFERENCE = "reference"
    DEREFERENCE = "dereference"
    
    # Subroutines and functions
    SUBROUTINE_DECLARATION = "subroutine_declaration"
    SUBROUTINE_CALL = "subroutine_call"
    ANONYMOUS_SUBROUTINE = "anonymous_subroutine"
    
    # Control structures
    IF_STATEMENT = "if_statement"
    UNLESS_STATEMENT = "unless_statement"
    WHILE_LOOP = "while_loop"
    UNTIL_LOOP = "until_loop"
    FOR_LOOP = "for_loop"
    FOREACH_LOOP = "foreach_loop"
    GIVEN_WHEN = "given_when"
    
    # Operators and expressions
    ASSIGNMENT = "assignment"
    BINARY_OPERATION = "binary_operation"
    UNARY_OPERATION = "unary_operation"
    TERNARY_OPERATION = "ternary_operation"
    REGEX_MATCH = "regex_match"
    REGEX_SUBSTITUTION = "regex_substitution"
    REGEX_TRANSLITERATION = "regex_transliteration"
    
    # String and regex
    STRING_LITERAL = "string_literal"
    REGEX_LITERAL = "regex_literal"
    HERE_DOCUMENT = "here_document"
    INTERPOLATED_STRING = "interpolated_string"
    QUOTED_WORD_LIST = "quoted_word_list"
    
    # Data structures
    ARRAY_LITERAL = "array_literal"
    HASH_LITERAL = "hash_literal"
    ARRAY_SLICE = "array_slice"
    HASH_SLICE = "hash_slice"
    
    # File operations
    FILEHANDLE = "filehandle"
    OPEN_STATEMENT = "open_statement"
    PRINT_STATEMENT = "print_statement"
    READLINE = "readline"
    
    # Object-oriented
    BLESS_EXPRESSION = "bless_expression"
    METHOD_CALL = "method_call"
    
    # Special constructs
    EVAL_EXPRESSION = "eval_expression"
    SPECIAL_VARIABLE = "special_variable"
    MAGIC_VARIABLE = "magic_variable"
    FORMAT_STATEMENT = "format_statement"
    
    # Literals and identifiers
    NUMERIC_LITERAL = "numeric_literal"
    IDENTIFIER = "identifier"
    BAREWORD = "bareword"

@dataclass
class PerlNode(ASTNode):
    """Base class for all Perl AST nodes"""
    node_type: PerlNodeType
    source_location: Optional[Dict[str, int]] = None
    context: str = "void"  # void, scalar, list
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        super().__post_init__()
        if self.node_id is None:
            self.node_id = str(uuid.uuid4())

@dataclass
class PerlProgram(PerlNode):
    """Perl program (script or module)"""
    statements: List['PerlStatement'] = field(default_factory=list)
    packages: List['PerlPackage'] = field(default_factory=list)
    use_statements: List['PerlUseStatement'] = field(default_factory=list)
    shebang: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.PROGRAM

@dataclass
class PerlPackage(PerlNode):
    """Perl package/namespace declaration"""
    name: str
    version: Optional[str] = None
    statements: List['PerlStatement'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.PACKAGE

@dataclass
class PerlUseStatement(PerlNode):
    """Use statement for importing modules"""
    module_name: str
    version: Optional[str] = None
    import_list: List[str] = field(default_factory=list)
    arguments: List['PerlExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.USE_STATEMENT

@dataclass
class PerlRequireStatement(PerlNode):
    """Require statement for runtime module loading"""
    module_name: Union[str, 'PerlExpression']
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.REQUIRE_STATEMENT

@dataclass
class PerlStatement(PerlNode):
    """Base class for Perl statements"""
    pass

@dataclass
class PerlVariable(PerlNode):
    """Base class for Perl variables"""
    name: str
    sigil: str  # $, @, %, &, *
    package: Optional[str] = None

@dataclass
class PerlScalarVariable(PerlVariable):
    """Perl scalar variable ($var)"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.SCALAR_VARIABLE
        self.sigil = "$"

@dataclass
class PerlArrayVariable(PerlVariable):
    """Perl array variable (@array)"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.ARRAY_VARIABLE
        self.sigil = "@"

@dataclass
class PerlHashVariable(PerlVariable):
    """Perl hash variable (%hash)"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.HASH_VARIABLE
        self.sigil = "%"

@dataclass
class PerlTypeglob(PerlVariable):
    """Perl typeglob (*glob)"""
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.TYPEGLOB
        self.sigil = "*"

@dataclass
class PerlReference(PerlNode):
    """Perl reference (\expression)"""
    expression: 'PerlExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.REFERENCE

@dataclass
class PerlDereference(PerlNode):
    """Perl dereference ($$ref, @$ref, %$ref)"""
    reference: 'PerlExpression'
    dereference_type: str  # scalar, array, hash, code, glob
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.DEREFERENCE

@dataclass
class PerlSubroutineDeclaration(PerlStatement):
    """Perl subroutine declaration"""
    name: str
    parameters: List[str] = field(default_factory=list)
    body: List[PerlStatement] = field(default_factory=list)
    attributes: List[str] = field(default_factory=list)
    prototype: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.SUBROUTINE_DECLARATION

@dataclass
class PerlSubroutineCall(PerlNode):
    """Perl subroutine call"""
    name: str
    arguments: List['PerlExpression'] = field(default_factory=list)
    ampersand_prefix: bool = False  # &subroutine_call
    package: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.SUBROUTINE_CALL

@dataclass
class PerlAnonymousSubroutine(PerlNode):
    """Perl anonymous subroutine (code reference)"""
    parameters: List[str] = field(default_factory=list)
    body: List[PerlStatement] = field(default_factory=list)
    prototype: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.ANONYMOUS_SUBROUTINE

@dataclass
class PerlIfStatement(PerlStatement):
    """Perl if/elsif/else statement"""
    condition: 'PerlExpression'
    then_block: List[PerlStatement] = field(default_factory=list)
    elsif_blocks: List['PerlElsifBlock'] = field(default_factory=list)
    else_block: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.IF_STATEMENT

@dataclass
class PerlElsifBlock(PerlNode):
    """Elsif block for if statements"""
    condition: 'PerlExpression'
    statements: List[PerlStatement] = field(default_factory=list)

@dataclass
class PerlUnlessStatement(PerlStatement):
    """Perl unless statement (negative if)"""
    condition: 'PerlExpression'
    then_block: List[PerlStatement] = field(default_factory=list)
    else_block: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.UNLESS_STATEMENT

@dataclass
class PerlWhileLoop(PerlStatement):
    """Perl while loop"""
    condition: 'PerlExpression'
    body: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.WHILE_LOOP

@dataclass
class PerlUntilLoop(PerlStatement):
    """Perl until loop (negative while)"""
    condition: 'PerlExpression'
    body: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.UNTIL_LOOP

@dataclass
class PerlForLoop(PerlStatement):
    """Perl C-style for loop"""
    initialization: Optional['PerlExpression']
    condition: Optional['PerlExpression']
    increment: Optional['PerlExpression']
    body: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.FOR_LOOP

@dataclass
class PerlForeachLoop(PerlStatement):
    """Perl foreach loop"""
    variable: Optional['PerlVariable']  # None uses $_
    iterable: 'PerlExpression'
    body: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.FOREACH_LOOP

@dataclass
class PerlGivenWhen(PerlStatement):
    """Perl given/when switch statement (Perl 5.10+)"""
    expression: 'PerlExpression'
    when_blocks: List['PerlWhenBlock'] = field(default_factory=list)
    default_block: List[PerlStatement] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.GIVEN_WHEN

@dataclass
class PerlWhenBlock(PerlNode):
    """When block for given/when statements"""
    condition: 'PerlExpression'
    statements: List[PerlStatement] = field(default_factory=list)

@dataclass
class PerlExpression(PerlNode):
    """Base class for Perl expressions"""
    pass

@dataclass
class PerlAssignment(PerlExpression):
    """Perl assignment operation"""
    left: 'PerlExpression'
    right: 'PerlExpression'
    operator: str = "="  # =, +=, -=, .=, etc.
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.ASSIGNMENT

@dataclass
class PerlBinaryOperation(PerlExpression):
    """Perl binary operation"""
    left: 'PerlExpression'
    right: 'PerlExpression'
    operator: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.BINARY_OPERATION

@dataclass
class PerlUnaryOperation(PerlExpression):
    """Perl unary operation"""
    operand: 'PerlExpression'
    operator: str
    prefix: bool = True  # True for prefix, False for postfix
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.UNARY_OPERATION

@dataclass
class PerlTernaryOperation(PerlExpression):
    """Perl ternary conditional operation (? :)"""
    condition: 'PerlExpression'
    true_expression: 'PerlExpression'
    false_expression: 'PerlExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.TERNARY_OPERATION

@dataclass
class PerlRegexMatch(PerlExpression):
    """Perl regex match operation (=~ or !~)"""
    string: 'PerlExpression'
    pattern: 'PerlRegexLiteral'
    operator: str = "=~"  # =~ or !~
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.REGEX_MATCH

@dataclass
class PerlRegexSubstitution(PerlExpression):
    """Perl regex substitution (s///)"""
    string: 'PerlExpression'
    pattern: str
    replacement: str
    flags: str = ""  # g, i, m, s, x, etc.
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.REGEX_SUBSTITUTION

@dataclass
class PerlRegexTransliteration(PerlExpression):
    """Perl transliteration operation (tr/// or y///)"""
    string: 'PerlExpression'
    search_list: str
    replacement_list: str
    flags: str = ""  # c, d, s
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.REGEX_TRANSLITERATION

@dataclass
class PerlStringLiteral(PerlExpression):
    """Perl string literal"""
    value: str
    quote_type: str = "double"  # single, double, qq, q
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.STRING_LITERAL

@dataclass
class PerlRegexLiteral(PerlExpression):
    """Perl regex literal"""
    pattern: str
    flags: str = ""  # i, m, s, x, g, etc.
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.REGEX_LITERAL

@dataclass
class PerlHereDocument(PerlExpression):
    """Perl here document"""
    delimiter: str
    content: str
    interpolate: bool = True
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.HERE_DOCUMENT

@dataclass
class PerlInterpolatedString(PerlExpression):
    """Perl string with variable interpolation"""
    parts: List[Union[str, 'PerlExpression']] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.INTERPOLATED_STRING

@dataclass
class PerlQuotedWordList(PerlExpression):
    """Perl quoted word list (qw//)"""
    words: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.QUOTED_WORD_LIST

@dataclass
class PerlArrayLiteral(PerlExpression):
    """Perl anonymous array literal"""
    elements: List['PerlExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.ARRAY_LITERAL

@dataclass
class PerlHashLiteral(PerlExpression):
    """Perl anonymous hash literal"""
    pairs: List['PerlHashPair'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.HASH_LITERAL

@dataclass
class PerlHashPair(PerlNode):
    """Key-value pair in hash literal"""
    key: 'PerlExpression'
    value: 'PerlExpression'

@dataclass
class PerlArraySlice(PerlExpression):
    """Perl array slice (@array[indices])"""
    array: 'PerlExpression'
    indices: List['PerlExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.ARRAY_SLICE

@dataclass
class PerlHashSlice(PerlExpression):
    """Perl hash slice (@hash{keys})"""
    hash: 'PerlExpression'
    keys: List['PerlExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.HASH_SLICE

@dataclass
class PerlFilehandle(PerlExpression):
    """Perl filehandle"""
    name: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.FILEHANDLE

@dataclass
class PerlOpenStatement(PerlStatement):
    """Perl open statement"""
    filehandle: 'PerlFilehandle'
    mode: str
    filename: 'PerlExpression'
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.OPEN_STATEMENT

@dataclass
class PerlPrintStatement(PerlStatement):
    """Perl print statement"""
    filehandle: Optional['PerlFilehandle'] = None
    arguments: List['PerlExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.PRINT_STATEMENT

@dataclass
class PerlReadline(PerlExpression):
    """Perl readline operation (<>)"""
    filehandle: Optional['PerlFilehandle'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.READLINE

@dataclass
class PerlBlessExpression(PerlExpression):
    """Perl bless expression for OOP"""
    reference: 'PerlExpression'
    class_name: Optional['PerlExpression'] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.BLESS_EXPRESSION

@dataclass
class PerlMethodCall(PerlExpression):
    """Perl method call (object->method())"""
    object: 'PerlExpression'
    method: str
    arguments: List['PerlExpression'] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.METHOD_CALL

@dataclass
class PerlEvalExpression(PerlExpression):
    """Perl eval expression"""
    expression: Union[str, 'PerlExpression']
    is_string_eval: bool = True  # True for eval "string", False for eval { block }
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.EVAL_EXPRESSION

@dataclass
class PerlSpecialVariable(PerlExpression):
    """Perl special variable ($_, @_, $&, etc.)"""
    name: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.SPECIAL_VARIABLE

@dataclass
class PerlMagicVariable(PerlExpression):
    """Perl magic variable (tied variable)"""
    name: str
    tie_class: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.MAGIC_VARIABLE

@dataclass
class PerlFormatStatement(PerlStatement):
    """Perl format statement for reports"""
    name: str
    format_lines: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.FORMAT_STATEMENT

@dataclass
class PerlNumericLiteral(PerlExpression):
    """Perl numeric literal"""
    value: Union[int, float]
    base: int = 10  # 2, 8, 10, 16
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.NUMERIC_LITERAL

@dataclass
class PerlIdentifier(PerlExpression):
    """Perl identifier"""
    name: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.IDENTIFIER

@dataclass
class PerlBareword(PerlExpression):
    """Perl bareword (unquoted string)"""
    name: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = PerlNodeType.BAREWORD

# Factory functions for common Perl constructs

def create_perl_scalar(name: str, package: Optional[str] = None) -> PerlScalarVariable:
    """Create Perl scalar variable"""
    return PerlScalarVariable(name=name, package=package)

def create_perl_array(name: str, package: Optional[str] = None) -> PerlArrayVariable:
    """Create Perl array variable"""
    return PerlArrayVariable(name=name, package=package)

def create_perl_hash(name: str, package: Optional[str] = None) -> PerlHashVariable:
    """Create Perl hash variable"""
    return PerlHashVariable(name=name, package=package)

def create_perl_subroutine(name: str, body: List[PerlStatement] = None) -> PerlSubroutineDeclaration:
    """Create Perl subroutine"""
    return PerlSubroutineDeclaration(name=name, body=body or [])

def create_perl_regex(pattern: str, flags: str = "") -> PerlRegexLiteral:
    """Create Perl regex literal"""
    return PerlRegexLiteral(pattern=pattern, flags=flags)

def create_perl_string(value: str, interpolate: bool = True) -> PerlStringLiteral:
    """Create Perl string literal"""
    quote_type = "double" if interpolate else "single"
    return PerlStringLiteral(value=value, quote_type=quote_type)

def create_perl_package(name: str) -> PerlPackage:
    """Create Perl package"""
    return PerlPackage(name=name)

# Export all public classes and functions
__all__ = [
    # Enums
    'PerlNodeType',
    
    # Base classes
    'PerlNode', 'PerlStatement', 'PerlExpression', 'PerlVariable',
    
    # Program structure
    'PerlProgram', 'PerlPackage', 'PerlUseStatement', 'PerlRequireStatement',
    
    # Variables and data types
    'PerlScalarVariable', 'PerlArrayVariable', 'PerlHashVariable', 'PerlTypeglob',
    'PerlReference', 'PerlDereference',
    
    # Subroutines
    'PerlSubroutineDeclaration', 'PerlSubroutineCall', 'PerlAnonymousSubroutine',
    
    # Control structures
    'PerlIfStatement', 'PerlElsifBlock', 'PerlUnlessStatement',
    'PerlWhileLoop', 'PerlUntilLoop', 'PerlForLoop', 'PerlForeachLoop',
    'PerlGivenWhen', 'PerlWhenBlock',
    
    # Operators and expressions
    'PerlAssignment', 'PerlBinaryOperation', 'PerlUnaryOperation', 'PerlTernaryOperation',
    'PerlRegexMatch', 'PerlRegexSubstitution', 'PerlRegexTransliteration',
    
    # String and regex
    'PerlStringLiteral', 'PerlRegexLiteral', 'PerlHereDocument',
    'PerlInterpolatedString', 'PerlQuotedWordList',
    
    # Data structures
    'PerlArrayLiteral', 'PerlHashLiteral', 'PerlHashPair',
    'PerlArraySlice', 'PerlHashSlice',
    
    # File operations
    'PerlFilehandle', 'PerlOpenStatement', 'PerlPrintStatement', 'PerlReadline',
    
    # Object-oriented
    'PerlBlessExpression', 'PerlMethodCall',
    
    # Special constructs
    'PerlEvalExpression', 'PerlSpecialVariable', 'PerlMagicVariable',
    'PerlFormatStatement',
    
    # Literals and identifiers
    'PerlNumericLiteral', 'PerlIdentifier', 'PerlBareword',
    
    # Factory functions
    'create_perl_scalar', 'create_perl_array', 'create_perl_hash',
    'create_perl_subroutine', 'create_perl_regex', 'create_perl_string',
    'create_perl_package'
] 