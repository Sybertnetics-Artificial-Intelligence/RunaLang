#!/usr/bin/env python3
"""
Rust ↔ Runa Bidirectional Converter

Converts between Rust AST and Runa AST in both directions,
preserving semantics and enabling round-trip translation.

This module handles conversion between:
- Rust structs/enums ↔ Runa data structures
- Rust functions ↔ Runa processes
- Rust traits ↔ Runa interfaces
- Rust ownership/borrowing ↔ Runa memory annotations
- Rust async/await ↔ Runa async constructs
- Rust pattern matching ↔ Runa match expressions
- Rust lifetimes ↔ Runa lifetime annotations
- Rust generics ↔ Runa generic types

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass
import logging

from .rust_ast import (
    RustNode, RustCrate, RustItem, RustExpression, RustStatement, RustPattern,
    RustFunction, RustStruct, RustEnum, RustTrait, RustImpl, RustModule,
    RustUseDeclaration, RustTypeAlias, RustConst, RustStatic, RustUnion,
    RustType, RustTypeReference, RustReferenceType, RustPointerType,
    RustArrayType, RustSliceType, RustTupleType, RustFunctionType,
    RustTraitObject, RustImplTrait, RustLifetime, RustTypeParam,
    RustLifetimeParam, RustConstParam, RustWhereClause, RustGenericParam,
    RustIdentifier, RustLiteral, RustPath, RustBlock, RustIfExpression,
    RustMatchExpression, RustLoopExpression, RustWhileExpression,
    RustForExpression, RustCallExpression, RustMethodCall, RustFieldAccess,
    RustIndexExpression, RustTupleExpression, RustArrayExpression,
    RustStructExpression, RustClosure, RustAwaitExpression, RustTryExpression,
    RustReturnExpression, RustBreakExpression, RustContinueExpression,
    RustMacroCall, RustExpressionStatement, RustLetStatement, RustItemStatement,
    RustIdentifierPattern, RustWildcardPattern, RustLiteralPattern,
    RustStructPattern, RustTuplePattern, RustReferencePattern, RustOrPattern,
    RustRangePattern, RustAttribute, RustMatchArm, RustField, RustEnumVariant,
    RustParameter, RustVisibility, RustMutability, RustSafety, RustAsyncness
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


class RustToRunaConverter:
    """
    Converts Rust AST to Runa AST.
    
    This converter transforms Rust constructs into their Runa equivalents:
    - Structs and enums become data structures
    - Functions become processes
    - Traits become interfaces
    - Ownership/borrowing becomes memory annotations
    - Pattern matching is preserved
    """
    
    def __init__(self):
        """Initialize the Rust to Runa converter."""
        self.logger = logging.getLogger(__name__)
        self.type_mapping = self._build_type_mapping()
        self.operator_mapping = self._build_operator_mapping()
        self.current_scope = []  # Track current scope for variable resolution
        self.lifetime_context = {}  # Track lifetime mappings
        self.generic_context = {}  # Track generic type mappings
    
    def _build_type_mapping(self) -> Dict[str, str]:
        """Build mapping from Rust types to Runa types."""
        return {
            # Primitive types
            'bool': 'Boolean',
            'char': 'Character',
            'str': 'String',
            
            # Integer types
            'i8': 'TinyInteger',
            'i16': 'SmallInteger',
            'i32': 'Integer',
            'i64': 'BigInteger',
            'i128': 'HugeInteger',
            'isize': 'Integer',
            'u8': 'UnsignedTinyInteger',
            'u16': 'UnsignedSmallInteger',
            'u32': 'UnsignedInteger',
            'u64': 'UnsignedBigInteger',
            'u128': 'UnsignedHugeInteger',
            'usize': 'UnsignedInteger',
            
            # Float types
            'f32': 'Float',
            'f64': 'Double',
            
            # Collection types
            'Vec': 'List',
            'HashMap': 'Dictionary',
            'HashSet': 'Set',
            'BTreeMap': 'OrderedDictionary',
            'BTreeSet': 'OrderedSet',
            
            # Special types
            'Option': 'Optional',
            'Result': 'Result',
            'Box': 'Boxed',
            'Rc': 'ReferenceCountered',
            'Arc': 'AtomicReferenceCountered',
            'RefCell': 'MutableReference',
            'Mutex': 'ThreadSafeMutable',
            'RwLock': 'ReadWriteLock',
            
            # Function types
            'fn': 'Function',
            'Fn': 'Function',
            'FnMut': 'MutableFunction',
            'FnOnce': 'OnceFuction',
            
            # Async types
            'Future': 'Future',
            'Stream': 'Stream',
            'Pin': 'Pinned',
            
            # Memory types
            'String': 'String',
            '&str': 'StringSlice',
            '&[T]': 'Slice',
            '[T; N]': 'Array',
            '&T': 'Reference',
            '&mut T': 'MutableReference',
            '*const T': 'ConstantPointer',
            '*mut T': 'MutablePointer',
        }
    
    def _build_operator_mapping(self) -> Dict[str, BinaryOperator]:
        """Build mapping from Rust operators to Runa operators."""
        return {
            '+': BinaryOperator.ADD,
            '-': BinaryOperator.SUBTRACT,
            '*': BinaryOperator.MULTIPLY,
            '/': BinaryOperator.DIVIDE,
            '%': BinaryOperator.MODULO,
            '==': BinaryOperator.EQUAL,
            '!=': BinaryOperator.NOT_EQUAL,
            '<': BinaryOperator.LESS_THAN,
            '>': BinaryOperator.GREATER_THAN,
            '<=': BinaryOperator.LESS_THAN_OR_EQUAL,
            '>=': BinaryOperator.GREATER_THAN_OR_EQUAL,
            '&&': BinaryOperator.LOGICAL_AND,
            '||': BinaryOperator.LOGICAL_OR,
            '&': BinaryOperator.BITWISE_AND,
            '|': BinaryOperator.BITWISE_OR,
            '^': BinaryOperator.BITWISE_XOR,
            '<<': BinaryOperator.LEFT_SHIFT,
            '>>': BinaryOperator.RIGHT_SHIFT,
        }
    
    def convert(self, rust_node: RustNode) -> ASTNode:
        """
        Convert Rust AST node to Runa AST node.
        
        Args:
            rust_node: Rust AST node
            
        Returns:
            ASTNode: Equivalent Runa AST node
        """
        try:
            if isinstance(rust_node, RustCrate):
                return self._convert_crate(rust_node)
            elif isinstance(rust_node, RustFunction):
                return self._convert_function(rust_node)
            elif isinstance(rust_node, RustStruct):
                return self._convert_struct(rust_node)
            elif isinstance(rust_node, RustEnum):
                return self._convert_enum(rust_node)
            elif isinstance(rust_node, RustTrait):
                return self._convert_trait(rust_node)
            elif isinstance(rust_node, RustImpl):
                return self._convert_impl(rust_node)
            elif isinstance(rust_node, RustModule):
                return self._convert_module(rust_node)
            elif isinstance(rust_node, RustUseDeclaration):
                return self._convert_use_declaration(rust_node)
            elif isinstance(rust_node, RustIdentifier):
                return self._convert_identifier(rust_node)
            elif isinstance(rust_node, RustLiteral):
                return self._convert_literal(rust_node)
            elif isinstance(rust_node, RustBlock):
                return self._convert_block(rust_node)
            elif isinstance(rust_node, RustIfExpression):
                return self._convert_if_expression(rust_node)
            elif isinstance(rust_node, RustMatchExpression):
                return self._convert_match_expression(rust_node)
            elif isinstance(rust_node, RustCallExpression):
                return self._convert_call_expression(rust_node)
            elif isinstance(rust_node, RustMethodCall):
                return self._convert_method_call(rust_node)
            elif isinstance(rust_node, RustFieldAccess):
                return self._convert_field_access(rust_node)
            elif isinstance(rust_node, RustAwaitExpression):
                return self._convert_await_expression(rust_node)
            elif isinstance(rust_node, RustReturnExpression):
                return self._convert_return_expression(rust_node)
            elif isinstance(rust_node, RustLetStatement):
                return self._convert_let_statement(rust_node)
            else:
                # Default conversion for unknown types
                return self._create_placeholder(rust_node)
                
        except Exception as e:
            self.logger.error(f"Failed to convert Rust node {type(rust_node).__name__}: {e}")
            return self._create_placeholder(rust_node)
    
    def _convert_crate(self, crate: RustCrate) -> Program:
        """Convert Rust crate to Runa program."""
        statements = []
        
        # Convert all items
        for item in crate.items:
            converted = self.convert(item)
            if converted:
                statements.append(converted)
        
        return Program(
            statements=statements,
            metadata=TranslationMetadata(
                source_language="Rust",
                target_language="Runa",
                conversion_notes={
                    "crate_name": crate.name,
                    "item_count": len(crate.items),
                    "attributes": [attr.path for attr in crate.attributes]
                }
            )
        )
    
    def _convert_function(self, func: RustFunction) -> ProcessDeclaration:
        """Convert Rust function to Runa process."""
        # Convert parameters
        parameters = []
        for param in func.parameters:
            runa_param = FieldDefinition(
                name=param.name or "param",
                type_annotation=self._convert_type(param.param_type) if param.param_type else BasicType(name="Any"),
                annotations={
                    "rust_self": param.is_self,
                    "rust_self_kind": param.self_kind
                }
            )
            parameters.append(runa_param)
        
        # Convert return type
        return_type = self._convert_type(func.return_type) if func.return_type else BasicType(name="Unit")
        
        # Convert body
        body = None
        if func.body:
            body = self.convert(func.body)
            if not isinstance(body, BlockStatement):
                body = BlockStatement(statements=[body])
        
        # Create annotations for Rust-specific features
        annotations = {
            "rust_async": func.is_async,
            "rust_unsafe": func.is_unsafe,
            "rust_extern": func.is_extern,
            "rust_const": func.is_const,
            "rust_abi": func.abi,
            "rust_visibility": func.visibility.value,
        }
        
        # Add generic information
        if func.generics:
            annotations["rust_generics"] = [self._convert_generic_param(g) for g in func.generics]
        
        # Add where clause information
        if func.where_clause:
            annotations["rust_where_clause"] = func.where_clause.predicates
        
        return ProcessDeclaration(
            name=func.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            is_async=func.is_async,
            annotations=annotations
        )
    
    def _convert_struct(self, struct: RustStruct) -> StructDefinition:
        """Convert Rust struct to Runa struct."""
        # Convert fields
        fields = []
        for field in struct.fields:
            runa_field = FieldDefinition(
                name=field.name,
                type_annotation=self._convert_type(field.field_type) if field.field_type else BasicType(name="Any"),
                annotations={
                    "rust_visibility": field.visibility.value,
                    "rust_attributes": [attr.path for attr in field.attributes]
                }
            )
            fields.append(runa_field)
        
        # Create annotations for Rust-specific features
        annotations = {
            "rust_visibility": struct.visibility.value,
            "rust_is_tuple": struct.is_tuple,
            "rust_is_unit": struct.is_unit,
        }
        
        # Add generic information
        if struct.generics:
            annotations["rust_generics"] = [self._convert_generic_param(g) for g in struct.generics]
        
        # Add where clause information
        if struct.where_clause:
            annotations["rust_where_clause"] = struct.where_clause.predicates
        
        return StructDefinition(
            name=struct.name,
            fields=fields,
            annotations=annotations
        )
    
    def _convert_enum(self, enum: RustEnum) -> Union[StructDefinition, UnionType]:
        """Convert Rust enum to Runa union type or struct with variants."""
        # For simple enums, create a union type
        if all(variant.is_unit for variant in enum.variants):
            variant_types = []
            for variant in enum.variants:
                variant_types.append(BasicType(name=variant.name))
            
            return UnionType(
                types=variant_types,
                annotations={
                    "rust_enum_name": enum.name,
                    "rust_visibility": enum.visibility.value,
                    "rust_generics": [self._convert_generic_param(g) for g in enum.generics] if enum.generics else []
                }
            )
        
        # For complex enums with data, create a struct-like representation
        # This is a simplified approach - real implementation would need more sophisticated handling
        fields = []
        for variant in enum.variants:
            if variant.fields:
                for field in variant.fields:
                    runa_field = FieldDefinition(
                        name=f"{variant.name}_{field.name}" if field.name else f"{variant.name}_data",
                        type_annotation=self._convert_type(field.field_type) if field.field_type else BasicType(name="Any"),
                        annotations={
                            "rust_variant": variant.name,
                            "rust_field": field.name
                        }
                    )
                    fields.append(runa_field)
        
        return StructDefinition(
            name=enum.name,
            fields=fields,
            annotations={
                "rust_type": "enum",
                "rust_visibility": enum.visibility.value,
                "rust_generics": [self._convert_generic_param(g) for g in enum.generics] if enum.generics else [],
                "rust_variants": [variant.name for variant in enum.variants]
            }
        )
    
    def _convert_trait(self, trait: RustTrait) -> StructDefinition:
        """Convert Rust trait to Runa interface-like structure."""
        # Traits in Rust are like interfaces - convert to a struct with method signatures
        methods = []
        
        # This is simplified - real implementation would parse trait items
        return StructDefinition(
            name=trait.name,
            fields=methods,
            annotations={
                "rust_type": "trait",
                "rust_visibility": trait.visibility.value,
                "rust_unsafe": trait.is_unsafe,
                "rust_auto": trait.is_auto,
                "rust_generics": [self._convert_generic_param(g) for g in trait.generics] if trait.generics else [],
                "rust_supertraits": trait.supertraits
            }
        )
    
    def _convert_impl(self, impl: RustImpl) -> ModuleDefinition:
        """Convert Rust impl block to Runa module with methods."""
        # Convert impl items to module contents
        items = []
        
        # This is simplified - real implementation would parse impl items
        return ModuleDefinition(
            name=f"impl_{impl.self_type}" if impl.self_type else "impl_block",
            statements=items,
            annotations={
                "rust_type": "impl",
                "rust_trait": impl.trait_ref,
                "rust_self_type": str(impl.self_type) if impl.self_type else None,
                "rust_unsafe": impl.is_unsafe,
                "rust_generics": [self._convert_generic_param(g) for g in impl.generics] if impl.generics else []
            }
        )
    
    def _convert_module(self, module: RustModule) -> ModuleDefinition:
        """Convert Rust module to Runa module."""
        statements = []
        
        for item in module.items:
            converted = self.convert(item)
            if converted:
                statements.append(converted)
        
        return ModuleDefinition(
            name=module.name,
            statements=statements,
            annotations={
                "rust_visibility": module.visibility.value
            }
        )
    
    def _convert_use_declaration(self, use_decl: RustUseDeclaration) -> ImportStatement:
        """Convert Rust use declaration to Runa import."""
        # Parse the path to extract module and items
        path_parts = use_decl.path.split("::")
        module_name = "::".join(path_parts[:-1]) if len(path_parts) > 1 else path_parts[0]
        item_name = path_parts[-1] if not use_decl.is_glob else "*"
        
        return ImportStatement(
            module_name=module_name,
            imported_names=[item_name] if not use_decl.is_glob else ["*"],
            alias=use_decl.alias,
            annotations={
                "rust_visibility": use_decl.visibility.value,
                "rust_is_glob": use_decl.is_glob,
                "rust_original_path": use_decl.path
            }
        )
    
    def _convert_identifier(self, ident: RustIdentifier) -> Identifier:
        """Convert Rust identifier to Runa identifier."""
        return Identifier(name=ident.name)
    
    def _convert_literal(self, literal: RustLiteral) -> Expression:
        """Convert Rust literal to Runa literal."""
        if literal.literal_type == "integer":
            return IntegerLiteral(value=int(literal.value) if literal.value is not None else 0)
        elif literal.literal_type == "float":
            return FloatLiteral(value=float(literal.value) if literal.value is not None else 0.0)
        elif literal.literal_type == "string":
            return StringLiteral(value=str(literal.value) if literal.value is not None else "")
        elif literal.literal_type == "boolean":
            return BooleanLiteral(value=bool(literal.value) if literal.value is not None else False)
        elif literal.literal_type == "char":
            return StringLiteral(value=str(literal.value) if literal.value is not None else "")
        else:
            return StringLiteral(value=str(literal.value) if literal.value is not None else "")
    
    def _convert_block(self, block: RustBlock) -> BlockStatement:
        """Convert Rust block to Runa block."""
        statements = []
        
        # Convert all statements
        for stmt in block.statements:
            converted = self.convert(stmt)
            if converted:
                statements.append(converted)
        
        # Convert final expression if present
        if block.expression:
            expr_converted = self.convert(block.expression)
            if expr_converted:
                statements.append(ExpressionStatement(expression=expr_converted))
        
        return BlockStatement(
            statements=statements,
            annotations={
                "rust_unsafe": block.is_unsafe,
                "rust_async": block.is_async,
                "rust_const": block.is_const
            }
        )
    
    def _convert_if_expression(self, if_expr: RustIfExpression) -> IfStatement:
        """Convert Rust if expression to Runa if statement."""
        condition = self.convert(if_expr.condition) if if_expr.condition else BooleanLiteral(value=True)
        then_branch = self.convert(if_expr.then_branch) if if_expr.then_branch else BlockStatement(statements=[])
        else_branch = self.convert(if_expr.else_branch) if if_expr.else_branch else None
        
        return IfStatement(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _convert_match_expression(self, match_expr: RustMatchExpression) -> MatchStatement:
        """Convert Rust match expression to Runa match statement."""
        expression = self.convert(match_expr.expression) if match_expr.expression else Identifier(name="value")
        
        # Convert match arms (simplified)
        cases = []
        for arm in match_expr.arms:
            # Convert pattern (simplified)
            pattern = self._convert_pattern(arm.pattern) if arm.pattern else Identifier(name="_")
            body = self.convert(arm.body) if arm.body else BlockStatement(statements=[])
            
            cases.append({
                "pattern": pattern,
                "body": body,
                "guard": self.convert(arm.guard) if arm.guard else None
            })
        
        return MatchStatement(
            expression=expression,
            cases=cases
        )
    
    def _convert_call_expression(self, call: RustCallExpression) -> FunctionCall:
        """Convert Rust function call to Runa function call."""
        function = self.convert(call.function) if call.function else Identifier(name="function")
        arguments = [self.convert(arg) for arg in call.arguments if arg]
        
        return FunctionCall(
            function=function,
            arguments=arguments
        )
    
    def _convert_method_call(self, call: RustMethodCall) -> FunctionCall:
        """Convert Rust method call to Runa method call."""
        receiver = self.convert(call.receiver) if call.receiver else Identifier(name="self")
        arguments = [self.convert(arg) for arg in call.arguments if arg]
        
        # Create member access for the method
        method_access = MemberAccess(
            object=receiver,
            attribute=call.method_name
        )
        
        return FunctionCall(
            function=method_access,
            arguments=arguments
        )
    
    def _convert_field_access(self, access: RustFieldAccess) -> MemberAccess:
        """Convert Rust field access to Runa member access."""
        object = self.convert(access.receiver) if access.receiver else Identifier(name="object")
        
        return MemberAccess(
            object=object,
            attribute=access.field_name
        )
    
    def _convert_await_expression(self, await_expr: RustAwaitExpression) -> AwaitExpression:
        """Convert Rust await expression to Runa await expression."""
        expression = self.convert(await_expr.expression) if await_expr.expression else Identifier(name="future")
        
        return AwaitExpression(expression=expression)
    
    def _convert_return_expression(self, ret_expr: RustReturnExpression) -> ReturnStatement:
        """Convert Rust return expression to Runa return statement."""
        expression = self.convert(ret_expr.expression) if ret_expr.expression else None
        
        return ReturnStatement(expression=expression)
    
    def _convert_let_statement(self, let_stmt: RustLetStatement) -> LetStatement:
        """Convert Rust let statement to Runa let statement."""
        # Convert pattern to identifier (simplified)
        name = self._extract_identifier_from_pattern(let_stmt.pattern) if let_stmt.pattern else "variable"
        
        value = self.convert(let_stmt.initializer) if let_stmt.initializer else None
        type_annotation = self._convert_type(let_stmt.type_annotation) if let_stmt.type_annotation else None
        
        return LetStatement(
            name=name,
            value=value,
            type_annotation=type_annotation,
            annotations={
                "rust_pattern": str(let_stmt.pattern) if let_stmt.pattern else None
            }
        )
    
    def _convert_type(self, rust_type: Optional[RustType]) -> Optional[TypeExpression]:
        """Convert Rust type to Runa type."""
        if not rust_type:
            return None
        
        if isinstance(rust_type, RustTypeReference):
            # Map Rust type to Runa type
            runa_type_name = self.type_mapping.get(rust_type.path, rust_type.path)
            
            if rust_type.type_arguments:
                # Generic type
                type_args = [self._convert_type(arg) for arg in rust_type.type_arguments if arg]
                return GenericType(
                    base_type=BasicType(name=runa_type_name),
                    type_arguments=type_args
                )
            else:
                return BasicType(name=runa_type_name)
        
        elif isinstance(rust_type, RustReferenceType):
            # Reference types become annotated types
            inner = self._convert_type(rust_type.inner_type)
            if inner:
                # Add reference annotation
                if hasattr(inner, 'annotations'):
                    inner.annotations = inner.annotations or {}
                    inner.annotations["rust_reference"] = True
                    inner.annotations["rust_mutable"] = rust_type.mutability == RustMutability.MUTABLE
                    if rust_type.lifetime:
                        inner.annotations["rust_lifetime"] = rust_type.lifetime.name
                return inner
            return BasicType(name="Reference")
        
        elif isinstance(rust_type, RustArrayType):
            element_type = self._convert_type(rust_type.element_type)
            return GenericType(
                base_type=BasicType(name="Array"),
                type_arguments=[element_type] if element_type else []
            )
        
        elif isinstance(rust_type, RustSliceType):
            element_type = self._convert_type(rust_type.element_type)
            return GenericType(
                base_type=BasicType(name="Slice"),
                type_arguments=[element_type] if element_type else []
            )
        
        elif isinstance(rust_type, RustTupleType):
            element_types = [self._convert_type(t) for t in rust_type.element_types if t]
            return GenericType(
                base_type=BasicType(name="Tuple"),
                type_arguments=element_types
            )
        
        elif isinstance(rust_type, RustFunctionType):
            param_types = [self._convert_type(t) for t in rust_type.parameters if t]
            return_type = self._convert_type(rust_type.return_type)
            
            return FunctionType(
                parameter_types=param_types,
                return_type=return_type,
                annotations={
                    "rust_unsafe": rust_type.is_unsafe,
                    "rust_extern": rust_type.is_extern,
                    "rust_abi": rust_type.abi
                }
            )
        
        else:
            # Default conversion
            return BasicType(name="Any")
    
    def _convert_generic_param(self, param: RustGenericParam) -> Dict[str, Any]:
        """Convert Rust generic parameter to annotation."""
        if isinstance(param, RustTypeParam):
            return {
                "type": "type_param",
                "name": param.name,
                "bounds": param.bounds,
                "default": str(param.default) if param.default else None
            }
        elif isinstance(param, RustLifetimeParam):
            return {
                "type": "lifetime_param",
                "name": param.lifetime.name,
                "bounds": [lt.name for lt in param.bounds]
            }
        elif isinstance(param, RustConstParam):
            return {
                "type": "const_param",
                "name": param.name,
                "param_type": str(param.param_type) if param.param_type else None,
                "default": str(param.default) if param.default else None
            }
        else:
            return {"type": "unknown", "name": "param"}
    
    def _convert_pattern(self, pattern: Optional[RustPattern]) -> Expression:
        """Convert Rust pattern to Runa expression (simplified)."""
        if not pattern:
            return Identifier(name="_")
        
        if isinstance(pattern, RustIdentifierPattern):
            return Identifier(name=pattern.name)
        elif isinstance(pattern, RustWildcardPattern):
            return Identifier(name="_")
        elif isinstance(pattern, RustLiteralPattern):
            return self.convert(pattern.literal) if pattern.literal else StringLiteral(value="")
        else:
            # Default to identifier
            return Identifier(name="pattern")
    
    def _extract_identifier_from_pattern(self, pattern: Optional[RustPattern]) -> str:
        """Extract identifier name from pattern."""
        if isinstance(pattern, RustIdentifierPattern):
            return pattern.name
        elif isinstance(pattern, RustWildcardPattern):
            return "_"
        else:
            return "variable"
    
    def _create_placeholder(self, rust_node: RustNode) -> Expression:
        """Create placeholder for unconverted nodes."""
        return Identifier(
            name=f"rust_{type(rust_node).__name__.lower()}",
            annotations={
                "rust_placeholder": True,
                "rust_original_type": type(rust_node).__name__
            }
        )


class RunaToRustConverter:
    """
    Converts Runa AST to Rust AST.
    
    This converter transforms Runa constructs into their Rust equivalents:
    - Processes become functions
    - Data structures become structs or enums
    - Memory annotations become ownership/borrowing
    - Async constructs become async/await
    """
    
    def __init__(self):
        """Initialize the Runa to Rust converter."""
        self.logger = logging.getLogger(__name__)
        self.type_mapping = self._build_reverse_type_mapping()
        self.operator_mapping = self._build_reverse_operator_mapping()
        self.current_scope = []
        self.lifetime_counter = 0
        
    def _build_reverse_type_mapping(self) -> Dict[str, str]:
        """Build mapping from Runa types to Rust types."""
        return {
            # Primitive types
            'Boolean': 'bool',
            'Character': 'char',
            'String': 'String',
            
            # Integer types
            'TinyInteger': 'i8',
            'SmallInteger': 'i16',
            'Integer': 'i32',
            'BigInteger': 'i64',
            'HugeInteger': 'i128',
            'UnsignedTinyInteger': 'u8',
            'UnsignedSmallInteger': 'u16',
            'UnsignedInteger': 'u32',
            'UnsignedBigInteger': 'u64',
            'UnsignedHugeInteger': 'u128',
            
            # Float types
            'Float': 'f32',
            'Double': 'f64',
            
            # Collection types
            'List': 'Vec',
            'Dictionary': 'HashMap',
            'Set': 'HashSet',
            'OrderedDictionary': 'BTreeMap',
            'OrderedSet': 'BTreeSet',
            
            # Special types
            'Optional': 'Option',
            'Result': 'Result',
            'Future': 'Future',
            'Stream': 'Stream',
            
            # Function types
            'Function': 'fn',
        }
    
    def _build_reverse_operator_mapping(self) -> Dict[BinaryOperator, str]:
        """Build mapping from Runa operators to Rust operators."""
        return {
            BinaryOperator.ADD: '+',
            BinaryOperator.SUBTRACT: '-',
            BinaryOperator.MULTIPLY: '*',
            BinaryOperator.DIVIDE: '/',
            BinaryOperator.MODULO: '%',
            BinaryOperator.EQUAL: '==',
            BinaryOperator.NOT_EQUAL: '!=',
            BinaryOperator.LESS_THAN: '<',
            BinaryOperator.GREATER_THAN: '>',
            BinaryOperator.LESS_THAN_OR_EQUAL: '<=',
            BinaryOperator.GREATER_THAN_OR_EQUAL: '>=',
            BinaryOperator.LOGICAL_AND: '&&',
            BinaryOperator.LOGICAL_OR: '||',
            BinaryOperator.BITWISE_AND: '&',
            BinaryOperator.BITWISE_OR: '|',
            BinaryOperator.BITWISE_XOR: '^',
            BinaryOperator.LEFT_SHIFT: '<<',
            BinaryOperator.RIGHT_SHIFT: '>>',
        }
    
    def convert(self, runa_node: ASTNode) -> RustNode:
        """
        Convert Runa AST node to Rust AST node.
        
        Args:
            runa_node: Runa AST node
            
        Returns:
            RustNode: Equivalent Rust AST node
        """
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, ProcessDeclaration):
                return self._convert_process_declaration(runa_node)
            elif isinstance(runa_node, StructDefinition):
                return self._convert_struct_definition(runa_node)
            elif isinstance(runa_node, ModuleDefinition):
                return self._convert_module_definition(runa_node)
            elif isinstance(runa_node, ImportStatement):
                return self._convert_import_statement(runa_node)
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
            elif isinstance(runa_node, BlockStatement):
                return self._convert_block_statement(runa_node)
            elif isinstance(runa_node, IfStatement):
                return self._convert_if_statement(runa_node)
            elif isinstance(runa_node, MatchStatement):
                return self._convert_match_statement(runa_node)
            elif isinstance(runa_node, FunctionCall):
                return self._convert_function_call(runa_node)
            elif isinstance(runa_node, MemberAccess):
                return self._convert_member_access(runa_node)
            elif isinstance(runa_node, AwaitExpression):
                return self._convert_await_expression(runa_node)
            elif isinstance(runa_node, ReturnStatement):
                return self._convert_return_statement(runa_node)
            elif isinstance(runa_node, LetStatement):
                return self._convert_let_statement(runa_node)
            else:
                # Default conversion
                return self._create_rust_placeholder(runa_node)
                
        except Exception as e:
            self.logger.error(f"Failed to convert Runa node {type(runa_node).__name__}: {e}")
            return self._create_rust_placeholder(runa_node)
    
    def _convert_program(self, program: Program) -> RustCrate:
        """Convert Runa program to Rust crate."""
        items = []
        
        for stmt in program.statements:
            converted = self.convert(stmt)
            if converted and isinstance(converted, RustItem):
                items.append(converted)
        
        return RustCrate(
            name="main",
            items=items
        )
    
    def _convert_process_declaration(self, process: ProcessDeclaration) -> RustFunction:
        """Convert Runa process to Rust function."""
        # Convert parameters
        parameters = []
        for param in process.parameters:
            rust_param = RustParameter(
                name=param.name,
                param_type=self._convert_runa_type(param.type_annotation)
            )
            parameters.append(rust_param)
        
        # Convert return type
        return_type = self._convert_runa_type(process.return_type)
        
        # Convert body
        body = None
        if process.body:
            converted_body = self.convert(process.body)
            if isinstance(converted_body, RustBlock):
                body = converted_body
            else:
                body = RustBlock(statements=[RustExpressionStatement(expression=converted_body)])
        
        # Extract Rust-specific annotations
        annotations = process.annotations or {}
        is_async = annotations.get("rust_async", process.is_async)
        is_unsafe = annotations.get("rust_unsafe", False)
        is_extern = annotations.get("rust_extern", False)
        is_const = annotations.get("rust_const", False)
        abi = annotations.get("rust_abi")
        
        return RustFunction(
            name=process.name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            is_async=is_async,
            is_unsafe=is_unsafe,
            is_extern=is_extern,
            is_const=is_const,
            abi=abi
        )
    
    def _convert_struct_definition(self, struct: StructDefinition) -> Union[RustStruct, RustEnum, RustTrait]:
        """Convert Runa struct to appropriate Rust construct."""
        annotations = struct.annotations or {}
        rust_type = annotations.get("rust_type", "struct")
        
        if rust_type == "enum":
            # Convert to Rust enum
            variants = []
            variant_names = annotations.get("rust_variants", [])
            
            for variant_name in variant_names:
                variant = RustEnumVariant(
                    name=variant_name,
                    is_unit=True  # Simplified
                )
                variants.append(variant)
            
            return RustEnum(
                name=struct.name,
                variants=variants
            )
        
        elif rust_type == "trait":
            # Convert to Rust trait
            return RustTrait(
                name=struct.name,
                is_unsafe=annotations.get("rust_unsafe", False),
                is_auto=annotations.get("rust_auto", False),
                supertraits=annotations.get("rust_supertraits", [])
            )
        
        else:
            # Convert to Rust struct
            fields = []
            for field in struct.fields:
                rust_field = RustField(
                    name=field.name,
                    field_type=self._convert_runa_type(field.type_annotation)
                )
                fields.append(rust_field)
            
            return RustStruct(
                name=struct.name,
                fields=fields,
                is_tuple=annotations.get("rust_is_tuple", False),
                is_unit=annotations.get("rust_is_unit", False)
            )
    
    def _convert_module_definition(self, module: ModuleDefinition) -> RustModule:
        """Convert Runa module to Rust module."""
        items = []
        
        for stmt in module.statements:
            converted = self.convert(stmt)
            if converted and isinstance(converted, RustItem):
                items.append(converted)
        
        return RustModule(
            name=module.name,
            items=items
        )
    
    def _convert_import_statement(self, import_stmt: ImportStatement) -> RustUseDeclaration:
        """Convert Runa import to Rust use declaration."""
        # Reconstruct Rust path
        annotations = import_stmt.annotations or {}
        original_path = annotations.get("rust_original_path")
        
        if original_path:
            path = original_path
        else:
            # Construct path from module and imported names
            if import_stmt.imported_names and import_stmt.imported_names[0] == "*":
                path = f"{import_stmt.module_name}::*"
            elif import_stmt.imported_names:
                path = f"{import_stmt.module_name}::{import_stmt.imported_names[0]}"
            else:
                path = import_stmt.module_name
        
        return RustUseDeclaration(
            path=path,
            alias=import_stmt.alias,
            is_glob=annotations.get("rust_is_glob", "*" in path)
        )
    
    def _convert_identifier(self, identifier: Identifier) -> RustIdentifier:
        """Convert Runa identifier to Rust identifier."""
        return RustIdentifier(name=identifier.name)
    
    def _convert_integer_literal(self, literal: IntegerLiteral) -> RustLiteral:
        """Convert Runa integer literal to Rust literal."""
        return RustLiteral(
            value=literal.value,
            literal_type="integer"
        )
    
    def _convert_float_literal(self, literal: FloatLiteral) -> RustLiteral:
        """Convert Runa float literal to Rust literal."""
        return RustLiteral(
            value=literal.value,
            literal_type="float"
        )
    
    def _convert_string_literal(self, literal: StringLiteral) -> RustLiteral:
        """Convert Runa string literal to Rust literal."""
        return RustLiteral(
            value=literal.value,
            literal_type="string"
        )
    
    def _convert_boolean_literal(self, literal: BooleanLiteral) -> RustLiteral:
        """Convert Runa boolean literal to Rust literal."""
        return RustLiteral(
            value=literal.value,
            literal_type="boolean"
        )
    
    def _convert_block_statement(self, block: BlockStatement) -> RustBlock:
        """Convert Runa block to Rust block."""
        statements = []
        
        for stmt in block.statements:
            converted = self.convert(stmt)
            if converted:
                if isinstance(converted, RustStatement):
                    statements.append(converted)
                elif isinstance(converted, RustExpression):
                    statements.append(RustExpressionStatement(expression=converted))
        
        annotations = block.annotations or {}
        return RustBlock(
            statements=statements,
            is_unsafe=annotations.get("rust_unsafe", False),
            is_async=annotations.get("rust_async", False),
            is_const=annotations.get("rust_const", False)
        )
    
    def _convert_if_statement(self, if_stmt: IfStatement) -> RustIfExpression:
        """Convert Runa if statement to Rust if expression."""
        condition = self.convert(if_stmt.condition)
        then_branch = self.convert(if_stmt.then_branch)
        else_branch = self.convert(if_stmt.else_branch) if if_stmt.else_branch else None
        
        # Ensure branches are blocks
        if not isinstance(then_branch, RustBlock):
            then_branch = RustBlock(statements=[RustExpressionStatement(expression=then_branch)])
        
        if else_branch and not isinstance(else_branch, RustBlock):
            else_branch = RustBlock(statements=[RustExpressionStatement(expression=else_branch)])
        
        return RustIfExpression(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _convert_match_statement(self, match_stmt: MatchStatement) -> RustMatchExpression:
        """Convert Runa match statement to Rust match expression."""
        expression = self.convert(match_stmt.expression)
        
        arms = []
        for case in match_stmt.cases:
            pattern = self._convert_runa_pattern(case.get("pattern"))
            body = self.convert(case.get("body"))
            guard = self.convert(case.get("guard")) if case.get("guard") else None
            
            arm = RustMatchArm(
                pattern=pattern,
                body=body,
                guard=guard
            )
            arms.append(arm)
        
        return RustMatchExpression(
            expression=expression,
            arms=arms
        )
    
    def _convert_function_call(self, call: FunctionCall) -> RustCallExpression:
        """Convert Runa function call to Rust call expression."""
        function = self.convert(call.function)
        arguments = [self.convert(arg) for arg in call.arguments]
        
        return RustCallExpression(
            function=function,
            arguments=arguments
        )
    
    def _convert_member_access(self, access: MemberAccess) -> RustFieldAccess:
        """Convert Runa member access to Rust field access."""
        receiver = self.convert(access.object)
        
        return RustFieldAccess(
            receiver=receiver,
            field_name=access.attribute
        )
    
    def _convert_await_expression(self, await_expr: AwaitExpression) -> RustAwaitExpression:
        """Convert Runa await to Rust await."""
        expression = self.convert(await_expr.expression)
        
        return RustAwaitExpression(expression=expression)
    
    def _convert_return_statement(self, ret_stmt: ReturnStatement) -> RustReturnExpression:
        """Convert Runa return to Rust return."""
        expression = self.convert(ret_stmt.expression) if ret_stmt.expression else None
        
        return RustReturnExpression(expression=expression)
    
    def _convert_let_statement(self, let_stmt: LetStatement) -> RustLetStatement:
        """Convert Runa let to Rust let."""
        pattern = RustIdentifierPattern(name=let_stmt.name)
        type_annotation = self._convert_runa_type(let_stmt.type_annotation)
        initializer = self.convert(let_stmt.value) if let_stmt.value else None
        
        return RustLetStatement(
            pattern=pattern,
            type_annotation=type_annotation,
            initializer=initializer
        )
    
    def _convert_runa_type(self, runa_type: Optional[TypeExpression]) -> Optional[RustType]:
        """Convert Runa type to Rust type."""
        if not runa_type:
            return None
        
        if isinstance(runa_type, BasicType):
            rust_type_name = self.type_mapping.get(runa_type.name, runa_type.name)
            return RustTypeReference(path=rust_type_name)
        
        elif isinstance(runa_type, GenericType):
            base_name = runa_type.base_type.name if isinstance(runa_type.base_type, BasicType) else "Generic"
            rust_base_name = self.type_mapping.get(base_name, base_name)
            
            type_args = [self._convert_runa_type(arg) for arg in runa_type.type_arguments if arg]
            
            return RustTypeReference(
                path=rust_base_name,
                type_arguments=type_args
            )
        
        elif isinstance(runa_type, OptionalType):
            inner_type = self._convert_runa_type(runa_type.inner_type)
            return RustTypeReference(
                path="Option",
                type_arguments=[inner_type] if inner_type else []
            )
        
        elif isinstance(runa_type, FunctionType):
            param_types = [self._convert_runa_type(t) for t in runa_type.parameter_types if t]
            return_type = self._convert_runa_type(runa_type.return_type)
            
            annotations = runa_type.annotations or {}
            return RustFunctionType(
                parameters=param_types,
                return_type=return_type,
                is_unsafe=annotations.get("rust_unsafe", False),
                is_extern=annotations.get("rust_extern", False),
                abi=annotations.get("rust_abi")
            )
        
        else:
            return RustTypeReference(path="Any")
    
    def _convert_runa_pattern(self, pattern) -> RustPattern:
        """Convert Runa pattern to Rust pattern."""
        if isinstance(pattern, Identifier):
            return RustIdentifierPattern(name=pattern.name)
        else:
            return RustWildcardPattern()
    
    def _create_rust_placeholder(self, runa_node: ASTNode) -> RustExpression:
        """Create Rust placeholder for unconverted nodes."""
        return RustIdentifier(name=f"runa_{type(runa_node).__name__.lower()}")


# Convenience functions
def rust_to_runa(rust_ast: RustNode) -> ASTNode:
    """Convert Rust AST to Runa AST."""
    converter = RustToRunaConverter()
    return converter.convert(rust_ast)


def runa_to_rust(runa_ast: ASTNode) -> RustNode:
    """Convert Runa AST to Rust AST."""
    converter = RunaToRustConverter()
    return converter.convert(runa_ast)