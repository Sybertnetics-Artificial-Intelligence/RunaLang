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
            statements.append(ExpressionStatement(
                StringLiteral(f"package {package_name}", "comment")
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
            
            statements.append(ExpressionStatement(
                StringLiteral(import_str, "comment")
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
    
    def convert_declaration(self, decl: JavaDeclaration) -> Union[Statement, List[Statement], None]:
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
    
    def convert_statement(self, stmt: JavaStatement) -> Union[Statement, List[Statement], None]:
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
            return BreakStatement()
        elif isinstance(stmt, JavaContinueStatement):
            return ContinueStatement()
        elif isinstance(stmt, JavaThrowStatement):
            return self._convert_throw_statement(stmt)
        elif isinstance(stmt, JavaTryStatement):
            return self._convert_try_statement(stmt)
        elif isinstance(stmt, JavaSynchronizedStatement):
            return self._convert_synchronized_statement(stmt)
        elif isinstance(stmt, JavaAssertStatement):
            return self._convert_assert_statement(stmt)
        elif isinstance(stmt, JavaEmptyStatement):
            return ExpressionStatement(StringLiteral(value=""))
        elif isinstance(stmt, JavaLabeledStatement):
            return self._convert_labeled_statement(stmt)
        elif isinstance(stmt, JavaYieldStatement):
            return self._convert_yield_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: JavaExpression) -> Expression:
        """Convert Java expression to Runa expression."""
        if isinstance(expr, JavaIntegerLiteral):
            return IntegerLiteral(value=expr.value)
        elif isinstance(expr, JavaFloatingLiteral):
            return FloatLiteral(value=expr.value)
        elif isinstance(expr, JavaStringLiteral):
            return StringLiteral(value=expr.value.strip('"'))
        elif isinstance(expr, JavaCharacterLiteral):
            return StringLiteral(expr.value.strip("'"), "character")
        elif isinstance(expr, JavaBooleanLiteral):
            return BooleanLiteral(value=expr.value)
        elif isinstance(expr, JavaNullLiteral):
            return StringLiteral(value="null")
        elif isinstance(expr, JavaTextBlock):
            return StringLiteral(value=expr.value.strip('"""'))
        elif isinstance(expr, JavaSimpleName):
            return Identifier(expr.identifier)
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
            return Identifier("this")
        elif isinstance(expr, JavaSuperExpression):
            return Identifier("super")
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
        return StringLiteral(value="unknown_expression")
    
    def _convert_class_declaration(self, decl: JavaClassDeclaration) -> ProcessDefinition:
        """Convert Java class declaration to Runa process definition."""
        # Convert Java class to a Runa process that represents the class structure
        
        # Create body statements for the class process
        body_statements = []
        
        # Add field declarations as let statements
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    body_statements.extend(field_vars)
                else:
                    body_statements.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                body_statements.append(method)
        
        # Create parameters for constructor-like behavior
        parameters = []
        
        # Handle inheritance with new Runa AST support
        base_classes = []
        interfaces = []
        
        if decl.superclass:
            base_classes.append(self._convert_type(decl.superclass))
        
        for interface in decl.super_interfaces:
            interfaces.append(self._convert_type(interface))
        
        # Set class modifiers based on Java class type
        is_abstract = any(mod == JavaModifier.ABSTRACT for mod in decl.modifiers)
        is_final = any(mod == JavaModifier.FINAL for mod in decl.modifiers)
        is_static = any(mod == JavaModifier.STATIC for mod in decl.modifiers)
        access_modifier = "public"  # Default
        for mod in decl.modifiers:
            if mod in [JavaModifier.PUBLIC, JavaModifier.PRIVATE, JavaModifier.PROTECTED]:
                access_modifier = mod.value
        
        return ProcessDefinition(
            name=decl.name,
            parameters=[],  # Classes don't have parameters
            return_type=None,
            body=body_statements,
            base_classes=base_classes,
            interfaces=interfaces,
            is_abstract=is_abstract,
            is_final=is_final,
            is_static=is_static,
            is_interface=False,
            access_modifier=access_modifier,
            type_parameters=[tp.name for tp in decl.type_parameters]
        )
    
    def _convert_interface_declaration(self, decl: JavaInterfaceDeclaration) -> ProcessDefinition:
        """Convert Java interface declaration to Runa process definition."""
        # Convert interface to a Runa process representing the interface contract
        
        body_statements = []
        
        # Add interface members as process definitions
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    body_statements.extend(field_vars)
                else:
                    body_statements.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                body_statements.append(method)
        
        # Handle super interfaces
        interfaces = []
        if hasattr(decl, 'super_interfaces'):
            for super_interface in decl.super_interfaces:
                interfaces.append(self._convert_type(super_interface))
        
        # Apply access modifiers
        access_modifier = "public"  # Default for interfaces
        if hasattr(decl, 'modifiers'):
            for mod in decl.modifiers:
                if mod in [JavaModifier.PUBLIC, JavaModifier.PRIVATE, JavaModifier.PROTECTED]:
                    access_modifier = mod.value
        
        # Handle type parameters
        type_parameters = []
        if hasattr(decl, 'type_parameters'):
            type_parameters = [tp.name for tp in decl.type_parameters]
        
        return ProcessDefinition(
            name=decl.name,
            parameters=[],
            return_type=None,
            body=body_statements,
            base_classes=[],
            interfaces=interfaces,
            is_abstract=True,  # Interfaces are inherently abstract
            is_final=False,
            is_static=False,
            is_interface=True,  # Mark as interface
            access_modifier=access_modifier,
            type_parameters=type_parameters
        )
    
    def _convert_enum_declaration(self, decl: JavaEnumDeclaration) -> ProcessDefinition:
        """Convert Java enum declaration to Runa process definition."""
        body_statements = []
        
        # Convert enum constants as let statements with proper values
        for enum_const in decl.enum_constants:
            # Handle enum constant arguments if present
            init_value = StringLiteral(value=enum_const.name)
            if hasattr(enum_const, 'arguments') and enum_const.arguments:
                # Enum constant with arguments - convert to function call
                args = [self.convert_expression(arg) for arg in enum_const.arguments]
                init_value = FunctionCall(
                    function_name="create_enum_instance",
                    arguments=[
                        ("name", StringLiteral(value=enum_const.name)),
                        ("args", ListLiteral(elements=args))
                    ]
                )
            
            body_statements.append(DefineStatement(
                identifier=enum_const.name,
                type_annotation=BasicType(decl.name),
                value=init_value,
                is_constant=True
            ))
        
        # Convert body declarations (fields and methods)
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    body_statements.extend(field_vars)
                else:
                    body_statements.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                body_statements.append(method)
        
        # Handle super interfaces for enums
        interfaces = []
        if hasattr(decl, 'super_interfaces'):
            for super_interface in decl.super_interfaces:
                interfaces.append(self._convert_type(super_interface))
        
        # Apply access modifiers
        access_modifier = "public"  # Default
        if hasattr(decl, 'modifiers'):
            for mod in decl.modifiers:
                if mod in [JavaModifier.PUBLIC, JavaModifier.PRIVATE, JavaModifier.PROTECTED]:
                    access_modifier = mod.value
        
        return ProcessDefinition(
            name=decl.name,
            parameters=[],
            return_type=None,
            body=body_statements,
            base_classes=[],
            interfaces=interfaces,
            is_abstract=False,
            is_final=True,  # Enums are final
            is_static=False,
            is_interface=False,
            is_enum=True,  # Mark as enum
            access_modifier=access_modifier
        )
    
    def _convert_record_declaration(self, decl: JavaRecordDeclaration) -> ProcessDefinition:
        """Convert Java record declaration to Runa process definition."""
        body_statements = []
        
        # Convert record parameters as let statements with automatic getters
        for param in decl.parameters:
            # Add field declaration
            body_statements.append(LetStatement(
                identifier=param.name,
                type_annotation=self._convert_type(param.parameter_type),
                value=None
            ))
            
            # Add automatic getter method
            getter_body = [ReturnStatement(value=Identifier(param.name))]
            body_statements.append(ProcessDefinition(
                name=param.name,  # Getter method with same name as field
                parameters=[],
                return_type=self._convert_type(param.parameter_type),
                body=getter_body
            ))
        
        # Convert body declarations (additional methods)
        for body_decl in decl.body_declarations:
            if isinstance(body_decl, JavaFieldDeclaration):
                field_vars = self._convert_field_declaration(body_decl)
                if isinstance(field_vars, list):
                    body_statements.extend(field_vars)
                else:
                    body_statements.append(field_vars)
            elif isinstance(body_decl, JavaMethodDeclaration):
                method = self._convert_method_declaration(body_decl)
                body_statements.append(method)
        
        # Convert record parameters to process parameters
        parameters = []
        for param in decl.parameters:
            runa_param = Parameter(
                name=param.name,
                type_annotation=self._convert_type(param.parameter_type)
            )
            parameters.append(runa_param)
        
        # Handle super interfaces for records
        interfaces = []
        if hasattr(decl, 'super_interfaces'):
            for super_interface in decl.super_interfaces:
                interfaces.append(self._convert_type(super_interface))
        
        # Apply access modifiers
        access_modifier = "public"  # Default
        if hasattr(decl, 'modifiers'):
            for mod in decl.modifiers:
                if mod in [JavaModifier.PUBLIC, JavaModifier.PRIVATE, JavaModifier.PROTECTED]:
                    access_modifier = mod.value
        
        # Handle type parameters
        type_parameters = []
        if hasattr(decl, 'type_parameters'):
            type_parameters = [tp.name for tp in decl.type_parameters]
        
        return ProcessDefinition(
            name=decl.name,
            parameters=parameters,
            return_type=None,
            body=body_statements,
            base_classes=[],
            interfaces=interfaces,
            is_abstract=False,
            is_final=True,  # Records are final
            is_static=False,
            is_interface=False,
            is_struct=True,  # Mark as struct/record
            access_modifier=access_modifier,
            type_parameters=type_parameters
        )
    
    def _convert_annotation_declaration(self, decl: JavaAnnotationDeclaration) -> ProcessDefinition:
        """Convert Java annotation declaration to Runa process definition."""
        # Convert annotation to a process representing metadata
        return ProcessDefinition(
            name=f"{decl.name}_Annotation",
            parameters=[],
            return_type=BasicType("Annotation"),
            body=[]
        )
    
    def _convert_method_declaration(self, decl: JavaMethodDeclaration) -> ProcessDefinition:
        """Convert Java method declaration."""
        # Convert parameters
        parameters = []
        for param in decl.parameters:
            param_type = self._convert_type(param.parameter_type)
            runa_param = Parameter(param.name, param_type)
            parameters.append(runa_param)
        
        # Convert return type
        return_type = BasicType("Void")
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
        
        return ProcessDefinition(
            decl.name,
            parameters,
            return_type,
            body
        )
    
    def _convert_field_declaration(self, decl: JavaFieldDeclaration) -> List[LetStatement]:
        """Convert Java field declaration."""
        variables = []
        
        for fragment in decl.fragments:
            var_type = self._convert_type(decl.variable_type)
            
            # Handle array dimensions
            if fragment.extra_dimensions > 0:
                for _ in range(fragment.extra_dimensions):
                    var_type = BasicType(f"Array[{var_type.name}]")
            
            initial_value = None
            if fragment.initializer:
                initial_value = self.convert_expression(fragment.initializer)
            
            variables.append(LetStatement(
                fragment.name,
                var_type,
                initial_value
            ))
        
        return variables
    
    def _convert_variable_declaration(self, decl: JavaVariableDeclaration) -> List[LetStatement]:
        """Convert Java variable declaration."""
        variables = []
        
        for fragment in decl.fragments:
            var_type = self._convert_type(decl.variable_type)
            
            # Handle array dimensions
            if fragment.extra_dimensions > 0:
                for _ in range(fragment.extra_dimensions):
                    var_type = BasicType(f"Array[{var_type.name}]")
            
            initial_value = None
            if fragment.initializer:
                initial_value = self.convert_expression(fragment.initializer)
            
            variables.append(LetStatement(
                fragment.name,
                var_type,
                initial_value
            ))
        
        return variables
    
    def _convert_module_declaration(self, decl: JavaModuleDeclaration) -> List[Statement]:
        """Convert Java module declaration."""
        statements = []
        
        # Module name
        module_name = self._expression_to_string(decl.name)
        statements.append(ExpressionStatement(
            StringLiteral(f"module {module_name}", "comment")
        ))
        
        # Module statements
        for stmt in decl.module_statements:
            if isinstance(stmt, JavaRequiresDirective):
                req_name = self._expression_to_string(stmt.module_name)
                # Handle requires modifiers
                modifiers = []
                if hasattr(stmt, 'modifiers'):
                    modifiers = [mod.value for mod in stmt.modifiers if hasattr(mod, 'value')]
                
                req_str = f"requires {' '.join(modifiers) + ' ' if modifiers else ''}{req_name}"
                statements.append(ImportStatement(
                    module_path=req_name,
                    alias=None,
                    imported_names=None
                ))
                
            elif isinstance(stmt, JavaExportsDirective):
                pkg_name = self._expression_to_string(stmt.package_name)
                # Handle target modules
                if stmt.target_modules:
                    target_names = [self._expression_to_string(target) for target in stmt.target_modules]
                    export_str = f"exports {pkg_name} to {', '.join(target_names)}"
                else:
                    export_str = f"exports {pkg_name}"
                
                statements.append(ExportStatement(
                    exported_names=[pkg_name]
                ))
                
            elif isinstance(stmt, JavaOpensDirective):
                pkg_name = self._expression_to_string(stmt.package_name)
                # Handle target modules for opens directive
                if stmt.target_modules:
                    target_names = [self._expression_to_string(target) for target in stmt.target_modules]
                    opens_str = f"opens {pkg_name} to {', '.join(target_names)}"
                else:
                    opens_str = f"opens {pkg_name}"
                
                # Convert opens to a special export with metadata
                statements.append(ExpressionStatement(
                    StringLiteral(opens_str, "module_directive")
                ))
                
            elif isinstance(stmt, JavaUsesDirective):
                service_name = self._expression_to_string(stmt.service_name)
                statements.append(ImportStatement(
                    module_path=service_name,
                    alias=None,
                    imported_names=["service"]
                ))
                
            elif isinstance(stmt, JavaProvidesDirective):
                service_name = self._expression_to_string(stmt.service_name)
                impl_names = [self._expression_to_string(impl) for impl in stmt.implementation_names]
                
                # Convert provides to export statement with service metadata
                statements.append(ExpressionStatement(
                    StringLiteral(f"provides {service_name} with {', '.join(impl_names)}", "module_directive")
                ))
        
        return statements
    
    def _convert_expression_statement(self, stmt: JavaExpressionStatement) -> ExpressionStatement:
        """Convert Java expression statement."""
        expr = self.convert_expression(stmt.expression)
        return ExpressionStatement(expr)
    
    def _convert_block_statement(self, stmt: JavaBlockStatement) -> List[Statement]:
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
    
    def _convert_if_statement(self, stmt: JavaIfStatement) -> IfStatement:
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
        
        return IfStatement(condition, then_body, else_body)
    
    def _convert_while_statement(self, stmt: JavaWhileStatement) -> WhileLoop:
        """Convert Java while statement."""
        condition = self.convert_expression(stmt.condition)
        
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return WhileLoop("while", condition, body)
    
    def _convert_for_statement(self, stmt: JavaForStatement) -> List[Statement]:
        """Convert Java for statement."""
        statements = []
        
        # Initializers
        for init in stmt.initializers:
            init_expr = self.convert_expression(init)
            statements.append(ExpressionStatement(init_expr))
        
        # Condition
        condition = BooleanLiteral(value=True)
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
            body.append(ExpressionStatement(updater_expr))
        
        loop = WhileLoop("while", condition, body)
        statements.append(loop)
        
        return statements
    
    def _convert_enhanced_for_statement(self, stmt: JavaEnhancedForStatement) -> ForEachLoop:
        """Convert Java enhanced for statement (for-each)."""
        # Convert directly to Runa ForEachLoop which is more appropriate
        iterable = self.convert_expression(stmt.expression)
        
        # Loop variable
        loop_var = stmt.parameter.name
        
        # Convert body
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        return ForEachLoop(
            variable=loop_var,
            iterable=iterable,
            block=body
        )
    
    def _convert_do_statement(self, stmt: JavaDoStatement) -> WhileLoop:
        """Convert Java do-while statement."""
        condition = self.convert_expression(stmt.condition)
        
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return WhileLoop("do_while", condition, body)
    
    def _convert_switch_statement(self, stmt: JavaSwitchStatement) -> MatchStatement:
        """Convert Java switch statement to Runa match statement."""
        switch_expr = self.convert_expression(stmt.expression)
        
        cases = []
        default_case = None
        
        for java_case in stmt.statements:
            if hasattr(java_case, 'expressions') and java_case.expressions:
                # Regular case with one or more expressions
                for case_expr in java_case.expressions:
                    pattern = LiteralPattern(value=self.convert_expression(case_expr))
                    
                    # Convert case body
                    case_body = []
                    if hasattr(java_case, 'statements'):
                        for case_stmt in java_case.statements:
                            converted_stmt = self.convert_statement(case_stmt)
                            if converted_stmt:
                                if isinstance(converted_stmt, list):
                                    case_body.extend(converted_stmt)
                                else:
                                    case_body.append(converted_stmt)
                    
                    cases.append(MatchCase(
                        pattern=pattern,
                        guard=None,
                        block=case_body
                    ))
            else:
                # Default case
                case_body = []
                if hasattr(java_case, 'statements'):
                    for case_stmt in java_case.statements:
                        converted_stmt = self.convert_statement(case_stmt)
                        if converted_stmt:
                            if isinstance(converted_stmt, list):
                                case_body.extend(converted_stmt)
                            else:
                                case_body.append(converted_stmt)
                
                default_case = MatchCase(
                    pattern=WildcardPattern(),
                    guard=None,
                    block=case_body
                )
        
        # Add default case if it exists
        if default_case:
            cases.append(default_case)
        
        return MatchStatement(
            value=switch_expr,
            cases=cases
        )
    
    def _convert_return_statement(self, stmt: JavaReturnStatement) -> ReturnStatement:
        """Convert Java return statement."""
        value = None
        if stmt.expression:
            value = self.convert_expression(stmt.expression)
        
        return ReturnStatement(value)
    
    def _convert_throw_statement(self, stmt: JavaThrowStatement) -> ExpressionStatement:
        """Convert Java throw statement."""
        exception_expr = self.convert_expression(stmt.expression)
        
        # Convert to function call
        throw_call = FunctionCall(
            Identifier("throw"),
            [exception_expr]
        )
        
        return ExpressionStatement(throw_call)
    
    def _convert_try_statement(self, stmt: JavaTryStatement) -> TryStatement:
        """Convert Java try statement to Runa try statement."""
        # Try block
        try_body = []
        converted_try = self.convert_statement(stmt.body)
        if isinstance(converted_try, list):
            try_body = converted_try
        elif converted_try:
            try_body = [converted_try]
        
        # Convert catch clauses
        catch_clauses = []
        for java_catch in stmt.catch_clauses:
            exception_type = None
            exception_name = None
            
            if java_catch.exception:
                if java_catch.exception.parameter_type:
                    exception_type = self._convert_type(java_catch.exception.parameter_type)
                if java_catch.exception.name:
                    exception_name = java_catch.exception.name
            
            # Convert catch body
            catch_body = []
            if java_catch.body:
                converted_catch = self.convert_statement(java_catch.body)
                if isinstance(converted_catch, list):
                    catch_body = converted_catch
                elif converted_catch:
                    catch_body = [converted_catch]
            
            catch_clauses.append(CatchClause(
                exception_type=exception_type,
                exception_name=exception_name,
                block=catch_body
            ))
        
        # Finally block
        finally_body = None
        if stmt.finally_block:
            converted_finally = self.convert_statement(stmt.finally_block)
            if isinstance(converted_finally, list):
                finally_body = converted_finally
            elif converted_finally:
                finally_body = [converted_finally]
        
        return TryStatement(
            try_block=try_body,
            catch_clauses=catch_clauses,
            finally_block=finally_body
        )
    
    def _convert_synchronized_statement(self, stmt: JavaSynchronizedStatement) -> List[Statement]:
        """Convert Java synchronized statement."""
        sync_expr = self.convert_expression(stmt.expression)
        
        # Add synchronization as comment
        statements = [ExpressionStatement(
            StringLiteral(f"synchronized", "comment")
        )]
        
        # Add body
        body = self.convert_statement(stmt.body)
        if isinstance(body, list):
            statements.extend(body)
        elif body:
            statements.append(body)
        
        return statements
    
    def _convert_assert_statement(self, stmt: JavaAssertStatement) -> ExpressionStatement:
        """Convert Java assert statement."""
        condition = self.convert_expression(stmt.condition)
        
        # Convert to function call
        assert_call = FunctionCall(
            Identifier("assert"),
            [condition]
        )
        
        return ExpressionStatement(assert_call)
    
    def _convert_labeled_statement(self, stmt: JavaLabeledStatement) -> List[Statement]:
        """Convert Java labeled statement."""
        statements = []
        
        # Add label as comment
        statements.append(ExpressionStatement(
            StringLiteral(f"label {stmt.label}", "comment")
        ))
        
        # Add body
        body = self.convert_statement(stmt.body)
        if isinstance(body, list):
            statements.extend(body)
        elif body:
            statements.append(body)
        
        return statements
    
    def _convert_yield_statement(self, stmt: JavaYieldStatement) -> ReturnStatement:
        """Convert Java yield statement."""
        value = None
        if stmt.expression:
            value = self.convert_expression(stmt.expression)
        
        return ReturnStatement(value)
    
    def _convert_qualified_name(self, expr: JavaQualifiedName) -> Identifier:
        """Convert Java qualified name."""
        qualifier = self._expression_to_string(expr.qualifier)
        return Identifier(f"{qualifier}.{expr.name.identifier}")
    
    def _convert_binary_expression(self, expr: JavaBinaryExpression) -> BinaryExpression:
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
        return BinaryExpression(left, runa_op, right)
    
    def _convert_unary_expression(self, expr: JavaUnaryExpression) -> UnaryExpression:
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
        return UnaryExpression(runa_op, operand)
    
    def _convert_conditional_expression(self, expr: JavaConditionalExpression) -> FunctionCall:
        """Convert Java conditional expression to Runa function call."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.then_expression)
        false_expr = self.convert_expression(expr.else_expression)
        
        # Convert ternary to a conditional function call
        return FunctionCall(
            Identifier("conditional"),
            [condition, true_expr, false_expr]
        )
    
    def _convert_assignment_expression(self, expr: JavaAssignmentExpression) -> SetStatement:
        """Convert Java assignment expression."""
        target = self.convert_expression(expr.left)
        value = self.convert_expression(expr.right)
        
        # Handle compound assignment operators
        if expr.operator == JavaOperator.ASSIGN:
            return SetStatement(target, value)
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
                binary_op = BinaryExpression(target, operator_map[expr.operator], value)
                return SetStatement(target, binary_op)
            
            return SetStatement(target, value)
    
    def _convert_method_invocation(self, expr: JavaMethodInvocation) -> FunctionCall:
        """Convert Java method invocation."""
        # Handle method calls
        if expr.expression:
            # Instance method call
            obj = self.convert_expression(expr.expression)
            method_access = MemberAccess(obj, expr.method_name)
            function = method_access
        else:
            # Static method call or local method call
            function = Identifier(expr.method_name)
        
        arguments = [self.convert_expression(arg) for arg in expr.arguments]
        
        return FunctionCall(function, arguments)
    
    def _convert_field_access(self, expr: JavaFieldAccess) -> MemberAccess:
        """Convert Java field access."""
        obj = self.convert_expression(expr.expression)
        return MemberAccess(obj, expr.field_name)
    
    def _convert_array_access(self, expr: JavaArrayAccess) -> IndexAccess:
        """Convert Java array access."""
        array = self.convert_expression(expr.array)
        index = self.convert_expression(expr.index)
        
        return IndexAccess(array, index)
    
    def _convert_cast_expression(self, expr: JavaCastExpression) -> FunctionCall:
        """Convert Java cast expression."""
        operand = self.convert_expression(expr.expression)
        target_type = self._convert_type(expr.target_type)
        
        # Convert cast to function call
        cast_function = Identifier(f"cast_to_{target_type.name}")
        return FunctionCall(cast_function, [operand])
    
    def _convert_instanceof_expression(self, expr: JavaInstanceofExpression) -> BinaryExpression:
        """Convert Java instanceof expression."""
        left = self.convert_expression(expr.expression)
        right = StringLiteral(value=self._type_to_string(expr.target_type))
        
        return BinaryExpression(left, "instanceof", right)
    
    def _convert_class_literal(self, expr: JavaClassLiteral) -> FunctionCall:
        """Convert Java class literal."""
        type_name = self._type_to_string(expr.target_type)
        return FunctionCall(
            Identifier("get_class"),
            [StringLiteral(value=type_name)]
        )
    
    def _convert_array_creation(self, expr: JavaArrayCreation) -> FunctionCall:
        """Convert Java array creation."""
        element_type = self._type_to_string(expr.element_type)
        
        # Handle array dimensions
        if expr.dimensions:
            # Array with explicit dimensions
            dimension_args = []
            for dimension in expr.dimensions:
                if dimension:  # Non-empty dimension
                    dimension_args.append(self.convert_expression(dimension))
                else:
                    # Empty dimension - use default size
                    dimension_args.append(IntegerLiteral(value=0))
            
            if len(dimension_args) == 1:
                # Single dimension array
                return FunctionCall(
                    function_name="create_array",
                    arguments=[
                        ("type", StringLiteral(value=element_type)),
                        ("size", dimension_args[0])
                    ]
                )
            else:
                # Multi-dimensional array
                return FunctionCall(
                    function_name="create_multidimensional_array",
                    arguments=[
                        ("type", StringLiteral(value=element_type)),
                        ("dimensions", ListLiteral(elements=dimension_args))
                    ]
                )
        elif expr.initializer:
            # Array with initializer
            init_expr = self.convert_expression(expr.initializer)
            return FunctionCall(
                function_name="create_array_from_initializer",
                arguments=[
                    ("type", StringLiteral(value=element_type)),
                    ("initializer", init_expr)
                ]
            )
        
        # Empty array creation
        return FunctionCall(
            function_name="create_empty_array",
            arguments=[("type", StringLiteral(value=element_type))]
        )
    
    def _convert_array_initializer(self, expr: JavaArrayInitializer) -> ListLiteral:
        """Convert Java array initializer."""
        elements = [self.convert_expression(elem) for elem in expr.expressions]
        return ListLiteral(elements)
    
    def _convert_lambda_expression(self, expr: JavaLambdaExpression) -> ProcessDefinition:
        """Convert Java lambda expression."""
        parameters = []
        for param in expr.parameters:
            param_type = self._convert_type(param.parameter_type)
            runa_param = Parameter(name=param.name, param_type=param_type)
            parameters.append(runa_param)
        
        body = []
        if isinstance(expr.body, JavaExpression):
            # Expression body
            body_expr = self.convert_expression(expr.body)
            body = [ReturnStatement(body_expr)]
        else:
            # Block body
            converted_body = self.convert_statement(expr.body)
            if isinstance(converted_body, list):
                body = converted_body
            elif converted_body:
                body = [converted_body]
        
        # Generate a unique name for the lambda
        lambda_name = f"lambda_{self.function_counter}"
        self.function_counter += 1
        
        return ProcessDefinition(
            name=lambda_name,
            parameters=parameters, 
            return_type=BasicType("Auto"),  # Inferred return type
            body=body
        )
    
    def _convert_method_reference(self, expr: JavaMethodReference) -> Identifier:
        """Convert Java method reference."""
        if expr.expression:
            # Instance method reference
            obj_name = self._expression_to_string(expr.expression)
            return Identifier(f"{obj_name}::{expr.method_name}")
        else:
            # Static method reference
            return Identifier(f"::{expr.method_name}")
    
    def _convert_type(self, java_type: JavaType) -> BasicType:
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
            return BasicType(runa_name)
        
        elif isinstance(java_type, JavaArrayType):
            # Convert array type
            component = self._convert_type(java_type.component_type)
            return BasicType(f"Array[{component.name}]")
        
        elif isinstance(java_type, JavaParameterizedType):
            # Convert generic type
            raw_type = self._convert_type(java_type.raw_type)
            type_args = [self._convert_type(arg) for arg in java_type.type_arguments]
            
            if type_args:
                type_arg_names = ", ".join(arg.name for arg in type_args)
                return BasicType(f"{raw_type.name}[{type_arg_names}]")
            else:
                return raw_type
        
        elif isinstance(java_type, JavaWildcardType):
            # Convert wildcard type
            if java_type.bound:
                bound_type = self._convert_type(java_type.bound)
                if java_type.is_upper_bound:
                    return BasicType(f"? extends {bound_type.name}")
                else:
                    return BasicType(f"? super {bound_type.name}")
            else:
                return BasicType("?")
        
        elif isinstance(java_type, JavaVarType):
            return BasicType("Auto")
        
        elif isinstance(java_type, JavaSimpleName):
            return BasicType(java_type.identifier)
        
        elif isinstance(java_type, JavaQualifiedName):
            return BasicType(self._expression_to_string(java_type))
        
        else:
            # Default fallback
            return BasicType("Object")
    
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
    
    def convert_statement(self, stmt: Statement) -> Union[JavaDeclaration, JavaStatement, List[Union[JavaDeclaration, JavaStatement]], None]:
        """Convert Runa statement to Java declaration or statement."""
        if isinstance(stmt, LetStatement):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, ProcessDefinition):
            return self._convert_function_declaration(stmt)
        elif isinstance(stmt, ProcessDefinition) and stmt.name.endswith('_Class'):
            return self._convert_process_to_class_declaration(stmt)
        elif isinstance(stmt, SetStatement):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            return self._convert_conditional(stmt)
        elif isinstance(stmt, WhileLoop):
            return self._convert_loop(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self._convert_return(stmt)
        elif isinstance(stmt, BreakStatement):
            return JavaBreakStatement()
        elif isinstance(stmt, ContinueStatement):
            return JavaContinueStatement()
        elif isinstance(stmt, ExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: Expression) -> JavaExpression:
        """Convert Runa expression to Java expression."""
        if isinstance(expr, StringLiteral):
            return self._convert_literal(expr)
        elif isinstance(expr, Identifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, BinaryExpression):
            return self._convert_binary_operation(expr)
        elif isinstance(expr, UnaryExpression):
            return self._convert_unary_operation(expr)
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call(expr)
        elif isinstance(expr, MemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, IndexAccess):
            return self._convert_index_access(expr)
        elif isinstance(expr, ConditionalExpression):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, ProcessDefinition):
            return self._convert_lambda(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list(expr)
        
        # Fallback
        return JavaSimpleName("unknown_expression")
    
    def _convert_variable_declaration(self, stmt: LetStatement) -> JavaVariableDeclaration:
        """Convert Runa variable declaration."""
        java_type = self._convert_type(stmt.type_annotation) if stmt.type_annotation else JavaPrimitiveType("object")
        
        initializer = None
        if stmt.value:
            initializer = self.convert_expression(stmt.value)
        
        fragment = JavaVariableDeclarationFragment(stmt.name, 0, initializer)
        
        return JavaVariableDeclaration(
            variable_type=java_type,
            fragments=[fragment]
        )
    
    def _convert_function_declaration(self, stmt: ProcessDefinition) -> JavaMethodDeclaration:
        """Convert Runa function declaration."""
        return_type = self._convert_type(stmt.return_type) if stmt.return_type else JavaPrimitiveType("void")
        
        parameters = []
        for param in stmt.parameters:
            java_type = self._convert_type(param.type_annotation) if param.type_annotation else JavaPrimitiveType("object")
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
    
    def _convert_process_to_class_declaration(self, stmt: ProcessDefinition) -> JavaClassDeclaration:
        """Convert Runa process definition back to Java class declaration."""
        # Extract class name (remove _Class suffix if present)
        class_name = stmt.name
        if class_name.endswith('_Class'):
            class_name = class_name[:-6]
        
        body_declarations = []
        
        # Convert body statements back to Java declarations
        for body_stmt in stmt.body:
            if isinstance(body_stmt, LetStatement):
                # Convert let statement to field declaration
                java_type = self._convert_type(body_stmt.type_annotation) if body_stmt.type_annotation else JavaPrimitiveType("object")
                initializer = None
                if body_stmt.value:
                    initializer = self.convert_expression(body_stmt.value)
                
                fragment = JavaVariableDeclarationFragment(body_stmt.name, 0, initializer)
                field_decl = JavaFieldDeclaration(
                    variable_type=java_type,
                    fragments=[fragment]
                )
                body_declarations.append(field_decl)
            elif isinstance(body_stmt, ProcessDefinition):
                # Convert nested process to method
                method_decl = self._convert_function_declaration(body_stmt)
                body_declarations.append(method_decl)
        
        return JavaClassDeclaration(
            name=class_name,
            superclass=None,
            super_interfaces=[],
            body_declarations=body_declarations
        )
    
    def _convert_class_declaration(self, stmt: ProcessDefinition) -> JavaClassDeclaration:
        """Convert Runa class declaration."""
        body_declarations = []
        
        # Convert body statements to field and method declarations
        for body_stmt in stmt.body:
            if isinstance(body_stmt, LetStatement):
                # Convert let statement to field declaration
                java_type = self._convert_type(body_stmt.type_annotation) if body_stmt.type_annotation else JavaPrimitiveType("object")
                initializer = None
                if body_stmt.value:
                    initializer = self.convert_expression(body_stmt.value)
                
                fragment = JavaVariableDeclarationFragment(body_stmt.name, 0, initializer)
                field_decl = JavaFieldDeclaration(
                    variable_type=java_type,
                    fragments=[fragment]
                )
                body_declarations.append(field_decl)
            elif isinstance(body_stmt, ProcessDefinition):
                # Convert nested process to method
                method_decl = self._convert_function_declaration(body_stmt)
                body_declarations.append(method_decl)
        
        # Handle inheritance with Runa AST support
        superclass = None
        super_interfaces = []
        
        if stmt.base_classes:
            # Take the first base class as superclass (Java single inheritance)
            superclass = self._convert_type(stmt.base_classes[0])
        
        if stmt.interfaces:
            # Convert all interfaces
            super_interfaces = [self._convert_type(interface) for interface in stmt.interfaces]
        
        # Apply modifiers based on ProcessDefinition flags
        modifiers = []
        if stmt.access_modifier == "public":
            modifiers.append(JavaModifier.PUBLIC)
        elif stmt.access_modifier == "private":
            modifiers.append(JavaModifier.PRIVATE)
        elif stmt.access_modifier == "protected":
            modifiers.append(JavaModifier.PROTECTED)
        
        if stmt.is_abstract:
            modifiers.append(JavaModifier.ABSTRACT)
        if stmt.is_final:
            modifiers.append(JavaModifier.FINAL)
        if stmt.is_static:
            modifiers.append(JavaModifier.STATIC)
        
        # Handle type parameters
        type_parameters = []
        for type_param in stmt.type_parameters:
            type_parameters.append(JavaTypeParameter(name=type_param))
        
        return JavaClassDeclaration(
            name=stmt.name,
            superclass=superclass,
            super_interfaces=super_interfaces,
            type_parameters=type_parameters,
            body_declarations=body_declarations,
            modifiers=modifiers
        )
    
    def _convert_assignment(self, stmt: SetStatement) -> JavaExpressionStatement:
        """Convert Runa assignment."""
        target = self.convert_expression(stmt.target)
        value = self.convert_expression(stmt.value)
        
        assignment = JavaAssignmentExpression(target, JavaOperator.ASSIGN, value)
        return JavaExpressionStatement(assignment)
    
    def _convert_conditional(self, stmt: IfStatement) -> JavaIfStatement:
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
    
    def _convert_loop(self, stmt: WhileLoop) -> JavaStatement:
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
    
    def _convert_return(self, stmt: ReturnStatement) -> JavaReturnStatement:
        """Convert Runa return."""
        value = None
        if stmt.value:
            value = self.convert_expression(stmt.value)
        
        return JavaReturnStatement(value)
    
    def _convert_expression_statement(self, stmt: ExpressionStatement) -> JavaExpressionStatement:
        """Convert Runa expression statement."""
        expr = self.convert_expression(stmt.expression)
        return JavaExpressionStatement(expr)
    
    def _convert_literal(self, expr: StringLiteral) -> JavaExpression:
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
    
    def _convert_identifier(self, expr: Identifier) -> JavaSimpleName:
        """Convert Runa identifier."""
        return JavaSimpleName(expr.name)
    
    def _convert_binary_operation(self, expr: BinaryExpression) -> JavaBinaryExpression:
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
    
    def _convert_unary_operation(self, expr: UnaryExpression) -> JavaUnaryExpression:
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
    
    def _convert_function_call(self, expr: FunctionCall) -> JavaMethodInvocation:
        """Convert Runa function call."""
        if isinstance(expr.function, MemberAccess):
            # Instance method call
            expression = self.convert_expression(expr.function.object)
            method_name = expr.function.member
        elif isinstance(expr.function, Identifier):
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
    
    def _convert_member_access(self, expr: MemberAccess) -> JavaFieldAccess:
        """Convert Runa member access."""
        object_expr = self.convert_expression(expr.object)
        return JavaFieldAccess(object_expr, expr.member)
    
    def _convert_index_access(self, expr: IndexAccess) -> JavaArrayAccess:
        """Convert Runa index access."""
        array = self.convert_expression(expr.object)
        index = self.convert_expression(expr.index)
        
        return JavaArrayAccess(array, index)
    
    def _convert_conditional_expression(self, expr: ConditionalExpression) -> JavaConditionalExpression:
        """Convert Runa conditional expression."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.when_true)
        false_expr = self.convert_expression(expr.when_false)
        
        return JavaConditionalExpression(condition, true_expr, false_expr)
    
    def _convert_lambda(self, expr: ProcessDefinition) -> JavaLambdaExpression:
        """Convert Runa lambda."""
        parameters = []
        for param in expr.parameters:
            java_type = self._convert_type(param.type_annotation) if param.type_annotation else JavaPrimitiveType("object")
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
    
    def _convert_list(self, expr: ListLiteral) -> JavaArrayInitializer:
        """Convert Runa list."""
        elements = [self.convert_expression(elem) for elem in expr.elements]
        return JavaArrayInitializer(elements)
    
    def _convert_type(self, runa_type: BasicType) -> JavaType:
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
            element_type = self._convert_type(BasicType(element_type_name))
            return JavaArrayType(element_type)
        
        # Handle generic types
        if "[" in runa_type.name and runa_type.name.endswith("]"):
            base_name = runa_type.name.split("[")[0]
            type_args_str = runa_type.name[runa_type.name.index("[")+1:-1]
            
            # Parse type arguments
            type_args = []
            if type_args_str.strip():
                # Split by comma and handle nested generics
                arg_parts = self._split_type_arguments(type_args_str)
                for arg_part in arg_parts:
                    arg_type = self._convert_type(BasicType(arg_part.strip()))
                    type_args.append(arg_type)
            
            # Create parameterized type
            raw_type = JavaSimpleName(base_name)
            return JavaParameterizedType(
                raw_type=raw_type,
                type_arguments=type_args
            )
        
        java_name = type_map.get(runa_type.name, runa_type.name)
        
        # Check if it's a primitive type
        if java_name in ["boolean", "byte", "char", "short", "int", "long", "float", "double", "void"]:
            return JavaPrimitiveType(java_name)
        else:
            return JavaSimpleName(java_name)
    
    def _split_type_arguments(self, type_args_str: str) -> List[str]:
        """Split type arguments string, handling nested generics."""
        if not type_args_str.strip():
            return []
        
        args = []
        current_arg = ""
        bracket_depth = 0
        
        for char in type_args_str:
            if char == '[':
                bracket_depth += 1
                current_arg += char
            elif char == ']':
                bracket_depth -= 1
                current_arg += char
            elif char == ',' and bracket_depth == 0:
                # Split point
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char
        
        # Add the last argument
        if current_arg.strip():
            args.append(current_arg.strip())
        
        return args


# Convenience functions
def java_to_runa(java_ast: JavaCompilationUnit) -> Program:
    """Convert Java AST to Runa AST."""
    converter = JavaToRunaConverter()
    return converter.convert(java_ast)


def runa_to_java(runa_ast: Program) -> JavaCompilationUnit:
    """Convert Runa AST to Java AST."""
    converter = RunaToJavaConverter()
    return converter.convert(runa_ast)