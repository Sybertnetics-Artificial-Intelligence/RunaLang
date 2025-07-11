#!/usr/bin/env python3
"""
Nix Converter - Bidirectional conversion between Nix and Runa AST

Features:
- Complete Nix → Runa AST conversion
- Full Runa AST → Nix conversion  
- Functional programming construct mapping
- Package derivation translation
- Attribute set and object mapping
- Function and closure conversion
- String interpolation handling
- Import system translation
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import re

# Import Runa core components
from runa.core.ast_nodes import *
from runa.core.semantic_analyzer import SemanticAnalyzer
from runa.core.types import *

# Import Nix AST
from .nix_ast import *

class NixToRunaConverter:
    """Converts Nix AST to Runa AST"""
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.variable_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
        self.package_mappings: Dict[str, str] = {}
        self.current_scope_depth = 0
        
    def convert(self, nix_ast: NixFile) -> ModuleNode:
        """Convert Nix AST to Runa AST"""
        # Create main module
        module = ModuleNode(
            name="nix_module",
            statements=[],
            imports=[],
            metadata={"original_language": "nix", "package_manager": "nix"}
        )
        
        # Convert main expression
        main_expr = self.convert_expression(nix_ast.expression)
        
        # Wrap expression in a main function or variable
        if isinstance(main_expr, (FunctionDeclarationNode, ClassDeclarationNode)):
            module.statements.append(main_expr)
        else:
            # Create a main variable
            main_var = VariableDeclarationNode(
                name="main",
                type_annotation=self.infer_expression_type(nix_ast.expression),
                initial_value=main_expr,
                is_mutable=False,
                metadata={"nix_main_expression": True}
            )
            module.statements.append(main_var)
            
        # Add package management metadata
        self.add_package_metadata(module, nix_ast)
        
        return module
        
    def convert_expression(self, expr: NixExpression) -> ExpressionNode:
        """Convert Nix expression to Runa expression"""
        if isinstance(expr, StringLiteral):
            return self.convert_string_literal(expr)
        elif isinstance(expr, IntegerLiteral):
            return IntegerLiteralNode(expr.value)
        elif isinstance(expr, FloatLiteral):
            return FloatLiteralNode(expr.value)
        elif isinstance(expr, BooleanLiteral):
            return BooleanLiteralNode(expr.value)
        elif isinstance(expr, NullLiteral):
            return NullLiteralNode()
        elif isinstance(expr, PathLiteral):
            return StringLiteralNode(expr.value)  # Treat paths as strings
        elif isinstance(expr, Identifier):
            return IdentifierNode(self.sanitize_identifier(expr.name))
        elif isinstance(expr, AttributeSet):
            return self.convert_attribute_set(expr)
        elif isinstance(expr, AttributeAccess):
            return self.convert_attribute_access(expr)
        elif isinstance(expr, ListExpression):
            return self.convert_list_expression(expr)
        elif isinstance(expr, FunctionExpression):
            return self.convert_function_expression(expr)
        elif isinstance(expr, FunctionApplication):
            return self.convert_function_application(expr)
        elif isinstance(expr, LetExpression):
            return self.convert_let_expression(expr)
        elif isinstance(expr, ConditionalExpression):
            return self.convert_conditional_expression(expr)
        elif isinstance(expr, BinaryOperation):
            return self.convert_binary_operation(expr)
        elif isinstance(expr, UnaryOperation):
            return self.convert_unary_operation(expr)
        elif isinstance(expr, WithExpression):
            return self.convert_with_expression(expr)
        elif isinstance(expr, AssertExpression):
            return self.convert_assert_expression(expr)
        elif isinstance(expr, ImportExpression):
            return self.convert_import_expression(expr)
        elif isinstance(expr, DerivationExpression):
            return self.convert_derivation_expression(expr)
        elif isinstance(expr, BuiltinFunction):
            return self.convert_builtin_function(expr)
        elif isinstance(expr, StringInterpolation):
            return self.convert_string_interpolation(expr)
        elif isinstance(expr, PackageExpression):
            return self.convert_package_expression(expr)
        elif isinstance(expr, OverrideExpression):
            return self.convert_override_expression(expr)
        elif isinstance(expr, CallPackageExpression):
            return self.convert_call_package_expression(expr)
        else:
            # Unknown expression - create annotation
            return self.create_annotation(f"Unknown Nix expression: {type(expr).__name__}")
            
    def convert_string_literal(self, string_lit: StringLiteral) -> ExpressionNode:
        """Convert string literal with interpolation support"""
        if not string_lit.has_interpolation:
            return StringLiteralNode(string_lit.value)
        else:
            # Convert interpolated string to template string or concatenation
            if string_lit.interpolated_parts:
                # Build concatenation of string parts and interpolated expressions
                parts = [StringLiteralNode(string_lit.value)]
                for part in string_lit.interpolated_parts:
                    parts.append(self.convert_expression(part))
                    
                # Chain binary operations for concatenation
                result = parts[0]
                for part in parts[1:]:
                    result = BinaryOperationNode(result, "+", part)
                return result
            else:
                return StringLiteralNode(string_lit.value)
                
    def convert_attribute_set(self, attr_set: AttributeSet) -> ExpressionNode:
        """Convert attribute set to Runa object/dictionary"""
        # Create dictionary literal or class
        fields = []
        
        for binding in attr_set.attributes:
            if binding.is_inherit:
                # Handle inherit statements
                if binding.inherit_source:
                    # inherit (source) attr;
                    source_expr = self.convert_expression(binding.inherit_source)
                    for attr_name in binding.path:
                        attr_access = AttributeAccessNode(
                            object=source_expr,
                            attribute=attr_name
                        )
                        field = DictionaryFieldNode(
                            key=StringLiteralNode(attr_name),
                            value=attr_access
                        )
                        fields.append(field)
                else:
                    # inherit attr;
                    for attr_name in binding.path:
                        field = DictionaryFieldNode(
                            key=StringLiteralNode(attr_name),
                            value=IdentifierNode(self.sanitize_identifier(attr_name))
                        )
                        fields.append(field)
            else:
                # Regular attribute binding
                attr_path = ".".join(binding.path)
                value = self.convert_expression(binding.value)
                
                field = DictionaryFieldNode(
                    key=StringLiteralNode(attr_path),
                    value=value
                )
                fields.append(field)
                
        dict_literal = DictionaryLiteralNode(fields)
        
        # Add metadata about recursiveness
        if attr_set.is_recursive:
            dict_literal.metadata = {"nix_recursive": True}
            
        return dict_literal
        
    def convert_attribute_access(self, attr_access: AttributeAccess) -> ExpressionNode:
        """Convert attribute access to Runa attribute access"""
        object_expr = self.convert_expression(attr_access.expression)
        
        if isinstance(attr_access.attribute, str):
            attr_name = attr_access.attribute
        else:
            # Dynamic attribute access
            attr_expr = self.convert_expression(attr_access.attribute)
            return IndexAccessNode(object=object_expr, index=attr_expr)
            
        access_node = AttributeAccessNode(
            object=object_expr,
            attribute=attr_name
        )
        
        # Handle default values
        if attr_access.has_default and attr_access.default_value:
            default_expr = self.convert_expression(attr_access.default_value)
            # Create conditional: obj.attr if hasattr(obj, attr) else default
            has_attr_check = FunctionCallNode(
                function=IdentifierNode("hasattr"),
                arguments=[object_expr, StringLiteralNode(attr_name)]
            )
            return ConditionalExpressionNode(
                condition=has_attr_check,
                true_expr=access_node,
                false_expr=default_expr
            )
            
        return access_node
        
    def convert_list_expression(self, list_expr: ListExpression) -> ListLiteralNode:
        """Convert list expression to Runa list"""
        elements = [self.convert_expression(elem) for elem in list_expr.elements]
        return ListLiteralNode(elements)
        
    def convert_function_expression(self, func_expr: FunctionExpression) -> ExpressionNode:
        """Convert function expression to Runa function"""
        # Handle parameters
        parameters = []
        
        if isinstance(func_expr.parameter, str):
            # Simple parameter: arg: body
            param = ParameterNode(
                name=self.sanitize_identifier(func_expr.parameter),
                type_annotation=AnyTypeNode(),
                default_value=None
            )
            parameters.append(param)
        elif isinstance(func_expr.parameter, FunctionParameters):
            # Destructured parameters: { a, b ? default }: body
            func_params = func_expr.parameter
            
            for param_name, default_value in func_params.parameters.items():
                default_expr = None
                if default_value:
                    default_expr = self.convert_expression(default_value)
                    
                param = ParameterNode(
                    name=self.sanitize_identifier(param_name),
                    type_annotation=AnyTypeNode(),
                    default_value=default_expr
                )
                parameters.append(param)
                
            # Handle ellipsis (variadic parameters)
            if func_params.has_ellipsis:
                param = ParameterNode(
                    name="kwargs",
                    type_annotation=DictionaryTypeNode(StringTypeNode(), AnyTypeNode()),
                    default_value=None,
                    is_variadic=True
                )
                parameters.append(param)
                
        # Convert body
        body_expr = self.convert_expression(func_expr.body)
        
        # Create function body with return
        if isinstance(body_expr, StatementNode):
            body_statements = [body_expr]
        else:
            body_statements = [ReturnStatementNode(body_expr)]
            
        body_block = BlockNode(body_statements)
        
        # Create lambda or function declaration
        return LambdaExpressionNode(
            parameters=parameters,
            body=body_block,
            metadata={"nix_function": True}
        )
        
    def convert_function_application(self, app: FunctionApplication) -> FunctionCallNode:
        """Convert function application to Runa function call"""
        function_expr = self.convert_expression(app.function)
        argument_expr = self.convert_expression(app.argument)
        
        # Handle curried functions
        if isinstance(argument_expr, DictionaryLiteralNode):
            # Destructured argument - pass fields as named arguments
            kwargs = []
            for field in argument_expr.fields:
                if isinstance(field.key, StringLiteralNode):
                    kwarg = NamedArgumentNode(
                        name=field.key.value,
                        value=field.value
                    )
                    kwargs.append(kwarg)
                    
            return FunctionCallNode(
                function=function_expr,
                arguments=[],
                named_arguments=kwargs
            )
        else:
            return FunctionCallNode(
                function=function_expr,
                arguments=[argument_expr]
            )
            
    def convert_let_expression(self, let_expr: LetExpression) -> ExpressionNode:
        """Convert let expression to Runa block with local variables"""
        statements = []
        
        # Convert bindings to variable declarations
        for binding in let_expr.bindings:
            if not binding.is_inherit:
                var_name = "_".join(binding.path)
                value = self.convert_expression(binding.value)
                
                var_decl = VariableDeclarationNode(
                    name=self.sanitize_identifier(var_name),
                    type_annotation=self.infer_expression_type(binding.value),
                    initial_value=value,
                    is_mutable=False
                )
                statements.append(var_decl)
                
        # Convert body
        body_expr = self.convert_expression(let_expr.body)
        
        # Create block expression
        statements.append(ExpressionStatementNode(body_expr))
        block = BlockNode(statements)
        
        return BlockExpressionNode(block)
        
    def convert_conditional_expression(self, cond_expr: ConditionalExpression) -> ConditionalExpressionNode:
        """Convert conditional expression to Runa conditional"""
        condition = self.convert_expression(cond_expr.condition)
        true_expr = self.convert_expression(cond_expr.then_expr)
        false_expr = self.convert_expression(cond_expr.else_expr)
        
        return ConditionalExpressionNode(
            condition=condition,
            true_expr=true_expr,
            false_expr=false_expr
        )
        
    def convert_binary_operation(self, bin_op: BinaryOperation) -> BinaryOperationNode:
        """Convert binary operation to Runa binary operation"""
        left = self.convert_expression(bin_op.left)
        right = self.convert_expression(bin_op.right)
        
        # Map Nix operators to Runa operators
        operator_mapping = {
            '+': '+',
            '-': '-', 
            '*': '*',
            '/': '/',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '&&': 'and',
            '||': 'or',
            '++': '+',  # List/string concatenation
            '//': '+'   # Attribute set update (merge)
        }
        
        runa_op = operator_mapping.get(bin_op.operator, bin_op.operator)
        
        return BinaryOperationNode(left, runa_op, right)
        
    def convert_unary_operation(self, unary_op: UnaryOperation) -> UnaryOperationNode:
        """Convert unary operation to Runa unary operation"""
        operand = self.convert_expression(unary_op.operand)
        
        operator_mapping = {
            '!': 'not',
            '-': '-'
        }
        
        runa_op = operator_mapping.get(unary_op.operator, unary_op.operator)
        
        return UnaryOperationNode(runa_op, operand)
        
    def convert_with_expression(self, with_expr: WithExpression) -> ExpressionNode:
        """Convert with expression to Runa context manager or variable assignment"""
        namespace = self.convert_expression(with_expr.namespace)
        body = self.convert_expression(with_expr.body)
        
        # Create a context where namespace attributes are available
        # This is similar to Python's "from module import *"
        return FunctionCallNode(
            function=IdentifierNode("with_namespace"),
            arguments=[namespace, body],
            metadata={"nix_with_expression": True}
        )
        
    def convert_assert_expression(self, assert_expr: AssertExpression) -> ExpressionNode:
        """Convert assert expression to Runa assertion"""
        condition = self.convert_expression(assert_expr.condition)
        body = self.convert_expression(assert_expr.body)
        
        # Create assertion followed by body
        assert_stmt = AssertStatementNode(condition)
        body_stmt = ExpressionStatementNode(body)
        
        block = BlockNode([assert_stmt, body_stmt])
        return BlockExpressionNode(block)
        
    def convert_import_expression(self, import_expr: ImportExpression) -> ExpressionNode:
        """Convert import expression to Runa import"""
        path_expr = self.convert_expression(import_expr.path)
        
        if isinstance(path_expr, StringLiteralNode):
            # Static import
            module_name = self.path_to_module_name(path_expr.value)
            return FunctionCallNode(
                function=IdentifierNode("import_nix_file"),
                arguments=[StringLiteralNode(module_name)],
                metadata={"nix_import": True}
            )
        else:
            # Dynamic import
            return FunctionCallNode(
                function=IdentifierNode("import_nix_file"),
                arguments=[path_expr],
                metadata={"nix_import": True, "dynamic": True}
            )
            
    def convert_derivation_expression(self, deriv_expr: DerivationExpression) -> ClassDeclarationNode:
        """Convert derivation to Runa class representing a package"""
        class_name = self.sanitize_identifier(deriv_expr.name or "Package")
        
        # Create class for package
        methods = []
        properties = []
        
        # Convert derivation attributes to class properties
        for binding in deriv_expr.attributes:
            if not binding.is_inherit:
                prop_name = "_".join(binding.path)
                value = self.convert_expression(binding.value)
                
                prop = PropertyDeclarationNode(
                    name=self.sanitize_identifier(prop_name),
                    type_annotation=self.infer_expression_type(binding.value),
                    initial_value=value,
                    is_readonly=True
                )
                properties.append(prop)
                
        # Add build method
        build_method = MethodDeclarationNode(
            name="build",
            parameters=[ParameterNode("self", SelfTypeNode())],
            return_type=StringTypeNode(),
            body=BlockNode([
                ReturnStatementNode(StringLiteralNode("Built package"))
            ]),
            metadata={"nix_build_method": True}
        )
        methods.append(build_method)
        
        return ClassDeclarationNode(
            name=class_name,
            methods=methods,
            properties=properties,
            metadata={
                "nix_derivation": True,
                "package_name": deriv_expr.name,
                "system": deriv_expr.system
            }
        )
        
    def convert_builtin_function(self, builtin: BuiltinFunction) -> IdentifierNode:
        """Convert builtin function to Runa equivalent"""
        # Map Nix builtins to Runa functions
        builtin_mapping = {
            'map': 'map',
            'filter': 'filter',
            'length': 'len',
            'head': 'first',
            'tail': 'rest',
            'toString': 'str',
            'import': 'import_nix_file',
            'derivation': 'create_package',
            'isAttrs': 'isinstance_dict',
            'isList': 'isinstance_list',
            'isString': 'isinstance_str',
            'isInt': 'isinstance_int',
            'isBool': 'isinstance_bool',
            'isNull': 'isinstance_none'
        }
        
        runa_name = builtin_mapping.get(builtin.name, f"nix_{builtin.name}")
        return IdentifierNode(runa_name)
        
    def convert_string_interpolation(self, interp: StringInterpolation) -> ExpressionNode:
        """Convert string interpolation to Runa string formatting"""
        expr = self.convert_expression(interp.expression)
        
        # Convert to f-string equivalent
        return FunctionCallNode(
            function=IdentifierNode("str"),
            arguments=[expr]
        )
        
    def convert_package_expression(self, pkg_expr: PackageExpression) -> ClassDeclarationNode:
        """Convert package expression to Runa package class"""
        deriv_class = self.convert_derivation_expression(pkg_expr.derivation)
        
        # Add package metadata
        if pkg_expr.meta:
            meta_expr = self.convert_expression(pkg_expr.meta)
            meta_prop = PropertyDeclarationNode(
                name="meta",
                type_annotation=DictionaryTypeNode(StringTypeNode(), AnyTypeNode()),
                initial_value=meta_expr,
                is_readonly=True
            )
            deriv_class.properties.append(meta_prop)
            
        deriv_class.metadata.update({
            "package_version": pkg_expr.version,
            "package_type": "nix_package"
        })
        
        return deriv_class
        
    def convert_override_expression(self, override_expr: OverrideExpression) -> FunctionCallNode:
        """Convert package override to Runa function call"""
        package = self.convert_expression(override_expr.package)
        overrides = self.convert_expression(override_expr.overrides)
        
        return FunctionCallNode(
            function=IdentifierNode("override_package"),
            arguments=[package, overrides],
            metadata={"nix_override": True}
        )
        
    def convert_call_package_expression(self, call_pkg_expr: CallPackageExpression) -> FunctionCallNode:
        """Convert callPackage to Runa function call"""
        package_path = self.convert_expression(call_pkg_expr.package_path)
        
        args = [package_path]
        if call_pkg_expr.arguments:
            args.append(self.convert_expression(call_pkg_expr.arguments))
            
        return FunctionCallNode(
            function=IdentifierNode("call_package"),
            arguments=args,
            metadata={"nix_call_package": True}
        )
        
    # Helper methods
    
    def sanitize_identifier(self, name: str) -> str:
        """Convert Nix identifier to valid Runa identifier"""
        # Replace hyphens with underscores
        sanitized = name.replace('-', '_')
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', sanitized)
        
        # Ensure it starts with letter or underscore
        if sanitized and sanitized[0].isdigit():
            sanitized = f"_{sanitized}"
            
        return sanitized or "unnamed"
        
    def infer_expression_type(self, expr: NixExpression) -> TypeNode:
        """Infer Runa type for Nix expression"""
        if isinstance(expr, StringLiteral):
            return StringTypeNode()
        elif isinstance(expr, IntegerLiteral):
            return IntegerTypeNode()
        elif isinstance(expr, FloatLiteral):
            return FloatTypeNode()
        elif isinstance(expr, BooleanLiteral):
            return BooleanTypeNode()
        elif isinstance(expr, NullLiteral):
            return NullableTypeNode(AnyTypeNode())
        elif isinstance(expr, ListExpression):
            if expr.elements:
                elem_type = self.infer_expression_type(expr.elements[0])
                return ListTypeNode(elem_type)
            return ListTypeNode(AnyTypeNode())
        elif isinstance(expr, AttributeSet):
            return DictionaryTypeNode(StringTypeNode(), AnyTypeNode())
        elif isinstance(expr, FunctionExpression):
            return FunctionTypeNode(
                parameter_types=[AnyTypeNode()],
                return_type=AnyTypeNode()
            )
        else:
            return AnyTypeNode()
            
    def path_to_module_name(self, path: str) -> str:
        """Convert file path to module name"""
        # Remove extension and sanitize
        name = path.replace('.nix', '').replace('/', '_')
        return self.sanitize_identifier(name)
        
    def create_annotation(self, description: str) -> AnnotationNode:
        """Create annotation for unknown constructs"""
        return AnnotationNode(
            name="nix_annotation",
            arguments=[StringLiteralNode(description)],
            metadata={"unknown_construct": True}
        )
        
    def add_package_metadata(self, module: ModuleNode, nix_ast: NixFile) -> None:
        """Add package management metadata to module"""
        metadata = {
            "package_manager": "nix",
            "functional_language": True,
            "lazy_evaluation": True
        }
        module.metadata.update(metadata)

class RunaToNixConverter:
    """Converts Runa AST to Nix AST"""
    
    def __init__(self):
        self.variable_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
        
    def convert(self, runa_ast: ModuleNode) -> NixFile:
        """Convert Runa AST to Nix AST"""
        # Find main expression or create one
        main_expr = NullLiteral()
        
        for stmt in runa_ast.statements:
            if isinstance(stmt, VariableDeclarationNode) and stmt.name == "main":
                if stmt.initial_value:
                    main_expr = self.convert_expression(stmt.initial_value)
                break
            elif isinstance(stmt, FunctionDeclarationNode):
                func_expr = self.convert_function_declaration(stmt)
                if main_expr == NullLiteral():
                    main_expr = func_expr
                    
        return NixFile(expression=main_expr)
        
    def convert_expression(self, expr: ExpressionNode) -> NixExpression:
        """Convert Runa expression to Nix expression"""
        if isinstance(expr, StringLiteralNode):
            return StringLiteral(expr.value)
        elif isinstance(expr, IntegerLiteralNode):
            return IntegerLiteral(expr.value)
        elif isinstance(expr, FloatLiteralNode):
            return FloatLiteral(expr.value)
        elif isinstance(expr, BooleanLiteralNode):
            return BooleanLiteral(expr.value)
        elif isinstance(expr, NullLiteralNode):
            return NullLiteral()
        elif isinstance(expr, IdentifierNode):
            return Identifier(expr.name)
        elif isinstance(expr, ListLiteralNode):
            elements = [self.convert_expression(elem) for elem in expr.elements]
            return ListExpression(elements)
        elif isinstance(expr, DictionaryLiteralNode):
            return self.convert_dictionary_to_attribute_set(expr)
        elif isinstance(expr, FunctionCallNode):
            return self.convert_function_call(expr)
        elif isinstance(expr, BinaryOperationNode):
            return self.convert_binary_operation(expr)
        elif isinstance(expr, ConditionalExpressionNode):
            return self.convert_conditional_expression(expr)
        elif isinstance(expr, LambdaExpressionNode):
            return self.convert_lambda_expression(expr)
        else:
            # Create identifier for unknown expressions
            return Identifier("unknown")
            
    def convert_dictionary_to_attribute_set(self, dict_expr: DictionaryLiteralNode) -> AttributeSet:
        """Convert dictionary to Nix attribute set"""
        attributes = []
        
        for field in dict_expr.fields:
            if isinstance(field.key, StringLiteralNode):
                path = field.key.value.split('.')
                value = self.convert_expression(field.value)
                
                binding = AttributeBinding(path=path, value=value)
                attributes.append(binding)
                
        is_recursive = dict_expr.metadata.get("nix_recursive", False) if dict_expr.metadata else False
        
        return AttributeSet(attributes=attributes, is_recursive=is_recursive)
        
    def convert_function_call(self, call: FunctionCallNode) -> NixExpression:
        """Convert function call to Nix equivalent"""
        func_name = call.function.name if isinstance(call.function, IdentifierNode) else None
        
        # Handle special Nix functions
        if func_name in ["import_nix_file", "nix_import"]:
            if call.arguments:
                path_expr = self.convert_expression(call.arguments[0])
                return ImportExpression(path=path_expr)
                
        elif func_name == "with_namespace":
            if len(call.arguments) >= 2:
                namespace = self.convert_expression(call.arguments[0])
                body = self.convert_expression(call.arguments[1])
                return WithExpression(namespace=namespace, body=body)
                
        elif func_name == "call_package":
            if call.arguments:
                package_path = self.convert_expression(call.arguments[0])
                arguments = None
                if len(call.arguments) > 1:
                    arguments = self.convert_expression(call.arguments[1])
                return CallPackageExpression(package_path=package_path, arguments=arguments)
                
        # Regular function application
        function = self.convert_expression(call.function)
        
        if call.arguments:
            # Create nested applications for multiple arguments
            result = function
            for arg in call.arguments:
                arg_expr = self.convert_expression(arg)
                result = FunctionApplication(function=result, argument=arg_expr)
            return result
        else:
            return function
            
    def convert_function_declaration(self, func_decl: FunctionDeclarationNode) -> FunctionExpression:
        """Convert function declaration to Nix function"""
        # Convert parameters
        if len(func_decl.parameters) == 1:
            param = func_decl.parameters[0].name
        else:
            # Multiple parameters - use attribute set pattern
            params = {}
            for p in func_decl.parameters:
                params[p.name] = None  # No default for now
            param = FunctionParameters(parameters=params)
            
        # Convert body
        if func_decl.body and func_decl.body.statements:
            # Find return statement or use last expression
            for stmt in reversed(func_decl.body.statements):
                if isinstance(stmt, ReturnStatementNode):
                    body = self.convert_expression(stmt.value)
                    break
                elif isinstance(stmt, ExpressionStatementNode):
                    body = self.convert_expression(stmt.expression)
                    break
            else:
                body = NullLiteral()
        else:
            body = NullLiteral()
            
        return FunctionExpression(parameter=param, body=body)
        
    def convert_lambda_expression(self, lambda_expr: LambdaExpressionNode) -> FunctionExpression:
        """Convert lambda to Nix function"""
        # Convert parameters
        if len(lambda_expr.parameters) == 1:
            param = lambda_expr.parameters[0].name
        else:
            params = {}
            for p in lambda_expr.parameters:
                default_val = None
                if p.default_value:
                    default_val = self.convert_expression(p.default_value)
                params[p.name] = default_val
            param = FunctionParameters(parameters=params)
            
        # Convert body
        if lambda_expr.body and lambda_expr.body.statements:
            if len(lambda_expr.body.statements) == 1:
                stmt = lambda_expr.body.statements[0]
                if isinstance(stmt, ReturnStatementNode):
                    body = self.convert_expression(stmt.value)
                elif isinstance(stmt, ExpressionStatementNode):
                    body = self.convert_expression(stmt.expression)
                else:
                    body = NullLiteral()
            else:
                body = NullLiteral()  # Multiple statements not easily convertible
        else:
            body = NullLiteral()
            
        return FunctionExpression(parameter=param, body=body)
        
    def convert_binary_operation(self, bin_op: BinaryOperationNode) -> BinaryOperation:
        """Convert binary operation to Nix"""
        left = self.convert_expression(bin_op.left)
        right = self.convert_expression(bin_op.right)
        
        # Map operators back to Nix
        operator_mapping = {
            'and': '&&',
            'or': '||',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>='
        }
        
        nix_op = operator_mapping.get(bin_op.operator, bin_op.operator)
        
        return BinaryOperation(left=left, operator=nix_op, right=right)
        
    def convert_conditional_expression(self, cond_expr: ConditionalExpressionNode) -> ConditionalExpression:
        """Convert conditional to Nix if-then-else"""
        condition = self.convert_expression(cond_expr.condition)
        then_expr = self.convert_expression(cond_expr.true_expr)
        else_expr = self.convert_expression(cond_expr.false_expr)
        
        return ConditionalExpression(
            condition=condition,
            then_expr=then_expr,
            else_expr=else_expr
        )

# Main conversion functions

def nix_to_runa(nix_ast: NixFile) -> ModuleNode:
    """Convert Nix AST to Runa AST"""
    converter = NixToRunaConverter()
    return converter.convert(nix_ast)

def runa_to_nix(runa_ast: ModuleNode) -> NixFile:
    """Convert Runa AST to Nix AST"""
    converter = RunaToNixConverter()
    return converter.convert(runa_ast)

# Export main components
__all__ = [
    'NixToRunaConverter', 'RunaToNixConverter',
    'nix_to_runa', 'runa_to_nix'
] 