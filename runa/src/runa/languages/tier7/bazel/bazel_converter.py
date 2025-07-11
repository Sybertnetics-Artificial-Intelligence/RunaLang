#!/usr/bin/env python3
"""
Bazel ↔ Runa AST Converter

Bidirectional conversion between Bazel AST and Runa AST including:
- BUILD files with rules and targets
- WORKSPACE files with external dependencies
- .bzl files with custom rules and macros  
- Starlark language constructs
- Label handling and validation
- Rule attribute mapping
"""

from typing import List, Dict, Any, Optional, Union
from runa.core.ast import *
from .bazel_ast import *


class BazelToRunaConverter:
    """Converts Bazel AST to Runa AST."""
    
    def __init__(self):
        self.scope_stack = []
        self.current_module = None
        
    def convert(self, bazel_node: BazelNode) -> RunaNode:
        """Convert a Bazel AST node to Runa AST."""
        if isinstance(bazel_node, BuildFile):
            return self._convert_build_file(bazel_node)
        elif isinstance(bazel_node, WorkspaceFile):
            return self._convert_workspace_file(bazel_node)
        elif isinstance(bazel_node, BzlFile):
            return self._convert_bzl_file(bazel_node)
        elif isinstance(bazel_node, TargetDefinition):
            return self._convert_target_definition(bazel_node)
        elif isinstance(bazel_node, RuleDefinition):
            return self._convert_rule_definition(bazel_node)
        elif isinstance(bazel_node, LoadStatement):
            return self._convert_load_statement(bazel_node)
        elif isinstance(bazel_node, FunctionDef):
            return self._convert_function_def(bazel_node)
        elif isinstance(bazel_node, Assignment):
            return self._convert_assignment(bazel_node)
        elif isinstance(bazel_node, IfStatement):
            return self._convert_if_statement(bazel_node)
        elif isinstance(bazel_node, ForLoop):
            return self._convert_for_loop(bazel_node)
        elif isinstance(bazel_node, Label):
            return self._convert_label(bazel_node)
        elif isinstance(bazel_node, ListExpr):
            return self._convert_list_expr(bazel_node)
        elif isinstance(bazel_node, DictExpr):
            return self._convert_dict_expr(bazel_node)
        elif isinstance(bazel_node, CallExpr):
            return self._convert_call_expr(bazel_node)
        elif isinstance(bazel_node, Identifier):
            return self._convert_identifier(bazel_node)
        elif isinstance(bazel_node, Literal):
            return self._convert_literal(bazel_node)
        else:
            raise ValueError(f"Unsupported Bazel node type: {type(bazel_node)}")
    
    def _convert_build_file(self, node: BuildFile) -> Module:
        """Convert BUILD file to Runa Module."""
        statements = []
        
        # Add package declaration
        package_decl = VariableDeclaration(
            name="package_name",
            value=StringLiteral(node.package_name),
            is_constant=True
        )
        statements.append(package_decl)
        
        # Convert statements
        for stmt in node.statements:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        return Module(
            name=node.package_name,
            statements=statements,
            imports=[],
            exports=[]
        )
    
    def _convert_workspace_file(self, node: WorkspaceFile) -> Module:
        """Convert WORKSPACE file to Runa Module."""
        statements = []
        
        # Add workspace declaration
        workspace_decl = VariableDeclaration(
            name="workspace_name",
            value=StringLiteral(node.workspace_name),
            is_constant=True
        )
        statements.append(workspace_decl)
        
        # Convert statements
        for stmt in node.statements:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        return Module(
            name=node.workspace_name,
            statements=statements,
            imports=[],
            exports=[]
        )
    
    def _convert_bzl_file(self, node: BzlFile) -> Module:
        """Convert .bzl file to Runa Module."""
        imports = []
        statements = []
        
        # Convert load statements to imports
        for load_stmt in node.load_statements:
            import_stmt = ImportStatement(
                module_path=load_stmt.file_path,
                symbols=load_stmt.symbols,
                alias=None
            )
            imports.append(import_stmt)
        
        # Convert other statements
        for stmt in node.statements:
            if not isinstance(stmt, LoadStatement):
                runa_stmt = self.convert(stmt)
                if runa_stmt:
                    statements.append(runa_stmt)
        
        return Module(
            name=node.file_name,
            statements=statements,
            imports=imports,
            exports=[]
        )
    
    def _convert_target_definition(self, node: TargetDefinition) -> FunctionCall:
        """Convert target definition to Runa function call."""
        arguments = []
        
        # Add target name as first argument
        arguments.append(Argument(
            name="name",
            value=StringLiteral(node.target_name),
            is_keyword=True
        ))
        
        # Convert attributes
        for attr_name, attr_value in node.attributes.items():
            if attr_name != "name":  # Skip name, already added
                runa_value = self.convert(attr_value)
                arguments.append(Argument(
                    name=attr_name,
                    value=runa_value,
                    is_keyword=True
                ))
        
        # Add visibility if present
        if node.visibility:
            visibility_list = ListLiteral([
                StringLiteral(vis) for vis in node.visibility
            ])
            arguments.append(Argument(
                name="visibility",
                value=visibility_list,
                is_keyword=True
            ))
        
        # Add tags if present
        if node.tags:
            tags_list = ListLiteral([
                StringLiteral(tag) for tag in node.tags
            ])
            arguments.append(Argument(
                name="tags",
                value=tags_list,
                is_keyword=True
            ))
        
        return FunctionCall(
            function=Identifier(node.rule_name),
            arguments=arguments
        )
    
    def _convert_rule_definition(self, node: RuleDefinition) -> FunctionDefinition:
        """Convert rule definition to Runa function."""
        parameters = []
        
        # Add implementation parameter
        parameters.append(Parameter(
            name="implementation",
            parameter_type=None,
            default_value=StringLiteral(node.implementation)
        ))
        
        # Convert attributes to parameters
        for attr_name, attr_def in node.attributes.items():
            param_type = self._map_bazel_type_to_runa(attr_def.attr_type)
            default_val = self._convert_attribute_default(attr_def.default) if attr_def.default else None
            
            parameters.append(Parameter(
                name=attr_name,
                parameter_type=param_type,
                default_value=default_val
            ))
        
        # Create function body (simplified for this implementation)
        body = Block([
            ReturnStatement(
                value=DictLiteral([
                    (StringLiteral("rule"), StringLiteral(node.name)),
                    (StringLiteral("implementation"), StringLiteral(node.implementation))
                ])
            )
        ])
        
        return FunctionDefinition(
            name=node.name,
            parameters=parameters,
            return_type=None,
            body=body,
            decorators=[]
        )
    
    def _convert_load_statement(self, node: LoadStatement) -> ImportStatement:
        """Convert load statement to Runa import."""
        return ImportStatement(
            module_path=node.file_path,
            symbols=node.symbols,
            alias=None
        )
    
    def _convert_function_def(self, node: FunctionDef) -> FunctionDefinition:
        """Convert function definition to Runa function."""
        parameters = []
        
        # Convert parameters
        for param_name in node.parameters:
            default_val = node.defaults.get(param_name)
            runa_default = self.convert(default_val) if default_val else None
            
            parameters.append(Parameter(
                name=param_name,
                parameter_type=None,
                default_value=runa_default
            ))
        
        # Convert body
        body_statements = []
        for stmt in node.body:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        body = Block(body_statements)
        
        return FunctionDefinition(
            name=node.name,
            parameters=parameters,
            return_type=None,
            body=body,
            decorators=[]
        )
    
    def _convert_assignment(self, node: Assignment) -> VariableDeclaration:
        """Convert assignment to Runa variable declaration."""
        runa_value = self.convert(node.value)
        
        return VariableDeclaration(
            name=node.target,
            value=runa_value,
            is_constant=False,
            variable_type=None
        )
    
    def _convert_if_statement(self, node: IfStatement) -> IfStatement:
        """Convert if statement to Runa if statement."""
        condition = self.convert(node.condition)
        
        then_block = Block([
            self.convert(stmt) for stmt in node.then_body if self.convert(stmt)
        ])
        
        else_block = None
        if node.else_body:
            else_block = Block([
                self.convert(stmt) for stmt in node.else_body if self.convert(stmt)
            ])
        
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def _convert_for_loop(self, node: ForLoop) -> ForLoop:
        """Convert for loop to Runa for loop."""
        iterable = self.convert(node.iterable)
        
        body_statements = []
        for stmt in node.body:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                body_statements.append(runa_stmt)
        
        body = Block(body_statements)
        
        return ForLoop(
            variable=Identifier(node.variable),
            iterable=iterable,
            body=body
        )
    
    def _convert_label(self, node: Label) -> StringLiteral:
        """Convert Bazel label to Runa string literal."""
        return StringLiteral(str(node))
    
    def _convert_list_expr(self, node: ListExpr) -> ListLiteral:
        """Convert list expression to Runa list literal."""
        elements = []
        for element in node.elements:
            runa_element = self.convert(element)
            elements.append(runa_element)
        
        return ListLiteral(elements)
    
    def _convert_dict_expr(self, node: DictExpr) -> DictLiteral:
        """Convert dict expression to Runa dict literal."""
        pairs = []
        for key, value in node.pairs:
            runa_key = self.convert(key)
            runa_value = self.convert(value)
            pairs.append((runa_key, runa_value))
        
        return DictLiteral(pairs)
    
    def _convert_call_expr(self, node: CallExpr) -> FunctionCall:
        """Convert call expression to Runa function call."""
        function = self.convert(node.function)
        
        arguments = []
        
        # Convert positional arguments
        for arg in node.args:
            runa_arg = self.convert(arg)
            arguments.append(Argument(
                name=None,
                value=runa_arg,
                is_keyword=False
            ))
        
        # Convert keyword arguments
        for name, value in node.kwargs.items():
            runa_value = self.convert(value)
            arguments.append(Argument(
                name=name,
                value=runa_value,
                is_keyword=True
            ))
        
        return FunctionCall(
            function=function,
            arguments=arguments
        )
    
    def _convert_identifier(self, node: Identifier) -> Identifier:
        """Convert identifier to Runa identifier."""
        return Identifier(node.name)
    
    def _convert_literal(self, node: Literal) -> Union[StringLiteral, IntegerLiteral, FloatLiteral, BooleanLiteral]:
        """Convert literal to appropriate Runa literal."""
        if node.literal_type == "string":
            return StringLiteral(node.value)
        elif node.literal_type == "integer":
            return IntegerLiteral(node.value)
        elif node.literal_type == "float":
            return FloatLiteral(node.value)
        elif node.literal_type == "boolean":
            return BooleanLiteral(node.value)
        else:
            return StringLiteral(str(node.value))
    
    def _map_bazel_type_to_runa(self, bazel_type: str) -> Optional[str]:
        """Map Bazel attribute type to Runa type."""
        type_mapping = {
            "string": "String",
            "label": "String",
            "string_list": "List[String]",
            "label_list": "List[String]", 
            "int": "Integer",
            "bool": "Boolean",
            "string_dict": "Dict[String, String]",
        }
        return type_mapping.get(bazel_type, "Any")
    
    def _convert_attribute_default(self, default_value: Any) -> Optional[RunaNode]:
        """Convert attribute default value to Runa node."""
        if isinstance(default_value, str):
            return StringLiteral(default_value)
        elif isinstance(default_value, int):
            return IntegerLiteral(default_value)
        elif isinstance(default_value, bool):
            return BooleanLiteral(default_value)
        elif isinstance(default_value, list):
            return ListLiteral([self._convert_attribute_default(item) for item in default_value])
        elif isinstance(default_value, dict):
            pairs = [(StringLiteral(k), self._convert_attribute_default(v)) for k, v in default_value.items()]
            return DictLiteral(pairs)
        else:
            return None


class RunaToBazelConverter:
    """Converts Runa AST to Bazel AST."""
    
    def __init__(self):
        self.target_file_type = "BUILD"  # BUILD, WORKSPACE, or BZL
        
    def convert(self, runa_node: RunaNode, file_type: str = "BUILD") -> BazelNode:
        """Convert a Runa AST node to Bazel AST."""
        self.target_file_type = file_type
        
        if isinstance(runa_node, Module):
            return self._convert_module(runa_node)
        elif isinstance(runa_node, FunctionCall):
            return self._convert_function_call(runa_node)
        elif isinstance(runa_node, FunctionDefinition):
            return self._convert_function_definition(runa_node)
        elif isinstance(runa_node, ImportStatement):
            return self._convert_import_statement(runa_node)
        elif isinstance(runa_node, VariableDeclaration):
            return self._convert_variable_declaration(runa_node)
        elif isinstance(runa_node, IfStatement):
            return self._convert_if_statement(runa_node)
        elif isinstance(runa_node, ForLoop):
            return self._convert_for_loop(runa_node)
        elif isinstance(runa_node, ListLiteral):
            return self._convert_list_literal(runa_node)
        elif isinstance(runa_node, DictLiteral):
            return self._convert_dict_literal(runa_node)
        elif isinstance(runa_node, StringLiteral):
            return self._convert_string_literal(runa_node)
        elif isinstance(runa_node, IntegerLiteral):
            return self._convert_integer_literal(runa_node)
        elif isinstance(runa_node, FloatLiteral):
            return self._convert_float_literal(runa_node)
        elif isinstance(runa_node, BooleanLiteral):
            return self._convert_boolean_literal(runa_node)
        elif isinstance(runa_node, Identifier):
            return self._convert_identifier(runa_node)
        else:
            raise ValueError(f"Unsupported Runa node type: {type(runa_node)}")
    
    def _convert_module(self, node: Module) -> Union[BuildFile, WorkspaceFile, BzlFile]:
        """Convert Runa Module to appropriate Bazel file type."""
        statements = []
        
        # Convert statements
        for stmt in node.statements:
            bazel_stmt = self.convert(stmt)
            if bazel_stmt:
                statements.append(bazel_stmt)
        
        if self.target_file_type == "WORKSPACE":
            return WorkspaceFile(
                workspace_name=node.name,
                statements=statements
            )
        elif self.target_file_type == "BZL":
            load_statements = [stmt for stmt in statements if isinstance(stmt, LoadStatement)]
            return BzlFile(
                file_name=node.name,
                statements=statements,
                load_statements=load_statements
            )
        else:  # BUILD file
            return BuildFile(
                package_name=node.name,
                statements=statements
            )
    
    def _convert_function_call(self, node: FunctionCall) -> TargetDefinition:
        """Convert function call to Bazel target definition."""
        rule_name = node.function.name if isinstance(node.function, Identifier) else str(node.function)
        
        attributes = {}
        target_name = "unknown"
        visibility = None
        tags = None
        
        # Process arguments
        for arg in node.arguments:
            if arg.is_keyword:
                if arg.name == "name":
                    target_name = arg.value.value if hasattr(arg.value, 'value') else str(arg.value)
                elif arg.name == "visibility":
                    if isinstance(arg.value, ListLiteral):
                        visibility = [elem.value for elem in arg.value.elements if hasattr(elem, 'value')]
                elif arg.name == "tags":
                    if isinstance(arg.value, ListLiteral):
                        tags = [elem.value for elem in arg.value.elements if hasattr(elem, 'value')]
                else:
                    bazel_value = self.convert(arg.value)
                    attributes[arg.name] = bazel_value
        
        return TargetDefinition(
            rule_name=rule_name,
            target_name=target_name,
            attributes=attributes,
            visibility=visibility,
            tags=tags
        )
    
    def _convert_function_definition(self, node: FunctionDefinition) -> Union[FunctionDef, RuleDefinition]:
        """Convert function definition to Bazel function or rule definition."""
        # Check if this looks like a rule definition
        is_rule = any(param.name == "implementation" for param in node.parameters)
        
        if is_rule:
            # Convert to rule definition
            implementation = ""
            attributes = {}
            
            for param in node.parameters:
                if param.name == "implementation":
                    if isinstance(param.default_value, StringLiteral):
                        implementation = param.default_value.value
                else:
                    attr_type = self._map_runa_type_to_bazel(param.parameter_type)
                    default_val = self._extract_default_value(param.default_value)
                    
                    attributes[param.name] = AttributeDefinition(
                        name=param.name,
                        attr_type=attr_type,
                        mandatory=param.default_value is None,
                        default=default_val
                    )
            
            return RuleDefinition(
                name=node.name,
                implementation=implementation,
                attributes=attributes
            )
        else:
            # Convert to regular function definition
            parameters = [param.name for param in node.parameters]
            defaults = {}
            
            for param in node.parameters:
                if param.default_value:
                    bazel_default = self.convert(param.default_value)
                    defaults[param.name] = bazel_default
            
            body_statements = []
            for stmt in node.body.statements:
                bazel_stmt = self.convert(stmt)
                if bazel_stmt:
                    body_statements.append(bazel_stmt)
            
            return FunctionDef(
                name=node.name,
                parameters=parameters,
                defaults=defaults,
                body=body_statements
            )
    
    def _convert_import_statement(self, node: ImportStatement) -> LoadStatement:
        """Convert import statement to Bazel load statement."""
        return LoadStatement(
            file_path=node.module_path,
            symbols=node.symbols or [],
            symbol_aliases={}
        )
    
    def _convert_variable_declaration(self, node: VariableDeclaration) -> Assignment:
        """Convert variable declaration to Bazel assignment."""
        bazel_value = self.convert(node.value)
        
        return Assignment(
            target=node.name,
            value=bazel_value,
            operator="="
        )
    
    def _convert_if_statement(self, node: IfStatement) -> IfStatement:
        """Convert if statement to Bazel if statement."""
        condition = self.convert(node.condition)
        
        then_body = []
        for stmt in node.then_block.statements:
            bazel_stmt = self.convert(stmt)
            if bazel_stmt:
                then_body.append(bazel_stmt)
        
        else_body = None
        if node.else_block:
            else_body = []
            for stmt in node.else_block.statements:
                bazel_stmt = self.convert(stmt)
                if bazel_stmt:
                    else_body.append(bazel_stmt)
        
        return IfStatement(
            condition=condition,
            then_body=then_body,
            else_body=else_body
        )
    
    def _convert_for_loop(self, node: ForLoop) -> ForLoop:
        """Convert for loop to Bazel for loop."""
        variable = node.variable.name if isinstance(node.variable, Identifier) else str(node.variable)
        iterable = self.convert(node.iterable)
        
        body = []
        for stmt in node.body.statements:
            bazel_stmt = self.convert(stmt)
            if bazel_stmt:
                body.append(bazel_stmt)
        
        return ForLoop(
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def _convert_list_literal(self, node: ListLiteral) -> ListExpr:
        """Convert list literal to Bazel list expression."""
        elements = []
        for element in node.elements:
            bazel_element = self.convert(element)
            elements.append(bazel_element)
        
        return ListExpr(elements=elements)
    
    def _convert_dict_literal(self, node: DictLiteral) -> DictExpr:
        """Convert dict literal to Bazel dict expression."""
        pairs = []
        for key, value in node.pairs:
            bazel_key = self.convert(key)
            bazel_value = self.convert(value)
            pairs.append((bazel_key, bazel_value))
        
        return DictExpr(pairs=pairs)
    
    def _convert_string_literal(self, node: StringLiteral) -> Literal:
        """Convert string literal to Bazel literal."""
        return Literal(node.value, "string")
    
    def _convert_integer_literal(self, node: IntegerLiteral) -> Literal:
        """Convert integer literal to Bazel literal."""
        return Literal(node.value, "integer")
    
    def _convert_float_literal(self, node: FloatLiteral) -> Literal:
        """Convert float literal to Bazel literal."""
        return Literal(node.value, "float")
    
    def _convert_boolean_literal(self, node: BooleanLiteral) -> Literal:
        """Convert boolean literal to Bazel literal."""
        return Literal(node.value, "boolean")
    
    def _convert_identifier(self, node: Identifier) -> Identifier:
        """Convert identifier to Bazel identifier."""
        return Identifier(node.name)
    
    def _map_runa_type_to_bazel(self, runa_type: Optional[str]) -> str:
        """Map Runa type to Bazel attribute type."""
        if not runa_type:
            return "string"
        
        type_mapping = {
            "String": "string",
            "Integer": "int",
            "Boolean": "bool",
            "List[String]": "string_list",
            "Dict[String, String]": "string_dict",
        }
        return type_mapping.get(runa_type, "string")
    
    def _extract_default_value(self, runa_node: Optional[RunaNode]) -> Any:
        """Extract default value from Runa node."""
        if runa_node is None:
            return None
        elif isinstance(runa_node, StringLiteral):
            return runa_node.value
        elif isinstance(runa_node, IntegerLiteral):
            return runa_node.value
        elif isinstance(runa_node, BooleanLiteral):
            return runa_node.value
        elif isinstance(runa_node, ListLiteral):
            return [self._extract_default_value(elem) for elem in runa_node.elements]
        elif isinstance(runa_node, DictLiteral):
            return {k.value: self._extract_default_value(v) for k, v in runa_node.pairs if hasattr(k, 'value')}
        else:
            return None


# Public API functions
def bazel_to_runa(bazel_node: BazelNode) -> RunaNode:
    """Convert Bazel AST to Runa AST."""
    converter = BazelToRunaConverter()
    return converter.convert(bazel_node)


def runa_to_bazel(runa_node: RunaNode, file_type: str = "BUILD") -> BazelNode:
    """Convert Runa AST to Bazel AST."""
    converter = RunaToBazelConverter()
    return converter.convert(runa_node, file_type)


# Export converter classes and functions
__all__ = [
    'BazelToRunaConverter',
    'RunaToBazelConverter', 
    'bazel_to_runa',
    'runa_to_bazel'
] 