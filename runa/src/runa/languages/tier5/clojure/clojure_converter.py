#!/usr/bin/env python3
"""
Clojure ↔ Runa Converter
"""

from typing import List, Optional, Dict, Any, Union
from runa.core.runa_ast import *
from .clojure_ast import *


class ClojureToRunaConverter:
    """Converts Clojure AST to Runa AST."""
    
    def __init__(self):
        self.type_mappings = {
            'nil': 'Nil',
            'boolean': 'Boolean',
            'number': 'Number',
            'string': 'String',
            'keyword': 'Keyword',
            'symbol': 'Symbol'
        }
    
    def convert(self, node: ClojureNode) -> RunaNode:
        method_name = f"convert_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.convert_generic)
        return method(node)
    
    def convert_generic(self, node):
        raise NotImplementedError(f"Conversion for {type(node)} not implemented")
    
    def convert_clojuremodule(self, node: ClojureModule) -> RunaModule:
        statements = []
        imports = []
        
        # Handle namespace
        if node.namespace:
            imports.append(RunaImport(module=node.namespace.name.name, alias=None))
        
        # Convert forms to statements
        for form in node.forms:
            statements.append(self.convert(form))
        
        return RunaModule(
            name="Main", 
            statements=statements, 
            imports=imports, 
            exports=[]
        )
    
    def convert_clojureliteral(self, node: ClojureLiteral) -> StringLiteral:
        return StringLiteral(node.value)
    
    def convert_clojuresymbol(self, node: ClojureSymbol) -> RunaVariable:
        return RunaVariable(node.qualified_name)
    
    def convert_clojurelist(self, node: ClojureList) -> FunctionCall:
        if not node.elements:
            return ListLiteral([])
        
        # Function call: first element is function, rest are arguments
        function = self.convert(node.elements[0])
        arguments = [self.convert(elem) for elem in node.elements[1:]]
        return FunctionCall(function=function, arguments=arguments)
    
    def convert_clojurevector(self, node: ClojureVector) -> ListLiteral:
        elements = [self.convert(elem) for elem in node.elements]
        return ListLiteral(elements)
    
    def convert_clojuremap(self, node: ClojureMap) -> RunaDict:
        pairs = []
        for key, value in node.pairs:
            pairs.append((self.convert(key), self.convert(value)))
        return RunaDict(pairs)
    
    def convert_clojureset(self, node: ClojureSet) -> SetStatement:
        elements = [self.convert(elem) for elem in node.elements]
        return SetStatement(elements)
    
    def convert_clojuredef(self, node: ClojureDef) -> LetStatement:
        return LetStatement(
            name=node.symbol.name,
            value=self.convert(node.value),
            body=StringLiteral(None)  # Top-level def doesn't have body
        )
    
    def convert_clojuredefn(self, node: ClojureDefn) -> RunaFunction:
        # Take first arity for simplification
        if node.arities:
            arity = node.arities[0]
            parameters = [Parameter(param.name, None) for param in arity.params]
            
            # Convert body to block
            if len(arity.body) == 1:
                body = self.convert(arity.body[0])
            else:
                body = Block([self.convert(expr) for expr in arity.body])
            
            return RunaFunction(
                name=node.name.name,
                parameters=parameters,
                body=body,
                return_type=None
            )
        
        return RunaFunction(
            name=node.name.name,
            parameters=[],
            body=StringLiteral(None),
            return_type=None
        )
    
    def convert_clojurefn(self, node: ClojureFn) -> ProcessDefinition:
        # Take first arity for simplification
        if node.arities:
            arity = node.arities[0]
            parameters = [Parameter(param.name, None) for param in arity.params]
            
            # Convert body
            if len(arity.body) == 1:
                body = self.convert(arity.body[0])
            else:
                body = Block([self.convert(expr) for expr in arity.body])
            
            return ProcessDefinition(parameters=parameters, body=body)
        
        return ProcessDefinition(parameters=[], body=StringLiteral(None))
    
    def convert_clojurelet(self, node: ClojureLet) -> LetStatement:
        # Convert multiple bindings to nested lets
        if not node.bindings:
            if node.body:
                return self.convert(node.body[0])
            return StringLiteral(None)
        
        # Start with innermost let
        body = Block([self.convert(expr) for expr in node.body]) if len(node.body) > 1 else self.convert(node.body[0])
        
        # Build nested lets from right to left
        for symbol, value in reversed(node.bindings):
            body = LetStatement(
                name=symbol.name,
                value=self.convert(value),
                body=body
            )
        
        return body
    
    def convert_clojureif(self, node: ClojureIf) -> RunaIf:
        return RunaIf(
            condition=self.convert(node.test),
            then_branch=self.convert(node.then_expr),
            else_branch=self.convert(node.else_expr) if node.else_expr else StringLiteral(None)
        )
    
    def convert_clojurecond(self, node: ClojureCond) -> RunaMatch:
        # Convert cond to nested if expressions or match
        cases = []
        for test, expr in node.clauses:
            pattern = StringLiteralPattern(True)  # Simplified
            body = self.convert(expr)
            cases.append(RunaMatchCase(pattern=pattern, body=body))
        
        # Use first test as match expression (simplified)
        if node.clauses:
            match_expr = self.convert(node.clauses[0][0])
        else:
            match_expr = StringLiteral(True)
        
        return RunaMatch(expression=match_expr, cases=cases)
    
    def convert_clojuredo(self, node: ClojureDo) -> Block:
        statements = [self.convert(expr) for expr in node.expressions]
        return Block(statements)
    
    def convert_clojureloop(self, node: ClojureLoop) -> WhileLoop:
        # Convert to while loop with initialization
        init_statements = []
        for symbol, value in node.bindings:
            init_statements.append(LetStatement(
                name=symbol.name,
                value=self.convert(value),
                body=StringLiteral(None)
            ))
        
        body = Block([self.convert(expr) for expr in node.body])
        
        return WhileLoop(
            condition=StringLiteral(True),  # Infinite loop, controlled by recur
            body=body
        )
    
    def convert_clojurerecur(self, node: ClojureRecur) -> ContinueStatement:
        # Convert recur to continue statement
        return ContinueStatement()
    
    def convert_clojurequote(self, node: ClojureQuote) -> RunaQuote:
        return RunaQuote(self.convert(node.expression))
    
    def convert_clojurens(self, node: ClojureNs) -> RunaModule:
        return RunaModule(
            name=node.name.name,
            statements=[],
            imports=[],
            exports=[]
        )


class RunaToClojureConverter:
    """Converts Runa AST to Clojure AST."""
    
    def __init__(self):
        self.type_mappings = {
            'Nil': 'nil',
            'Boolean': 'boolean', 
            'Number': 'number',
            'String': 'string',
            'Keyword': 'keyword',
            'Symbol': 'symbol'
        }
    
    def convert(self, node: RunaNode) -> ClojureNode:
        method_name = f"convert_{node.__class__.__name__.lower()}"
        method = getattr(self, method_name, self.convert_generic)
        return method(node)
    
    def convert_generic(self, node):
        raise NotImplementedError(f"Conversion for {type(node)} not implemented")
    
    def convert_runamodule(self, node: RunaModule) -> ClojureModule:
        forms = []
        namespace = None
        
        # Create namespace if module has a name
        if node.name and node.name != "Main":
            namespace = ClojureNs(name=ClojureSymbol(node.name))
        
        # Convert statements to forms
        for stmt in node.statements:
            converted = self.convert(stmt)
            if isinstance(converted, ClojureForm):
                forms.append(converted)
        
        return ClojureModule(namespace=namespace, forms=forms)
    
    def convert_runaliteral(self, node: StringLiteral) -> ClojureLiteral:
        if node.value is None:
            return ClojureLiteral(None, "nil")
        elif isinstance(node.value, bool):
            return ClojureLiteral(node.value, "boolean")
        elif isinstance(node.value, (int, float)):
            return ClojureLiteral(node.value, "number")
        elif isinstance(node.value, str):
            return ClojureLiteral(node.value, "string")
        else:
            return ClojureLiteral(str(node.value), "string")
    
    def convert_runavariable(self, node: RunaVariable) -> ClojureSymbol:
        if '/' in node.name:
            namespace, name = node.name.split('/', 1)
            return ClojureSymbol(name, namespace)
        return ClojureSymbol(node.name)
    
    def convert_runacall(self, node: FunctionCall) -> ClojureList:
        elements = [self.convert(node.function)]
        elements.extend([self.convert(arg) for arg in node.arguments])
        return ClojureList(elements)
    
    def convert_runalist(self, node: ListLiteral) -> ClojureVector:
        elements = [self.convert(elem) for elem in node.elements]
        return ClojureVector(elements)
    
    def convert_runadict(self, node: RunaDict) -> ClojureMap:
        pairs = []
        for key, value in node.pairs:
            pairs.append((self.convert(key), self.convert(value)))
        return ClojureMap(pairs)
    
    def convert_runaset(self, node: SetStatement) -> ClojureSet:
        elements = [self.convert(elem) for elem in node.elements]
        return ClojureSet(elements)
    
    def convert_runalet(self, node: LetStatement) -> ClojureLet:
        symbol = ClojureSymbol(node.name)
        value = self.convert(node.value)
        body = [self.convert(node.body)]
        bindings = [(symbol, value)]
        
        return ClojureLet(bindings=bindings, body=body)
    
    def convert_runafunction(self, node: RunaFunction) -> ClojureDefn:
        name = ClojureSymbol(node.name)
        params = [ClojureSymbol(param.name) for param in node.parameters]
        body = [self.convert(node.body)]
        
        arity = ClojureFnArity(params=params, body=body)
        return ClojureDefn(name=name, arities=[arity])
    
    def convert_runalambda(self, node: ProcessDefinition) -> ClojureFn:
        params = [ClojureSymbol(param.name) for param in node.parameters]
        body = [self.convert(node.body)]
        
        arity = ClojureFnArity(params=params, body=body)
        return ClojureFn(arities=[arity])
    
    def convert_runaif(self, node: RunaIf) -> ClojureIf:
        test = self.convert(node.condition)
        then_expr = self.convert(node.then_branch)
        else_expr = self.convert(node.else_branch) if node.else_branch else None
        
        return ClojureIf(test=test, then_expr=then_expr, else_expr=else_expr)
    
    def convert_runamatch(self, node: RunaMatch) -> ClojureCond:
        # Convert match to cond
        clauses = []
        for case in node.cases:
            # Simplified: use literal true for test
            test = ClojureLiteral(True, "boolean")
            expr = self.convert(case.body)
            clauses.append((test, expr))
        
        return ClojureCond(clauses=clauses)
    
    def convert_runablock(self, node: Block) -> ClojureDo:
        expressions = [self.convert(stmt) for stmt in node.statements]
        return ClojureDo(expressions=expressions)
    
    def convert_runaloop(self, node: WhileLoop) -> ClojureLoop:
        # Convert to loop with empty bindings
        body = [self.convert(node.body)]
        return ClojureLoop(bindings=[], body=body)
    
    def convert_runacontinue(self, node: ContinueStatement) -> ClojureRecur:
        return ClojureRecur(args=[])
    
    def convert_runaquote(self, node: RunaQuote) -> ClojureQuote:
        return ClojureQuote(self.convert(node.expression))


# Convenience functions
def clojure_to_runa(clojure_ast: ClojureNode) -> RunaNode:
    """Convert Clojure AST to Runa AST."""
    converter = ClojureToRunaConverter()
    return converter.convert(clojure_ast)

def runa_to_clojure(runa_ast: RunaNode) -> ClojureNode:
    """Convert Runa AST to Clojure AST."""
    converter = RunaToClojureConverter()
    return converter.convert(runa_ast) 