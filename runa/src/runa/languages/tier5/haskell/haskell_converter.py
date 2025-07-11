#!/usr/bin/env python3
"""
Haskell ↔ Runa Converter

Bidirectional converter between Haskell AST and Runa AST.
Handles functional programming constructs, pattern matching,
type classes, and Haskell-specific features.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from runa.core.ast import *
from .haskell_ast import *


class HaskellToRunaConverter:
    """Converts Haskell AST to Runa AST."""
    
    def __init__(self):
        self.context = {}
        self.type_mappings = {
            'Int': 'Integer',
            'Float': 'Float',
            'Double': 'Float',
            'String': 'String',
            'Bool': 'Boolean',
            'Char': 'Character',
            '()': 'Unit'
        }
    
    def convert(self, node: HsNode) -> RunaNode:
        """Convert Haskell AST node to Runa AST."""
        method_name = f"convert_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.convert_generic)
        return method(node)
    
    def convert_generic(self, node: HsNode) -> RunaNode:
        """Generic conversion fallback."""
        raise NotImplementedError(f"Conversion for {type(node)} not implemented")
    
    def convert_hsmodule(self, node: HsModule) -> RunaModule:
        """Convert Haskell module."""
        statements = []
        
        # Convert imports
        for imp in node.imports:
            statements.append(self.convert_hsimport(imp))
        
        # Convert declarations
        for decl in node.declarations:
            statements.append(self.convert(decl))
        
        return RunaModule(
            name=node.name or "Main",
            statements=statements,
            imports=[],
            exports=[]
        )
    
    def convert_hsimport(self, node: HsImport) -> RunaImport:
        """Convert import declaration."""
        return RunaImport(
            module=node.module_name,
            alias=node.alias,
            qualified=node.qualified
        )
    
    def convert_hsfunctiondeclaration(self, node: HsFunctionDeclaration) -> RunaFunction:
        """Convert function declaration."""
        # Take first clause for simplicity
        clause = node.clauses[0] if node.clauses else None
        if not clause:
            return RunaFunction(name=node.name, parameters=[], body=StringLiteral(None))
        
        parameters = []
        for pattern in clause.patterns:
            if isinstance(pattern, HsVariablePattern):
                parameters.append(Parameter(pattern.name, None))
        
        body = self.convert(clause.expression)
        
        return RunaFunction(
            name=node.name,
            parameters=parameters,
            body=body,
            return_type=None
        )
    
    def convert_hstypesignature(self, node: HsTypeSignature) -> BasicTypeAnnotation:
        """Convert type signature."""
        return BasicTypeAnnotation(
            target=node.names[0],
            type_expr=self.convert_type(node.type_expr)
        )
    
    def convert_hsdatadeclaration(self, node: HsDataDeclaration) -> RunaClass:
        """Convert data declaration to class."""
        methods = []
        
        for constructor in node.constructors:
            params = []
            for i, field_type in enumerate(constructor.fields):
                field_name = (constructor.field_names[i] 
                             if constructor.field_names and i < len(constructor.field_names)
                             else f"field{i}")
                params.append(Parameter(field_name, self.convert_type(field_type)))
            
            methods.append(RunaFunction(
                name=constructor.name,
                parameters=params,
                body=StringLiteral(None)
            ))
        
        return RunaClass(
            name=node.name,
            base_classes=[],
            methods=methods
        )
    
    def convert_hsliteral(self, node: HsLiteral) -> StringLiteral:
        """Convert literal."""
        return StringLiteral(node.value)
    
    def convert_hsvariable(self, node: HsVariable) -> RunaVariable:
        """Convert variable."""
        return RunaVariable(node.name)
    
    def convert_hsconstructor(self, node: HsConstructor) -> RunaVariable:
        """Convert constructor to variable."""
        return RunaVariable(node.name)
    
    def convert_hsapplication(self, node: HsApplication) -> FunctionCall:
        """Convert function application."""
        return FunctionCall(
            function=self.convert(node.function),
            arguments=[self.convert(arg) for arg in node.arguments]
        )
    
    def convert_hslambda(self, node: HsLambda) -> ProcessDefinition:
        """Convert lambda expression."""
        parameters = []
        for param in node.parameters:
            if isinstance(param, HsVariablePattern):
                parameters.append(Parameter(param.name, None))
        
        return ProcessDefinition(
            parameters=parameters,
            body=self.convert(node.body)
        )
    
    def convert_hsif(self, node: HsIf) -> RunaIf:
        """Convert if expression."""
        return RunaIf(
            condition=self.convert(node.condition),
            then_branch=self.convert(node.then_expr),
            else_branch=self.convert(node.else_expr)
        )
    
    def convert_hscase(self, node: HsCase) -> RunaMatch:
        """Convert case expression."""
        cases = []
        for alt in node.alternatives:
            pattern = self.convert_pattern(alt.pattern)
            body = self.convert(alt.expression)
            cases.append(RunaMatchCase(pattern=pattern, body=body))
        
        return RunaMatch(
            expression=self.convert(node.expression),
            cases=cases
        )
    
    def convert_hslist(self, node: HsList) -> ListLiteral:
        """Convert list expression."""
        return ListLiteral([self.convert(elem) for elem in node.elements])
    
    def convert_hstuple(self, node: HsTuple) -> RunaTuple:
        """Convert tuple expression."""
        return RunaTuple([self.convert(elem) for elem in node.elements])
    
    def convert_pattern(self, pattern: HsPattern) -> Pattern:
        """Convert pattern."""
        if isinstance(pattern, HsVariablePattern):
            return RunaVariablePattern(pattern.name)
        elif isinstance(pattern, HsWildcardPattern):
            return WildcardPattern()
        elif isinstance(pattern, HsLiteralPattern):
            return StringLiteralPattern(pattern.literal.value)
        elif isinstance(pattern, HsConstructorPattern):
            return RunaConstructorPattern(
                name=pattern.constructor,
                patterns=[self.convert_pattern(p) for p in pattern.patterns]
            )
        elif isinstance(pattern, HsListPattern):
            return ListPattern([self.convert_pattern(p) for p in pattern.patterns])
        elif isinstance(pattern, HsTuplePattern):
            return RunaTuplePattern([self.convert_pattern(p) for p in pattern.patterns])
        else:
            return WildcardPattern()
    
    def convert_type(self, type_expr: HsType) -> BasicType:
        """Convert type expression."""
        if isinstance(type_expr, HsTypeVariable):
            return BasicTypeVariable(type_expr.name)
        elif isinstance(type_expr, HsTypeConstructor):
            mapped_name = self.type_mappings.get(type_expr.name, type_expr.name)
            return BasicTypeConstructor(mapped_name)
        elif isinstance(type_expr, HsFunctionType):
            return FunctionType(
                parameter_types=[self.convert_type(type_expr.from_type)],
                return_type=self.convert_type(type_expr.to_type)
            )
        elif isinstance(type_expr, HsListType):
            return ListLiteralType(self.convert_type(type_expr.element_type))
        elif isinstance(type_expr, HsTupleType):
            return RunaTupleType([self.convert_type(t) for t in type_expr.types])
        elif isinstance(type_expr, HsTypeApplication):
            return RunaParametricType(
                base=self.convert_type(type_expr.constructor),
                parameters=[self.convert_type(arg) for arg in type_expr.arguments]
            )
        else:
            return BasicTypeConstructor("Any")


class RunaToHaskellConverter:
    """Converts Runa AST to Haskell AST."""
    
    def __init__(self):
        self.context = {}
        self.type_mappings = {
            'Integer': 'Int',
            'Float': 'Double',
            'String': 'String',
            'Boolean': 'Bool',
            'Character': 'Char',
            'Unit': '()'
        }
    
    def convert(self, node: RunaNode) -> HsNode:
        """Convert Runa AST node to Haskell AST."""
        method_name = f"convert_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.convert_generic)
        return method(node)
    
    def convert_generic(self, node: RunaNode) -> HsNode:
        """Generic conversion fallback."""
        raise NotImplementedError(f"Conversion for {type(node)} not implemented")
    
    def convert_runamodule(self, node: RunaModule) -> HsModule:
        """Convert Runa module."""
        imports = []
        declarations = []
        
        for stmt in node.statements:
            if isinstance(stmt, RunaImport):
                imports.append(self.convert_runaimport(stmt))
            else:
                declarations.append(self.convert(stmt))
        
        return HsModule(
            name=node.name,
            exports=None,
            imports=imports,
            declarations=declarations
        )
    
    def convert_runaimport(self, node: RunaImport) -> HsImport:
        """Convert import statement."""
        return HsImport(
            module_name=node.module,
            qualified=node.qualified,
            alias=node.alias
        )
    
    def convert_runafunction(self, node: RunaFunction) -> HsFunctionDeclaration:
        """Convert function."""
        patterns = []
        for param in node.parameters:
            patterns.append(HsVariablePattern(name=param.name))
        
        guard = HsGuard(
            condition=hs_lit_bool(True),
            expression=self.convert(node.body)
        )
        
        clause = HsClause(
            patterns=patterns,
            guards=[guard],
            expression=self.convert(node.body)
        )
        
        return HsFunctionDeclaration(name=node.name, clauses=[clause])
    
    def convert_runaclass(self, node: RunaClass) -> HsDataDeclaration:
        """Convert class to data declaration."""
        constructors = []
        
        for method in node.methods:
            fields = []
            for param in method.parameters:
                if param.type_annotation:
                    fields.append(self.convert_type(param.type_annotation))
                else:
                    fields.append(HsTypeVariable(name="a"))
            
            constructors.append(HsDataConstructor(
                name=method.name,
                fields=fields
            ))
        
        return HsDataDeclaration(
            name=node.name,
            parameters=[],
            constructors=constructors
        )
    
    def convert_runaliteral(self, node: StringLiteral) -> HsLiteral:
        """Convert literal."""
        if isinstance(node.value, int):
            literal_type = "integer"
        elif isinstance(node.value, float):
            literal_type = "float"
        elif isinstance(node.value, str):
            literal_type = "string"
        elif isinstance(node.value, bool):
            literal_type = "boolean"
        else:
            literal_type = "string"
        
        return HsLiteral(value=node.value, literal_type=literal_type)
    
    def convert_runavariable(self, node: RunaVariable) -> HsVariable:
        """Convert variable."""
        # Determine if it's a constructor (starts with uppercase)
        if node.name and node.name[0].isupper():
            return HsConstructor(name=node.name)
        return HsVariable(name=node.name)
    
    def convert_runacall(self, node: FunctionCall) -> HsApplication:
        """Convert function call."""
        return HsApplication(
            function=self.convert(node.function),
            arguments=[self.convert(arg) for arg in node.arguments]
        )
    
    def convert_runalambda(self, node: ProcessDefinition) -> HsLambda:
        """Convert lambda."""
        parameters = []
        for param in node.parameters:
            parameters.append(HsVariablePattern(name=param.name))
        
        return HsLambda(
            parameters=parameters,
            body=self.convert(node.body)
        )
    
    def convert_runaif(self, node: RunaIf) -> HsIf:
        """Convert if statement."""
        return HsIf(
            condition=self.convert(node.condition),
            then_expr=self.convert(node.then_branch),
            else_expr=self.convert(node.else_branch)
        )
    
    def convert_runamatch(self, node: RunaMatch) -> HsCase:
        """Convert match statement."""
        alternatives = []
        for case in node.cases:
            pattern = self.convert_pattern(case.pattern)
            guard = HsGuard(
                condition=hs_lit_bool(True),
                expression=self.convert(case.body)
            )
            alternatives.append(HsAlternative(
                pattern=pattern,
                guards=[guard],
                expression=self.convert(case.body)
            ))
        
        return HsCase(
            expression=self.convert(node.expression),
            alternatives=alternatives
        )
    
    def convert_runalist(self, node: ListLiteral) -> HsList:
        """Convert list."""
        return HsList([self.convert(elem) for elem in node.elements])
    
    def convert_runatuple(self, node: RunaTuple) -> HsTuple:
        """Convert tuple."""
        return HsTuple([self.convert(elem) for elem in node.elements])
    
    def convert_pattern(self, pattern: Pattern) -> HsPattern:
        """Convert pattern."""
        if isinstance(pattern, RunaVariablePattern):
            return HsVariablePattern(pattern.name)
        elif isinstance(pattern, WildcardPattern):
            return HsWildcardPattern()
        elif isinstance(pattern, StringLiteralPattern):
            literal = self.convert_runaliteral(StringLiteral(pattern.value))
            return HsLiteralPattern(literal=literal)
        elif isinstance(pattern, RunaConstructorPattern):
            return HsConstructorPattern(
                constructor=pattern.name,
                patterns=[self.convert_pattern(p) for p in pattern.patterns]
            )
        elif isinstance(pattern, ListPattern):
            return HsListPattern([self.convert_pattern(p) for p in pattern.patterns])
        elif isinstance(pattern, RunaTuplePattern):
            return HsTuplePattern([self.convert_pattern(p) for p in pattern.patterns])
        else:
            return HsWildcardPattern()
    
    def convert_type(self, type_expr: BasicType) -> HsType:
        """Convert type expression."""
        if isinstance(type_expr, BasicTypeVariable):
            return HsTypeVariable(type_expr.name)
        elif isinstance(type_expr, BasicTypeConstructor):
            mapped_name = self.type_mappings.get(type_expr.name, type_expr.name)
            return HsTypeConstructor(mapped_name)
        elif isinstance(type_expr, FunctionType):
            param_type = (type_expr.parameter_types[0] 
                         if type_expr.parameter_types 
                         else HsTypeVariable("a"))
            return HsFunctionType(
                from_type=self.convert_type(param_type),
                to_type=self.convert_type(type_expr.return_type)
            )
        elif isinstance(type_expr, ListLiteralType):
            return HsListType(self.convert_type(type_expr.element_type))
        elif isinstance(type_expr, RunaTupleType):
            return HsTupleType([self.convert_type(t) for t in type_expr.types])
        elif isinstance(type_expr, RunaParametricType):
            return HsTypeApplication(
                constructor=self.convert_type(type_expr.base),
                arguments=[self.convert_type(param) for param in type_expr.parameters]
            )
        else:
            return HsTypeConstructor("String")


# Conversion functions
def haskell_to_runa(haskell_ast: HsNode) -> RunaNode:
    """Convert Haskell AST to Runa AST."""
    converter = HaskellToRunaConverter()
    return converter.convert(haskell_ast)


def runa_to_haskell(runa_ast: RunaNode) -> HsNode:
    """Convert Runa AST to Haskell AST."""
    converter = RunaToHaskellConverter()
    return converter.convert(runa_ast)


# Export all components
__all__ = [
    "HaskellToRunaConverter",
    "RunaToHaskellConverter", 
    "haskell_to_runa",
    "runa_to_haskell"
] 