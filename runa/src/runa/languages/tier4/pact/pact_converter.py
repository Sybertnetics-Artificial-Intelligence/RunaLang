#!/usr/bin/env python3
"""
Pact-Runa AST Converter

Bidirectional converter between Pact AST and Runa AST.
Handles LISP-like syntax, capabilities, formal verification, and Kadena-specific features.
"""

from typing import Optional, List, Dict, Any, Union
from ...runa.runa_ast import *
from .pact_ast import *


class PactToRunaConverter:
    """Converts Pact AST to Runa AST."""
    
    def __init__(self):
        self.symbol_table = {}
        self.capability_mappings = {}
    
    def convert_program(self, pact_program: PactProgram) -> Program:
        """Convert Pact program to Runa program."""
        runa_modules = []
        
        for module in pact_program.modules:
            runa_module = self.convert_module(module)
            if runa_module:
                runa_modules.append(runa_module)
        
        return Program(
            name="PactProgram",
            modules=runa_modules,
            metadata={"source_language": "pact", "target": "kadena"}
        )
    
    def convert_module(self, pact_module: PactModule) -> RunaModule:
        """Convert Pact module to Runa module."""
        runa_declarations = []
        
        for decl in pact_module.declarations:
            runa_decl = self.convert_declaration(decl)
            if runa_decl:
                runa_declarations.append(runa_decl)
        
        return RunaModule(
            name=pact_module.name,
            imports=[],
            declarations=runa_declarations,
            metadata={
                "source_language": "pact",
                "governance": str(pact_module.governance) if pact_module.governance else None,
                "implements": pact_module.implements,
                "blessed": pact_module.blessed
            }
        )
    
    def convert_declaration(self, decl: PactDeclaration) -> Optional[Declaration]:
        """Convert Pact declaration to Runa declaration."""
        if isinstance(decl, PactDefun):
            return self.convert_defun(decl)
        elif isinstance(decl, PactDefcap):
            return self.convert_defcap(decl)
        elif isinstance(decl, PactDefconst):
            return self.convert_defconst(decl)
        elif isinstance(decl, PactDefschema):
            return self.convert_defschema(decl)
        elif isinstance(decl, PactDeftable):
            return self.convert_deftable(decl)
        else:
            return None
    
    def convert_defun(self, defun: PactDefun) -> ProcessDefinition:
        """Convert Pact function to Runa function."""
        runa_params = []
        for param in defun.parameters:
            runa_params.append(Parameter(
                name=param.name,
                parameter_type=self.convert_type(param.pact_type) if param.pact_type else None
            ))
        
        return ProcessDefinition(
            name=defun.name,
            parameters=runa_params,
            return_type=self.convert_type(defun.return_type) if defun.return_type else None,
            body=self.convert_expression(defun.body),
            decorators=[],
            metadata={
                "source_language": "pact",
                "documentation": defun.documentation,
                "formal_verification": len(defun.model) > 0
            }
        )
    
    def convert_defcap(self, defcap: PactDefcap) -> ProcessDefinition:
        """Convert Pact capability to Runa function with capability decorator."""
        runa_params = []
        for param in defcap.parameters:
            runa_params.append(Parameter(
                name=param.name,
                parameter_type=self.convert_type(param.pact_type) if param.pact_type else None
            ))
        
        return ProcessDefinition(
            name=defcap.name,
            parameters=runa_params,
            return_type=BasicType(name="Boolean"),
            body=self.convert_expression(defcap.body),
            decorators=[RunaDecorator(name="capability", arguments=[])],
            metadata={
                "source_language": "pact",
                "capability": True,
                "managed": str(defcap.managed) if defcap.managed else None
            }
        )
    
    def convert_expression(self, expr: Optional[PactExpression]) -> Optional[Expression]:
        """Convert Pact expression to Runa expression."""
        if not expr:
            return None
        
        if isinstance(expr, PactLiteral):
            return self.convert_literal(expr)
        elif isinstance(expr, PactVariable):
            return Identifier(name=expr.name)
        elif isinstance(expr, PactFunctionCall):
            return self.convert_function_call(expr)
        elif isinstance(expr, PactIf):
            return self.convert_if(expr)
        elif isinstance(expr, PactLet):
            return self.convert_let(expr)
        elif isinstance(expr, PactObject):
            return self.convert_object(expr)
        else:
            return None
    
    def convert_literal(self, literal: PactLiteral) -> StringLiteral:
        """Convert Pact literal to Runa literal."""
        type_mapping = {
            "integer": StringLiteralType.INTEGER,
            "decimal": StringLiteralType.FLOAT,
            "string": StringLiteralType.STRING,
            "bool": StringLiteralType.BOOLEAN
        }
        
        return StringLiteral(
            value=literal.value,
            literal_type=type_mapping.get(literal.literal_type, StringLiteralType.STRING)
        )
    
    def convert_function_call(self, call: PactFunctionCall) -> FunctionCall:
        """Convert Pact function call to Runa function call."""
        runa_args = []
        for arg in call.arguments:
            runa_arg = self.convert_expression(arg)
            if runa_arg:
                runa_args.append(runa_arg)
        
        return FunctionCall(
            function=Identifier(name=call.function),
            arguments=runa_args,
            metadata={"source_language": "pact"}
        )
    
    def convert_type(self, pact_type: Optional[PactType]) -> Optional[BasicType]:
        """Convert Pact type to Runa type."""
        if not pact_type:
            return None
        
        type_mapping = {
            "integer": "Integer",
            "decimal": "Float",
            "string": "String",
            "bool": "Boolean",
            "object": "Object",
            "list": "List",
            "time": "DateTime",
            "keyset": "Keyset",
            "guard": "Guard"
        }
        
        runa_name = type_mapping.get(pact_type.name, pact_type.name)
        return BasicType(name=runa_name)


class RunaToPactConverter:
    """Converts Runa AST to Pact AST."""
    
    def __init__(self):
        self.symbol_table = {}
    
    def convert_program(self, runa_program: Program) -> PactProgram:
        """Convert Runa program to Pact program."""
        pact_modules = []
        
        for module in runa_program.modules:
            pact_module = self.convert_module(module)
            if pact_module:
                pact_modules.append(pact_module)
        
        return PactProgram(modules=pact_modules)
    
    def convert_module(self, runa_module: RunaModule) -> PactModule:
        """Convert Runa module to Pact module."""
        pact_declarations = []
        
        for decl in runa_module.declarations:
            pact_decl = self.convert_declaration(decl)
            if pact_decl:
                pact_declarations.append(pact_decl)
        
        return PactModule(
            name=runa_module.name,
            declarations=pact_declarations
        )
    
    def convert_declaration(self, decl: Declaration) -> Optional[PactDeclaration]:
        """Convert Runa declaration to Pact declaration."""
        if isinstance(decl, ProcessDefinition):
            # Check if it's a capability
            if any(d.name == "capability" for d in decl.decorators):
                return self.convert_to_defcap(decl)
            else:
                return self.convert_to_defun(decl)
        elif isinstance(decl, LetStatement):
            return self.convert_to_defconst(decl)
        else:
            return None
    
    def convert_to_defun(self, decl: ProcessDefinition) -> PactDefun:
        """Convert Runa function to Pact defun."""
        pact_params = []
        for param in decl.parameters:
            pact_params.append(PactParameter(
                name=param.name,
                pact_type=self.convert_type(param.parameter_type)
            ))
        
        return PactDefun(
            name=decl.name,
            parameters=pact_params,
            return_type=self.convert_type(decl.return_type),
            body=self.convert_expression(decl.body)
        )
    
    def convert_to_defcap(self, decl: ProcessDefinition) -> PactDefcap:
        """Convert Runa function to Pact capability."""
        pact_params = []
        for param in decl.parameters:
            pact_params.append(PactParameter(
                name=param.name,
                pact_type=self.convert_type(param.parameter_type)
            ))
        
        return PactDefcap(
            name=decl.name,
            parameters=pact_params,
            body=self.convert_expression(decl.body)
        )
    
    def convert_expression(self, expr: Optional[Expression]) -> Optional[PactExpression]:
        """Convert Runa expression to Pact expression."""
        if not expr:
            return None
        
        if isinstance(expr, StringLiteral):
            return self.convert_literal(expr)
        elif isinstance(expr, Identifier):
            return PactVariable(name=expr.name)
        elif isinstance(expr, FunctionCall):
            return self.convert_function_call(expr)
        else:
            return None
    
    def convert_literal(self, literal: StringLiteral) -> PactLiteral:
        """Convert Runa literal to Pact literal."""
        type_mapping = {
            StringLiteralType.INTEGER: "integer",
            StringLiteralType.FLOAT: "decimal",
            StringLiteralType.STRING: "string",
            StringLiteralType.BOOLEAN: "bool"
        }
        
        return PactLiteral(
            value=literal.value,
            literal_type=type_mapping.get(literal.literal_type, "string")
        )
    
    def convert_function_call(self, call: FunctionCall) -> PactFunctionCall:
        """Convert Runa function call to Pact function call."""
        function_name = call.function.name if isinstance(call.function, Identifier) else str(call.function)
        
        pact_args = []
        for arg in call.arguments:
            pact_arg = self.convert_expression(arg)
            if pact_arg:
                pact_args.append(pact_arg)
        
        return PactFunctionCall(function=function_name, arguments=pact_args)
    
    def convert_type(self, runa_type: Optional[BasicType]) -> Optional[PactType]:
        """Convert Runa type to Pact type."""
        if not runa_type:
            return None
        
        type_mapping = {
            "Integer": "integer",
            "Float": "decimal",
            "String": "string",
            "Boolean": "bool",
            "Object": "object",
            "List": "list",
            "DateTime": "time"
        }
        
        pact_name = type_mapping.get(runa_type.name, runa_type.name.lower())
        return PactType(name=pact_name)


def pact_to_runa(pact_ast: PactProgram) -> Program:
    """Convert Pact AST to Runa AST."""
    converter = PactToRunaConverter()
    return converter.convert_program(pact_ast)


def runa_to_pact(runa_ast: Program) -> PactProgram:
    """Convert Runa AST to Pact AST."""
    converter = RunaToPactConverter()
    return converter.convert_program(runa_ast) 