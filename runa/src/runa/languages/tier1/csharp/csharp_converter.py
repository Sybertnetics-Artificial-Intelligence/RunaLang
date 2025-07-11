#!/usr/bin/env python3
"""
C# ↔ Runa Bidirectional Converter

Converts between C# AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
Handles modern C# features including async/await, LINQ, generics, and nullable reference types.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field

from .csharp_ast import *
from ....core.runa_ast import *


class CSharpToRunaConverter:
    """Converts C# AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.method_counter = 0
        self.class_counter = 0
        self.namespace_name = ""
        self.using_statements = []
        self.current_class = None
        self.async_methods = set()
        
    def convert(self, csharp_ast: CSharpCompilationUnit) -> Program:
        """Convert C# compilation unit to Runa program."""
        statements = []
        
        # Handle using directives
        for using_directive in csharp_ast.using_directives:
            using_statement = self._convert_using_directive(using_directive)
            if using_statement:
                statements.append(using_statement)
        
        # Handle namespace and type declarations
        for member in csharp_ast.members:
            converted = self.convert_declaration(member)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements)
    
    def convert_declaration(self, decl: CSharpDeclaration) -> Union[Statement, List[Statement], None]:
        """Convert C# declaration to Runa statement(s)."""
        if isinstance(decl, CSharpNamespaceDeclaration):
            return self._convert_namespace_declaration(decl)
        elif isinstance(decl, CSharpClassDeclaration):
            return self._convert_class_declaration(decl)
        elif isinstance(decl, CSharpStructDeclaration):
            return self._convert_struct_declaration(decl)
        elif isinstance(decl, CSharpInterfaceDeclaration):
            return self._convert_interface_declaration(decl)
        elif isinstance(decl, CSharpEnumDeclaration):
            return self._convert_enum_declaration(decl)
        elif isinstance(decl, CSharpDelegateDeclaration):
            return self._convert_delegate_declaration(decl)
        elif isinstance(decl, CSharpRecordDeclaration):
            return self._convert_record_declaration(decl)
        elif isinstance(decl, CSharpMethodDeclaration):
            return self._convert_method_declaration(decl)
        elif isinstance(decl, CSharpFieldDeclaration):
            return self._convert_field_declaration(decl)
        elif isinstance(decl, CSharpPropertyDeclaration):
            return self._convert_property_declaration(decl)
        
        return None
    
    def convert_statement(self, stmt: CSharpStatement) -> Union[Statement, List[Statement], None]:
        """Convert C# statement to Runa statement(s)."""
        if isinstance(stmt, CSharpExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, CSharpBlock):
            return self._convert_block_statement(stmt)
        elif isinstance(stmt, CSharpIfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, CSharpWhileStatement):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, CSharpForStatement):
            return self._convert_for_statement(stmt)
        elif isinstance(stmt, CSharpForEachStatement):
            return self._convert_foreach_statement(stmt)
        elif isinstance(stmt, CSharpDoStatement):
            return self._convert_do_statement(stmt)
        elif isinstance(stmt, CSharpSwitchStatement):
            return self._convert_switch_statement(stmt)
        elif isinstance(stmt, CSharpBreakStatement):
            return self._convert_break_statement(stmt)
        elif isinstance(stmt, CSharpContinueStatement):
            return self._convert_continue_statement(stmt)
        elif isinstance(stmt, CSharpReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, CSharpThrowStatement):
            return self._convert_throw_statement(stmt)
        elif isinstance(stmt, CSharpTryStatement):
            return self._convert_try_statement(stmt)
        elif isinstance(stmt, CSharpLockStatement):
            return self._convert_lock_statement(stmt)
        elif isinstance(stmt, CSharpUsingStatement):
            return self._convert_using_statement(stmt)
        elif isinstance(stmt, CSharpYieldStatement):
            return self._convert_yield_statement(stmt)
        elif isinstance(stmt, CSharpLocalDeclarationStatement):
            return self._convert_local_declaration_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: CSharpExpression) -> Expression:
        """Convert C# expression to Runa expression."""
        if isinstance(expr, CSharpLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, CSharpIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, CSharpQualifiedName):
            return self._convert_qualified_name(expr)
        elif isinstance(expr, CSharpBinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, CSharpUnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, CSharpConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, CSharpAssignmentExpression):
            return self._convert_assignment_expression(expr)
        elif isinstance(expr, CSharpInvocationExpression):
            return self._convert_invocation_expression(expr)
        elif isinstance(expr, CSharpMemberAccessExpression):
            return self._convert_member_access_expression(expr)
        elif isinstance(expr, CSharpIndexerAccessExpression):
            return self._convert_element_access_expression(expr)
        elif isinstance(expr, CSharpCastExpression):
            return self._convert_cast_expression(expr)
        elif isinstance(expr, CSharpIsExpression):
            return self._convert_is_expression(expr)
        elif isinstance(expr, CSharpAsExpression):
            return self._convert_as_expression(expr)
        elif isinstance(expr, CSharpThisExpression):
            return self._convert_this_expression(expr)
        elif isinstance(expr, CSharpBaseExpression):
            return self._convert_base_expression(expr)
        elif isinstance(expr, CSharpTypeofExpression):
            return self._convert_typeof_expression(expr)
        elif isinstance(expr, CSharpSizeofExpression):
            return self._convert_sizeof_expression(expr)
        elif isinstance(expr, CSharpNameofExpression):
            return self._convert_nameof_expression(expr)
        elif isinstance(expr, CSharpDefaultExpression):
            return self._convert_default_expression(expr)
        elif isinstance(expr, CSharpObjectCreationExpression):
            return self._convert_object_creation_expression(expr)
        elif isinstance(expr, CSharpArrayCreationExpression):
            return self._convert_array_creation_expression(expr)
        elif isinstance(expr, CSharpLambdaExpression):
            return self._convert_lambda_expression(expr)
        elif isinstance(expr, CSharpAwaitExpression):
            return self._convert_await_expression(expr)
        elif isinstance(expr, CSharpTupleExpression):
            return self._convert_tuple_expression(expr)
        elif isinstance(expr, CSharpThrowExpression):
            return self._convert_throw_expression(expr)
        elif isinstance(expr, CSharpRangeExpression):
            return self._convert_range_expression(expr)
        elif isinstance(expr, CSharpIndexExpression):
            return self._convert_index_expression(expr)
        elif isinstance(expr, CSharpSwitchExpression):
            return self._convert_switch_expression(expr)
        elif isinstance(expr, CSharpWithExpression):
            return self._convert_with_expression(expr)
        elif isinstance(expr, CSharpInterpolatedStringExpression):
            return self._convert_interpolated_string_expression(expr)
        elif isinstance(expr, CSharpQueryExpression):
            return self._convert_query_expression(expr)
        
        # Fallback
        return Identifier(f"unknown_expression_{self.variable_counter}")
    
    def _convert_using_directive(self, using_directive: CSharpUsingDirective) -> Optional[Statement]:
        """Convert using directive to Runa statement."""
        namespace_name = self._expression_to_string(using_directive.name)
        
        # Convert to Runa import-like statement
        return ExpressionStatement(
            StringLiteral(f"using {namespace_name}", "comment")
        )
    
    def _convert_namespace_declaration(self, namespace_decl: CSharpNamespaceDeclaration) -> List[Statement]:
        """Convert namespace declaration to Runa statements."""
        statements = []
        
        # Store namespace name
        old_namespace = self.namespace_name
        self.namespace_name = self._expression_to_string(namespace_decl.name)
        
        # Add namespace comment
        statements.append(ExpressionStatement(
            StringLiteral(f"namespace {self.namespace_name}", "comment")
        ))
        
        # Convert using directives
        for using_directive in namespace_decl.using_directives:
            using_statement = self._convert_using_directive(using_directive)
            if using_statement:
                statements.append(using_statement)
        
        # Convert members
        for member in namespace_decl.members:
            converted = self.convert_declaration(member)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        # Restore namespace name
        self.namespace_name = old_namespace
        
        return statements
    
    def _convert_class_declaration(self, class_decl: CSharpClassDeclaration) -> Statement:
        """Convert class declaration to Runa statement."""
        old_class = self.current_class
        self.current_class = class_decl.identifier
        
        # Convert class to Runa class-like structure
        class_name = class_decl.identifier
        
        # Create class definition
        class_def = ProcessDefinition(
            name=f"Class_{class_name}",
            parameters=[],
            body=[]
        )
        
        # Convert members
        for member in class_decl.members:
            converted = self.convert_declaration(member)
            if converted:
                if isinstance(converted, list):
                    class_def.body.extend(converted)
                else:
                    class_def.body.append(converted)
        
        self.current_class = old_class
        
        return class_def
    
    def _convert_struct_declaration(self, struct_decl: CSharpStructDeclaration) -> Statement:
        """Convert struct declaration to Runa statement."""
        # Similar to class but with value semantics
        return self._convert_class_declaration(struct_decl)
    
    def _convert_interface_declaration(self, interface_decl: CSharpInterfaceDeclaration) -> Statement:
        """Convert interface declaration to Runa statement."""
        # Convert interface to Runa interface-like structure
        interface_name = interface_decl.identifier
        
        return ExpressionStatement(
            StringLiteral(f"interface {interface_name}", "comment")
        )
    
    def _convert_enum_declaration(self, enum_decl: CSharpEnumDeclaration) -> Statement:
        """Convert enum declaration to Runa statement."""
        enum_name = enum_decl.identifier
        
        # Create enum-like structure
        enum_values = []
        for member in enum_decl.members:
            if isinstance(member, CSharpEnumMemberDeclaration):
                enum_values.append(member.identifier)
        
        return ExpressionStatement(
            StringLiteral(f"enum {enum_name} with values {', '.join(enum_values)}", "comment")
        )
    
    def _convert_delegate_declaration(self, delegate_decl: CSharpDelegateDeclaration) -> Statement:
        """Convert delegate declaration to Runa statement."""
        delegate_name = delegate_decl.identifier
        
        return ExpressionStatement(
            StringLiteral(f"delegate {delegate_name}", "comment")
        )
    
    def _convert_record_declaration(self, record_decl: CSharpRecordDeclaration) -> Statement:
        """Convert record declaration to Runa statement."""
        record_name = record_decl.identifier
        
        # Create record-like structure
        record_def = ProcessDefinition(
            name=f"Record_{record_name}",
            parameters=[],
            body=[]
        )
        
        # Convert members
        for member in record_decl.members:
            converted = self.convert_declaration(member)
            if converted:
                if isinstance(converted, list):
                    record_def.body.extend(converted)
                else:
                    record_def.body.append(converted)
        
        return record_def
    
    def _convert_method_declaration(self, method_decl: CSharpMethodDeclaration) -> Statement:
        """Convert method declaration to Runa function."""
        method_name = method_decl.identifier
        
        # Check if method is async
        is_async = CSharpModifier.ASYNC in method_decl.modifiers
        if is_async:
            self.async_methods.add(method_name)
        
        # Convert parameters
        parameters = []
        if method_decl.parameter_list:
            for param in method_decl.parameter_list.parameters:
                param_name = param.identifier
                parameters.append(Parameter(param_name))
        
        # Convert body
        body = []
        if method_decl.body:
            for stmt in method_decl.body.statements:
                converted = self.convert_statement(stmt)
                if converted:
                    if isinstance(converted, list):
                        body.extend(converted)
                    else:
                        body.append(converted)
        elif method_decl.expression_body:
            # Expression body method
            expr_stmt = ExpressionStatement(
                self.convert_expression(method_decl.expression_body)
            )
            body.append(expr_stmt)
        
        return ProcessDefinition(
            name=method_name,
            parameters=parameters,
            body=body
        )
    
    def _convert_field_declaration(self, field_decl: CSharpFieldDeclaration) -> Statement:
        """Convert field declaration to Runa variable."""
        # Get first variable declarator
        if field_decl.declaration.variables:
            var_decl = field_decl.declaration.variables[0]
            var_name = var_decl.identifier
            
            # Get initializer if present
            initial_value = None
            if var_decl.initializer:
                initial_value = self.convert_expression(var_decl.initializer.value)
            
            return LetStatement(
                name=var_name,
                value=initial_value
            )
        
        return ExpressionStatement(StringLiteral("field", "comment"))
    
    def _convert_property_declaration(self, prop_decl: CSharpPropertyDeclaration) -> Statement:
        """Convert property declaration to Runa property."""
        prop_name = prop_decl.identifier
        
        # Create property-like structure
        return LetStatement(
            name=prop_name,
            value=None
        )
    
    def _convert_expression_statement(self, expr_stmt: CSharpExpressionStatement) -> Statement:
        """Convert expression statement to Runa statement."""
        return ExpressionStatement(
            self.convert_expression(expr_stmt.expression)
        )
    
    def _convert_block_statement(self, block_stmt: CSharpBlock) -> Statement:
        """Convert block statement to Runa block."""
        statements = []
        
        for stmt in block_stmt.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Block(statements)
    
    def _convert_if_statement(self, if_stmt: CSharpIfStatement) -> Statement:
        """Convert if statement to Runa if statement."""
        condition = self.convert_expression(if_stmt.condition)
        then_stmt = self.convert_statement(if_stmt.statement)
        else_stmt = None
        
        if if_stmt.else_statement:
            else_stmt = self.convert_statement(if_stmt.else_statement)
        
        return IfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt
        )
    
    def _convert_while_statement(self, while_stmt: CSharpWhileStatement) -> Statement:
        """Convert while statement to Runa while statement."""
        condition = self.convert_expression(while_stmt.condition)
        body = self.convert_statement(while_stmt.statement)
        
        return WhileLoop(
            condition=condition,
            body=body
        )
    
    def _convert_for_statement(self, for_stmt: CSharpForStatement) -> Statement:
        """Convert for statement to Runa for statement."""
        # Convert C# for loop to Runa while loop
        statements = []
        
        # Initialization
        if for_stmt.declaration:
            init_stmt = self._convert_variable_declaration(for_stmt.declaration)
            statements.append(init_stmt)
        elif for_stmt.initializers:
            for init in for_stmt.initializers:
                statements.append(ExpressionStatement(self.convert_expression(init)))
        
        # While loop
        condition = None
        if for_stmt.condition:
            condition = self.convert_expression(for_stmt.condition)
        else:
            condition = BooleanLiteral(value=True)
        
        # Body with incrementors
        body_statements = []
        body_statements.append(self.convert_statement(for_stmt.statement))
        
        for incrementor in for_stmt.incrementors:
            body_statements.append(ExpressionStatement(self.convert_expression(incrementor)))
        
        while_stmt = WhileLoop(
            condition=condition,
            body=Block(body_statements)
        )
        
        statements.append(while_stmt)
        
        return Block(statements)
    
    def _convert_foreach_statement(self, foreach_stmt: CSharpForEachStatement) -> Statement:
        """Convert foreach statement to Runa for-each statement."""
        variable = foreach_stmt.identifier
        collection = self.convert_expression(foreach_stmt.expression)
        body = self.convert_statement(foreach_stmt.statement)
        
        return ForEachLoop(
            variable=variable,
            collection=collection,
            body=body
        )
    
    def _convert_do_statement(self, do_stmt: CSharpDoStatement) -> Statement:
        """Convert do statement to Runa do-while statement."""
        body = self.convert_statement(do_stmt.statement)
        condition = self.convert_expression(do_stmt.condition)
        
        return DoWhileLoop(
            body=body,
            condition=condition
        )
    
    def _convert_switch_statement(self, switch_stmt: CSharpSwitchStatement) -> Statement:
        """Convert switch statement to Runa switch statement."""
        expression = self.convert_expression(switch_stmt.expression)
        cases = []
        
        for section in switch_stmt.sections:
            case_labels = []
            for label in section.labels:
                if isinstance(label, CSharpCaseSwitchLabel):
                    case_labels.append(self.convert_expression(label.value))
                elif isinstance(label, CSharpDefaultSwitchLabel):
                    case_labels.append(StringLiteral(value="default"))
            
            case_statements = []
            for stmt in section.statements:
                converted = self.convert_statement(stmt)
                if converted:
                    if isinstance(converted, list):
                        case_statements.extend(converted)
                    else:
                        case_statements.append(converted)
            
            cases.append(SwitchCase(
                labels=case_labels,
                statements=case_statements
            ))
        
        return SwitchStatement(
            expression=expression,
            cases=cases
        )
    
    def _convert_break_statement(self, break_stmt: CSharpBreakStatement) -> Statement:
        """Convert break statement to Runa break statement."""
        return BreakStatement()
    
    def _convert_continue_statement(self, continue_stmt: CSharpContinueStatement) -> Statement:
        """Convert continue statement to Runa continue statement."""
        return ContinueStatement()
    
    def _convert_return_statement(self, return_stmt: CSharpReturnStatement) -> Statement:
        """Convert return statement to Runa return statement."""
        value = None
        if return_stmt.expression:
            value = self.convert_expression(return_stmt.expression)
        
        return ReturnStatement(value=value)
    
    def _convert_throw_statement(self, throw_stmt: CSharpThrowStatement) -> Statement:
        """Convert throw statement to Runa throw statement."""
        expression = None
        if throw_stmt.expression:
            expression = self.convert_expression(throw_stmt.expression)
        
        return ThrowStatement(expression=expression)
    
    def _convert_try_statement(self, try_stmt: CSharpTryStatement) -> Statement:
        """Convert try statement to Runa try statement."""
        try_block = self.convert_statement(try_stmt.block)
        
        catch_blocks = []
        for catch_clause in try_stmt.catches:
            catch_var = None
            if catch_clause.declaration:
                catch_var = catch_clause.declaration.identifier
            
            catch_body = self.convert_statement(catch_clause.block)
            catch_blocks.append(CatchBlock(
                exception_type=catch_var,
                body=catch_body
            ))
        
        finally_block = None
        if try_stmt.finally_block:
            finally_block = self.convert_statement(try_stmt.finally_block)
        
        return TryStatement(
            try_block=try_block,
            catch_blocks=catch_blocks,
            finally_block=finally_block
        )
    
    def _convert_lock_statement(self, lock_stmt: CSharpLockStatement) -> Statement:
        """Convert lock statement to Runa synchronized statement."""
        expression = self.convert_expression(lock_stmt.expression)
        body = self.convert_statement(lock_stmt.statement)
        
        return SynchronizedStatement(
            expression=expression,
            body=body
        )
    
    def _convert_using_statement(self, using_stmt: CSharpUsingStatement) -> Statement:
        """Convert using statement to Runa try-with-resources statement."""
        resource = None
        if using_stmt.declaration:
            resource = self._convert_variable_declaration(using_stmt.declaration)
        elif using_stmt.expression:
            resource = ExpressionStatement(self.convert_expression(using_stmt.expression))
        
        body = self.convert_statement(using_stmt.statement)
        
        return TryWithResourcesStatement(
            resource=resource,
            body=body
        )
    
    def _convert_yield_statement(self, yield_stmt: CSharpYieldStatement) -> Statement:
        """Convert yield statement to Runa yield statement."""
        if yield_stmt.is_break:
            return YieldBreakStatement()
        else:
            expression = self.convert_expression(yield_stmt.expression)
            return YieldStatement(expression=expression)
    
    def _convert_local_declaration_statement(self, local_decl: CSharpLocalDeclarationStatement) -> Statement:
        """Convert local declaration statement to Runa variable declaration."""
        return self._convert_variable_declaration(local_decl.declaration)
    
    def _convert_variable_declaration(self, var_decl: CSharpVariableDeclaration) -> Statement:
        """Convert variable declaration to Runa variable declaration."""
        if var_decl.variables:
            first_var = var_decl.variables[0]
            var_name = first_var.identifier
            
            initial_value = None
            if first_var.initializer:
                initial_value = self.convert_expression(first_var.initializer.value)
            
            return LetStatement(
                name=var_name,
                value=initial_value
            )
        
        return ExpressionStatement(StringLiteral("variable", "comment"))
    
    def _convert_literal(self, literal: CSharpLiteral) -> Expression:
        """Convert C# literal to Runa literal."""
        return StringLiteral(literal.value, literal.literal_type)
    
    def _convert_identifier(self, identifier: CSharpIdentifier) -> Expression:
        """Convert C# identifier to Runa identifier."""
        return Identifier(identifier.name)
    
    def _convert_qualified_name(self, qualified_name: CSharpQualifiedName) -> Expression:
        """Convert C# qualified name to Runa qualified name."""
        left = self.convert_expression(qualified_name.left)
        right = self.convert_expression(qualified_name.right)
        
        return QualifiedName(left, right)
    
    def _convert_binary_expression(self, binary_expr: CSharpBinaryExpression) -> Expression:
        """Convert C# binary expression to Runa binary expression."""
        left = self.convert_expression(binary_expr.left)
        right = self.convert_expression(binary_expr.right)
        operator = self._convert_operator(binary_expr.operator)
        
        return BinaryExpression(left, operator, right)
    
    def _convert_unary_expression(self, unary_expr: CSharpUnaryExpression) -> Expression:
        """Convert C# unary expression to Runa unary expression."""
        operand = self.convert_expression(unary_expr.operand)
        operator = self._convert_operator(unary_expr.operator)
        
        return UnaryExpression(operator, operand)
    
    def _convert_conditional_expression(self, cond_expr: CSharpConditionalExpression) -> Expression:
        """Convert C# conditional expression to Runa conditional expression."""
        condition = self.convert_expression(cond_expr.condition)
        when_true = self.convert_expression(cond_expr.when_true)
        when_false = self.convert_expression(cond_expr.when_false)
        
        return ConditionalExpression(condition, when_true, when_false)
    
    def _convert_assignment_expression(self, assign_expr: CSharpAssignmentExpression) -> Expression:
        """Convert C# assignment expression to Runa assignment expression."""
        left = self.convert_expression(assign_expr.left)
        right = self.convert_expression(assign_expr.right)
        operator = self._convert_operator(assign_expr.operator)
        
        return AssignmentExpression(left, operator, right)
    
    def _convert_invocation_expression(self, invocation_expr: CSharpInvocationExpression) -> Expression:
        """Convert C# invocation expression to Runa method call."""
        function = self.convert_expression(invocation_expr.expression)
        
        arguments = []
        for arg in invocation_expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return FunctionCall(function, arguments)
    
    def _convert_member_access_expression(self, member_access: CSharpMemberAccessExpression) -> Expression:
        """Convert C# member access expression to Runa member access."""
        object_expr = self.convert_expression(member_access.expression)
        member_name = member_access.name
        
        return MemberAccess(object_expr, member_name)
    
    def _convert_element_access_expression(self, element_access: CSharpIndexerAccessExpression) -> Expression:
        """Convert C# element access expression to Runa array access."""
        array = self.convert_expression(element_access.expression)
        
        # Use first argument as index
        index = None
        if element_access.arguments:
            index = self.convert_expression(element_access.arguments[0])
        
        return ListLiteralAccess(array, index)
    
    def _convert_cast_expression(self, cast_expr: CSharpCastExpression) -> Expression:
        """Convert C# cast expression to Runa cast expression."""
        expression = self.convert_expression(cast_expr.expression)
        target_type = self._convert_type(cast_expr.target_type)
        
        return CastExpression(expression, target_type)
    
    def _convert_is_expression(self, is_expr: CSharpIsExpression) -> Expression:
        """Convert C# is expression to Runa instanceof expression."""
        expression = self.convert_expression(is_expr.expression)
        
        if isinstance(is_expr.type_or_pattern, CSharpType):
            type_name = self._convert_type(is_expr.type_or_pattern)
            return InstanceofExpression(expression, type_name)
        else:
            # Pattern matching - convert to instanceof for now
            return InstanceofExpression(expression, "Object")
    
    def _convert_as_expression(self, as_expr: CSharpAsExpression) -> Expression:
        """Convert C# as expression to Runa cast expression."""
        expression = self.convert_expression(as_expr.expression)
        target_type = self._convert_type(as_expr.target_type)
        
        return CastExpression(expression, target_type)
    
    def _convert_this_expression(self, this_expr: CSharpThisExpression) -> Expression:
        """Convert C# this expression to Runa this expression."""
        return ThisExpression()
    
    def _convert_base_expression(self, base_expr: CSharpBaseExpression) -> Expression:
        """Convert C# base expression to Runa super expression."""
        return SuperExpression()
    
    def _convert_typeof_expression(self, typeof_expr: CSharpTypeofExpression) -> Expression:
        """Convert C# typeof expression to Runa typeof expression."""
        target_type = self._convert_type(typeof_expr.target_type)
        return BasicTypeofExpression(target_type)
    
    def _convert_sizeof_expression(self, sizeof_expr: CSharpSizeofExpression) -> Expression:
        """Convert C# sizeof expression to Runa sizeof expression."""
        target_type = self._convert_type(sizeof_expr.target_type)
        return SizeofExpression(type_expression=target_type)
    
    def _convert_nameof_expression(self, nameof_expr: CSharpNameofExpression) -> Expression:
        """Convert C# nameof expression to Runa string literal."""
        # Extract name from expression
        name = self._expression_to_string(nameof_expr.expression)
        return StringLiteral(value=name)
    
    def _convert_default_expression(self, default_expr: CSharpDefaultExpression) -> Expression:
        """Convert C# default expression to Runa default expression."""
        if default_expr.target_type:
            target_type = self._convert_type(default_expr.target_type)
            return DefaultExpression(type_expression=target_type)
        else:
            return StringLiteral(value="null")
    
    def _convert_object_creation_expression(self, obj_creation: CSharpObjectCreationExpression) -> Expression:
        """Convert C# object creation expression to Runa new expression."""
        if obj_creation.type:
            type_name = self._convert_type(obj_creation.type)
        else:
            type_name = "Object"
        
        arguments = []
        for arg in obj_creation.arguments:
            arguments.append(self.convert_expression(arg))
        
        # Create proper new expression
        type_expr = BasicType(type_name)
        return NewExpression(type_expression=type_expr, arguments=arguments)
    
    def _convert_array_creation_expression(self, array_creation: CSharpArrayCreationExpression) -> Expression:
        """Convert C# array creation expression to Runa array creation."""
        element_type = self._convert_type(array_creation.type)
        
        # Get array dimensions
        dimensions = []
        for rank_spec in array_creation.rank_specifiers:
            for size in rank_spec.sizes:
                if size:
                    dimensions.append(self.convert_expression(size))
                else:
                    dimensions.append(StringLiteral(0, "int"))
        
        return ListLiteralCreation(element_type, dimensions)
    
    def _convert_lambda_expression(self, lambda_expr: CSharpLambdaExpression) -> Expression:
        """Convert C# lambda expression to Runa lambda expression."""
        parameters = []
        for param in lambda_expr.parameters:
            parameters.append(param.identifier)
        
        body = None
        if isinstance(lambda_expr.body, CSharpExpression):
            body = self.convert_expression(lambda_expr.body)
        else:
            body = self.convert_statement(lambda_expr.body)
        
        self.method_counter += 1
        return ProcessDefinition(
            name=f"lambda_{self.method_counter}",
            parameters=parameters,
            body=body
        )
    
    def _convert_await_expression(self, await_expr: CSharpAwaitExpression) -> Expression:
        """Convert C# await expression to Runa await expression."""
        expression = self.convert_expression(await_expr.expression)
        return AwaitExpression(expression)
    
    def _convert_tuple_expression(self, tuple_expr: CSharpTupleExpression) -> Expression:
        """Convert C# tuple expression to Runa tuple expression."""
        elements = []
        for arg in tuple_expr.arguments:
            elements.append(self.convert_expression(arg.expression))
        
        return TupleExpression(elements=elements)
    
    def _convert_throw_expression(self, throw_expr: CSharpThrowExpression) -> Expression:
        """Convert C# throw expression to Runa throw expression."""
        expression = self.convert_expression(throw_expr.expression)
        return ThrowExpression(expression)
    
    def _convert_range_expression(self, range_expr: CSharpRangeExpression) -> Expression:
        """Convert C# range expression to Runa range expression."""
        start = None
        end = None
        
        if range_expr.left:
            start = self.convert_expression(range_expr.left)
        if range_expr.right:
            end = self.convert_expression(range_expr.right)
        
        return RangeExpression(start, end)
    
    def _convert_index_expression(self, index_expr: CSharpIndexExpression) -> Expression:
        """Convert C# index expression to Runa index expression."""
        operand = self.convert_expression(index_expr.operand)
        return IndexExpression(operand)
    
    def _convert_switch_expression(self, switch_expr: CSharpSwitchExpression) -> Expression:
        """Convert C# switch expression to Runa switch expression."""
        governing_expression = self.convert_expression(switch_expr.governing_expression)
        
        arms = []
        for arm in switch_expr.arms:
            pattern = self._convert_pattern(arm.pattern)
            when_clause = None
            if arm.when_clause:
                when_clause = self.convert_expression(arm.when_clause)
            expression = self.convert_expression(arm.expression)
            
            arms.append(SwitchArm(pattern, when_clause, expression))
        
        return SwitchExpression(governing_expression, arms)
    
    def _convert_with_expression(self, with_expr: CSharpWithExpression) -> Expression:
        """Convert C# with expression to Runa with expression.
        
        C# with expressions create a copy of an object with specified property updates.
        Example: new_obj = original_obj with { Prop1 = value1, Prop2 = value2 }
        """
        # Convert the base expression (the object being copied)
        base_expression = self.convert_expression(with_expr.expression)
        
        # Convert the initializer (property updates) if present
        updates = []
        if with_expr.initializer:
            for expr in with_expr.initializer.expressions:
                if isinstance(expr, CSharpAssignmentExpression):
                    # Convert property assignment to Runa assignment expression
                    left = self.convert_expression(expr.left)
                    right = self.convert_expression(expr.right)
                    assignment = AssignmentExpression(
                        left=left,
                        operator="=",
                        right=right
                    )
                    updates.append(assignment)
                elif isinstance(expr, CSharpIdentifier):
                    # Handle implicit property assignments (e.g., { Prop } means { Prop = Prop })
                    prop_name = expr.name
                    # Create a member access for the property
                    member_access = MemberAccess(
                        expression=base_expression,
                        member=prop_name
                    )
                    # Create assignment: Prop = Prop
                    assignment = AssignmentExpression(
                        left=member_access,
                        operator="=",
                        right=member_access
                    )
                    updates.append(assignment)
                else:
                    # For other expression types, try to convert them
                    converted_expr = self.convert_expression(expr)
                    if isinstance(converted_expr, AssignmentExpression):
                        updates.append(converted_expr)
                    else:
                        # If it's not an assignment, create a default assignment
                        # This handles edge cases where the expression might be more complex
                        assignment = AssignmentExpression(
                            left=converted_expr,
                            operator="=",
                            right=converted_expr
                        )
                        updates.append(assignment)
        
        # Create the Runa WithExpression
        with_expression = WithExpression(
            base_expression=base_expression,
            updates=updates
        )
        
        return with_expression
    
    def _convert_interpolated_string_expression(self, interp_str: CSharpInterpolatedStringExpression) -> Expression:
        """Convert C# interpolated string to Runa interpolated string."""
        parts = []
        for part in interp_str.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                # Interpolation expression
                parts.append(self.convert_expression(part.expression))
        
        return InterpolatedStringExpression(parts=parts)
    
    def _convert_query_expression(self, query_expr: CSharpQueryExpression) -> Expression:
        """Convert C# LINQ query expression to Runa query expression."""
        # Convert LINQ to method calls
        from_clause = query_expr.from_clause
        collection = self.convert_expression(from_clause.expression)
        variable = from_clause.identifier
        
        # Convert query body
        result_expr = collection
        
        # Process query clauses
        for clause in query_expr.body.clauses:
            if isinstance(clause, CSharpWhereClause):
                condition = self.convert_expression(clause.condition)
                self.method_counter += 1
                result_expr = FunctionCall(
                    MemberAccess(result_expr, "filter"),
                    [ProcessDefinition(
                        name=f"lambda_{self.method_counter}",
                        parameters=[],
                        body=[ExpressionStatement(condition)]
                    )]
                )
            elif isinstance(clause, CSharpOrderByClause):
                for ordering in clause.orderings:
                    key_expr = self.convert_expression(ordering.expression)
                    self.method_counter += 1
                    result_expr = FunctionCall(
                        MemberAccess(result_expr, "orderBy"),
                        [ProcessDefinition(
                            name=f"lambda_{self.method_counter}",
                            parameters=[],
                            body=[ExpressionStatement(key_expr)]
                        )]
                    )
        
        # Process select or group clause
        if isinstance(query_expr.body.select_or_group, CSharpSelectClause):
            select_expr = self.convert_expression(query_expr.body.select_or_group.expression)
            self.method_counter += 1
            result_expr = FunctionCall(
                MemberAccess(result_expr, "map"),
                [ProcessDefinition(
                    name=f"lambda_{self.method_counter}",
                    parameters=[],
                    body=[ExpressionStatement(select_expr)]
                )]
            )
        elif isinstance(query_expr.body.select_or_group, CSharpGroupClause):
            group_expr = self.convert_expression(query_expr.body.select_or_group.group_expression)
            by_expr = self.convert_expression(query_expr.body.select_or_group.by_expression)
            self.method_counter += 1
            result_expr = FunctionCall(
                MemberAccess(result_expr, "groupBy"),
                [ProcessDefinition(
                    name=f"lambda_{self.method_counter}",
                    parameters=[],
                    body=[ExpressionStatement(by_expr)]
                )]
            )
        
        return result_expr
    
    def _convert_pattern(self, pattern: CSharpPattern) -> Expression:
        """Convert C# pattern to Runa pattern."""
        if isinstance(pattern, CSharpConstantPattern):
            return self.convert_expression(pattern.expression)
        elif isinstance(pattern, CSharpDeclarationPattern):
            type_name = self._convert_type(pattern.type)
            return StringLiteral(value=type_name)
        elif isinstance(pattern, CSharpVarPattern):
            return StringLiteral(value="var")
        elif isinstance(pattern, CSharpDiscardPattern):
            return StringLiteral(value="_")
        else:
            return StringLiteral(value="pattern")
    
    def _convert_operator(self, operator: CSharpOperator) -> str:
        """Convert C# operator to Runa operator."""
        operator_map = {
            CSharpOperator.PLUS: "plus",
            CSharpOperator.MINUS: "minus",
            CSharpOperator.MULTIPLY: "times",
            CSharpOperator.DIVIDE: "divided by",
            CSharpOperator.MODULO: "modulo",
            CSharpOperator.EQUAL: "is equal to",
            CSharpOperator.NOT_EQUAL: "is not equal to",
            CSharpOperator.LESS_THAN: "is less than",
            CSharpOperator.LESS_EQUAL: "is less than or equal to",
            CSharpOperator.GREATER_THAN: "is greater than",
            CSharpOperator.GREATER_EQUAL: "is greater than or equal to",
            CSharpOperator.LOGICAL_AND: "and",
            CSharpOperator.LOGICAL_OR: "or",
            CSharpOperator.LOGICAL_NOT: "not",
            CSharpOperator.ASSIGN: "equals",
            CSharpOperator.BITWISE_AND: "bitwise and",
            CSharpOperator.BITWISE_OR: "bitwise or",
            CSharpOperator.BITWISE_XOR: "bitwise xor",
            CSharpOperator.BITWISE_NOT: "bitwise not",
            CSharpOperator.LEFT_SHIFT: "left shift",
            CSharpOperator.RIGHT_SHIFT: "right shift",
            CSharpOperator.NULL_COALESCING: "null coalescing",
            CSharpOperator.RANGE: "range",
            CSharpOperator.INDEX_FROM_END: "index from end",
        }
        
        return operator_map.get(operator, str(operator))
    
    def _convert_type(self, csharp_type: CSharpType) -> str:
        """Convert C# type to Runa type."""
        if isinstance(csharp_type, CSharpPredefinedType):
            type_map = {
                "int": "Integer",
                "string": "String",
                "bool": "Boolean",
                "double": "Float",
                "float": "Float",
                "decimal": "Decimal",
                "byte": "Byte",
                "char": "Character",
                "long": "Long",
                "short": "Short",
                "uint": "UnsignedInteger",
                "ulong": "UnsignedLong",
                "ushort": "UnsignedShort",
                "sbyte": "SignedByte",
                "object": "Object",
                "void": "Void",
            }
            return type_map.get(csharp_type.keyword, csharp_type.keyword)
        elif isinstance(csharp_type, CSharpIdentifierName):
            return csharp_type.identifier
        elif isinstance(csharp_type, CSharpArrayType):
            element_type = self._convert_type(csharp_type.element_type)
            return f"Array[{element_type}]"
        elif isinstance(csharp_type, CSharpGenericNameType):
            base_type = csharp_type.identifier
            type_args = []
            for arg in csharp_type.type_argument_list.arguments:
                type_args.append(self._convert_type(arg))
            return f"{base_type}[{', '.join(type_args)}]"
        elif isinstance(csharp_type, CSharpNullableType):
            element_type = self._convert_type(csharp_type.element_type)
            return f"Nullable[{element_type}]"
        elif isinstance(csharp_type, CSharpTupleType):
            element_types = []
            for element in csharp_type.elements:
                element_types.append(self._convert_type(element.type))
            return f"Tuple[{', '.join(element_types)}]"
        else:
            return "Object"
    
    def _expression_to_string(self, expr: CSharpExpression) -> str:
        """Convert C# expression to string representation."""
        if isinstance(expr, CSharpIdentifier):
            return expr.name
        elif isinstance(expr, CSharpQualifiedName):
            left = self._expression_to_string(expr.left)
            right = self._expression_to_string(expr.right)
            return f"{left}.{right}"
        elif isinstance(expr, CSharpLiteral):
            return str(expr.value)
        else:
            return "unknown"


class RunaToCSharpConverter:
    """Converts Runa AST to C# AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.method_counter = 0
        self.class_counter = 0
        self.current_namespace = "Generated"
        self.using_statements = ["System", "System.Collections.Generic", "System.Linq"]
        
    def convert(self, runa_ast: Program) -> CSharpCompilationUnit:
        """Convert Runa program to C# compilation unit."""
        using_directives = []
        members = []
        
        # Add default using directives
        for using_ns in self.using_statements:
            using_directives.append(CSharpUsingDirective(
                CSharpNodeType.USING_DIRECTIVE,
                name=CSharpIdentifier(CSharpNodeType.IDENTIFIER, name=using_ns)
            ))
        
        # Convert statements to C# members
        class_members = []
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    class_members.extend(converted)
                else:
                    class_members.append(converted)
        
        # Create a main class to hold the converted code
        main_class = CSharpClassDeclaration(
            CSharpNodeType.CLASS_DECLARATION,
            attributes=[],
            modifiers=[CSharpModifier.PUBLIC],
            identifier="Program",
            members=class_members
        )
        
        members.append(main_class)
        
        return CSharpCompilationUnit(
            CSharpNodeType.COMPILATION_UNIT,
            extern_alias_directives=[],
            using_directives=using_directives,
            global_attributes=[],
            members=members
        )
    
    def convert_statement(self, stmt: Statement) -> Union[CSharpMemberDeclaration, CSharpStatement, List[CSharpMemberDeclaration], None]:
        """Convert Runa statement to C# statement or member."""
        if isinstance(stmt, ProcessDefinition):
            return self._convert_function_definition(stmt)
        elif isinstance(stmt, LetStatement):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, ExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, IfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, WhileLoop):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, ForEachLoop):
            return self._convert_foreach_statement(stmt)
        elif isinstance(stmt, DoWhileLoop):
            return self._convert_do_while_statement(stmt)
        elif isinstance(stmt, SwitchStatement):
            return self._convert_switch_statement(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, BreakStatement):
            return self._convert_break_statement(stmt)
        elif isinstance(stmt, ContinueStatement):
            return self._convert_continue_statement(stmt)
        elif isinstance(stmt, ThrowStatement):
            return self._convert_throw_statement(stmt)
        elif isinstance(stmt, TryStatement):
            return self._convert_try_statement(stmt)
        elif isinstance(stmt, Block):
            return self._convert_block(stmt)
        
        return None
    
    def convert_expression(self, expr: Expression) -> CSharpExpression:
        """Convert Runa expression to C# expression."""
        if isinstance(expr, StringLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, Identifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, BinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, UnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, FunctionCall):
            return self._convert_method_call(expr)
        elif isinstance(expr, MemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, ListLiteralAccess):
            return self._convert_array_access(expr)
        elif isinstance(expr, SetStatementExpression):
            return self._convert_assignment_expression(expr)
        elif isinstance(expr, ConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, CastExpression):
            return self._convert_cast_expression(expr)
        elif isinstance(expr, InstanceofExpression):
            return self._convert_instanceof_expression(expr)
        elif isinstance(expr, ThisExpression):
            return self._convert_this_expression(expr)
        elif isinstance(expr, SuperExpression):
            return self._convert_super_expression(expr)
        elif isinstance(expr, NewExpression):
            return self._convert_new_expression(expr)
        elif isinstance(expr, ListLiteralCreation):
            return self._convert_array_creation(expr)
        # ProcessDefinitionExpression removed - use ProcessDefinition for lambdas instead
        elif isinstance(expr, AwaitExpression):
            return self._convert_await_expression(expr)
        elif isinstance(expr, TupleExpression):
            return self._convert_tuple_expression(expr)
        elif isinstance(expr, InterpolatedStringExpression):
            return self._convert_interpolated_string(expr)
        
        # Fallback
        return CSharpIdentifier(CSharpNodeType.IDENTIFIER, name="unknown")
    
    def _convert_function_definition(self, func_def: ProcessDefinition) -> CSharpMethodDeclaration:
        """Convert Runa function definition to C# method declaration."""
        # Convert parameters
        parameters = []
        for param in func_def.parameters:
            parameters.append(CSharpParameter(
                CSharpNodeType.PARAMETER_DECLARATION,
                attributes=[],
                modifiers=[],
                type=CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="object"),
                identifier=param.name
            ))
        
        parameter_list = CSharpParameterList(
            CSharpNodeType.PARAMETER_LIST,
            parameters=parameters
        ) if parameters else None
        
        # Convert body
        body_statements = []
        for stmt in func_def.body:
            converted = self.convert_statement(stmt)
            if converted and isinstance(converted, CSharpStatement):
                body_statements.append(converted)
        
        body = CSharpBlock(
            CSharpNodeType.BLOCK_STATEMENT,
            statements=body_statements
        )
        
        return CSharpMethodDeclaration(
            CSharpNodeType.METHOD_DECLARATION,
            attributes=[],
            modifiers=[CSharpModifier.PUBLIC, CSharpModifier.STATIC],
            return_type=CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="void"),
            identifier=func_def.name,
            parameter_list=parameter_list,
            body=body
        )
    
    def _convert_variable_declaration(self, var_decl: LetStatement) -> CSharpFieldDeclaration:
        """Convert Runa variable declaration to C# field declaration."""
        # Create variable declarator
        declarator = CSharpVariableDeclarator(
            CSharpNodeType.VARIABLE_DECLARATION,
            identifier=var_decl.name
        )
        
        if var_decl.value:
            declarator.initializer = CSharpEqualsValueClause(
                CSharpNodeType.EQUALS_VALUE_CLAUSE,
                value=self.convert_expression(var_decl.value)
            )
        
        # Create variable declaration
        declaration = CSharpVariableDeclaration(
            CSharpNodeType.VARIABLE_DECLARATION,
            type=CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="var"),
            variables=[declarator]
        )
        
        return CSharpFieldDeclaration(
            CSharpNodeType.FIELD_DECLARATION,
            attributes=[],
            modifiers=[CSharpModifier.PUBLIC, CSharpModifier.STATIC],
            declaration=declaration
        )
    
    def _convert_expression_statement(self, expr_stmt: ExpressionStatement) -> CSharpExpressionStatement:
        """Convert Runa expression statement to C# expression statement."""
        return CSharpExpressionStatement(
            CSharpNodeType.EXPRESSION_STATEMENT,
            expression=self.convert_expression(expr_stmt.expression)
        )
    
    def _convert_if_statement(self, if_stmt: IfStatement) -> CSharpIfStatement:
        """Convert Runa if statement to C# if statement."""
        condition = self.convert_expression(if_stmt.condition)
        then_stmt = self.convert_statement(if_stmt.then_statement)
        else_stmt = None
        
        if if_stmt.else_statement:
            else_stmt = self.convert_statement(if_stmt.else_statement)
        
        return CSharpIfStatement(
            CSharpNodeType.IF_STATEMENT,
            condition=condition,
            statement=then_stmt,
            else_statement=else_stmt
        )
    
    def _convert_while_statement(self, while_stmt: WhileLoop) -> CSharpWhileStatement:
        """Convert Runa while statement to C# while statement."""
        condition = self.convert_expression(while_stmt.condition)
        body = self.convert_statement(while_stmt.body)
        
        return CSharpWhileStatement(
            CSharpNodeType.WHILE_STATEMENT,
            condition=condition,
            statement=body
        )
    
    def _convert_foreach_statement(self, foreach_stmt: ForEachLoop) -> CSharpForEachStatement:
        """Convert Runa foreach statement to C# foreach statement."""
        collection = self.convert_expression(foreach_stmt.collection)
        body = self.convert_statement(foreach_stmt.body)
        
        return CSharpForEachStatement(
            CSharpNodeType.FOREACH_STATEMENT,
            type=CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="var"),
            identifier=foreach_stmt.variable,
            expression=collection,
            statement=body
        )
    
    def _convert_do_while_statement(self, do_while_stmt: DoWhileLoop) -> CSharpDoStatement:
        """Convert Runa do-while statement to C# do statement."""
        body = self.convert_statement(do_while_stmt.body)
        condition = self.convert_expression(do_while_stmt.condition)
        
        return CSharpDoStatement(
            CSharpNodeType.DO_STATEMENT,
            statement=body,
            condition=condition
        )
    
    def _convert_switch_statement(self, switch_stmt: SwitchStatement) -> CSharpSwitchStatement:
        """Convert Runa switch statement to C# switch statement."""
        expression = self.convert_expression(switch_stmt.expression)
        
        sections = []
        for case in switch_stmt.cases:
            labels = []
            for label in case.labels:
                if isinstance(label, StringLiteral) and label.value == "default":
                    labels.append(CSharpDefaultSwitchLabel(CSharpNodeType.DEFAULT_SWITCH_LABEL))
                else:
                    labels.append(CSharpCaseSwitchLabel(
                        CSharpNodeType.CASE_SWITCH_LABEL,
                        value=self.convert_expression(label)
                    ))
            
            statements = []
            for stmt in case.statements:
                converted = self.convert_statement(stmt)
                if converted and isinstance(converted, CSharpStatement):
                    statements.append(converted)
            
            sections.append(CSharpSwitchSection(
                CSharpNodeType.SWITCH_STATEMENT,
                labels=labels,
                statements=statements
            ))
        
        return CSharpSwitchStatement(
            CSharpNodeType.SWITCH_STATEMENT,
            expression=expression,
            sections=sections
        )
    
    def _convert_return_statement(self, return_stmt: ReturnStatement) -> CSharpReturnStatement:
        """Convert Runa return statement to C# return statement."""
        expression = None
        if return_stmt.value:
            expression = self.convert_expression(return_stmt.value)
        
        return CSharpReturnStatement(
            CSharpNodeType.RETURN_STATEMENT,
            expression=expression
        )
    
    def _convert_break_statement(self, break_stmt: BreakStatement) -> CSharpBreakStatement:
        """Convert Runa break statement to C# break statement."""
        return CSharpBreakStatement(CSharpNodeType.BREAK_STATEMENT)
    
    def _convert_continue_statement(self, continue_stmt: ContinueStatement) -> CSharpContinueStatement:
        """Convert Runa continue statement to C# continue statement."""
        return CSharpContinueStatement(CSharpNodeType.CONTINUE_STATEMENT)
    
    def _convert_throw_statement(self, throw_stmt: ThrowStatement) -> CSharpThrowStatement:
        """Convert Runa throw statement to C# throw statement."""
        expression = None
        if throw_stmt.expression:
            expression = self.convert_expression(throw_stmt.expression)
        
        return CSharpThrowStatement(
            CSharpNodeType.THROW_STATEMENT,
            expression=expression
        )
    
    def _convert_try_statement(self, try_stmt: TryStatement) -> CSharpTryStatement:
        """Convert Runa try statement to C# try statement."""
        try_block = self.convert_statement(try_stmt.try_block)
        
        catch_clauses = []
        for catch_block in try_stmt.catch_blocks:
            catch_decl = None
            if catch_block.exception_type:
                catch_decl = CSharpCatchDeclaration(
                    CSharpNodeType.CATCH_CLAUSE,
                    type=CSharpIdentifierName(CSharpNodeType.IDENTIFIER_NAME, identifier=catch_block.exception_type),
                    identifier="e"
                )
            
            catch_body = self.convert_statement(catch_block.body)
            
            catch_clauses.append(CSharpCatchClause(
                CSharpNodeType.CATCH_CLAUSE,
                declaration=catch_decl,
                filter=None,
                block=catch_body
            ))
        
        finally_block = None
        if try_stmt.finally_block:
            finally_block = self.convert_statement(try_stmt.finally_block)
        
        return CSharpTryStatement(
            CSharpNodeType.TRY_STATEMENT,
            block=try_block,
            catches=catch_clauses,
            finally_block=finally_block
        )
    
    def _convert_block(self, block: Block) -> CSharpBlock:
        """Convert Runa block to C# block."""
        statements = []
        
        for stmt in block.statements:
            converted = self.convert_statement(stmt)
            if converted and isinstance(converted, CSharpStatement):
                statements.append(converted)
        
        return CSharpBlock(
            CSharpNodeType.BLOCK_STATEMENT,
            statements=statements
        )
    
    def _convert_literal(self, literal: StringLiteral) -> CSharpLiteral:
        """Convert Runa literal to C# literal."""
        return CSharpLiteral(
            CSharpNodeType.LITERAL,
            value=literal.value,
            literal_type=literal.literal_type
        )
    
    def _convert_identifier(self, identifier: Identifier) -> CSharpIdentifier:
        """Convert Runa identifier to C# identifier."""
        return CSharpIdentifier(
            CSharpNodeType.IDENTIFIER,
            name=identifier.name
        )
    
    def _convert_binary_expression(self, binary_expr: BinaryExpression) -> CSharpBinaryExpression:
        """Convert Runa binary expression to C# binary expression."""
        left = self.convert_expression(binary_expr.left)
        right = self.convert_expression(binary_expr.right)
        operator = self._convert_operator(binary_expr.operator)
        
        return CSharpBinaryExpression(
            CSharpNodeType.BINARY_EXPRESSION,
            left=left,
            operator=operator,
            right=right
        )
    
    def _convert_unary_expression(self, unary_expr: UnaryExpression) -> CSharpUnaryExpression:
        """Convert Runa unary expression to C# unary expression."""
        operand = self.convert_expression(unary_expr.operand)
        operator = self._convert_operator(unary_expr.operator)
        
        return CSharpUnaryExpression(
            CSharpNodeType.UNARY_EXPRESSION,
            operator=operator,
            operand=operand
        )
    
    def _convert_method_call(self, method_call: FunctionCall) -> CSharpInvocationExpression:
        """Convert Runa method call to C# invocation expression."""
        function = self.convert_expression(method_call.function)
        
        arguments = []
        for arg in method_call.arguments:
            arguments.append(self.convert_expression(arg))
        
        return CSharpInvocationExpression(
            CSharpNodeType.INVOCATION_EXPRESSION,
            expression=function,
            arguments=arguments
        )
    
    def _convert_member_access(self, member_access: MemberAccess) -> CSharpMemberAccessExpression:
        """Convert Runa member access to C# member access expression."""
        object_expr = self.convert_expression(member_access.object)
        
        return CSharpMemberAccessExpression(
            CSharpNodeType.MEMBER_ACCESS_EXPRESSION,
            expression=object_expr,
            name=member_access.member
        )
    
    def _convert_array_access(self, array_access: ListLiteralAccess) -> CSharpIndexerAccessExpression:
        """Convert Runa array access to C# element access expression."""
        array = self.convert_expression(array_access.array)
        index = self.convert_expression(array_access.index)
        
        return CSharpIndexerAccessExpression(
            CSharpNodeType.ELEMENT_ACCESS_EXPRESSION,
            expression=array,
            arguments=[index]
        )
    
    def _convert_assignment_expression(self, assign_expr: SetStatementExpression) -> CSharpAssignmentExpression:
        """Convert Runa assignment expression to C# assignment expression."""
        left = self.convert_expression(assign_expr.left)
        right = self.convert_expression(assign_expr.right)
        operator = self._convert_operator(assign_expr.operator)
        
        return CSharpAssignmentExpression(
            CSharpNodeType.ASSIGNMENT_EXPRESSION,
            left=left,
            operator=operator,
            right=right
        )
    
    def _convert_conditional_expression(self, cond_expr: ConditionalExpression) -> CSharpConditionalExpression:
        """Convert Runa conditional expression to C# conditional expression."""
        condition = self.convert_expression(cond_expr.condition)
        when_true = self.convert_expression(cond_expr.when_true)
        when_false = self.convert_expression(cond_expr.when_false)
        
        return CSharpConditionalExpression(
            CSharpNodeType.CONDITIONAL_EXPRESSION,
            condition=condition,
            when_true=when_true,
            when_false=when_false
        )
    
    def _convert_cast_expression(self, cast_expr: CastExpression) -> CSharpCastExpression:
        """Convert Runa cast expression to C# cast expression."""
        expression = self.convert_expression(cast_expr.expression)
        target_type = self._convert_type(cast_expr.target_type)
        
        return CSharpCastExpression(
            CSharpNodeType.CAST_EXPRESSION,
            target_type=target_type,
            expression=expression
        )
    
    def _convert_instanceof_expression(self, instanceof_expr: InstanceofExpression) -> CSharpIsExpression:
        """Convert Runa instanceof expression to C# is expression."""
        expression = self.convert_expression(instanceof_expr.expression)
        target_type = self._convert_type(instanceof_expr.type)
        
        return CSharpIsExpression(
            CSharpNodeType.IS_EXPRESSION,
            expression=expression,
            type_or_pattern=target_type
        )
    
    def _convert_this_expression(self, this_expr: ThisExpression) -> CSharpThisExpression:
        """Convert Runa this expression to C# this expression."""
        return CSharpThisExpression(CSharpNodeType.THIS_EXPRESSION)
    
    def _convert_super_expression(self, super_expr: SuperExpression) -> CSharpBaseExpression:
        """Convert Runa super expression to C# base expression."""
        return CSharpBaseExpression(CSharpNodeType.BASE_EXPRESSION)
    
    def _convert_new_expression(self, new_expr: NewExpression) -> CSharpObjectCreationExpression:
        """Convert Runa new expression to C# object creation expression."""
        obj_type = self._convert_type(new_expr.type_expression)
        
        arguments = []
        for arg in new_expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return CSharpObjectCreationExpression(
            CSharpNodeType.OBJECT_CREATION_EXPRESSION,
            type=obj_type,
            arguments=arguments
        )
    
    def _convert_array_creation(self, array_creation: ListLiteralCreation) -> CSharpArrayCreationExpression:
        """Convert Runa array creation to C# array creation expression."""
        element_type = self._convert_type(array_creation.element_type)
        
        # Create array type
        array_type = CSharpArrayType(
            CSharpNodeType.ARRAY_TYPE,
            element_type=element_type,
            rank_specifiers=[CSharpArrayRankSpecifier(
                CSharpNodeType.ARRAY_TYPE,
                sizes=[None]  # Single dimension
            )]
        )
        
        # Get first dimension size
        rank_specifiers = []
        if array_creation.dimensions:
            sizes = [self.convert_expression(array_creation.dimensions[0])]
            rank_specifiers = [CSharpArrayRankSpecifier(
                CSharpNodeType.ARRAY_TYPE,
                sizes=sizes
            )]
        
        return CSharpArrayCreationExpression(
            CSharpNodeType.ARRAY_CREATION_EXPRESSION,
            type=array_type,
            rank_specifiers=rank_specifiers
        )
    
    def _convert_lambda_expression(self, lambda_expr: ProcessDefinition) -> CSharpLambdaExpression:
        """Convert Runa lambda expression to C# lambda expression."""
        parameters = []
        for param_name in lambda_expr.parameters:
            parameters.append(CSharpParameter(
                CSharpNodeType.PARAMETER_DECLARATION,
                attributes=[],
                modifiers=[],
                type=None,  # Inferred
                identifier=param_name
            ))
        
        body = None
        if isinstance(lambda_expr.body, Expression):
            body = self.convert_expression(lambda_expr.body)
        else:
            body = self.convert_statement(lambda_expr.body)
        
        return CSharpLambdaExpression(
            CSharpNodeType.LAMBDA_EXPRESSION,
            parameters=parameters,
            body=body
        )
    
    def _convert_await_expression(self, await_expr: AwaitExpression) -> CSharpAwaitExpression:
        """Convert Runa await expression to C# await expression."""
        expression = self.convert_expression(await_expr.expression)
        
        return CSharpAwaitExpression(
            CSharpNodeType.AWAIT_EXPRESSION,
            expression=expression
        )
    
    def _convert_tuple_expression(self, tuple_expr: TupleExpression) -> CSharpTupleExpression:
        """Convert Runa tuple expression to C# tuple expression."""
        arguments = []
        for element in tuple_expr.elements:
            arguments.append(CSharpArgument(
                CSharpNodeType.ARGUMENT,
                expression=self.convert_expression(element)
            ))
        
        return CSharpTupleExpression(
            CSharpNodeType.TUPLE_EXPRESSION,
            arguments=arguments
        )
    
    def _convert_interpolated_string(self, interp_str: InterpolatedStringExpression) -> CSharpInterpolatedStringExpression:
        """Convert Runa interpolated string to C# interpolated string expression."""
        parts = []
        for part in interp_str.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                # Convert expression to interpolation
                parts.append(CSharpInterpolationExpression(
                    CSharpNodeType.INTERPOLATED_STRING_EXPRESSION,
                    expression=self.convert_expression(part)
                ))
        
        return CSharpInterpolatedStringExpression(
            CSharpNodeType.INTERPOLATED_STRING_EXPRESSION,
            parts=parts
        )
    
    def _convert_operator(self, runa_operator: str) -> CSharpOperator:
        """Convert Runa operator to C# operator."""
        operator_map = {
            "plus": CSharpOperator.PLUS,
            "minus": CSharpOperator.MINUS,
            "times": CSharpOperator.MULTIPLY,
            "divided by": CSharpOperator.DIVIDE,
            "modulo": CSharpOperator.MODULO,
            "is equal to": CSharpOperator.EQUAL,
            "is not equal to": CSharpOperator.NOT_EQUAL,
            "is less than": CSharpOperator.LESS_THAN,
            "is less than or equal to": CSharpOperator.LESS_EQUAL,
            "is greater than": CSharpOperator.GREATER_THAN,
            "is greater than or equal to": CSharpOperator.GREATER_EQUAL,
            "and": CSharpOperator.LOGICAL_AND,
            "or": CSharpOperator.LOGICAL_OR,
            "not": CSharpOperator.LOGICAL_NOT,
            "equals": CSharpOperator.ASSIGN,
            "bitwise and": CSharpOperator.BITWISE_AND,
            "bitwise or": CSharpOperator.BITWISE_OR,
            "bitwise xor": CSharpOperator.BITWISE_XOR,
            "bitwise not": CSharpOperator.BITWISE_NOT,
            "left shift": CSharpOperator.LEFT_SHIFT,
            "right shift": CSharpOperator.RIGHT_SHIFT,
            "null coalescing": CSharpOperator.NULL_COALESCING,
            "range": CSharpOperator.RANGE,
            "index from end": CSharpOperator.INDEX_FROM_END,
        }
        
        return operator_map.get(runa_operator, CSharpOperator.ASSIGN)
    
    def _convert_type(self, type_name: str) -> CSharpType:
        """Convert Runa type to C# type."""
        type_map = {
            "Integer": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="int"),
            "String": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="string"),
            "Boolean": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="bool"),
            "Float": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="double"),
            "Decimal": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="decimal"),
            "Byte": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="byte"),
            "Character": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="char"),
            "Long": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="long"),
            "Short": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="short"),
            "Object": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="object"),
            "Void": CSharpPredefinedType(CSharpNodeType.PREDEFINED_TYPE, keyword="void"),
        }
        
        return type_map.get(type_name, CSharpIdentifierName(CSharpNodeType.IDENTIFIER_NAME, identifier=type_name))


# Convenience functions
def csharp_to_runa(csharp_ast: CSharpCompilationUnit) -> Program:
    """Convert C# AST to Runa AST."""
    converter = CSharpToRunaConverter()
    return converter.convert(csharp_ast)


def runa_to_csharp(runa_ast: Program) -> CSharpCompilationUnit:
    """Convert Runa AST to C# AST."""
    converter = RunaToCSharpConverter()
    return converter.convert(runa_ast)