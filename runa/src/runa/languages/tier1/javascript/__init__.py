#!/usr/bin/env python3
"""
JavaScript Language Support for Runa

Complete JavaScript toolchain providing parsing, AST conversion, code generation,
and round-trip verification for the Runa universal translation system.
"""

from .js_ast import *
from .js_parser import parse_javascript
from .js_converter import js_to_runa, runa_to_js
from .js_generator import JSCodeGenerator
from .js_toolchain import (
    JavaScriptToolchain,
    parse_js,
    generate_js,
    js_round_trip_verify,
    js_to_runa_translate,
    runa_to_js_translate
)

__all__ = [
    # AST classes
    "JSNode",
    "JSProgram", 
    "JSLiteral",
    "JSIdentifier",
    "JSBinaryExpression",
    "JSUnaryExpression",
    "JSFunctionDeclaration",
    "JSVariableDeclaration",
    "JSIfStatement",
    "JSWhileStatement",
    "JSForStatement",
    "JSReturnStatement",
    "JSBreakStatement",
    "JSContinueStatement",
    "JSBlockStatement",
    "JSExpressionStatement",
    "JSCallExpression",
    "JSMemberExpression",
    "JSArrayExpression",
    "JSObjectExpression",
    "JSProperty",
    "JSThisExpression",
    "JSArrowFunctionExpression",
    "JSFunctionExpression",
    "JSTemplateLiteral",
    "JSAwaitExpression",
    "JSYieldExpression",
    "JSAssignmentExpression",
    "JSUpdateExpression",
    "JSLogicalExpression",
    "JSConditionalExpression",
    "JSNewExpression",
    "JSSequenceExpression",
    "JSThrowStatement",
    "JSTryStatement",
    "JSCatchClause",
    "JSEmptyStatement",
    "JSDebuggerStatement",
    
    # Enums
    "JSNodeType",
    "JSLiteralType", 
    "JSOperator",
    "JSVariableKind",
    "JSFunctionKind",
    "JSPropertyKind",
    "JSModuleKind",
    
    # Parser
    "parse_javascript",
    
    # Converter
    "js_to_runa",
    "runa_to_js",
    
    # Generator
    "JSCodeGenerator",
    
    # Toolchain
    "JavaScriptToolchain",
    "parse_js",
    "generate_js", 
    "js_round_trip_verify",
    "js_to_runa_translate",
    "runa_to_js_translate",
]

# Module metadata
__version__ = "1.0.0"
__author__ = "Runa Development Team"
__description__ = "JavaScript language support for Runa universal translation system"
__language__ = "javascript"
__tier__ = 1
__file_extensions__ = [".js", ".mjs", ".cjs"]
__mime_types__ = ["application/javascript", "text/javascript"]