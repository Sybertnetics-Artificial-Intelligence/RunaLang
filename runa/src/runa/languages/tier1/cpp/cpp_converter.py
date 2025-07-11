#!/usr/bin/env python3
"""
C++ ↔ Runa Bidirectional Converter

Converts between C++ AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.
Handles modern C++ features including templates, lambdas, and RAII.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

from .cpp_ast import *
from ....core.runa_ast import *


class CppToRunaConverter:
    """Converts C++ AST to Runa AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0
        self.scope_stack = []
    
    def convert(self, cpp_ast: CppTranslationUnit) -> Program:
        """Convert C++ translation unit to Runa program."""
        statements = []
        
        for decl in cpp_ast.declarations:
            converted = self.convert_declaration(decl)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return Program(statements)
    
    def convert_declaration(self, decl: CppDeclaration) -> Union[Statement, List[Statement], None]:
        """Convert C++ declaration to Runa statement(s)."""
        if isinstance(decl, CppVariableDecl):
            return self._convert_variable_decl(decl)
        elif isinstance(decl, CppFunctionDecl):
            return self._convert_function_decl(decl)
        elif isinstance(decl, CppClassDecl):
            return self._convert_class_decl(decl)
        elif isinstance(decl, CppNamespaceDecl):
            return self._convert_namespace_decl(decl)
        elif isinstance(decl, CppTemplateDecl):
            return self._convert_template_decl(decl)
        
        return None
    
    def convert_statement(self, stmt: CppStatement) -> Union[Statement, List[Statement], None]:
        """Convert C++ statement to Runa statement(s)."""
        if isinstance(stmt, CppExpressionStmt):
            return self._convert_expression_stmt(stmt)
        elif isinstance(stmt, CppCompoundStmt):
            return self._convert_compound_stmt(stmt)
        elif isinstance(stmt, CppIfStmt):
            return self._convert_if_stmt(stmt)
        elif isinstance(stmt, CppWhileStmt):
            return self._convert_while_stmt(stmt)
        elif isinstance(stmt, CppForStmt):
            return self._convert_for_stmt(stmt)
        elif isinstance(stmt, CppRangeForStmt):
            return self._convert_range_for_stmt(stmt)
        elif isinstance(stmt, CppReturnStmt):
            return self._convert_return_stmt(stmt)
        elif isinstance(stmt, CppBreakStmt):
            return BreakStatement()
        elif isinstance(stmt, CppContinueStmt):
            return ContinueStatement()
        
        return None
    
    def convert_expression(self, expr: CppExpression) -> Expression:
        """Convert C++ expression to Runa expression."""
        if isinstance(expr, CppIntegerLiteral):
            return self._convert_integer_literal(expr)
        elif isinstance(expr, CppFloatingLiteral):
            return self._convert_floating_literal(expr)
        elif isinstance(expr, CppStringLiteral):
            return self._convert_string_literal(expr)
        elif isinstance(expr, CppCharacterLiteral):
            return self._convert_character_literal(expr)
        elif isinstance(expr, CppBooleanLiteral):
            return self._convert_boolean_literal(expr)
        elif isinstance(expr, CppNullptrLiteral):
            return self._convert_nullptr_literal(expr)
        elif isinstance(expr, CppIdentifier):
            return self._convert_identifier(expr)
        elif isinstance(expr, CppQualifiedName):
            return self._convert_qualified_name(expr)
        elif isinstance(expr, CppBinaryOp):
            return self._convert_binary_op(expr)
        elif isinstance(expr, CppUnaryOp):
            return self._convert_unary_op(expr)
        elif isinstance(expr, CppConditionalOp):
            return self._convert_conditional_op(expr)
        elif isinstance(expr, CppAssignment):
            return self._convert_assignment(expr)
        elif isinstance(expr, CppCall):
            return self._convert_call(expr)
        elif isinstance(expr, CppMemberAccess):
            return self._convert_member_access(expr)
        elif isinstance(expr, CppArraySubscript):
            return self._convert_array_subscript(expr)
        elif isinstance(expr, CppCast):
            return self._convert_cast(expr)
        elif isinstance(expr, CppNewExpr):
            return self._convert_new_expr(expr)
        elif isinstance(expr, CppDeleteExpr):
            return self._convert_delete_expr(expr)
        elif isinstance(expr, CppLambda):
            return self._convert_lambda(expr)
        elif isinstance(expr, CppInitializerList):
            return self._convert_initializer_list(expr)
        
        # Fallback for unknown expressions
        return StringLiteral("unknown_expression")
    
    def _convert_variable_decl(self, decl: CppVariableDecl) -> LetStatement:
        """Convert C++ variable declaration."""
        runa_type = self._convert_type(decl.var_type)
        initial_value = None
        
        if decl.initializer:
            initial_value = self.convert_expression(decl.initializer)
        
        return LetStatement(
            identifier=decl.name,
            value=initial_value,
            type_annotation=runa_type
        )
    
    def _convert_function_decl(self, decl: CppFunctionDecl) -> ProcessDefinition:
        """Convert C++ function declaration."""
        parameters = []
        
        for param in decl.parameters.parameters:
            param_type = self._convert_type(param.param_type)
            param_name = param.name or f"param_{len(parameters)}"
            
            runa_param = Parameter(
                name=param_name,
                type_annotation=param_type
            )
            parameters.append(runa_param)
        
        return_type = self._convert_type(decl.return_type)
        
        body_statements = []
        if decl.body:
            converted_body = self.convert_statement(decl.body)
            if isinstance(converted_body, list):
                body_statements = converted_body
            elif converted_body:
                body_statements = [converted_body]
        
        return ProcessDefinition(
            name=decl.name,
            parameters=parameters,
            return_type=return_type,
            body=body_statements
        )
    
    def _convert_class_decl(self, decl: CppClassDecl) -> TypeDefinition:
        """Convert C++ class declaration to Runa type definition."""
        try:
            # Convert class name
            class_name = decl.name if decl.name else "AnonymousClass"
            
            # Handle template classes
            if hasattr(decl, 'template_params') and decl.template_params:
                template_params = self._convert_template_parameters(decl.template_params)
                class_name = f"{class_name}<{', '.join(template_params)}>"
            
            # Convert base classes (inheritance)
            base_types = []
            if decl.base_clause:
                for base in decl.base_clause.bases:
                    base_type = self._convert_type(base.type)
                    if base_type:
                        # Handle access specifiers
                        access = base.access_specifier if hasattr(base, 'access_specifier') else "public"
                        if access == "public":
                            base_types.append(base_type)
                        # For private/protected inheritance, we'll add metadata
                        elif access in ["private", "protected"]:
                            base_types.append(f"{access}_{base_type}")
            
            # Convert class members
            members = []
            if decl.members:
                for member in decl.members:
                    converted_member = self._convert_class_member(member)
                    if converted_member:
                        members.append(converted_member)
            
            # Create type definition with inheritance
            if base_types:
                # Create composite type with inheritance
                base_type = base_types[0] if len(base_types) == 1 else f"Composite({', '.join(base_types)})"
                # Create ProcessDefinition with class-like features for C++ classes
                process_def = ProcessDefinition(
                    name=class_name,
                    parameters=[],
                    return_type=BasicType("Object"),
                    body=members,
                    base_classes=[BasicType(base_type)] if base_types else []
                )
                type_def = process_def
            else:
                # Simple type definition
                # Simple class definition as ProcessDefinition
                process_def = ProcessDefinition(
                    name=class_name,
                    parameters=[],
                    return_type=BasicType("Object"),
                    body=members
                )
                type_def = process_def
            
            # Add class metadata
            if hasattr(decl, 'storage_class') and decl.storage_class:
                type_def.metadata = type_def.metadata or {}
                type_def.metadata["storage_class"] = decl.storage_class
            
            # Handle virtual inheritance
            if decl.base_clause and any(getattr(base, 'is_virtual', False) for base in decl.base_clause.bases):
                type_def.metadata = type_def.metadata or {}
                type_def.metadata["virtual_inheritance"] = True
            
            return type_def
            
        except Exception as e:
            self._log_error(f"Error converting class declaration: {e}")
            # Fallback to basic type
            return ProcessDefinition(
                name=decl.name or "UnknownClass",
                parameters=[],
                return_type=BasicType("Object"),
                body=[]
            )
    
    def _convert_class_member(self, member) -> Optional[Statement]:
        """Convert individual class member."""
        try:
            if hasattr(member, 'kind'):
                if member.kind == "field":
                    return self._convert_field_declaration(member)
                elif member.kind == "method":
                    return self._convert_method_declaration(member)
                elif member.kind == "constructor":
                    return self._convert_constructor_declaration(member)
                elif member.kind == "destructor":
                    return self._convert_destructor_declaration(member)
                elif member.kind == "operator":
                    return self._convert_operator_declaration(member)
                elif member.kind == "typedef":
                    return self._convert_typedef_declaration(member)
                elif member.kind == "enum":
                    return self._convert_enum_declaration(member)
                elif member.kind == "class":
                    return self._convert_nested_class_declaration(member)
                elif member.kind == "friend":
                    return self._convert_friend_declaration(member)
                elif member.kind == "using":
                    return self._convert_using_declaration(member)
            
            # Fallback for unknown member types
            return self.convert_declaration(member)
            
        except Exception as e:
            self._log_error(f"Error converting class member: {e}")
            return None
    
    def _convert_field_declaration(self, field) -> Statement:
        """Convert class field declaration."""
        field_name = field.name if hasattr(field, 'name') else "unknown_field"
        field_type = self._convert_type(field.type) if hasattr(field, 'type') else "any"
        
        # Handle access specifier
        access = getattr(field, 'access_specifier', 'private')
        
        # Handle static fields
        is_static = getattr(field, 'storage_class', '') == 'static'
        
        # Handle const fields
        is_const = getattr(field, 'is_const', False)
        
        # Handle reference fields
        is_reference = getattr(field, 'is_reference', False)
        
        # Create field declaration
        # Convert field to LetStatement with metadata
        field_stmt = LetStatement(
            identifier=field_name,
            type_annotation=BasicType(field_type) if isinstance(field_type, str) else field_type,
            value=None
        )
        
        # Add metadata for access and modifiers
        field_stmt.metadata = field_stmt.metadata or {}
        field_stmt.metadata["access_specifier"] = access
        field_stmt.metadata["is_static"] = is_static
        field_stmt.metadata["is_const"] = is_const
        field_stmt.metadata["is_reference"] = is_reference
        
        return field_stmt
    
    def _convert_method_declaration(self, method) -> Statement:
        """Convert class method declaration."""
        method_name = method.name if hasattr(method, 'name') else "unknown_method"
        return_type = self._convert_type(method.return_type) if hasattr(method, 'return_type') else "void"
        
        # Convert parameters
        parameters = []
        if hasattr(method, 'parameters') and method.parameters:
            for param in method.parameters:
                param_name = param.name if hasattr(param, 'name') else "param"
                param_type = self._convert_type(param.type) if hasattr(param, 'type') else "any"
                default_value = None
                if hasattr(param, 'default_value') and param.default_value:
                    default_value = self.convert_expression(param.default_value)
                
                parameters.append(Parameter(
                    name=param_name,
                    type=param_type,
                    default_value=default_value
                ))
        
        # Handle access specifier
        access = getattr(method, 'access_specifier', 'private')
        
        # Handle method modifiers
        modifiers = []
        if getattr(method, 'is_virtual', False):
            modifiers.append("virtual")
        if getattr(method, 'is_pure_virtual', False):
            modifiers.append("pure_virtual")
        if getattr(method, 'is_const', False):
            modifiers.append("const")
        if getattr(method, 'storage_class', '') == 'static':
            modifiers.append("static")
        if getattr(method, 'is_inline', False):
            modifiers.append("inline")
        
        # Handle method body
        body = None
        if hasattr(method, 'body') and method.body:
            body = self.convert_statement(method.body)
        
        method_def = ProcessDefinition(
            name=method_name,
            parameters=parameters,
            return_type=BasicType(return_type) if isinstance(return_type, str) else return_type,
            body=body if body else []
        )
        
        # Add metadata for access and modifiers
        method_def.metadata = method_def.metadata or {}
        method_def.metadata["access_specifier"] = access
        method_def.metadata["modifiers"] = modifiers
        
        return method_def
    
    def _convert_constructor_declaration(self, ctor) -> Statement:
        """Convert constructor declaration."""
        class_name = ctor.name if hasattr(ctor, 'name') else "UnknownClass"
        
        # Convert parameters
        parameters = []
        if hasattr(ctor, 'parameters') and ctor.parameters:
            for param in ctor.parameters:
                param_name = param.name if hasattr(param, 'name') else "param"
                param_type = self._convert_type(param.type) if hasattr(param, 'type') else "any"
                default_value = None
                if hasattr(param, 'default_value') and param.default_value:
                    default_value = self.convert_expression(param.default_value)
                
                parameters.append(Parameter(
                    name=param_name,
                    type=param_type,
                    default_value=default_value
                ))
        
        # Handle access specifier
        access = getattr(ctor, 'access_specifier', 'public')
        
        # Handle constructor modifiers
        modifiers = []
        if getattr(ctor, 'is_explicit', False):
            modifiers.append("explicit")
        if getattr(ctor, 'storage_class', '') == 'static':
            modifiers.append("static")
        
        # Handle constructor body
        body = None
        if hasattr(ctor, 'body') and ctor.body:
            body = self.convert_statement(ctor.body)
        
        # Handle initializer list
        initializers = []
        if hasattr(ctor, 'initializer_list') and ctor.initializer_list:
            for init in ctor.initializer_list:
                member_name = init.member if hasattr(init, 'member') else "unknown"
                init_value = self.convert_expression(init.value) if hasattr(init, 'value') else None
                if init_value:
                    initializers.append(f"{member_name} = {init_value}")
        
        # Constructor as special ProcessDefinition
        ctor_def = ProcessDefinition(
            name=f"__init__{class_name}",
            parameters=parameters,
            return_type=BasicType(class_name),
            body=body if body else []
        )
        
        # Add metadata for constructor specifics
        ctor_def.metadata = ctor_def.metadata or {}
        ctor_def.metadata["is_constructor"] = True
        ctor_def.metadata["access_specifier"] = access
        ctor_def.metadata["modifiers"] = modifiers
        ctor_def.metadata["initializers"] = initializers
        
        return ctor_def
    
    def _convert_destructor_declaration(self, dtor) -> Statement:
        """Convert destructor declaration."""
        class_name = dtor.name if hasattr(dtor, 'name') else "UnknownClass"
        
        # Handle access specifier
        access = getattr(dtor, 'access_specifier', 'public')
        
        # Handle destructor modifiers
        modifiers = []
        if getattr(dtor, 'is_virtual', False):
            modifiers.append("virtual")
        if getattr(dtor, 'is_pure_virtual', False):
            modifiers.append("pure_virtual")
        
        # Handle destructor body
        body = None
        if hasattr(dtor, 'body') and dtor.body:
            body = self.convert_statement(dtor.body)
        
        # Destructor as special ProcessDefinition
        dtor_def = ProcessDefinition(
            name=f"__del__{class_name}",
            parameters=[],
            return_type=BasicType("Void"),
            body=body if body else []
        )
        
        # Add metadata for destructor specifics
        dtor_def.metadata = dtor_def.metadata or {}
        dtor_def.metadata["is_destructor"] = True
        dtor_def.metadata["access_specifier"] = access
        dtor_def.metadata["modifiers"] = modifiers
        
        return dtor_def
    
    def _convert_operator_declaration(self, op) -> Statement:
        """Convert operator overload declaration."""
        operator_name = op.operator if hasattr(op, 'operator') else "unknown"
        
        # Convert parameters
        parameters = []
        if hasattr(op, 'parameters') and op.parameters:
            for param in op.parameters:
                param_name = param.name if hasattr(param, 'name') else "param"
                param_type = self._convert_type(param.type) if hasattr(param, 'type') else "any"
                parameters.append(Parameter(
                    name=param_name,
                    type=param_type
                ))
        
        return_type = self._convert_type(op.return_type) if hasattr(op, 'return_type') else "any"
        
        # Handle access specifier
        access = getattr(op, 'access_specifier', 'public')
        
        # Handle operator modifiers
        modifiers = []
        if getattr(op, 'is_const', False):
            modifiers.append("const")
        
        # Handle operator body
        body = None
        if hasattr(op, 'body') and op.body:
            body = self.convert_statement(op.body)
        
        # Operator as special ProcessDefinition
        op_def = ProcessDefinition(
            name=f"__operator_{operator_name}__",
            parameters=parameters,
            return_type=BasicType(return_type) if isinstance(return_type, str) else return_type,
            body=body if body else []
        )
        
        # Add metadata for operator specifics
        op_def.metadata = op_def.metadata or {}
        op_def.metadata["is_operator"] = True
        op_def.metadata["operator_name"] = operator_name
        op_def.metadata["access_specifier"] = access
        op_def.metadata["modifiers"] = modifiers
        
        return op_def
    
    def _convert_template_parameters(self, template_params) -> List[str]:
        """Convert template parameters to string representations."""
        params = []
        if hasattr(template_params, 'parameters'):
            for param in template_params.parameters:
                if hasattr(param, 'kind'):
                    if param.kind == "type":
                        param_name = param.name if hasattr(param, 'name') else "T"
                        default_type = ""
                        if hasattr(param, 'default_value') and param.default_value:
                            default_type = f" = {self._convert_type(param.default_value)}"
                        params.append(f"typename {param_name}{default_type}")
                    elif param.kind == "non_type":
                        param_name = param.name if hasattr(param, 'name') else "N"
                        param_type = self._convert_type(param.type) if hasattr(param, 'type') else "int"
                        default_value = ""
                        if hasattr(param, 'default_value') and param.default_value:
                            default_value = f" = {self.convert_expression(param.default_value)}"
                        params.append(f"{param_type} {param_name}{default_value}")
                    elif param.kind == "template":
                        param_name = param.name if hasattr(param, 'name') else "T"
                        params.append(f"template<typename> class {param_name}")
        return params
    
    def _convert_namespace_decl(self, decl: CppNamespaceDecl) -> List[Statement]:
        """Convert C++ namespace declaration."""
        statements = []
        
        # Add namespace comment
        if decl.name:
            comment = ExpressionStatement(
                StringLiteral(f"namespace {decl.name}")
            )
            statements.append(comment)
        
        # Convert namespace contents
        for member_decl in decl.declarations:
            converted = self.convert_declaration(member_decl)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return statements
    
    def _convert_template_decl(self, decl: CppTemplateDecl) -> Statement:
        """Convert C++ template declaration to Runa equivalent."""
        try:
            # Convert template parameters
            template_params = []
            if decl.template_params and hasattr(decl.template_params, 'parameters'):
                for param in decl.template_params.parameters:
                    converted_param = self._convert_template_parameter(param)
                    if converted_param:
                        template_params.append(converted_param)
            
            # Convert the templated declaration
            converted_decl = self.convert_declaration(decl.declaration)
            
            # Handle different types of templated declarations
            if isinstance(converted_decl, ProcessDefinition):
                # Template function
                return self._create_template_function(converted_decl, template_params)
            elif isinstance(converted_decl, TypeDefinition):
                # Template class
                return self._create_template_class(converted_decl, template_params)
            elif isinstance(converted_decl, (LetStatement, DefineStatement)):
                # Template variable (C++17)
                return self._create_template_variable(converted_decl, template_params)
            else:
                # Generic template declaration
                return self._create_generic_template(converted_decl, template_params)
                
        except Exception as e:
            self._log_error(f"Error converting template declaration: {e}")
            # Fallback to basic conversion
            converted_decl = self.convert_declaration(decl.declaration)
            if isinstance(converted_decl, ProcessDefinition):
                converted_decl.name = f"template_{converted_decl.name}"
            return converted_decl
    
    def _convert_template_parameter(self, param) -> Optional[str]:
        """Convert individual template parameter."""
        try:
            if hasattr(param, 'kind'):
                if param.kind == "type":
                    # Type parameter: typename T
                    param_name = param.name if hasattr(param, 'name') else "T"
                    default_type = ""
                    if hasattr(param, 'default_value') and param.default_value:
                        default_type = f" = {self._convert_type(param.default_value)}"
                    
                    # Handle constraints (C++20 concepts)
                    constraints = ""
                    if hasattr(param, 'constraints') and param.constraints:
                        constraint_list = []
                        for constraint in param.constraints:
                            if hasattr(constraint, 'name'):
                                constraint_list.append(constraint.name)
                        if constraint_list:
                            constraints = f" requires {', '.join(constraint_list)}"
                    
                    return f"typename {param_name}{default_type}{constraints}"
                
                elif param.kind == "non_type":
                    # Non-type parameter: int N
                    param_name = param.name if hasattr(param, 'name') else "N"
                    param_type = self._convert_type(param.type) if hasattr(param, 'type') else "int"
                    default_value = ""
                    if hasattr(param, 'default_value') and param.default_value:
                        default_value = f" = {self._convert_expression(param.default_value)}"
                    
                    return f"{param_type} {param_name}{default_value}"
                
                elif param.kind == "template":
                    # Template template parameter: template<typename> class Container
                    param_name = param.name if hasattr(param, 'name') else "T"
                    template_params = ""
                    if hasattr(param, 'template_params') and param.template_params:
                        param_list = []
                        for tp in param.template_params.parameters:
                            if hasattr(tp, 'kind') and tp.kind == "type":
                                param_list.append("typename")
                        if param_list:
                            template_params = f"<{', '.join(param_list)}>"
                    
                    return f"template{template_params} class {param_name}"
                
                elif param.kind == "concept":
                    # C++20 concept parameter
                    param_name = param.name if hasattr(param, 'name') else "C"
                    concept_name = param.concept_name if hasattr(param, 'concept_name') else "Concept"
                    return f"{concept_name} {param_name}"
            
            return None
            
        except Exception as e:
            self._log_error(f"Error converting template parameter: {e}")
            return None
    
    def _create_template_function(self, func: ProcessDefinition, template_params: List[str]) -> ProcessDefinition:
        """Create template function with proper parameter handling."""
        # Add template parameters as metadata
        func.metadata = func.metadata or {}
        func.metadata["template_parameters"] = template_params
        func.metadata["is_template"] = True
        
        # Modify function name to indicate it's a template
        if template_params:
            param_names = []
            for param in template_params:
                # Extract parameter name from template parameter string
                try:
                    if "typename" in param:
                        parts = param.split("typename")
                        if len(parts) > 1:
                            name = parts[1].split()[0].split("=")[0].strip()
                            param_names.append(name)
                    elif "template" in param and "class" in param:
                        parts = param.split("class")
                        if len(parts) > 1:
                            name = parts[1].strip().split()[0]
                            param_names.append(name)
                    else:
                        parts = param.split()
                        if len(parts) > 1:
                            name = parts[1].split("=")[0].strip()
                            param_names.append(name)
                except (IndexError, AttributeError):
                    # Fallback if parsing fails
                    param_names.append("UnknownParam")
            
            func.name = f"{func.name}<{', '.join(param_names)}>"
        
        return func
    
    def _create_template_class(self, class_def: TypeDefinition, template_params: List[str]) -> TypeDefinition:
        """Create template class with proper parameter handling."""
        # Add template parameters as metadata
        class_def.metadata = class_def.metadata or {}
        class_def.metadata["template_parameters"] = template_params
        class_def.metadata["is_template"] = True
        
        # Modify class name to indicate it's a template
        if template_params:
            param_names = []
            for param in template_params:
                # Extract parameter name from template parameter string
                try:
                    if "typename" in param:
                        parts = param.split("typename")
                        if len(parts) > 1:
                            name = parts[1].split()[0].split("=")[0].strip()
                            param_names.append(name)
                    elif "template" in param and "class" in param:
                        parts = param.split("class")
                        if len(parts) > 1:
                            name = parts[1].strip().split()[0]
                            param_names.append(name)
                    else:
                        parts = param.split()
                        if len(parts) > 1:
                            name = parts[1].split("=")[0].strip()
                            param_names.append(name)
                except (IndexError, AttributeError):
                    # Fallback if parsing fails
                    param_names.append("UnknownParam")
            
            class_def.name = f"{class_def.name}<{', '.join(param_names)}>"
        
        return class_def
    
    def _create_template_variable(self, var: Union[LetStatement, DefineStatement], template_params: List[str]) -> Union[LetStatement, DefineStatement]:
        """Create template variable (C++17 feature)."""
        # Add template parameters as metadata
        var.metadata = var.metadata or {}
        var.metadata["template_parameters"] = template_params
        var.metadata["is_template"] = True
        
        # Modify variable name to indicate it's a template
        if template_params:
            param_names = []
            for param in template_params:
                if "typename" in param:
                    name = param.split("typename")[1].split()[0].split("=")[0].strip()
                    param_names.append(name)
                else:
                    name = param.split()[1].split("=")[0].strip()
                    param_names.append(name)
            
            var.name = f"{var.name}<{', '.join(param_names)}>"
        
        return var
    
    def _create_generic_template(self, decl: Statement, template_params: List[str]) -> Statement:
        """Create generic template declaration."""
        # Add template parameters as metadata
        if hasattr(decl, 'metadata'):
            decl.metadata = decl.metadata or {}
            decl.metadata["template_parameters"] = template_params
            decl.metadata["is_template"] = True
        
        return decl
    
    def _convert_template_specialization(self, spec) -> Statement:
        """Convert template specialization."""
        try:
            # Convert the specialized declaration
            converted_decl = self.convert_declaration(spec.declaration)
            
            # Add specialization metadata
            if hasattr(converted_decl, 'metadata'):
                converted_decl.metadata = converted_decl.metadata or {}
                converted_decl.metadata["is_specialization"] = True
                
                # Add template arguments
                if hasattr(spec, 'template_args') and spec.template_args:
                    args = []
                    for arg in spec.template_args:
                        if hasattr(arg, 'kind'):
                            if arg.kind == "type":
                                args.append(self._convert_type(arg.type))
                            elif arg.kind == "non_type":
                                args.append(self.convert_expression(arg.value))
                            elif arg.kind == "template":
                                args.append("template")
                    converted_decl.metadata["template_arguments"] = args
            
            return converted_decl
            
        except Exception as e:
            self._log_error(f"Error converting template specialization: {e}")
            return self.convert_declaration(spec.declaration)
    
    def _convert_concept_declaration(self, concept) -> Statement:
        """Convert C++20 concept declaration."""
        try:
            concept_name = concept.name if hasattr(concept, 'name') else "UnknownConcept"
            
            # Convert concept parameters
            parameters = []
            if hasattr(concept, 'parameters') and concept.parameters:
                for param in concept.parameters:
                    param_name = param.name if hasattr(param, 'name') else "T"
                    param_type = self._convert_type(param.type) if hasattr(param, 'type') else "any"
                    parameters.append(Parameter(name=param_name, type=param_type))
            
            # Convert concept body (constraint expression)
            body = None
            if hasattr(concept, 'body') and concept.body:
                body = self.convert_expression(concept.body)
            
            # Concept as special ProcessDefinition
            concept_def = ProcessDefinition(
                name=concept_name,
                parameters=parameters,
                return_type=BasicType("Boolean"),
                body=[ExpressionStatement(body)] if body else []
            )
            
            # Add metadata for concept specifics
            concept_def.metadata = concept_def.metadata or {}
            concept_def.metadata["is_concept"] = True
            
            return concept_def
            
        except Exception as e:
            self._log_error(f"Error converting concept declaration: {e}")
            return None
    
    def _convert_expression_stmt(self, stmt: CppExpressionStmt) -> ExpressionStatement:
        """Convert C++ expression statement."""
        if stmt.expression:
            expr = self.convert_expression(stmt.expression)
            return ExpressionStatement(expression=expr)
        else:
           return ExpressionStatement(expression=StringLiteral(value=""))
    
    def _convert_compound_stmt(self, stmt: CppCompoundStmt) -> List[Statement]:
        """Convert C++ compound statement."""
        statements = []
        
        for cpp_stmt in stmt.statements:
            converted = self.convert_statement(cpp_stmt)
            if converted:
                if isinstance(converted, list):
                    statements.extend(converted)
                else:
                    statements.append(converted)
        
        return statements
    
    def _convert_if_stmt(self, stmt: CppIfStmt) -> IfStatement:
        """Convert C++ if statement."""
        condition = self.convert_expression(stmt.condition)
        
        then_body = []
        converted_then = self.convert_statement(stmt.then_stmt)
        if isinstance(converted_then, list):
            then_body = converted_then
        elif converted_then:
            then_body = [converted_then]
        
        else_body = []
        if stmt.else_stmt:
            converted_else = self.convert_statement(stmt.else_stmt)
            if isinstance(converted_else, list):
                else_body = converted_else
            elif converted_else:
                else_body = [converted_else]
        
        return IfStatement(
            condition=condition,
            then_block=then_body,
            else_block=else_body if else_body else None
        )
    
    def _convert_while_stmt(self, stmt: CppWhileStmt) -> WhileLoop:
        """Convert C++ while statement."""
        condition = self.convert_expression(stmt.condition)
        
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return WhileLoop(
            condition=condition,
            block=body
        )
    
    def _convert_for_stmt(self, stmt: CppForStmt) -> List[Statement]:
        """Convert C++ for statement."""
        # Convert for loop to while loop equivalent
        statements = []
        
        # Initialization
        if stmt.init:
            init_stmt = self.convert_statement(stmt.init)
            if init_stmt:
                if isinstance(init_stmt, list):
                    statements.extend(init_stmt)
                else:
                    statements.append(init_stmt)
        
        # Condition
        condition = None
        if stmt.condition:
            condition = self.convert_expression(stmt.condition)
        else:
            condition = BooleanLiteral(value=True)
        
        # Body with increment
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        # Add increment to end of body
        if stmt.increment:
            increment_expr = self.convert_expression(stmt.increment)
            body.append(ExpressionStatement(expression=increment_expr))
        
        loop = WhileLoop(condition=condition, block=body)
        statements.append(loop)
        
        return statements
    
    def _convert_range_for_stmt(self, stmt: CppRangeForStmt) -> ForEachLoop:
        """Convert C++ range-based for statement."""
        # Convert range-for to iterator-based loop
        iterator_var = f"_iterator_{self.variable_counter}"
        self.variable_counter += 1
        
        range_expr = self.convert_expression(stmt.range)
        
        # Convert to a simple for-each loop
        body = []
        converted_body = self.convert_statement(stmt.body)
        if isinstance(converted_body, list):
            body.extend(converted_body)
        elif converted_body:
            body.append(converted_body)
        
        # Extract variable name from declaration or use as string
        if hasattr(stmt, 'variable'):
            if hasattr(stmt.variable, 'name'):
                var_name = stmt.variable.name
            else:
                var_name = str(stmt.variable)
        else:
            var_name = f"iter_var_{self.variable_counter}"
            self.variable_counter += 1
        
        return ForEachLoop(
            variable=var_name,
            iterable=range_expr,
            block=body
        )
    
    def _convert_return_stmt(self, stmt: CppReturnStmt) -> ReturnStatement:
        """Convert C++ return statement."""
        value = None
        if stmt.value:
            value = self.convert_expression(stmt.value)
        
        return ReturnStatement(value=value)
    
    def _convert_integer_literal(self, expr: CppIntegerLiteral) -> IntegerLiteral:
        """Convert C++ integer literal."""
        return IntegerLiteral(value=expr.value)
    
    def _convert_floating_literal(self, expr: CppFloatingLiteral) -> StringLiteral:
        """Convert C++ floating point literal."""
        return FloatLiteral(value=expr.value)
    
    def _convert_string_literal(self, expr: CppStringLiteral) -> StringLiteral:
        """Convert C++ string literal."""
        # Remove quotes and handle escape sequences
        value = expr.value
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return StringLiteral(value=value)
    
    def _convert_character_literal(self, expr: CppCharacterLiteral) -> StringLiteral:
        """Convert C++ character literal."""
        value = expr.value
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        return StringLiteral(value, "character")
    
    def _convert_boolean_literal(self, expr: CppBooleanLiteral) -> StringLiteral:
        """Convert C++ boolean literal."""
        return BooleanLiteral(value=expr.value)
    
    def _convert_nullptr_literal(self, expr: CppNullptrLiteral) -> StringLiteral:
        """Convert C++ nullptr literal."""
        return StringLiteral(value="null")
    
    def _convert_identifier(self, expr: CppIdentifier) -> Identifier:
        """Convert C++ identifier."""
        return Identifier(name=expr.name)
    
    def _convert_qualified_name(self, expr: CppQualifiedName) -> Identifier:
        """Convert C++ qualified name."""
        # Flatten qualified name to simple identifier
        if expr.scope:
            scope_name = self._expression_to_string(self.convert_expression(expr.scope))
            return Identifier(name=f"{scope_name}::{expr.name}")
        else:
            return Identifier(name=expr.name)
    
    def _convert_binary_op(self, expr: CppBinaryOp) -> BinaryExpression:
        """Convert C++ binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map C++ operators to Runa operators
        operator_map = {
            CppOperator.ADD: BinaryOperator.PLUS,
            CppOperator.SUB: BinaryOperator.MINUS,
            CppOperator.MUL: BinaryOperator.MULTIPLY,
            CppOperator.DIV: BinaryOperator.DIVIDE,
            CppOperator.MOD: BinaryOperator.MODULO,
            CppOperator.EQ: BinaryOperator.EQUALS,
            CppOperator.NE: BinaryOperator.NOT_EQUALS,
            CppOperator.LT: BinaryOperator.LESS_THAN,
            CppOperator.LE: BinaryOperator.LESS_EQUAL,
            CppOperator.GT: BinaryOperator.GREATER_THAN,
            CppOperator.GE: BinaryOperator.GREATER_EQUAL,
            CppOperator.LOGICAL_AND: BinaryOperator.AND,
            CppOperator.LOGICAL_OR: BinaryOperator.OR,
        }
        
        runa_op = operator_map.get(expr.operator, BinaryOperator.PLUS)
        return BinaryExpression(
            left=left,
            operator=runa_op,
            right=right
        )
    
    def _convert_unary_op(self, expr: CppUnaryOp) -> UnaryExpression:
        """Convert C++ unary operation."""
        operand = self.convert_expression(expr.operand)
        
        # Map C++ unary operators to Runa operators
        operator_map = {
            CppOperator.LOGICAL_NOT: "not",
            CppOperator.BIT_NOT: "bitwise not",
            CppOperator.ADD: "positive",
            CppOperator.SUB: "negative",
            CppOperator.PRE_INC: "increment",
            CppOperator.POST_INC: "increment",
            CppOperator.PRE_DEC: "decrement",
            CppOperator.POST_DEC: "decrement",
        }
        
        runa_op = operator_map.get(expr.operator, "unknown_unary_op")
        return UnaryExpression(
            operator=runa_op,
            operand=operand
        )
    
    def _convert_conditional_op(self, expr: CppConditionalOp) -> IfStatement:
        """Convert C++ ternary conditional operator."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.true_expr)
        false_expr = self.convert_expression(expr.false_expr)
        
        # Convert ternary to if-else statement
        return IfStatement(
            condition=condition,
            then_block=[ExpressionStatement(expression=true_expr)],
            else_block=[ExpressionStatement(expression=false_expr)]
        )
    
    def _convert_assignment(self, expr: CppAssignment) -> SetStatement:
        """Convert C++ assignment expression."""
        target = self.convert_expression(expr.left)
        value = self.convert_expression(expr.right)
        
        # Handle compound assignment operators
        if expr.operator == CppOperator.ASSIGN:
            return SetStatement(target=target, value=value)
        else:
            # Convert compound assignment to regular assignment with binary op
            operator_map = {
                CppOperator.ADD_ASSIGN: BinaryOperator.PLUS,
                CppOperator.SUB_ASSIGN: BinaryOperator.MINUS,
                CppOperator.MUL_ASSIGN: BinaryOperator.MULTIPLY,
                CppOperator.DIV_ASSIGN: BinaryOperator.DIVIDE,
                CppOperator.MOD_ASSIGN: BinaryOperator.MODULO,
            }
            
            if expr.operator in operator_map:
                binary_op = BinaryExpression(
                    left=target,
                    operator=operator_map[expr.operator],
                    right=value
                )
                return SetStatement(target=target, value=binary_op)
            
            return SetStatement(target=target, value=value)
    
    def _convert_call(self, expr: CppCall) -> FunctionCall:
        """Convert C++ function call."""
        function = self.convert_expression(expr.function)
        arguments = [(f"arg_{i}", arg) for i, arg in enumerate([self.convert_expression(arg) for arg in expr.arguments])]
        
        # Extract function name
        if hasattr(function, 'name'):
            func_name = function.name
        else:
            func_name = "unknown_function"
            
        return FunctionCall(
            function_name=func_name,
            arguments=arguments
        )
    
    def _convert_member_access(self, expr: CppMemberAccess) -> MemberAccess:
        """Convert C++ member access."""
        object_expr = self.convert_expression(expr.object)
        return MemberAccess(
            object=object_expr,
            member=expr.member
        )
    
    def _convert_array_subscript(self, expr: CppArraySubscript) -> IndexAccess:
        """Convert C++ array subscript."""
        array = self.convert_expression(expr.array)
        index = self.convert_expression(expr.index)
        
        return IndexAccess(
            object=array,
            index=index
        )
    
    def _convert_cast(self, expr: CppCast) -> FunctionCall:
        """Convert C++ cast to Runa type conversion."""
        operand = self.convert_expression(expr.operand)
        target_type = self._convert_type(expr.target_type)
        
        # Convert cast to function call
        type_name = getattr(target_type, 'name', 'Unknown')
        return FunctionCall(
            function_name=f"cast_to_{type_name}",
            arguments=[("value", operand)]
        )
    
    def _convert_new_expr(self, expr: CppNewExpr) -> FunctionCall:
        """Convert C++ new expression."""
        type_name = self._type_to_string(expr.target_type)
        
        args = []
        if expr.initializer:
            args.append(self.convert_expression(expr.initializer))
        
        if expr.is_array and expr.array_size:
            # Array allocation
            size_arg = self.convert_expression(expr.array_size)
            return FunctionCall(
                function_name=f"new_array_{type_name}",
                arguments=[("size", size_arg)] + [(f"arg_{i}", arg) for i, arg in enumerate(args)]
            )
        else:
            # Single object allocation
            return FunctionCall(
                function_name=f"new_{type_name}",
                arguments=[(f"arg_{i}", arg) for i, arg in enumerate(args)]
            )
    
    def _convert_delete_expr(self, expr: CppDeleteExpr) -> FunctionCall:
        """Convert C++ delete expression."""
        operand = self.convert_expression(expr.operand)
        
        if expr.is_array:
            return FunctionCall(
                function_name="delete_array",
                arguments=[("object", operand)]
            )
        else:
            return FunctionCall(
                function_name="delete",
                arguments=[("object", operand)]
            )
    
    def _convert_lambda(self, expr: CppLambda) -> ProcessDefinition:
        """Convert C++ lambda expression."""
        parameters = []
        if expr.parameters:
            for param in expr.parameters.parameters:
                param_type = self._convert_type(param.param_type)
                param_name = param.name or f"lambda_param_{len(parameters)}"
                runa_param = Parameter(param_name, param_type)
                parameters.append(runa_param)
        
        body = []
        converted_body = self.convert_statement(expr.body)
        if isinstance(converted_body, list):
            body = converted_body
        elif converted_body:
            body = [converted_body]
        
        return_type = None
        if expr.return_type:
            return_type = self._convert_type(expr.return_type)
        
        lambda_def = ProcessDefinition(
            name=f"lambda_{self.function_counter}",
            parameters=parameters,
            return_type=return_type,
            body=body
        )
        self.function_counter += 1
        
        # Add metadata for lambda
        lambda_def.metadata = lambda_def.metadata or {}
        lambda_def.metadata["is_lambda"] = True
        
        return lambda_def
    
    def _convert_initializer_list(self, expr: CppInitializerList) -> ListLiteral:
        """Convert C++ initializer list."""
        elements = [self.convert_expression(elem) for elem in expr.elements]
        return ListLiteral(elements)
    
    def _convert_type(self, cpp_type: CppType) -> BasicType:
        """Convert C++ type to Runa type."""
        if isinstance(cpp_type, CppBuiltinType):
            # Map C++ builtin types to Runa types
            type_map = {
                "int": "Integer",
                "float": "Float",
                "double": "Float",
                "char": "Character",
                "bool": "Boolean",
                "void": "Void",
                "string": "String",
                "std::string": "String",
            }
            runa_name = type_map.get(cpp_type.name, cpp_type.name)
            return BasicType(runa_name)
        
        elif isinstance(cpp_type, CppPointerType):
            # Convert pointer type
            pointee = self._convert_type(cpp_type.pointee_type)
            return BasicType(f"Pointer[{pointee.name}]")
        
        elif isinstance(cpp_type, CppReferenceType):
            # Convert reference type
            referenced = self._convert_type(cpp_type.referenced_type)
            return BasicType(f"Reference[{referenced.name}]")
        
        elif isinstance(cpp_type, CppArrayType):
            # Convert array type
            element = self._convert_type(cpp_type.element_type)
            return BasicType(f"Array[{element.name}]")
        
        elif isinstance(cpp_type, CppAutoType):
            return BasicType("Auto")
        
        else:
            # Default fallback
            return BasicType("Unknown")
    
    def _type_to_string(self, cpp_type: CppType) -> str:
        """Convert C++ type to string representation."""
        if isinstance(cpp_type, CppBuiltinType):
            return cpp_type.name
        elif isinstance(cpp_type, CppPointerType):
            return f"{self._type_to_string(cpp_type.pointee_type)}*"
        elif isinstance(cpp_type, CppReferenceType):
            return f"{self._type_to_string(cpp_type.referenced_type)}&"
        else:
            return "unknown_type"
    
    def _expression_to_string(self, expr: Expression) -> str:
        """Convert Runa expression to string representation."""
        if isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, StringLiteral):
            return str(expr.value)
        else:
            return "unknown_expr"
    
    def _log_error(self, message: str):
        """Log error message to stderr."""
        import sys
        print(f"CPP Converter Error: {message}", file=sys.stderr)


class RunaToCppConverter:
    """Converts Runa AST to C++ AST."""
    
    def __init__(self):
        self.variable_counter = 0
        self.function_counter = 0
        self.class_counter = 0
    
    def convert(self, runa_ast: Program) -> CppTranslationUnit:
        """Convert Runa program to C++ translation unit."""
        declarations = []
        
        for stmt in runa_ast.statements:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    declarations.extend(converted)
                else:
                    declarations.append(converted)
        
        return CppTranslationUnit(declarations)
    
    def convert_statement(self, stmt: Statement) -> Union[CppDeclaration, CppStatement, List[Union[CppDeclaration, CppStatement]], None]:
        """Convert Runa statement to C++ declaration or statement."""
        if isinstance(stmt, LetStatement):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, ProcessDefinition):
            return self._convert_function_declaration(stmt)
        elif isinstance(stmt, TypeDefinition):
            return self._convert_class_declaration(stmt)
        elif isinstance(stmt, SetStatement):
            return self._convert_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            return self._convert_conditional(stmt)
        elif isinstance(stmt, WhileLoop):
            return self._convert_loop(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self._convert_return(stmt)
        elif isinstance(stmt, BreakStatement):
            return CppBreakStmt()
        elif isinstance(stmt, ContinueStatement):
            return CppContinueStmt()
        elif isinstance(stmt, ExpressionStatement):
            return self._convert_expression_statement(stmt)
        
        return None
    
    def convert_expression(self, expr: Expression) -> CppExpression:
        """Convert Runa expression to C++ expression."""
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
        elif isinstance(expr, IfStatement):
            return self._convert_conditional_expression(expr)
        elif isinstance(expr, ProcessDefinition):
            return self._convert_lambda(expr)
        elif isinstance(expr, ListLiteral):
            return self._convert_list(expr)
        
        # Fallback
        return CppIdentifier("unknown_expression")
    
    def _convert_variable_declaration(self, stmt: LetStatement) -> CppVariableDecl:
        """Convert Runa variable declaration."""
        cpp_type = self._convert_type(stmt.type_annotation)
        
        initializer = None
        if stmt.value:
            initializer = self.convert_expression(stmt.value)
        
        return CppVariableDecl(name=stmt.identifier, var_type=cpp_type, initializer=initializer)
    
    def _convert_function_declaration(self, stmt: ProcessDefinition) -> CppFunctionDecl:
        """Convert Runa function declaration."""
        return_type = self._convert_type(stmt.return_type)
        
        parameters = []
        for param in stmt.parameters:
            cpp_type = self._convert_type(param.type_annotation)
            default_value = None
            if hasattr(param, 'default_value') and param.default_value:
                default_value = self.convert_expression(param.default_value)
            
            cpp_param = CppParameter(
                name=param.name,
                param_type=cpp_type,
                default_value=default_value
            )
            parameters.append(cpp_param)
        
        param_list = CppParameterList(parameters=parameters)
        
        body = None
        if stmt.body:
            cpp_statements = []
            for runa_stmt in stmt.body:
                converted = self.convert_statement(runa_stmt)
                if converted:
                    if isinstance(converted, list):
                        cpp_statements.extend(converted)
                    else:
                        cpp_statements.append(converted)
            
            body = CppCompoundStmt(statements=cpp_statements)
        
        return CppFunctionDecl(name=stmt.name, return_type=return_type, parameters=param_list, body=body)
    
    def _convert_class_declaration(self, stmt: TypeDefinition) -> CppClassDecl:
        """Convert Runa class declaration."""
        members = []
        
        # Convert fields
        for field in stmt.fields:
            member = self._convert_variable_declaration(field)
            members.append(member)
        
        # Convert methods
        for method in stmt.methods:
            member = self._convert_function_declaration(method)
            members.append(member)
        
        # Handle base classes
        base_classes = []
        for base_name in stmt.base_classes:
            base_type = CppBuiltinType(name=base_name)
            base_spec = CppBaseSpecifier(base_type=base_type)
            base_classes.append(base_spec)
        
        return CppClassDecl(name=stmt.name, base_classes=base_classes, members=members)
    
    def _convert_assignment(self, stmt: SetStatement) -> CppExpressionStmt:
        """Convert Runa assignment."""
        target = self.convert_expression(stmt.target)
        value = self.convert_expression(stmt.value)
        
        assignment = CppAssignment(left=target, operator=CppOperator.ASSIGN, right=value)
        return CppExpressionStmt(expression=assignment)
    
    def _convert_conditional(self, stmt: IfStatement) -> CppIfStmt:
        """Convert Runa conditional."""
        condition = self.convert_expression(stmt.condition)
        
        then_statements = []
        for then_stmt in stmt.then_block:
            converted = self.convert_statement(then_stmt)
            if converted:
                if isinstance(converted, list):
                    then_statements.extend(converted)
                else:
                    then_statements.append(converted)
        
        then_body = CppCompoundStmt(statements=then_statements)
        
        else_body = None
        if stmt.else_block:
            else_statements = []
            for else_stmt in stmt.else_block:
                converted = self.convert_statement(else_stmt)
                if converted:
                    if isinstance(converted, list):
                        else_statements.extend(converted)
                    else:
                        else_statements.append(converted)
            
            else_body = CppCompoundStmt(statements=else_statements)
        
        return CppIfStmt(condition=condition, then_stmt=then_body, else_stmt=else_body)
    
    def _convert_loop(self, stmt: WhileLoop) -> CppStatement:
        """Convert Runa loop."""
        condition = self.convert_expression(stmt.condition)
        
        body_statements = []
        for body_stmt in stmt.block:
            converted = self.convert_statement(body_stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = CppCompoundStmt(statements=body_statements)
        
        if stmt.loop_type == "while":
            return CppWhileStmt(condition=condition, body=body)
        else:
            # Default to while loop
            return CppWhileStmt(condition=condition, body=body)
    
    def _convert_return(self, stmt: ReturnStatement) -> CppReturnStmt:
        """Convert Runa return."""
        value = None
        if stmt.value:
            value = self.convert_expression(stmt.value)
        
        return CppReturnStmt(value=value)
    
    def _convert_expression_statement(self, stmt: ExpressionStatement) -> CppExpressionStmt:
        """Convert Runa expression statement."""
        expr = self.convert_expression(stmt.expression)
        return CppExpressionStmt(expression=expr)
    
    def _convert_literal(self, expr: StringLiteral) -> CppExpression:
        """Convert Runa literal."""
        if expr.literal_type == "integer":
            return CppIntegerLiteral(value=expr.value)
        elif expr.literal_type == "float":
            return CppFloatingLiteral(value=expr.value)
        elif expr.literal_type == "string":
            return CppStringLiteral(value=f'"{expr.value}"')
        elif expr.literal_type == "character":
            return CppCharacterLiteral(value=f"'{expr.value}'")
        elif expr.literal_type == "boolean":
            return CppBooleanLiteral(value=expr.value)
        elif expr.literal_type == "null":
            return CppNullptrLiteral()
        else:
            return CppStringLiteral(value=f'"{expr.value}"')
    
    def _convert_identifier(self, expr: Identifier) -> CppIdentifier:
        """Convert Runa identifier."""
        return CppIdentifier(name=expr.name)
    
    def _convert_binary_operation(self, expr: BinaryExpression) -> CppBinaryOp:
        """Convert Runa binary operation."""
        left = self.convert_expression(expr.left)
        right = self.convert_expression(expr.right)
        
        # Map Runa operators to C++ operators
        operator_map = {
            "plus": CppOperator.ADD,
            "minus": CppOperator.SUB,
            "times": CppOperator.MUL,
            "divided by": CppOperator.DIV,
            "modulo": CppOperator.MOD,
            "is equal to": CppOperator.EQ,
            "is not equal to": CppOperator.NE,
            "is less than": CppOperator.LT,
            "is less than or equal to": CppOperator.LE,
            "is greater than": CppOperator.GT,
            "is greater than or equal to": CppOperator.GE,
            "and": CppOperator.LOGICAL_AND,
            "or": CppOperator.LOGICAL_OR,
        }
        
        cpp_op = operator_map.get(expr.operator, CppOperator.ADD)
        return CppBinaryOp(left=left, operator=cpp_op, right=right)
    
    def _convert_unary_operation(self, expr: UnaryExpression) -> CppUnaryOp:
        """Convert Runa unary operation."""
        operand = self.convert_expression(expr.operand)
        
        operator_map = {
            "not": CppOperator.LOGICAL_NOT,
            "negative": CppOperator.SUB,
            "positive": CppOperator.ADD,
            "increment": CppOperator.PRE_INC,
            "decrement": CppOperator.PRE_DEC,
        }
        
        cpp_op = operator_map.get(expr.operator, CppOperator.LOGICAL_NOT)
        return CppUnaryOp(operator=cpp_op, operand=operand)
    
    def _convert_function_call(self, expr: FunctionCall) -> CppCall:
        """Convert Runa function call."""
        # FunctionCall has function_name (str) and arguments (list of tuples)
        function_name = expr.function_name
        arguments = [self.convert_expression(arg[1]) for arg in expr.arguments]
        function = CppIdentifier(name=function_name)
        
        return CppCall(function=function, arguments=arguments)
    
    def _convert_member_access(self, expr: MemberAccess) -> CppMemberAccess:
        """Convert Runa member access."""
        object_expr = self.convert_expression(expr.object)
        return CppMemberAccess(object=object_expr, member=expr.member)
    
    def _convert_index_access(self, expr: IndexAccess) -> CppArraySubscript:
        """Convert Runa index access."""
        array = self.convert_expression(expr.object)
        index = self.convert_expression(expr.index)
        
        return CppArraySubscript(array=array, index=index)
    
    def _convert_conditional_expression(self, expr: IfStatement) -> CppConditionalOp:
        """Convert Runa conditional expression."""
        condition = self.convert_expression(expr.condition)
        true_expr = self.convert_expression(expr.true_value)
        false_expr = self.convert_expression(expr.false_value)
        
        return CppConditionalOp(condition=condition, true_expr=true_expr, false_expr=false_expr)
    
    def _convert_lambda(self, expr: ProcessDefinition) -> CppLambda:
        """Convert Runa lambda."""
        parameters = []
        for param in expr.parameters:
            cpp_type = self._convert_type(param.type_annotation)
            cpp_param = CppParameter(name=param.name, param_type=cpp_type)
            parameters.append(cpp_param)
        
        param_list = CppParameterList(parameters=parameters)
        
        body_statements = []
        for stmt in expr.body:
            converted = self.convert_statement(stmt)
            if converted:
                if isinstance(converted, list):
                    body_statements.extend(converted)
                else:
                    body_statements.append(converted)
        
        body = CppCompoundStmt(statements=body_statements)
        
        return_type = None
        if expr.return_type:
            return_type = self._convert_type(expr.return_type)
        
        return CppLambda(
            parameters=param_list,
            return_type=return_type,
            body=body
        )
    
    def _convert_list(self, expr: ListLiteral) -> CppInitializerList:
        """Convert Runa list."""
        elements = [self.convert_expression(elem) for elem in expr.elements]
        return CppInitializerList(elements=elements)
    
    def _convert_type(self, runa_type: BasicType) -> CppType:
        """Convert Runa type to C++ type."""
        # Map Runa types to C++ types
        type_map = {
            "Integer": "int",
            "Float": "double",
            "Character": "char",
            "Boolean": "bool",
            "String": "std::string",
            "Void": "void",
        }
        
        cpp_name = type_map.get(runa_type.name, runa_type.name)
        return CppBuiltinType(name=cpp_name)


# Convenience functions
def cpp_to_runa(cpp_ast: CppTranslationUnit) -> Program:
    """Convert C++ AST to Runa AST."""
    converter = CppToRunaConverter()
    return converter.convert(cpp_ast)


def runa_to_cpp(runa_ast: Program) -> CppTranslationUnit:
    """Convert Runa AST to C++ AST."""
    converter = RunaToCppConverter()
    return converter.convert(runa_ast)