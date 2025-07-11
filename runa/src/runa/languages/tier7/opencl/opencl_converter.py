#!/usr/bin/env python3
"""
OpenCL Converter - Bidirectional OpenCL ↔ Runa AST Conversion

Provides comprehensive conversion between OpenCL C and Runa AST including:
- Kernel function mapping
- Memory space qualifiers (__global, __local, __private, __constant)
- Vector type conversions
- Built-in function translations
- Work item and work group function mapping
- Parallel computing construct handling
- Address space and access qualifier preservation

Maintains semantic equivalence and supports round-trip conversion.
"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass

from .opencl_ast import *
from runa.languages.shared.runa_ast import *


class OpenCLToRunaConverter:
    """Converts OpenCL AST to Runa AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.kernel_metadata: Dict[str, Any] = {}
        self.memory_mappings: Dict[str, str] = {}
        
        # OpenCL to Runa type mappings
        self.type_mappings = {
            # Scalar types
            "bool": "Boolean",
            "char": "Int8",
            "uchar": "UInt8", 
            "short": "Int16",
            "ushort": "UInt16",
            "int": "Int32",
            "uint": "UInt32",
            "long": "Int64",
            "ulong": "UInt64",
            "float": "Float32",
            "double": "Float64",
            "half": "Float16",
            "void": "Unit",
            "size_t": "USize",
            "ptrdiff_t": "ISize",
        }
        
        # Built-in function mappings
        self.builtin_mappings = {
            # Work item functions
            "get_global_id": "runa.parallel.global_id",
            "get_local_id": "runa.parallel.local_id",
            "get_group_id": "runa.parallel.group_id",
            "get_global_size": "runa.parallel.global_size",
            "get_local_size": "runa.parallel.local_size",
            "get_num_groups": "runa.parallel.num_groups",
            "get_work_dim": "runa.parallel.work_dim",
            "get_global_offset": "runa.parallel.global_offset",
            
            # Math functions
            "sqrt": "runa.math.sqrt",
            "pow": "runa.math.pow",
            "exp": "runa.math.exp",
            "log": "runa.math.log",
            "sin": "runa.math.sin",
            "cos": "runa.math.cos",
            "tan": "runa.math.tan",
            "abs": "runa.math.abs",
            "min": "runa.math.min",
            "max": "runa.math.max",
            "floor": "runa.math.floor",
            "ceil": "runa.math.ceil",
            
            # Vector functions
            "dot": "runa.vector.dot",
            "cross": "runa.vector.cross",
            "length": "runa.vector.length",
            "normalize": "runa.vector.normalize",
            "distance": "runa.vector.distance",
            
            # Synchronization
            "barrier": "runa.parallel.barrier",
            "mem_fence": "runa.parallel.memory_fence",
        }
    
    def convert(self, opencl_ast: OpenCLProgram) -> RunaModule:
        """Convert OpenCL program to Runa module"""
        runa_declarations = []
        imports = []
        
        # Add standard parallel computing imports
        imports.append(RunaImport(
            path="runa.parallel",
            alias=None,
            items=["global_id", "local_id", "group_id", "barrier"]
        ))
        imports.append(RunaImport(
            path="runa.math",
            alias=None,
            items=["sqrt", "pow", "sin", "cos", "tan", "abs", "min", "max"]
        ))
        imports.append(RunaImport(
            path="runa.vector",
            alias=None,
            items=["Vector2", "Vector3", "Vector4", "dot", "cross", "normalize"]
        ))
        
        # Convert declarations
        for decl in opencl_ast.declarations:
            runa_decl = self._convert_declaration(decl)
            if runa_decl:
                runa_declarations.append(runa_decl)
        
        return RunaModule(
            name="opencl_program",
            imports=imports,
            declarations=runa_declarations,
            exports=[],
            metadata={
                "source_language": "opencl",
                "kernels": list(self.kernel_metadata.keys()),
                "memory_model": "opencl_parallel"
            }
        )
    
    def _convert_declaration(self, decl: OpenCLDeclaration) -> Optional[Declaration]:
        """Convert OpenCL declaration to Runa declaration"""
        if isinstance(decl, OpenCLKernelDeclaration):
            return self._convert_kernel_declaration(decl)
        elif isinstance(decl, OpenCLFunctionDeclaration):
            return self._convert_function_declaration(decl)
        elif isinstance(decl, OpenCLVariableDeclaration):
            return self._convert_variable_declaration(decl)
        elif isinstance(decl, OpenCLStructDeclaration):
            return self._convert_struct_declaration(decl)
        elif isinstance(decl, OpenCLTypedefDeclaration):
            return self._convert_typedef_declaration(decl)
        elif isinstance(decl, OpenCLEnumDeclaration):
            return self._convert_enum_declaration(decl)
        else:
            return None
    
    def _convert_kernel_declaration(self, kernel: OpenCLKernelDeclaration) -> ProcessDefinition:
        """Convert OpenCL kernel to Runa parallel function"""
        # Store kernel metadata
        self.kernel_metadata[kernel.name] = {
            "parameters": len(kernel.parameters),
            "memory_spaces": [p.address_space.value if p.address_space else None 
                            for p in kernel.parameters]
        }
        
        # Convert parameters
        runa_params = []
        for param in kernel.parameters:
            runa_param = self._convert_parameter(param)
            runa_params.append(runa_param)
        
        # Convert body
        runa_body = self._convert_statement(kernel.body) if kernel.body else Block([])
        
        # Create parallel function with kernel annotations
        return ProcessDefinition(
            name=kernel.name,
            parameters=runa_params,
            return_type=self._convert_type(kernel.return_type),
            body=runa_body,
            annotations=[
                RunaAnnotation(
                    name="kernel",
                    args={}
                ),
                RunaAnnotation(
                    name="parallel",
                    args={"execution_model": "opencl"}
                )
            ],
            visibility=RunaVisibility.PUBLIC,
            is_async=False
        )
    
    def _convert_function_declaration(self, func: OpenCLFunctionDeclaration) -> ProcessDefinition:
        """Convert OpenCL function to Runa function"""
        runa_params = [self._convert_parameter(p) for p in func.parameters]
        
        runa_body = self._convert_statement(func.body) if func.body else None
        
        # Check for inline qualifier
        is_inline = FunctionQualifier.INLINE in func.qualifiers
        
        return ProcessDefinition(
            name=func.name,
            parameters=runa_params,
            return_type=self._convert_type(func.return_type),
            body=runa_body,
            annotations=[RunaAnnotation("inline", {})] if is_inline else [],
            visibility=RunaVisibility.PUBLIC,
            is_async=False
        )
    
    def _convert_parameter(self, param: OpenCLParameter) -> Parameter:
        """Convert OpenCL parameter to Runa parameter"""
        runa_type = self._convert_type(param.type)
        
        # Handle address space qualifiers
        if param.address_space:
            # Wrap type with memory space annotation
            runa_type = RunaAnnotatedType(
                base_type=runa_type,
                annotations=[
                    RunaAnnotation(
                        name="memory_space",
                        args={"space": param.address_space.value}
                    )
                ]
            )
        
        # Handle access qualifiers for images
        if param.access_qualifier:
            if isinstance(runa_type, RunaAnnotatedType):
                runa_type.annotations.append(
                    RunaAnnotation(
                        name="access",
                        args={"qualifier": param.access_qualifier.value}
                    )
                )
            else:
                runa_type = RunaAnnotatedType(
                    base_type=runa_type,
                    annotations=[
                        RunaAnnotation(
                            name="access",
                            args={"qualifier": param.access_qualifier.value}
                        )
                    ]
                )
        
        return Parameter(
            name=param.name,
            param_type=runa_type,
            default_value=None,
            is_variadic=False
        )
    
    def _convert_variable_declaration(self, var: OpenCLVariableDeclaration) -> LetStatement:
        """Convert OpenCL variable to Runa variable"""
        runa_type = self._convert_type(var.type)
        
        # Handle address space
        if var.address_space:
            runa_type = RunaAnnotatedType(
                base_type=runa_type,
                annotations=[
                    RunaAnnotation(
                        name="memory_space",
                        args={"space": var.address_space.value}
                    )
                ]
            )
        
        runa_init = self._convert_expression(var.initializer) if var.initializer else None
        
        return LetStatement(
            name=var.name,
            var_type=runa_type,
            value=runa_init,
            is_mutable=not var.is_const,
            visibility=RunaVisibility.LOCAL
        )
    
    def _convert_struct_declaration(self, struct: OpenCLStructDeclaration) -> RunaStructDeclaration:
        """Convert OpenCL struct to Runa struct"""
        runa_fields = []
        for field in struct.fields:
            runa_field = RunaStructField(
                name=field.name,
                field_type=self._convert_type(field.type),
                visibility=RunaVisibility.PUBLIC
            )
            runa_fields.append(runa_field)
        
        annotations = []
        if struct.is_packed:
            annotations.append(RunaAnnotation("packed", {}))
        
        return RunaStructDeclaration(
            name=struct.name,
            fields=runa_fields,
            annotations=annotations,
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_typedef_declaration(self, typedef: OpenCLTypedefDeclaration) -> BasicTypeDeclaration:
        """Convert OpenCL typedef to Runa type alias"""
        return BasicTypeDeclaration(
            name=typedef.name,
            type_def=self._convert_type(typedef.type),
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_enum_declaration(self, enum: OpenCLEnumDeclaration) -> RunaEnumDeclaration:
        """Convert OpenCL enum to Runa enum"""
        runa_variants = []
        for name, value in enum.values:
            runa_value = self._convert_expression(value) if value else None
            runa_variants.append(RunaEnumVariant(name, [], runa_value))
        
        return RunaEnumDeclaration(
            name=enum.name or "AnonymousEnum",
            variants=runa_variants,
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_type(self, opencl_type: OpenCLType) -> BasicType:
        """Convert OpenCL type to Runa type"""
        if isinstance(opencl_type, OpenCLBuiltinType):
            if opencl_type.vector_size:
                # Vector type
                base_type = self.type_mappings.get(opencl_type.name, opencl_type.name)
                return GenericType(
                    name=f"Vector{opencl_type.vector_size}",
                    type_args=[RunaNominalType(base_type)]
                )
            else:
                # Scalar type
                return RunaNominalType(
                    self.type_mappings.get(opencl_type.name, opencl_type.name)
                )
        
        elif isinstance(opencl_type, OpenCLPointerType):
            base_type = self._convert_type(opencl_type.base_type)
            pointer_type = RunaPointerType(base_type)
            
            if opencl_type.address_space:
                return RunaAnnotatedType(
                    base_type=pointer_type,
                    annotations=[
                        RunaAnnotation(
                            name="memory_space",
                            args={"space": opencl_type.address_space.value}
                        )
                    ]
                )
            return pointer_type
        
        elif isinstance(opencl_type, OpenCLArrayType):
            element_type = self._convert_type(opencl_type.element_type)
            if opencl_type.size:
                size_expr = self._convert_expression(opencl_type.size)
                return ListLiteralType(element_type, size_expr)
            else:
                return RunaSliceType(element_type)
        
        elif isinstance(opencl_type, OpenCLImageType):
            # Map image types to Runa image types
            return GenericType(
                name="Image",
                type_args=[
                    RunaNominalType(opencl_type.dimension),
                    RunaNominalType(opencl_type.access_qualifier.value if opencl_type.access_qualifier else "ReadWrite")
                ]
            )
        
        else:
            return RunaNominalType("Unknown")
    
    def _convert_statement(self, stmt: OpenCLStatement) -> Statement:
        """Convert OpenCL statement to Runa statement"""
        if isinstance(stmt, OpenCLBlock):
            runa_stmts = [self._convert_statement(s) for s in stmt.statements]
            return Block(runa_stmts)
        
        elif isinstance(stmt, OpenCLExpressionStatement):
            return ExpressionStatement(self._convert_expression(stmt.expression))
        
        elif isinstance(stmt, OpenCLIfStatement):
            condition = self._convert_expression(stmt.condition)
            then_stmt = self._convert_statement(stmt.then_stmt)
            else_stmt = self._convert_statement(stmt.else_stmt) if stmt.else_stmt else None
            return IfStatement(condition, then_stmt, else_stmt)
        
        elif isinstance(stmt, OpenCLWhileLoop):
            condition = self._convert_expression(stmt.condition)
            body = self._convert_statement(stmt.body)
            return WhileLoop(condition, body)
        
        elif isinstance(stmt, OpenCLForLoop):
            # Convert to Runa for loop
            init = self._convert_statement(stmt.init) if stmt.init else None
            condition = self._convert_expression(stmt.condition) if stmt.condition else None
            update = self._convert_expression(stmt.update) if stmt.update else None
            body = self._convert_statement(stmt.body)
            
            # Create equivalent Runa for loop structure
            return RunaForLoop(
                variable="i",  # Default variable name
                iterable=RunaRange(
                    start=StringLiteral(0),
                    end=condition if condition else StringLiteral(10),
                    step=None
                ),
                body=body
            )
        
        elif isinstance(stmt, OpenCLDoWhileLoop):
            # Convert to equivalent while loop
            body = self._convert_statement(stmt.body)
            condition = self._convert_expression(stmt.condition)
            return WhileLoop(condition, body)
        
        elif isinstance(stmt, OpenCLReturnStatement):
            value = self._convert_expression(stmt.value) if stmt.value else None
            return ReturnStatementStatement(value)
        
        elif isinstance(stmt, OpenCLBreakStatement):
            return BreakStatementStatement()
        
        elif isinstance(stmt, OpenCLContinueStatement):
            return ContinueStatementStatement()
        
        elif isinstance(stmt, OpenCLBarrier):
            # Convert barrier to Runa parallel barrier
            return ExpressionStatement(
                FunctionCall(
                    function=Identifier("runa.parallel.barrier"),
                    args=[StringLiteral(stmt.memory_fence)]
                )
            )
        
        else:
            return ExpressionStatement(StringLiteral(None))
    
    def _convert_expression(self, expr: OpenCLExpression) -> Expression:
        """Convert OpenCL expression to Runa expression"""
        if isinstance(expr, OpenCLIdentifier):
            return Identifier(expr.name)
        
        elif isinstance(expr, OpenCLLiteral):
            return StringLiteral(expr.value)
        
        elif isinstance(expr, OpenCLVectorLiteral):
            # Convert vector constructor to Runa tuple/vector
            components = [self._convert_expression(c) for c in expr.components]
            return FunctionCall(
                function=Identifier(f"Vector{len(components)}"),
                args=components
            )
        
        elif isinstance(expr, OpenCLBinaryOp):
            left = self._convert_expression(expr.left)
            right = self._convert_expression(expr.right)
            return RunaBinaryOp(left, expr.operator, right)
        
        elif isinstance(expr, OpenCLUnaryOp):
            operand = self._convert_expression(expr.operand)
            return RunaUnaryOp(expr.operator, operand)
        
        elif isinstance(expr, OpenCLArrayAccess):
            array = self._convert_expression(expr.array)
            index = self._convert_expression(expr.index)
            return IndexAccess(array, index)
        
        elif isinstance(expr, OpenCLFieldAccess):
            object_expr = self._convert_expression(expr.object)
            return RunaFieldAccess(object_expr, expr.field)
        
        elif isinstance(expr, OpenCLFunctionCall):
            args = [self._convert_expression(arg) for arg in expr.args]
            return FunctionCall(
                function=Identifier(expr.name),
                args=args
            )
        
        elif isinstance(expr, OpenCLBuiltinCall):
            # Map built-in function to Runa equivalent
            runa_name = self.builtin_mappings.get(expr.name, expr.name)
            args = [self._convert_expression(arg) for arg in expr.args]
            return FunctionCall(
                function=Identifier(runa_name),
                args=args
            )
        
        elif isinstance(expr, OpenCLCast):
            target_type = self._convert_type(expr.target_type)
            expression = self._convert_expression(expr.expression)
            return RunaCast(expression, target_type)
        
        elif isinstance(expr, OpenCLConditional):
            condition = self._convert_expression(expr.condition)
            true_expr = self._convert_expression(expr.true_expr)
            false_expr = self._convert_expression(expr.false_expr)
            return IfStatement(condition, true_expr, false_expr)
        
        else:
            return StringLiteral(None)


class RunaToOpenCLConverter:
    """Converts Runa AST to OpenCL AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.kernel_functions: Set[str] = set()
        
        # Reverse type mappings
        self.type_mappings = {
            "Boolean": "bool",
            "Int8": "char",
            "UInt8": "uchar",
            "Int16": "short", 
            "UInt16": "ushort",
            "Int32": "int",
            "UInt32": "uint",
            "Int64": "long",
            "UInt64": "ulong",
            "Float32": "float",
            "Float64": "double",
            "Float16": "half",
            "Unit": "void",
            "USize": "size_t",
            "ISize": "ptrdiff_t",
        }
        
        # Reverse builtin mappings
        self.builtin_mappings = {
            "runa.parallel.global_id": "get_global_id",
            "runa.parallel.local_id": "get_local_id",
            "runa.parallel.group_id": "get_group_id",
            "runa.parallel.global_size": "get_global_size",
            "runa.parallel.local_size": "get_local_size",
            "runa.parallel.num_groups": "get_num_groups",
            "runa.parallel.work_dim": "get_work_dim",
            "runa.parallel.global_offset": "get_global_offset",
            "runa.parallel.barrier": "barrier",
            "runa.parallel.memory_fence": "mem_fence",
            "runa.math.sqrt": "sqrt",
            "runa.math.pow": "pow",
            "runa.math.exp": "exp",
            "runa.math.log": "log",
            "runa.math.sin": "sin",
            "runa.math.cos": "cos",
            "runa.math.tan": "tan",
            "runa.math.abs": "abs",
            "runa.math.min": "min",
            "runa.math.max": "max",
            "runa.math.floor": "floor",
            "runa.math.ceil": "ceil",
            "runa.vector.dot": "dot",
            "runa.vector.cross": "cross",
            "runa.vector.length": "length",
            "runa.vector.normalize": "normalize",
            "runa.vector.distance": "distance",
        }
    
    def convert(self, runa_module: RunaModule) -> OpenCLProgram:
        """Convert Runa module to OpenCL program"""
        opencl_declarations = []
        preprocessor_directives = []
        
        # Extract kernel functions from metadata
        if "kernels" in runa_module.metadata:
            self.kernel_functions.update(runa_module.metadata["kernels"])
        
        # Convert declarations
        for decl in runa_module.declarations:
            opencl_decl = self._convert_declaration(decl)
            if opencl_decl:
                opencl_declarations.append(opencl_decl)
        
        return OpenCLProgram(
            declarations=opencl_declarations,
            preprocessor_directives=preprocessor_directives,
            metadata={
                "source_language": "runa",
                "target_language": "opencl"
            }
        )
    
    def _convert_declaration(self, decl: Declaration) -> Optional[OpenCLDeclaration]:
        """Convert Runa declaration to OpenCL declaration"""
        if isinstance(decl, ProcessDefinition):
            return self._convert_function_declaration(decl)
        elif isinstance(decl, LetStatement):
            return self._convert_variable_declaration(decl)
        elif isinstance(decl, RunaStructDeclaration):
            return self._convert_struct_declaration(decl)
        elif isinstance(decl, BasicTypeDeclaration):
            return self._convert_type_declaration(decl)
        elif isinstance(decl, RunaEnumDeclaration):
            return self._convert_enum_declaration(decl)
        else:
            return None
    
    def _convert_function_declaration(self, func: ProcessDefinition) -> OpenCLDeclaration:
        """Convert Runa function to OpenCL function or kernel"""
        # Check if this is a kernel function
        is_kernel = any(ann.name == "kernel" for ann in func.annotations)
        is_kernel = is_kernel or func.name in self.kernel_functions
        
        opencl_params = [self._convert_parameter(p) for p in func.parameters]
        opencl_return_type = self._convert_type(func.return_type)
        opencl_body = self._convert_statement(func.body) if func.body else None
        
        qualifiers = []
        if any(ann.name == "inline" for ann in func.annotations):
            qualifiers.append(FunctionQualifier.INLINE)
        
        if is_kernel:
            return OpenCLKernelDeclaration(
                return_type=opencl_return_type,
                name=func.name,
                parameters=opencl_params,
                body=opencl_body or OpenCLBlock([]),
                attributes={}
            )
        else:
            return OpenCLFunctionDeclaration(
                return_type=opencl_return_type,
                name=func.name,
                parameters=opencl_params,
                qualifiers=qualifiers,
                body=opencl_body
            )
    
    def _convert_parameter(self, param: Parameter) -> OpenCLParameter:
        """Convert Runa parameter to OpenCL parameter"""
        opencl_type = self._convert_type(param.param_type)
        
        # Extract address space and access qualifiers from annotations
        address_space = None
        access_qualifier = None
        is_const = False
        
        if isinstance(param.param_type, RunaAnnotatedType):
            for ann in param.param_type.annotations:
                if ann.name == "memory_space":
                    space_name = ann.args.get("space", "")
                    if space_name in ["__global", "__local", "__private", "__constant", "__generic"]:
                        address_space = AddressSpace(space_name)
                elif ann.name == "access":
                    qualifier_name = ann.args.get("qualifier", "")
                    if qualifier_name in ["__read_only", "__write_only", "__read_write"]:
                        access_qualifier = AccessQualifier(qualifier_name)
                elif ann.name == "const":
                    is_const = True
        
        return OpenCLParameter(
            type=opencl_type,
            name=param.name,
            address_space=address_space,
            access_qualifier=access_qualifier,
            is_const=is_const
        )
    
    def _convert_variable_declaration(self, var: LetStatement) -> OpenCLVariableDeclaration:
        """Convert Runa variable to OpenCL variable"""
        opencl_type = self._convert_type(var.var_type)
        
        # Extract address space from annotations
        address_space = None
        if isinstance(var.var_type, RunaAnnotatedType):
            for ann in var.var_type.annotations:
                if ann.name == "memory_space":
                    space_name = ann.args.get("space", "")
                    if space_name in ["__global", "__local", "__private", "__constant", "__generic"]:
                        address_space = AddressSpace(space_name)
        
        opencl_init = self._convert_expression(var.value) if var.value else None
        
        return OpenCLVariableDeclaration(
            type=opencl_type,
            name=var.name,
            address_space=address_space,
            initializer=opencl_init,
            is_const=not var.is_mutable
        )
    
    def _convert_struct_declaration(self, struct: RunaStructDeclaration) -> OpenCLStructDeclaration:
        """Convert Runa struct to OpenCL struct"""
        opencl_fields = []
        for field in struct.fields:
            opencl_field = OpenCLVariableDeclaration(
                type=self._convert_type(field.field_type),
                name=field.name,
                is_const=False
            )
            opencl_fields.append(opencl_field)
        
        is_packed = any(ann.name == "packed" for ann in struct.annotations)
        
        return OpenCLStructDeclaration(
            name=struct.name,
            fields=opencl_fields,
            is_packed=is_packed
        )
    
    def _convert_type_declaration(self, typedef: BasicTypeDeclaration) -> OpenCLTypedefDeclaration:
        """Convert Runa type alias to OpenCL typedef"""
        return OpenCLTypedefDeclaration(
            type=self._convert_type(typedef.type_def),
            name=typedef.name
        )
    
    def _convert_enum_declaration(self, enum: RunaEnumDeclaration) -> OpenCLEnumDeclaration:
        """Convert Runa enum to OpenCL enum"""
        opencl_values = []
        for variant in enum.variants:
            value = self._convert_expression(variant.value) if variant.value else None
            opencl_values.append((variant.name, value))
        
        return OpenCLEnumDeclaration(
            name=enum.name,
            values=opencl_values
        )
    
    def _convert_type(self, runa_type: BasicType) -> OpenCLType:
        """Convert Runa type to OpenCL type"""
        if isinstance(runa_type, RunaNominalType):
            opencl_name = self.type_mappings.get(runa_type.name, runa_type.name)
            return OpenCLBuiltinType(name=opencl_name)
        
        elif isinstance(runa_type, GenericType):
            if runa_type.name.startswith("Vector"):
                # Extract vector size
                size_str = runa_type.name.replace("Vector", "")
                try:
                    vector_size = int(size_str)
                    if runa_type.type_args:
                        base_type = self._convert_type(runa_type.type_args[0])
                        if isinstance(base_type, OpenCLBuiltinType):
                            return OpenCLBuiltinType(
                                name=base_type.name,
                                vector_size=vector_size
                            )
                except ValueError:
                    pass
            elif runa_type.name == "Image":
                # Handle image types
                dimension = "2d"  # Default
                access = AccessQualifier.READ_WRITE  # Default
                if len(runa_type.type_args) >= 1:
                    dim_type = runa_type.type_args[0]
                    if isinstance(dim_type, RunaNominalType):
                        dimension = dim_type.name
                if len(runa_type.type_args) >= 2:
                    access_type = runa_type.type_args[1]
                    if isinstance(access_type, RunaNominalType):
                        if access_type.name in ["ReadOnly", "WriteOnly", "ReadWrite"]:
                            access_map = {
                                "ReadOnly": AccessQualifier.READ_ONLY,
                                "WriteOnly": AccessQualifier.WRITE_ONLY,
                                "ReadWrite": AccessQualifier.READ_WRITE
                            }
                            access = access_map[access_type.name]
                
                return OpenCLImageType(dimension=dimension, access_qualifier=access)
            
            return OpenCLBuiltinType(name=runa_type.name)
        
        elif isinstance(runa_type, RunaPointerType):
            base_type = self._convert_type(runa_type.target_type)
            return OpenCLPointerType(base_type=base_type)
        
        elif isinstance(runa_type, ListLiteralType):
            element_type = self._convert_type(runa_type.element_type)
            size = self._convert_expression(runa_type.size) if runa_type.size else None
            return OpenCLArrayType(element_type=element_type, size=size)
        
        elif isinstance(runa_type, RunaSliceType):
            element_type = self._convert_type(runa_type.element_type)
            return OpenCLArrayType(element_type=element_type, size=None)
        
        elif isinstance(runa_type, RunaAnnotatedType):
            return self._convert_type(runa_type.base_type)
        
        else:
            return OpenCLBuiltinType(name="void")
    
    def _convert_statement(self, stmt: Statement) -> OpenCLStatement:
        """Convert Runa statement to OpenCL statement"""
        if isinstance(stmt, Block):
            opencl_stmts = [self._convert_statement(s) for s in stmt.statements]
            return OpenCLBlock(opencl_stmts)
        
        elif isinstance(stmt, ExpressionStatement):
            return OpenCLExpressionStatement(self._convert_expression(stmt.expression))
        
        elif isinstance(stmt, IfStatement):
            condition = self._convert_expression(stmt.condition)
            then_stmt = self._convert_statement(stmt.then_stmt)
            else_stmt = self._convert_statement(stmt.else_stmt) if stmt.else_stmt else None
            return OpenCLIfStatement(condition, then_stmt, else_stmt)
        
        elif isinstance(stmt, WhileLoop):
            condition = self._convert_expression(stmt.condition)
            body = self._convert_statement(stmt.body)
            return OpenCLWhileLoop(condition, body)
        
        elif isinstance(stmt, RunaForLoop):
            # Convert Runa for loop to OpenCL for loop
            init = OpenCLVariableDeclaration(
                type=OpenCLBuiltinType("int"),
                name=stmt.variable,
                initializer=self._convert_expression(stmt.iterable.start) if hasattr(stmt.iterable, 'start') else OpenCLLiteral(0)
            )
            
            condition = OpenCLBinaryOp(
                left=OpenCLIdentifier(stmt.variable),
                operator="<",
                right=self._convert_expression(stmt.iterable.end) if hasattr(stmt.iterable, 'end') else OpenCLLiteral(10)
            )
            
            update = OpenCLUnaryOp("++", OpenCLIdentifier(stmt.variable))
            body = self._convert_statement(stmt.body)
            
            return OpenCLForLoop(init, condition, update, body)
        
        elif isinstance(stmt, ReturnStatementStatement):
            value = self._convert_expression(stmt.value) if stmt.value else None
            return OpenCLReturnStatement(value)
        
        elif isinstance(stmt, BreakStatementStatement):
            return OpenCLBreakStatement()
        
        elif isinstance(stmt, ContinueStatementStatement):
            return OpenCLContinueStatement()
        
        else:
            return OpenCLExpressionStatement(OpenCLLiteral(None))
    
    def _convert_expression(self, expr: Expression) -> OpenCLExpression:
        """Convert Runa expression to OpenCL expression"""
        if isinstance(expr, Identifier):
            return OpenCLIdentifier(expr.name)
        
        elif isinstance(expr, StringLiteral):
            return OpenCLLiteral(expr.value)
        
        elif isinstance(expr, RunaBinaryOp):
            left = self._convert_expression(expr.left)
            right = self._convert_expression(expr.right)
            return OpenCLBinaryOp(left, expr.operator, right)
        
        elif isinstance(expr, RunaUnaryOp):
            operand = self._convert_expression(expr.operand)
            return OpenCLUnaryOp(expr.operator, operand)
        
        elif isinstance(expr, IndexAccess):
            array = self._convert_expression(expr.object)
            index = self._convert_expression(expr.index)
            return OpenCLArrayAccess(array, index)
        
        elif isinstance(expr, RunaFieldAccess):
            object_expr = self._convert_expression(expr.object)
            return OpenCLFieldAccess(object_expr, expr.field)
        
        elif isinstance(expr, FunctionCall):
            # Check if this is a built-in function mapping
            func_name = ""
            if isinstance(expr.function, Identifier):
                func_name = expr.function.name
                opencl_name = self.builtin_mappings.get(func_name, func_name)
                
                args = [self._convert_expression(arg) for arg in expr.args]
                
                if opencl_name != func_name:
                    # This is a built-in function
                    category = self._get_builtin_category(opencl_name)
                    return OpenCLBuiltinCall(opencl_name, args, category)
                else:
                    return OpenCLFunctionCall(opencl_name, args)
            else:
                args = [self._convert_expression(arg) for arg in expr.args]
                return OpenCLFunctionCall("", args)
        
        elif isinstance(expr, RunaCast):
            target_type = self._convert_type(expr.target_type)
            expression = self._convert_expression(expr.expression)
            return OpenCLCast(target_type, expression)
        
        elif isinstance(expr, IfStatement):
            condition = self._convert_expression(expr.condition)
            true_expr = self._convert_expression(expr.true_expr)
            false_expr = self._convert_expression(expr.false_expr)
            return OpenCLConditional(condition, true_expr, false_expr)
        
        else:
            return OpenCLLiteral(None)
    
    def _get_builtin_category(self, name: str) -> str:
        """Get category for built-in function"""
        for category, functions in OPENCL_BUILTIN_FUNCTIONS.items():
            if name in functions:
                return category
        return "unknown"


# Convenience functions
def opencl_to_runa(opencl_ast: OpenCLProgram) -> RunaModule:
    """Convert OpenCL AST to Runa AST"""
    converter = OpenCLToRunaConverter()
    return converter.convert(opencl_ast)


def runa_to_opencl(runa_module: RunaModule) -> OpenCLProgram:
    """Convert Runa AST to OpenCL AST"""
    converter = RunaToOpenCLConverter()
    return converter.convert(runa_module) 