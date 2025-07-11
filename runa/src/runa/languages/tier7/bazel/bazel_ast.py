#!/usr/bin/env python3
"""
Bazel AST (Abstract Syntax Tree) Implementation

Complete AST structure for Bazel build files including:
- BUILD files with rules and targets
- WORKSPACE files with external dependencies
- .bzl files with custom rules and macros
- Label syntax and target addressing
- Starlark language constructs
- Aspects and build event streaming
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class BazelNodeType(Enum):
    """Enumeration of all Bazel AST node types."""
    # File level
    BUILD_FILE = "build_file"
    WORKSPACE_FILE = "workspace_file"
    BZL_FILE = "bzl_file"
    
    # Rule and target definitions
    RULE_DEFINITION = "rule_definition"
    TARGET_DEFINITION = "target_definition"
    PACKAGE_GROUP = "package_group"
    
    # Workspace constructs
    WORKSPACE_RULE = "workspace_rule"
    BIND_RULE = "bind_rule"
    LOCAL_REPOSITORY = "local_repository"
    GIT_REPOSITORY = "git_repository"
    HTTP_ARCHIVE = "http_archive"
    
    # Starlark language constructs
    FUNCTION_DEF = "function_def"
    LOAD_STATEMENT = "load_statement"
    ASSIGNMENT = "assignment"
    IF_STATEMENT = "if_statement"
    FOR_LOOP = "for_loop"
    
    # Expressions
    LABEL = "label"
    ATTRIBUTE = "attribute"
    LIST_EXPR = "list_expr"
    DICT_EXPR = "dict_expr"
    CALL_EXPR = "call_expr"
    IDENTIFIER = "identifier"
    LITERAL = "literal"
    
    # Advanced features
    ASPECT = "aspect"
    PROVIDER = "provider"
    CONFIGURATION = "configuration"
    TRANSITION = "transition"


@dataclass
class BazelNode(ABC):
    """Base class for all Bazel AST nodes."""
    node_type: BazelNodeType
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    source_file: Optional[str] = None
    
    @abstractmethod
    def accept(self, visitor: 'BazelVisitor') -> Any:
        """Accept a visitor for traversal."""
        pass


@dataclass
class BazelExpression(BazelNode):
    """Base class for Bazel expressions."""
    pass


@dataclass
class BazelStatement(BazelNode):
    """Base class for Bazel statements."""
    pass


@dataclass
class BazelDeclaration(BazelNode):
    """Base class for Bazel declarations."""
    pass


# === File Level Nodes ===

@dataclass
class BuildFile(BazelNode):
    """Represents a BUILD file."""
    package_name: str
    statements: List[BazelStatement] = field(default_factory=list)
    visibility: Optional[List[str]] = None
    licenses: Optional[List[str]] = None
    
    def __post_init__(self):
        self.node_type = BazelNodeType.BUILD_FILE
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_build_file(self)


@dataclass
class WorkspaceFile(BazelNode):
    """Represents a WORKSPACE file."""
    workspace_name: str
    statements: List[BazelStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.WORKSPACE_FILE
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_workspace_file(self)


@dataclass
class BzlFile(BazelNode):
    """Represents a .bzl file with custom rules and macros."""
    file_name: str
    statements: List[BazelStatement] = field(default_factory=list)
    load_statements: List['LoadStatement'] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.BZL_FILE
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_bzl_file(self)


# === Rule and Target Definitions ===

@dataclass
class RuleDefinition(BazelDeclaration):
    """Represents a rule definition (custom build rule)."""
    name: str
    implementation: str
    attributes: Dict[str, 'AttributeDefinition'] = field(default_factory=dict)
    outputs: Optional[List[str]] = None
    executable: bool = False
    test: bool = False
    
    def __post_init__(self):
        self.node_type = BazelNodeType.RULE_DEFINITION
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_rule_definition(self)


@dataclass
class TargetDefinition(BazelDeclaration):
    """Represents a target definition in a BUILD file."""
    rule_name: str
    target_name: str
    attributes: Dict[str, BazelExpression] = field(default_factory=dict)
    visibility: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    
    def __post_init__(self):
        self.node_type = BazelNodeType.TARGET_DEFINITION
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_target_definition(self)


@dataclass
class PackageGroup(BazelDeclaration):
    """Represents a package_group definition."""
    name: str
    packages: List[str] = field(default_factory=list)
    includes: Optional[List[str]] = None
    
    def __post_init__(self):
        self.node_type = BazelNodeType.PACKAGE_GROUP
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_package_group(self)


# === Workspace Constructs ===

@dataclass
class WorkspaceRule(BazelStatement):
    """Represents a workspace rule (external dependency)."""
    rule_name: str
    attributes: Dict[str, BazelExpression] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.WORKSPACE_RULE
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_workspace_rule(self)


@dataclass
class LocalRepository(WorkspaceRule):
    """Represents a local_repository rule."""
    path: str
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = BazelNodeType.LOCAL_REPOSITORY
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_local_repository(self)


@dataclass
class GitRepository(WorkspaceRule):
    """Represents a git_repository rule."""
    remote: str
    commit: Optional[str] = None
    tag: Optional[str] = None
    branch: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = BazelNodeType.GIT_REPOSITORY
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_git_repository(self)


@dataclass
class HttpArchive(WorkspaceRule):
    """Represents an http_archive rule."""
    url: str
    sha256: Optional[str] = None
    strip_prefix: Optional[str] = None
    build_file: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        self.node_type = BazelNodeType.HTTP_ARCHIVE
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_http_archive(self)


# === Starlark Language Constructs ===

@dataclass
class LoadStatement(BazelStatement):
    """Represents a load statement."""
    file_path: str
    symbols: List[str] = field(default_factory=list)
    symbol_aliases: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.LOAD_STATEMENT
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_load_statement(self)


@dataclass
class FunctionDef(BazelDeclaration):
    """Represents a function definition."""
    name: str
    parameters: List[str] = field(default_factory=list)
    defaults: Dict[str, BazelExpression] = field(default_factory=dict)
    body: List[BazelStatement] = field(default_factory=list)
    return_type: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = BazelNodeType.FUNCTION_DEF
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_function_def(self)


@dataclass
class Assignment(BazelStatement):
    """Represents variable assignment."""
    target: str
    value: BazelExpression
    operator: str = "="
    
    def __post_init__(self):
        self.node_type = BazelNodeType.ASSIGNMENT
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_assignment(self)


@dataclass
class IfStatement(BazelStatement):
    """Represents an if statement."""
    condition: BazelExpression
    then_body: List[BazelStatement] = field(default_factory=list)
    else_body: Optional[List[BazelStatement]] = None
    elif_clauses: List[tuple] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.IF_STATEMENT
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_if_statement(self)


@dataclass
class ForLoop(BazelStatement):
    """Represents a for loop."""
    variable: str
    iterable: BazelExpression
    body: List[BazelStatement] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.FOR_LOOP
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_for_loop(self)


# === Expressions ===

@dataclass
class Label(BazelExpression):
    """Represents a Bazel label (target reference)."""
    package: Optional[str]
    target: str
    repository: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = BazelNodeType.LABEL
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_label(self)
    
    def __str__(self) -> str:
        """Return the string representation of the label."""
        parts = []
        if self.repository:
            parts.append(f"@{self.repository}")
        if self.package:
            parts.append(f"//{self.package}")
        parts.append(f":{self.target}")
        return "".join(parts)


@dataclass
class Attribute(BazelExpression):
    """Represents an attribute access."""
    object: BazelExpression
    attribute: str
    
    def __post_init__(self):
        self.node_type = BazelNodeType.ATTRIBUTE
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_attribute(self)


@dataclass
class ListExpr(BazelExpression):
    """Represents a list expression."""
    elements: List[BazelExpression] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.LIST_EXPR
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_list_expr(self)


@dataclass
class DictExpr(BazelExpression):
    """Represents a dictionary expression."""
    pairs: List[tuple] = field(default_factory=list)  # List of (key, value) tuples
    
    def __post_init__(self):
        self.node_type = BazelNodeType.DICT_EXPR
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_dict_expr(self)


@dataclass
class CallExpr(BazelExpression):
    """Represents a function call."""
    function: BazelExpression
    args: List[BazelExpression] = field(default_factory=list)
    kwargs: Dict[str, BazelExpression] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.CALL_EXPR
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_call_expr(self)


@dataclass
class Identifier(BazelExpression):
    """Represents an identifier."""
    name: str
    
    def __post_init__(self):
        self.node_type = BazelNodeType.IDENTIFIER
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_identifier(self)


@dataclass
class Literal(BazelExpression):
    """Represents a literal value (string, number, boolean)."""
    value: Union[str, int, float, bool]
    literal_type: str  # 'string', 'integer', 'float', 'boolean'
    
    def __post_init__(self):
        self.node_type = BazelNodeType.LITERAL
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_literal(self)


# === Advanced Features ===

@dataclass
class AttributeDefinition:
    """Represents an attribute definition in a rule."""
    name: str
    attr_type: str  # 'string', 'label', 'string_list', etc.
    mandatory: bool = False
    default: Optional[Any] = None
    doc: Optional[str] = None
    cfg: Optional[str] = None


@dataclass
class Aspect(BazelDeclaration):
    """Represents an aspect definition."""
    name: str
    implementation: str
    attr_aspects: List[str] = field(default_factory=list)
    attrs: Dict[str, AttributeDefinition] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = BazelNodeType.ASPECT
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_aspect(self)


@dataclass
class Provider(BazelDeclaration):
    """Represents a provider definition."""
    name: str
    fields: List[str] = field(default_factory=list)
    doc: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = BazelNodeType.PROVIDER
    
    def accept(self, visitor: 'BazelVisitor') -> Any:
        return visitor.visit_provider(self)


# === Visitor Pattern ===

class BazelVisitor(ABC):
    """Abstract visitor for traversing Bazel AST."""
    
    @abstractmethod
    def visit_build_file(self, node: BuildFile) -> Any:
        pass
    
    @abstractmethod
    def visit_workspace_file(self, node: WorkspaceFile) -> Any:
        pass
    
    @abstractmethod
    def visit_bzl_file(self, node: BzlFile) -> Any:
        pass
    
    @abstractmethod
    def visit_rule_definition(self, node: RuleDefinition) -> Any:
        pass
    
    @abstractmethod
    def visit_target_definition(self, node: TargetDefinition) -> Any:
        pass
    
    @abstractmethod
    def visit_package_group(self, node: PackageGroup) -> Any:
        pass
    
    @abstractmethod
    def visit_workspace_rule(self, node: WorkspaceRule) -> Any:
        pass
    
    @abstractmethod
    def visit_local_repository(self, node: LocalRepository) -> Any:
        pass
    
    @abstractmethod
    def visit_git_repository(self, node: GitRepository) -> Any:
        pass
    
    @abstractmethod
    def visit_http_archive(self, node: HttpArchive) -> Any:
        pass
    
    @abstractmethod
    def visit_load_statement(self, node: LoadStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_function_def(self, node: FunctionDef) -> Any:
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment) -> Any:
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> Any:
        pass
    
    @abstractmethod
    def visit_for_loop(self, node: ForLoop) -> Any:
        pass
    
    @abstractmethod
    def visit_label(self, node: Label) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute(self, node: Attribute) -> Any:
        pass
    
    @abstractmethod
    def visit_list_expr(self, node: ListExpr) -> Any:
        pass
    
    @abstractmethod
    def visit_dict_expr(self, node: DictExpr) -> Any:
        pass
    
    @abstractmethod
    def visit_call_expr(self, node: CallExpr) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        pass
    
    @abstractmethod
    def visit_literal(self, node: Literal) -> Any:
        pass
    
    @abstractmethod
    def visit_aspect(self, node: Aspect) -> Any:
        pass
    
    @abstractmethod
    def visit_provider(self, node: Provider) -> Any:
        pass


# === Utility Functions ===

def create_label(label_str: str) -> Label:
    """Parse a label string into a Label object."""
    if label_str.startswith('@'):
        # External repository
        parts = label_str[1:].split('//', 1)
        repository = parts[0]
        if len(parts) > 1:
            pkg_target = parts[1].split(':', 1)
            package = pkg_target[0] if pkg_target[0] else None
            target = pkg_target[1] if len(pkg_target) > 1 else pkg_target[0]
        else:
            package = None
            target = repository
    elif label_str.startswith('//'):
        # Absolute label
        repository = None
        pkg_target = label_str[2:].split(':', 1)
        package = pkg_target[0] if pkg_target[0] else None
        target = pkg_target[1] if len(pkg_target) > 1 else pkg_target[0]
    elif ':' in label_str:
        # Relative label with explicit target
        repository = None
        package = None
        target = label_str.split(':', 1)[1]
    else:
        # Simple target name
        repository = None
        package = None
        target = label_str
    
    return Label(package=package, target=target, repository=repository)


def is_valid_target_name(name: str) -> bool:
    """Check if a target name is valid according to Bazel rules."""
    if not name or name.startswith('_'):
        return False
    # Simplified validation - in practice, Bazel has more complex rules
    invalid_chars = [' ', '\t', '\n', '/', '\\', ':']
    return not any(char in name for char in invalid_chars) 