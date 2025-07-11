#!/usr/bin/env python3
"""
Scala ↔ Runa Bidirectional Converter

Converts between Scala AST and Runa AST in both directions.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from .scala_ast import *
from ....core.runa_ast import *


class ScalaToRunaConverter:
    """Converts Scala AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'Int': 'Integer',
            'Long': 'Integer',
            'Float': 'Float',
            'Double': 'Float',
            'String': 'String',
            'Boolean': 'Boolean',
            'Char': 'Character',
            'Unit': 'Void',
            'Any': 'Any',
            'AnyRef': 'Any',
            'AnyVal': 'Any',
            'Nothing': 'Never',
            'Null': 'Null',
            'List': 'List',
            'Vector': 'List',
            'Set': 'Set',
            'Map': 'Dictionary',
            'Array': 'List',
            'Option': 'Optional',
            'Some': 'Optional',
            'None': 'Null',
            'Either': 'Union',
            'Try': 'Result',
            'Future': 'Future',
        }
    
    def convert(self, scala_node: ScalaNode) -> ASTNode:
        """Convert Scala AST node to Runa AST node."""
        try:
            if isinstance(scala_node, ScalaSourceFile):
                return self._convert_source_file(scala_node)
            elif isinstance(scala_node, ScalaClassDeclaration):
                return self._convert_class_declaration(scala_node)
            elif isinstance(scala_node, ScalaTraitDeclaration):
                return self._convert_trait_declaration(scala_node)
            elif isinstance(scala_node, ScalaObjectDeclaration):
                return self._convert_object_declaration(scala_node)
            elif isinstance(scala_node, ScalaEnumDeclaration):
                return self._convert_enum_declaration(scala_node)
            elif isinstance(scala_node, ScalaFunctionDeclaration):
                return self._convert_function_declaration(scala_node)
            elif isinstance(scala_node, ScalaValueDeclaration):
                return self._convert_value_declaration(scala_node)
            elif isinstance(scala_node, ScalaVariableDeclaration):
                return self._convert_variable_declaration(scala_node)
            elif isinstance(scala_node, ScalaIdentifier):
                return self._convert_identifier(scala_node)
            elif isinstance(scala_node, ScalaLiteral):
                return self._convert_literal(scala_node)
            elif isinstance(scala_node, ScalaIfExpression):
                return self._convert_if_expression(scala_node)
            elif isinstance(scala_node, ScalaMatchExpression):
                return self._convert_match_expression(scala_node)
            elif isinstance(scala_node, ScalaForExpression):
                return self._convert_for_expression(scala_node)
            elif isinstance(scala_node, ScalaBlockExpression):
                return self._convert_block_expression(scala_node)
            elif isinstance(scala_node, ScalaFunctionCallExpression):
                return self._convert_function_call_expression(scala_node)
            elif isinstance(scala_node, ScalaMethodCallExpression):
                return self._convert_method_call_expression(scala_node)
            elif isinstance(scala_node, ScalaBinaryExpression):
                return self._convert_binary_expression(scala_node)
            elif isinstance(scala_node, ScalaUnaryExpression):
                return self._convert_unary_expression(scala_node)
            elif isinstance(scala_node, ScalaLambdaExpression):
                return self._convert_lambda_expression(scala_node)
            elif isinstance(scala_node, ScalaTupleExpression):
                return self._convert_tuple_expression(scala_node)
            elif isinstance(scala_node, ScalaListExpression):
                return self._convert_list_expression(scala_node)
            elif isinstance(scala_node, ScalaNewExpression):
                return self._convert_new_expression(scala_node)
            elif isinstance(scala_node, ScalaAssignmentExpression):
                return self._convert_assignment_expression(scala_node)
            else:
                return self._create_placeholder(scala_node)
        except Exception as e:
            self.logger.error(f"Failed to convert Scala node: {e}")
            return self._create_placeholder(scala_node)
    
    def _convert_source_file(self, source_file: ScalaSourceFile) -> Program:
        """Convert Scala source file to Runa program."""
        statements = []
        
        # Convert package declaration
        if source_file.package_declaration:
            statements.append(PackageStatement(
                name=source_file.package_declaration.name
            ))
        
        # Convert imports
        for import_decl in source_file.imports:
            if import_decl.selectors:
                # Import with selectors
                for selector in import_decl.selectors:
                    if "=>" in selector:
                        parts = selector.split("=>")
                        original_name = parts[0].strip()
                        alias = parts[1].strip()
                        statements.append(ImportStatement(
                            module_name=f"{import_decl.path}.{original_name}",
                            imported_names=[alias]
                        ))
                    else:
                        statements.append(ImportStatement(
                            module_name=f"{import_decl.path}.{selector}",
                            imported_names=[selector]
                        ))
            else:
                # Simple import
                statements.append(ImportStatement(
                    module_name=import_decl.path,
                    imported_names=["*"]
                ))
        
        # Convert declarations
        for decl in source_file.declarations:
            converted = self.convert(decl)
            if converted:
                statements.append(converted)
        
        return Program(statements=statements)
    
    def _convert_class_declaration(self, class_decl: ScalaClassDeclaration) -> StructDefinition:
        """Convert Scala class to Runa struct."""
        fields = []
        
        # Convert constructor parameters to fields
        for param in class_decl.constructor_parameters:
            field = FieldDefinition(
                name=param.name,
                type_annotation=self._convert_type(param.parameter_type),
                annotations={
                    "scala_implicit": param.is_implicit,
                    "scala_by_name": param.is_by_name,
                    "scala_varargs": param.is_varargs
                }
            )
            fields.append(field)
        
        # Convert member declarations that are fields
        for member in class_decl.members:
            if isinstance(member, (ScalaValueDeclaration, ScalaVariableDeclaration)):
                field = FieldDefinition(
                    name=member.name,
                    type_annotation=self._convert_type(member.type_annotation),
                    annotations={
                        "scala_mutable": isinstance(member, ScalaVariableDeclaration),
                        "scala_lazy": getattr(member, 'is_lazy', False),
                        "scala_implicit": getattr(member, 'is_implicit', False),
                        "scala_override": getattr(member, 'is_override', False)
                    }
                )
                fields.append(field)
        
        return StructDefinition(
            name=class_decl.name,
            fields=fields,
            annotations={
                "scala_type": "class",
                "scala_abstract": class_decl.is_abstract,
                "scala_final": class_decl.is_final,
                "scala_sealed": class_decl.is_sealed,
                "scala_case": class_decl.is_case,
                "scala_extends": class_decl.extends_clause.name if class_decl.extends_clause else None,
                "scala_with": [t.name for t in class_decl.with_clauses if hasattr(t, 'name')],
                "scala_type_params": [tp.name for tp in class_decl.type_parameters]
            }
        )
    
    def _convert_trait_declaration(self, trait_decl: ScalaTraitDeclaration) -> StructDefinition:
        """Convert Scala trait to Runa struct."""
        fields = []
        
        # Convert member declarations that are fields
        for member in trait_decl.members:
            if isinstance(member, (ScalaValueDeclaration, ScalaVariableDeclaration)):
                field = FieldDefinition(
                    name=member.name,
                    type_annotation=self._convert_type(member.type_annotation),
                    annotations={
                        "scala_mutable": isinstance(member, ScalaVariableDeclaration),
                        "scala_lazy": getattr(member, 'is_lazy', False),
                        "scala_implicit": getattr(member, 'is_implicit', False),
                        "scala_override": getattr(member, 'is_override', False)
                    }
                )
                fields.append(field)
        
        return StructDefinition(
            name=trait_decl.name,
            fields=fields,
            annotations={
                "scala_type": "trait",
                "scala_sealed": trait_decl.is_sealed,
                "scala_extends": trait_decl.extends_clause.name if trait_decl.extends_clause else None,
                "scala_with": [t.name for t in trait_decl.with_clauses if hasattr(t, 'name')],
                "scala_type_params": [tp.name for tp in trait_decl.type_parameters]
            }
        )
    
    def _convert_object_declaration(self, object_decl: ScalaObjectDeclaration) -> StructDefinition:
        """Convert Scala object to Runa struct."""
        fields = []
        
        # Convert member declarations that are fields
        for member in object_decl.members:
            if isinstance(member, (ScalaValueDeclaration, ScalaVariableDeclaration)):
                field = FieldDefinition(
                    name=member.name,
                    type_annotation=self._convert_type(member.type_annotation),
                    annotations={
                        "scala_mutable": isinstance(member, ScalaVariableDeclaration),
                        "scala_lazy": getattr(member, 'is_lazy', False),
                        "scala_implicit": getattr(member, 'is_implicit', False),
                        "scala_override": getattr(member, 'is_override', False)
                    }
                )
                fields.append(field)
        
        return StructDefinition(
            name=object_decl.name,
            fields=fields,
            annotations={
                "scala_type": "object",
                "scala_case": object_decl.is_case,
                "scala_extends": object_decl.extends_clause.name if object_decl.extends_clause else None,
                "scala_with": [t.name for t in object_decl.with_clauses if hasattr(t, 'name')]
            }
        )
    
    def _convert_enum_declaration(self, enum_decl: ScalaEnumDeclaration) -> UnionType:
        """Convert Scala enum to Runa union type."""
        types = []
        
        for case in enum_decl.cases:
            types.append(BasicType(name=case.name))
        
        return UnionType(
            types=types,
            annotations={
                "scala_enum": enum_decl.name,
                "scala_type_params": [tp.name for tp in enum_decl.type_parameters]
            }
        )
    
    def _convert_function_declaration(self, func_decl: ScalaFunctionDeclaration) -> ProcessDeclaration:
        """Convert Scala function to Runa process."""
        parameters = []
        
        # Convert all parameter lists (flatten for Runa)
        for param_list in func_decl.parameter_lists:
            for param in param_list:
                field = FieldDefinition(
                    name=param.name,
                    type_annotation=self._convert_type(param.parameter_type),
                    annotations={
                        "scala_implicit": param.is_implicit,
                        "scala_by_name": param.is_by_name,
                        "scala_varargs": param.is_varargs,
                        "scala_using": param.is_using
                    }
                )
                parameters.append(field)
        
        # Convert body
        body = None
        if func_decl.body:
            body = self.convert(func_decl.body)
        
        return ProcessDeclaration(
            name=func_decl.name,
            parameters=parameters,
            return_type=self._convert_type(func_decl.return_type),
            body=body,
            annotations={
                "scala_abstract": func_decl.is_abstract,
                "scala_override": func_decl.is_override,
                "scala_implicit": func_decl.is_implicit,
                "scala_inline": func_decl.is_inline,
                "scala_type_params": [tp.name for tp in func_decl.type_parameters]
            }
        )
    
    def _convert_value_declaration(self, val_decl: ScalaValueDeclaration) -> LetStatement:
        """Convert Scala val to Runa let statement."""
        return LetStatement(
            name=val_decl.name,
            type_annotation=self._convert_type(val_decl.type_annotation),
            value=self.convert(val_decl.value) if val_decl.value else None,
            annotations={
                "scala_lazy": val_decl.is_lazy,
                "scala_implicit": val_decl.is_implicit,
                "scala_override": val_decl.is_override
            }
        )
    
    def _convert_variable_declaration(self, var_decl: ScalaVariableDeclaration) -> VariableDeclaration:
        """Convert Scala var to Runa variable declaration."""
        return VariableDeclaration(
            name=var_decl.name,
            type_annotation=self._convert_type(var_decl.type_annotation),
            initial_value=self.convert(var_decl.value) if var_decl.value else None,
            annotations={
                "scala_override": var_decl.is_override
            }
        )
    
    def _convert_identifier(self, identifier: ScalaIdentifier) -> Identifier:
        """Convert Scala identifier to Runa identifier."""
        return Identifier(name=identifier.name)
    
    def _convert_literal(self, literal: ScalaLiteral) -> Expression:
        """Convert Scala literal to Runa literal."""
        if literal.literal_type in ["int", "long"]:
            return IntegerLiteral(value=int(literal.value))
        elif literal.literal_type in ["float", "double"]:
            return FloatLiteral(value=float(literal.value))
        elif literal.literal_type == "string":
            return StringLiteral(value=str(literal.value))
        elif literal.literal_type == "char":
            return CharacterLiteral(value=str(literal.value))
        elif literal.literal_type == "bool":
            return BooleanLiteral(value=bool(literal.value))
        elif literal.literal_type == "null":
            return NullLiteral()
        elif literal.literal_type == "unit":
            return UnitLiteral()
        elif literal.literal_type == "symbol":
            return SymbolLiteral(value=str(literal.value))
        else:
            return StringLiteral(value=str(literal.value))
    
    def _convert_if_expression(self, if_expr: ScalaIfExpression) -> IfExpression:
        """Convert Scala if expression to Runa if expression."""
        return IfExpression(
            condition=self.convert(if_expr.condition) if if_expr.condition else None,
            then_expression=self.convert(if_expr.then_expression) if if_expr.then_expression else None,
            else_expression=self.convert(if_expr.else_expression) if if_expr.else_expression else None
        )
    
    def _convert_match_expression(self, match_expr: ScalaMatchExpression) -> MatchExpression:
        """Convert Scala match expression to Runa match expression."""
        cases = []
        
        for scala_case in match_expr.cases:
            pattern = self._convert_pattern(scala_case.pattern)
            guard = self.convert(scala_case.guard) if scala_case.guard else None
            body = self.convert(scala_case.body) if scala_case.body else None
            
            case = MatchCase(
                pattern=pattern,
                guard=guard,
                body=body
            )
            cases.append(case)
        
        return MatchExpression(
            scrutinee=self.convert(match_expr.scrutinee) if match_expr.scrutinee else None,
            cases=cases
        )
    
    def _convert_for_expression(self, for_expr: ScalaForExpression) -> ForExpression:
        """Convert Scala for expression to Runa for expression."""
        # Convert generators to comprehensions
        comprehensions = []
        
        for generator in for_expr.generators:
            pattern = self._convert_pattern(generator.pattern)
            iterable = self.convert(generator.expression) if generator.expression else None
            
            comprehension = Comprehension(
                target=pattern,
                iter=iterable,
                conditions=[self.convert(guard) for guard in generator.guards]
            )
            comprehensions.append(comprehension)
        
        if for_expr.is_yield and for_expr.yield_expression:
            # For-yield becomes list comprehension
            return ListComprehension(
                element=self.convert(for_expr.yield_expression),
                comprehensions=comprehensions
            )
        else:
            # For-do becomes for loop
            return ForExpression(
                target=comprehensions[0].target if comprehensions else None,
                iter=comprehensions[0].iter if comprehensions else None,
                body=self.convert(for_expr.yield_expression) if for_expr.yield_expression else None
            )
    
    def _convert_block_expression(self, block_expr: ScalaBlockExpression) -> BlockExpression:
        """Convert Scala block expression to Runa block expression."""
        statements = []
        
        # Convert statements
        for stmt in block_expr.statements:
            converted = self.convert(stmt)
            if converted:
                statements.append(converted)
        
        # Convert result expression
        result = None
        if block_expr.result_expression:
            result = self.convert(block_expr.result_expression)
        
        return BlockExpression(
            statements=statements,
            result_expression=result
        )
    
    def _convert_function_call_expression(self, call_expr: ScalaFunctionCallExpression) -> FunctionCall:
        """Convert Scala function call to Runa function call."""
        # Flatten argument lists
        arguments = []
        for arg_list in call_expr.arguments:
            for arg in arg_list:
                arguments.append(self.convert(arg.value) if arg.value else None)
        
        return FunctionCall(
            function=self.convert(call_expr.function) if call_expr.function else None,
            arguments=[arg for arg in arguments if arg is not None]
        )
    
    def _convert_method_call_expression(self, method_call: ScalaMethodCallExpression) -> MethodCall:
        """Convert Scala method call to Runa method call."""
        # Flatten argument lists
        arguments = []
        for arg_list in method_call.arguments:
            for arg in arg_list:
                arguments.append(self.convert(arg.value) if arg.value else None)
        
        return MethodCall(
            receiver=self.convert(method_call.receiver) if method_call.receiver else None,
            method_name=method_call.method_name,
            arguments=[arg for arg in arguments if arg is not None]
        )
    
    def _convert_binary_expression(self, binary_expr: ScalaBinaryExpression) -> BinaryOperation:
        """Convert Scala binary expression to Runa binary operation."""
        return BinaryOperation(
            left=self.convert(binary_expr.left) if binary_expr.left else None,
            operator=self._convert_operator(binary_expr.operator),
            right=self.convert(binary_expr.right) if binary_expr.right else None
        )
    
    def _convert_unary_expression(self, unary_expr: ScalaUnaryExpression) -> UnaryOperation:
        """Convert Scala unary expression to Runa unary operation."""
        return UnaryOperation(
            operator=self._convert_operator(unary_expr.operator),
            operand=self.convert(unary_expr.operand) if unary_expr.operand else None
        )
    
    def _convert_lambda_expression(self, lambda_expr: ScalaLambdaExpression) -> LambdaExpression:
        """Convert Scala lambda expression to Runa lambda expression."""
        parameters = []
        
        for param in lambda_expr.parameters:
            field = FieldDefinition(
                name=param.name,
                type_annotation=self._convert_type(param.parameter_type)
            )
            parameters.append(field)
        
        return LambdaExpression(
            parameters=parameters,
            body=self.convert(lambda_expr.body) if lambda_expr.body else None
        )
    
    def _convert_tuple_expression(self, tuple_expr: ScalaTupleExpression) -> TupleExpression:
        """Convert Scala tuple expression to Runa tuple expression."""
        elements = []
        
        for element in tuple_expr.elements:
            converted = self.convert(element)
            if converted:
                elements.append(converted)
        
        return TupleExpression(elements=elements)
    
    def _convert_list_expression(self, list_expr: ScalaListExpression) -> ListExpression:
        """Convert Scala list expression to Runa list expression."""
        elements = []
        
        for element in list_expr.elements:
            converted = self.convert(element)
            if converted:
                elements.append(converted)
        
        return ListExpression(elements=elements)
    
    def _convert_new_expression(self, new_expr: ScalaNewExpression) -> ConstructorCall:
        """Convert Scala new expression to Runa constructor call."""
        # Flatten argument lists
        arguments = []
        for arg_list in new_expr.arguments:
            for arg in arg_list:
                arguments.append(self.convert(arg.value) if arg.value else None)
        
        return ConstructorCall(
            class_name=new_expr.class_type.name if hasattr(new_expr.class_type, 'name') else str(new_expr.class_type),
            arguments=[arg for arg in arguments if arg is not None]
        )
    
    def _convert_assignment_expression(self, assign_expr: ScalaAssignmentExpression) -> Assignment:
        """Convert Scala assignment expression to Runa assignment."""
        return Assignment(
            target=self.convert(assign_expr.target) if assign_expr.target else None,
            value=self.convert(assign_expr.value) if assign_expr.value else None
        )
    
    def _convert_pattern(self, pattern: ScalaPattern) -> Pattern:
        """Convert Scala pattern to Runa pattern."""
        if isinstance(pattern, ScalaWildcardPattern):
            return WildcardPattern()
        elif isinstance(pattern, ScalaIdentifierPattern):
            return VariablePattern(name=pattern.name)
        elif isinstance(pattern, ScalaLiteralPattern):
            return LiteralPattern(value=self.convert(pattern.literal) if pattern.literal else None)
        elif isinstance(pattern, ScalaConstructorPattern):
            patterns = [self._convert_pattern(p) for p in pattern.patterns]
            return ConstructorPattern(
                constructor=pattern.constructor.name if hasattr(pattern.constructor, 'name') else str(pattern.constructor),
                patterns=patterns
            )
        elif isinstance(pattern, ScalaTuplePattern):
            patterns = [self._convert_pattern(p) for p in pattern.patterns]
            return TuplePattern(patterns=patterns)
        elif isinstance(pattern, ScalaTypedPattern):
            return TypedPattern(
                pattern=self._convert_pattern(pattern.pattern) if pattern.pattern else None,
                type_annotation=self._convert_type(pattern.pattern_type)
            )
        else:
            return WildcardPattern()
    
    def _convert_type(self, scala_type: Optional[ScalaType]) -> Optional[TypeExpression]:
        """Convert Scala type to Runa type."""
        if not scala_type:
            return None
        
        if isinstance(scala_type, ScalaTypeIdentifier):
            runa_type_name = self.type_mapping.get(scala_type.name, scala_type.name)
            
            if scala_type.type_arguments:
                # Generic type
                type_args = [self._convert_type(arg) for arg in scala_type.type_arguments]
                return GenericType(
                    base_type=BasicType(name=runa_type_name),
                    type_arguments=[arg for arg in type_args if arg is not None]
                )
            else:
                return BasicType(name=runa_type_name)
        
        elif isinstance(scala_type, ScalaFunctionType):
            param_types = [self._convert_type(pt) for pt in scala_type.parameter_types]
            return FunctionType(
                parameter_types=[pt for pt in param_types if pt is not None],
                return_type=self._convert_type(scala_type.return_type)
            )
        
        elif isinstance(scala_type, ScalaTupleType):
            element_types = [self._convert_type(et) for et in scala_type.element_types]
            return TupleType(element_types=[et for et in element_types if et is not None])
        
        elif isinstance(scala_type, ScalaCompoundType):
            types = [self._convert_type(t) for t in scala_type.types]
            return IntersectionType(types=[t for t in types if t is not None])
        
        else:
            return BasicType(name="Any")
    
    def _convert_operator(self, operator: str) -> str:
        """Convert Scala operator to Runa operator."""
        operator_mapping = {
            '+': 'plus',
            '-': 'minus',
            '*': 'times',
            '/': 'divided by',
            '%': 'modulo',
            '==': 'is equal to',
            '!=': 'is not equal to',
            '<': 'is less than',
            '>': 'is greater than',
            '<=': 'is less than or equal to',
            '>=': 'is greater than or equal to',
            '&&': 'and',
            '||': 'or',
            '!': 'not',
            '&': 'bitwise and',
            '|': 'bitwise or',
            '^': 'bitwise xor',
            '~': 'bitwise not',
            '<<': 'left shift',
            '>>': 'right shift',
            '>>>': 'unsigned right shift',
        }
        
        return operator_mapping.get(operator, operator)
    
    def _create_placeholder(self, scala_node: ScalaNode) -> Expression:
        """Create placeholder for unconverted nodes."""
        return Identifier(name=f"scala_{type(scala_node).__name__.lower()}")


class RunaToScalaConverter:
    """Converts Runa AST to Scala AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.type_mapping = {
            'Integer': 'Int',
            'Float': 'Double',
            'String': 'String',
            'Boolean': 'Boolean',
            'Character': 'Char',
            'Void': 'Unit',
            'Any': 'Any',
            'Never': 'Nothing',
            'Null': 'Null',
            'List': 'List',
            'Set': 'Set',
            'Dictionary': 'Map',
            'Optional': 'Option',
            'Union': 'Either',
            'Result': 'Try',
            'Future': 'Future',
        }
    
    def convert(self, runa_node: ASTNode) -> ScalaNode:
        """Convert Runa AST node to Scala AST node."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, StructDefinition):
                return self._convert_struct_definition(runa_node)
            elif isinstance(runa_node, ProcessDeclaration):
                return self._convert_process_declaration(runa_node)
            elif isinstance(runa_node, LetStatement):
                return self._convert_let_statement(runa_node)
            elif isinstance(runa_node, VariableDeclaration):
                return self._convert_variable_declaration(runa_node)
            elif isinstance(runa_node, Identifier):
                return self._convert_identifier(runa_node)
            elif isinstance(runa_node, IntegerLiteral):
                return self._convert_integer_literal(runa_node)
            elif isinstance(runa_node, FloatLiteral):
                return self._convert_float_literal(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return self._convert_string_literal(runa_node)
            elif isinstance(runa_node, BooleanLiteral):
                return self._convert_boolean_literal(runa_node)
            elif isinstance(runa_node, NullLiteral):
                return self._convert_null_literal(runa_node)
            elif isinstance(runa_node, IfExpression):
                return self._convert_if_expression(runa_node)
            elif isinstance(runa_node, MatchExpression):
                return self._convert_match_expression(runa_node)
            elif isinstance(runa_node, ForExpression):
                return self._convert_for_expression(runa_node)
            elif isinstance(runa_node, BlockExpression):
                return self._convert_block_expression(runa_node)
            elif isinstance(runa_node, FunctionCall):
                return self._convert_function_call(runa_node)
            elif isinstance(runa_node, MethodCall):
                return self._convert_method_call(runa_node)
            elif isinstance(runa_node, BinaryOperation):
                return self._convert_binary_operation(runa_node)
            elif isinstance(runa_node, UnaryOperation):
                return self._convert_unary_operation(runa_node)
            elif isinstance(runa_node, LambdaExpression):
                return self._convert_lambda_expression(runa_node)
            elif isinstance(runa_node, TupleExpression):
                return self._convert_tuple_expression(runa_node)
            elif isinstance(runa_node, ListExpression):
                return self._convert_list_expression(runa_node)
            elif isinstance(runa_node, Assignment):
                return self._convert_assignment(runa_node)
            else:
                return self._create_scala_placeholder(runa_node)
        except Exception as e:
            self.logger.error(f"Failed to convert Runa node: {e}")
            return self._create_scala_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> ScalaSourceFile:
        """Convert Runa program to Scala source file."""
        package_decl = None
        imports = []
        declarations = []
        
        for stmt in program.statements:
            if isinstance(stmt, PackageStatement):
                package_decl = ScalaPackageDeclaration(name=stmt.name)
            elif isinstance(stmt, ImportStatement):
                imports.append(ScalaImportDeclaration(
                    path=stmt.module_name,
                    selectors=stmt.imported_names if stmt.imported_names != ["*"] else []
                ))
            elif isinstance(stmt, (StructDefinition, ProcessDeclaration)):
                converted = self.convert(stmt)
                if isinstance(converted, ScalaDeclaration):
                    declarations.append(converted)
        
        return ScalaSourceFile(
            package_declaration=package_decl,
            imports=imports,
            declarations=declarations
        )
    
    def _convert_struct_definition(self, struct_def: StructDefinition) -> ScalaDeclaration:
        """Convert Runa struct to Scala class/trait/object."""
        annotations = struct_def.annotations or {}
        scala_type = annotations.get("scala_type", "class")
        
        # Convert fields to constructor parameters or members
        constructor_params = []
        members = []
        
        for field in struct_def.fields:
            param = ScalaParameter(
                name=field.name,
                parameter_type=self._convert_runa_type(field.type_annotation)
            )
            constructor_params.append(param)
            
            # Also add as member if it's a var
            field_annotations = field.annotations or {}
            if field_annotations.get("scala_mutable", False):
                member = ScalaVariableDeclaration(
                    name=field.name,
                    type_annotation=self._convert_runa_type(field.type_annotation)
                )
                members.append(member)
            else:
                member = ScalaValueDeclaration(
                    name=field.name,
                    type_annotation=self._convert_runa_type(field.type_annotation)
                )
                members.append(member)
        
        # Create appropriate declaration type
        if scala_type == "trait":
            return ScalaTraitDeclaration(
                name=struct_def.name,
                members=members,
                is_sealed=annotations.get("scala_sealed", False)
            )
        elif scala_type == "object":
            return ScalaObjectDeclaration(
                name=struct_def.name,
                members=members,
                is_case=annotations.get("scala_case", False)
            )
        else:  # class
            return ScalaClassDeclaration(
                name=struct_def.name,
                constructor_parameters=constructor_params,
                members=members,
                is_abstract=annotations.get("scala_abstract", False),
                is_final=annotations.get("scala_final", False),
                is_sealed=annotations.get("scala_sealed", False),
                is_case=annotations.get("scala_case", False)
            )
    
    def _convert_process_declaration(self, process: ProcessDeclaration) -> ScalaFunctionDeclaration:
        """Convert Runa process to Scala function."""
        parameters = []
        
        for param in process.parameters:
            scala_param = ScalaParameter(
                name=param.name,
                parameter_type=self._convert_runa_type(param.type_annotation)
            )
            parameters.append(scala_param)
        
        # Convert body
        body = None
        if process.body:
            body = self.convert(process.body)
        
        annotations = process.annotations or {}
        
        return ScalaFunctionDeclaration(
            name=process.name,
            parameter_lists=[parameters] if parameters else [],
            return_type=self._convert_runa_type(process.return_type),
            body=body,
            is_abstract=annotations.get("scala_abstract", False),
            is_override=annotations.get("scala_override", False),
            is_implicit=annotations.get("scala_implicit", False),
            is_inline=annotations.get("scala_inline", False)
        )
    
    def _convert_let_statement(self, let_stmt: LetStatement) -> ScalaValueDeclaration:
        """Convert Runa let statement to Scala val."""
        annotations = let_stmt.annotations or {}
        
        return ScalaValueDeclaration(
            name=let_stmt.name,
            type_annotation=self._convert_runa_type(let_stmt.type_annotation),
            value=self.convert(let_stmt.value) if let_stmt.value else None,
            is_lazy=annotations.get("scala_lazy", False),
            is_implicit=annotations.get("scala_implicit", False),
            is_override=annotations.get("scala_override", False)
        )
    
    def _convert_variable_declaration(self, var_decl: VariableDeclaration) -> ScalaVariableDeclaration:
        """Convert Runa variable declaration to Scala var."""
        annotations = var_decl.annotations or {}
        
        return ScalaVariableDeclaration(
            name=var_decl.name,
            type_annotation=self._convert_runa_type(var_decl.type_annotation),
            value=self.convert(var_decl.initial_value) if var_decl.initial_value else None,
            is_override=annotations.get("scala_override", False)
        )
    
    def _convert_identifier(self, identifier: Identifier) -> ScalaIdentifier:
        """Convert Runa identifier to Scala identifier."""
        return ScalaIdentifier(name=identifier.name)
    
    def _convert_integer_literal(self, literal: IntegerLiteral) -> ScalaLiteral:
        """Convert Runa integer literal to Scala literal."""
        return ScalaLiteral(value=literal.value, literal_type="int")
    
    def _convert_float_literal(self, literal: FloatLiteral) -> ScalaLiteral:
        """Convert Runa float literal to Scala literal."""
        return ScalaLiteral(value=literal.value, literal_type="double")
    
    def _convert_string_literal(self, literal: StringLiteral) -> ScalaLiteral:
        """Convert Runa string literal to Scala literal."""
        return ScalaLiteral(value=literal.value, literal_type="string")
    
    def _convert_boolean_literal(self, literal: BooleanLiteral) -> ScalaLiteral:
        """Convert Runa boolean literal to Scala literal."""
        return ScalaLiteral(value=literal.value, literal_type="bool")
    
    def _convert_null_literal(self, literal: NullLiteral) -> ScalaLiteral:
        """Convert Runa null literal to Scala literal."""
        return ScalaLiteral(value=None, literal_type="null")
    
    def _convert_if_expression(self, if_expr: IfExpression) -> ScalaIfExpression:
        """Convert Runa if expression to Scala if expression."""
        return ScalaIfExpression(
            condition=self.convert(if_expr.condition) if if_expr.condition else None,
            then_expression=self.convert(if_expr.then_expression) if if_expr.then_expression else None,
            else_expression=self.convert(if_expr.else_expression) if if_expr.else_expression else None
        )
    
    def _convert_match_expression(self, match_expr: MatchExpression) -> ScalaMatchExpression:
        """Convert Runa match expression to Scala match expression."""
        cases = []
        
        for runa_case in match_expr.cases:
            pattern = self._convert_pattern(runa_case.pattern)
            guard = self.convert(runa_case.guard) if runa_case.guard else None
            body = self.convert(runa_case.body) if runa_case.body else None
            
            case = ScalaMatchCase(
                pattern=pattern,
                guard=guard,
                body=body
            )
            cases.append(case)
        
        return ScalaMatchExpression(
            scrutinee=self.convert(match_expr.scrutinee) if match_expr.scrutinee else None,
            cases=cases
        )
    
    def _convert_for_expression(self, for_expr: ForExpression) -> ScalaForExpression:
        """Convert Runa for expression to Scala for expression."""
        # Create generator
        pattern = self._convert_pattern(for_expr.target) if for_expr.target else ScalaWildcardPattern()
        generator = ScalaGenerator(
            pattern=pattern,
            expression=self.convert(for_expr.iter) if for_expr.iter else None
        )
        
        return ScalaForExpression(
            generators=[generator],
            yield_expression=self.convert(for_expr.body) if for_expr.body else None,
            is_yield=True
        )
    
    def _convert_block_expression(self, block_expr: BlockExpression) -> ScalaBlockExpression:
        """Convert Runa block expression to Scala block expression."""
        statements = []
        
        for stmt in block_expr.statements:
            converted = self.convert(stmt)
            if converted:
                statements.append(converted)
        
        result = None
        if block_expr.result_expression:
            result = self.convert(block_expr.result_expression)
        
        return ScalaBlockExpression(
            statements=statements,
            result_expression=result
        )
    
    def _convert_function_call(self, func_call: FunctionCall) -> ScalaFunctionCallExpression:
        """Convert Runa function call to Scala function call."""
        arguments = []
        for arg in func_call.arguments:
            scala_arg = ScalaArgument(value=self.convert(arg))
            arguments.append(scala_arg)
        
        return ScalaFunctionCallExpression(
            function=self.convert(func_call.function) if func_call.function else None,
            arguments=[arguments] if arguments else []
        )
    
    def _convert_method_call(self, method_call: MethodCall) -> ScalaMethodCallExpression:
        """Convert Runa method call to Scala method call."""
        arguments = []
        for arg in method_call.arguments:
            scala_arg = ScalaArgument(value=self.convert(arg))
            arguments.append(scala_arg)
        
        return ScalaMethodCallExpression(
            receiver=self.convert(method_call.receiver) if method_call.receiver else None,
            method_name=method_call.method_name,
            arguments=[arguments] if arguments else []
        )
    
    def _convert_binary_operation(self, binary_op: BinaryOperation) -> ScalaBinaryExpression:
        """Convert Runa binary operation to Scala binary expression."""
        return ScalaBinaryExpression(
            left=self.convert(binary_op.left) if binary_op.left else None,
            operator=self._convert_operator(binary_op.operator),
            right=self.convert(binary_op.right) if binary_op.right else None
        )
    
    def _convert_unary_operation(self, unary_op: UnaryOperation) -> ScalaUnaryExpression:
        """Convert Runa unary operation to Scala unary expression."""
        return ScalaUnaryExpression(
            operator=self._convert_operator(unary_op.operator),
            operand=self.convert(unary_op.operand) if unary_op.operand else None
        )
    
    def _convert_lambda_expression(self, lambda_expr: LambdaExpression) -> ScalaLambdaExpression:
        """Convert Runa lambda expression to Scala lambda expression."""
        parameters = []
        
        for param in lambda_expr.parameters:
            scala_param = ScalaParameter(
                name=param.name,
                parameter_type=self._convert_runa_type(param.type_annotation)
            )
            parameters.append(scala_param)
        
        return ScalaLambdaExpression(
            parameters=parameters,
            body=self.convert(lambda_expr.body) if lambda_expr.body else None
        )
    
    def _convert_tuple_expression(self, tuple_expr: TupleExpression) -> ScalaTupleExpression:
        """Convert Runa tuple expression to Scala tuple expression."""
        elements = []
        
        for element in tuple_expr.elements:
            converted = self.convert(element)
            if converted:
                elements.append(converted)
        
        return ScalaTupleExpression(elements=elements)
    
    def _convert_list_expression(self, list_expr: ListExpression) -> ScalaListExpression:
        """Convert Runa list expression to Scala list expression."""
        elements = []
        
        for element in list_expr.elements:
            converted = self.convert(element)
            if converted:
                elements.append(converted)
        
        return ScalaListExpression(elements=elements)
    
    def _convert_assignment(self, assignment: Assignment) -> ScalaAssignmentExpression:
        """Convert Runa assignment to Scala assignment expression."""
        return ScalaAssignmentExpression(
            target=self.convert(assignment.target) if assignment.target else None,
            value=self.convert(assignment.value) if assignment.value else None
        )
    
    def _convert_pattern(self, pattern: Pattern) -> ScalaPattern:
        """Convert Runa pattern to Scala pattern."""
        if isinstance(pattern, WildcardPattern):
            return ScalaWildcardPattern()
        elif isinstance(pattern, VariablePattern):
            return ScalaIdentifierPattern(name=pattern.name)
        elif isinstance(pattern, LiteralPattern):
            return ScalaLiteralPattern(literal=self.convert(pattern.value) if pattern.value else None)
        elif isinstance(pattern, ConstructorPattern):
            patterns = [self._convert_pattern(p) for p in pattern.patterns]
            return ScalaConstructorPattern(
                constructor=ScalaIdentifier(name=pattern.constructor),
                patterns=patterns
            )
        elif isinstance(pattern, TuplePattern):
            patterns = [self._convert_pattern(p) for p in pattern.patterns]
            return ScalaTuplePattern(patterns=patterns)
        elif isinstance(pattern, TypedPattern):
            return ScalaTypedPattern(
                pattern=self._convert_pattern(pattern.pattern) if pattern.pattern else None,
                pattern_type=self._convert_runa_type(pattern.type_annotation)
            )
        else:
            return ScalaWildcardPattern()
    
    def _convert_runa_type(self, runa_type: Optional[TypeExpression]) -> Optional[ScalaType]:
        """Convert Runa type to Scala type."""
        if not runa_type:
            return None
        
        if isinstance(runa_type, BasicType):
            scala_type_name = self.type_mapping.get(runa_type.name, runa_type.name)
            return ScalaTypeIdentifier(name=scala_type_name)
        
        elif isinstance(runa_type, GenericType):
            base_name = runa_type.base_type.name if isinstance(runa_type.base_type, BasicType) else "Generic"
            scala_base_name = self.type_mapping.get(base_name, base_name)
            
            type_args = [self._convert_runa_type(arg) for arg in runa_type.type_arguments]
            return ScalaTypeIdentifier(
                name=scala_base_name,
                type_arguments=[arg for arg in type_args if arg is not None]
            )
        
        elif isinstance(runa_type, FunctionType):
            param_types = [self._convert_runa_type(pt) for pt in runa_type.parameter_types]
            return ScalaFunctionType(
                parameter_types=[pt for pt in param_types if pt is not None],
                return_type=self._convert_runa_type(runa_type.return_type)
            )
        
        elif isinstance(runa_type, TupleType):
            element_types = [self._convert_runa_type(et) for et in runa_type.element_types]
            return ScalaTupleType(element_types=[et for et in element_types if et is not None])
        
        elif isinstance(runa_type, UnionType):
            # Convert to Either for binary union, or compound type for multiple
            types = [self._convert_runa_type(t) for t in runa_type.types]
            valid_types = [t for t in types if t is not None]
            
            if len(valid_types) == 2:
                # Binary union -> Either
                return ScalaTypeIdentifier(
                    name="Either",
                    type_arguments=valid_types
                )
            else:
                # Multiple types -> compound type
                return ScalaCompoundType(types=valid_types)
        
        elif isinstance(runa_type, IntersectionType):
            types = [self._convert_runa_type(t) for t in runa_type.types]
            return ScalaCompoundType(types=[t for t in types if t is not None])
        
        else:
            return ScalaTypeIdentifier(name="Any")
    
    def _convert_operator(self, operator: str) -> str:
        """Convert Runa operator to Scala operator."""
        operator_mapping = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'divided by': '/',
            'modulo': '%',
            'is equal to': '==',
            'is not equal to': '!=',
            'is less than': '<',
            'is greater than': '>',
            'is less than or equal to': '<=',
            'is greater than or equal to': '>=',
            'and': '&&',
            'or': '||',
            'not': '!',
            'bitwise and': '&',
            'bitwise or': '|',
            'bitwise xor': '^',
            'bitwise not': '~',
            'left shift': '<<',
            'right shift': '>>',
            'unsigned right shift': '>>>',
        }
        
        return operator_mapping.get(operator, operator)
    
    def _create_scala_placeholder(self, runa_node: ASTNode) -> ScalaExpression:
        """Create Scala placeholder for unconverted nodes."""
        return ScalaIdentifier(name=f"runa_{type(runa_node).__name__.lower()}")


# Convenience functions
def scala_to_runa(scala_ast: ScalaNode) -> ASTNode:
    """Convert Scala AST to Runa AST."""
    converter = ScalaToRunaConverter()
    return converter.convert(scala_ast)


def runa_to_scala(runa_ast: ASTNode) -> ScalaNode:
    """Convert Runa AST to Scala AST."""
    converter = RunaToScalaConverter()
    return converter.convert(runa_ast)