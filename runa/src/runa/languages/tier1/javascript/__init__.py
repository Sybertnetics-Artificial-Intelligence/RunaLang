#!/usr/bin/env python3
"""
JavaScript Language Support for Runa

Complete JavaScript toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .js_ast import *

# Package metadata
__version__ = "1.0.0"
__author__ = "Sybertnetics AI Solutions"
__description__ = "JavaScript AST node definitions with dataclass field fixes"

# Available AST classes (exported from js_ast)
__all__ = [
    # Base classes
    "JSNode", "JSExpression", "JSStatement",
    
    # Expression classes
    "JSLiteral", "JSIdentifier", "JSBinaryExpression", "JSUnaryExpression",
    "JSCallExpression", "JSMemberExpression", "JSArrayExpression", "JSObjectExpression",
    "JSFunctionExpression", "JSArrowFunctionExpression", "JSConditionalExpression",
    "JSAssignmentExpression", "JSUpdateExpression", "JSLogicalExpression",
    "JSNewExpression", "JSThisExpression", "JSSuper", "JSSequenceExpression",
    "JSAwaitExpression", "JSYieldExpression", "JSTemplateLiteral",
    
    # Statement classes  
    "JSExpressionStatement", "JSBlockStatement", "JSVariableDeclaration",
    "JSFunctionDeclaration", "JSIfStatement", "JSWhileStatement", "JSForStatement",
    "JSReturnStatement", "JSBreakStatement", "JSContinueStatement", "JSThrowStatement",
    "JSTryStatement", "JSEmptyStatement", "JSDebuggerStatement",
    
    # Supporting classes
    "JSProperty", "JSVariableDeclarator", "JSCatchClause", "JSProgram",
    
    # Enums
    "JSNodeType", "JSLiteralType", "JSOperator", "JSVariableKind", 
    "JSFunctionKind", "JSPropertyKind", "JSModuleKind",
    
    # Visitor
    "JSNodeVisitor",
]

# Module metadata
__language__ = "javascript"
__tier__ = 1
__file_extensions__ = [".js", ".mjs", ".cjs"]
__mime_types__ = ["application/javascript", "text/javascript"]