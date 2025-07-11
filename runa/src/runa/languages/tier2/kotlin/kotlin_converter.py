#!/usr/bin/env python3
"""
Kotlin ↔ Runa Bidirectional Converter

Converts between Kotlin AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.

This module handles conversion between:
- Kotlin classes and objects ↔ Runa structures
- Kotlin functions and properties ↔ Runa processes and variables
- Kotlin coroutines ↔ Runa async constructs
- Kotlin null safety ↔ Runa optional types
- Kotlin data classes ↔ Runa data structures
- Kotlin sealed classes ↔ Runa union types

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
import logging

from .kotlin_ast import (
    KotlinNode, KotlinProgram, KotlinStatement, KotlinExpression,
    KotlinClassDeclaration, KotlinFunctionDeclaration, KotlinPropertyDeclaration,
    KotlinPackageDeclaration, KotlinImportDeclaration, KotlinBinaryExpression,
    KotlinUnaryExpression, KotlinCallExpression, KotlinLambdaExpression,
    KotlinIfExpression, KotlinWhenExpression, KotlinTryExpression,
    KotlinIdentifier, KotlinLiteral, KotlinStringTemplate, KotlinType,
    KotlinBlock, KotlinReturnStatement, KotlinAssignment, KotlinForStatement,
    KotlinWhileStatement, KotlinModifier, KotlinVisibility, KotlinClassKind,
    KotlinOperator, KotlinVariance, KotlinNodeType
)

# Import Runa AST nodes
from ....core.runa_ast import (
    ASTNode, Program, Statement, Expression, Declaration, TypeExpression,
    BasicType, GenericType, UnionType, IntersectionType, OptionalType,
    FunctionType, IntegerLiteral, FloatLiteral, StringLiteral, BooleanLiteral,
    ListLiteral, DictionaryLiteral, Identifier, MemberAccess, IndexAccess,
    BinaryOperator, BinaryExpression, UnaryExpression, FunctionCall,
    LetStatement, DefineStatement, SetStatement, IfStatement, WhileStatement,
    ForStatement, TryStatement, RaiseStatement, ReturnStatement, BreakStatement,
    ContinueStatement, ExpressionStatement, ProcessDeclaration, StructDefinition,
    MethodDefinition, FieldDefinition, PropertyDefinition, AnnotationDefinition,
    ImportStatement, ExportStatement, ModuleDefinition, BlockStatement,
    MatchStatement, ConditionalExpression, ListComprehension, LambdaExpression,
    AwaitExpression, YieldExpression, SpreadExpression, TupleExpression,
    SliceExpression, AssignmentExpression, AugmentedAssignmentExpression,
    ChainedComparisonExpression, TernaryExpression, CompoundStatement,
    SourceLocation, TranslationMetadata
)


class KotlinToRunaConverter:
    """
    Converts Kotlin AST to Runa AST.
    
    This converter transforms Kotlin constructs into their Runa equivalents:
    - Classes and objects become structures
    - Functions become processes
    - Properties become variables
    - Coroutines become async constructs
    - Null safety types become optional types
    """
    
    def __init__(self):
        """Initialize the Kotlin to Runa converter."""
        self.logger = logging.getLogger(__name__)
        self.type_mapping = self._build_type_mapping()
        self.operator_mapping = self._build_operator_mapping()
        self.current_scope = []  # Track current scope for variable resolution
        self.package_name = None  # Track current package
    
    def _build_type_mapping(self) -> Dict[str, str]:
        """Build mapping from Kotlin types to Runa types."""
        return {
            # Basic types
            'Int': 'Integer',
            'Long': 'BigInteger',
            'Short': 'SmallInteger',
            'Byte': 'TinyInteger',
            'Float': 'Float',
            'Double': 'Float',
            'Boolean': 'Boolean',
            'String': 'String',
            'Char': 'Character',
            'Unit': 'Unit',
            'Nothing': 'Nothing',
            
            # Collection types
            'List': 'List',
            'MutableList': 'MutableList',
            'Set': 'Set',
            'MutableSet': 'MutableSet',
            'Map': 'Dictionary',
            'MutableMap': 'MutableDictionary',
            'Array': 'Array',
            
            # Special types
            'Any': 'Any',
            'Any?': 'Optional[Any]',
            'Function': 'Function',
            'Pair': 'Tuple',
            'Triple': 'Tuple',
        }
    
    def _build_operator_mapping(self) -> Dict[str, BinaryOperator]:
        """Build mapping from Kotlin operators to Runa operators."""
        return {
            '+': BinaryOperator.PLUS,
            '-': BinaryOperator.MINUS,
            '*': BinaryOperator.MULTIPLY,
            '/': BinaryOperator.DIVIDE,
            '%': BinaryOperator.MODULO,
            '==': BinaryOperator.EQUALS,
            '!=': BinaryOperator.NOT_EQUALS,
            '>': BinaryOperator.GREATER_THAN,
            '<': BinaryOperator.LESS_THAN,
            '>=': BinaryOperator.GREATER_EQUAL,
            '<=': BinaryOperator.LESS_EQUAL,
            '&&': BinaryOperator.AND,
            '||': BinaryOperator.OR,
            '===': BinaryOperator.EQUALS,  # Identity equals mapped to equals
            '!==': BinaryOperator.NOT_EQUALS,  # Identity not equals
            '..': BinaryOperator.FOLLOWED_BY,  # Range operator
            'in': BinaryOperator.EQUALS,  # Simplified mapping
            '?:': BinaryOperator.OR,  # Elvis operator
        }
    
    def convert(self, kotlin_ast: KotlinProgram) -> Program:
        """
        Convert Kotlin program to Runa program.
        
        Args:
            kotlin_ast: Kotlin AST to convert
            
        Returns:
            Program: Runa AST
        """
        statements = []
        
        # Convert package declaration to module definition
        if kotlin_ast.package_declaration:
            self.package_name = kotlin_ast.package_declaration.name
            module_def = ModuleDefinition(
                name=self.package_name,
                description=f"Module for {self.package_name}",
                version="1.0.0"
            )
            statements.append(module_def)
        
        # Convert imports
        for import_decl in kotlin_ast.imports:
            import_stmt = self._convert_import_declaration(import_decl)
            if import_stmt:
                statements.append(import_stmt)
        
        # Convert declarations
        for decl in kotlin_ast.declarations:
            converted = self.convert_statement(decl)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements=statements)
    
    def convert_statement(self, stmt: KotlinStatement) -> Union[Statement, List[Statement], None]:
        """Convert Kotlin statement to Runa statement(s)."""
        if isinstance(stmt, KotlinClassDeclaration):
            return self._convert_class_declaration(stmt)
        elif isinstance(stmt, KotlinFunctionDeclaration):
            return self._convert_function_declaration(stmt)
        elif isinstance(stmt, KotlinPropertyDeclaration):
            return self._convert_property_declaration(stmt)
        elif isinstance(stmt, KotlinReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, KotlinAssignment):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, KotlinForStatement):
            return self._convert_for_statement(stmt)
        elif isinstance(stmt, KotlinWhileStatement):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, KotlinBlock):
            return self._convert_block(stmt)
        elif isinstance(stmt, KotlinExpression):
            return ExpressionStatement(expression=self.convert_expression(stmt))
        else:
            self.logger.warning(f"Unsupported Kotlin statement type: {type(stmt)}")
            return None
    
    def _convert_import_declaration(self, import_decl: KotlinImportDeclaration) -> ImportStatement:
        """Convert Kotlin import to Runa import."""
        return ImportStatement(
            module=import_decl.path,
            alias=import_decl.alias,
            items=None  # Import all by default
        )
    
    def _convert_class_declaration(self, class_decl: KotlinClassDeclaration) -> StructDefinition:
        """Convert Kotlin class to Runa structure."""
        # Convert modifiers to determine visibility and other properties
        is_abstract = any(mod.name == "abstract" for mod in class_decl.modifiers)
        is_final = any(mod.name == "final" for mod in class_decl.modifiers)
        is_open = any(mod.name == "open" for mod in class_decl.modifiers)
        is_data = any(mod.name == "data" for mod in class_decl.modifiers)
        is_sealed = any(mod.name == "sealed" for mod in class_decl.modifiers)
        
        # Convert class members to fields and methods
        fields = []
        methods = []
        
        for member in class_decl.members:
            if isinstance(member, KotlinPropertyDeclaration):
                field = self._convert_property_to_field(member)
                if field:
                    fields.append(field)
            elif isinstance(member, KotlinFunctionDeclaration):
                method = self._convert_function_to_method(member)
                if method:
                    methods.append(method)
        
        # Convert supertypes
        base_types = []
        for supertype in class_decl.supertypes:
            base_type = self._convert_type_to_runa(supertype)
            if base_type:
                base_types.append(base_type)
        
        return StructDefinition(
            name=class_decl.name,
            fields=fields,
            methods=methods,
            base_types=base_types,
            is_abstract=is_abstract,
            is_data_structure=is_data,
            is_sealed=is_sealed,
            description=f"Kotlin class {class_decl.name}"
        )
    
    def _convert_function_declaration(self, func_decl: KotlinFunctionDeclaration) -> ProcessDeclaration:
        """Convert Kotlin function to Runa process."""
        # Convert modifiers
        is_suspend = any(mod.name == "suspend" for mod in func_decl.modifiers)
        is_inline = any(mod.name == "inline" for mod in func_decl.modifiers)
        
        # Convert parameters
        parameters = []
        for param in func_decl.parameters:
            param_type = self._convert_type_to_runa(param.get('type'))
            parameters.append({
                'name': param.get('name'),
                'type': param_type,
                'default_value': param.get('default_value')
            })
        
        # Convert return type
        return_type = None
        if func_decl.return_type:
            return_type = self._convert_type_to_runa(func_decl.return_type)
        
        # Convert body
        body = None
        if func_decl.body:
            if isinstance(func_decl.body, KotlinBlock):
                body = self._convert_block(func_decl.body)
            else:
                # Expression body
                body = BlockStatement(statements=[
                    ReturnStatement(value=self.convert_expression(func_decl.body))
                ])
        
        return ProcessDeclaration(
            name=func_decl.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            is_async=is_suspend,
            is_inline=is_inline,
            description=f"Kotlin function {func_decl.name}"
        )
    
    def _convert_property_declaration(self, prop_decl: KotlinPropertyDeclaration) -> Union[LetStatement, DefineStatement]:
        """Convert Kotlin property to Runa variable declaration."""
        # Convert type
        prop_type = None
        if prop_decl.type:
            prop_type = self._convert_type_to_runa(prop_decl.type)
        
        # Convert initializer
        initializer = None
        if prop_decl.initializer:
            initializer = self.convert_expression(prop_decl.initializer)
        
        # Determine if it's constant
        is_const = any(mod.name == "const" for mod in prop_decl.modifiers)
        
        if is_const or not prop_decl.is_var:
            # Use DefineStatement for val (immutable) properties
            return DefineStatement(
                identifier=prop_decl.name,
                type_annotation=prop_type,
                value=initializer,
                is_constant=is_const
            )
        else:
            # Use LetStatement for var (mutable) properties
            return LetStatement(
                identifier=prop_decl.name,
                type_annotation=prop_type,
                value=initializer
            )
    
    def _convert_return_statement(self, return_stmt: KotlinReturnStatement) -> ReturnStatement:
        """Convert Kotlin return statement to Runa return statement."""
        value = None
        if return_stmt.value:
            value = self.convert_expression(return_stmt.value)
        
        return ReturnStatement(value=value)
    
    def _convert_assignment(self, assignment: KotlinAssignment) -> SetStatement:
        """Convert Kotlin assignment to Runa set statement."""
        target = assignment.target
        value = self.convert_expression(assignment.value)
        
        if isinstance(target, KotlinIdentifier):
            return SetStatement(
                identifier=target.name,
                value=value
            )
        else:
            # Complex assignment target
            return SetStatement(
                identifier="complex_target",
                value=value
            )
    
    def _convert_for_statement(self, for_stmt: KotlinForStatement) -> ForStatement:
        """Convert Kotlin for statement to Runa for statement."""
        # Kotlin for loops are typically for-in loops
        variable = for_stmt.variable
        iterable = self.convert_expression(for_stmt.iterable)
        body = self._convert_block(for_stmt.body)
        
        return ForStatement(
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def _convert_while_statement(self, while_stmt: KotlinWhileStatement) -> WhileStatement:
        """Convert Kotlin while statement to Runa while statement."""
        condition = self.convert_expression(while_stmt.condition)
        body = self._convert_block(while_stmt.body)
        
        return WhileStatement(
            condition=condition,
            body=body
        )
    
    def _convert_block(self, block: KotlinBlock) -> BlockStatement:
        """Convert Kotlin block to Runa block statement."""
        statements = []
        
        for stmt in block.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return BlockStatement(statements=statements)
    
    def convert_expression(self, expr: KotlinExpression) -> Expression:
        """Convert Kotlin expression to Runa expression."""
        if isinstance(expr, KotlinLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, KotlinIdentifier):
            return Identifier(name=expr.name)
        elif isinstance(expr, KotlinBinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, KotlinUnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, KotlinCallExpression):
            return self._convert_call_expression(expr)
        elif isinstance(expr, KotlinLambdaExpression):
            return self._convert_lambda_expression(expr)
        elif isinstance(expr, KotlinIfExpression):
            return self._convert_if_expression(expr)
        elif isinstance(expr, KotlinWhenExpression):
            return self._convert_when_expression(expr)
        elif isinstance(expr, KotlinTryExpression):
            return self._convert_try_expression(expr)
        elif isinstance(expr, KotlinStringTemplate):
            return self._convert_string_template(expr)
        else:
            self.logger.warning(f"Unsupported Kotlin expression type: {type(expr)}")
            return Identifier(name="unsupported_expression")
    
    def _convert_literal(self, literal: KotlinLiteral) -> Expression:
        """Convert Kotlin literal to Runa literal."""
        if literal.type == "Int" or literal.type == "Long":
            return IntegerLiteral(value=int(literal.value))
        elif literal.type == "Float" or literal.type == "Double":
            return FloatLiteral(value=float(literal.value))
        elif literal.type == "String":
            return StringLiteral(value=str(literal.value))
        elif literal.type == "Boolean":
            return BooleanLiteral(value=bool(literal.value))
        elif literal.type == "Char":
            return StringLiteral(value=str(literal.value))
        elif literal.value is None:
            return Identifier(name="null")
        else:
            return StringLiteral(value=str(literal.value))
    
    def _convert_binary_expression(self, expr: KotlinBinaryExpression) -> Expression:
        """Convert Kotlin binary expression to Runa binary expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Handle special Kotlin operators
        if expr.operator.value == "?.":
            # Safe call operator - create a conditional expression
            null_check = BinaryExpression(
                left=left,
                operator=BinaryOperator.NOT_EQUALS,
                right=Identifier(name="null")
            )
            return ConditionalExpression(
                condition=null_check,
                true_expression=right,
                false_expression=Identifier(name="null")
            )
        elif expr.operator.value == "?:":
            # Elvis operator - create a conditional expression
            null_check = BinaryExpression(
                left=left,
                operator=BinaryOperator.NOT_EQUALS,
                right=Identifier(name="null")
            )
            return ConditionalExpression(
                condition=null_check,
                true_expression=left,
                false_expression=right
            )
        else:
            # Regular binary operators
            runa_operator = self.operator_mapping.get(expr.operator.value, BinaryOperator.EQUALS)
            return BinaryExpression(
                left=left,
                operator=runa_operator,
                right=right
            )
    
    def _convert_unary_expression(self, expr: KotlinUnaryExpression) -> Expression:
        """Convert Kotlin unary expression to Runa unary expression."""
        operand = self.convert_expression(expr.operand)
        
        if expr.operator.value == "!!":
            # Not-null assertion - in Runa, this is just the operand
            return operand
        else:
            operator_str = "not" if expr.operator.value == "!" else expr.operator.value
            return UnaryExpression(
                operator=operator_str,
                operand=operand
            )
    
    def _convert_call_expression(self, expr: KotlinCallExpression) -> Expression:
        """Convert Kotlin call expression to Runa function call."""
        if isinstance(expr.callee, KotlinIdentifier):
            function_name = expr.callee.name
        else:
            function_name = "unknown_function"
        
        # Convert arguments
        arguments = []
        for i, arg in enumerate(expr.arguments):
            converted_arg = self.convert_expression(arg)
            arguments.append((f"arg{i}", converted_arg))
        
        return FunctionCall(
            function_name=function_name,
            arguments=arguments
        )
    
    def _convert_lambda_expression(self, expr: KotlinLambdaExpression) -> LambdaExpression:
        """Convert Kotlin lambda expression to Runa lambda expression."""
        # Convert parameters
        parameters = []
        for param in expr.parameters:
            parameters.append(param.get('name', 'it'))
        
        # Convert body
        body = self._convert_block(expr.body)
        
        return LambdaExpression(
            parameters=parameters,
            body=body
        )
    
    def _convert_if_expression(self, expr: KotlinIfExpression) -> ConditionalExpression:
        """Convert Kotlin if expression to Runa conditional expression."""
        condition = self.convert_expression(expr.condition)
        
        true_expr = None
        if isinstance(expr.then_branch, KotlinBlock):
            # Block - get the last expression or create a default
            if expr.then_branch.statements:
                last_stmt = expr.then_branch.statements[-1]
                if isinstance(last_stmt, KotlinExpression):
                    true_expr = self.convert_expression(last_stmt)
                else:
                    true_expr = Identifier(name="unit")
            else:
                true_expr = Identifier(name="unit")
        else:
            true_expr = self.convert_expression(expr.then_branch)
        
        false_expr = None
        if expr.else_branch:
            if isinstance(expr.else_branch, KotlinBlock):
                if expr.else_branch.statements:
                    last_stmt = expr.else_branch.statements[-1]
                    if isinstance(last_stmt, KotlinExpression):
                        false_expr = self.convert_expression(last_stmt)
                    else:
                        false_expr = Identifier(name="unit")
                else:
                    false_expr = Identifier(name="unit")
            else:
                false_expr = self.convert_expression(expr.else_branch)
        else:
            false_expr = Identifier(name="unit")
        
        return ConditionalExpression(
            condition=condition,
            true_expression=true_expr,
            false_expression=false_expr
        )
    
    def _convert_when_expression(self, expr: KotlinWhenExpression) -> MatchStatement:
        """Convert Kotlin when expression to Runa match statement."""
        subject = None
        if expr.subject:
            subject = self.convert_expression(expr.subject)
        
        # Convert when entries to match cases
        cases = []
        for entry in expr.entries:
            conditions = entry.get('conditions', [])
            body = entry.get('body')
            
            # Convert conditions
            patterns = []
            for condition in conditions:
                if condition == "else":
                    patterns.append(Identifier(name="_"))  # Default pattern
                else:
                    patterns.append(self.convert_expression(condition))
            
            # Convert body
            if isinstance(body, KotlinBlock):
                body_stmt = self._convert_block(body)
            else:
                body_stmt = ExpressionStatement(expression=self.convert_expression(body))
            
            cases.append({
                'patterns': patterns,
                'body': body_stmt
            })
        
        return MatchStatement(
            subject=subject,
            cases=cases
        )
    
    def _convert_try_expression(self, expr: KotlinTryExpression) -> TryStatement:
        """Convert Kotlin try expression to Runa try statement."""
        try_block = self._convert_block(expr.try_block)
        
        # Convert catch blocks
        catch_blocks = []
        for catch_block in expr.catch_blocks:
            param = catch_block.get('parameter')
            body = catch_block.get('body')
            
            exception_type = None
            if param and param.get('type'):
                exception_type = self._convert_type_to_runa(param['type'])
            
            catch_body = self._convert_block(body)
            
            catch_blocks.append({
                'exception_type': exception_type,
                'variable': param.get('name') if param else None,
                'body': catch_body
            })
        
        # Convert finally block
        finally_block = None
        if expr.finally_block:
            finally_block = self._convert_block(expr.finally_block)
        
        return TryStatement(
            try_block=try_block,
            catch_blocks=catch_blocks,
            finally_block=finally_block
        )
    
    def _convert_string_template(self, expr: KotlinStringTemplate) -> Expression:
        """Convert Kotlin string template to Runa string interpolation."""
        # For now, convert to a simple string literal
        # In a full implementation, this would handle interpolation
        return StringLiteral(value=str(expr.value))
    
    def _convert_property_to_field(self, prop: KotlinPropertyDeclaration) -> FieldDefinition:
        """Convert Kotlin property to Runa field definition."""
        field_type = None
        if prop.type:
            field_type = self._convert_type_to_runa(prop.type)
        
        default_value = None
        if prop.initializer:
            default_value = self.convert_expression(prop.initializer)
        
        is_required = not prop.is_var  # val properties are required
        
        return FieldDefinition(
            name=prop.name,
            type=field_type,
            default_value=default_value,
            is_required=is_required,
            is_mutable=prop.is_var
        )
    
    def _convert_function_to_method(self, func: KotlinFunctionDeclaration) -> MethodDefinition:
        """Convert Kotlin function to Runa method definition."""
        # Convert parameters
        parameters = []
        for param in func.parameters:
            param_type = self._convert_type_to_runa(param.get('type'))
            parameters.append({
                'name': param.get('name'),
                'type': param_type
            })
        
        # Convert return type
        return_type = None
        if func.return_type:
            return_type = self._convert_type_to_runa(func.return_type)
        
        # Convert body
        body = None
        if func.body:
            if isinstance(func.body, KotlinBlock):
                body = self._convert_block(func.body)
            else:
                body = BlockStatement(statements=[
                    ReturnStatement(value=self.convert_expression(func.body))
                ])
        
        return MethodDefinition(
            name=func.name,
            parameters=parameters,
            return_type=return_type,
            body=body
        )
    
    def _convert_type_to_runa(self, kotlin_type: KotlinType) -> TypeExpression:
        """Convert Kotlin type to Runa type expression."""
        if not kotlin_type:
            return BasicType(name="Any")
        
        base_name = kotlin_type.name
        runa_type_name = self.type_mapping.get(base_name, base_name)
        
        # Handle nullable types
        if kotlin_type.nullable:
            inner_type = BasicType(name=runa_type_name)
            return OptionalType(inner_type=inner_type)
        
        # Handle generic types
        if kotlin_type.type_arguments:
            type_args = []
            for arg in kotlin_type.type_arguments:
                type_args.append(self._convert_type_to_runa(arg))
            return GenericType(base_type=runa_type_name, type_args=type_args)
        
        return BasicType(name=runa_type_name)


class RunaToKotlinConverter:
    """
    Converts Runa AST to Kotlin AST.
    
    This converter transforms Runa constructs into their Kotlin equivalents:
    - Structures become classes
    - Processes become functions
    - Variables become properties
    - Async constructs become coroutines
    - Optional types become nullable types
    """
    
    def __init__(self):
        """Initialize the Runa to Kotlin converter."""
        self.logger = logging.getLogger(__name__)
        self.type_mapping = self._build_type_mapping()
        self.operator_mapping = self._build_operator_mapping()
        self.current_package = None
        self.imports = []
    
    def _build_type_mapping(self) -> Dict[str, str]:
        """Build mapping from Runa types to Kotlin types."""
        return {
            # Basic types
            'Integer': 'Int',
            'BigInteger': 'Long',
            'SmallInteger': 'Short',
            'TinyInteger': 'Byte',
            'Float': 'Double',
            'Boolean': 'Boolean',
            'String': 'String',
            'Character': 'Char',
            'Unit': 'Unit',
            'Nothing': 'Nothing',
            'Any': 'Any',
            
            # Collection types
            'List': 'List',
            'MutableList': 'MutableList',
            'Set': 'Set',
            'MutableSet': 'MutableSet',
            'Dictionary': 'Map',
            'MutableDictionary': 'MutableMap',
            'Array': 'Array',
            'Tuple': 'Pair',
        }
    
    def _build_operator_mapping(self) -> Dict[BinaryOperator, str]:
        """Build mapping from Runa operators to Kotlin operators."""
        return {
            BinaryOperator.PLUS: '+',
            BinaryOperator.MINUS: '-',
            BinaryOperator.MULTIPLY: '*',
            BinaryOperator.DIVIDE: '/',
            BinaryOperator.MODULO: '%',
            BinaryOperator.EQUALS: '==',
            BinaryOperator.NOT_EQUALS: '!=',
            BinaryOperator.GREATER_THAN: '>',
            BinaryOperator.LESS_THAN: '<',
            BinaryOperator.GREATER_EQUAL: '>=',
            BinaryOperator.LESS_EQUAL: '<=',
            BinaryOperator.AND: '&&',
            BinaryOperator.OR: '||',
            BinaryOperator.FOLLOWED_BY: '..',  # Range operator
        }
    
    def convert(self, runa_ast: Program) -> KotlinProgram:
        """
        Convert Runa program to Kotlin program.
        
        Args:
            runa_ast: Runa AST to convert
            
        Returns:
            KotlinProgram: Kotlin AST
        """
        package_declaration = None
        imports = []
        declarations = []
        
        for stmt in runa_ast.statements:
            if isinstance(stmt, ModuleDefinition):
                package_declaration = KotlinPackageDeclaration(name=stmt.name)
                self.current_package = stmt.name
            elif isinstance(stmt, ImportStatement):
                import_decl = KotlinImportDeclaration(
                    path=stmt.module,
                    alias=stmt.alias
                )
                imports.append(import_decl)
            else:
                converted = self.convert_statement(stmt)
                if converted:
                    if isinstance(converted, list):
                        declarations.extend(converted)
                    else:
                        declarations.append(converted)
        
        return KotlinProgram(
            package_declaration=package_declaration,
            imports=imports,
            declarations=declarations
        )
    
    def convert_statement(self, stmt: Statement) -> Union[KotlinStatement, List[KotlinStatement], None]:
        """Convert Runa statement to Kotlin statement(s)."""
        if isinstance(stmt, StructDefinition):
            return self._convert_struct_definition(stmt)
        elif isinstance(stmt, ProcessDeclaration):
            return self._convert_process_declaration(stmt)
        elif isinstance(stmt, LetStatement):
            return self._convert_let_statement(stmt)
        elif isinstance(stmt, DefineStatement):
            return self._convert_define_statement(stmt)
        elif isinstance(stmt, SetStatement):
            return self._convert_set_statement(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, IfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, WhileStatement):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, ForStatement):
            return self._convert_for_statement(stmt)
        elif isinstance(stmt, TryStatement):
            return self._convert_try_statement(stmt)
        elif isinstance(stmt, ExpressionStatement):
            return KotlinExpression(expression=self.convert_expression(stmt.expression))
        elif isinstance(stmt, BlockStatement):
            return self._convert_block_statement(stmt)
        else:
            self.logger.warning(f"Unsupported Runa statement type: {type(stmt)}")
            return None
    
    def _convert_struct_definition(self, struct_def: StructDefinition) -> KotlinClassDeclaration:
        """Convert Runa structure definition to Kotlin class."""
        # Convert modifiers
        modifiers = []
        if struct_def.is_abstract:
            modifiers.append(KotlinModifier(name="abstract"))
        if struct_def.is_data_structure:
            modifiers.append(KotlinModifier(name="data"))
        if struct_def.is_sealed:
            modifiers.append(KotlinModifier(name="sealed"))
        
        # Convert fields to properties
        members = []
        for field in struct_def.fields:
            prop = self._convert_field_to_property(field)
            if prop:
                members.append(prop)
        
        # Convert methods to functions
        for method in struct_def.methods:
            func = self._convert_method_to_function(method)
            if func:
                members.append(func)
        
        # Convert base types to supertypes
        supertypes = []
        for base_type in struct_def.base_types:
            kotlin_type = self._convert_type_to_kotlin(base_type)
            if kotlin_type:
                supertypes.append(kotlin_type)
        
        return KotlinClassDeclaration(
            modifiers=modifiers,
            name=struct_def.name,
            type_parameters=[],
            primary_constructor=None,
            supertypes=supertypes,
            members=members
        )
    
    def _convert_process_declaration(self, process_decl: ProcessDeclaration) -> KotlinFunctionDeclaration:
        """Convert Runa process declaration to Kotlin function."""
        # Convert modifiers
        modifiers = []
        if process_decl.is_async:
            modifiers.append(KotlinModifier(name="suspend"))
        if process_decl.is_inline:
            modifiers.append(KotlinModifier(name="inline"))
        
        # Convert parameters
        parameters = []
        for param in process_decl.parameters:
            param_type = self._convert_type_to_kotlin(param.get('type'))
            parameters.append({
                'name': param.get('name'),
                'type': param_type,
                'default_value': param.get('default_value')
            })
        
        # Convert return type
        return_type = None
        if process_decl.return_type:
            return_type = self._convert_type_to_kotlin(process_decl.return_type)
        
        # Convert body
        body = None
        if process_decl.body:
            body = self._convert_block_statement(process_decl.body)
        
        return KotlinFunctionDeclaration(
            modifiers=modifiers,
            name=process_decl.name,
            type_parameters=[],
            parameters=parameters,
            return_type=return_type,
            body=body
        )
    
    def _convert_let_statement(self, let_stmt: LetStatement) -> KotlinPropertyDeclaration:
        """Convert Runa let statement to Kotlin var property."""
        prop_type = None
        if let_stmt.type_annotation:
            prop_type = self._convert_type_to_kotlin(let_stmt.type_annotation)
        
        initializer = None
        if let_stmt.value:
            initializer = self.convert_expression(let_stmt.value)
        
        return KotlinPropertyDeclaration(
            modifiers=[],
            is_var=True,
            name=let_stmt.identifier,
            type=prop_type,
            initializer=initializer
        )
    
    def _convert_define_statement(self, define_stmt: DefineStatement) -> KotlinPropertyDeclaration:
        """Convert Runa define statement to Kotlin val property."""
        prop_type = None
        if define_stmt.type_annotation:
            prop_type = self._convert_type_to_kotlin(define_stmt.type_annotation)
        
        initializer = None
        if define_stmt.value:
            initializer = self.convert_expression(define_stmt.value)
        
        modifiers = []
        if define_stmt.is_constant:
            modifiers.append(KotlinModifier(name="const"))
        
        return KotlinPropertyDeclaration(
            modifiers=modifiers,
            is_var=False,
            name=define_stmt.identifier,
            type=prop_type,
            initializer=initializer
        )
    
    def _convert_set_statement(self, set_stmt: SetStatement) -> KotlinAssignment:
        """Convert Runa set statement to Kotlin assignment."""
        target = KotlinIdentifier(name=set_stmt.identifier)
        value = self.convert_expression(set_stmt.value)
        
        return KotlinAssignment(
            target=target,
            value=value
        )
    
    def _convert_return_statement(self, return_stmt: ReturnStatement) -> KotlinReturnStatement:
        """Convert Runa return statement to Kotlin return statement."""
        value = None
        if return_stmt.value:
            value = self.convert_expression(return_stmt.value)
        
        return KotlinReturnStatement(value=value)
    
    def _convert_if_statement(self, if_stmt: IfStatement) -> KotlinIfExpression:
        """Convert Runa if statement to Kotlin if expression."""
        condition = self.convert_expression(if_stmt.condition)
        then_branch = self._convert_block_statement(if_stmt.then_branch)
        
        else_branch = None
        if if_stmt.else_branch:
            else_branch = self._convert_block_statement(if_stmt.else_branch)
        
        return KotlinIfExpression(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _convert_while_statement(self, while_stmt: WhileStatement) -> KotlinWhileStatement:
        """Convert Runa while statement to Kotlin while statement."""
        condition = self.convert_expression(while_stmt.condition)
        body = self._convert_block_statement(while_stmt.body)
        
        return KotlinWhileStatement(
            condition=condition,
            body=body
        )
    
    def _convert_for_statement(self, for_stmt: ForStatement) -> KotlinForStatement:
        """Convert Runa for statement to Kotlin for statement."""
        variable = for_stmt.variable
        iterable = self.convert_expression(for_stmt.iterable)
        body = self._convert_block_statement(for_stmt.body)
        
        return KotlinForStatement(
            variable=variable,
            iterable=iterable,
            body=body
        )
    
    def _convert_try_statement(self, try_stmt: TryStatement) -> KotlinTryExpression:
        """Convert Runa try statement to Kotlin try expression."""
        try_block = self._convert_block_statement(try_stmt.try_block)
        
        catch_blocks = []
        for catch_block in try_stmt.catch_blocks:
            param_type = self._convert_type_to_kotlin(catch_block.get('exception_type'))
            param_name = catch_block.get('variable', 'e')
            catch_body = self._convert_block_statement(catch_block.get('body'))
            
            catch_blocks.append({
                'parameter': {'name': param_name, 'type': param_type},
                'body': catch_body
            })
        
        finally_block = None
        if try_stmt.finally_block:
            finally_block = self._convert_block_statement(try_stmt.finally_block)
        
        return KotlinTryExpression(
            try_block=try_block,
            catch_blocks=catch_blocks,
            finally_block=finally_block
        )
    
    def _convert_block_statement(self, block_stmt: BlockStatement) -> KotlinBlock:
        """Convert Runa block statement to Kotlin block."""
        statements = []
        
        for stmt in block_stmt.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return KotlinBlock(statements=statements)
    
    def convert_expression(self, expr: Expression) -> KotlinExpression:
        """Convert Runa expression to Kotlin expression."""
        if isinstance(expr, IntegerLiteral):
            return KotlinLiteral(value=expr.value, type="Int")
        elif isinstance(expr, FloatLiteral):
            return KotlinLiteral(value=expr.value, type="Double")
        elif isinstance(expr, StringLiteral):
            return KotlinLiteral(value=expr.value, type="String")
        elif isinstance(expr, BooleanLiteral):
            return KotlinLiteral(value=expr.value, type="Boolean")
        elif isinstance(expr, Identifier):
            if expr.name == "null":
                return KotlinLiteral(value=None, type="Nothing?")
            else:
                return KotlinIdentifier(name=expr.name)
        elif isinstance(expr, BinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, UnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, ConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, LambdaExpression):
            return self._convert_lambda_expression(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list_literal(expr)
        elif isinstance(expr, MemberAccess):
            return self._convert_member_access(expr)
        else:
            self.logger.warning(f"Unsupported Runa expression type: {type(expr)}")
            return KotlinIdentifier(name="unsupported_expression")
    
    def _convert_binary_expression(self, expr: BinaryExpression) -> KotlinExpression:
        """Convert Runa binary expression to Kotlin binary expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        kotlin_operator = self.operator_mapping.get(expr.operator, '==')
        
        return KotlinBinaryExpression(
            left=left,
            operator=KotlinOperator(kotlin_operator),
            right=right
        )
    
    def _convert_unary_expression(self, expr: UnaryExpression) -> KotlinExpression:
        """Convert Runa unary expression to Kotlin unary expression."""
        operand = self.convert_expression(expr.operand)
        
        kotlin_operator = "!" if expr.operator == "not" else expr.operator
        
        return KotlinUnaryExpression(
            operator=KotlinOperator(kotlin_operator),
            operand=operand,
            is_prefix=True
        )
    
    def _convert_function_call(self, expr: FunctionCall) -> KotlinExpression:
        """Convert Runa function call to Kotlin call expression."""
        callee = KotlinIdentifier(name=expr.function_name)
        
        arguments = []
        for arg_name, arg_value in expr.arguments:
            arguments.append(self.convert_expression(arg_value))
        
        return KotlinCallExpression(
            callee=callee,
            arguments=arguments
        )
    
    def _convert_conditional_expression(self, expr: ConditionalExpression) -> KotlinExpression:
        """Convert Runa conditional expression to Kotlin if expression."""
        condition = self.convert_expression(expr.condition)
        then_branch = self.convert_expression(expr.true_expression)
        else_branch = self.convert_expression(expr.false_expression)
        
        return KotlinIfExpression(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _convert_lambda_expression(self, expr: LambdaExpression) -> KotlinExpression:
        """Convert Runa lambda expression to Kotlin lambda expression."""
        parameters = []
        for param in expr.parameters:
            parameters.append({'name': param})
        
        body = self._convert_block_statement(expr.body)
        
        return KotlinLambdaExpression(
            parameters=parameters,
            body=body
        )
    
    def _convert_list_literal(self, expr: ListLiteral) -> KotlinExpression:
        """Convert Runa list literal to Kotlin list creation."""
        elements = []
        for element in expr.elements:
            elements.append(self.convert_expression(element))
        
        # Create a function call to listOf
        return KotlinCallExpression(
            callee=KotlinIdentifier(name="listOf"),
            arguments=elements
        )
    
    def _convert_member_access(self, expr: MemberAccess) -> KotlinExpression:
        """Convert Runa member access to Kotlin member access."""
        obj = self.convert_expression(expr.object)
        
        # Create a member access expression (simplified)
        return KotlinCallExpression(
            callee=obj,
            arguments=[]
        )
    
    def _convert_field_to_property(self, field: FieldDefinition) -> KotlinPropertyDeclaration:
        """Convert Runa field definition to Kotlin property."""
        prop_type = None
        if field.type:
            prop_type = self._convert_type_to_kotlin(field.type)
        
        initializer = None
        if field.default_value:
            initializer = self.convert_expression(field.default_value)
        
        return KotlinPropertyDeclaration(
            modifiers=[],
            is_var=field.is_mutable,
            name=field.name,
            type=prop_type,
            initializer=initializer
        )
    
    def _convert_method_to_function(self, method: MethodDefinition) -> KotlinFunctionDeclaration:
        """Convert Runa method definition to Kotlin function."""
        # Convert parameters
        parameters = []
        for param in method.parameters:
            param_type = self._convert_type_to_kotlin(param.get('type'))
            parameters.append({
                'name': param.get('name'),
                'type': param_type
            })
        
        # Convert return type
        return_type = None
        if method.return_type:
            return_type = self._convert_type_to_kotlin(method.return_type)
        
        # Convert body
        body = None
        if method.body:
            body = self._convert_block_statement(method.body)
        
        return KotlinFunctionDeclaration(
            modifiers=[],
            name=method.name,
            type_parameters=[],
            parameters=parameters,
            return_type=return_type,
            body=body
        )
    
    def _convert_type_to_kotlin(self, runa_type: TypeExpression) -> KotlinType:
        """Convert Runa type expression to Kotlin type."""
        if not runa_type:
            return KotlinType(name="Any")
        
        if isinstance(runa_type, BasicType):
            kotlin_type_name = self.type_mapping.get(runa_type.name, runa_type.name)
            return KotlinType(name=kotlin_type_name, nullable=False)
        
        elif isinstance(runa_type, OptionalType):
            inner_type = self._convert_type_to_kotlin(runa_type.inner_type)
            return KotlinType(name=inner_type.name, nullable=True)
        
        elif isinstance(runa_type, GenericType):
            base_type = self.type_mapping.get(runa_type.base_type, runa_type.base_type)
            
            type_arguments = []
            for arg in runa_type.type_args:
                type_arguments.append(self._convert_type_to_kotlin(arg))
            
            return KotlinType(
                name=base_type,
                nullable=False,
                type_arguments=type_arguments
            )
        
        else:
            return KotlinType(name="Any", nullable=False)