#!/usr/bin/env python3
"""
Plutus-Runa AST Converter

Bidirectional converter between Plutus AST and Runa AST.
Handles Haskell-based smart contract constructs, UPLC compilation, and Cardano-specific features.
"""

from typing import Optional, List, Dict, Any, Union
from ...runa.runa_ast import *
from .plutus_ast import *


class PlutusToRunaConverter:
    """Converts Plutus AST to Runa AST."""
    
    def __init__(self):
        self.symbol_table = {}
        self.type_mappings = {}
        self.context_stack = []
    
    def convert_program(self, plutus_program: PlutusProgram) -> Program:
        """Convert Plutus program to Runa program."""
        runa_modules = []
        
        for module in plutus_program.modules:
            runa_module = self.convert_module(module)
            if runa_module:
                runa_modules.append(runa_module)
        
        return Program(
            name="PlutusProgram",
            modules=runa_modules,
            metadata={"source_language": "plutus", "target": "cardano"}
        )
    
    def convert_module(self, plutus_module: PlutusModule) -> RunaModule:
        """Convert Plutus module to Runa module."""
        # Convert imports
        runa_imports = []
        for imp in plutus_module.imports:
            runa_import = self.convert_import(imp)
            if runa_import:
                runa_imports.append(runa_import)
        
        # Convert declarations
        runa_declarations = []
        for decl in plutus_module.declarations:
            runa_decl = self.convert_declaration(decl)
            if runa_decl:
                runa_declarations.append(runa_decl)
        
        return RunaModule(
            name=plutus_module.name,
            imports=runa_imports,
            declarations=runa_declarations,
            metadata={"original_exports": [exp.name for exp in plutus_module.exports]}
        )
    
    def convert_import(self, plutus_import: PlutusImport) -> RunaImport:
        """Convert Plutus import to Runa import."""
        return RunaImport(
            module_path=plutus_import.module_name.replace('.', '/'),
            alias=plutus_import.alias,
            imports=plutus_import.imports or [],
            metadata={
                "qualified": plutus_import.qualified,
                "original_module": plutus_import.module_name
            }
        )
    
    def convert_declaration(self, decl: PlutusDeclaration) -> Optional[Declaration]:
        """Convert Plutus declaration to Runa declaration."""
        if isinstance(decl, PlutusFunctionDeclaration):
            return self.convert_function_declaration(decl)
        elif isinstance(decl, PlutusValueDeclaration):
            return self.convert_value_declaration(decl)
        elif isinstance(decl, PlutusDataDeclaration):
            return self.convert_data_declaration(decl)
        elif isinstance(decl, PlutusValidator):
            return self.convert_validator(decl)
        elif isinstance(decl, PlutusMintingPolicy):
            return self.convert_minting_policy(decl)
        elif isinstance(decl, PlutusNewtypeDeclaration):
            return self.convert_newtype_declaration(decl)
        else:
            return None
    
    def convert_function_declaration(self, decl: PlutusFunctionDeclaration) -> ProcessDefinition:
        """Convert Plutus function declaration to Runa."""
        # Convert parameters
        runa_params = []
        for i, param in enumerate(decl.parameters):
            runa_params.append(Parameter(
                name=param,
                parameter_type=self.convert_type(decl.type_signature) if decl.type_signature else None,
                default_value=None
            ))
        
        # Convert body
        runa_body = self.convert_expression(decl.body)
        
        # Convert type signature
        runa_return_type = None
        if decl.type_signature and isinstance(decl.type_signature, PlutusFunctionType):
            runa_return_type = self.convert_type(decl.type_signature.codomain)
        
        return ProcessDefinition(
            name=decl.name,
            parameters=runa_params,
            return_type=runa_return_type,
            body=runa_body,
            decorators=[],
            metadata={
                "source_language": "plutus",
                "haskell_signature": str(decl.type_signature) if decl.type_signature else None,
                "where_clause": str(decl.where_clause) if decl.where_clause else None
            }
        )
    
    def convert_value_declaration(self, decl: PlutusValueDeclaration) -> LetStatement:
        """Convert Plutus value declaration to Runa."""
        return LetStatement(
            name=decl.name,
            value_type=self.convert_type(decl.type_signature) if decl.type_signature else None,
            initial_value=self.convert_expression(decl.expression),
            is_constant=True,
            metadata={"source_language": "plutus"}
        )
    
    def convert_data_declaration(self, decl: PlutusDataDeclaration) -> RunaStructDeclaration:
        """Convert Plutus data declaration to Runa struct."""
        # Create base struct for the data type
        fields = []
        
        # Handle algebraic data types with multiple constructors
        if len(decl.constructors) == 1:
            # Single constructor - convert to struct
            constructor = decl.constructors[0]
            for i, field_type in enumerate(constructor.fields):
                fields.append(RunaStructField(
                    name=f"field_{i}",
                    field_type=self.convert_type(field_type),
                    default_value=None
                ))
        else:
            # Multiple constructors - convert to tagged union
            for constructor in decl.constructors:
                fields.append(RunaStructField(
                    name=constructor.name.lower(),
                    field_type=BasicType(
                        name="Optional",
                        type_args=[self.convert_constructor_to_type(constructor)]
                    ),
                    default_value=None
                ))
        
        return RunaStructDeclaration(
            name=decl.name,
            fields=fields,
            methods=[],
            decorators=[],
            metadata={
                "source_language": "plutus",
                "algebraic_data_type": True,
                "constructors": [c.name for c in decl.constructors],
                "deriving": decl.deriving,
                "type_parameters": decl.type_parameters
            }
        )
    
    def convert_validator(self, validator: PlutusValidator) -> ProcessDefinition:
        """Convert Plutus validator to Runa function."""
        # Create validator function parameters
        runa_params = [
            Parameter(name="datum", parameter_type=BasicType(name="Any")),
            Parameter(name="redeemer", parameter_type=BasicType(name="Any")),
            Parameter(name="script_context", parameter_type=BasicType(name="ScriptContext"))
        ]
        
        # Add custom parameters
        for param in validator.parameters:
            runa_params.append(Parameter(
                name=param,
                parameter_type=BasicType(name="Any")
            ))
        
        return ProcessDefinition(
            name=validator.name,
            parameters=runa_params,
            return_type=BasicType(name="Boolean"),
            body=self.convert_expression(validator.body),
            decorators=[RunaDecorator(name="validator", arguments=[])],
            metadata={
                "source_language": "plutus",
                "validator_type": validator.validator_type,
                "cardano_validator": True
            }
        )
    
    def convert_minting_policy(self, policy: PlutusMintingPolicy) -> ProcessDefinition:
        """Convert Plutus minting policy to Runa function."""
        runa_params = [
            Parameter(name="redeemer", parameter_type=BasicType(name="Any")),
            Parameter(name="script_context", parameter_type=BasicType(name="ScriptContext"))
        ]
        
        # Add custom parameters
        for param in policy.parameters:
            runa_params.append(Parameter(
                name=param,
                parameter_type=BasicType(name="Any")
            ))
        
        return ProcessDefinition(
            name=policy.name,
            parameters=runa_params,
            return_type=BasicType(name="Boolean"),
            body=self.convert_expression(policy.body),
            decorators=[RunaDecorator(name="minting_policy", arguments=[])],
            metadata={
                "source_language": "plutus",
                "minting_policy": True
            }
        )
    
    def convert_newtype_declaration(self, decl: PlutusNewtypeDeclaration) -> BasicTypeAlias:
        """Convert Plutus newtype to Runa type alias."""
        base_type = self.convert_constructor_to_type(decl.constructor)
        
        return BasicTypeAlias(
            name=decl.name,
            aliased_type=base_type,
            metadata={
                "source_language": "plutus",
                "newtype": True,
                "deriving": decl.deriving
            }
        )
    
    def convert_expression(self, expr: PlutusExpression) -> Optional[Expression]:
        """Convert Plutus expression to Runa expression."""
        if isinstance(expr, PlutusLiteral):
            return self.convert_literal(expr)
        elif isinstance(expr, PlutusVariableReference):
            return self.convert_variable_reference(expr)
        elif isinstance(expr, PlutusApplication):
            return self.convert_application(expr)
        elif isinstance(expr, PlutusLambdaExpression):
            return self.convert_lambda(expr)
        elif isinstance(expr, PlutusLetBinding):
            return self.convert_let_binding(expr)
        elif isinstance(expr, PlutusCaseExpression):
            return self.convert_case_expression(expr)
        elif isinstance(expr, PlutusIfExpression):
            return self.convert_if_expression(expr)
        elif isinstance(expr, PlutusBuiltinFunction):
            return self.convert_builtin_function(expr)
        elif isinstance(expr, PlutusDoNotation):
            return self.convert_do_notation(expr)
        else:
            return None
    
    def convert_literal(self, literal: PlutusLiteral) -> StringLiteral:
        """Convert Plutus literal to Runa literal."""
        if literal.literal_type == "integer":
            return StringLiteral(value=literal.value, literal_type=StringLiteralType.INTEGER)
        elif literal.literal_type == "rational":
            return StringLiteral(value=literal.value, literal_type=StringLiteralType.FLOAT)
        elif literal.literal_type == "string":
            return StringLiteral(value=literal.value, literal_type=StringLiteralType.STRING)
        elif literal.literal_type == "char":
            return StringLiteral(value=literal.value, literal_type=StringLiteralType.STRING)
        else:
            return StringLiteral(value=literal.value, literal_type=StringLiteralType.STRING)
    
    def convert_variable_reference(self, var_ref: PlutusVariableReference) -> Identifier:
        """Convert Plutus variable reference to Runa identifier."""
        return Identifier(
            name=var_ref.name,
            metadata={"qualified": var_ref.qualified}
        )
    
    def convert_application(self, app: PlutusApplication) -> FunctionCall:
        """Convert Plutus function application to Runa function call."""
        function_expr = self.convert_expression(app.function)
        
        # Convert arguments
        runa_args = []
        for arg in app.arguments:
            runa_arg = self.convert_expression(arg)
            if runa_arg:
                runa_args.append(runa_arg)
        
        return FunctionCall(
            function=function_expr,
            arguments=runa_args,
            metadata={"source_language": "plutus"}
        )
    
    def convert_lambda(self, lambda_expr: PlutusLambdaExpression) -> ProcessDefinitionExpression:
        """Convert Plutus lambda to Runa lambda."""
        # Convert parameters
        runa_params = []
        for param in lambda_expr.parameters:
            runa_params.append(Parameter(
                name=param,
                parameter_type=None  # Haskell has type inference
            ))
        
        runa_body = self.convert_expression(lambda_expr.body)
        
        return ProcessDefinitionExpression(
            parameters=runa_params,
            body=runa_body,
            metadata={"source_language": "plutus"}
        )
    
    def convert_let_binding(self, let_expr: PlutusLetBinding) -> BlockExpression:
        """Convert Plutus let binding to Runa block expression."""
        statements = []
        
        # Convert bindings to variable declarations
        for binding in let_expr.bindings:
            var_decl = LetStatement(
                name=binding.name,
                value_type=self.convert_type(binding.type_signature) if binding.type_signature else None,
                initial_value=self.convert_expression(binding.expression),
                is_constant=True
            )
            statements.append(var_decl)
        
        # Convert final expression
        final_expr = self.convert_expression(let_expr.expression)
        if final_expr:
            statements.append(ReturnStatementStatement(value=final_expr))
        
        return BlockExpression(
            statements=statements,
            metadata={"source_language": "plutus", "let_binding": True}
        )
    
    def convert_case_expression(self, case_expr: PlutusCaseExpression) -> RunaMatchExpression:
        """Convert Plutus case expression to Runa match expression."""
        value = self.convert_expression(case_expr.expression)
        
        # Convert alternatives to match arms
        arms = []
        for alt in case_expr.alternatives:
            pattern = self.convert_pattern(alt.pattern)
            guard = None
            body = self.convert_expression(alt.expression)
            
            if pattern and body:
                arms.append(RunaMatchArm(
                    pattern=pattern,
                    guard=guard,
                    body=body
                ))
        
        return RunaMatchExpression(
            value=value,
            arms=arms,
            metadata={"source_language": "plutus"}
        )
    
    def convert_if_expression(self, if_expr: PlutusIfExpression) -> IfStatementExpression:
        """Convert Plutus if expression to Runa conditional."""
        condition = self.convert_expression(if_expr.condition)
        then_expr = self.convert_expression(if_expr.then_expression)
        else_expr = self.convert_expression(if_expr.else_expression)
        
        return IfStatementExpression(
            condition=condition,
            then_expression=then_expr,
            else_expression=else_expr,
            metadata={"source_language": "plutus"}
        )
    
    def convert_builtin_function(self, builtin: PlutusBuiltinFunction) -> FunctionCall:
        """Convert Plutus builtin function to Runa function call."""
        # Map Plutus builtins to Runa equivalents
        builtin_mapping = {
            'addInteger': 'add',
            'subtractInteger': 'subtract',
            'multiplyInteger': 'multiply',
            'divideInteger': 'divide',
            'equalsInteger': 'equals',
            'lessThanInteger': 'less_than',
            'appendByteString': 'concat',
            'sha2_256': 'sha256',
            'trace': 'debug_print',
            'ifThenElse': 'if_then_else',
        }
        
        runa_name = builtin_mapping.get(builtin.name, builtin.name)
        
        return FunctionCall(
            function=Identifier(name=runa_name),
            arguments=[],
            metadata={
                "source_language": "plutus",
                "plutus_builtin": builtin.name,
                "builtin_type": builtin.builtin_type
            }
        )
    
    def convert_do_notation(self, do_expr: PlutusDoNotation) -> BlockExpression:
        """Convert Plutus do notation to Runa block expression."""
        statements = []
        
        for stmt in do_expr.statements:
            if stmt.statement_type == "bind":
                # Convert monadic bind to assignment
                if hasattr(stmt.content, 'variable') and hasattr(stmt.content, 'expression'):
                    var_decl = LetStatement(
                        name=stmt.content.variable,
                        initial_value=self.convert_expression(stmt.content.expression),
                        is_constant=False
                    )
                    statements.append(var_decl)
            elif stmt.statement_type == "let":
                # Convert let statement
                if hasattr(stmt.content, 'bindings'):
                    for binding in stmt.content.bindings:
                        var_decl = LetStatement(
                            name=binding.name,
                            initial_value=self.convert_expression(binding.expression),
                            is_constant=True
                        )
                        statements.append(var_decl)
            elif stmt.statement_type == "expression":
                # Convert expression statement
                expr = self.convert_expression(stmt.content)
                if expr:
                    statements.append(ExpressionStatement(expression=expr))
        
        return BlockExpression(
            statements=statements,
            metadata={"source_language": "plutus", "do_notation": True}
        )
    
    def convert_pattern(self, pattern: PlutusPattern) -> Optional[Pattern]:
        """Convert Plutus pattern to Runa pattern."""
        if isinstance(pattern, PlutusVariablePattern):
            if pattern.name == "_":
                return WildcardPattern()
            else:
                return RunaVariablePattern(name=pattern.name)
        elif isinstance(pattern, PlutusConstructorPattern):
            sub_patterns = []
            for sub_pat in pattern.patterns:
                runa_sub_pat = self.convert_pattern(sub_pat)
                if runa_sub_pat:
                    sub_patterns.append(runa_sub_pat)
            
            return RunaConstructorPattern(
                constructor=pattern.constructor,
                patterns=sub_patterns
            )
        elif isinstance(pattern, PlutusLiteralPattern):
            return StringLiteralPattern(
                value=pattern.value,
                literal_type=self.map_literal_type(pattern.literal_type)
            )
        else:
            return None
    
    def convert_type(self, plutus_type: Optional[PlutusType]) -> Optional[BasicType]:
        """Convert Plutus type to Runa type."""
        if not plutus_type:
            return None
        
        if isinstance(plutus_type, PlutusTypeConstructor):
            # Map Haskell/Plutus types to Runa types
            type_mapping = {
                'Integer': 'Integer',
                'Bool': 'Boolean',
                'String': 'String',
                'ByteString': 'Bytes',
                'Data': 'Any',
                'ScriptContext': 'ScriptContext',
                'Value': 'Value',
                'Address': 'Address',
                'TxOut': 'TransactionOutput',
                'TxInfo': 'TransactionInfo',
                'Maybe': 'Optional',
                'Either': 'Result',
                '[]': 'List',
                '()': 'Unit'
            }
            
            runa_name = type_mapping.get(plutus_type.name, plutus_type.name)
            
            # Convert type arguments
            type_args = []
            for arg in plutus_type.arguments:
                runa_arg = self.convert_type(arg)
                if runa_arg:
                    type_args.append(runa_arg)
            
            return BasicType(name=runa_name, type_args=type_args)
        
        elif isinstance(plutus_type, PlutusTypeVariable):
            return BasicType(name=plutus_type.name, is_generic=True)
        
        elif isinstance(plutus_type, PlutusFunctionType):
            # Convert function type to Runa function type
            domain = self.convert_type(plutus_type.domain)
            codomain = self.convert_type(plutus_type.codomain)
            
            return BasicType(
                name="Function",
                type_args=[domain, codomain] if domain and codomain else []
            )
        
        else:
            return BasicType(name="Any")
    
    def convert_constructor_to_type(self, constructor: PlutusConstructor) -> BasicType:
        """Convert Plutus constructor to Runa type."""
        if len(constructor.fields) == 0:
            return BasicType(name="Unit")
        elif len(constructor.fields) == 1:
            return self.convert_type(constructor.fields[0]) or BasicType(name="Any")
        else:
            # Multiple fields - convert to tuple
            field_types = []
            for field in constructor.fields:
                field_type = self.convert_type(field)
                if field_type:
                    field_types.append(field_type)
            
            return BasicType(name="Tuple", type_args=field_types)
    
    def map_literal_type(self, plutus_literal_type: str) -> StringLiteralType:
        """Map Plutus literal type to Runa literal type."""
        mapping = {
            'integer': StringLiteralType.INTEGER,
            'rational': StringLiteralType.FLOAT,
            'string': StringLiteralType.STRING,
            'char': StringLiteralType.STRING
        }
        return mapping.get(plutus_literal_type, StringLiteralType.STRING)


class RunaToPlutusConverter:
    """Converts Runa AST to Plutus AST."""
    
    def __init__(self):
        self.symbol_table = {}
        self.type_mappings = {}
        self.context_stack = []
    
    def convert_program(self, runa_program: Program) -> PlutusProgram:
        """Convert Runa program to Plutus program."""
        plutus_modules = []
        
        for module in runa_program.modules:
            plutus_module = self.convert_module(module)
            if plutus_module:
                plutus_modules.append(plutus_module)
        
        return PlutusProgram(modules=plutus_modules)
    
    def convert_module(self, runa_module: RunaModule) -> PlutusModule:
        """Convert Runa module to Plutus module."""
        # Convert imports
        plutus_imports = []
        for imp in runa_module.imports:
            plutus_import = self.convert_import(imp)
            if plutus_import:
                plutus_imports.append(plutus_import)
        
        # Convert declarations
        plutus_declarations = []
        for decl in runa_module.declarations:
            plutus_decl = self.convert_declaration(decl)
            if plutus_decl:
                plutus_declarations.append(plutus_decl)
        
        # Create default exports
        exports = []
        for decl in plutus_declarations:
            exports.append(PlutusExport(name=decl.name))
        
        return PlutusModule(
            name=runa_module.name,
            imports=plutus_imports,
            exports=exports,
            declarations=plutus_declarations
        )
    
    def convert_import(self, runa_import: RunaImport) -> PlutusImport:
        """Convert Runa import to Plutus import."""
        module_name = runa_import.module_path.replace('/', '.')
        
        return PlutusImport(
            module_name=module_name,
            qualified=runa_import.metadata.get("qualified", False),
            alias=runa_import.alias,
            imports=runa_import.imports
        )
    
    def convert_declaration(self, decl: Declaration) -> Optional[PlutusDeclaration]:
        """Convert Runa declaration to Plutus declaration."""
        if isinstance(decl, ProcessDefinition):
            # Check if it's a validator or minting policy
            if any(d.name == "validator" for d in decl.decorators):
                return self.convert_to_validator(decl)
            elif any(d.name == "minting_policy" for d in decl.decorators):
                return self.convert_to_minting_policy(decl)
            else:
                return self.convert_function_declaration(decl)
        elif isinstance(decl, LetStatement):
            return self.convert_value_declaration(decl)
        elif isinstance(decl, RunaStructDeclaration):
            return self.convert_struct_declaration(decl)
        elif isinstance(decl, BasicTypeAlias):
            return self.convert_type_alias(decl)
        else:
            return None
    
    def convert_function_declaration(self, decl: ProcessDefinition) -> PlutusFunctionDeclaration:
        """Convert Runa function declaration to Plutus."""
        # Extract parameter names
        param_names = [param.name for param in decl.parameters]
        
        # Convert body
        plutus_body = self.convert_expression(decl.body)
        
        # Convert type signature
        plutus_type = self.convert_function_type(decl.parameters, decl.return_type)
        
        return PlutusFunctionDeclaration(
            name=decl.name,
            parameters=param_names,
            type_signature=plutus_type,
            body=plutus_body
        )
    
    def convert_to_validator(self, decl: ProcessDefinition) -> PlutusValidator:
        """Convert Runa function to Plutus validator."""
        # Extract non-standard parameters (beyond datum, redeemer, script_context)
        custom_params = []
        for param in decl.parameters:
            if param.name not in ['datum', 'redeemer', 'script_context']:
                custom_params.append(param.name)
        
        return PlutusValidator(
            name=decl.name,
            validator_type="spending",
            parameters=custom_params,
            body=self.convert_expression(decl.body)
        )
    
    def convert_to_minting_policy(self, decl: ProcessDefinition) -> PlutusMintingPolicy:
        """Convert Runa function to Plutus minting policy."""
        # Extract non-standard parameters (beyond redeemer, script_context)
        custom_params = []
        for param in decl.parameters:
            if param.name not in ['redeemer', 'script_context']:
                custom_params.append(param.name)
        
        return PlutusMintingPolicy(
            name=decl.name,
            parameters=custom_params,
            body=self.convert_expression(decl.body)
        )
    
    def convert_expression(self, expr: Optional[Expression]) -> Optional[PlutusExpression]:
        """Convert Runa expression to Plutus expression."""
        if not expr:
            return None
        
        if isinstance(expr, StringLiteral):
            return self.convert_literal(expr)
        elif isinstance(expr, Identifier):
            return self.convert_identifier(expr)
        elif isinstance(expr, FunctionCall):
            return self.convert_function_call(expr)
        elif isinstance(expr, ProcessDefinitionExpression):
            return self.convert_lambda_expression(expr)
        elif isinstance(expr, BlockExpression):
            return self.convert_block_expression(expr)
        elif isinstance(expr, RunaMatchExpression):
            return self.convert_match_expression(expr)
        elif isinstance(expr, IfStatementExpression):
            return self.convert_conditional_expression(expr)
        else:
            return None
    
    def convert_literal(self, literal: StringLiteral) -> PlutusLiteral:
        """Convert Runa literal to Plutus literal."""
        if literal.literal_type == StringLiteralType.INTEGER:
            return PlutusLiteral(value=literal.value, literal_type="integer")
        elif literal.literal_type == StringLiteralType.FLOAT:
            return PlutusLiteral(value=literal.value, literal_type="rational")
        elif literal.literal_type == StringLiteralType.STRING:
            return PlutusLiteral(value=literal.value, literal_type="string")
        elif literal.literal_type == StringLiteralType.BOOLEAN:
            return PlutusVariableReference(name="True" if literal.value else "False")
        else:
            return PlutusLiteral(value=literal.value, literal_type="string")
    
    def convert_identifier(self, identifier: Identifier) -> PlutusVariableReference:
        """Convert Runa identifier to Plutus variable reference."""
        return PlutusVariableReference(
            name=identifier.name,
            qualified=identifier.metadata.get("qualified", False)
        )
    
    def convert_function_call(self, call: FunctionCall) -> PlutusApplication:
        """Convert Runa function call to Plutus application."""
        function = self.convert_expression(call.function)
        
        # Convert arguments
        plutus_args = []
        for arg in call.arguments:
            plutus_arg = self.convert_expression(arg)
            if plutus_arg:
                plutus_args.append(plutus_arg)
        
        return PlutusApplication(function=function, arguments=plutus_args)
    
    def convert_lambda_expression(self, lambda_expr: ProcessDefinitionExpression) -> PlutusLambdaExpression:
        """Convert Runa lambda to Plutus lambda."""
        param_names = [param.name for param in lambda_expr.parameters]
        plutus_body = self.convert_expression(lambda_expr.body)
        
        return PlutusLambdaExpression(parameters=param_names, body=plutus_body)
    
    def convert_block_expression(self, block: BlockExpression) -> PlutusLetBinding:
        """Convert Runa block expression to Plutus let binding."""
        bindings = []
        final_expr = None
        
        for stmt in block.statements:
            if isinstance(stmt, LetStatement):
                binding = PlutusBinding(
                    name=stmt.name,
                    expression=self.convert_expression(stmt.initial_value),
                    type_signature=self.convert_type(stmt.value_type)
                )
                bindings.append(binding)
            elif isinstance(stmt, ReturnStatementStatement):
                final_expr = self.convert_expression(stmt.value)
            elif isinstance(stmt, ExpressionStatement):
                # Last expression becomes the final expression
                final_expr = self.convert_expression(stmt.expression)
        
        if not final_expr:
            # Default return value
            final_expr = PlutusVariableReference(name="()")
        
        return PlutusLetBinding(bindings=bindings, expression=final_expr)
    
    def convert_match_expression(self, match_expr: RunaMatchExpression) -> PlutusCaseExpression:
        """Convert Runa match expression to Plutus case expression."""
        expr = self.convert_expression(match_expr.value)
        
        alternatives = []
        for arm in match_expr.arms:
            pattern = self.convert_pattern(arm.pattern)
            body = self.convert_expression(arm.body)
            
            if pattern and body:
                alternatives.append(PlutusAlternative(pattern=pattern, expression=body))
        
        return PlutusCaseExpression(expression=expr, alternatives=alternatives)
    
    def convert_conditional_expression(self, cond_expr: IfStatementExpression) -> PlutusIfExpression:
        """Convert Runa conditional to Plutus if expression."""
        condition = self.convert_expression(cond_expr.condition)
        then_expr = self.convert_expression(cond_expr.then_expression)
        else_expr = self.convert_expression(cond_expr.else_expression)
        
        return PlutusIfExpression(
            condition=condition,
            then_expression=then_expr,
            else_expression=else_expr
        )
    
    def convert_pattern(self, pattern: Pattern) -> Optional[PlutusPattern]:
        """Convert Runa pattern to Plutus pattern."""
        if isinstance(pattern, RunaVariablePattern):
            return PlutusVariablePattern(name=pattern.name)
        elif isinstance(pattern, WildcardPattern):
            return PlutusVariablePattern(name="_")
        elif isinstance(pattern, RunaConstructorPattern):
            sub_patterns = []
            for sub_pat in pattern.patterns:
                plutus_sub_pat = self.convert_pattern(sub_pat)
                if plutus_sub_pat:
                    sub_patterns.append(plutus_sub_pat)
            
            return PlutusConstructorPattern(
                constructor=pattern.constructor,
                patterns=sub_patterns
            )
        elif isinstance(pattern, StringLiteralPattern):
            return PlutusLiteralPattern(
                value=pattern.value,
                literal_type=self.map_runa_literal_type(pattern.literal_type)
            )
        else:
            return None
    
    def convert_type(self, runa_type: Optional[BasicType]) -> Optional[PlutusType]:
        """Convert Runa type to Plutus type."""
        if not runa_type:
            return None
        
        # Map Runa types to Haskell/Plutus types
        type_mapping = {
            'Integer': 'Integer',
            'Boolean': 'Bool',
            'String': 'String',
            'Bytes': 'ByteString',
            'Any': 'Data',
            'ScriptContext': 'ScriptContext',
            'Value': 'Value',
            'Address': 'Address',
            'TransactionOutput': 'TxOut',
            'TransactionInfo': 'TxInfo',
            'Optional': 'Maybe',
            'Result': 'Either',
            'List': '[]',
            'Unit': '()'
        }
        
        plutus_name = type_mapping.get(runa_type.name, runa_type.name)
        
        if runa_type.is_generic:
            return PlutusTypeVariable(name=plutus_name)
        else:
            # Convert type arguments
            type_args = []
            for arg in runa_type.type_args:
                plutus_arg = self.convert_type(arg)
                if plutus_arg:
                    type_args.append(plutus_arg)
            
            return PlutusTypeConstructor(name=plutus_name, arguments=type_args)
    
    def convert_function_type(self, parameters: List[Parameter], return_type: Optional[BasicType]) -> Optional[PlutusType]:
        """Convert function signature to Plutus function type."""
        if not parameters and not return_type:
            return None
        
        # Build function type from right to left
        current_type = self.convert_type(return_type) if return_type else PlutusTypeConstructor(name="()")
        
        # Add parameter types
        for param in reversed(parameters):
            param_type = self.convert_type(param.parameter_type) if param.parameter_type else PlutusTypeConstructor(name="Data")
            current_type = PlutusFunctionType(domain=param_type, codomain=current_type)
        
        return current_type
    
    def map_runa_literal_type(self, runa_literal_type: StringLiteralType) -> str:
        """Map Runa literal type to Plutus literal type."""
        mapping = {
            StringLiteralType.INTEGER: 'integer',
            StringLiteralType.FLOAT: 'rational',
            StringLiteralType.STRING: 'string',
            StringLiteralType.BOOLEAN: 'bool'
        }
        return mapping.get(runa_literal_type, 'string')


def plutus_to_runa(plutus_ast: PlutusProgram) -> Program:
    """Convert Plutus AST to Runa AST."""
    converter = PlutusToRunaConverter()
    return converter.convert_program(plutus_ast)


def runa_to_plutus(runa_ast: Program) -> PlutusProgram:
    """Convert Runa AST to Plutus AST."""
    converter = RunaToPlutusConverter()
    return converter.convert_program(runa_ast) 