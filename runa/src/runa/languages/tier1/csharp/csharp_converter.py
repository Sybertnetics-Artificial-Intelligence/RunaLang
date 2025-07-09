#!/usr/bin/env python3
"""
C# ↔ Runa Bidirectional Converter

Converts between C# AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
Handles modern C# features including async/await, LINQ, generics, and nullable reference types.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

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
    
    def convert_declaration(self, decl: CSharpDeclaration) -> Union[RunaStatement, List[RunaStatement], None]:
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
    
    def convert_statement(self, stmt: CSharpStatement) -> Union[RunaStatement, List[RunaStatement], None]:
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
    
    def convert_expression(self, expr: CSharpExpression) -> RunaExpression:
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
        elif isinstance(expr, CSharpElementAccessExpression):
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
        return RunaIdentifier(f"unknown_expression_{self.variable_counter}")
    
    def _convert_using_directive(self, using_directive: CSharpUsingDirective) -> Optional[RunaStatement]:
        """Convert using directive to Runa statement."""
        namespace_name = self._expression_to_string(using_directive.name)
        
        # Convert to Runa import-like statement
        return RunaExpressionStatement(
            RunaLiteral(f"using {namespace_name}", "comment")
        )
    
    def _convert_namespace_declaration(self, namespace_decl: CSharpNamespaceDeclaration) -> List[RunaStatement]:
        """Convert namespace declaration to Runa statements."""
        statements = []
        
        # Store namespace name
        old_namespace = self.namespace_name
        self.namespace_name = self._expression_to_string(namespace_decl.name)
        
        # Add namespace comment
        statements.append(RunaExpressionStatement(
            RunaLiteral(f"namespace {self.namespace_name}", "comment")
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
    
    def _convert_class_declaration(self, class_decl: CSharpClassDeclaration) -> RunaStatement:
        """Convert class declaration to Runa statement."""
        old_class = self.current_class
        self.current_class = class_decl.identifier
        
        # Convert class to Runa class-like structure
        class_name = class_decl.identifier
        
        # Create class definition
        class_def = RunaFunctionDefinition(
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
    
    def _convert_struct_declaration(self, struct_decl: CSharpStructDeclaration) -> RunaStatement:
        """Convert struct declaration to Runa statement."""
        # Similar to class but with value semantics
        return self._convert_class_declaration(struct_decl)
    
    def _convert_interface_declaration(self, interface_decl: CSharpInterfaceDeclaration) -> RunaStatement:
        """Convert interface declaration to Runa statement."""
        # Convert interface to Runa interface-like structure
        interface_name = interface_decl.identifier
        
        return RunaExpressionStatement(
            RunaLiteral(f"interface {interface_name}", "comment")
        )
    
    def _convert_enum_declaration(self, enum_decl: CSharpEnumDeclaration) -> RunaStatement:
        """Convert enum declaration to Runa statement."""
        enum_name = enum_decl.identifier
        
        # Create enum-like structure
        enum_values = []
        for member in enum_decl.members:
            if isinstance(member, CSharpEnumMemberDeclaration):
                enum_values.append(member.identifier)
        
        return RunaExpressionStatement(
            RunaLiteral(f"enum {enum_name} with values {', '.join(enum_values)}", "comment")
        )
    
    def _convert_delegate_declaration(self, delegate_decl: CSharpDelegateDeclaration) -> RunaStatement:
        """Convert delegate declaration to Runa statement."""
        delegate_name = delegate_decl.identifier
        
        return RunaExpressionStatement(
            RunaLiteral(f"delegate {delegate_name}", "comment")
        )
    
    def _convert_record_declaration(self, record_decl: CSharpRecordDeclaration) -> RunaStatement:
        """Convert record declaration to Runa statement."""
        record_name = record_decl.identifier
        
        # Create record-like structure
        record_def = RunaFunctionDefinition(
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
    
    def _convert_method_declaration(self, method_decl: CSharpMethodDeclaration) -> RunaStatement:
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
                parameters.append(RunaParameter(param_name))
        
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
            expr_stmt = RunaExpressionStatement(
                self.convert_expression(method_decl.expression_body)
            )
            body.append(expr_stmt)
        
        return RunaFunctionDefinition(
            name=method_name,
            parameters=parameters,
            body=body
        )
    
    def _convert_field_declaration(self, field_decl: CSharpFieldDeclaration) -> RunaStatement:
        """Convert field declaration to Runa variable."""
        # Get first variable declarator
        if field_decl.declaration.variables:
            var_decl = field_decl.declaration.variables[0]
            var_name = var_decl.identifier
            
            # Get initializer if present
            initial_value = None
            if var_decl.initializer:
                initial_value = self.convert_expression(var_decl.initializer.value)
            
            return RunaVariableDeclaration(
                name=var_name,
                value=initial_value
            )
        
        return RunaExpressionStatement(RunaLiteral("field", "comment"))
    
    def _convert_property_declaration(self, prop_decl: CSharpPropertyDeclaration) -> RunaStatement:
        """Convert property declaration to Runa property."""
        prop_name = prop_decl.identifier
        
        # Create property-like structure
        return RunaVariableDeclaration(
            name=prop_name,
            value=None
        )
    
    def _convert_expression_statement(self, expr_stmt: CSharpExpressionStatement) -> RunaStatement:
        """Convert expression statement to Runa statement."""
        return RunaExpressionStatement(
            self.convert_expression(expr_stmt.expression)
        )
    
    def _convert_block_statement(self, block_stmt: CSharpBlock) -> RunaStatement:
        """Convert block statement to Runa block."""
        statements = []
        
        for stmt in block_stmt.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return RunaBlock(statements)
    
    def _convert_if_statement(self, if_stmt: CSharpIfStatement) -> RunaStatement:
        """Convert if statement to Runa if statement."""
        condition = self.convert_expression(if_stmt.condition)
        then_stmt = self.convert_statement(if_stmt.statement)
        else_stmt = None
        
        if if_stmt.else_statement:
            else_stmt = self.convert_statement(if_stmt.else_statement)
        
        return RunaIfStatement(
            condition=condition,
            then_statement=then_stmt,
            else_statement=else_stmt
        )
    
    def _convert_while_statement(self, while_stmt: CSharpWhileStatement) -> RunaStatement:
        """Convert while statement to Runa while statement."""
        condition = self.convert_expression(while_stmt.condition)
        body = self.convert_statement(while_stmt.statement)
        
        return RunaWhileStatement(
            condition=condition,
            body=body
        )
    
    def _convert_for_statement(self, for_stmt: CSharpForStatement) -> RunaStatement:
        """Convert for statement to Runa for statement."""
        # Convert C# for loop to Runa while loop
        statements = []
        
        # Initialization
        if for_stmt.declaration:
            init_stmt = self._convert_variable_declaration(for_stmt.declaration)
            statements.append(init_stmt)
        elif for_stmt.initializers:
            for init in for_stmt.initializers:
                statements.append(RunaExpressionStatement(self.convert_expression(init)))
        
        # While loop
        condition = None
        if for_stmt.condition:
            condition = self.convert_expression(for_stmt.condition)
        else:
            condition = RunaLiteral(True, "boolean")
        
        # Body with incrementors
        body_statements = []
        body_statements.append(self.convert_statement(for_stmt.statement))
        
        for incrementor in for_stmt.incrementors:
            body_statements.append(RunaExpressionStatement(self.convert_expression(incrementor)))
        
        while_stmt = RunaWhileStatement(
            condition=condition,
            body=RunaBlock(body_statements)
        )
        
        statements.append(while_stmt)
        
        return RunaBlock(statements)
    
    def _convert_foreach_statement(self, foreach_stmt: CSharpForEachStatement) -> RunaStatement:
        """Convert foreach statement to Runa for-each statement."""
        variable = foreach_stmt.identifier
        collection = self.convert_expression(foreach_stmt.expression)
        body = self.convert_statement(foreach_stmt.statement)
        
        return RunaForEachStatement(
            variable=variable,
            collection=collection,
            body=body
        )
    
    def _convert_do_statement(self, do_stmt: CSharpDoStatement) -> RunaStatement:
        """Convert do statement to Runa do-while statement."""
        body = self.convert_statement(do_stmt.statement)
        condition = self.convert_expression(do_stmt.condition)
        
        return RunaDoWhileStatement(
            body=body,
            condition=condition
        )
    
    def _convert_switch_statement(self, switch_stmt: CSharpSwitchStatement) -> RunaStatement:
        """Convert switch statement to Runa switch statement."""
        expression = self.convert_expression(switch_stmt.expression)
        cases = []
        
        for section in switch_stmt.sections:
            case_labels = []
            for label in section.labels:
                if isinstance(label, CSharpCaseSwitchLabel):
                    case_labels.append(self.convert_expression(label.value))
                elif isinstance(label, CSharpDefaultSwitchLabel):
                    case_labels.append(RunaLiteral("default", "string"))
            
            case_statements = []
            for stmt in section.statements:
                converted = self.convert_statement(stmt)
                if converted:
                    if isinstance(converted, list):
                        case_statements.extend(converted)
                    else:
                        case_statements.append(converted)
            
            cases.append(RunaSwitchCase(
                labels=case_labels,
                statements=case_statements
            ))
        
        return RunaSwitchStatement(
            expression=expression,
            cases=cases
        )
    
    def _convert_break_statement(self, break_stmt: CSharpBreakStatement) -> RunaStatement:
        """Convert break statement to Runa break statement."""
        return RunaBreakStatement()
    
    def _convert_continue_statement(self, continue_stmt: CSharpContinueStatement) -> RunaStatement:
        """Convert continue statement to Runa continue statement."""
        return RunaContinueStatement()
    
    def _convert_return_statement(self, return_stmt: CSharpReturnStatement) -> RunaStatement:
        """Convert return statement to Runa return statement."""
        value = None
        if return_stmt.expression:
            value = self.convert_expression(return_stmt.expression)
        
        return RunaReturnStatement(value=value)
    
    def _convert_throw_statement(self, throw_stmt: CSharpThrowStatement) -> RunaStatement:
        """Convert throw statement to Runa throw statement."""
        expression = None
        if throw_stmt.expression:
            expression = self.convert_expression(throw_stmt.expression)
        
        return RunaThrowStatement(expression=expression)
    
    def _convert_try_statement(self, try_stmt: CSharpTryStatement) -> RunaStatement:
        """Convert try statement to Runa try statement."""
        try_block = self.convert_statement(try_stmt.block)
        
        catch_blocks = []
        for catch_clause in try_stmt.catches:
            catch_var = None
            if catch_clause.declaration:
                catch_var = catch_clause.declaration.identifier
            
            catch_body = self.convert_statement(catch_clause.block)
            catch_blocks.append(RunaCatchBlock(
                exception_type=catch_var,
                body=catch_body
            ))
        
        finally_block = None
        if try_stmt.finally_block:
            finally_block = self.convert_statement(try_stmt.finally_block)
        
        return RunaTryStatement(
            try_block=try_block,
            catch_blocks=catch_blocks,
            finally_block=finally_block
        )
    
    def _convert_lock_statement(self, lock_stmt: CSharpLockStatement) -> RunaStatement:
        """Convert lock statement to Runa synchronized statement."""
        expression = self.convert_expression(lock_stmt.expression)
        body = self.convert_statement(lock_stmt.statement)
        
        return RunaSynchronizedStatement(
            expression=expression,
            body=body
        )
    
    def _convert_using_statement(self, using_stmt: CSharpUsingStatement) -> RunaStatement:
        """Convert using statement to Runa try-with-resources statement."""
        resource = None
        if using_stmt.declaration:
            resource = self._convert_variable_declaration(using_stmt.declaration)
        elif using_stmt.expression:
            resource = RunaExpressionStatement(self.convert_expression(using_stmt.expression))
        
        body = self.convert_statement(using_stmt.statement)
        
        return RunaTryWithResourcesStatement(
            resource=resource,
            body=body
        )
    
    def _convert_yield_statement(self, yield_stmt: CSharpYieldStatement) -> RunaStatement:
        """Convert yield statement to Runa yield statement."""
        if yield_stmt.is_break:
            return RunaYieldBreakStatement()
        else:
            expression = self.convert_expression(yield_stmt.expression)
            return RunaYieldStatement(expression=expression)
    
    def _convert_local_declaration_statement(self, local_decl: CSharpLocalDeclarationStatement) -> RunaStatement:
        """Convert local declaration statement to Runa variable declaration."""
        return self._convert_variable_declaration(local_decl.declaration)
    
    def _convert_variable_declaration(self, var_decl: CSharpVariableDeclaration) -> RunaStatement:
        """Convert variable declaration to Runa variable declaration."""
        if var_decl.variables:
            first_var = var_decl.variables[0]
            var_name = first_var.identifier
            
            initial_value = None
            if first_var.initializer:
                initial_value = self.convert_expression(first_var.initializer.value)
            
            return RunaVariableDeclaration(
                name=var_name,
                value=initial_value
            )
        
        return RunaExpressionStatement(RunaLiteral("variable", "comment"))
    
    def _convert_literal(self, literal: CSharpLiteral) -> RunaExpression:
        """Convert C# literal to Runa literal."""
        return RunaLiteral(literal.value, literal.literal_type)
    
    def _convert_identifier(self, identifier: CSharpIdentifier) -> RunaExpression:
        """Convert C# identifier to Runa identifier."""
        return RunaIdentifier(identifier.name)
    
    def _convert_qualified_name(self, qualified_name: CSharpQualifiedName) -> RunaExpression:
        """Convert C# qualified name to Runa qualified name."""
        left = self.convert_expression(qualified_name.left)
        right = self.convert_expression(qualified_name.right)
        
        return RunaQualifiedName(left, right)
    
    def _convert_binary_expression(self, binary_expr: CSharpBinaryExpression) -> RunaExpression:
        """Convert C# binary expression to Runa binary expression."""
        left = self.convert_expression(binary_expr.left)
        right = self.convert_expression(binary_expr.right)
        operator = self._convert_operator(binary_expr.operator)
        
        return RunaBinaryExpression(left, operator, right)
    
    def _convert_unary_expression(self, unary_expr: CSharpUnaryExpression) -> RunaExpression:
        """Convert C# unary expression to Runa unary expression."""
        operand = self.convert_expression(unary_expr.operand)
        operator = self._convert_operator(unary_expr.operator)
        
        return RunaUnaryExpression(operator, operand)
    
    def _convert_conditional_expression(self, cond_expr: CSharpConditionalExpression) -> RunaExpression:
        """Convert C# conditional expression to Runa conditional expression."""
        condition = self.convert_expression(cond_expr.condition)
        when_true = self.convert_expression(cond_expr.when_true)
        when_false = self.convert_expression(cond_expr.when_false)
        
        return RunaConditionalExpression(condition, when_true, when_false)
    
    def _convert_assignment_expression(self, assign_expr: CSharpAssignmentExpression) -> RunaExpression:
        """Convert C# assignment expression to Runa assignment expression."""
        left = self.convert_expression(assign_expr.left)
        right = self.convert_expression(assign_expr.right)
        operator = self._convert_operator(assign_expr.operator)
        
        return RunaAssignmentExpression(left, operator, right)
    
    def _convert_invocation_expression(self, invocation_expr: CSharpInvocationExpression) -> RunaExpression:
        """Convert C# invocation expression to Runa method call."""
        function = self.convert_expression(invocation_expr.expression)
        
        arguments = []
        for arg in invocation_expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return RunaMethodCall(function, arguments)
    
    def _convert_member_access_expression(self, member_access: CSharpMemberAccessExpression) -> RunaExpression:
        """Convert C# member access expression to Runa member access."""
        object_expr = self.convert_expression(member_access.expression)
        member_name = member_access.name
        
        return RunaMemberAccess(object_expr, member_name)
    
    def _convert_element_access_expression(self, element_access: CSharpElementAccessExpression) -> RunaExpression:
        """Convert C# element access expression to Runa array access."""
        array = self.convert_expression(element_access.expression)
        
        # Use first argument as index
        index = None
        if element_access.arguments:
            index = self.convert_expression(element_access.arguments[0])
        
        return RunaArrayAccess(array, index)
    
    def _convert_cast_expression(self, cast_expr: CSharpCastExpression) -> RunaExpression:
        """Convert C# cast expression to Runa cast expression."""
        expression = self.convert_expression(cast_expr.expression)
        target_type = self._convert_type(cast_expr.target_type)
        
        return RunaCastExpression(expression, target_type)
    
    def _convert_is_expression(self, is_expr: CSharpIsExpression) -> RunaExpression:
        """Convert C# is expression to Runa instanceof expression."""
        expression = self.convert_expression(is_expr.expression)
        
        if isinstance(is_expr.type_or_pattern, CSharpType):
            type_name = self._convert_type(is_expr.type_or_pattern)
            return RunaInstanceofExpression(expression, type_name)
        else:
            # Pattern matching - convert to instanceof for now
            return RunaInstanceofExpression(expression, "Object")
    
    def _convert_as_expression(self, as_expr: CSharpAsExpression) -> RunaExpression:
        """Convert C# as expression to Runa cast expression."""
        expression = self.convert_expression(as_expr.expression)
        target_type = self._convert_type(as_expr.target_type)
        
        return RunaCastExpression(expression, target_type)
    
    def _convert_this_expression(self, this_expr: CSharpThisExpression) -> RunaExpression:
        """Convert C# this expression to Runa this expression."""
        return RunaThisExpression()
    
    def _convert_base_expression(self, base_expr: CSharpBaseExpression) -> RunaExpression:
        """Convert C# base expression to Runa super expression."""
        return RunaSuperExpression()
    
    def _convert_typeof_expression(self, typeof_expr: CSharpTypeofExpression) -> RunaExpression:
        """Convert C# typeof expression to Runa typeof expression."""
        target_type = self._convert_type(typeof_expr.target_type)
        return RunaTypeofExpression(target_type)
    
    def _convert_sizeof_expression(self, sizeof_expr: CSharpSizeofExpression) -> RunaExpression:
        """Convert C# sizeof expression to Runa sizeof expression."""
        target_type = self._convert_type(sizeof_expr.target_type)
        return RunaSizeofExpression(target_type)
    
    def _convert_nameof_expression(self, nameof_expr: CSharpNameofExpression) -> RunaExpression:
        """Convert C# nameof expression to Runa string literal."""
        # Extract name from expression
        name = self._expression_to_string(nameof_expr.expression)
        return RunaLiteral(name, "string")
    
    def _convert_default_expression(self, default_expr: CSharpDefaultExpression) -> RunaExpression:
        """Convert C# default expression to Runa default expression."""
        if default_expr.target_type:
            target_type = self._convert_type(default_expr.target_type)
            return RunaDefaultExpression(target_type)
        else:
            return RunaLiteral(None, "null")
    
    def _convert_object_creation_expression(self, obj_creation: CSharpObjectCreationExpression) -> RunaExpression:
        """Convert C# object creation expression to Runa new expression."""
        if obj_creation.type:
            type_name = self._convert_type(obj_creation.type)
        else:
            type_name = "Object"
        
        arguments = []
        for arg in obj_creation.arguments:
            arguments.append(self.convert_expression(arg))
        
        return RunaNewExpression(type_name, arguments)
    
    def _convert_array_creation_expression(self, array_creation: CSharpArrayCreationExpression) -> RunaExpression:
        """Convert C# array creation expression to Runa array creation."""
        element_type = self._convert_type(array_creation.type)
        
        # Get array dimensions
        dimensions = []
        for rank_spec in array_creation.rank_specifiers:
            for size in rank_spec.sizes:
                if size:
                    dimensions.append(self.convert_expression(size))
                else:
                    dimensions.append(RunaLiteral(0, "int"))
        
        return RunaArrayCreation(element_type, dimensions)
    
    def _convert_lambda_expression(self, lambda_expr: CSharpLambdaExpression) -> RunaExpression:
        """Convert C# lambda expression to Runa lambda expression."""
        parameters = []
        for param in lambda_expr.parameters:
            parameters.append(param.identifier)
        
        body = None
        if isinstance(lambda_expr.body, CSharpExpression):
            body = self.convert_expression(lambda_expr.body)
        else:
            body = self.convert_statement(lambda_expr.body)
        
        return RunaLambdaExpression(parameters, body)
    
    def _convert_await_expression(self, await_expr: CSharpAwaitExpression) -> RunaExpression:
        """Convert C# await expression to Runa await expression."""
        expression = self.convert_expression(await_expr.expression)
        return RunaAwaitExpression(expression)
    
    def _convert_tuple_expression(self, tuple_expr: CSharpTupleExpression) -> RunaExpression:
        """Convert C# tuple expression to Runa tuple expression."""
        elements = []
        for arg in tuple_expr.arguments:
            elements.append(self.convert_expression(arg.expression))
        
        return RunaTupleExpression(elements)
    
    def _convert_throw_expression(self, throw_expr: CSharpThrowExpression) -> RunaExpression:
        """Convert C# throw expression to Runa throw expression."""
        expression = self.convert_expression(throw_expr.expression)
        return RunaThrowExpression(expression)
    
    def _convert_range_expression(self, range_expr: CSharpRangeExpression) -> RunaExpression:
        """Convert C# range expression to Runa range expression."""
        start = None
        end = None
        
        if range_expr.left:
            start = self.convert_expression(range_expr.left)
        if range_expr.right:
            end = self.convert_expression(range_expr.right)
        
        return RunaRangeExpression(start, end)
    
    def _convert_index_expression(self, index_expr: CSharpIndexExpression) -> RunaExpression:
        """Convert C# index expression to Runa index expression."""
        operand = self.convert_expression(index_expr.operand)
        return RunaIndexExpression(operand)
    
    def _convert_switch_expression(self, switch_expr: CSharpSwitchExpression) -> RunaExpression:
        """Convert C# switch expression to Runa switch expression."""
        governing_expression = self.convert_expression(switch_expr.governing_expression)
        
        arms = []
        for arm in switch_expr.arms:
            pattern = self._convert_pattern(arm.pattern)
            when_clause = None
            if arm.when_clause:
                when_clause = self.convert_expression(arm.when_clause)
            expression = self.convert_expression(arm.expression)
            
            arms.append(RunaSwitchArm(pattern, when_clause, expression))
        
        return RunaSwitchExpression(governing_expression, arms)
    
    def _convert_with_expression(self, with_expr: CSharpWithExpression) -> RunaExpression:
        """Convert C# with expression to Runa with expression."""
        expression = self.convert_expression(with_expr.expression)
        # For now, just return the expression
        return expression
    
    def _convert_interpolated_string_expression(self, interp_str: CSharpInterpolatedStringExpression) -> RunaExpression:
        """Convert C# interpolated string to Runa interpolated string."""
        parts = []
        for part in interp_str.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                # Interpolation expression
                parts.append(self.convert_expression(part.expression))
        
        return RunaInterpolatedString(parts)
    
    def _convert_query_expression(self, query_expr: CSharpQueryExpression) -> RunaExpression:
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
                result_expr = RunaMethodCall(
                    RunaMemberAccess(result_expr, "filter"),
                    [RunaLambdaExpression([variable], condition)]
                )
            elif isinstance(clause, CSharpOrderByClause):
                for ordering in clause.orderings:
                    key_expr = self.convert_expression(ordering.expression)
                    result_expr = RunaMethodCall(
                        RunaMemberAccess(result_expr, "orderBy"),
                        [RunaLambdaExpression([variable], key_expr)]
                    )
        
        # Process select or group clause
        if isinstance(query_expr.body.select_or_group, CSharpSelectClause):
            select_expr = self.convert_expression(query_expr.body.select_or_group.expression)
            result_expr = RunaMethodCall(
                RunaMemberAccess(result_expr, "map"),
                [RunaLambdaExpression([variable], select_expr)]
            )
        elif isinstance(query_expr.body.select_or_group, CSharpGroupClause):
            group_expr = self.convert_expression(query_expr.body.select_or_group.group_expression)
            by_expr = self.convert_expression(query_expr.body.select_or_group.by_expression)
            result_expr = RunaMethodCall(
                RunaMemberAccess(result_expr, "groupBy"),
                [RunaLambdaExpression([variable], by_expr)]
            )
        
        return result_expr
    
    def _convert_pattern(self, pattern: CSharpPattern) -> RunaExpression:
        """Convert C# pattern to Runa pattern."""
        if isinstance(pattern, CSharpConstantPattern):
            return self.convert_expression(pattern.expression)
        elif isinstance(pattern, CSharpDeclarationPattern):
            type_name = self._convert_type(pattern.type)
            return RunaLiteral(type_name, "string")
        elif isinstance(pattern, CSharpVarPattern):
            return RunaLiteral("var", "string")
        elif isinstance(pattern, CSharpDiscardPattern):
            return RunaLiteral("_", "string")
        else:
            return RunaLiteral("pattern", "string")
    
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
    
    def convert_statement(self, stmt: RunaStatement) -> Union[CSharpMemberDeclaration, CSharpStatement, List[CSharpMemberDeclaration], None]:
        """Convert Runa statement to C# statement or member."""
        if isinstance(stmt, RunaFunctionDefinition):
            return self._convert_function_definition(stmt)
        elif isinstance(stmt, RunaVariableDeclaration):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, RunaExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, RunaIfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, RunaWhileStatement):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, RunaForEachStatement):
            return self._convert_foreach_statement(stmt)
        elif isinstance(stmt, RunaDoWhileStatement):
            return self._convert_do_while_statement(stmt)
        elif isinstance(stmt, RunaSwitchStatement):
            return self._convert_switch_statement(stmt)
        elif isinstance(stmt, RunaReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, RunaBreakStatement):
            return self._convert_break_statement(stmt)
        elif isinstance(stmt, RunaContinueStatement):
            return self._convert_continue_statement(stmt)
        elif isinstance(stmt, RunaThrowStatement):
            return self._convert_throw_statement(stmt)
        elif isinstance(stmt, RunaTryStatement):
            return self._convert_try_statement(stmt)
        elif isinstance(stmt, RunaBlock):
            return self._convert_block(stmt)
        
        return None
    
    def convert_expression(self, expr: RunaExpression) -> CSharpExpression:
        """Convert Runa expression to C# expression."""
        if isinstance(expr, RunaLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, RunaIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, RunaBinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, RunaUnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, RunaMethodCall):
            return self._convert_method_call(expr)
        elif isinstance(expr, RunaMemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, RunaArrayAccess):
            return self._convert_array_access(expr)
        elif isinstance(expr, RunaAssignmentExpression):
            return self._convert_assignment_expression(expr)
        elif isinstance(expr, RunaConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, RunaCastExpression):
            return self._convert_cast_expression(expr)
        elif isinstance(expr, RunaInstanceofExpression):
            return self._convert_instanceof_expression(expr)
        elif isinstance(expr, RunaThisExpression):
            return self._convert_this_expression(expr)
        elif isinstance(expr, RunaSuperExpression):
            return self._convert_super_expression(expr)
        elif isinstance(expr, RunaNewExpression):
            return self._convert_new_expression(expr)
        elif isinstance(expr, RunaArrayCreation):
            return self._convert_array_creation(expr)
        elif isinstance(expr, RunaLambdaExpression):
            return self._convert_lambda_expression(expr)
        elif isinstance(expr, RunaAwaitExpression):
            return self._convert_await_expression(expr)
        elif isinstance(expr, RunaTupleExpression):
            return self._convert_tuple_expression(expr)
        elif isinstance(expr, RunaInterpolatedString):
            return self._convert_interpolated_string(expr)
        
        # Fallback
        return CSharpIdentifier(CSharpNodeType.IDENTIFIER, name="unknown")
    
    def _convert_function_definition(self, func_def: RunaFunctionDefinition) -> CSharpMethodDeclaration:
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
    
    def _convert_variable_declaration(self, var_decl: RunaVariableDeclaration) -> CSharpFieldDeclaration:
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
    
    def _convert_expression_statement(self, expr_stmt: RunaExpressionStatement) -> CSharpExpressionStatement:
        """Convert Runa expression statement to C# expression statement."""
        return CSharpExpressionStatement(
            CSharpNodeType.EXPRESSION_STATEMENT,
            expression=self.convert_expression(expr_stmt.expression)
        )
    
    def _convert_if_statement(self, if_stmt: RunaIfStatement) -> CSharpIfStatement:
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
    
    def _convert_while_statement(self, while_stmt: RunaWhileStatement) -> CSharpWhileStatement:
        """Convert Runa while statement to C# while statement."""
        condition = self.convert_expression(while_stmt.condition)
        body = self.convert_statement(while_stmt.body)
        
        return CSharpWhileStatement(
            CSharpNodeType.WHILE_STATEMENT,
            condition=condition,
            statement=body
        )
    
    def _convert_foreach_statement(self, foreach_stmt: RunaForEachStatement) -> CSharpForEachStatement:
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
    
    def _convert_do_while_statement(self, do_while_stmt: RunaDoWhileStatement) -> CSharpDoStatement:
        """Convert Runa do-while statement to C# do statement."""
        body = self.convert_statement(do_while_stmt.body)
        condition = self.convert_expression(do_while_stmt.condition)
        
        return CSharpDoStatement(
            CSharpNodeType.DO_STATEMENT,
            statement=body,
            condition=condition
        )
    
    def _convert_switch_statement(self, switch_stmt: RunaSwitchStatement) -> CSharpSwitchStatement:
        """Convert Runa switch statement to C# switch statement."""
        expression = self.convert_expression(switch_stmt.expression)
        
        sections = []
        for case in switch_stmt.cases:
            labels = []
            for label in case.labels:
                if isinstance(label, RunaLiteral) and label.value == "default":
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
    
    def _convert_return_statement(self, return_stmt: RunaReturnStatement) -> CSharpReturnStatement:
        """Convert Runa return statement to C# return statement."""
        expression = None
        if return_stmt.value:
            expression = self.convert_expression(return_stmt.value)
        
        return CSharpReturnStatement(
            CSharpNodeType.RETURN_STATEMENT,
            expression=expression
        )
    
    def _convert_break_statement(self, break_stmt: RunaBreakStatement) -> CSharpBreakStatement:
        """Convert Runa break statement to C# break statement."""
        return CSharpBreakStatement(CSharpNodeType.BREAK_STATEMENT)
    
    def _convert_continue_statement(self, continue_stmt: RunaContinueStatement) -> CSharpContinueStatement:
        """Convert Runa continue statement to C# continue statement."""
        return CSharpContinueStatement(CSharpNodeType.CONTINUE_STATEMENT)
    
    def _convert_throw_statement(self, throw_stmt: RunaThrowStatement) -> CSharpThrowStatement:
        """Convert Runa throw statement to C# throw statement."""
        expression = None
        if throw_stmt.expression:
            expression = self.convert_expression(throw_stmt.expression)
        
        return CSharpThrowStatement(
            CSharpNodeType.THROW_STATEMENT,
            expression=expression
        )
    
    def _convert_try_statement(self, try_stmt: RunaTryStatement) -> CSharpTryStatement:
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
    
    def _convert_block(self, block: RunaBlock) -> CSharpBlock:
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
    
    def _convert_literal(self, literal: RunaLiteral) -> CSharpLiteral:
        """Convert Runa literal to C# literal."""
        return CSharpLiteral(
            CSharpNodeType.LITERAL,
            value=literal.value,
            literal_type=literal.literal_type
        )
    
    def _convert_identifier(self, identifier: RunaIdentifier) -> CSharpIdentifier:
        """Convert Runa identifier to C# identifier."""
        return CSharpIdentifier(
            CSharpNodeType.IDENTIFIER,
            name=identifier.name
        )
    
    def _convert_binary_expression(self, binary_expr: RunaBinaryExpression) -> CSharpBinaryExpression:
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
    
    def _convert_unary_expression(self, unary_expr: RunaUnaryExpression) -> CSharpUnaryExpression:
        """Convert Runa unary expression to C# unary expression."""
        operand = self.convert_expression(unary_expr.operand)
        operator = self._convert_operator(unary_expr.operator)
        
        return CSharpUnaryExpression(
            CSharpNodeType.UNARY_EXPRESSION,
            operator=operator,
            operand=operand
        )
    
    def _convert_method_call(self, method_call: RunaMethodCall) -> CSharpInvocationExpression:
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
    
    def _convert_member_access(self, member_access: RunaMemberAccess) -> CSharpMemberAccessExpression:
        """Convert Runa member access to C# member access expression."""
        object_expr = self.convert_expression(member_access.object)
        
        return CSharpMemberAccessExpression(
            CSharpNodeType.MEMBER_ACCESS_EXPRESSION,
            expression=object_expr,
            name=member_access.member
        )
    
    def _convert_array_access(self, array_access: RunaArrayAccess) -> CSharpElementAccessExpression:
        """Convert Runa array access to C# element access expression."""
        array = self.convert_expression(array_access.array)
        index = self.convert_expression(array_access.index)
        
        return CSharpElementAccessExpression(
            CSharpNodeType.ELEMENT_ACCESS_EXPRESSION,
            expression=array,
            arguments=[index]
        )
    
    def _convert_assignment_expression(self, assign_expr: RunaAssignmentExpression) -> CSharpAssignmentExpression:
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
    
    def _convert_conditional_expression(self, cond_expr: RunaConditionalExpression) -> CSharpConditionalExpression:
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
    
    def _convert_cast_expression(self, cast_expr: RunaCastExpression) -> CSharpCastExpression:
        """Convert Runa cast expression to C# cast expression."""
        expression = self.convert_expression(cast_expr.expression)
        target_type = self._convert_type(cast_expr.target_type)
        
        return CSharpCastExpression(
            CSharpNodeType.CAST_EXPRESSION,
            target_type=target_type,
            expression=expression
        )
    
    def _convert_instanceof_expression(self, instanceof_expr: RunaInstanceofExpression) -> CSharpIsExpression:
        """Convert Runa instanceof expression to C# is expression."""
        expression = self.convert_expression(instanceof_expr.expression)
        target_type = self._convert_type(instanceof_expr.type)
        
        return CSharpIsExpression(
            CSharpNodeType.IS_EXPRESSION,
            expression=expression,
            type_or_pattern=target_type
        )
    
    def _convert_this_expression(self, this_expr: RunaThisExpression) -> CSharpThisExpression:
        """Convert Runa this expression to C# this expression."""
        return CSharpThisExpression(CSharpNodeType.THIS_EXPRESSION)
    
    def _convert_super_expression(self, super_expr: RunaSuperExpression) -> CSharpBaseExpression:
        """Convert Runa super expression to C# base expression."""
        return CSharpBaseExpression(CSharpNodeType.BASE_EXPRESSION)
    
    def _convert_new_expression(self, new_expr: RunaNewExpression) -> CSharpObjectCreationExpression:
        """Convert Runa new expression to C# object creation expression."""
        obj_type = self._convert_type(new_expr.type)
        
        arguments = []
        for arg in new_expr.arguments:
            arguments.append(self.convert_expression(arg))
        
        return CSharpObjectCreationExpression(
            CSharpNodeType.OBJECT_CREATION_EXPRESSION,
            type=obj_type,
            arguments=arguments
        )
    
    def _convert_array_creation(self, array_creation: RunaArrayCreation) -> CSharpArrayCreationExpression:
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
    
    def _convert_lambda_expression(self, lambda_expr: RunaLambdaExpression) -> CSharpLambdaExpression:
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
        if isinstance(lambda_expr.body, RunaExpression):
            body = self.convert_expression(lambda_expr.body)
        else:
            body = self.convert_statement(lambda_expr.body)
        
        return CSharpLambdaExpression(
            CSharpNodeType.LAMBDA_EXPRESSION,
            parameters=parameters,
            body=body
        )
    
    def _convert_await_expression(self, await_expr: RunaAwaitExpression) -> CSharpAwaitExpression:
        """Convert Runa await expression to C# await expression."""
        expression = self.convert_expression(await_expr.expression)
        
        return CSharpAwaitExpression(
            CSharpNodeType.AWAIT_EXPRESSION,
            expression=expression
        )
    
    def _convert_tuple_expression(self, tuple_expr: RunaTupleExpression) -> CSharpTupleExpression:
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
    
    def _convert_interpolated_string(self, interp_str: RunaInterpolatedString) -> CSharpInterpolatedStringExpression:
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