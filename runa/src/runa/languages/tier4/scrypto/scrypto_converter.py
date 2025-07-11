"""
Bidirectional converter between Scrypto AST and Runa AST.

This converter handles the mapping between Scrypto's asset-oriented programming
constructs and Runa's universal representation, including:
- Blueprint/Component architecture
- Resource management (fungible/non-fungible tokens)
- Bucket and Vault operations
- Badge-based authentication
- SBOR encoding and Radix Engine API calls
"""

from typing import List, Dict, Any, Optional, Union
import json

from runa.core.ast.base_ast import RunaAST, RunaASTNode, RunaNodeType
from runa.core.ast.expressions import *
from runa.core.ast.statements import *
from runa.core.ast.declarations import *

from .scrypto_ast import *


class ScryptoToRunaConverter:
    """Converts Scrypto AST to Runa AST"""
    
    def __init__(self):
        self.context = {
            'current_blueprint': None,
            'current_component': None,
            'resource_definitions': {},
            'vault_mappings': {},
            'bucket_mappings': {}
        }
    
    def convert(self, scrypto_ast: ScryptoAST) -> RunaAST:
        """Convert Scrypto AST to Runa AST"""
        runa_nodes = []
        
        # Convert program structure
        for package in scrypto_ast.root.packages:
            package_node = self.convert_package(package)
            runa_nodes.append(package_node)
        
        return RunaAST(
            root=RunaModule(
                name="scrypto_program",
                body=runa_nodes,
                imports=[self.convert_use_statement(use_stmt) 
                         for use_stmt in scrypto_ast.root.use_statements]
            )
        )
    
    def convert_package(self, package: ScryptoPackage) -> RunaModule:
        """Convert Scrypto package to Runa module"""
        body = []
        
        for blueprint in package.blueprints:
            blueprint_node = self.convert_blueprint(blueprint)
            body.append(blueprint_node)
        
        return RunaModule(
            name=package.name,
            body=body,
            metadata={
                'package_type': 'scrypto',
                'version': package.version,
                'dependencies': package.dependencies
            }
        )
    
    def convert_blueprint(self, blueprint: ScryptoBlueprint) -> RunaClass:
        """Convert Scrypto blueprint to Runa class"""
        self.context['current_blueprint'] = blueprint.name
        
        # Convert state struct to class fields
        fields = []
        for field in blueprint.state_struct.fields:
            runa_field = RunaVariable(
                name=field.name,
                type_annotation=self.convert_type(field.field_type),
                value=None,
                is_constant=False,
                visibility=field.visibility
            )
            fields.append(runa_field)
        
        # Convert methods
        methods = []
        
        # Convert instantiate functions as constructors
        for func in blueprint.instantiate_functions:
            constructor = self.convert_instantiate_function(func)
            methods.append(constructor)
        
        # Convert regular methods
        for method in blueprint.methods:
            runa_method = self.convert_method(method)
            methods.append(runa_method)
        
        return RunaClass(
            name=blueprint.name,
            fields=fields,
            methods=methods,
            parent_classes=[],
            metadata={
                'blueprint_type': 'scrypto',
                'component_state': blueprint.state_struct.name,
                'traits': blueprint.traits,
                'doc_comment': blueprint.doc_comment
            }
        )
    
    def convert_instantiate_function(self, func: ScryptoFunction) -> RunaMethod:
        """Convert Scrypto instantiate function to Runa constructor"""
        parameters = [self.convert_parameter(param) for param in func.parameters]
        body = self.convert_block(func.body)
        
        return RunaMethod(
            name="__init__",
            parameters=parameters,
            return_type=self.convert_type(func.return_type) if func.return_type else None,
            body=body,
            is_static=True,
            visibility=func.visibility,
            metadata={
                'original_name': func.name,
                'is_instantiate': True,
                'scrypto_function': True
            }
        )
    
    def convert_method(self, method: ScryptoMethod) -> RunaMethod:
        """Convert Scrypto method to Runa method"""
        parameters = [self.convert_parameter(param) for param in method.parameters]
        body = self.convert_block(method.body)
        
        return RunaMethod(
            name=method.name,
            parameters=parameters,
            return_type=self.convert_type(method.return_type) if method.return_type else None,
            body=body,
            is_static=False,
            visibility=method.visibility,
            metadata={
                'is_mutable': method.is_mutable,
                'access_rule': method.access_rule.value if method.access_rule else None,
                'scrypto_method': True
            }
        )
    
    def convert_parameter(self, param: ScryptoParameter) -> Parameter:
        """Convert Scrypto parameter to Runa parameter"""
        return Parameter(
            name=param.name,
            type_annotation=self.convert_type(param.param_type),
            default_value=self.convert_expression(param.default_value) if param.default_value else None,
            metadata={
                'is_mutable': param.is_mutable
            }
        )
    
    def convert_type(self, scrypto_type: Optional[ScryptoType]) -> Optional[BasicType]:
        """Convert Scrypto type to Runa type"""
        if not scrypto_type:
            return None
        
        # Map Scrypto-specific types to Runa equivalents
        type_mapping = {
            # Primitive types
            'bool': 'Boolean',
            'u8': 'UInt8', 'u16': 'UInt16', 'u32': 'UInt32', 'u64': 'UInt64', 'u128': 'UInt128',
            'i8': 'Int8', 'i16': 'Int16', 'i32': 'Int32', 'i64': 'Int64', 'i128': 'Int128',
            'f32': 'Float32', 'f64': 'Float64',
            'String': 'String', 'str': 'String',
            
            # Scrypto-specific types
            'ComponentAddress': 'Address',
            'ResourceAddress': 'Address',
            'PackageAddress': 'Address',
            'Bucket': 'AssetContainer',
            'Vault': 'AssetStorage',
            'Proof': 'AssetProof',
            'Decimal': 'BigDecimal',
            'PreciseDecimal': 'BigDecimal',
            
            # Collections
            'Vec': 'Array',
            'HashMap': 'Map',
            'BTreeMap': 'OrderedMap',
            'Option': 'Optional',
            'Result': 'Result'
        }
        
        base_type = type_mapping.get(scrypto_type.name, scrypto_type.name)
        
        # Handle generics
        generic_types = []
        for generic in scrypto_type.generics:
            generic_types.append(self.convert_type(generic))
        
        return BasicType(
            name=base_type,
            generic_parameters=generic_types,
            metadata={
                'original_scrypto_type': scrypto_type.name,
                'is_reference': scrypto_type.is_reference,
                'is_mutable': scrypto_type.is_mutable
            }
        )
    
    def convert_block(self, block: ScryptoBlock) -> List[Statement]:
        """Convert Scrypto block to list of Runa statements"""
        return [self.convert_statement(stmt) for stmt in block.statements if stmt]
    
    def convert_statement(self, stmt: ScryptoStatement) -> Statement:
        """Convert Scrypto statement to Runa statement"""
        if isinstance(stmt, ScryptoLetStatement):
            return LetStatement(
                name=stmt.name,
                type_annotation=self.convert_type(stmt.type_annotation),
                value=self.convert_expression(stmt.value) if stmt.value else None,
                is_constant=not stmt.is_mutable,
                metadata={'is_mutable': stmt.is_mutable}
            )
        
        elif isinstance(stmt, ScryptoReturnStatement):
            return ReturnStatement(
                value=self.convert_expression(stmt.value) if stmt.value else None
            )
        
        elif isinstance(stmt, ScryptoExpressionStatement):
            return ExpressionStatement(
                expression=self.convert_expression(stmt.expression)
            )
        
        else:
            return ExpressionStatement(
                expression=StringLiteral(value="// Unknown statement type", literal_type="string")
            )
    
    def convert_expression(self, expr: Optional[ScryptoExpression]) -> Optional[Expression]:
        """Convert Scrypto expression to Runa expression"""
        if not expr:
            return None
        
        if isinstance(expr, ScryptoLiteralExpression):
            return StringLiteral(
                value=expr.value,
                literal_type=expr.literal_type
            )
        
        elif isinstance(expr, ScryptoIdentifierExpression):
            return Identifier(name=expr.name)
        
        elif isinstance(expr, ScryptoMethodCallExpression):
            return self.convert_method_call(expr)
        
        elif isinstance(expr, ScryptoFunctionCallExpression):
            return self.convert_function_call(expr)
        
        elif isinstance(expr, ScryptoRadixEngineCallExpression):
            return self.convert_radix_engine_call(expr)
        
        elif isinstance(expr, ScryptoBucketExpression):
            return self.convert_bucket_operation(expr)
        
        elif isinstance(expr, ScryptoVaultExpression):
            return self.convert_vault_operation(expr)
        
        elif isinstance(expr, ScryptoStructExpression):
            return self.convert_struct_instantiation(expr)
        
        elif isinstance(expr, ScryptoMacroCall):
            return self.convert_macro_call(expr)
        
        else:
            return StringLiteral(
                value=f"// Unsupported expression: {type(expr).__name__}",
                literal_type="string"
            )
    
    def convert_method_call(self, call: ScryptoMethodCallExpression) -> RunaMethodCall:
        """Convert Scrypto method call to Runa method call"""
        receiver = self.convert_expression(call.receiver)
        arguments = [self.convert_expression(arg) for arg in call.arguments]
        
        return RunaMethodCall(
            receiver=receiver,
            method_name=call.method_name,
            arguments=arguments,
            metadata={'scrypto_method_call': True}
        )
    
    def convert_function_call(self, call: ScryptoFunctionCallExpression) -> FunctionCall:
        """Convert Scrypto function call to Runa function call"""
        arguments = [self.convert_expression(arg) for arg in call.arguments]
        
        return FunctionCall(
            function_name=call.function_name,
            arguments=arguments,
            metadata={'scrypto_function_call': True}
        )
    
    def convert_radix_engine_call(self, call: ScryptoRadixEngineCallExpression) -> RunaMethodCall:
        """Convert Radix Engine API call to Runa method call"""
        arguments = [self.convert_expression(arg) for arg in call.arguments]
        
        # Create a special receiver representing the Radix Engine API
        receiver = Identifier(name=f"RadixEngine.{call.api_name}")
        
        return RunaMethodCall(
            receiver=receiver,
            method_name=call.method_name,
            arguments=arguments,
            metadata={
                'radix_engine_call': True,
                'api_name': call.api_name
            }
        )
    
    def convert_bucket_operation(self, expr: ScryptoBucketExpression) -> RunaMethodCall:
        """Convert bucket operation to Runa method call"""
        bucket = self.convert_expression(expr.bucket)
        arguments = []
        
        if expr.amount:
            arguments.append(self.convert_expression(expr.amount))
        
        return RunaMethodCall(
            receiver=bucket,
            method_name=expr.operation,
            arguments=arguments,
            metadata={'bucket_operation': True}
        )
    
    def convert_vault_operation(self, expr: ScryptoVaultExpression) -> RunaMethodCall:
        """Convert vault operation to Runa method call"""
        vault = self.convert_expression(expr.vault)
        arguments = []
        
        if expr.amount:
            arguments.append(self.convert_expression(expr.amount))
        
        return RunaMethodCall(
            receiver=vault,
            method_name=expr.operation,
            arguments=arguments,
            metadata={'vault_operation': True}
        )
    
    def convert_struct_instantiation(self, expr: ScryptoStructExpression) -> RunaObjectInstantiation:
        """Convert struct instantiation to Runa object instantiation"""
        field_values = {}
        for field_name, field_expr in expr.fields.items():
            field_values[field_name] = self.convert_expression(field_expr)
        
        return RunaObjectInstantiation(
            class_name=expr.struct_name,
            arguments=[],
            field_values=field_values
        )
    
    def convert_macro_call(self, call: ScryptoMacroCall) -> FunctionCall:
        """Convert Scrypto macro call to Runa function call"""
        return FunctionCall(
            function_name=f"scrypto_macro_{call.macro_name}",
            arguments=[StringLiteral(value=arg, literal_type="string") for arg in call.arguments],
            metadata={'macro_call': True, 'macro_name': call.macro_name}
        )
    
    def convert_use_statement(self, use_stmt: ScryptoUseStatement) -> RunaImport:
        """Convert Scrypto use statement to Runa import"""
        return RunaImport(
            module_name=use_stmt.path,
            alias=use_stmt.alias,
            is_wildcard=use_stmt.is_glob
        )


class RunaToScryptoConverter:
    """Converts Runa AST to Scrypto AST"""
    
    def __init__(self):
        self.context = {
            'current_blueprint': None,
            'imports': [],
            'scrypto_features': set()
        }
    
    def convert(self, runa_ast: RunaAST) -> ScryptoAST:
        """Convert Runa AST to Scrypto AST"""
        if not isinstance(runa_ast.root, RunaModule):
            raise ValueError("Expected RunaModule as root node")
        
        # Convert main module
        package = self.convert_module_to_package(runa_ast.root)
        
        # Create use statements
        use_statements = []
        use_statements.append(ScryptoUseStatement(
            path="scrypto::prelude",
            is_glob=True
        ))
        
        # Add additional imports based on detected features
        if 'radix_engine' in self.context['scrypto_features']:
            use_statements.append(ScryptoUseStatement(
                path="radix_engine_interface::prelude",
                is_glob=True
            ))
        
        program = ScryptoProgram(
            packages=[package],
            use_statements=use_statements
        )
        
        return ScryptoAST(program)
    
    def convert_module_to_package(self, module: RunaModule) -> ScryptoPackage:
        """Convert Runa module to Scrypto package"""
        blueprints = []
        
        for node in module.body:
            if isinstance(node, RunaClass):
                blueprint = self.convert_class_to_blueprint(node)
                blueprints.append(blueprint)
        
        return ScryptoPackage(
            name=module.name or "default",
            version="1.0.0",
            blueprints=blueprints
        )
    
    def convert_class_to_blueprint(self, runa_class: RunaClass) -> ScryptoBlueprint:
        """Convert Runa class to Scrypto blueprint"""
        self.context['current_blueprint'] = runa_class.name
        
        # Convert fields to state struct
        struct_fields = []
        for field in runa_class.fields:
            scrypto_field = ScryptoStructField(
                name=field.name,
                field_type=self.convert_type_to_scrypto(field.type_annotation),
                visibility=field.visibility or "pub"
            )
            struct_fields.append(scrypto_field)
        
        state_struct = ScryptoStruct(
            name=runa_class.name,
            fields=struct_fields,
            derives=["ScryptoSbor"]
        )
        
        # Convert methods
        methods = []
        instantiate_functions = []
        
        for method in runa_class.methods:
            if method.name == "__init__" or method.metadata.get('is_instantiate'):
                func = self.convert_constructor_to_instantiate(method)
                instantiate_functions.append(func)
            else:
                scrypto_method = self.convert_method_to_scrypto(method)
                methods.append(scrypto_method)
        
        return ScryptoBlueprint(
            name=runa_class.name,
            state_struct=state_struct,
            methods=methods,
            instantiate_functions=instantiate_functions
        )
    
    def convert_constructor_to_instantiate(self, method: RunaMethod) -> ScryptoFunction:
        """Convert Runa constructor to Scrypto instantiate function"""
        parameters = [self.convert_parameter_to_scrypto(param) for param in method.parameters]
        body = self.convert_statements_to_block(method.body)
        
        return ScryptoFunction(
            name=method.metadata.get('original_name', 'instantiate'),
            parameters=parameters,
            return_type=ScryptoType(name="ComponentAddress"),
            body=body,
            visibility="pub",
            is_instantiate=True
        )
    
    def convert_method_to_scrypto(self, method: RunaMethod) -> ScryptoMethod:
        """Convert Runa method to Scrypto method"""
        parameters = [self.convert_parameter_to_scrypto(param) for param in method.parameters]
        body = self.convert_statements_to_block(method.body)
        
        return ScryptoMethod(
            name=method.name,
            parameters=parameters,
            return_type=self.convert_type_to_scrypto(method.return_type),
            body=body,
            visibility=method.visibility or "pub",
            is_mutable=method.metadata.get('is_mutable', False)
        )
    
    def convert_parameter_to_scrypto(self, param: Parameter) -> ScryptoParameter:
        """Convert Runa parameter to Scrypto parameter"""
        return ScryptoParameter(
            name=param.name,
            param_type=self.convert_type_to_scrypto(param.type_annotation),
            is_mutable=param.metadata.get('is_mutable', False)
        )
    
    def convert_type_to_scrypto(self, runa_type: Optional[BasicType]) -> Optional[ScryptoType]:
        """Convert Runa type to Scrypto type"""
        if not runa_type:
            return None
        
        # Reverse mapping from Runa types to Scrypto types
        type_mapping = {
            'Boolean': 'bool',
            'UInt8': 'u8', 'UInt16': 'u16', 'UInt32': 'u32', 'UInt64': 'u64', 'UInt128': 'u128',
            'Int8': 'i8', 'Int16': 'i16', 'Int32': 'i32', 'Int64': 'i64', 'Int128': 'i128',
            'Float32': 'f32', 'Float64': 'f64',
            'String': 'String',
            
            'Address': 'ComponentAddress',  # Default to ComponentAddress
            'AssetContainer': 'Bucket',
            'AssetStorage': 'Vault',
            'AssetProof': 'Proof',
            'BigDecimal': 'Decimal',
            
            'Array': 'Vec',
            'Map': 'HashMap',
            'OrderedMap': 'BTreeMap',
            'Optional': 'Option',
            'Result': 'Result'
        }
        
        scrypto_type_name = type_mapping.get(runa_type.name, runa_type.name)
        
        # Handle original Scrypto type from metadata
        if runa_type.metadata and 'original_scrypto_type' in runa_type.metadata:
            scrypto_type_name = runa_type.metadata['original_scrypto_type']
        
        # Handle generics
        generics = []
        for generic in runa_type.generic_parameters or []:
            generics.append(self.convert_type_to_scrypto(generic))
        
        return ScryptoType(
            name=scrypto_type_name,
            generics=generics,
            is_reference=runa_type.metadata.get('is_reference', False),
            is_mutable=runa_type.metadata.get('is_mutable', False)
        )
    
    def convert_statements_to_block(self, statements: List[Statement]) -> ScryptoBlock:
        """Convert list of Runa statements to Scrypto block"""
        scrypto_statements = []
        
        for stmt in statements:
            scrypto_stmt = self.convert_statement_to_scrypto(stmt)
            if scrypto_stmt:
                scrypto_statements.append(scrypto_stmt)
        
        return ScryptoBlock(statements=scrypto_statements)
    
    def convert_statement_to_scrypto(self, stmt: Statement) -> Optional[ScryptoStatement]:
        """Convert Runa statement to Scrypto statement"""
        if isinstance(stmt, LetStatement):
            return ScryptoLetStatement(
                name=stmt.name,
                type_annotation=self.convert_type_to_scrypto(stmt.type_annotation),
                value=self.convert_expression_to_scrypto(stmt.value),
                is_mutable=stmt.metadata.get('is_mutable', not stmt.is_constant)
            )
        
        elif isinstance(stmt, ReturnStatement):
            return ScryptoReturnStatement(
                value=self.convert_expression_to_scrypto(stmt.value)
            )
        
        elif isinstance(stmt, ExpressionStatement):
            expr = self.convert_expression_to_scrypto(stmt.expression)
            return ScryptoExpressionStatement(expression=expr) if expr else None
        
        return None
    
    def convert_expression_to_scrypto(self, expr: Optional[Expression]) -> Optional[ScryptoExpression]:
        """Convert Runa expression to Scrypto expression"""
        if not expr:
            return None
        
        if isinstance(expr, StringLiteral):
            return ScryptoLiteralExpression(
                value=expr.value,
                literal_type=expr.literal_type
            )
        
        elif isinstance(expr, Identifier):
            return ScryptoIdentifierExpression(name=expr.name)
        
        elif isinstance(expr, RunaMethodCall):
            receiver = self.convert_expression_to_scrypto(expr.receiver)
            arguments = [self.convert_expression_to_scrypto(arg) for arg in expr.arguments if arg]
            
            # Check for special conversions
            if expr.metadata.get('radix_engine_call'):
                self.context['scrypto_features'].add('radix_engine')
                return ScryptoRadixEngineCallExpression(
                    api_name=expr.metadata.get('api_name', 'Unknown'),
                    method_name=expr.method_name,
                    arguments=arguments
                )
            
            elif expr.metadata.get('bucket_operation'):
                return ScryptoBucketExpression(
                    operation=expr.method_name,
                    bucket=receiver,
                    amount=arguments[0] if arguments else None
                )
            
            elif expr.metadata.get('vault_operation'):
                return ScryptoVaultExpression(
                    operation=expr.method_name,
                    vault=receiver,
                    amount=arguments[0] if arguments else None
                )
            
            else:
                return ScryptoMethodCallExpression(
                    receiver=receiver,
                    method_name=expr.method_name,
                    arguments=arguments
                )
        
        elif isinstance(expr, FunctionCall):
            arguments = [self.convert_expression_to_scrypto(arg) for arg in expr.arguments if arg]
            
            # Check for macro call
            if expr.metadata.get('macro_call'):
                return ScryptoMacroCall(
                    macro_name=expr.metadata.get('macro_name', expr.function_name),
                    arguments=[arg.value if isinstance(arg, ScryptoLiteralExpression) else str(arg) 
                              for arg in arguments]
                )
            
            return ScryptoFunctionCallExpression(
                function_name=expr.function_name,
                arguments=arguments
            )
        
        return ScryptoLiteralExpression(
            value=f"// Unsupported expression: {type(expr).__name__}",
            literal_type="string"
        )


def convert_scrypto_to_runa(scrypto_ast: ScryptoAST) -> RunaAST:
    """Convert Scrypto AST to Runa AST"""
    converter = ScryptoToRunaConverter()
    return converter.convert(scrypto_ast)


def convert_runa_to_scrypto(runa_ast: RunaAST) -> ScryptoAST:
    """Convert Runa AST to Scrypto AST"""
    converter = RunaToScryptoConverter()
    return converter.convert(runa_ast) 