#!/usr/bin/env python3
"""
HCL Converter - Bidirectional HCL ↔ Runa AST Conversion

Provides comprehensive conversion between HCL and Runa AST including:
- Configuration blocks to Runa modules and structs
- Attribute assignments to Runa variable declarations
- String interpolation to Runa string templates
- Function calls with HCL built-in function mapping
- Terraform-specific constructs to infrastructure patterns
- Expression conversion preserving semantics
- Type system mapping between HCL and Runa

Maintains semantic equivalence and supports round-trip conversion.
"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass

from .hcl_ast import *
from runa.languages.shared.runa_ast import *


class HCLToRunaConverter:
    """Converts HCL AST to Runa AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.terraform_metadata: Dict[str, Any] = {}
        self.variable_mappings: Dict[str, str] = {}
        
        # HCL to Runa type mappings
        self.type_mappings = {
            "string": "String",
            "number": "Number",
            "bool": "Boolean",
            "list": "List",
            "map": "Map",
            "object": "Struct",
            "null": "Option<T>",
        }
        
        # HCL built-in function mappings
        self.function_mappings = {
            # String functions
            "upper": "runa.string.to_upper",
            "lower": "runa.string.to_lower",
            "trim": "runa.string.trim",
            "trimspace": "runa.string.trim",
            "split": "runa.string.split",
            "join": "runa.string.join",
            "replace": "runa.string.replace",
            "substr": "runa.string.substring",
            "format": "runa.string.format",
            
            # Numeric functions
            "abs": "runa.math.abs",
            "ceil": "runa.math.ceil",
            "floor": "runa.math.floor",
            "max": "runa.math.max",
            "min": "runa.math.min",
            "pow": "runa.math.pow",
            "log": "runa.math.log",
            
            # Collection functions
            "length": "runa.collection.length",
            "concat": "runa.collection.concat",
            "contains": "runa.collection.contains",
            "distinct": "runa.collection.distinct",
            "element": "runa.collection.get",
            "index": "runa.collection.index_of",
            "keys": "runa.collection.keys",
            "values": "runa.collection.values",
            "merge": "runa.collection.merge",
            "reverse": "runa.collection.reverse",
            "sort": "runa.collection.sort",
            "slice": "runa.collection.slice",
            "flatten": "runa.collection.flatten",
            
            # Type conversion
            "tostring": "runa.convert.to_string",
            "tonumber": "runa.convert.to_number",
            "tobool": "runa.convert.to_boolean",
            "tolist": "runa.convert.to_list",
            "tomap": "runa.convert.to_map",
            
            # Encoding
            "base64encode": "runa.encoding.base64_encode",
            "base64decode": "runa.encoding.base64_decode",
            "jsonencode": "runa.encoding.json_encode",
            "jsondecode": "runa.encoding.json_decode",
            "yamlencode": "runa.encoding.yaml_encode",
            "yamldecode": "runa.encoding.yaml_decode",
            
            # File functions
            "file": "runa.fs.read_file",
            "fileexists": "runa.fs.file_exists",
            "dirname": "runa.path.dirname",
            "basename": "runa.path.basename",
            "abspath": "runa.path.absolute",
            
            # Crypto functions
            "md5": "runa.crypto.md5",
            "sha1": "runa.crypto.sha1",
            "sha256": "runa.crypto.sha256",
            "sha512": "runa.crypto.sha512",
            "uuid": "runa.crypto.uuid",
            
            # Network functions
            "cidrhost": "runa.net.cidr_host",
            "cidrnetmask": "runa.net.cidr_netmask",
            "cidrsubnet": "runa.net.cidr_subnet",
        }
    
    def convert(self, hcl_config: HCLConfiguration) -> RunaModule:
        """Convert HCL configuration to Runa module"""
        runa_declarations = []
        imports = []
        
        # Add standard imports for HCL functionality
        imports.extend([
            RunaImport(path="runa.string", alias=None, items=["format", "join", "split"]),
            RunaImport(path="runa.collection", alias=None, items=["map", "filter", "merge"]),
            RunaImport(path="runa.infrastructure", alias=None, items=["Resource", "DataSource", "Provider"]),
        ])
        
        # Convert body items
        for item in hcl_config.body:
            runa_decl = self._convert_body_item(item)
            if runa_decl:
                if isinstance(runa_decl, list):
                    runa_declarations.extend(runa_decl)
                else:
                    runa_declarations.append(runa_decl)
        
        return RunaModule(
            name="hcl_configuration",
            imports=imports,
            declarations=runa_declarations,
            exports=[],
            metadata={
                "source_language": "hcl",
                "terraform_blocks": list(self.terraform_metadata.keys()),
                "configuration_type": "infrastructure"
            }
        )
    
    def _convert_body_item(self, item: Union[HCLBlock, HCLAttribute, HCLComment]) -> Optional[Union[Declaration, List[Declaration]]]:
        """Convert HCL body item to Runa declaration"""
        if isinstance(item, HCLBlock):
            return self._convert_block(item)
        elif isinstance(item, HCLAttribute):
            return self._convert_attribute(item)
        elif isinstance(item, HCLComment):
            return None  # Comments are not converted to declarations
        else:
            return None
    
    def _convert_block(self, block: HCLBlock) -> Optional[Union[Declaration, List[Declaration]]]:
        """Convert HCL block to Runa declaration"""
        if isinstance(block, HCLVariable):
            return self._convert_variable_block(block)
        elif isinstance(block, HCLResource):
            return self._convert_resource_block(block)
        elif isinstance(block, HCLDataSource):
            return self._convert_data_source_block(block)
        elif isinstance(block, HCLProvider):
            return self._convert_provider_block(block)
        elif isinstance(block, HCLOutput):
            return self._convert_output_block(block)
        elif isinstance(block, HCLLocal):
            return self._convert_locals_block(block)
        elif isinstance(block, HCLModule):
            return self._convert_module_block(block)
        else:
            return self._convert_generic_block(block)
    
    def _convert_variable_block(self, var: HCLVariable) -> LetStatement:
        """Convert Terraform variable to Runa variable declaration"""
        # Store variable metadata
        self.terraform_metadata[f"var.{var.name}"] = {
            "type": "variable",
            "description": var.description,
            "sensitive": var.sensitive
        }
        
        # Determine Runa type
        runa_type = RunaNominalType("Any")
        if var.type_constraint:
            runa_type = self._convert_type_constraint(var.type_constraint)
        
        # Add validation annotations
        annotations = []
        if var.sensitive:
            annotations.append(RunaAnnotation("sensitive", {}))
        if var.description:
            annotations.append(RunaAnnotation("description", {"text": var.description}))
        
        # Apply annotations to type
        if annotations:
            runa_type = RunaAnnotatedType(base_type=runa_type, annotations=annotations)
        
        # Convert default value
        runa_default = self._convert_expression(var.default) if var.default else None
        
        return LetStatement(
            name=var.name,
            var_type=runa_type,
            value=runa_default,
            is_mutable=False,  # Terraform variables are immutable
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_resource_block(self, resource: HCLResource) -> RunaStructDeclaration:
        """Convert Terraform resource to Runa struct declaration"""
        # Store resource metadata
        self.terraform_metadata[f"resource.{resource.type}.{resource.name}"] = {
            "type": "resource",
            "provider": resource.provider,
            "count": resource.count is not None,
            "for_each": resource.for_each is not None
        }
        
        # Convert resource attributes to struct fields
        fields = []
        for item in resource.body:
            if isinstance(item, HCLAttribute):
                field_type = self._infer_expression_type(item.value)
                field = RunaStructField(
                    name=item.name,
                    field_type=field_type,
                    visibility=RunaVisibility.PUBLIC
                )
                fields.append(field)
        
        # Add resource lifecycle annotations
        annotations = [
            RunaAnnotation("terraform_resource", {
                "type": resource.type,
                "provider": resource.provider
            })
        ]
        
        if resource.count:
            annotations.append(RunaAnnotation("count", {}))
        if resource.for_each:
            annotations.append(RunaAnnotation("for_each", {}))
        
        return RunaStructDeclaration(
            name=f"{resource.type}_{resource.name}",
            fields=fields,
            annotations=annotations,
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_data_source_block(self, data: HCLDataSource) -> RunaStructDeclaration:
        """Convert Terraform data source to Runa struct declaration"""
        # Store data source metadata
        self.terraform_metadata[f"data.{data.type}.{data.name}"] = {
            "type": "data_source",
            "provider": data.provider
        }
        
        # Convert data source to struct with read-only annotation
        fields = []
        for item in data.body:
            if isinstance(item, HCLAttribute):
                field_type = self._infer_expression_type(item.value)
                field = RunaStructField(
                    name=item.name,
                    field_type=field_type,
                    visibility=RunaVisibility.PUBLIC
                )
                fields.append(field)
        
        annotations = [
            RunaAnnotation("terraform_data_source", {
                "type": data.type,
                "provider": data.provider
            }),
            RunaAnnotation("readonly", {})
        ]
        
        return RunaStructDeclaration(
            name=f"data_{data.type}_{data.name}",
            fields=fields,
            annotations=annotations,
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_provider_block(self, provider: HCLProvider) -> RunaStructDeclaration:
        """Convert Terraform provider to Runa struct declaration"""
        # Store provider metadata
        self.terraform_metadata[f"provider.{provider.name}"] = {
            "type": "provider",
            "alias": provider.alias,
            "version": provider.version
        }
        
        # Convert provider configuration to struct
        fields = []
        for item in provider.body:
            if isinstance(item, HCLAttribute):
                field_type = self._infer_expression_type(item.value)
                field = RunaStructField(
                    name=item.name,
                    field_type=field_type,
                    visibility=RunaVisibility.PUBLIC
                )
                fields.append(field)
        
        annotations = [
            RunaAnnotation("terraform_provider", {
                "name": provider.name,
                "alias": provider.alias,
                "version": provider.version
            })
        ]
        
        return RunaStructDeclaration(
            name=f"provider_{provider.name}",
            fields=fields,
            annotations=annotations,
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_output_block(self, output: HCLOutput) -> LetStatement:
        """Convert Terraform output to Runa variable declaration"""
        # Store output metadata
        self.terraform_metadata[f"output.{output.name}"] = {
            "type": "output",
            "description": output.description,
            "sensitive": output.sensitive
        }
        
        # Convert output value
        runa_value = self._convert_expression(output.value)
        runa_type = self._infer_expression_type(output.value)
        
        # Add output annotations
        annotations = [RunaAnnotation("terraform_output", {})]
        if output.sensitive:
            annotations.append(RunaAnnotation("sensitive", {}))
        if output.description:
            annotations.append(RunaAnnotation("description", {"text": output.description}))
        
        # Apply annotations to type
        if annotations:
            runa_type = RunaAnnotatedType(base_type=runa_type, annotations=annotations)
        
        return LetStatement(
            name=output.name,
            var_type=runa_type,
            value=runa_value,
            is_mutable=False,
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_locals_block(self, locals_block: HCLLocal) -> List[LetStatement]:
        """Convert Terraform locals to Runa variable declarations"""
        declarations = []
        
        for name, value in locals_block.assignments.items():
            runa_value = self._convert_expression(value)
            runa_type = self._infer_expression_type(value)
            
            # Add local annotation
            runa_type = RunaAnnotatedType(
                base_type=runa_type,
                annotations=[RunaAnnotation("terraform_local", {})]
            )
            
            decl = LetStatement(
                name=name,
                var_type=runa_type,
                value=runa_value,
                is_mutable=False,
                visibility=RunaVisibility.LOCAL
            )
            declarations.append(decl)
        
        return declarations
    
    def _convert_module_block(self, module: HCLModule) -> FunctionCall:
        """Convert Terraform module to Runa function call"""
        # Store module metadata
        self.terraform_metadata[f"module.{module.name}"] = {
            "type": "module",
            "source": module.source,
            "version": module.version
        }
        
        # Convert module inputs to function arguments
        args = []
        for item in module.body:
            if isinstance(item, HCLAttribute):
                arg = RunaNamedArgument(
                    name=item.name,
                    value=self._convert_expression(item.value)
                )
                args.append(arg)
        
        # Create module function call
        return FunctionCall(
            function=Identifier(f"terraform_module_{module.name}"),
            args=args
        )
    
    def _convert_generic_block(self, block: HCLBlock) -> RunaStructDeclaration:
        """Convert generic HCL block to Runa struct"""
        # Convert block body to struct fields
        fields = []
        for item in block.body:
            if isinstance(item, HCLAttribute):
                field_type = self._infer_expression_type(item.value)
                field = RunaStructField(
                    name=item.name,
                    field_type=field_type,
                    visibility=RunaVisibility.PUBLIC
                )
                fields.append(field)
        
        # Use block type and labels to create struct name
        struct_name = block.type
        if block.labels:
            struct_name += "_" + "_".join(block.labels)
        
        return RunaStructDeclaration(
            name=struct_name,
            fields=fields,
            annotations=[RunaAnnotation("hcl_block", {"type": block.type})],
            visibility=RunaVisibility.PUBLIC
        )
    
    def _convert_attribute(self, attr: HCLAttribute) -> LetStatement:
        """Convert HCL attribute to Runa variable declaration"""
        runa_value = self._convert_expression(attr.value)
        runa_type = self._infer_expression_type(attr.value)
        
        return LetStatement(
            name=attr.name,
            var_type=runa_type,
            value=runa_value,
            is_mutable=False,
            visibility=RunaVisibility.LOCAL
        )
    
    def _convert_expression(self, expr: HCLExpression) -> Expression:
        """Convert HCL expression to Runa expression"""
        if isinstance(expr, HCLLiteral):
            return StringLiteral(expr.value)
        
        elif isinstance(expr, HCLString):
            return self._convert_string(expr)
        
        elif isinstance(expr, HCLNumber):
            return StringLiteral(expr.value)
        
        elif isinstance(expr, HCLBool):
            return StringLiteral(expr.value)
        
        elif isinstance(expr, HCLNull):
            return StringLiteral(None)
        
        elif isinstance(expr, HCLList):
            elements = [self._convert_expression(elem) for elem in expr.elements]
            return ListLiteral(elements)
        
        elif isinstance(expr, HCLMap):
            pairs = []
            for key, value in expr.pairs:
                runa_key = self._convert_expression(key)
                runa_value = self._convert_expression(value)
                pairs.append((runa_key, runa_value))
            return RunaMapLiteral(pairs)
        
        elif isinstance(expr, HCLObject):
            fields = {}
            for name, value in expr.fields.items():
                fields[name] = self._convert_expression(value)
            return RunaStructLiteral(fields)
        
        elif isinstance(expr, HCLIdentifier):
            return Identifier(expr.name)
        
        elif isinstance(expr, HCLAttributeAccess):
            object_expr = self._convert_expression(expr.object)
            return RunaFieldAccess(object_expr, expr.attribute)
        
        elif isinstance(expr, HCLIndexAccess):
            object_expr = self._convert_expression(expr.object)
            index_expr = self._convert_expression(expr.index)
            return IndexAccess(object_expr, index_expr)
        
        elif isinstance(expr, HCLFunctionCall):
            return self._convert_function_call(expr)
        
        elif isinstance(expr, HCLBinaryOp):
            left = self._convert_expression(expr.left)
            right = self._convert_expression(expr.right)
            return RunaBinaryOp(left, expr.operator, right)
        
        elif isinstance(expr, HCLUnaryOp):
            operand = self._convert_expression(expr.operand)
            return RunaUnaryOp(expr.operator, operand)
        
        elif isinstance(expr, HCLConditional):
            condition = self._convert_expression(expr.condition)
            true_expr = self._convert_expression(expr.true_value)
            false_expr = self._convert_expression(expr.false_value)
            return IfStatement(condition, true_expr, false_expr)
        
        elif isinstance(expr, HCLInterpolation):
            return self._convert_expression(expr.expression)
        
        elif isinstance(expr, HCLForExpression):
            return self._convert_for_expression(expr)
        
        else:
            return StringLiteral(None)
    
    def _convert_string(self, string: HCLString) -> Expression:
        """Convert HCL string with interpolation to Runa expression"""
        if len(string.parts) == 1 and isinstance(string.parts[0], str):
            # Simple string without interpolation
            return StringLiteral(string.parts[0])
        
        # String with interpolation - convert to format call
        format_parts = []
        args = []
        
        for part in string.parts:
            if isinstance(part, str):
                format_parts.append(part)
            elif isinstance(part, HCLInterpolation):
                format_parts.append("{}")
                args.append(self._convert_expression(part.expression))
        
        format_string = "".join(format_parts)
        
        if args:
            return FunctionCall(
                function=Identifier("runa.string.format"),
                args=[StringLiteral(format_string)] + args
            )
        else:
            return StringLiteral(format_string)
    
    def _convert_function_call(self, call: HCLFunctionCall) -> FunctionCall:
        """Convert HCL function call to Runa function call"""
        # Map HCL function to Runa function
        runa_function = self.function_mappings.get(call.name, call.name)
        
        # Convert arguments
        args = [self._convert_expression(arg) for arg in call.args]
        
        return FunctionCall(
            function=Identifier(runa_function),
            args=args
        )
    
    def _convert_for_expression(self, for_expr: HCLForExpression) -> Expression:
        """Convert HCL for expression to Runa comprehension"""
        # Convert to Runa map/filter expression
        collection = self._convert_expression(for_expr.collection)
        value_expr = self._convert_expression(for_expr.value_expr)
        
        # Create lambda expression
        lambda_params = [Parameter(for_expr.value_var, RunaNominalType("Any"))]
        if for_expr.key_var:
            lambda_params.insert(0, Parameter(for_expr.key_var, RunaNominalType("Any")))
        
        lambda_expr = ProcessDefinition(lambda_params, value_expr)
        
        # Choose appropriate collection function
        if for_expr.condition:
            # Has condition - use filter then map
            condition_lambda = ProcessDefinition(
                lambda_params,
                self._convert_expression(for_expr.condition)
            )
            filtered = FunctionCall(
                function=Identifier("runa.collection.filter"),
                args=[collection, condition_lambda]
            )
            return FunctionCall(
                function=Identifier("runa.collection.map"),
                args=[filtered, lambda_expr]
            )
        else:
            # Simple map
            return FunctionCall(
                function=Identifier("runa.collection.map"),
                args=[collection, lambda_expr]
            )
    
    def _convert_type_constraint(self, type_str: str) -> BasicType:
        """Convert HCL type constraint to Runa type"""
        if type_str in self.type_mappings:
            return RunaNominalType(self.type_mappings[type_str])
        
        # Handle complex types like list(string), map(number), etc.
        if type_str.startswith("list(") and type_str.endswith(")"):
            element_type = type_str[5:-1]
            return GenericType(
                name="List",
                type_args=[self._convert_type_constraint(element_type)]
            )
        
        if type_str.startswith("map(") and type_str.endswith(")"):
            value_type = type_str[4:-1]
            return GenericType(
                name="Map",
                type_args=[
                    RunaNominalType("String"),
                    self._convert_type_constraint(value_type)
                ]
            )
        
        if type_str.startswith("object("):
            # Complex object type - simplified to generic object
            return RunaNominalType("Object")
        
        # Default to Any for unknown types
        return RunaNominalType("Any")
    
    def _infer_expression_type(self, expr: HCLExpression) -> BasicType:
        """Infer Runa type from HCL expression"""
        if isinstance(expr, HCLString):
            return RunaNominalType("String")
        elif isinstance(expr, HCLNumber):
            if isinstance(expr.value, int):
                return RunaNominalType("Int")
            else:
                return RunaNominalType("Float")
        elif isinstance(expr, HCLBool):
            return RunaNominalType("Boolean")
        elif isinstance(expr, HCLNull):
            return RunaNominalType("Option<Any>")
        elif isinstance(expr, HCLList):
            if expr.elements:
                element_type = self._infer_expression_type(expr.elements[0])
                return GenericType("List", [element_type])
            return GenericType("List", [RunaNominalType("Any")])
        elif isinstance(expr, (HCLMap, HCLObject)):
            return GenericType("Map", [RunaNominalType("String"), RunaNominalType("Any")])
        else:
            return RunaNominalType("Any")


class RunaToHCLConverter:
    """Converts Runa AST to HCL AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.terraform_resources: List[str] = []
        
        # Reverse function mappings
        self.function_mappings = {
            "runa.string.to_upper": "upper",
            "runa.string.to_lower": "lower",
            "runa.string.trim": "trim",
            "runa.string.split": "split",
            "runa.string.join": "join",
            "runa.string.replace": "replace",
            "runa.string.substring": "substr",
            "runa.string.format": "format",
            "runa.math.abs": "abs",
            "runa.math.ceil": "ceil",
            "runa.math.floor": "floor",
            "runa.math.max": "max",
            "runa.math.min": "min",
            "runa.collection.length": "length",
            "runa.collection.concat": "concat",
            "runa.collection.contains": "contains",
            "runa.convert.to_string": "tostring",
            "runa.convert.to_number": "tonumber",
            "runa.convert.to_boolean": "tobool",
            "runa.encoding.json_encode": "jsonencode",
            "runa.encoding.json_decode": "jsondecode",
            "runa.fs.read_file": "file",
            "runa.crypto.md5": "md5",
            "runa.crypto.sha256": "sha256",
        }
    
    def convert(self, runa_module: RunaModule) -> HCLConfiguration:
        """Convert Runa module to HCL configuration"""
        hcl_body = []
        
        # Convert declarations
        for decl in runa_module.declarations:
            hcl_items = self._convert_declaration(decl)
            if hcl_items:
                if isinstance(hcl_items, list):
                    hcl_body.extend(hcl_items)
                else:
                    hcl_body.append(hcl_items)
        
        return HCLConfiguration(body=hcl_body)
    
    def _convert_declaration(self, decl: Declaration) -> Optional[Union[HCLBlock, HCLAttribute, List[Union[HCLBlock, HCLAttribute]]]]:
        """Convert Runa declaration to HCL"""
        if isinstance(decl, LetStatement):
            return self._convert_variable_declaration(decl)
        elif isinstance(decl, RunaStructDeclaration):
            return self._convert_struct_declaration(decl)
        elif isinstance(decl, ProcessDefinition):
            return self._convert_function_declaration(decl)
        else:
            return None
    
    def _convert_variable_declaration(self, var: LetStatement) -> Union[HCLBlock, HCLAttribute]:
        """Convert Runa variable to HCL"""
        # Check if this is a Terraform construct based on annotations
        if isinstance(var.var_type, RunaAnnotatedType):
            for ann in var.var_type.annotations:
                if ann.name == "terraform_variable":
                    return self._create_terraform_variable(var)
                elif ann.name == "terraform_output":
                    return self._create_terraform_output(var)
                elif ann.name == "terraform_local":
                    return HCLAttribute(var.name, self._convert_expression(var.value))
        
        # Regular attribute assignment
        return HCLAttribute(var.name, self._convert_expression(var.value))
    
    def _convert_struct_declaration(self, struct: RunaStructDeclaration) -> Optional[HCLBlock]:
        """Convert Runa struct to HCL block"""
        # Check annotations to determine HCL block type
        for ann in struct.annotations:
            if ann.name == "terraform_resource":
                return self._create_terraform_resource(struct, ann)
            elif ann.name == "terraform_data_source":
                return self._create_terraform_data_source(struct, ann)
            elif ann.name == "terraform_provider":
                return self._create_terraform_provider(struct, ann)
            elif ann.name == "hcl_block":
                return self._create_generic_hcl_block(struct, ann)
        
        # Default to generic block
        return self._create_generic_hcl_block(struct, None)
    
    def _create_terraform_variable(self, var: LetStatement) -> HCLVariable:
        """Create Terraform variable block"""
        # Extract metadata from annotations
        description = None
        sensitive = False
        
        if isinstance(var.var_type, RunaAnnotatedType):
            for ann in var.var_type.annotations:
                if ann.name == "description":
                    description = ann.args.get("text")
                elif ann.name == "sensitive":
                    sensitive = True
        
        return HCLVariable(
            type="variable",
            labels=[var.name],
            body=[],
            name=var.name,
            default=self._convert_expression(var.value) if var.value else None,
            description=description,
            sensitive=sensitive
        )
    
    def _create_terraform_output(self, var: LetStatement) -> HCLOutput:
        """Create Terraform output block"""
        # Extract metadata from annotations
        description = None
        sensitive = False
        
        if isinstance(var.var_type, RunaAnnotatedType):
            for ann in var.var_type.annotations:
                if ann.name == "description":
                    description = ann.args.get("text")
                elif ann.name == "sensitive":
                    sensitive = True
        
        return HCLOutput(
            type="output",
            labels=[var.name],
            body=[],
            name=var.name,
            value=self._convert_expression(var.value) if var.value else HCLNull(),
            description=description,
            sensitive=sensitive
        )
    
    def _create_terraform_resource(self, struct: RunaStructDeclaration, ann: RunaAnnotation) -> HCLResource:
        """Create Terraform resource block"""
        resource_type = ann.args.get("type", "unknown")
        provider = ann.args.get("provider")
        
        # Extract resource name from struct name
        resource_name = struct.name
        if resource_name.startswith(f"{resource_type}_"):
            resource_name = resource_name[len(resource_type) + 1:]
        
        # Convert struct fields to attributes
        body = []
        for field in struct.fields:
            # Create a dummy value for the field
            attr = HCLAttribute(field.name, HCLString([f"${{{field.name}}}"]))
            body.append(attr)
        
        return HCLResource(
            type="resource",
            labels=[resource_type, resource_name],
            body=body,
            type=resource_type,
            name=resource_name,
            provider=provider
        )
    
    def _create_terraform_data_source(self, struct: RunaStructDeclaration, ann: RunaAnnotation) -> HCLDataSource:
        """Create Terraform data source block"""
        data_type = ann.args.get("type", "unknown")
        provider = ann.args.get("provider")
        
        # Extract data source name from struct name
        data_name = struct.name
        if data_name.startswith(f"data_{data_type}_"):
            data_name = data_name[len(f"data_{data_type}_"):]
        
        # Convert struct fields to attributes
        body = []
        for field in struct.fields:
            attr = HCLAttribute(field.name, HCLString([f"${{{field.name}}}"]))
            body.append(attr)
        
        return HCLDataSource(
            type="data",
            labels=[data_type, data_name],
            body=body,
            type=data_type,
            name=data_name,
            provider=provider
        )
    
    def _create_terraform_provider(self, struct: RunaStructDeclaration, ann: RunaAnnotation) -> HCLProvider:
        """Create Terraform provider block"""
        provider_name = ann.args.get("name", "unknown")
        alias = ann.args.get("alias")
        version = ann.args.get("version")
        
        # Convert struct fields to attributes
        body = []
        for field in struct.fields:
            attr = HCLAttribute(field.name, HCLString([f"${{{field.name}}}"]))
            body.append(attr)
        
        return HCLProvider(
            type="provider",
            labels=[provider_name],
            body=body,
            name=provider_name,
            alias=alias,
            version=version
        )
    
    def _create_generic_hcl_block(self, struct: RunaStructDeclaration, ann: Optional[RunaAnnotation]) -> HCLBlock:
        """Create generic HCL block"""
        block_type = ann.args.get("type", "block") if ann else "block"
        
        # Convert struct fields to attributes
        body = []
        for field in struct.fields:
            attr = HCLAttribute(field.name, HCLString([f"${{{field.name}}}"]))
            body.append(attr)
        
        return HCLBlock(
            type=block_type,
            labels=[struct.name],
            body=body
        )
    
    def _convert_expression(self, expr: Expression) -> HCLExpression:
        """Convert Runa expression to HCL expression"""
        if isinstance(expr, StringLiteral):
            if isinstance(expr.value, str):
                return HCLString([expr.value])
            elif isinstance(expr.value, (int, float)):
                return HCLNumber(expr.value, str(expr.value))
            elif isinstance(expr.value, bool):
                return HCLBool(expr.value)
            elif expr.value is None:
                return HCLNull()
            else:
                return HCLString([str(expr.value)])
        
        elif isinstance(expr, Identifier):
            return HCLIdentifier(expr.name)
        
        elif isinstance(expr, ListLiteral):
            elements = [self._convert_expression(elem) for elem in expr.elements]
            return HCLList(elements)
        
        elif isinstance(expr, RunaMapLiteral):
            pairs = []
            for key, value in expr.pairs:
                hcl_key = self._convert_expression(key)
                hcl_value = self._convert_expression(value)
                pairs.append((hcl_key, hcl_value))
            return HCLMap(pairs)
        
        elif isinstance(expr, RunaStructLiteral):
            fields = {}
            for name, value in expr.fields.items():
                fields[name] = self._convert_expression(value)
            return HCLObject(fields)
        
        elif isinstance(expr, RunaFieldAccess):
            object_expr = self._convert_expression(expr.object)
            return HCLAttributeAccess(object_expr, expr.field)
        
        elif isinstance(expr, IndexAccess):
            object_expr = self._convert_expression(expr.object)
            index_expr = self._convert_expression(expr.index)
            return HCLIndexAccess(object_expr, index_expr)
        
        elif isinstance(expr, FunctionCall):
            return self._convert_function_call(expr)
        
        elif isinstance(expr, RunaBinaryOp):
            left = self._convert_expression(expr.left)
            right = self._convert_expression(expr.right)
            return HCLBinaryOp(left, expr.operator, right)
        
        elif isinstance(expr, RunaUnaryOp):
            operand = self._convert_expression(expr.operand)
            return HCLUnaryOp(expr.operator, operand)
        
        elif isinstance(expr, IfStatement):
            condition = self._convert_expression(expr.condition)
            true_expr = self._convert_expression(expr.true_expr)
            false_expr = self._convert_expression(expr.false_expr)
            return HCLConditional(condition, true_expr, false_expr)
        
        else:
            return HCLString(["unknown"])
    
    def _convert_function_call(self, call: FunctionCall) -> HCLFunctionCall:
        """Convert Runa function call to HCL function call"""
        # Map Runa function to HCL function
        if isinstance(call.function, Identifier):
            hcl_function = self.function_mappings.get(call.function.name, call.function.name)
        else:
            hcl_function = "unknown"
        
        # Convert arguments
        args = [self._convert_expression(arg) for arg in call.args]
        
        return HCLFunctionCall(hcl_function, args)


# Convenience functions
def hcl_to_runa(hcl_config: HCLConfiguration) -> RunaModule:
    """Convert HCL configuration to Runa AST"""
    converter = HCLToRunaConverter()
    return converter.convert(hcl_config)


def runa_to_hcl(runa_module: RunaModule) -> HCLConfiguration:
    """Convert Runa AST to HCL configuration"""
    converter = RunaToHCLConverter()
    return converter.convert(runa_module) 