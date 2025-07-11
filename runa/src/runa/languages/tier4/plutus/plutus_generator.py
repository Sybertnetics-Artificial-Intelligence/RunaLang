#!/usr/bin/env python3
"""
Plutus Code Generator

Generates idiomatic Haskell-based Plutus smart contract code from AST.
Supports UPLC compilation targets, Cardano-specific constructs, and functional programming patterns.
"""

from typing import List, Optional, Dict, Any, Set
from io import StringIO
from .plutus_ast import *


class PlutusCodeStyle:
    """Configuration for Plutus code style."""
    
    def __init__(self):
        self.indent_size = 2
        self.use_spaces = True
        self.max_line_length = 100
        self.function_style = "haskell"  # haskell, pointfree
        self.type_annotations = True
        self.pragma_style = "modern"
        self.import_style = "qualified"
        self.comment_style = "haddock"


class PlutusFormatter:
    """Formats Plutus code according to style guidelines."""
    
    def __init__(self, style: PlutusCodeStyle):
        self.style = style
        self.indent_level = 0
        self.output = StringIO()
        self.line_start = True
    
    def write(self, text: str) -> None:
        """Write text to output."""
        if self.line_start and text.strip():
            self.output.write(" " * (self.indent_level * self.style.indent_size))
            self.line_start = False
        self.output.write(text)
    
    def write_line(self, text: str = "") -> None:
        """Write line with newline."""
        if text:
            self.write(text)
        self.output.write("\n")
        self.line_start = True
    
    def indent(self) -> None:
        """Increase indentation level."""
        self.indent_level += 1
    
    def dedent(self) -> None:
        """Decrease indentation level."""
        if self.indent_level > 0:
            self.indent_level -= 1
    
    def get_output(self) -> str:
        """Get formatted output."""
        return self.output.getvalue()


class PlutusCodeGenerator:
    """Generates Plutus smart contract code from AST."""
    
    def __init__(self, style: PlutusCodeStyle = None):
        self.style = style or PlutusCodeStyle()
        self.formatter = PlutusFormatter(self.style)
        self.symbol_table = {}
        self.imports_needed = set()
        self.language_extensions = set()
        self.current_module = None
    
    def generate_program(self, program: PlutusProgram) -> str:
        """Generate complete Plutus program."""
        self.formatter = PlutusFormatter(self.style)
        
        for module in program.modules:
            self.generate_module(module)
            self.formatter.write_line()
        
        return self.formatter.get_output()
    
    def generate_module(self, module: PlutusModule) -> None:
        """Generate Plutus module."""
        self.current_module = module
        
        # Generate language pragmas
        self.generate_language_pragmas()
        
        # Generate module header
        self.generate_module_header(module)
        
        # Generate imports
        self.generate_imports(module)
        
        # Generate declarations
        for decl in module.declarations:
            self.generate_declaration(decl)
            self.formatter.write_line()
    
    def generate_language_pragmas(self) -> None:
        """Generate language extension pragmas."""
        default_extensions = {
            "DataKinds",
            "DeriveAnyClass",
            "DeriveGeneric",
            "DerivingStrategies",
            "ExplicitForAll",
            "GeneralizedNewtypeDeriving",
            "ImportQualifiedPost",
            "MultiParamTypeClasses",
            "NamedFieldPuns",
            "NoImplicitPrelude",
            "OverloadedStrings",
            "RecordWildCards",
            "ScopedTypeVariables",
            "Strict",
            "TemplateHaskell",
            "TypeApplications",
            "TypeFamilies",
            "TypeOperators"
        }
        
        extensions = default_extensions.union(self.language_extensions)
        
        for extension in sorted(extensions):
            self.formatter.write_line(f"{{-# LANGUAGE {extension} #-}}")
        
        if extensions:
            self.formatter.write_line()
    
    def generate_module_header(self, module: PlutusModule) -> None:
        """Generate module header with exports."""
        self.formatter.write(f"module {module.name}")
        
        if module.exports:
            self.formatter.write_line(" (")
            self.formatter.indent()
            
            for i, export in enumerate(module.exports):
                if i > 0:
                    self.formatter.write_line(",")
                self.formatter.write(f"  {export.name}")
            
            self.formatter.dedent()
            self.formatter.write_line()
            self.formatter.write_line(") where")
        else:
            self.formatter.write_line(" where")
        
        self.formatter.write_line()
    
    def generate_imports(self, module: PlutusModule) -> None:
        """Generate import statements."""
        # Standard Plutus imports
        standard_imports = [
            "import PlutusTx",
            "import PlutusTx.Prelude hiding (Semigroup(..), unless)",
            "import Ledger",
            "import Ledger.Constraints as Constraints",
            "import Ledger.Scripts",
            "import Ledger.Typed.Scripts",
            "import Playground.Contract (printJson, printSchemas, ensureKnownCurrencies, stage)",
            "import Playground.TH (mkKnownCurrencies, mkSchemaDefinitions)",
            "import Playground.Types (KnownCurrency (..))",
            "import Prelude (IO, Semigroup (..), String)",
            "import Text.Printf (printf)"
        ]
        
        # Generate standard imports
        for imp in standard_imports:
            self.formatter.write_line(imp)
        
        if standard_imports:
            self.formatter.write_line()
        
        # Generate user imports
        for imp in module.imports:
            self.generate_import(imp)
        
        if module.imports:
            self.formatter.write_line()
    
    def generate_import(self, imp: PlutusImport) -> None:
        """Generate single import statement."""
        import_line = "import"
        
        if imp.qualified:
            import_line += " qualified"
        
        import_line += f" {imp.module_name}"
        
        if imp.alias:
            import_line += f" as {imp.alias}"
        
        if imp.imports:
            import_line += " ("
            import_line += ", ".join(imp.imports)
            import_line += ")"
        
        self.formatter.write_line(import_line)
    
    def generate_declaration(self, decl: PlutusDeclaration) -> None:
        """Generate declaration."""
        if isinstance(decl, PlutusFunctionDeclaration):
            self.generate_function_declaration(decl)
        elif isinstance(decl, PlutusValueDeclaration):
            self.generate_value_declaration(decl)
        elif isinstance(decl, PlutusDataDeclaration):
            self.generate_data_declaration(decl)
        elif isinstance(decl, PlutusNewtypeDeclaration):
            self.generate_newtype_declaration(decl)
        elif isinstance(decl, PlutusValidator):
            self.generate_validator(decl)
        elif isinstance(decl, PlutusMintingPolicy):
            self.generate_minting_policy(decl)
    
    def generate_function_declaration(self, decl: PlutusFunctionDeclaration) -> None:
        """Generate function declaration."""
        # Generate type signature
        if decl.type_signature and self.style.type_annotations:
            self.formatter.write_line(f"{decl.name} :: {self.generate_type(decl.type_signature)}")
        
        # Generate function definition
        self.formatter.write(f"{decl.name}")
        
        if decl.parameters:
            for param in decl.parameters:
                self.formatter.write(f" {param}")
        
        self.formatter.write(" = ")
        
        if self.should_use_multiline(decl.body):
            self.formatter.write_line()
            self.formatter.indent()
            self.generate_expression(decl.body)
            self.formatter.dedent()
        else:
            self.generate_expression(decl.body)
        
        # Generate where clause if present
        if decl.where_clause:
            self.formatter.write_line()
            self.formatter.write_line("  where")
            self.formatter.indent()
            self.generate_where_clause(decl.where_clause)
            self.formatter.dedent()
    
    def generate_value_declaration(self, decl: PlutusValueDeclaration) -> None:
        """Generate value declaration."""
        # Generate type signature
        if decl.type_signature and self.style.type_annotations:
            self.formatter.write_line(f"{decl.name} :: {self.generate_type(decl.type_signature)}")
        
        # Generate value definition
        self.formatter.write(f"{decl.name} = ")
        self.generate_expression(decl.expression)
    
    def generate_data_declaration(self, decl: PlutusDataDeclaration) -> None:
        """Generate data type declaration."""
        self.formatter.write("data ")
        self.formatter.write(decl.name)
        
        # Type parameters
        if decl.type_parameters:
            for param in decl.type_parameters:
                self.formatter.write(f" {param}")
        
        self.formatter.write(" =")
        
        # Constructors
        if len(decl.constructors) == 1:
            # Single constructor on same line
            self.formatter.write(" ")
            self.generate_constructor(decl.constructors[0])
        else:
            # Multiple constructors, each on new line
            self.formatter.write_line()
            self.formatter.indent()
            
            for i, constructor in enumerate(decl.constructors):
                if i > 0:
                    self.formatter.write_line()
                    self.formatter.write("| ")
                else:
                    self.formatter.write("  ")
                self.generate_constructor(constructor)
            
            self.formatter.dedent()
        
        # Deriving clause
        if decl.deriving:
            self.formatter.write_line()
            self.formatter.write("  deriving (")
            self.formatter.write(", ".join(decl.deriving))
            self.formatter.write(")")
        
        # Add PlutusTx instances
        self.formatter.write_line()
        self.formatter.write_line(f"PlutusTx.unstableMakeIsData ''{decl.name}")
    
    def generate_constructor(self, constructor: PlutusConstructor) -> None:
        """Generate data constructor."""
        self.formatter.write(constructor.name)
        
        for field in constructor.fields:
            self.formatter.write(" ")
            if self.needs_parentheses_type(field):
                self.formatter.write("(")
                self.formatter.write(self.generate_type(field))
                self.formatter.write(")")
            else:
                self.formatter.write(self.generate_type(field))
    
    def generate_newtype_declaration(self, decl: PlutusNewtypeDeclaration) -> None:
        """Generate newtype declaration."""
        self.formatter.write("newtype ")
        self.formatter.write(decl.name)
        
        # Type parameters
        if decl.type_parameters:
            for param in decl.type_parameters:
                self.formatter.write(f" {param}")
        
        self.formatter.write(" = ")
        self.generate_constructor(decl.constructor)
        
        # Deriving clause
        if decl.deriving:
            self.formatter.write_line()
            self.formatter.write("  deriving (")
            self.formatter.write(", ".join(decl.deriving))
            self.formatter.write(")")
    
    def generate_validator(self, validator: PlutusValidator) -> None:
        """Generate Plutus validator."""
        # Generate validator function
        self.formatter.write_line(f"{{-# INLINABLE {validator.name} #-}}")
        
        if self.style.type_annotations:
            self.formatter.write_line(f"{validator.name} :: BuiltinData -> BuiltinData -> BuiltinData -> ()")
        
        self.formatter.write(f"{validator.name} datum redeemer ctx")
        
        # Add custom parameters
        for param in validator.parameters:
            self.formatter.write(f" {param}")
        
        self.formatter.write(" = ")
        
        if self.should_use_multiline(validator.body):
            self.formatter.write_line()
            self.formatter.indent()
            self.generate_expression(validator.body)
            self.formatter.dedent()
        else:
            self.generate_expression(validator.body)
        
        self.formatter.write_line()
        self.formatter.write_line()
        
        # Generate validator script
        validator_script_name = f"{validator.name}Script"
        self.formatter.write_line(f"{validator_script_name} :: Validator")
        self.formatter.write_line(f"{validator_script_name} = mkValidatorScript $$(PlutusTx.compile [|| {validator.name} ||])")
        
        self.formatter.write_line()
        
        # Generate validator address
        address_name = f"{validator.name}Address"
        self.formatter.write_line(f"{address_name} :: Ledger.Address")
        self.formatter.write_line(f"{address_name} = scriptAddress {validator_script_name}")
    
    def generate_minting_policy(self, policy: PlutusMintingPolicy) -> None:
        """Generate Plutus minting policy."""
        # Generate policy function
        self.formatter.write_line(f"{{-# INLINABLE {policy.name} #-}}")
        
        if self.style.type_annotations:
            self.formatter.write_line(f"{policy.name} :: BuiltinData -> BuiltinData -> ()")
        
        self.formatter.write(f"{policy.name} redeemer ctx")
        
        # Add custom parameters
        for param in policy.parameters:
            self.formatter.write(f" {param}")
        
        self.formatter.write(" = ")
        
        if self.should_use_multiline(policy.body):
            self.formatter.write_line()
            self.formatter.indent()
            self.generate_expression(policy.body)
            self.formatter.dedent()
        else:
            self.generate_expression(policy.body)
        
        self.formatter.write_line()
        self.formatter.write_line()
        
        # Generate minting policy script
        policy_script_name = f"{policy.name}Script"
        self.formatter.write_line(f"{policy_script_name} :: MintingPolicy")
        self.formatter.write_line(f"{policy_script_name} = mkMintingPolicyScript $$(PlutusTx.compile [|| {policy.name} ||])")
        
        self.formatter.write_line()
        
        # Generate currency symbol
        symbol_name = f"{policy.name}Symbol"
        self.formatter.write_line(f"{symbol_name} :: CurrencySymbol")
        self.formatter.write_line(f"{symbol_name} = scriptCurrencySymbol {policy_script_name}")
    
    def generate_expression(self, expr: PlutusExpression) -> None:
        """Generate expression."""
        if isinstance(expr, PlutusLiteral):
            self.generate_literal(expr)
        elif isinstance(expr, PlutusVariableReference):
            self.generate_variable_reference(expr)
        elif isinstance(expr, PlutusApplication):
            self.generate_application(expr)
        elif isinstance(expr, PlutusLambdaExpression):
            self.generate_lambda_expression(expr)
        elif isinstance(expr, PlutusLetBinding):
            self.generate_let_binding(expr)
        elif isinstance(expr, PlutusCaseExpression):
            self.generate_case_expression(expr)
        elif isinstance(expr, PlutusIfExpression):
            self.generate_if_expression(expr)
        elif isinstance(expr, PlutusBuiltinFunction):
            self.generate_builtin_function(expr)
        elif isinstance(expr, PlutusDoNotation):
            self.generate_do_notation(expr)
        else:
            self.formatter.write("()")  # Default fallback
    
    def generate_literal(self, literal: PlutusLiteral) -> None:
        """Generate literal value."""
        if literal.literal_type == "integer":
            self.formatter.write(str(literal.value))
        elif literal.literal_type == "rational":
            self.formatter.write(str(literal.value))
        elif literal.literal_type == "string":
            escaped = literal.value.replace("\\", "\\\\").replace('"', '\\"')
            self.formatter.write(f'"{escaped}"')
        elif literal.literal_type == "char":
            escaped = literal.value.replace("\\", "\\\\").replace("'", "\\'")
            self.formatter.write(f"'{escaped}'")
        else:
            self.formatter.write(str(literal.value))
    
    def generate_variable_reference(self, var_ref: PlutusVariableReference) -> None:
        """Generate variable reference."""
        if var_ref.qualified:
            self.formatter.write(var_ref.name)
        else:
            self.formatter.write(var_ref.name)
    
    def generate_application(self, app: PlutusApplication) -> None:
        """Generate function application."""
        # Check if we need parentheses
        needs_parens = self.needs_parentheses_expr(app.function)
        
        if needs_parens:
            self.formatter.write("(")
        
        self.generate_expression(app.function)
        
        if needs_parens:
            self.formatter.write(")")
        
        # Generate arguments
        for arg in app.arguments:
            self.formatter.write(" ")
            
            arg_needs_parens = self.needs_parentheses_expr(arg)
            if arg_needs_parens:
                self.formatter.write("(")
            
            self.generate_expression(arg)
            
            if arg_needs_parens:
                self.formatter.write(")")
    
    def generate_lambda_expression(self, lambda_expr: PlutusLambdaExpression) -> None:
        """Generate lambda expression."""
        self.formatter.write("\\")
        
        for i, param in enumerate(lambda_expr.parameters):
            if i > 0:
                self.formatter.write(" ")
            self.formatter.write(param)
        
        self.formatter.write(" -> ")
        self.generate_expression(lambda_expr.body)
    
    def generate_let_binding(self, let_expr: PlutusLetBinding) -> None:
        """Generate let binding."""
        self.formatter.write("let")
        self.formatter.write_line()
        self.formatter.indent()
        
        # Generate bindings
        for i, binding in enumerate(let_expr.bindings):
            if i > 0:
                self.formatter.write_line()
            
            self.formatter.write(f"{binding.name}")
            
            if binding.type_signature and self.style.type_annotations:
                self.formatter.write(f" :: {self.generate_type(binding.type_signature)}")
                self.formatter.write_line()
                self.formatter.write(f"{binding.name}")
            
            self.formatter.write(" = ")
            self.generate_expression(binding.expression)
        
        self.formatter.dedent()
        self.formatter.write_line()
        self.formatter.write("in ")
        self.generate_expression(let_expr.expression)
    
    def generate_case_expression(self, case_expr: PlutusCaseExpression) -> None:
        """Generate case expression."""
        self.formatter.write("case ")
        self.generate_expression(case_expr.expression)
        self.formatter.write(" of")
        self.formatter.write_line()
        self.formatter.indent()
        
        for i, alt in enumerate(case_expr.alternatives):
            if i > 0:
                self.formatter.write_line()
            
            self.generate_pattern(alt.pattern)
            self.formatter.write(" -> ")
            
            if self.should_use_multiline(alt.expression):
                self.formatter.write_line()
                self.formatter.indent()
                self.generate_expression(alt.expression)
                self.formatter.dedent()
            else:
                self.generate_expression(alt.expression)
        
        self.formatter.dedent()
    
    def generate_if_expression(self, if_expr: PlutusIfExpression) -> None:
        """Generate if expression."""
        self.formatter.write("if ")
        self.generate_expression(if_expr.condition)
        self.formatter.write_line()
        self.formatter.write("then ")
        self.generate_expression(if_expr.then_expression)
        self.formatter.write_line()
        self.formatter.write("else ")
        self.generate_expression(if_expr.else_expression)
    
    def generate_builtin_function(self, builtin: PlutusBuiltinFunction) -> None:
        """Generate builtin function."""
        self.formatter.write(builtin.name)
    
    def generate_do_notation(self, do_expr: PlutusDoNotation) -> None:
        """Generate do notation."""
        self.formatter.write("do")
        self.formatter.write_line()
        self.formatter.indent()
        
        for i, stmt in enumerate(do_expr.statements):
            if i > 0:
                self.formatter.write_line()
            
            self.generate_do_statement(stmt)
        
        self.formatter.dedent()
    
    def generate_do_statement(self, stmt: PlutusDoStatement) -> None:
        """Generate do statement."""
        if stmt.statement_type == "bind":
            # Variable binding: var <- expr
            if hasattr(stmt.content, 'variable') and hasattr(stmt.content, 'expression'):
                self.formatter.write(f"{stmt.content.variable} <- ")
                self.generate_expression(stmt.content.expression)
        elif stmt.statement_type == "let":
            # Let binding: let var = expr
            self.formatter.write("let ")
            if hasattr(stmt.content, 'bindings'):
                for i, binding in enumerate(stmt.content.bindings):
                    if i > 0:
                        self.formatter.write_line()
                        self.formatter.write("    ")
                    self.formatter.write(f"{binding.name} = ")
                    self.generate_expression(binding.expression)
        elif stmt.statement_type == "expression":
            # Expression statement
            self.generate_expression(stmt.content)
    
    def generate_pattern(self, pattern: PlutusPattern) -> None:
        """Generate pattern."""
        if isinstance(pattern, PlutusVariablePattern):
            self.formatter.write(pattern.name)
        elif isinstance(pattern, PlutusConstructorPattern):
            self.formatter.write(pattern.constructor)
            for sub_pattern in pattern.patterns:
                self.formatter.write(" ")
                
                if self.needs_parentheses_pattern(sub_pattern):
                    self.formatter.write("(")
                    self.generate_pattern(sub_pattern)
                    self.formatter.write(")")
                else:
                    self.generate_pattern(sub_pattern)
        elif isinstance(pattern, PlutusLiteralPattern):
            if pattern.literal_type == "integer":
                self.formatter.write(str(pattern.value))
            elif pattern.literal_type == "string":
                escaped = pattern.value.replace("\\", "\\\\").replace('"', '\\"')
                self.formatter.write(f'"{escaped}"')
            else:
                self.formatter.write(str(pattern.value))
    
    def generate_type(self, plutus_type: PlutusType) -> str:
        """Generate type expression."""
        if isinstance(plutus_type, PlutusTypeConstructor):
            result = plutus_type.name
            if plutus_type.arguments:
                result += " " + " ".join(self.generate_type(arg) for arg in plutus_type.arguments)
            return result
        elif isinstance(plutus_type, PlutusTypeVariable):
            return plutus_type.name
        elif isinstance(plutus_type, PlutusFunctionType):
            domain = self.generate_type(plutus_type.domain)
            codomain = self.generate_type(plutus_type.codomain)
            
            # Add parentheses if needed
            if self.needs_parentheses_type(plutus_type.domain):
                domain = f"({domain})"
            
            return f"{domain} -> {codomain}"
        else:
            return "Data"  # Default fallback
    
    def generate_where_clause(self, where_clause: PlutusWhereClause) -> None:
        """Generate where clause."""
        for i, binding in enumerate(where_clause.bindings):
            if i > 0:
                self.formatter.write_line()
            
            self.formatter.write(f"{binding.name} = ")
            self.generate_expression(binding.expression)
    
    def should_use_multiline(self, expr: PlutusExpression) -> bool:
        """Determine if expression should use multiple lines."""
        if isinstance(expr, (PlutusLetBinding, PlutusCaseExpression, PlutusDoNotation)):
            return True
        elif isinstance(expr, PlutusIfExpression):
            return True
        elif isinstance(expr, PlutusLambdaExpression):
            return self.should_use_multiline(expr.body)
        else:
            return False
    
    def needs_parentheses_expr(self, expr: PlutusExpression) -> bool:
        """Determine if expression needs parentheses."""
        if isinstance(expr, (PlutusApplication, PlutusLambdaExpression)):
            return True
        elif isinstance(expr, (PlutusLetBinding, PlutusCaseExpression, PlutusIfExpression)):
            return True
        else:
            return False
    
    def needs_parentheses_pattern(self, pattern: PlutusPattern) -> bool:
        """Determine if pattern needs parentheses."""
        if isinstance(pattern, PlutusConstructorPattern):
            return len(pattern.patterns) > 0
        else:
            return False
    
    def needs_parentheses_type(self, plutus_type: PlutusType) -> bool:
        """Determine if type needs parentheses."""
        if isinstance(plutus_type, PlutusFunctionType):
            return True
        elif isinstance(plutus_type, PlutusTypeConstructor):
            return len(plutus_type.arguments) > 0
        else:
            return False


def generate_plutus(ast: PlutusProgram, style: PlutusCodeStyle = None) -> str:
    """Generate Plutus code from AST."""
    generator = PlutusCodeGenerator(style)
    return generator.generate_program(ast) 