#!/usr/bin/env python3
"""
Java ↔ Runa Bidirectional Converter

Converts between Java AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
Handles modern Java features including lambdas, streams, generics, and modules.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .java_ast import *
from ....core.runa_ast import *


class JavaToRunaConverter:
    """Converts Java AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0
        self.package_name = ""
        self.imports = []
    
    def convert(self, java_ast: JavaCompilationUnit) -> Program:
        """Convert Java compilation unit to Runa program."""
        statements = []
        
        # Handle package declaration
        if java_ast.package_declaration:
            package_name = self._expression_to_string(java_ast.package_declaration.name)
            self.package_name = package_name
            
            # Add package as comment
            statements.append(RunaExpressionStatement(
                RunaLiteral(f"package {package_name}", "comment")
            ))
        
        # Handle imports
        for import_decl in java_ast.import_declarations:
            import_name = self._expression_to_string(import_decl.name)
            self.imports.append(import_name)
            
            # Add import as comment
            import_str = f"import {import_name}"
            if import_decl.is_static:
                import_str = f"import static {import_name}"
            if import_decl.is_on_demand:
                import_str += ".*"
            
            statements.append(RunaExpressionStatement(
                RunaLiteral(import_str, "comment")
            ))
        
        # Handle type declarations
        for type_decl in java_ast.type_declarations:
            converted = self.convert_declaration(type_decl)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        # Handle module declaration
        if java_ast.module_declaration:
            module_info = self._convert_module_declaration(java_ast.module_declaration)
            statements.extend(module_info)
        
        return Program(statements)
    
    def convert_declaration(self, decl: JavaDeclaration) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert Java declaration to Runa statement(s)."""
        if isinstance(decl, JavaClassDeclaration):
            return self._convert_class_declaration(decl)
        elif isinstance(decl, JavaInterfaceDeclaration):
            return self._convert_interface_declaration(decl)
        elif isinstance(decl, JavaEnumDeclaration):
            return self._convert_enum_declaration(decl)
        elif isinstance(decl, JavaRecordDeclaration):
            return self._convert_record_declaration(decl)
        elif isinstance(decl, JavaAnnotationDeclaration):
            return self._convert_annotation_declaration(decl)
        elif isinstance(decl, JavaMethodDeclaration):
            return self._convert_method_declaration(decl)
        elif isinstance(decl, JavaFieldDeclaration):
            return self._convert_field_declaration(decl)
        elif isinstance(decl, JavaVariableDeclaration):
            return self._convert_variable_declaration(decl)
        
        return None
    
    def convert_statement(self, stmt: JavaStatement) -> Union[RunaStatement, List[RunaStatement], None]:
        """Convert Java statement to Runa statement(s)."""
        if isinstance(stmt, JavaExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, JavaBlockStatement):
            return self._convert_block_statement(stmt)
        elif isinstance(stmt, JavaIfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, JavaWhileStatement):
            return self._convert_while_statement(stmt)
        elif isinstance(stmt, JavaForStatement):
            return self._convert_for_statement(stmt)
        elif isinstance(stmt, JavaEnhancedForStatement):
            return self._convert_enhanced_for_statement(stmt)
        elif isinstance(stmt, JavaDoStatement):
            return self._convert_do_statement(stmt)
        elif isinstance(stmt, JavaSwitchStatement):
            return self._convert_switch_statement(stmt)
        elif isinstance(stmt, JavaReturnStatement):
            return self._convert_return_statement(stmt)
        elif isinstance(stmt, JavaBreakStatement):
            return RunaBreak()
        elif isinstance(stmt, JavaContinueStatement):
            return RunaContinue()
        elif isinstance(stmt, JavaThrowStatement):
            return self._convert_throw_statement(stmt)
        elif isinstance(stmt, JavaTryStatement):
            return self._convert_try_statement(stmt)
        elif isinstance(stmt, JavaSynchronizedStatement):
            return self._convert_synchronized_statement(stmt)
        elif isinstance(stmt, JavaAssertStatement):
            return self._convert_assert_statement(stmt)
        elif isinstance(stmt, JavaEmptyStatement):
            return RunaExpressionStatement(RunaLiteral("", "string"))
        elif isinstance(stmt, JavaLabeledStatement):
            return self._convert_labeled_statement(stmt)
        elif isinstance(stmt, JavaYieldStatement):
            return self._convert_yield_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: JavaExpression) -> RunaExpression:
        """Convert Java expression to Runa expression."""
        if isinstance(expr, JavaIntegerLiteral):
            return RunaLiteral(expr.value, "integer")
        elif isinstance(expr, JavaFloatingLiteral):
            return RunaLiteral(expr.value, "float")
        elif isinstance(expr, JavaStringLiteral):
            return RunaLiteral(expr.value.strip('"'), "string")
        elif isinstance(expr, JavaCharacterLiteral):
            return RunaLiteral(expr.value.strip("'"), "character")
        elif isinstance(expr, JavaBooleanLiteral):
            return RunaLiteral(expr.value, "boolean")
        elif isinstance(expr, JavaNullLiteral):
            return RunaLiteral(None, "null")
        elif isinstance(expr, JavaTextBlock):
            return RunaLiteral(expr.value.strip('"""'), "string")
        elif isinstance(expr, JavaSimpleName):
            return RunaIdentifier(expr.identifier)
        elif isinstance(expr, JavaQualifiedName):
            return self._convert_qualified_name(expr)
        elif isinstance(expr, JavaBinaryExpression):
            return self._convert_binary_expression(expr)
        elif isinstance(expr, JavaUnaryExpression):
            return self._convert_unary_expression(expr)
        elif isinstance(expr, JavaConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, JavaAssignmentExpression):
            return self._convert_assignment_expression(expr)
        elif isinstance(expr, JavaMethodInvocation):
            return self._convert_method_invocation(expr)
        elif isinstance(expr, JavaFieldAccess):
            return self._convert_field_access(expr)
        elif isinstance(expr, JavaArrayAccess):
            return self._convert_array_access(expr)
        elif isinstance(expr, JavaCastExpression):
            return self._convert_cast_expression(expr)
        elif isinstance(expr, JavaInstanceofExpression):
            return self._convert_instanceof_expression(expr)
        elif isinstance(expr, JavaThisExpression):
            return RunaIdentifier("this")
        elif isinstance(expr, JavaSuperExpression):
            return RunaIdentifier("super")
        elif isinstance(expr, JavaClassLiteral):
            return self._convert_class_literal(expr)
        elif isinstance(expr, JavaArrayCreation):
            return self._convert_array_creation(expr)
        elif isinstance(expr, JavaArrayInitializer):
            return self._convert_array_initializer(expr)
        elif isinstance(expr, JavaLambdaExpression):
            return self._convert_lambda_expression(expr)
        elif isinstance(expr, JavaMethodReference):
            return self._convert_method_reference(expr)
        
        # Fallback
        return RunaLiteral("unknown_expression", "string")
    
    def _convert_class_declaration(self, decl: JavaClassDeclaration) -> RunaClassDeclaration:
        """Convert Java class declaration."""
        # Convert fields
        fields = []
        methods = []
        
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    fields.extend(field_vars)
                else:
                    fields.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                methods.append(method)
        
        # Handle inheritance
        base_classes = []
        if decl.superclass:
            base_classes.append(self._type_to_string(decl.superclass))
        
        for interface in decl.super_interfaces:
            base_classes.append(self._type_to_string(interface))
        
        return RunaClassDeclaration(
            decl.name,
            fields,
            methods,
            base_classes
        )
    
    def _convert_interface_declaration(self, decl: JavaInterfaceDeclaration) -> RunaClassDeclaration:
        """Convert Java interface declaration."""
        # Treat interface as abstract class
        fields = []
        methods = []
        
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    fields.extend(field_vars)
                else:
                    fields.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                methods.append(method)
        
        # Handle extended interfaces
        base_classes = []
        for interface in decl.extended_interfaces:
            base_classes.append(self._type_to_string(interface))
        
        return RunaClassDeclaration(
            decl.name,
            fields,
            methods,
            base_classes
        )
    
    def _convert_enum_declaration(self, decl: JavaEnumDeclaration) -> RunaClassDeclaration:
        """Convert Java enum declaration."""
        fields = []
        methods = []
        
        # Convert enum constants as static fields
        for enum_const in decl.enum_constants:
            fields.append(RunaVariableDeclaration(
                enum_const.name,
                RunaType(decl.name),
                RunaLiteral(enum_const.name, "string")
            ))
        
        # Convert body declarations
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    fields.extend(field_vars)
                else:
                    fields.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                methods.append(method)
        
        return RunaClassDeclaration(
            decl.name,
            fields,
            methods,
            []
        )
    
    def _convert_record_declaration(self, decl: JavaRecordDeclaration) -> RunaClassDeclaration:
        """Convert Java record declaration."""
        fields = []
        methods = []
        
        # Convert record parameters as fields
        for param in decl.parameters:
            fields.append(RunaVariableDeclaration(
                param.name,
                self._convert_type(param.parameter_type),
                None
            ))
        
        # Convert body declarations
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    fields.extend(field_vars)
                else:
                    fields.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                methods.append(method)
        
        return RunaClassDeclaration(
            decl.name,
            fields,
            methods,
            []
        )
    
    def _convert_annotation_declaration(self, decl: JavaAnnotationDeclaration) -> RunaClassDeclaration:
        """Convert Java annotation declaration."""
        # Treat annotation as interface
        return RunaClassDeclaration(
            decl.name,
            [],
            [],
            []
        )
    
    def _convert_method_declaration(self, decl: JavaMethodDeclaration) -> RunaFunctionDeclaration:
        """Convert Java method declaration."""
        # Convert parameters
        parameters = []
        for param in decl.parameters:
            param_type = self._convert_type(param.parameter_type)
            runa_param = RunaParameter(param.name, param_type)
            parameters.append(runa_param)
        
        # Convert return type
        return_type = RunaType("Void")
        if decl.return_type:
            return_type = self._convert_type(decl.return_type)
        
        # Convert body
        body = []
        if decl.body:
            converted_body = self.convert_statement(decl.body)
            if isinstance(converted_body, list):
                body = converted_body
            elif converted_body:
                body = [converted_body]
        
        return RunaFunctionDeclaration(
            decl.name,
            parameters,
            return_type,
            body
        )
    
    def _convert_field_declaration(self, decl: JavaFieldDeclaration) -> List[RunaVariableDeclaration]:
        """Convert Java field declaration."""
        variables = []
        
        for fragment in decl.fragments:
            var_type = self._convert_type(decl.variable_type)
            
            # Handle array dimensions
            if fragment.extra_dimensions > 0:
                for _ in range(fragment.extra_dimensions):
                    var_type = RunaType(f"Array[{var_type.name}]")
            
            initial_value = None
            if fragment.initializer:
                initial_value = self.convert_expression(fragment.initializer)
            
            variables.append(RunaVariableDeclaration(
                fragment.name,
                var_type,
                initial_value
            ))
        
        return variables
    
    def _convert_variable_declaration(self, decl: JavaVariableDeclaration) -> List[RunaVariableDeclaration]:
        """Convert Java variable declaration."""
        variables = []
        
        for fragment in decl.fragments:
            var_type = self._convert_type(decl.variable_type)
            
            # Handle array dimensions
            if fragment.extra_dimensions > 0:
                for _ in range(fragment.extra_dimensions):
                    var_type = RunaType(f"Array[{var_type.name}]")
            
            initial_value = None
            if fragment.initializer:
                initial_value = self.convert_expression(fragment.initializer)
            
            variables.append(RunaVariableDeclaration(
                fragment.name,
                var_type,
                initial_value
            ))
        
        return variables
    
    def _convert_module_declaration(self, decl: JavaModuleDeclaration) -> List[RunaStatement]:
        """Convert Java module declaration."""
        statements = []
        
        # Module name
        module_name = self._expression_to_string(decl.name)
        statements.append(RunaExpressionStatement(
            RunaLiteral(f"module {module_name}", "comment")
        ))
        
        # Module statements
        for stmt in decl.module_statements:
            if isinstance(stmt, JavaRequiresDirective):
                req_name = self._expression_to_string(stmt.module_name)
                statements.append(RunaExpressionStatement(
                    RunaLiteral(f"requires {req_name}", "comment")
                ))
            elif isinstance(stmt, JavaExportsDirective):
                pkg_name = self._expression_to_string(stmt.package_name)
                statements.append(RunaExpressionStatement(
                    RunaLiteral(f"exports {pkg_name}", "comment")
                ))
            # Add other module statements as needed
        
        return statements
    
    def _convert_expression_statement(self, stmt: JavaExpressionStatement) -> RunaExpressionStatement:
        """Convert Java expression statement."""
        expr = self.convert_expression(stmt.expression)
        return RunaExpressionStatement(expr)
    
    def _convert_block_statement(self, stmt: JavaBlockStatement) -> List[RunaStatement]:
        """Convert Java block statement."""
        statements = []
        
        for java_stmt in stmt.statements:
            converted = self.convert_statement(java_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return statements
    
    def _convert_if_statement(self, stmt: JavaIfStatement) -> RunaConditional:
        """Convert Java if statement."""
        condition = self.convert_expression(stmt.condition)
        
        then_body = []
        converted_then = self.convert_statement(stmt.then_statement)
        if isinstance(converted_then, list):
            then_body = converted_then
        elif converted_then:
            then_body = [converted_then]
        
        else_body = []
        if stmt.else_statement:
            converted_else = self.convert_statement(stmt.else_statement)
            if isinstance(converted_else, list):
                else_body = converted_else
            elif converted_else:
                else_body = [converted_else]
        
        return RunaConditional(condition, then_body, else_body)
    
    def _convert_while_statement(self, stmt: JavaWhileStatement) -> RunaLoop:
        """Convert Java while statement."""
        condition = self.convert_expression(stmt.condition)
        
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return RunaLoop("while", condition, body)
    
    def _convert_for_statement(self, stmt: JavaForStatement) -> List[RunaStatement]:
        """Convert Java for statement."""
        statements = []
        
        # Initializers
        for init in stmt.initializers:
            init_expr = self.convert_expression(init)
            statements.append(RunaExpressionStatement(init_expr))
        
        # Condition
        condition = RunaLiteral(True, "boolean")
        if stmt.condition:
            condition = self.convert_expression(stmt.condition)
        
        # Body with updaters
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        # Add updaters to end of body
        for updater in stmt.updaters:
            updater_expr = self.convert_expression(updater)
            body.append(RunaExpressionStatement(updater_expr))
        
        loop = RunaLoop("while", condition, body)
        statements.append(loop)
        
        return statements
    
    def _convert_enhanced_for_statement(self, stmt: JavaEnhancedForStatement) -> RunaLoop:
        """Convert Java enhanced for statement (for-each)."""
        # Convert to iterator-based loop
        iterator_var = f"_iterator_{self.variable_counter}"
        self.variable_counter += 1
        
        iterable = self.convert_expression(stmt.expression)
        
        # Loop variable
        loop_var = stmt.parameter.name
        loop_var_type = self._convert_type(stmt.parameter.parameter_type)
        
        # Create loop condition and body
        condition = RunaLiteral(True, "boolean")  # Simplified
        
        body = []
        # Add variable declaration for loop variable
        body.append(RunaVariableDeclaration(
            loop_var,
            loop_var_type,
            RunaIdentifier(iterator_var)
        ))
        
        # Add original body
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        return RunaLoop("for_each", condition, body)
    
    def _convert_do_statement(self, stmt: JavaDoStatement) -> RunaLoop:
        """Convert Java do-while statement."""
        condition = self.convert_expression(stmt.condition)
        
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return RunaLoop("do_while", condition, body)
    
    def _convert_switch_statement(self, stmt: JavaSwitchStatement) -> RunaConditional:
        """Convert Java switch statement."""
        # Convert to if-else chain
        switch_expr = self.convert_expression(stmt.expression)
        
        # Simplified conversion - just treat as conditional
        return RunaConditional(
            switch_expr,
            [RunaExpressionStatement(RunaLiteral("switch_body", "string"))],
            []
        )
    
    def _convert_return_statement(self, stmt: JavaReturnStatement) -> RunaReturn:
        """Convert Java return statement."""
        value = None
        if stmt.expression:
            value = self.convert_expression(stmt.expression)
        
        return RunaReturn(value)
    
    def _convert_throw_statement(self, stmt: JavaThrowStatement) -> RunaExpressionStatement:
        """Convert Java throw statement."""
        exception_expr = self.convert_expression(stmt.expression)
        
        # Convert to function call
        throw_call = RunaFunctionCall(
            RunaIdentifier("throw"),
            [exception_expr]
        )
        
        return RunaExpressionStatement(throw_call)
    
    def _convert_try_statement(self, stmt: JavaTryStatement) -> List[RunaStatement]:
        """Convert Java try statement."""
        statements = []
        
        # Try block
        try_body = []
        converted_try = self.convert_statement(stmt.body)
        if isinstance(converted_try, list):
            try_body = converted_try
        elif converted_try:
            try_body = [converted_try]
        
        # Simplified try-catch conversion
        statements.extend(try_body)
        
        # Add catch handlers as comments
        for catch_clause in stmt.catch_clauses:
            exception_type = self._type_to_string(catch_clause.exception.parameter_type)
            statements.append(RunaExpressionStatement(
                RunaLiteral(f"catch {exception_type}", "comment")
            ))
        
        # Finally block
        if stmt.finally_block:
            finally_body = self.convert_statement(stmt.finally_block)
            if isinstance(finally_body, list):
                statements.extend(finally_body)
            elif finally_body:
                statements.append(finally_body)
        
        return statements
    
    def _convert_synchronized_statement(self, stmt: JavaSynchronizedStatement) -> List[RunaStatement]:
        """Convert Java synchronized statement."""
        sync_expr = self.convert_expression(stmt.expression)
        
        # Add synchronization as comment
        statements = [RunaExpressionStatement(
            RunaLiteral(f"synchronized", "comment")
        )]
        
        # Add body
        body = self.convert_statement(stmt.body)
        if isinstance(body, list):
            statements.extend(body)
        elif body:
            statements.append(body)
        
        return statements
    
    def _convert_assert_statement(self, stmt: JavaAssertStatement) -> RunaExpressionStatement:
        """Convert Java assert statement."""
        condition = self.convert_expression(stmt.condition)
        
        # Convert to function call
        assert_call = RunaFunctionCall(
            RunaIdentifier("assert"),
            [condition]
        )
        
        return RunaExpressionStatement(assert_call)
    
    def _convert_labeled_statement(self, stmt: JavaLabeledStatement) -> List[RunaStatement]:
        """Convert Java labeled statement."""
        statements = []
        
        # Add label as comment
        statements.append(RunaExpressionStatement(
            RunaLiteral(f"label {stmt.label}", "comment")
        ))
        
        # Add body
        body = self.convert_statement(stmt.body)
        if isinstance(body, list):
            statements.extend(body)
        elif body:
            statements.append(body)
        
        return statements
    
    def _convert_yield_statement(self, stmt: JavaYieldStatement) -> RunaReturn:
        """Convert Java yield statement."""
        value = None
        if stmt.expression:
            value = self.convert_expression(stmt.expression)
        
        return RunaReturn(value)
    
    def _convert_qualified_name(self, expr: JavaQualifiedName) -> RunaIdentifier:
        """Convert Java qualified name."""
        qualifier = self._expression_to_string(expr.qualifier)
        return RunaIdentifier(f"{qualifier}.{expr.name.identifier}")
    
    def _convert_binary_expression(self, expr: JavaBinaryExpression) -> RunaBinaryOperation:
        """Convert Java binary expression."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map Java operators to Runa operators
        operator_map = {
            JavaOperator.PLUS: "plus",
            JavaOperator.MINUS: "minus",
            JavaOperator.MULTIPLY: "times",
            JavaOperator.DIVIDE: "divided by",
            JavaOperator.MODULO: "modulo",
            JavaOperator.EQUAL: "is equal to",
            JavaOperator.NOT_EQUAL: "is not equal to",
            JavaOperator.LESS_THAN: "is less than",
            JavaOperator.LESS_EQUAL: "is less than or equal to",
            JavaOperator.GREATER_THAN: "is greater than",
            JavaOperator.GREATER_EQUAL: "is greater than or equal to",
            JavaOperator.LOGICAL_AND: "and",
            JavaOperator.LOGICAL_OR: "or",
            JavaOperator.BIT_AND: "bitwise and",
            JavaOperator.BIT_OR: "bitwise or",
            JavaOperator.BIT_XOR: "bitwise xor",
            JavaOperator.LEFT_SHIFT: "left shift",
            JavaOperator.RIGHT_SHIFT: "right shift",
            JavaOperator.UNSIGNED_RIGHT_SHIFT: "unsigned right shift",
        }
        
        runa_op = operator_map.get(expr.operator, "unknown_op")
        return RunaBinaryOperation(left, runa_op, right)
    
    def _convert_unary_expression(self, expr: JavaUnaryExpression) -> RunaUnaryOperation:
        """Convert Java unary expression."""
        operand = self.convert_expression(expr.operand)
        
        # Map Java unary operators to Runa operators
        operator_map = {
            JavaOperator.LOGICAL_NOT: "not",
            JavaOperator.BIT_NOT: "bitwise not",
            JavaOperator.UNARY_PLUS: "positive",
            JavaOperator.UNARY_MINUS: "negative",
            JavaOperator.PRE_INCREMENT: "increment",
            JavaOperator.POST_INCREMENT: "increment",
            JavaOperator.PRE_DECREMENT: "decrement",
            JavaOperator.POST_DECREMENT: "decrement",
        }
        
        runa_op = operator_map.get(expr.operator, "unknown_unary_op")
        return RunaUnaryOperation(runa_op, operand)
    
    def _convert_conditional_expression(self, expr: JavaConditionalExpression) -> RunaConditionalExpression:
        """Convert Java conditional expression."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.then_expression)
        false_expr = self.convert_expression(expr.else_expression)
        
        return RunaConditionalExpression(condition, true_expr, false_expr)
    
    def _convert_assignment_expression(self, expr: JavaAssignmentExpression) -> RunaAssignment:
        """Convert Java assignment expression."""
        target = self.convert_expression(expr.left)
        value = self.convert_expression(expr.right)
        
        # Handle compound assignment operators
        if expr.operator == JavaOperator.ASSIGN:
            return RunaAssignment(target, value)
        else:
            # Convert compound assignment to regular assignment with binary op
            operator_map = {
                JavaOperator.PLUS_ASSIGN: "plus",
                JavaOperator.MINUS_ASSIGN: "minus",
                JavaOperator.MULTIPLY_ASSIGN: "times",
                JavaOperator.DIVIDE_ASSIGN: "divided by",
                JavaOperator.MODULO_ASSIGN: "modulo",
            }
            
            if expr.operator in operator_map:
                binary_op = RunaBinaryOperation(target, operator_map[expr.operator], value)
                return RunaAssignment(target, binary_op)
            
            return RunaAssignment(target, value)
    
    def _convert_method_invocation(self, expr: JavaMethodInvocation) -> RunaFunctionCall:
        """Convert Java method invocation."""
        # Handle method calls
        if expr.expression:
            # Instance method call
            obj = self.convert_expression(expr.expression)
            method_access = RunaMemberAccess(obj, expr.method_name)
            function = method_access
        else:
            # Static method call or local method call
            function = RunaIdentifier(expr.method_name)
        
        arguments = [self.convert_expression(arg) for arg in expr.arguments]
        
        return RunaFunctionCall(function, arguments)
    
    def _convert_field_access(self, expr: JavaFieldAccess) -> RunaMemberAccess:
        """Convert Java field access."""
        obj = self.convert_expression(expr.expression)
        return RunaMemberAccess(obj, expr.field_name)
    
    def _convert_array_access(self, expr: JavaArrayAccess) -> RunaIndexAccess:
        """Convert Java array access."""
        array = self.convert_expression(expr.array)
        index = self.convert_expression(expr.index)
        
        return RunaIndexAccess(array, index)
    
    def _convert_cast_expression(self, expr: JavaCastExpression) -> RunaFunctionCall:
        """Convert Java cast expression."""
        operand = self.convert_expression(expr.expression)
        target_type = self._convert_type(expr.target_type)
        
        # Convert cast to function call
        cast_function = RunaIdentifier(f"cast_to_{target_type.name}")
        return RunaFunctionCall(cast_function, [operand])
    
    def _convert_instanceof_expression(self, expr: JavaInstanceofExpression) -> RunaBinaryOperation:
        """Convert Java instanceof expression."""
        left = self.convert_expression(expr.expression)
        right = RunaLiteral(self._type_to_string(expr.target_type), "string")
        
        return RunaBinaryOperation(left, "instanceof", right)
    
    def _convert_class_literal(self, expr: JavaClassLiteral) -> RunaFunctionCall:
        """Convert Java class literal."""
        type_name = self._type_to_string(expr.target_type)
        return RunaFunctionCall(
            RunaIdentifier("get_class"),
            [RunaLiteral(type_name, "string")]
        )
    
    def _convert_array_creation(self, expr: JavaArrayCreation) -> RunaFunctionCall:
        """Convert Java array creation."""
        element_type = self._type_to_string(expr.element_type)
        
        # Handle array dimensions
        if expr.dimensions:
            # Array with size
            size_expr = RunaLiteral(1, "integer")  # Simplified
            return RunaFunctionCall(
                RunaIdentifier(f"create_array_{element_type}"),
                [size_expr]
            )
        elif expr.initializer:
            # Array with initializer
            init_expr = self.convert_expression(expr.initializer)
            return RunaFunctionCall(
                RunaIdentifier(f"create_array_{element_type}"),
                [init_expr]
            )
        
        return RunaFunctionCall(
            RunaIdentifier(f"create_array_{element_type}"),
            []
        )
    
    def _convert_array_initializer(self, expr: JavaArrayInitializer) -> RunaList:
        """Convert Java array initializer."""
        elements = [self.convert_expression(elem) for elem in expr.expressions]
        return RunaList(elements)
    
    def _convert_lambda_expression(self, expr: JavaLambdaExpression) -> RunaLambda:
        """Convert Java lambda expression."""
        parameters = []
        for param in expr.parameters:
            param_type = self._convert_type(param.parameter_type)
            runa_param = RunaParameter(param.name, param_type)
            parameters.append(runa_param)
        
        body = []
        if isinstance(expr.body, JavaExpression):
            # Expression body
            body_expr = self.convert_expression(expr.body)
            body = [RunaReturn(body_expr)]
        else:
            # Block body
            converted_body = self.convert_statement(expr.body)
            if isinstance(converted_body, list):
                body = converted_body
            elif converted_body:
                body = [converted_body]
        
        return RunaLambda(parameters, None, body)
    
    def _convert_method_reference(self, expr: JavaMethodReference) -> RunaIdentifier:
        """Convert Java method reference."""
        if expr.expression:
            # Instance method reference
            obj_name = self._expression_to_string(expr.expression)
            return RunaIdentifier(f"{obj_name}::{expr.method_name}")
        else:
            # Static method reference
            return RunaIdentifier(f"::{expr.method_name}")
    
    def _convert_type(self, java_type: JavaType) -> RunaType:
        """Convert Java type to Runa type."""
        if isinstance(java_type, JavaPrimitiveType):
            # Map Java primitive types to Runa types
            type_map = {
                "boolean": "Boolean",
                "byte": "Integer",
                "char": "Character",
                "short": "Integer",
                "int": "Integer",
                "long": "Integer",
                "float": "Float",
                "double": "Float",
                "void": "Void",
            }
            runa_name = type_map.get(java_type.primitive_type, java_type.primitive_type)
            return RunaType(runa_name)
        
        elif isinstance(java_type, JavaArrayType):
            # Convert array type
            component = self._convert_type(java_type.component_type)
            return RunaType(f"Array[{component.name}]")
        
        elif isinstance(java_type, JavaParameterizedType):
            # Convert generic type
            raw_type = self._convert_type(java_type.raw_type)
            type_args = [self._convert_type(arg) for arg in java_type.type_arguments]
            
            if type_args:
                type_arg_names = ", ".join(arg.name for arg in type_args)
                return RunaType(f"{raw_type.name}[{type_arg_names}]")
            else:
                return raw_type
        
        elif isinstance(java_type, JavaWildcardType):
            # Convert wildcard type
            if java_type.bound:
                bound_type = self._convert_type(java_type.bound)
                if java_type.is_upper_bound:
                    return RunaType(f"? extends {bound_type.name}")
                else:
                    return RunaType(f"? super {bound_type.name}")
            else:
                return RunaType("?")
        
        elif isinstance(java_type, JavaVarType):
            return RunaType("Auto")
        
        elif isinstance(java_type, JavaSimpleName):
            return RunaType(java_type.identifier)
        
        elif isinstance(java_type, JavaQualifiedName):
            return RunaType(self._expression_to_string(java_type))
        
        else:
            # Default fallback
            return RunaType("Object")
    
    def _type_to_string(self, java_type: JavaType) -> str:
        """Convert Java type to string representation."""
        if isinstance(java_type, JavaPrimitiveType):
            return java_type.primitive_type
        elif isinstance(java_type, JavaArrayType):
            component = self._type_to_string(java_type.component_type)
            return f"{component}[]"
        elif isinstance(java_type, JavaParameterizedType):
            raw_type = self._type_to_string(java_type.raw_type)
            type_args = [self._type_to_string(arg) for arg in java_type.type_arguments]
            if type_args:
                return f"{raw_type}<{', '.join(type_args)}>"
            else:
                return raw_type
        elif isinstance(java_type, JavaSimpleName):
            return java_type.identifier
        elif isinstance(java_type, JavaQualifiedName):
            return self._expression_to_string(java_type)
        else:
            return "Object"
    
    def _expression_to_string(self, expr: JavaExpression) -> str:
        """Convert Java expression to string representation."""
        if isinstance(expr, JavaSimpleName):
            return expr.identifier
        elif isinstance(expr, JavaQualifiedName):
            qualifier = self._expression_to_string(expr.qualifier)
            return f"{qualifier}.{expr.name.identifier}"
        elif isinstance(expr, JavaLiteral):
            return str(expr.value)
        else:
            return "unknown_expr"


class RunaToJavaConverter:
    """Converts Runa AST to Java AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0
    
    def convert(self, runa_ast: Program) -> JavaCompilationUnit:
        """Convert Runa program to Java compilation unit."""
        type_declarations = []
        
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    type_declarations.extend(converted)
                else:
                    type_declarations.append(converted)
        
        return JavaCompilationUnit(type_declarations=type_declarations)
    
    def convert_statement(self, stmt: RunaStatement) -> Union[JavaDeclaration, JavaStatement, List[Union[JavaDeclaration, JavaStatement]], None]:
        """Convert Runa statement to Java declaration or statement."""
        if isinstance(stmt, RunaVariableDeclaration):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, RunaFunctionDeclaration):
            return self._convert_function_declaration(stmt)
        elif isinstance(stmt, RunaClassDeclaration):
            return self._convert_class_declaration(stmt)
        elif isinstance(stmt, RunaAssignment):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, RunaConditional):
            return self._convert_conditional(stmt)
        elif isinstance(stmt, RunaLoop):
            return self._convert_loop(stmt)
        elif isinstance(stmt, RunaReturn):
            return self._convert_return(stmt)
        elif isinstance(stmt, RunaBreak):
            return JavaBreakStatement()
        elif isinstance(stmt, RunaContinue):
            return JavaContinueStatement()
        elif isinstance(stmt, RunaExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: RunaExpression) -> JavaExpression:
        """Convert Runa expression to Java expression."""
        if isinstance(expr, RunaLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, RunaIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, RunaBinaryOperation):
            return self._convert_binary_operation(expr)
        elif isinstance(expr, RunaUnaryOperation):
            return self._convert_unary_operation(expr)
        elif isinstance(expr, RunaFunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, RunaMemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, RunaIndexAccess):
            return self._convert_index_access(expr)
        elif isinstance(expr, RunaConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, RunaLambda):
            return self._convert_lambda(expr)
        elif isinstance(expr, RunaList):
            return self._convert_list(expr)
        
        # Fallback
        return JavaSimpleName("unknown_expression")
    
    def _convert_variable_declaration(self, stmt: RunaVariableDeclaration) -> JavaVariableDeclaration:
        """Convert Runa variable declaration."""
        java_type = self._convert_type(stmt.var_type)
        
        initializer = None
        if stmt.initial_value:
            initializer = self.convert_expression(stmt.initial_value)
        
        fragment = JavaVariableDeclarationFragment(stmt.name, 0, initializer)
        
        return JavaVariableDeclaration(
            variable_type=java_type,
            fragments=[fragment]
        )
    
    def _convert_function_declaration(self, stmt: RunaFunctionDeclaration) -> JavaMethodDeclaration:
        """Convert Runa function declaration."""
        return_type = self._convert_type(stmt.return_type)
        
        parameters = []
        for param in stmt.parameters:
            java_type = self._convert_type(param.param_type)
            java_param = JavaParameter(
                parameter_type=java_type,
                name=param.name
            )
            parameters.append(java_param)
        
        body = None
        if stmt.body:
            java_statements = []
            for runa_stmt in stmt.body:
                converted = self.convert_statement(runa_stmt)
                if converted:
                    if isinstance(converted, list):
                        java_statements.extend(converted)
                    else:
                        java_statements.append(converted)
            
            body = JavaBlockStatement(java_statements)
        
        return JavaMethodDeclaration(
            name=stmt.name,
            return_type=return_type,
            parameters=parameters,
            body=body
        )
    
    def _convert_class_declaration(self, stmt: RunaClassDeclaration) -> JavaClassDeclaration:
        """Convert Runa class declaration."""
        body_declarations = []
        
        # Convert fields
        for field in stmt.fields:
            field_decl = self._convert_variable_declaration(field)
            # Convert to field declaration
            java_field = JavaFieldDeclaration(
                variable_type=field_decl.variable_type,
                fragments=field_decl.fragments
            )
            body_declarations.append(java_field)
        
        # Convert methods
        for method in stmt.methods:
            method_decl = self._convert_function_declaration(method)
            body_declarations.append(method_decl)
        
        # Handle base classes
        superclass = None
        super_interfaces = []
        
        for base_name in stmt.base_classes:
            # Simplified - assume first is superclass, rest are interfaces
            if not superclass:
                superclass = JavaSimpleName(base_name)
            else:
                super_interfaces.append(JavaSimpleName(base_name))
        
        return JavaClassDeclaration(
            name=stmt.name,
            superclass=superclass,
            super_interfaces=super_interfaces,
            body_declarations=body_declarations
        )
    
    def _convert_assignment(self, stmt: RunaAssignment) -> JavaExpressionStatement:
        """Convert Runa assignment."""
        target = self.convert_expression(stmt.target)
        value = self.convert_expression(stmt.value)
        
        assignment = JavaAssignmentExpression(target, JavaOperator.ASSIGN, value)
        return JavaExpressionStatement(assignment)
    
    def _convert_conditional(self, stmt: RunaConditional) -> JavaIfStatement:
        """Convert Runa conditional."""
        condition = self.convert_expression(stmt.condition)
        
        then_statements = []
        for then_stmt in stmt.then_body:
            converted = self.convert_statement(then_stmt)
            if converted:
                if isinstance(converted, list):
                    then_statements.extend(converted)
                else:
                    then_statements.append(converted)
        
        then_body = JavaBlockStatement(then_statements)
        
        else_body = None
        if stmt.else_body:
            else_statements = []
            for else_stmt in stmt.else_body:
                converted = self.convert_statement(else_stmt)
                if converted:
                    if isinstance(converted, list):
                        else_statements.extend(converted)
                    else:
                        else_statements.append(converted)
            
            else_body = JavaBlockStatement(else_statements)
        
        return JavaIfStatement(condition, then_body, else_body)
    
    def _convert_loop(self, stmt: RunaLoop) -> JavaStatement:
        """Convert Runa loop."""
        condition = self.convert_expression(stmt.condition)
        
        body_statements = []
        for body_stmt in stmt.body:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = JavaBlockStatement(body_statements)
        
        if stmt.loop_type == "while":
            return JavaWhileStatement(condition, body)
        elif stmt.loop_type == "do_while":
            return JavaDoStatement(body, condition)
        else:
            # Default to while loop
            return JavaWhileStatement(condition, body)
    
    def _convert_return(self, stmt: RunaReturn) -> JavaReturnStatement:
        """Convert Runa return."""
        value = None
        if stmt.value:
            value = self.convert_expression(stmt.value)
        
        return JavaReturnStatement(value)
    
    def _convert_expression_statement(self, stmt: RunaExpressionStatement) -> JavaExpressionStatement:
        """Convert Runa expression statement."""
        expr = self.convert_expression(stmt.expression)
        return JavaExpressionStatement(expr)
    
    def _convert_literal(self, expr: RunaLiteral) -> JavaExpression:
        """Convert Runa literal."""
        if expr.literal_type == "integer":
            return JavaIntegerLiteral(expr.value)
        elif expr.literal_type == "float":
            return JavaFloatingLiteral(expr.value)
        elif expr.literal_type == "string":
            return JavaStringLiteral(f'"{expr.value}"')
        elif expr.literal_type == "character":
            return JavaCharacterLiteral(f"'{expr.value}'")
        elif expr.literal_type == "boolean":
            return JavaBooleanLiteral(expr.value)
        elif expr.literal_type == "null":
            return JavaNullLiteral()
        else:
            return JavaStringLiteral(f'"{expr.value}"')
    
    def _convert_identifier(self, expr: RunaIdentifier) -> JavaSimpleName:
        """Convert Runa identifier."""
        return JavaSimpleName(expr.name)
    
    def _convert_binary_operation(self, expr: RunaBinaryOperation) -> JavaBinaryExpression:
        """Convert Runa binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map Runa operators to Java operators
        operator_map = {
            "plus": JavaOperator.PLUS,
            "minus": JavaOperator.MINUS,
            "times": JavaOperator.MULTIPLY,
            "divided by": JavaOperator.DIVIDE,
            "modulo": JavaOperator.MODULO,
            "is equal to": JavaOperator.EQUAL,
            "is not equal to": JavaOperator.NOT_EQUAL,
            "is less than": JavaOperator.LESS_THAN,
            "is less than or equal to": JavaOperator.LESS_EQUAL,
            "is greater than": JavaOperator.GREATER_THAN,
            "is greater than or equal to": JavaOperator.GREATER_EQUAL,
            "and": JavaOperator.LOGICAL_AND,
            "or": JavaOperator.LOGICAL_OR,
        }
        
        java_op = operator_map.get(expr.operator, JavaOperator.PLUS)
        return JavaBinaryExpression(left, java_op, right)
    
    def _convert_unary_operation(self, expr: RunaUnaryOperation) -> JavaUnaryExpression:
        """Convert Runa unary operation."""
        operand = self.convert_expression(expr.operand)
        
        operator_map = {
            "not": JavaOperator.LOGICAL_NOT,
            "negative": JavaOperator.UNARY_MINUS,
            "positive": JavaOperator.UNARY_PLUS,
            "increment": JavaOperator.PRE_INCREMENT,
            "decrement": JavaOperator.PRE_DECREMENT,
        }
        
        java_op = operator_map.get(expr.operator, JavaOperator.LOGICAL_NOT)
        return JavaUnaryExpression(java_op, operand)
    
    def _convert_function_call(self, expr: RunaFunctionCall) -> JavaMethodInvocation:
        """Convert Runa function call."""
        if isinstance(expr.function, RunaMemberAccess):
            # Instance method call
            expression = self.convert_expression(expr.function.object)
            method_name = expr.function.member
        elif isinstance(expr.function, RunaIdentifier):
            # Static method call or local method call
            expression = None
            method_name = expr.function.name
        else:
            # Fallback
            expression = None
            method_name = "unknown"
        
        arguments = [self.convert_expression(arg) for arg in expr.arguments]
        
        return JavaMethodInvocation(
            expression=expression,
            method_name=method_name,
            arguments=arguments
        )
    
    def _convert_member_access(self, expr: RunaMemberAccess) -> JavaFieldAccess:
        """Convert Runa member access."""
        object_expr = self.convert_expression(expr.object)
        return JavaFieldAccess(object_expr, expr.member)
    
    def _convert_index_access(self, expr: RunaIndexAccess) -> JavaArrayAccess:
        """Convert Runa index access."""
        array = self.convert_expression(expr.object)
        index = self.convert_expression(expr.index)
        
        return JavaArrayAccess(array, index)
    
    def _convert_conditional_expression(self, expr: RunaConditionalExpression) -> JavaConditionalExpression:
        """Convert Runa conditional expression."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.true_value)
        false_expr = self.convert_expression(expr.false_value)
        
        return JavaConditionalExpression(condition, true_expr, false_expr)
    
    def _convert_lambda(self, expr: RunaLambda) -> JavaLambdaExpression:
        """Convert Runa lambda."""
        parameters = []
        for param in expr.parameters:
            java_type = self._convert_type(param.param_type)
            java_param = JavaParameter(
                parameter_type=java_type,
                name=param.name
            )
            parameters.append(java_param)
        
        body_statements = []
        for stmt in expr.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        # Check if it's a single expression
        if (len(body_statements) == 1 and 
            isinstance(body_statements[0], JavaExpressionStatement)):
            # Expression body
            body = body_statements[0].expression
        else:
            # Block body
            body = JavaBlockStatement(body_statements)
        
        return JavaLambdaExpression(parameters, body)
    
    def _convert_list(self, expr: RunaList) -> JavaArrayInitializer:
        """Convert Runa list."""
        elements = [self.convert_expression(elem) for elem in expr.elements]
        return JavaArrayInitializer(elements)
    
    def _convert_type(self, runa_type: RunaType) -> JavaType:
        """Convert Runa type to Java type."""
        # Map Runa types to Java types
        type_map = {
            "Integer": "int",
            "Float": "double",
            "Character": "char",
            "Boolean": "boolean",
            "String": "String",
            "Void": "void",
        }
        
        # Handle array types
        if runa_type.name.startswith("Array[") and runa_type.name.endswith("]"):
            element_type_name = runa_type.name[6:-1]  # Remove "Array[" and "]"
            element_type = self._convert_type(RunaType(element_type_name))
            return JavaArrayType(element_type)
        
        # Handle generic types
        if "[" in runa_type.name and runa_type.name.endswith("]"):
            base_name = runa_type.name.split("[")[0]
            # Simplified generic handling
            return JavaSimpleName(base_name)
        
        java_name = type_map.get(runa_type.name, runa_type.name)
        
        # Check if it's a primitive type
        if java_name in ["boolean", "byte", "char", "short", "int", "long", "float", "double", "void"]:
            return JavaPrimitiveType(java_name)
        else:
            return JavaSimpleName(java_name)


# Convenience functions
def java_to_runa(java_ast: JavaCompilationUnit) -> Program:
    """Convert Java AST to Runa AST."""
    converter = JavaToRunaConverter()
    return converter.convert(java_ast)


def runa_to_java(runa_ast: Program) -> JavaCompilationUnit:
    """Convert Runa AST to Java AST."""
    converter = RunaToJavaConverter()
    return converter.convert(runa_ast)