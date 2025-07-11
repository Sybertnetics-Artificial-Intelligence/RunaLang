"""
LIGO AST ↔ Runa AST Converter

Handles bidirectional conversion between LIGO AST nodes and Runa AST nodes,
supporting both JsLIGO and CameLIGO syntax variants.
"""

from typing import Any, Dict, List, Optional, Union
from runa.ast.base import RunaNode
from runa.ast.expressions import (
    StringLiteral, Identifier, FunctionCall, RunaBinaryOp,
    RunaUnaryOp, IfStatement, ProcessDefinition, ListLiteral,
    RunaDictLiteral, RunaAttributeAccess, IndexAccess
)
from runa.ast.statements import (
    SetStatement, RunaFunctionDef, ReturnStatement, RunaIf,
    RunaWhile, RunaFor, Block, RunaTryCatch, RunaImport
)
from runa.ast.declarations import (
    RunaClassDef, RunaModuleDef, RunaVariableDecl, RunaInterfaceDef
)
from runa.ast.types import (
    BasicType, RunaPrimitiveType, FunctionType, GenericType,
    UnionType, RunaRecordType, ListLiteralType
)

from .ligo_ast import *


class LIGOToRunaConverter:
    """Converts LIGO AST nodes to Runa AST nodes."""
    
    def __init__(self, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO):
        self.syntax_style = syntax_style
        self.current_module = None
        
    def convert(self, node: LIGONode) -> RunaNode:
        """Convert any LIGO AST node to corresponding Runa AST node."""
        method_name = f"convert_{type(node).__name__}"
        converter = getattr(self, method_name, self.convert_generic)
        return converter(node)
    
    def convert_generic(self, node: LIGONode) -> RunaNode:
        """Generic converter for unknown node types."""
        # Create a generic expression with the node's text representation
        return Identifier(name=str(node), source_info=node.source_info)
    
    # Program and Module conversion
    def convert_LIGOProgram(self, node: LIGOProgram) -> RunaModuleDef:
        """Convert LIGO program to Runa module."""
        statements = [self.convert(stmt) for stmt in node.declarations]
        
        return RunaModuleDef(
            name=node.name or "main",
            body=statements,
            imports=[],
            exports=[],
            source_info=node.source_info
        )
    
    # Type conversions
    def convert_LIGOType(self, node: LIGOType) -> BasicType:
        """Convert LIGO type to Runa type."""
        if isinstance(node, LIGOPrimitiveType):
            return self.convert_LIGOPrimitiveType(node)
        elif isinstance(node, LIGORecordType):
            return self.convert_LIGORecordType(node) 
        elif isinstance(node, LIGOVariantType):
            return self.convert_LIGOVariantType(node)
        elif isinstance(node, LIGOListType):
            return self.convert_LIGOListType(node)
        elif isinstance(node, LIGOMapType):
            return self.convert_LIGOMapType(node)
        elif isinstance(node, LIGOOptionType):
            return self.convert_LIGOOptionType(node)
        elif isinstance(node, LIGOTupleType):
            return self.convert_LIGOTupleType(node)
        elif isinstance(node, LIGOFunctionType):
            return self.convert_LIGOFunctionType(node)
        else:
            return RunaPrimitiveType(name="unknown", source_info=node.source_info)
    
    def convert_LIGOPrimitiveType(self, node: LIGOPrimitiveType) -> RunaPrimitiveType:
        """Convert LIGO primitive type to Runa primitive type."""
        type_map = {
            "int": "int",
            "nat": "int", 
            "string": "str",
            "bytes": "bytes",
            "bool": "bool",
            "unit": "None",
            "address": "str",
            "tez": "decimal",
            "timestamp": "datetime",
            "mutez": "int"
        }
        
        runa_type = type_map.get(node.name, node.name)
        return RunaPrimitiveType(name=runa_type, source_info=node.source_info)
    
    def convert_LIGORecordType(self, node: LIGORecordType) -> RunaRecordType:
        """Convert LIGO record type to Runa record type."""
        fields = {}
        for field in node.fields:
            fields[field.name] = self.convert(field.type_annotation)
            
        return RunaRecordType(
            fields=fields,
            source_info=node.source_info
        )
    
    def convert_LIGOVariantType(self, node: LIGOVariantType) -> UnionType:
        """Convert LIGO variant type to Runa union type."""
        types = []
        for variant in node.variants:
            if variant.type_annotation:
                types.append(self.convert(variant.type_annotation))
            else:
                types.append(RunaPrimitiveType(name=variant.name))
                
        return UnionType(types=types, source_info=node.source_info)
    
    def convert_LIGOListType(self, node: LIGOListType) -> ListLiteralType:
        """Convert LIGO list type to Runa array type."""
        element_type = self.convert(node.element_type)
        return ListLiteralType(element_type=element_type, source_info=node.source_info)
    
    def convert_LIGOMapType(self, node: LIGOMapType) -> GenericType:
        """Convert LIGO map type to Runa generic type."""
        key_type = self.convert(node.key_type)
        value_type = self.convert(node.value_type)
        
        return GenericType(
            base_type=RunaPrimitiveType(name="dict"),
            type_args=[key_type, value_type],
            source_info=node.source_info
        )
    
    def convert_LIGOOptionType(self, node: LIGOOptionType) -> UnionType:
        """Convert LIGO option type to Runa union type."""
        inner_type = self.convert(node.inner_type)
        none_type = RunaPrimitiveType(name="None")
        
        return UnionType(
            types=[inner_type, none_type],
            source_info=node.source_info
        )
    
    def convert_LIGOTupleType(self, node: LIGOTupleType) -> GenericType:
        """Convert LIGO tuple type to Runa generic type."""
        element_types = [self.convert(t) for t in node.element_types]
        
        return GenericType(
            base_type=RunaPrimitiveType(name="tuple"),
            type_args=element_types,
            source_info=node.source_info
        )
    
    def convert_LIGOFunctionType(self, node: LIGOFunctionType) -> FunctionType:
        """Convert LIGO function type to Runa function type."""
        param_types = [self.convert(p) for p in node.param_types]
        return_type = self.convert(node.return_type)
        
        return FunctionType(
            param_types=param_types,
            return_type=return_type,
            source_info=node.source_info
        )
    
    # Expression conversions
    def convert_LIGOLiteral(self, node: LIGOLiteral) -> StringLiteral:
        """Convert LIGO literal to Runa literal."""
        return StringLiteral(
            value=node.value,
            type_hint=node.literal_type,
            source_info=node.source_info
        )
    
    def convert_LIGOIdentifier(self, node: LIGOIdentifier) -> Identifier:
        """Convert LIGO identifier to Runa identifier."""
        return Identifier(
            name=node.name,
            source_info=node.source_info
        )
    
    def convert_LIGOBinaryOp(self, node: LIGOBinaryOp) -> RunaBinaryOp:
        """Convert LIGO binary operation to Runa binary operation."""
        left = self.convert(node.left)
        right = self.convert(node.right)
        
        # Map LIGO operators to Runa operators
        op_map = {
            "+": "+", "-": "-", "*": "*", "/": "/", "mod": "%",
            "=": "==", "<>": "!=", "<": "<", ">": ">", 
            "<=": "<=", ">=": ">=", "&&": "and", "||": "or",
            "^": "+",  # String concatenation
        }
        
        operator = op_map.get(node.operator, node.operator)
        
        return RunaBinaryOp(
            left=left,
            operator=operator,
            right=right,
            source_info=node.source_info
        )
    
    def convert_LIGOUnaryOp(self, node: LIGOUnaryOp) -> RunaUnaryOp:
        """Convert LIGO unary operation to Runa unary operation."""
        operand = self.convert(node.operand)
        
        op_map = {
            "-": "-",
            "not": "not"
        }
        
        operator = op_map.get(node.operator, node.operator)
        
        return RunaUnaryOp(
            operator=operator,
            operand=operand,
            source_info=node.source_info
        )
    
    def convert_LIGOFunctionCall(self, node: LIGOFunctionCall) -> FunctionCall:
        """Convert LIGO function call to Runa function call."""
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.arguments]
        
        return FunctionCall(
            function=function,
            args=args,
            keywords={},
            source_info=node.source_info
        )
    
    def convert_LIGOConditional(self, node: LIGOConditional) -> IfStatement:
        """Convert LIGO conditional to Runa conditional."""
        test = self.convert(node.condition)
        if_true = self.convert(node.then_expr)
        if_false = self.convert(node.else_expr) if node.else_expr else None
        
        return IfStatement(
            test=test,
            if_true=if_true,
            if_false=if_false,
            source_info=node.source_info
        )
    
    def convert_LIGOLambda(self, node: LIGOLambda) -> ProcessDefinition:
        """Convert LIGO lambda to Runa lambda."""
        params = [p.name for p in node.parameters]
        body = self.convert(node.body)
        
        return ProcessDefinition(
            params=params,
            body=body,
            source_info=node.source_info
        )
    
    def convert_LIGORecordAccess(self, node: LIGORecordAccess) -> RunaAttributeAccess:
        """Convert LIGO record access to Runa attribute access."""
        object = self.convert(node.record)
        
        return RunaAttributeAccess(
            object=object,
            attribute=node.field,
            source_info=node.source_info
        )
    
    def convert_LIGOListAccess(self, node: LIGOListAccess) -> IndexAccess:
        """Convert LIGO list access to Runa index access."""
        object = self.convert(node.list_expr)
        index = self.convert(node.index)
        
        return IndexAccess(
            object=object,
            index=index,
            source_info=node.source_info
        )
    
    def convert_LIGOMapAccess(self, node: LIGOMapAccess) -> IndexAccess:
        """Convert LIGO map access to Runa index access."""
        object = self.convert(node.map_expr)
        key = self.convert(node.key)
        
        return IndexAccess(
            object=object,
            index=key,
            source_info=node.source_info
        )
    
    # Statement conversions  
    def convert_LIGOVariableDecl(self, node: LIGOVariableDecl) -> RunaVariableDecl:
        """Convert LIGO variable declaration to Runa variable declaration."""
        value = self.convert(node.value) if node.value else None
        type_hint = self.convert(node.type_annotation) if node.type_annotation else None
        
        return RunaVariableDecl(
            name=node.name,
            type_hint=type_hint,
            value=value,
            is_const=node.is_const,
            source_info=node.source_info
        )
    
    def convert_LIGOFunctionDecl(self, node: LIGOFunctionDecl) -> RunaFunctionDef:
        """Convert LIGO function declaration to Runa function definition."""
        params = []
        for param in node.parameters:
            param_type = self.convert(param.type_annotation) if param.type_annotation else None
            params.append((param.name, param_type))
        
        body_stmts = [self.convert(stmt) for stmt in node.body]
        body = Block(statements=body_stmts)
        
        return_type = self.convert(node.return_type) if node.return_type else None
        
        return RunaFunctionDef(
            name=node.name,
            params=params,
            body=body,
            return_type=return_type,
            decorators=[],
            source_info=node.source_info
        )
    
    def convert_LIGOTypeDecl(self, node: LIGOTypeDecl) -> RunaClassDef:
        """Convert LIGO type declaration to Runa class definition."""
        # Convert type declaration to a class for structured representation
        body = []
        
        if isinstance(node.type_def, LIGORecordType):
            # Add field declarations as class attributes
            for field in node.type_def.fields:
                field_decl = RunaVariableDecl(
                    name=field.name,
                    type_hint=self.convert(field.type_annotation),
                    value=None,
                    source_info=field.source_info
                )
                body.append(field_decl)
        
        return RunaClassDef(
            name=node.name,
            bases=[],
            body=body,
            decorators=[],
            source_info=node.source_info
        )


class RunaToLIGOConverter:
    """Converts Runa AST nodes to LIGO AST nodes."""
    
    def __init__(self, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO):
        self.syntax_style = syntax_style
        
    def convert(self, node: RunaNode) -> LIGONode:
        """Convert any Runa AST node to corresponding LIGO AST node."""
        method_name = f"convert_{type(node).__name__}"
        converter = getattr(self, method_name, self.convert_generic)
        return converter(node)
    
    def convert_generic(self, node: RunaNode) -> LIGONode:
        """Generic converter for unknown node types."""
        return LIGOIdentifier(name=str(node), source_info=node.source_info)
    
    # Module and program conversion
    def convert_RunaModuleDef(self, node: RunaModuleDef) -> LIGOProgram:
        """Convert Runa module to LIGO program."""
        declarations = []
        
        for stmt in node.body:
            ligo_node = self.convert(stmt)
            if ligo_node:
                declarations.append(ligo_node)
        
        return LIGOProgram(
            name=node.name,
            declarations=declarations,
            syntax_style=self.syntax_style,
            source_info=node.source_info
        )
    
    # Type conversions
    def convert_RunaPrimitiveType(self, node: RunaPrimitiveType) -> LIGOPrimitiveType:
        """Convert Runa primitive type to LIGO primitive type."""
        type_map = {
            "int": "int",
            "str": "string",
            "bytes": "bytes", 
            "bool": "bool",
            "None": "unit",
            "decimal": "tez",
            "datetime": "timestamp"
        }
        
        ligo_type = type_map.get(node.name, node.name)
        return LIGOPrimitiveType(name=ligo_type, source_info=node.source_info)
    
    def convert_ListLiteralType(self, node: ListLiteralType) -> LIGOListType:
        """Convert Runa array type to LIGO list type."""
        element_type = self.convert(node.element_type)
        return LIGOListType(element_type=element_type, source_info=node.source_info)
    
    def convert_FunctionType(self, node: FunctionType) -> LIGOFunctionType:
        """Convert Runa function type to LIGO function type."""
        param_types = [self.convert(t) for t in node.param_types]
        return_type = self.convert(node.return_type)
        
        return LIGOFunctionType(
            param_types=param_types,
            return_type=return_type,
            source_info=node.source_info
        )
    
    # Expression conversions
    def convert_StringLiteral(self, node: StringLiteral) -> LIGOLiteral:
        """Convert Runa literal to LIGO literal."""
        return LIGOLiteral(
            value=node.value,
            literal_type=str(node.type_hint) if node.type_hint else None,
            source_info=node.source_info
        )
    
    def convert_Identifier(self, node: Identifier) -> LIGOIdentifier:
        """Convert Runa identifier to LIGO identifier."""
        return LIGOIdentifier(name=node.name, source_info=node.source_info)
    
    def convert_RunaBinaryOp(self, node: RunaBinaryOp) -> LIGOBinaryOp:
        """Convert Runa binary operation to LIGO binary operation."""
        left = self.convert(node.left)
        right = self.convert(node.right)
        
        # Map Runa operators to LIGO operators
        op_map = {
            "==": "=", "!=": "<>", "and": "&&", "or": "||",
            "%": "mod"
        }
        
        operator = op_map.get(node.operator, node.operator)
        
        return LIGOBinaryOp(
            left=left,
            operator=operator,
            right=right,
            source_info=node.source_info
        )
    
    def convert_RunaUnaryOp(self, node: RunaUnaryOp) -> LIGOUnaryOp:
        """Convert Runa unary operation to LIGO unary operation."""
        operand = self.convert(node.operand)
        
        op_map = {
            "not": "not"
        }
        
        operator = op_map.get(node.operator, node.operator)
        
        return LIGOUnaryOp(
            operator=operator,
            operand=operand,
            source_info=node.source_info
        )
    
    def convert_FunctionCall(self, node: FunctionCall) -> LIGOFunctionCall:
        """Convert Runa function call to LIGO function call."""
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.args]
        
        return LIGOFunctionCall(
            function=function,
            arguments=args,
            source_info=node.source_info
        )
    
    def convert_IfStatement(self, node: IfStatement) -> LIGOConditional:
        """Convert Runa conditional to LIGO conditional."""
        condition = self.convert(node.test)
        then_expr = self.convert(node.if_true)
        else_expr = self.convert(node.if_false) if node.if_false else None
        
        return LIGOConditional(
            condition=condition,
            then_expr=then_expr,
            else_expr=else_expr,
            source_info=node.source_info
        )
    
    def convert_RunaAttributeAccess(self, node: RunaAttributeAccess) -> LIGORecordAccess:
        """Convert Runa attribute access to LIGO record access."""
        record = self.convert(node.object)
        
        return LIGORecordAccess(
            record=record,
            field=node.attribute,
            source_info=node.source_info
        )
    
    def convert_IndexAccess(self, node: IndexAccess) -> LIGOListAccess:
        """Convert Runa index access to LIGO list access."""
        list_expr = self.convert(node.object)
        index = self.convert(node.index)
        
        return LIGOListAccess(
            list_expr=list_expr,
            index=index,
            source_info=node.source_info
        )
    
    # Statement conversions
    def convert_RunaVariableDecl(self, node: RunaVariableDecl) -> LIGOVariableDecl:
        """Convert Runa variable declaration to LIGO variable declaration."""
        value = self.convert(node.value) if node.value else None
        type_annotation = self.convert(node.type_hint) if node.type_hint else None
        
        return LIGOVariableDecl(
            name=node.name,
            type_annotation=type_annotation,
            value=value,
            is_const=node.is_const,
            source_info=node.source_info
        )
    
    def convert_RunaFunctionDef(self, node: RunaFunctionDef) -> LIGOFunctionDecl:
        """Convert Runa function definition to LIGO function declaration."""
        parameters = []
        for param_name, param_type in node.params:
            type_annotation = self.convert(param_type) if param_type else None
            parameters.append(LIGOParameter(
                name=param_name,
                type_annotation=type_annotation
            ))
        
        body = []
        if isinstance(node.body, Block):
            body = [self.convert(stmt) for stmt in node.body.statements]
        else:
            body = [self.convert(node.body)]
        
        return_type = self.convert(node.return_type) if node.return_type else None
        
        return LIGOFunctionDecl(
            name=node.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            visibility=LIGOVisibility.PUBLIC,
            source_info=node.source_info
        )


def ligo_to_runa(ligo_ast: LIGONode, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO) -> RunaNode:
    """Convert LIGO AST to Runa AST."""
    converter = LIGOToRunaConverter(syntax_style)
    return converter.convert(ligo_ast)


def runa_to_ligo(runa_ast: RunaNode, syntax_style: LIGOSyntax = LIGOSyntax.JSLIGO) -> LIGONode:
    """Convert Runa AST to LIGO AST."""
    converter = RunaToLIGOConverter(syntax_style)
    return converter.convert(runa_ast) 