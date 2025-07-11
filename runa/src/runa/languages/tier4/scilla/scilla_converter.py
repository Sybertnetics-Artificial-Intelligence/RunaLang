"""
Scilla ↔ Runa AST Converter

This module provides bidirectional conversion between Scilla and Runa ASTs.
Handles smart contract constructs, functional programming patterns, and
type system mapping between the two languages.

Key Features:
- Smart contract structure mapping
- Functional programming construct conversion
- Type system compatibility
- Pattern matching translation
- Message passing and event handling
"""

from typing import List, Optional, Union, Dict, Any
from dataclasses import dataclass

from runa.core.base_components import Node, NodeType
from .scilla_ast import *


class ScillaToRunaConverter:
    """Converts Scilla AST to Runa AST"""
    
    def __init__(self):
        self.imports = []
        self.current_scope = []
        
    def convert(self, scilla_node: ScillaProgram) -> Node:
        """Convert Scilla program to Runa AST"""
        return self._convert_program(scilla_node)
    
    def _convert_program(self, node: ScillaProgram) -> Node:
        """Convert Scilla program"""
        statements = []
        
        # Add version comment
        statements.append(Node(
            node_type=NodeType.COMMENT,
            value=f"Scilla version {node.scilla_version}",
            metadata={"original_scilla_version": node.scilla_version}
        ))
        
        # Convert imports
        for imp in node.contract.imports:
            statements.append(self._convert_import(imp))
        
        # Convert library if present
        if node.contract.library:
            statements.append(self._convert_library(node.contract.library))
        
        # Convert contract
        statements.append(self._convert_contract(node.contract))
        
        return Node(
            node_type=NodeType.PROGRAM,
            children=statements,
            metadata={"language": "scilla"}
        )
    
    def _convert_import(self, node: ScillaImport) -> Node:
        """Convert import statement"""
        return Node(
            node_type=NodeType.IMPORT,
            value=node.module,
            metadata={"items": node.items}
        )
    
    def _convert_library(self, node: ScillaLibrary) -> Node:
        """Convert library declaration"""
        statements = []
        
        # Convert type declarations
        for type_decl in node.type_declarations:
            statements.append(self._convert_adt_declaration(type_decl))
        
        # Convert function declarations
        for func_decl in node.function_declarations:
            statements.append(self._convert_library_function(func_decl))
        
        return Node(
            node_type=NodeType.CLASS_DEFINITION,
            value=node.name,
            children=statements,
            metadata={"is_library": True}
        )
    
    def _convert_contract(self, node: ScillaContract) -> Node:
        """Convert contract declaration"""
        members = []
        
        # Convert immutable parameters as constructor parameters
        if node.immutable_params:
            constructor_params = []
            for param in node.immutable_params:
                constructor_params.append(Node(
                    node_type=NodeType.PARAMETER,
                    value=param.name,
                    metadata={
                        "type": self._convert_type_to_string(param.type),
                        "immutable": True
                    }
                ))
            
            constructor = Node(
                node_type=NodeType.FUNCTION_DEFINITION,
                value="__init__",
                children=constructor_params,
                metadata={"is_constructor": True}
            )
            members.append(constructor)
        
        # Convert fields
        for field in node.fields:
            members.append(self._convert_field(field))
        
        # Convert transitions
        for transition in node.transitions:
            members.append(self._convert_transition(transition))
        
        # Convert procedures
        for procedure in node.procedures:
            members.append(self._convert_procedure(procedure))
        
        return Node(
            node_type=NodeType.CLASS_DEFINITION,
            value=node.name,
            children=members,
            metadata={
                "is_contract": True,
                "type_params": [tp.name for tp in node.type_params]
            }
        )
    
    def _convert_field(self, node: ScillaFieldDeclaration) -> Node:
        """Convert contract field"""
        field_node = Node(
            node_type=NodeType.VARIABLE_DECLARATION,
            value=node.name,
            metadata={
                "type": self._convert_type_to_string(node.type),
                "mutability": node.mutability.value,
                "is_field": True
            }
        )
        
        if node.init_value:
            field_node.children = [self._convert_expression(node.init_value)]
        
        return field_node
    
    def _convert_transition(self, node: ScillaTransition) -> Node:
        """Convert contract transition"""
        params = []
        for param in node.params:
            params.append(Node(
                node_type=NodeType.PARAMETER,
                value=param.name,
                metadata={"type": self._convert_type_to_string(param.type)}
            ))
        
        body = []
        for stmt in node.statements:
            body.append(self._convert_statement(stmt))
        
        return Node(
            node_type=NodeType.FUNCTION_DEFINITION,
            value=node.name,
            children=params + body,
            metadata={
                "is_transition": True,
                "visibility": "public",
                "transition_type": node.transition_type.value
            }
        )
    
    def _convert_procedure(self, node: ScillaProcedure) -> Node:
        """Convert contract procedure"""
        params = []
        for param in node.params:
            params.append(Node(
                node_type=NodeType.PARAMETER,
                value=param.name,
                metadata={"type": self._convert_type_to_string(param.type)}
            ))
        
        body = []
        for stmt in node.statements:
            body.append(self._convert_statement(stmt))
        
        return Node(
            node_type=NodeType.FUNCTION_DEFINITION,
            value=node.name,
            children=params + body,
            metadata={
                "is_procedure": True,
                "visibility": "private"
            }
        )
    
    def _convert_adt_declaration(self, node: ScillaADTDeclaration) -> Node:
        """Convert algebraic data type"""
        constructors = []
        for constructor in node.constructors:
            constructors.append(Node(
                node_type=NodeType.FUNCTION_DEFINITION,
                value=constructor.name,
                metadata={
                    "is_constructor": True,
                    "arg_types": [self._convert_type_to_string(t) for t in constructor.arg_types]
                }
            ))
        
        return Node(
            node_type=NodeType.CLASS_DEFINITION,
            value=node.name,
            children=constructors,
            metadata={
                "is_adt": True,
                "type_params": [tp.name for tp in node.type_params]
            }
        )
    
    def _convert_library_function(self, node: ScillaLibraryFunction) -> Node:
        """Convert library function"""
        params = []
        for param in node.params:
            params.append(Node(
                node_type=NodeType.PARAMETER,
                value=param.name,
                metadata={"type": self._convert_type_to_string(param.type)}
            ))
        
        body = [self._convert_expression(node.body)]
        
        return Node(
            node_type=NodeType.FUNCTION_DEFINITION,
            value=node.name,
            children=params + body,
            metadata={
                "return_type": self._convert_type_to_string(node.return_type),
                "type_params": [tp.name for tp in node.type_params],
                "is_library_function": True
            }
        )
    
    def _convert_statement(self, node: ScillaStatement) -> Node:
        """Convert Scilla statement to Runa"""
        if isinstance(node, ScillaLoad):
            return Node(
                node_type=NodeType.ASSIGNMENT,
                value=node.var,
                children=[Node(
                    node_type=NodeType.FIELD_ACCESS,
                    value=node.field
                )],
                metadata={"is_load": True}
            )
        
        elif isinstance(node, ScillaStore):
            return Node(
                node_type=NodeType.ASSIGNMENT,
                value=node.field,
                children=[self._convert_expression(node.value)],
                metadata={"is_store": True}
            )
        
        elif isinstance(node, ScillaBind):
            return Node(
                node_type=NodeType.VARIABLE_DECLARATION,
                value=node.var,
                children=[self._convert_expression(node.value)]
            )
        
        elif isinstance(node, ScillaMapUpdate):
            return Node(
                node_type=NodeType.ASSIGNMENT,
                children=[
                    Node(
                        node_type=NodeType.INDEX_ACCESS,
                        value=node.map_name,
                        children=[self._convert_expression(node.key)]
                    ),
                    self._convert_expression(node.value)
                ],
                metadata={"is_map_update": True}
            )
        
        elif isinstance(node, ScillaMapDelete):
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                value="delete",
                children=[
                    Node(
                        node_type=NodeType.INDEX_ACCESS,
                        value=node.map_name,
                        children=[self._convert_expression(node.key)]
                    )
                ]
            )
        
        elif isinstance(node, ScillaSend):
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                value="send",
                children=[self._convert_expression(node.messages)]
            )
        
        elif isinstance(node, ScillaEvent):
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                value="emit",
                children=[self._convert_expression(node.event)]
            )
        
        elif isinstance(node, ScillaThrow):
            return Node(
                node_type=NodeType.THROW_STATEMENT,
                children=[self._convert_expression(node.exception)]
            )
        
        elif isinstance(node, ScillaAccept):
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                value="accept",
                children=[]
            )
        
        elif isinstance(node, ScillaMatchStmt):
            return self._convert_match_statement(node)
        
        else:
            return Node(
                node_type=NodeType.EXPRESSION_STATEMENT,
                children=[self._convert_expression(node)]
            )
    
    def _convert_expression(self, node: ScillaExpression) -> Node:
        """Convert Scilla expression to Runa"""
        if isinstance(node, ScillaIdentifier):
            return Node(
                node_type=NodeType.IDENTIFIER,
                value=node.name
            )
        
        elif isinstance(node, ScillaLiteral):
            return self._convert_literal(node.literal)
        
        elif isinstance(node, ScillaApplication):
            args = [self._convert_expression(arg) for arg in node.args]
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                children=[self._convert_expression(node.function)] + args
            )
        
        elif isinstance(node, ScillaBuiltinCall):
            args = [self._convert_expression(arg) for arg in node.args]
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                value=node.builtin,
                children=args,
                metadata={
                    "is_builtin": True,
                    "type_args": [self._convert_type_to_string(t) for t in node.type_args]
                }
            )
        
        elif isinstance(node, ScillaLet):
            return self._convert_let_expression(node)
        
        elif isinstance(node, ScillaMatch):
            return self._convert_match_expression(node)
        
        elif isinstance(node, ScillaConstructor):
            args = [self._convert_expression(arg) for arg in node.args]
            return Node(
                node_type=NodeType.FUNCTION_CALL,
                value=node.name,
                children=args,
                metadata={"is_constructor": True}
            )
        
        elif isinstance(node, ScillaMapAccess):
            return Node(
                node_type=NodeType.INDEX_ACCESS,
                children=[
                    self._convert_expression(node.map_expr),
                    self._convert_expression(node.key)
                ]
            )
        
        elif isinstance(node, ScillaFieldAccess):
            return Node(
                node_type=NodeType.FIELD_ACCESS,
                value=node.field
            )
        
        elif isinstance(node, ScillaMessageConstruction):
            return self._convert_message_construction(node)
        
        elif isinstance(node, ScillaEventConstruction):
            return self._convert_event_construction(node)
        
        elif isinstance(node, ScillaLambda):
            return self._convert_lambda(node)
        
        elif isinstance(node, ScillaTFun):
            return self._convert_type_abstraction(node)
        
        elif isinstance(node, ScillaTApp):
            return self._convert_type_application(node)
        
        else:
            return Node(
                node_type=NodeType.LITERAL,
                value=str(node)
            )
    
    def _convert_literal(self, node) -> Node:
        """Convert literal values"""
        if isinstance(node, ScillaIntLiteral):
            return Node(
                node_type=NodeType.LITERAL,
                value=node.value,
                metadata={"type": "integer", "type_hint": node.type_hint}
            )
        
        elif isinstance(node, ScillaStringLiteral):
            return Node(
                node_type=NodeType.LITERAL,
                value=f'"{node.value}"',
                metadata={"type": "string"}
            )
        
        elif isinstance(node, ScillaBoolLiteral):
            return Node(
                node_type=NodeType.LITERAL,
                value=str(node.value).lower(),
                metadata={"type": "boolean"}
            )
        
        elif isinstance(node, ScillaByStrLiteral):
            return Node(
                node_type=NodeType.LITERAL,
                value=node.value,
                metadata={"type": "bystring", "width": node.width}
            )
        
        elif isinstance(node, ScillaAddressLiteral):
            return Node(
                node_type=NodeType.LITERAL,
                value=node.value,
                metadata={"type": "address"}
            )
        
        else:
            return Node(
                node_type=NodeType.LITERAL,
                value=str(node)
            )
    
    def _convert_let_expression(self, node: ScillaLet) -> Node:
        """Convert let expression"""
        bindings = []
        for pattern, expr in node.bindings:
            bindings.append(Node(
                node_type=NodeType.VARIABLE_DECLARATION,
                value=self._pattern_to_name(pattern),
                children=[self._convert_expression(expr)],
                metadata={"pattern": self._convert_pattern_to_metadata(pattern)}
            ))
        
        body = self._convert_expression(node.body)
        
        return Node(
            node_type=NodeType.BLOCK,
            children=bindings + [body],
            metadata={"is_let_expression": True}
        )
    
    def _convert_match_expression(self, node: ScillaMatch) -> Node:
        """Convert match expression"""
        cases = []
        for pattern, expr in node.branches:
            case_node = Node(
                node_type=NodeType.MATCH_CASE,
                children=[self._convert_expression(expr)],
                metadata={
                    "pattern": self._convert_pattern_to_metadata(pattern),
                    "pattern_name": self._pattern_to_name(pattern)
                }
            )
            cases.append(case_node)
        
        return Node(
            node_type=NodeType.MATCH_EXPRESSION,
            children=[self._convert_expression(node.expr)] + cases
        )
    
    def _convert_match_statement(self, node: ScillaMatchStmt) -> Node:
        """Convert match statement"""
        cases = []
        for pattern, statements in node.branches:
            case_body = [self._convert_statement(stmt) for stmt in statements]
            case_node = Node(
                node_type=NodeType.MATCH_CASE,
                children=case_body,
                metadata={
                    "pattern": self._convert_pattern_to_metadata(pattern),
                    "pattern_name": self._pattern_to_name(pattern)
                }
            )
            cases.append(case_node)
        
        return Node(
            node_type=NodeType.MATCH_STATEMENT,
            children=[self._convert_expression(node.expr)] + cases
        )
    
    def _convert_message_construction(self, node: ScillaMessageConstruction) -> Node:
        """Convert message construction"""
        fields = []
        for name, expr in node.fields.items():
            fields.append(Node(
                node_type=NodeType.ASSIGNMENT,
                value=name,
                children=[self._convert_expression(expr)]
            ))
        
        return Node(
            node_type=NodeType.OBJECT_LITERAL,
            children=fields,
            metadata={"is_message": True}
        )
    
    def _convert_event_construction(self, node: ScillaEventConstruction) -> Node:
        """Convert event construction"""
        params = []
        for name, expr in node.params.items():
            params.append(Node(
                node_type=NodeType.ASSIGNMENT,
                value=name,
                children=[self._convert_expression(expr)]
            ))
        
        return Node(
            node_type=NodeType.FUNCTION_CALL,
            value=node.name,
            children=params,
            metadata={"is_event": True}
        )
    
    def _convert_lambda(self, node: ScillaLambda) -> Node:
        """Convert lambda expression"""
        params = []
        for name, param_type in node.params:
            params.append(Node(
                node_type=NodeType.PARAMETER,
                value=name,
                metadata={"type": self._convert_type_to_string(param_type)}
            ))
        
        body = self._convert_expression(node.body)
        
        return Node(
            node_type=NodeType.LAMBDA_EXPRESSION,
            children=params + [body]
        )
    
    def _convert_type_abstraction(self, node: ScillaTFun) -> Node:
        """Convert type abstraction"""
        body = self._convert_expression(node.body)
        
        return Node(
            node_type=NodeType.LAMBDA_EXPRESSION,
            children=[body],
            metadata={
                "is_type_abstraction": True,
                "type_vars": node.type_vars
            }
        )
    
    def _convert_type_application(self, node: ScillaTApp) -> Node:
        """Convert type application"""
        return Node(
            node_type=NodeType.FUNCTION_CALL,
            children=[self._convert_expression(node.expr)],
            metadata={
                "is_type_application": True,
                "type_args": [self._convert_type_to_string(t) for t in node.type_args]
            }
        )
    
    def _convert_type_to_string(self, scilla_type: ScillaType) -> str:
        """Convert Scilla type to string representation"""
        if isinstance(scilla_type, ScillaPrimitive):
            return scilla_type.type.value
        elif isinstance(scilla_type, ScillaMapType):
            key_str = self._convert_type_to_string(scilla_type.key_type)
            val_str = self._convert_type_to_string(scilla_type.value_type)
            return f"Map<{key_str}, {val_str}>"
        elif isinstance(scilla_type, ScillaListType):
            elem_str = self._convert_type_to_string(scilla_type.element_type)
            return f"List<{elem_str}>"
        elif isinstance(scilla_type, ScillaOptionType):
            elem_str = self._convert_type_to_string(scilla_type.element_type)
            return f"Option<{elem_str}>"
        elif isinstance(scilla_type, ScillaPairType):
            first_str = self._convert_type_to_string(scilla_type.first_type)
            second_str = self._convert_type_to_string(scilla_type.second_type)
            return f"Pair<{first_str}, {second_str}>"
        elif isinstance(scilla_type, ScillaCustomType):
            if scilla_type.type_args:
                args_str = ", ".join(self._convert_type_to_string(t) for t in scilla_type.type_args)
                return f"{scilla_type.name}<{args_str}>"
            return scilla_type.name
        elif isinstance(scilla_type, ScillaFunctionType):
            args_str = " -> ".join(self._convert_type_to_string(t) for t in scilla_type.arg_types)
            ret_str = self._convert_type_to_string(scilla_type.return_type)
            return f"({args_str}) -> {ret_str}"
        else:
            return str(scilla_type)
    
    def _pattern_to_name(self, pattern: ScillaPattern) -> str:
        """Extract variable name from pattern"""
        if isinstance(pattern, ScillaVariablePattern):
            return pattern.name
        elif isinstance(pattern, ScillaConstructorPattern):
            return pattern.constructor
        elif isinstance(pattern, ScillaWildcardPattern):
            return "_"
        else:
            return "pattern_var"
    
    def _convert_pattern_to_metadata(self, pattern: ScillaPattern) -> Dict[str, Any]:
        """Convert pattern to metadata"""
        if isinstance(pattern, ScillaVariablePattern):
            return {"type": "variable", "name": pattern.name}
        elif isinstance(pattern, ScillaConstructorPattern):
            return {
                "type": "constructor",
                "name": pattern.constructor,
                "args": [self._convert_pattern_to_metadata(arg) for arg in pattern.args]
            }
        elif isinstance(pattern, ScillaWildcardPattern):
            return {"type": "wildcard"}
        elif isinstance(pattern, ScillaLiteralPattern):
            return {"type": "literal", "value": str(pattern.literal)}
        else:
            return {"type": "unknown"}


class RunaToScillaConverter:
    """Converts Runa AST to Scilla AST"""
    
    def __init__(self):
        self.current_contract = None
        self.field_counter = 0
        
    def convert(self, runa_node: Node) -> ScillaProgram:
        """Convert Runa AST to Scilla program"""
        return self._convert_program(runa_node)
    
    def _convert_program(self, node: Node) -> ScillaProgram:
        """Convert Runa program to Scilla"""
        contract = None
        libraries = []
        version = "0"
        
        for child in node.children:
            if child.metadata.get("is_contract"):
                contract = self._convert_contract(child)
            elif child.metadata.get("is_library"):
                library = self._convert_library(child)
                libraries.append(library)
            elif child.node_type == NodeType.COMMENT and "scilla_version" in child.metadata:
                version = child.metadata["original_scilla_version"]
        
        if not contract:
            # Create a default contract
            contract = ScillaContract(
                name="DefaultContract",
                library=None,
                imports=[],
                type_params=[],
                immutable_params=[],
                fields=[],
                transitions=[],
                procedures=[]
            )
        
        return ScillaProgram(
            scilla_version=version,
            libraries=libraries,
            contract=contract
        )
    
    def _convert_contract(self, node: Node) -> ScillaContract:
        """Convert class definition to Scilla contract"""
        fields = []
        transitions = []
        procedures = []
        immutable_params = []
        
        for child in node.children:
            if child.metadata.get("is_field"):
                fields.append(self._convert_field(child))
            elif child.metadata.get("is_transition"):
                transitions.append(self._convert_transition(child))
            elif child.metadata.get("is_procedure"):
                procedures.append(self._convert_procedure(child))
            elif child.metadata.get("is_constructor"):
                for param in child.children:
                    if param.node_type == NodeType.PARAMETER:
                        immutable_params.append(ScillaParameter(
                            name=param.value,
                            type=self._convert_string_to_type(param.metadata.get("type", "String"))
                        ))
        
        return ScillaContract(
            name=node.value,
            library=None,
            imports=[],
            type_params=[],
            immutable_params=immutable_params,
            fields=fields,
            transitions=transitions,
            procedures=procedures
        )
    
    def _convert_library(self, node: Node) -> ScillaLibrary:
        """Convert library"""
        type_declarations = []
        function_declarations = []
        
        for child in node.children:
            if child.metadata.get("is_adt"):
                type_declarations.append(self._convert_adt(child))
            elif child.metadata.get("is_library_function"):
                function_declarations.append(self._convert_library_function(child))
        
        return ScillaLibrary(
            name=node.value,
            imports=[],
            type_declarations=type_declarations,
            function_declarations=function_declarations
        )
    
    def _convert_field(self, node: Node) -> ScillaFieldDeclaration:
        """Convert field declaration"""
        init_value = None
        if node.children:
            init_value = self._convert_expression(node.children[0])
        
        mutability = ScillaFieldType.MUTABLE
        if node.metadata.get("mutability") == "immutable":
            mutability = ScillaFieldType.IMMUTABLE
        
        return ScillaFieldDeclaration(
            name=node.value,
            type=self._convert_string_to_type(node.metadata.get("type", "String")),
            mutability=mutability,
            init_value=init_value
        )
    
    def _convert_transition(self, node: Node) -> ScillaTransition:
        """Convert transition"""
        params = []
        statements = []
        
        for child in node.children:
            if child.node_type == NodeType.PARAMETER:
                params.append(ScillaParameter(
                    name=child.value,
                    type=self._convert_string_to_type(child.metadata.get("type", "String"))
                ))
            else:
                statements.append(self._convert_statement(child))
        
        return ScillaTransition(
            name=node.value,
            params=params,
            statements=statements
        )
    
    def _convert_procedure(self, node: Node) -> ScillaProcedure:
        """Convert procedure"""
        params = []
        statements = []
        
        for child in node.children:
            if child.node_type == NodeType.PARAMETER:
                params.append(ScillaParameter(
                    name=child.value,
                    type=self._convert_string_to_type(child.metadata.get("type", "String"))
                ))
            else:
                statements.append(self._convert_statement(child))
        
        return ScillaProcedure(
            name=node.value,
            params=params,
            statements=statements
        )
    
    def _convert_statement(self, node: Node) -> ScillaStatement:
        """Convert statement"""
        if node.node_type == NodeType.ASSIGNMENT:
            if node.metadata.get("is_load"):
                return ScillaLoad(var=node.value, field=node.children[0].value)
            elif node.metadata.get("is_store"):
                return ScillaStore(field=node.value, value=self._convert_expression(node.children[0]))
            else:
                return ScillaBind(var=node.value, value=self._convert_expression(node.children[0]))
        
        elif node.node_type == NodeType.FUNCTION_CALL:
            if node.value == "send":
                return ScillaSend(messages=self._convert_expression(node.children[0]))
            elif node.value == "emit":
                return ScillaEvent(event=self._convert_expression(node.children[0]))
            elif node.value == "accept":
                return ScillaAccept()
        
        elif node.node_type == NodeType.THROW_STATEMENT:
            return ScillaThrow(exception=self._convert_expression(node.children[0]))
        
        return ScillaBind(var=f"temp_{self.field_counter}", value=self._convert_expression(node))
    
    def _convert_expression(self, node: Node) -> ScillaExpression:
        """Convert expression"""
        if node.node_type == NodeType.IDENTIFIER:
            return ScillaIdentifier(name=node.value)
        
        elif node.node_type == NodeType.LITERAL:
            return self._convert_literal_to_scilla(node)
        
        elif node.node_type == NodeType.FUNCTION_CALL:
            if node.metadata.get("is_builtin"):
                args = [self._convert_expression(child) for child in node.children]
                return ScillaBuiltinCall(
                    builtin=node.value,
                    args=args,
                    type_args=[]
                )
            else:
                function = ScillaIdentifier(name=node.value)
                args = [self._convert_expression(child) for child in node.children]
                return ScillaApplication(function=function, args=args)
        
        else:
            return ScillaIdentifier(name="unknown")
    
    def _convert_literal_to_scilla(self, node: Node) -> ScillaLiteral:
        """Convert literal to Scilla"""
        if node.metadata.get("type") == "integer":
            return ScillaLiteral(literal=ScillaIntLiteral(value=node.value))
        elif node.metadata.get("type") == "string":
            # Remove quotes
            value = node.value.strip('"\'')
            return ScillaLiteral(literal=ScillaStringLiteral(value=value))
        elif node.metadata.get("type") == "boolean":
            return ScillaLiteral(literal=ScillaBoolLiteral(value=node.value.lower() == "true"))
        else:
            return ScillaLiteral(literal=ScillaStringLiteral(value=str(node.value)))
    
    def _convert_string_to_type(self, type_str: str) -> ScillaType:
        """Convert string type to Scilla type"""
        type_map = {
            "Uint32": ScillaPrimitive(type=ScillaPrimitiveType.UINT32),
            "Uint64": ScillaPrimitive(type=ScillaPrimitiveType.UINT64),
            "Uint128": ScillaPrimitive(type=ScillaPrimitiveType.UINT128),
            "Uint256": ScillaPrimitive(type=ScillaPrimitiveType.UINT256),
            "Int32": ScillaPrimitive(type=ScillaPrimitiveType.INT32),
            "Int64": ScillaPrimitive(type=ScillaPrimitiveType.INT64),
            "Int128": ScillaPrimitive(type=ScillaPrimitiveType.INT128),
            "Int256": ScillaPrimitive(type=ScillaPrimitiveType.INT256),
            "String": ScillaPrimitive(type=ScillaPrimitiveType.STRING),
            "ByStr": ScillaPrimitive(type=ScillaPrimitiveType.BYSTR),
            "BNum": ScillaPrimitive(type=ScillaPrimitiveType.BNUM),
            "Message": ScillaPrimitive(type=ScillaPrimitiveType.MESSAGE),
            "Event": ScillaPrimitive(type=ScillaPrimitiveType.EVENT),
            "Exception": ScillaPrimitive(type=ScillaPrimitiveType.EXCEPTION),
        }
        
        return type_map.get(type_str, ScillaPrimitive(type=ScillaPrimitiveType.STRING))
    
    def _convert_adt(self, node: Node) -> ScillaADTDeclaration:
        """Convert ADT declaration"""
        constructors = []
        for child in node.children:
            if child.metadata.get("is_constructor"):
                arg_types = []
                for arg_type_str in child.metadata.get("arg_types", []):
                    arg_types.append(self._convert_string_to_type(arg_type_str))
                
                constructors.append(ScillaADTConstructor(
                    name=child.value,
                    arg_types=arg_types
                ))
        
        return ScillaADTDeclaration(
            name=node.value,
            type_params=[],
            constructors=constructors
        )
    
    def _convert_library_function(self, node: Node) -> ScillaLibraryFunction:
        """Convert library function"""
        params = []
        body_nodes = []
        
        for child in node.children:
            if child.node_type == NodeType.PARAMETER:
                params.append(ScillaParameter(
                    name=child.value,
                    type=self._convert_string_to_type(child.metadata.get("type", "String"))
                ))
            else:
                body_nodes.append(child)
        
        # Use first expression as body
        body = self._convert_expression(body_nodes[0]) if body_nodes else ScillaIdentifier(name="unit")
        
        return ScillaLibraryFunction(
            name=node.value,
            type_params=[],
            params=params,
            return_type=self._convert_string_to_type(node.metadata.get("return_type", "String")),
            body=body
        ) 