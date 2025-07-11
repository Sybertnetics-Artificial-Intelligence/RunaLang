"""
Scrypto code generator for asset-oriented smart contracts.

This generator creates idiomatic Scrypto code from AST representation, supporting:
- Blueprint definitions and component instantiation
- Resource creation and management
- Bucket and Vault operations for asset handling
- Badge-based authentication
- SBOR encoding and Radix Engine API calls
- Proper Rust syntax with Scrypto extensions
"""

from typing import List, Dict, Any, Optional, Set
from .scrypto_ast import *


class ScryptoCodeGenerator:
    """
    Generates idiomatic Scrypto code from AST representation.
    
    Supports all asset-oriented programming features including blueprints,
    components, resources, buckets, vaults, and Radix Engine API calls.
    """
    
    def __init__(self):
        self.indent_level = 0
        self.indent_size = 4
        self.output_lines = []
        self.imports = set()
        self.features_used = set()
    
    def generate(self, ast: ScryptoAST) -> str:
        """Generate complete Scrypto code from AST"""
        self.output_lines = []
        self.imports = set()
        self.features_used = set()
        
        # Generate the program
        self.generate_program(ast.root)
        
        # Combine all output
        return '\n'.join(self.output_lines)
    
    def generate_program(self, program: ScryptoProgram):
        """Generate complete Scrypto program"""
        # Add default imports for Scrypto
        self.add_line("use scrypto::prelude::*;")
        self.add_line("")
        
        # Generate use statements
        for use_stmt in program.use_statements:
            self.generate_use_statement(use_stmt)
        
        if program.use_statements:
            self.add_line("")
        
        # Generate packages
        for package in program.packages:
            self.generate_package(package)
    
    def generate_package(self, package: ScryptoPackage):
        """Generate Scrypto package (as module if needed)"""
        if package.name != "default":
            self.add_line(f"mod {package.name} {{")
            self.indent()
        
        # Generate blueprints
        for i, blueprint in enumerate(package.blueprints):
            if i > 0:
                self.add_line("")
            self.generate_blueprint(blueprint)
        
        if package.name != "default":
            self.dedent()
            self.add_line("}")
    
    def generate_blueprint(self, blueprint: ScryptoBlueprint):
        """Generate blueprint definition"""
        # Add doc comment if present
        if blueprint.doc_comment:
            self.add_line(f"/// {blueprint.doc_comment}")
        
        # Generate state struct with ScryptoSbor derive
        self.add_line("#[derive(ScryptoSbor)]")
        self.generate_struct(blueprint.state_struct)
        
        self.add_line("")
        
        # Generate impl block
        self.add_line(f"impl {blueprint.name} {{")
        self.indent()
        
        # Generate instantiate functions
        for func in blueprint.instantiate_functions:
            self.generate_instantiate_function(func)
            self.add_line("")
        
        # Generate methods
        for method in blueprint.methods:
            self.generate_method(method)
            self.add_line("")
        
        self.dedent()
        self.add_line("}")
    
    def generate_struct(self, struct: ScryptoStruct):
        """Generate struct definition"""
        if struct.doc_comment:
            self.add_line(f"/// {struct.doc_comment}")
        
        # Add derives
        if struct.derives:
            derives = ", ".join(struct.derives)
            self.add_line(f"#[derive({derives})]")
        
        self.add_line(f"pub struct {struct.name} {{")
        self.indent()
        
        # Generate fields
        for field in struct.fields:
            self.generate_struct_field(field)
        
        self.dedent()
        self.add_line("}")
    
    def generate_struct_field(self, field: ScryptoStructField):
        """Generate struct field"""
        if field.doc_comment:
            self.add_line(f"/// {field.doc_comment}")
        
        type_str = self.generate_type(field.field_type)
        visibility = "pub " if field.visibility == "pub" else ""
        self.add_line(f"{visibility}{field.name}: {type_str},")
    
    def generate_instantiate_function(self, func: ScryptoFunction):
        """Generate instantiate function"""
        params = self.generate_parameter_list(func.parameters)
        return_type = self.generate_type(func.return_type) if func.return_type else "ComponentAddress"
        
        self.add_line(f"pub fn {func.name}({params}) -> {return_type} {{")
        self.indent()
        
        self.generate_block(func.body)
        
        self.dedent()
        self.add_line("}")
    
    def generate_method(self, method: ScryptoMethod):
        """Generate method definition"""
        # Determine self parameter
        self_param = ""
        if method.parameters and method.parameters[0].name in ["self", "&self", "&mut self"]:
            self_param = method.parameters[0].name
            remaining_params = method.parameters[1:]
        else:
            if method.is_mutable:
                self_param = "&mut self"
            else:
                self_param = "&self"
            remaining_params = method.parameters
        
        params = self.generate_parameter_list(remaining_params)
        if params:
            full_params = f"{self_param}, {params}"
        else:
            full_params = self_param
        
        return_type_str = ""
        if method.return_type:
            return_type_str = f" -> {self.generate_type(method.return_type)}"
        
        visibility = "pub " if method.visibility == "pub" else ""
        self.add_line(f"{visibility}fn {method.name}({full_params}){return_type_str} {{")
        self.indent()
        
        self.generate_block(method.body)
        
        self.dedent()
        self.add_line("}")
    
    def generate_parameter_list(self, parameters: List[ScryptoParameter]) -> str:
        """Generate parameter list"""
        param_strs = []
        for param in parameters:
            param_str = f"{param.name}: {self.generate_type(param.param_type)}"
            param_strs.append(param_str)
        return ", ".join(param_strs)
    
    def generate_type(self, scrypto_type: Optional[ScryptoType]) -> str:
        """Generate type annotation"""
        if not scrypto_type:
            return "()"
        
        base_type = scrypto_type.name
        
        # Handle generics
        if scrypto_type.generics:
            generic_strs = [self.generate_type(g) for g in scrypto_type.generics]
            base_type = f"{base_type}<{', '.join(generic_strs)}>"
        
        # Handle references
        if scrypto_type.is_reference:
            if scrypto_type.is_mutable:
                base_type = f"&mut {base_type}"
            else:
                base_type = f"&{base_type}"
        
        return base_type
    
    def generate_block(self, block: ScryptoBlock):
        """Generate block of statements"""
        for stmt in block.statements:
            self.generate_statement(stmt)
    
    def generate_statement(self, stmt: ScryptoStatement):
        """Generate statement"""
        if isinstance(stmt, ScryptoLetStatement):
            self.generate_let_statement(stmt)
        
        elif isinstance(stmt, ScryptoReturnStatement):
            self.generate_return_statement(stmt)
        
        elif isinstance(stmt, ScryptoExpressionStatement):
            expr_str = self.generate_expression(stmt.expression)
            self.add_line(f"{expr_str};")
    
    def generate_let_statement(self, stmt: ScryptoLetStatement):
        """Generate let statement"""
        mut_str = "mut " if stmt.is_mutable else ""
        type_str = f": {self.generate_type(stmt.type_annotation)}" if stmt.type_annotation else ""
        
        if stmt.value:
            value_str = self.generate_expression(stmt.value)
            self.add_line(f"let {mut_str}{stmt.name}{type_str} = {value_str};")
        else:
            self.add_line(f"let {mut_str}{stmt.name}{type_str};")
    
    def generate_return_statement(self, stmt: ScryptoReturnStatement):
        """Generate return statement"""
        if stmt.value:
            value_str = self.generate_expression(stmt.value)
            self.add_line(f"return {value_str};")
        else:
            self.add_line("return;")
    
    def generate_expression(self, expr: ScryptoExpression) -> str:
        """Generate expression"""
        if isinstance(expr, ScryptoLiteralExpression):
            return self.generate_literal(expr)
        
        elif isinstance(expr, ScryptoIdentifierExpression):
            return expr.name
        
        elif isinstance(expr, ScryptoMethodCallExpression):
            return self.generate_method_call(expr)
        
        elif isinstance(expr, ScryptoFunctionCallExpression):
            return self.generate_function_call(expr)
        
        elif isinstance(expr, ScryptoRadixEngineCallExpression):
            return self.generate_radix_engine_call(expr)
        
        elif isinstance(expr, ScryptoResourceManagerCall):
            return self.generate_resource_manager_call(expr)
        
        elif isinstance(expr, ScryptoBucketExpression):
            return self.generate_bucket_operation(expr)
        
        elif isinstance(expr, ScryptoVaultExpression):
            return self.generate_vault_operation(expr)
        
        elif isinstance(expr, ScryptoStructExpression):
            return self.generate_struct_instantiation(expr)
        
        elif isinstance(expr, ScryptoMacroCall):
            return self.generate_macro_call(expr)
        
        elif isinstance(expr, ScryptoFieldAccessExpression):
            receiver = self.generate_expression(expr.receiver)
            return f"{receiver}.{expr.field_name}"
        
        elif isinstance(expr, ScryptoTupleExpression):
            elements = [self.generate_expression(e) for e in expr.elements]
            return f"({', '.join(elements)})"
        
        elif isinstance(expr, ScryptoArrayExpression):
            elements = [self.generate_expression(e) for e in expr.elements]
            return f"vec![{', '.join(elements)}]"
        
        else:
            return "/* Unknown expression */"
    
    def generate_literal(self, literal: ScryptoLiteralExpression) -> str:
        """Generate literal expression"""
        if literal.literal_type == "string":
            return f'"{literal.value}"'
        elif literal.literal_type == "boolean":
            return "true" if literal.value else "false"
        elif literal.literal_type == "decimal":
            return f'dec!("{literal.value}")'
        else:
            return str(literal.value)
    
    def generate_method_call(self, call: ScryptoMethodCallExpression) -> str:
        """Generate method call"""
        receiver = self.generate_expression(call.receiver)
        args = [self.generate_expression(arg) for arg in call.arguments]
        args_str = ", ".join(args)
        return f"{receiver}.{call.method_name}({args_str})"
    
    def generate_function_call(self, call: ScryptoFunctionCallExpression) -> str:
        """Generate function call"""
        args = [self.generate_expression(arg) for arg in call.arguments]
        args_str = ", ".join(args)
        return f"{call.function_name}({args_str})"
    
    def generate_radix_engine_call(self, call: ScryptoRadixEngineCallExpression) -> str:
        """Generate Radix Engine API call"""
        args = [self.generate_expression(arg) for arg in call.arguments]
        args_str = ", ".join(args)
        
        # Map common Radix Engine calls
        if call.api_name == "ResourceManager":
            if call.method_name == "create_fungible_resource":
                self.features_used.add("resource_creation")
                return f"ResourceBuilder::new_fungible({args_str})"
            elif call.method_name == "create_non_fungible_resource":
                self.features_used.add("resource_creation")
                return f"ResourceBuilder::new_non_fungible({args_str})"
        
        elif call.api_name == "ComponentManager":
            if call.method_name == "instantiate_component":
                return f"component.instantiate({args_str})"
        
        # Default format
        return f"{call.api_name}::{call.method_name}({args_str})"
    
    def generate_resource_manager_call(self, call: ScryptoResourceManagerCall) -> str:
        """Generate resource manager call"""
        params = []
        for key, value in call.parameters.items():
            param_str = f"{key}: {self.generate_expression(value)}"
            params.append(param_str)
        
        params_str = ", ".join(params)
        
        if call.operation == "create_fungible_resource":
            return f"ResourceBuilder::new_fungible().{params_str}.create()"
        elif call.operation == "create_non_fungible_resource":
            return f"ResourceBuilder::new_non_fungible().{params_str}.create()"
        else:
            return f"ResourceManager::{call.operation}({params_str})"
    
    def generate_bucket_operation(self, expr: ScryptoBucketExpression) -> str:
        """Generate bucket operation"""
        bucket = self.generate_expression(expr.bucket)
        
        if expr.operation == "take":
            if expr.amount:
                amount = self.generate_expression(expr.amount)
                return f"{bucket}.take({amount})"
            else:
                return f"{bucket}.take_all()"
        
        elif expr.operation == "put":
            if expr.amount:
                amount = self.generate_expression(expr.amount)
                return f"{bucket}.put({amount})"
            else:
                return f"{bucket}.put_all()"
        
        elif expr.operation == "amount":
            return f"{bucket}.amount()"
        
        elif expr.operation == "resource_address":
            return f"{bucket}.resource_address()"
        
        else:
            return f"{bucket}.{expr.operation}()"
    
    def generate_vault_operation(self, expr: ScryptoVaultExpression) -> str:
        """Generate vault operation"""
        vault = self.generate_expression(expr.vault)
        
        if expr.operation == "take":
            if expr.amount:
                amount = self.generate_expression(expr.amount)
                return f"{vault}.take({amount})"
            else:
                return f"{vault}.take_all()"
        
        elif expr.operation == "put":
            if expr.amount:
                amount = self.generate_expression(expr.amount)
                return f"{vault}.put({amount})"
            else:
                return f"{vault}.put_all()"
        
        elif expr.operation == "amount":
            return f"{vault}.amount()"
        
        elif expr.operation == "resource_address":
            return f"{vault}.resource_address()"
        
        else:
            return f"{vault}.{expr.operation}()"
    
    def generate_struct_instantiation(self, expr: ScryptoStructExpression) -> str:
        """Generate struct instantiation"""
        fields = []
        for field_name, field_expr in expr.fields.items():
            field_value = self.generate_expression(field_expr)
            fields.append(f"{field_name}: {field_value}")
        
        fields_str = ", ".join(fields)
        return f"{expr.struct_name} {{ {fields_str} }}"
    
    def generate_macro_call(self, call: ScryptoMacroCall) -> str:
        """Generate macro call"""
        args_str = ", ".join(f'"{arg}"' for arg in call.arguments)
        return f"{call.macro_name}!({args_str})"
    
    def generate_use_statement(self, use_stmt: ScryptoUseStatement):
        """Generate use statement"""
        if use_stmt.is_glob:
            self.add_line(f"use {use_stmt.path}::*;")
        elif use_stmt.alias:
            self.add_line(f"use {use_stmt.path} as {use_stmt.alias};")
        else:
            self.add_line(f"use {use_stmt.path};")
    
    def add_line(self, line: str = ""):
        """Add line with proper indentation"""
        if line:
            indent = " " * (self.indent_level * self.indent_size)
            self.output_lines.append(f"{indent}{line}")
        else:
            self.output_lines.append("")
    
    def indent(self):
        """Increase indentation level"""
        self.indent_level += 1
    
    def dedent(self):
        """Decrease indentation level"""
        self.indent_level = max(0, self.indent_level - 1)


def generate_scrypto_code(ast: ScryptoAST) -> str:
    """
    Generate Scrypto code from AST.
    
    Args:
        ast: ScryptoAST to generate code from
        
    Returns:
        str: Generated Scrypto source code
    """
    generator = ScryptoCodeGenerator()
    return generator.generate(ast)


def generate_blueprint_template(
    name: str,
    fields: List[Dict[str, str]],
    methods: List[Dict[str, Any]]
) -> str:
    """
    Generate a blueprint template with specified structure.
    
    Args:
        name: Blueprint name
        fields: List of field definitions with 'name' and 'type'
        methods: List of method definitions
        
    Returns:
        str: Generated Scrypto blueprint code
    """
    # Create state struct
    struct_fields = []
    for field in fields:
        struct_field = ScryptoStructField(
            name=field['name'],
            field_type=ScryptoType(name=field['type']),
            visibility="pub"
        )
        struct_fields.append(struct_field)
    
    state_struct = ScryptoStruct(
        name=name,
        fields=struct_fields,
        derives=["ScryptoSbor"]
    )
    
    # Create methods
    blueprint_methods = []
    instantiate_functions = []
    
    for method_def in methods:
        method = ScryptoMethod(
            name=method_def['name'],
            parameters=[],
            return_type=None,
            body=ScryptoBlock(statements=[]),
            visibility="pub",
            is_mutable=method_def.get('is_mutable', False)
        )
        
        if method_def['name'] == 'instantiate':
            instantiate_functions.append(method)
        else:
            blueprint_methods.append(method)
    
    # Create blueprint
    blueprint = ScryptoBlueprint(
        name=name,
        state_struct=state_struct,
        methods=blueprint_methods,
        instantiate_functions=instantiate_functions
    )
    
    # Create program
    package = ScryptoPackage(
        name="default",
        version="1.0.0",
        blueprints=[blueprint]
    )
    
    program = ScryptoProgram(
        packages=[package],
        use_statements=[ScryptoUseStatement(path="scrypto::prelude", is_glob=True)]
    )
    
    ast = ScryptoAST(program)
    return generate_scrypto_code(ast)


# Example usage
if __name__ == "__main__":
    # Generate a simple gumball machine blueprint
    template = generate_blueprint_template(
        name="GumballMachine",
        fields=[
            {"name": "gumball_vault", "type": "Vault"},
            {"name": "collected_xrd", "type": "Vault"},
            {"name": "price", "type": "Decimal"}
        ],
        methods=[
            {"name": "instantiate", "is_mutable": False},
            {"name": "buy_gumball", "is_mutable": True}
        ]
    )
    
    print("Generated Scrypto Blueprint:")
    print("=" * 50)
    print(template) 