#!/usr/bin/env python3
"""
OCaml ↔ Runa Converter
"""

from typing import List, Optional, Dict, Any, Union
from runa.core.ast import *
from .ocaml_ast import *


class OcamlToRunaConverter:
    """Converts OCaml AST to Runa AST."""
    
    def __init__(self):
        self.type_mappings = {
            'int': 'Integer',
            'float': 'Float', 
            'string': 'String',
            'bool': 'Boolean',
            'unit': 'Unit'
        }
    
    def convert(self, node: OcamlNode) -> RunaNode:
        method_name = f"convert_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.convert_generic)
        return method(node)
    
    def convert_generic(self, node):
        raise NotImplementedError(f"Conversion for {type(node)} not implemented")
    
    def convert_ocamlmodule(self, node: OcamlModule) -> RunaModule:
        statements = [self.convert(decl) for decl in node.declarations]
        return RunaModule(name="Main", statements=statements, imports=[], exports=[])
    
    def convert_ocamlliteral(self, node: OcamlLiteral) -> StringLiteral:
        return StringLiteral(node.value)
    
    def convert_ocamlidentifier(self, node: OcamlIdentifier) -> RunaVariable:
        return RunaVariable(node.name)
    
    def convert_ocamlconstructor(self, node: OcamlConstructor) -> RunaVariable:
        return RunaVariable(node.name)
    
    def convert_ocamlapplication(self, node: OcamlApplication) -> FunctionCall:
        return FunctionCall(
            function=self.convert(node.function),
            arguments=[self.convert(arg) for arg in node.arguments]
        )
    
    def convert_ocamlfunction(self, node: OcamlFunction) -> ProcessDefinition:
        parameters = []
        for param in node.parameters:
            if isinstance(param, OcamlVariablePattern):
                parameters.append(Parameter(param.name, None))
        return ProcessDefinition(parameters=parameters, body=self.convert(node.body))
    
    def convert_ocamllet(self, node: OcamlLet) -> LetStatement:
        if isinstance(node.pattern, OcamlVariablePattern):
            name = node.pattern.name
        else:
            name = "temp"
        
        return LetStatement(
            name=name,
            value=self.convert(node.value),
            body=self.convert(node.body)
        )
    
    def convert_ocamlif(self, node: OcamlIf) -> RunaIf:
        return RunaIf(
            condition=self.convert(node.condition),
            then_branch=self.convert(node.then_expr),
            else_branch=self.convert(node.else_expr) if node.else_expr else StringLiteral(None)
        )
    
    def convert_ocamlmatch(self, node: OcamlMatch) -> RunaMatch:
        cases = []
        for case in node.cases:
            pattern = self.convert_pattern(case.pattern)
            body = self.convert(case.expression)
            cases.append(RunaMatchCase(pattern=pattern, body=body))
        
        return RunaMatch(expression=self.convert(node.expression), cases=cases)
    
    def convert_ocamltuple(self, node: OcamlTuple) -> RunaTuple:
        return RunaTuple([self.convert(elem) for elem in node.elements])
    
    def convert_ocamllist(self, node: OcamlList) -> ListLiteral:
        return ListLiteral([self.convert(elem) for elem in node.elements])
    
    def convert_ocamlvaluedeclaration(self, node: OcamlValueDeclaration) -> RunaFunction:
        if isinstance(node.pattern, OcamlVariablePattern):
            name = node.pattern.name
        else:
            name = "anonymous"
        
        return RunaFunction(
            name=name,
            parameters=[],
            body=self.convert(node.expression),
            return_type=None
        )
    
    def convert_pattern(self, pattern: OcamlPattern) -> Pattern:
        if isinstance(pattern, OcamlVariablePattern):
            return RunaVariablePattern(pattern.name)
        elif isinstance(pattern, OcamlWildcardPattern):
            return WildcardPattern()
        elif isinstance(pattern, OcamlConstructorPattern):
            return RunaConstructorPattern(
                name=pattern.constructor,
                patterns=[self.convert_pattern(p) for p in pattern.patterns]
            )
        else:
            return WildcardPattern()


class RunaToOcamlConverter:
    """Converts Runa AST to OCaml AST."""
    
    def __init__(self):
        self.type_mappings = {
            'Integer': 'int',
            'Float': 'float',
            'String': 'string', 
            'Boolean': 'bool',
            'Unit': 'unit'
        }
    
    def convert(self, node: RunaNode) -> OcamlNode:
        method_name = f"convert_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.convert_generic)
        return method(node)
    
    def convert_generic(self, node):
        raise NotImplementedError(f"Conversion for {type(node)} not implemented")
    
    def convert_runamodule(self, node: RunaModule) -> OcamlModule:
        declarations = []
        for stmt in node.statements:
            declarations.append(self.convert(stmt))
        return OcamlModule(declarations=declarations)
    
    def convert_runaliteral(self, node: StringLiteral) -> OcamlLiteral:
        if isinstance(node.value, int):
            literal_type = "int"
        elif isinstance(node.value, float):
            literal_type = "float"
        elif isinstance(node.value, str):
            literal_type = "string"
        elif isinstance(node.value, bool):
            literal_type = "bool"
        else:
            literal_type = "string"
        
        return OcamlLiteral(value=node.value, literal_type=literal_type)
    
    def convert_runavariable(self, node: RunaVariable) -> OcamlIdentifier:
        if node.name and node.name[0].isupper():
            return OcamlConstructor(name=node.name)
        return OcamlIdentifier(name=node.name)
    
    def convert_runacall(self, node: FunctionCall) -> OcamlApplication:
        return OcamlApplication(
            function=self.convert(node.function),
            arguments=[self.convert(arg) for arg in node.arguments]
        )
    
    def convert_runalambda(self, node: ProcessDefinition) -> OcamlFunction:
        parameters = []
        for param in node.parameters:
            parameters.append(OcamlVariablePattern(name=param.name))
        
        return OcamlFunction(
            parameters=parameters,
            body=self.convert(node.body)
        )
    
    def convert_runafunction(self, node: RunaFunction) -> OcamlValueDeclaration:
        pattern = OcamlVariablePattern(name=node.name)
        
        if node.parameters:
            # Create function expression
            func_params = []
            for param in node.parameters:
                func_params.append(OcamlVariablePattern(name=param.name))
            
            expression = OcamlFunction(
                parameters=func_params,
                body=self.convert(node.body)
            )
        else:
            expression = self.convert(node.body)
        
        return OcamlValueDeclaration(
            pattern=pattern,
            expression=expression,
            recursive=False
        )


def ocaml_to_runa(ocaml_ast: OcamlNode) -> RunaNode:
    """Convert OCaml AST to Runa AST."""
    converter = OcamlToRunaConverter()
    return converter.convert(ocaml_ast)


def runa_to_ocaml(runa_ast: RunaNode) -> OcamlNode:
    """Convert Runa AST to OCaml AST."""
    converter = RunaToOcamlConverter()
    return converter.convert(runa_ast)


__all__ = [
    "OcamlToRunaConverter", "RunaToOcamlConverter",
    "ocaml_to_runa", "runa_to_ocaml"
] 