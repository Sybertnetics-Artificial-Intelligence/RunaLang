"""
SmartPy AST ↔ Runa AST Converter

Handles bidirectional conversion between SmartPy AST nodes and Runa AST nodes.
SmartPy provides Python-like syntax for Tezos smart contracts.
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

from .smartpy_ast import *


class SmartPyToRunaConverter:
    """Converts SmartPy AST nodes to Runa AST nodes."""
    
    def __init__(self):
        self.current_contract = None
        
    def convert(self, node: SmartPyNode) -> RunaNode:
        """Convert any SmartPy AST node to corresponding Runa AST node."""
        method_name = f"convert_{type(node).__name__}"
        converter = getattr(self, method_name, self.convert_generic)
        return converter(node)
    
    def convert_generic(self, node: SmartPyNode) -> RunaNode:
        """Generic converter for unknown node types."""
        return Identifier(name=str(node), source_info=node.source_info)
    
    # Module and program conversion
    def convert_SmartPyModule(self, node: SmartPyModule) -> RunaModuleDef:
        """Convert SmartPy module to Runa module."""
        statements = []
        
        # Convert imports
        for import_node in node.imports:
            statements.append(self.convert(import_node))
        
        # Convert declarations
        for decl in node.declarations:
            runa_node = self.convert(decl)
            if runa_node:
                statements.append(runa_node)
        
        return RunaModuleDef(
            name="smartpy_module",
            body=statements,
            imports=[],
            exports=[],
            source_info=node.source_info
        )
    
    def convert_SmartPyProgram(self, node: SmartPyProgram) -> RunaModuleDef:
        """Convert SmartPy program to Runa module."""
        return self.convert(node.main_module)
    
    # Import conversion
    def convert_SmartPyImport(self, node: SmartPyImport) -> RunaImport:
        """Convert SmartPy import to Runa import."""
        return RunaImport(
            module=node.module,
            alias=node.alias,
            names=node.names or [],
            source_info=node.source_info
        )
    
    # Type conversions
    def convert_SmartPyTypeAnnotation(self, node: SmartPyTypeAnnotation) -> BasicType:
        """Convert SmartPy type annotation to Runa type."""
        if isinstance(node, SmartPyPrimitiveType):
            return self.convert_SmartPyPrimitiveType(node)
        elif isinstance(node, SmartPyListType):
            return self.convert_SmartPyListType(node)
        elif isinstance(node, SmartPyMapType):
            return self.convert_SmartPyMapType(node)
        elif isinstance(node, SmartPyRecordType):
            return self.convert_SmartPyRecordType(node)
        else:
            return RunaPrimitiveType(name="unknown", source_info=node.source_info)
    
    def convert_SmartPyPrimitiveType(self, node: SmartPyPrimitiveType) -> RunaPrimitiveType:
        """Convert SmartPy primitive type to Runa primitive type."""
        type_map = {
            SmartPyType.INT: "int",
            SmartPyType.NAT: "int",
            SmartPyType.STRING: "str",
            SmartPyType.BYTES: "bytes",
            SmartPyType.BOOL: "bool",
            SmartPyType.UNIT: "None",
            SmartPyType.ADDRESS: "str",
            SmartPyType.TIMESTAMP: "datetime",
            SmartPyType.MUTEZ: "decimal"
        }
        
        runa_type = type_map.get(node.type_name, str(node.type_name.value))
        return RunaPrimitiveType(name=runa_type, source_info=node.source_info)
    
    def convert_SmartPyListType(self, node: SmartPyListType) -> ListLiteralType:
        """Convert SmartPy list type to Runa array type."""
        element_type = self.convert(node.element_type)
        return ListLiteralType(element_type=element_type, source_info=node.source_info)
    
    def convert_SmartPyMapType(self, node: SmartPyMapType) -> GenericType:
        """Convert SmartPy map type to Runa generic type."""
        key_type = self.convert(node.key_type)
        value_type = self.convert(node.value_type)
        
        return GenericType(
            base_type=RunaPrimitiveType(name="dict"),
            type_args=[key_type, value_type],
            source_info=node.source_info
        )
    
    def convert_SmartPyRecordType(self, node: SmartPyRecordType) -> RunaRecordType:
        """Convert SmartPy record type to Runa record type."""
        fields = {}
        for field_name, field_type in node.fields.items():
            fields[field_name] = self.convert(field_type)
        
        return RunaRecordType(fields=fields, source_info=node.source_info)
    
    # Expression conversions
    def convert_SmartPyLiteral(self, node: SmartPyLiteral) -> StringLiteral:
        """Convert SmartPy literal to Runa literal."""
        return StringLiteral(
            value=node.value,
            type_hint=node.type_hint,
            source_info=node.source_info
        )
    
    def convert_SmartPyIdentifier(self, node: SmartPyIdentifier) -> Identifier:
        """Convert SmartPy identifier to Runa identifier."""
        return Identifier(
            name=node.name,
            source_info=node.source_info
        )
    
    def convert_SmartPyBinaryOp(self, node: SmartPyBinaryOp) -> RunaBinaryOp:
        """Convert SmartPy binary operation to Runa binary operation."""
        left = self.convert(node.left)
        right = self.convert(node.right)
        
        return RunaBinaryOp(
            left=left,
            operator=node.operator,
            right=right,
            source_info=node.source_info
        )
    
    def convert_SmartPyUnaryOp(self, node: SmartPyUnaryOp) -> RunaUnaryOp:
        """Convert SmartPy unary operation to Runa unary operation."""
        operand = self.convert(node.operand)
        
        return RunaUnaryOp(
            operator=node.operator,
            operand=operand,
            source_info=node.source_info
        )
    
    def convert_SmartPyFunctionCall(self, node: SmartPyFunctionCall) -> FunctionCall:
        """Convert SmartPy function call to Runa function call."""
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.args]
        keywords = {k: self.convert(v) for k, v in node.keywords.items()}
        
        return FunctionCall(
            function=function,
            args=args,
            keywords=keywords,
            source_info=node.source_info
        )
    
    def convert_SmartPyAttributeAccess(self, node: SmartPyAttributeAccess) -> RunaAttributeAccess:
        """Convert SmartPy attribute access to Runa attribute access."""
        object = self.convert(node.object)
        
        return RunaAttributeAccess(
            object=object,
            attribute=node.attribute,
            source_info=node.source_info
        )
    
    def convert_SmartPyIndexAccess(self, node: SmartPyIndexAccess) -> IndexAccess:
        """Convert SmartPy index access to Runa index access."""
        object = self.convert(node.object)
        index = self.convert(node.index)
        
        return IndexAccess(
            object=object,
            index=index,
            source_info=node.source_info
        )
    
    def convert_SmartPyConditional(self, node: SmartPyConditional) -> IfStatement:
        """Convert SmartPy conditional to Runa conditional."""
        test = self.convert(node.test)
        if_true = self.convert(node.if_true)
        if_false = self.convert(node.if_false)
        
        return IfStatement(
            test=test,
            if_true=if_true,
            if_false=if_false,
            source_info=node.source_info
        )
    
    def convert_SmartPyLambda(self, node: SmartPyLambda) -> ProcessDefinition:
        """Convert SmartPy lambda to Runa lambda."""
        body = self.convert(node.body)
        
        return ProcessDefinition(
            params=node.parameters,
            body=body,
            source_info=node.source_info
        )
    
    def convert_SmartPyListLiteral(self, node: SmartPyListLiteral) -> ListLiteral:
        """Convert SmartPy list literal to Runa list literal."""
        elements = [self.convert(elem) for elem in node.elements]
        
        return ListLiteral(
            elements=elements,
            source_info=node.source_info
        )
    
    def convert_SmartPyMapLiteral(self, node: SmartPyMapLiteral) -> RunaDictLiteral:
        """Convert SmartPy map literal to Runa dict literal."""
        pairs = {}
        for key_expr, value_expr in node.pairs:
            # For dict literals, we need string keys
            if isinstance(key_expr, SmartPyLiteral):
                key = str(key_expr.value)
            else:
                key = str(key_expr)
            pairs[key] = self.convert(value_expr)
        
        return RunaDictLiteral(
            pairs=pairs,
            source_info=node.source_info
        )
    
    # SmartPy built-in expressions
    def convert_SmartPySender(self, node: SmartPySender) -> Identifier:
        """Convert sp.sender to Runa identifier."""
        return Identifier(name="sender", source_info=node.source_info)
    
    def convert_SmartPyAmount(self, node: SmartPyAmount) -> Identifier:
        """Convert sp.amount to Runa identifier."""
        return Identifier(name="amount", source_info=node.source_info)
    
    def convert_SmartPyBalance(self, node: SmartPyBalance) -> Identifier:
        """Convert sp.balance to Runa identifier."""
        return Identifier(name="balance", source_info=node.source_info)
    
    def convert_SmartPyNow(self, node: SmartPyNow) -> Identifier:
        """Convert sp.now to Runa identifier."""
        return Identifier(name="now", source_info=node.source_info)
    
    # Statement conversions
    def convert_SmartPyAssignment(self, node: SmartPyAssignment) -> SetStatement:
        """Convert SmartPy assignment to Runa assignment."""
        target = self.convert(node.target)
        value = self.convert(node.value)
        
        return SetStatement(
            target=target,
            value=value,
            source_info=node.source_info
        )
    
    def convert_SmartPyAugmentedAssignment(self, node: SmartPyAugmentedAssignment) -> SetStatement:
        """Convert SmartPy augmented assignment to Runa assignment."""
        target = self.convert(node.target)
        value = self.convert(node.value)
        
        # Convert += to regular assignment with binary operation
        if node.operator in ["+=", "-=", "*=", "/="]:
            op = node.operator[:-1]  # Remove '='
            value = RunaBinaryOp(
                left=target,
                operator=op,
                right=value,
                source_info=node.source_info
            )
        
        return SetStatement(
            target=target,
            value=value,
            source_info=node.source_info
        )
    
    def convert_SmartPyExpressionStatement(self, node: SmartPyExpressionStatement) -> RunaNode:
        """Convert SmartPy expression statement."""
        return self.convert(node.expression)
    
    def convert_SmartPyIf(self, node: SmartPyIf) -> RunaIf:
        """Convert SmartPy if statement to Runa if."""
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        orelse = [self.convert(stmt) for stmt in node.orelse]
        
        return RunaIf(
            test=test,
            body=body,
            orelse=orelse,
            source_info=node.source_info
        )
    
    def convert_SmartPyFor(self, node: SmartPyFor) -> RunaFor:
        """Convert SmartPy for statement to Runa for."""
        iter_expr = self.convert(node.iter)
        body = [self.convert(stmt) for stmt in node.body]
        
        return RunaFor(
            target=node.target,
            iter=iter_expr,
            body=body,
            source_info=node.source_info
        )
    
    def convert_SmartPyWhile(self, node: SmartPyWhile) -> RunaWhile:
        """Convert SmartPy while statement to Runa while."""
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        
        return RunaWhile(
            test=test,
            body=body,
            source_info=node.source_info
        )
    
    def convert_SmartPyReturn(self, node: SmartPyReturn) -> ReturnStatement:
        """Convert SmartPy return statement to Runa return."""
        value = self.convert(node.value) if node.value else None
        
        return ReturnStatement(
            value=value,
            source_info=node.source_info
        )
    
    # SmartPy specific statements
    def convert_SmartPyVerify(self, node: SmartPyVerify) -> FunctionCall:
        """Convert sp.verify() to Runa function call."""
        condition = self.convert(node.condition)
        args = [condition]
        
        if node.message:
            args.append(self.convert(node.message))
        
        return FunctionCall(
            function=Identifier(name="verify"),
            args=args,
            keywords={},
            source_info=node.source_info
        )
    
    def convert_SmartPyFailwith(self, node: SmartPyFailwith) -> FunctionCall:
        """Convert sp.failwith() to Runa function call."""
        value = self.convert(node.value)
        
        return FunctionCall(
            function=Identifier(name="fail"),
            args=[value],
            keywords={},
            source_info=node.source_info
        )
    
    # Declaration conversions
    def convert_SmartPyContractDef(self, node: SmartPyContractDef) -> RunaClassDef:
        """Convert SmartPy contract definition to Runa class."""
        self.current_contract = node
        
        body = []
        
        # Convert init method
        if node.init_method:
            body.append(self.convert(node.init_method))
        
        # Convert regular methods
        for method in node.methods:
            body.append(self.convert(method))
        
        # Convert entry points
        for entry_point in node.entry_points:
            body.append(self.convert(entry_point))
        
        self.current_contract = None
        
        return RunaClassDef(
            name=node.name,
            bases=node.base_classes,
            body=body,
            decorators=[],
            source_info=node.source_info
        )
    
    def convert_SmartPyMethodDef(self, node: SmartPyMethodDef) -> RunaFunctionDef:
        """Convert SmartPy method definition to Runa function."""
        params = [(param, None) for param in node.parameters]
        body_stmts = [self.convert(stmt) for stmt in node.body]
        body = Block(statements=body_stmts)
        
        decorators = []
        if node.is_entry_point:
            decorators.append("entry_point")
        
        return RunaFunctionDef(
            name=node.name,
            params=params,
            body=body,
            return_type=None,
            decorators=decorators,
            source_info=node.source_info
        )
    
    def convert_SmartPyFunctionDef(self, node: SmartPyFunctionDef) -> RunaFunctionDef:
        """Convert SmartPy function definition to Runa function."""
        params = [(param, None) for param in node.parameters]
        body_stmts = [self.convert(stmt) for stmt in node.body]
        body = Block(statements=body_stmts)
        
        return RunaFunctionDef(
            name=node.name,
            params=params,
            body=body,
            return_type=None,
            decorators=node.decorators,
            source_info=node.source_info
        )
    
    def convert_SmartPyVariableDef(self, node: SmartPyVariableDef) -> RunaVariableDecl:
        """Convert SmartPy variable definition to Runa variable declaration."""
        value = self.convert(node.value)
        type_hint = self.convert(node.type_hint) if node.type_hint else None
        
        return RunaVariableDecl(
            name=node.name,
            type_hint=type_hint,
            value=value,
            is_const=False,
            source_info=node.source_info
        )
    
    # Storage initialization
    def convert_SmartPyStorageInit(self, node: SmartPyStorageInit) -> FunctionCall:
        """Convert storage initialization to function call."""
        keywords = {}
        for field_name, field_value in node.fields.items():
            keywords[field_name] = self.convert(field_value)
        
        return FunctionCall(
            function=Identifier(name="init_storage"),
            args=[],
            keywords=keywords,
            source_info=node.source_info
        )


class RunaToSmartPyConverter:
    """Converts Runa AST nodes to SmartPy AST nodes."""
    
    def __init__(self):
        pass
        
    def convert(self, node: RunaNode) -> SmartPyNode:
        """Convert any Runa AST node to corresponding SmartPy AST node."""
        method_name = f"convert_{type(node).__name__}"
        converter = getattr(self, method_name, self.convert_generic)
        return converter(node)
    
    def convert_generic(self, node: RunaNode) -> SmartPyNode:
        """Generic converter for unknown node types."""
        return SmartPyIdentifier(name=str(node), source_info=node.source_info)
    
    # Module conversion
    def convert_RunaModuleDef(self, node: RunaModuleDef) -> SmartPyModule:
        """Convert Runa module to SmartPy module."""
        declarations = []
        imports = []
        
        for stmt in node.body:
            if isinstance(stmt, RunaImport):
                imports.append(self.convert(stmt))
            else:
                smartpy_node = self.convert(stmt)
                if smartpy_node:
                    declarations.append(smartpy_node)
        
        return SmartPyModule(
            declarations=declarations,
            imports=imports,
            source_info=node.source_info
        )
    
    # Import conversion
    def convert_RunaImport(self, node: RunaImport) -> SmartPyImport:
        """Convert Runa import to SmartPy import."""
        return SmartPyImport(
            module=node.module,
            alias=node.alias,
            names=node.names,
            source_info=node.source_info
        )
    
    # Type conversions
    def convert_RunaPrimitiveType(self, node: RunaPrimitiveType) -> SmartPyPrimitiveType:
        """Convert Runa primitive type to SmartPy primitive type."""
        type_map = {
            "int": SmartPyType.INT,
            "str": SmartPyType.STRING,
            "bytes": SmartPyType.BYTES,
            "bool": SmartPyType.BOOL,
            "None": SmartPyType.UNIT,
            "decimal": SmartPyType.MUTEZ,
            "datetime": SmartPyType.TIMESTAMP
        }
        
        smartpy_type = type_map.get(node.name, SmartPyType.STRING)
        return SmartPyPrimitiveType(
            type_name=smartpy_type,
            source_info=node.source_info
        )
    
    def convert_ListLiteralType(self, node: ListLiteralType) -> SmartPyListType:
        """Convert Runa array type to SmartPy list type."""
        element_type = self.convert(node.element_type)
        return SmartPyListType(
            element_type=element_type,
            source_info=node.source_info
        )
    
    # Expression conversions
    def convert_StringLiteral(self, node: StringLiteral) -> SmartPyLiteral:
        """Convert Runa literal to SmartPy literal."""
        return SmartPyLiteral(
            value=node.value,
            type_hint=node.type_hint,
            source_info=node.source_info
        )
    
    def convert_Identifier(self, node: Identifier) -> SmartPyIdentifier:
        """Convert Runa identifier to SmartPy identifier."""
        return SmartPyIdentifier(
            name=node.name,
            source_info=node.source_info
        )
    
    def convert_RunaBinaryOp(self, node: RunaBinaryOp) -> SmartPyBinaryOp:
        """Convert Runa binary operation to SmartPy binary operation."""
        left = self.convert(node.left)
        right = self.convert(node.right)
        
        return SmartPyBinaryOp(
            left=left,
            operator=node.operator,
            right=right,
            source_info=node.source_info
        )
    
    def convert_RunaUnaryOp(self, node: RunaUnaryOp) -> SmartPyUnaryOp:
        """Convert Runa unary operation to SmartPy unary operation."""
        operand = self.convert(node.operand)
        
        return SmartPyUnaryOp(
            operator=node.operator,
            operand=operand,
            source_info=node.source_info
        )
    
    def convert_FunctionCall(self, node: FunctionCall) -> SmartPyFunctionCall:
        """Convert Runa function call to SmartPy function call."""
        function = self.convert(node.function)
        args = [self.convert(arg) for arg in node.args]
        keywords = {k: self.convert(v) for k, v in node.keywords.items()}
        
        return SmartPyFunctionCall(
            function=function,
            args=args,
            keywords=keywords,
            source_info=node.source_info
        )
    
    def convert_RunaAttributeAccess(self, node: RunaAttributeAccess) -> SmartPyAttributeAccess:
        """Convert Runa attribute access to SmartPy attribute access."""
        object = self.convert(node.object)
        
        return SmartPyAttributeAccess(
            object=object,
            attribute=node.attribute,
            source_info=node.source_info
        )
    
    def convert_IndexAccess(self, node: IndexAccess) -> SmartPyIndexAccess:
        """Convert Runa index access to SmartPy index access."""
        object = self.convert(node.object)
        index = self.convert(node.index)
        
        return SmartPyIndexAccess(
            object=object,
            index=index,
            source_info=node.source_info
        )
    
    # Statement conversions
    def convert_SetStatement(self, node: SetStatement) -> SmartPyAssignment:
        """Convert Runa assignment to SmartPy assignment."""
        target = self.convert(node.target)
        value = self.convert(node.value)
        
        return SmartPyAssignment(
            target=target,
            value=value,
            source_info=node.source_info
        )
    
    def convert_RunaIf(self, node: RunaIf) -> SmartPyIf:
        """Convert Runa if statement to SmartPy if."""
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        orelse = [self.convert(stmt) for stmt in node.orelse]
        
        return SmartPyIf(
            test=test,
            body=body,
            orelse=orelse,
            source_info=node.source_info
        )
    
    def convert_RunaFor(self, node: RunaFor) -> SmartPyFor:
        """Convert Runa for statement to SmartPy for."""
        iter_expr = self.convert(node.iter)
        body = [self.convert(stmt) for stmt in node.body]
        
        return SmartPyFor(
            target=node.target,
            iter=iter_expr,
            body=body,
            source_info=node.source_info
        )
    
    def convert_RunaWhile(self, node: RunaWhile) -> SmartPyWhile:
        """Convert Runa while statement to SmartPy while."""
        test = self.convert(node.test)
        body = [self.convert(stmt) for stmt in node.body]
        
        return SmartPyWhile(
            test=test,
            body=body,
            source_info=node.source_info
        )
    
    def convert_ReturnStatement(self, node: ReturnStatement) -> SmartPyReturn:
        """Convert Runa return statement to SmartPy return."""
        value = self.convert(node.value) if node.value else None
        
        return SmartPyReturn(
            value=value,
            source_info=node.source_info
        )
    
    # Declaration conversions
    def convert_RunaClassDef(self, node: RunaClassDef) -> SmartPyContractDef:
        """Convert Runa class definition to SmartPy contract."""
        methods = []
        entry_points = []
        init_method = None
        
        for item in node.body:
            if isinstance(item, RunaFunctionDef):
                method = self.convert_runa_function_to_method(item)
                if method.name == "__init__":
                    init_method = method
                elif method.is_entry_point:
                    entry_points.append(method)
                else:
                    methods.append(method)
        
        return SmartPyContractDef(
            name=node.name,
            base_classes=node.bases,
            methods=methods,
            entry_points=entry_points,
            init_method=init_method,
            source_info=node.source_info
        )
    
    def convert_runa_function_to_method(self, node: RunaFunctionDef) -> SmartPyMethodDef:
        """Convert Runa function to SmartPy method."""
        parameters = [param[0] for param in node.params]
        body = []
        
        if isinstance(node.body, Block):
            body = [self.convert(stmt) for stmt in node.body.statements]
        else:
            body = [self.convert(node.body)]
        
        is_entry_point = "entry_point" in node.decorators
        
        return SmartPyMethodDef(
            name=node.name,
            parameters=parameters,
            body=body,
            decorators=node.decorators,
            is_entry_point=is_entry_point,
            source_info=node.source_info
        )
    
    def convert_RunaFunctionDef(self, node: RunaFunctionDef) -> SmartPyFunctionDef:
        """Convert Runa function definition to SmartPy function."""
        parameters = [param[0] for param in node.params]
        body = []
        
        if isinstance(node.body, Block):
            body = [self.convert(stmt) for stmt in node.body.statements]
        else:
            body = [self.convert(node.body)]
        
        return SmartPyFunctionDef(
            name=node.name,
            parameters=parameters,
            body=body,
            decorators=node.decorators,
            source_info=node.source_info
        )
    
    def convert_RunaVariableDecl(self, node: RunaVariableDecl) -> SmartPyVariableDef:
        """Convert Runa variable declaration to SmartPy variable definition."""
        value = self.convert(node.value) if node.value else None
        type_hint = self.convert(node.type_hint) if node.type_hint else None
        
        return SmartPyVariableDef(
            name=node.name,
            value=value,
            type_hint=type_hint,
            source_info=node.source_info
        )


def smartpy_to_runa(smartpy_ast: SmartPyNode) -> RunaNode:
    """Convert SmartPy AST to Runa AST."""
    converter = SmartPyToRunaConverter()
    return converter.convert(smartpy_ast)


def runa_to_smartpy(runa_ast: RunaNode) -> SmartPyNode:
    """Convert Runa AST to SmartPy AST."""
    converter = RunaToSmartPyConverter()
    return converter.convert(runa_ast) 