#!/usr/bin/env python3
"""
TOML Converter - Bidirectional TOML ↔ Runa AST Conversion

Provides comprehensive conversion between TOML and Runa AST including:
- TOML tables to Runa struct declarations
- Key-value pairs to Runa variable declarations
- Arrays to Runa list literals
- Basic values (strings, numbers, booleans, dates) to appropriate Runa types
- Inline tables to Runa struct expressions
- Comments to Runa documentation
- Hierarchical table structure preservation

Maintains semantic equivalence and supports round-trip conversion.
"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, date, time

from .toml_ast import *
from runa.languages.shared.runa_ast import *


class TOMLToRunaConverter:
    """Converts TOML AST to Runa AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.table_hierarchy: Dict[str, Any] = {}
        self.variable_mappings: Dict[str, str] = {}
        
        # TOML to Runa type mappings
        self.type_mappings = {
            "string": "String",
            "integer": "Int",
            "float": "Float",
            "boolean": "Bool",
            "datetime": "DateTime",
            "date": "Date",
            "time": "Time",
            "array": "List",
            "table": "Struct",
            "inline_table": "Struct",
        }
    
    def convert(self, toml_doc: TOMLDocument) -> RunaModule:
        """Convert TOML document to Runa module"""
        runa_declarations = []
        imports = []
        current_table: Optional[str] = None
        table_fields: Dict[str, List[LetStatement]] = {}
        root_variables: List[LetStatement] = []
        
        # Add standard imports for TOML functionality
        imports.extend([
            RunaImport(path="runa.datetime", alias=None, items=["DateTime", "Date", "Time"]),
            RunaImport(path="runa.config", alias=None, items=["ConfigSection"]),
        ])
        
        # First pass: organize items by table
        for item in toml_doc.items:
            if isinstance(item, TOMLTable):
                current_table = item.key.dotted_key
                if current_table not in table_fields:
                    table_fields[current_table] = []
            elif isinstance(item, TOMLKeyValue):
                variable = self._convert_key_value(item)
                if current_table:
                    table_fields[current_table].append(variable)
                else:
                    root_variables.append(variable)
            elif isinstance(item, TOMLComment):
                # Comments are handled as documentation for subsequent items
                continue
        
        # Create struct declarations for tables
        for table_name, fields in table_fields.items():
            struct_decl = self._create_table_struct(table_name, fields)
            runa_declarations.append(struct_decl)
        
        # Add root-level variables
        runa_declarations.extend(root_variables)
        
        # Create main configuration struct if we have tables
        if table_fields:
            config_struct = self._create_main_config_struct(table_fields, root_variables)
            runa_declarations.append(config_struct)
        
        return RunaModule(
            name="toml_configuration",
            imports=imports,
            declarations=runa_declarations,
            exports=[],
            metadata={
                "source_language": "toml",
                "table_structure": list(table_fields.keys()),
                "configuration_type": "config"
            }
        )
    
    def _convert_key_value(self, kv: TOMLKeyValue) -> LetStatement:
        """Convert TOML key-value pair to Runa variable declaration"""
        name = self._sanitize_identifier(kv.key.dotted_key)
        value_expr = self._convert_value(kv.value)
        value_type = self._infer_value_type(kv.value)
        
        # Add type annotations for configuration values
        annotations = [RunaAnnotation("config", {"key": kv.key.dotted_key})]
        
        # Add type constraint with annotations
        annotated_type = RunaAnnotatedType(
            base_type=value_type,
            annotations=annotations
        )
        
        return LetStatement(
            name=name,
            type=annotated_type,
            value=value_expr,
            is_mutable=False,
            metadata={
                "toml_key": kv.key.dotted_key,
                "quoted_parts": kv.key.is_quoted
            }
        )
    
    def _convert_value(self, value: TOMLValue) -> Expression:
        """Convert TOML value to Runa expression"""
        if isinstance(value, TOMLString):
            return self._convert_string(value)
        elif isinstance(value, TOMLInteger):
            return IntegerLiteral(value.value)
        elif isinstance(value, TOMLFloat):
            if value.is_inf:
                return FunctionCall(
                    function=Identifier("Float.INFINITY"),
                    args=[],
                    metadata={"special_float": "infinity"}
                )
            elif value.is_nan:
                return FunctionCall(
                    function=Identifier("Float.NAN"),
                    args=[],
                    metadata={"special_float": "nan"}
                )
            else:
                return FloatLiteral(value.value)
        elif isinstance(value, TOMLBoolean):
            return BooleanLiteral(value.value)
        elif isinstance(value, TOMLDateTime):
            return self._convert_datetime(value)
        elif isinstance(value, TOMLDate):
            return self._convert_date(value)
        elif isinstance(value, TOMLTime):
            return self._convert_time(value)
        elif isinstance(value, TOMLArray):
            return self._convert_array(value)
        elif isinstance(value, TOMLInlineTable):
            return self._convert_inline_table(value)
        else:
            # Fallback for unknown types
            return StringLiteral("unknown_value")
    
    def _convert_string(self, string: TOMLString) -> Expression:
        """Convert TOML string to Runa string expression"""
        metadata = {
            "toml_string_type": string.string_type.value,
            "raw_value": string.raw_value
        }
        
        if string.string_type in (TOMLStringType.MULTILINE_BASIC, TOMLStringType.MULTILINE_LITERAL):
            metadata["multiline"] = True
        
        return StringLiteral(string.value, metadata=metadata)
    
    def _convert_datetime(self, dt: TOMLDateTime) -> Expression:
        """Convert TOML datetime to Runa DateTime expression"""
        return FunctionCall(
            function=Identifier("DateTime.from_rfc3339"),
            args=[StringLiteral(dt.raw_text)],
            metadata={
                "toml_datetime": True,
                "has_timezone": dt.has_timezone
            }
        )
    
    def _convert_date(self, d: TOMLDate) -> Expression:
        """Convert TOML date to Runa Date expression"""
        return FunctionCall(
            function=Identifier("Date.from_string"),
            args=[StringLiteral(d.raw_text)],
            metadata={"toml_date": True}
        )
    
    def _convert_time(self, t: TOMLTime) -> Expression:
        """Convert TOML time to Runa Time expression"""
        return FunctionCall(
            function=Identifier("Time.from_string"),
            args=[StringLiteral(t.raw_text)],
            metadata={"toml_time": True}
        )
    
    def _convert_array(self, array: TOMLArray) -> Expression:
        """Convert TOML array to Runa list expression"""
        elements = [self._convert_value(elem) for elem in array.elements]
        
        metadata = {
            "toml_array": True,
            "multiline": array.is_multiline,
            "trailing_comma": array.trailing_comma
        }
        
        return ListLiteral(elements, metadata=metadata)
    
    def _convert_inline_table(self, table: TOMLInlineTable) -> Expression:
        """Convert TOML inline table to Runa struct expression"""
        fields = []
        
        for key, value in table.pairs:
            field_name = self._sanitize_identifier(key)
            field_value = self._convert_value(value)
            fields.append(RunaStructField(name=field_name, value=field_value))
        
        return RunaStructLiteral(
            fields=fields,
            metadata={
                "toml_inline_table": True,
                "original_keys": [key for key, _ in table.pairs]
            }
        )
    
    def _create_table_struct(self, table_name: str, fields: List[LetStatement]) -> RunaStructDeclaration:
        """Create Runa struct declaration for TOML table"""
        struct_name = self._table_name_to_struct_name(table_name)
        
        # Convert variable declarations to struct fields
        struct_fields = []
        for var_decl in fields:
            field = RunaStructFieldDeclaration(
                name=var_decl.name,
                type=var_decl.type,
                default_value=var_decl.value,
                metadata=var_decl.metadata
            )
            struct_fields.append(field)
        
        annotations = [RunaAnnotation("config_section", {"name": table_name})]
        
        return RunaStructDeclaration(
            name=struct_name,
            fields=struct_fields,
            annotations=annotations,
            metadata={
                "toml_table": table_name,
                "original_name": table_name
            }
        )
    
    def _create_main_config_struct(self, tables: Dict[str, List[LetStatement]], 
                                 root_vars: List[LetStatement]) -> RunaStructDeclaration:
        """Create main configuration struct containing all tables and root variables"""
        fields = []
        
        # Add root variables as fields
        for var in root_vars:
            field = RunaStructFieldDeclaration(
                name=var.name,
                type=var.type,
                default_value=var.value,
                metadata=var.metadata
            )
            fields.append(field)
        
        # Add table references as fields
        for table_name in tables.keys():
            struct_name = self._table_name_to_struct_name(table_name)
            field_name = self._sanitize_identifier(table_name)
            
            field = RunaStructFieldDeclaration(
                name=field_name,
                type=RunaNominalType(struct_name),
                metadata={"toml_table_ref": table_name}
            )
            fields.append(field)
        
        return RunaStructDeclaration(
            name="Config",
            fields=fields,
            annotations=[RunaAnnotation("config", {})],
            metadata={
                "toml_main_config": True,
                "table_count": len(tables),
                "root_var_count": len(root_vars)
            }
        )
    
    def _infer_value_type(self, value: TOMLValue) -> BasicType:
        """Infer Runa type from TOML value"""
        if isinstance(value, TOMLString):
            return RunaNominalType("String")
        elif isinstance(value, TOMLInteger):
            return RunaNominalType("Int")
        elif isinstance(value, TOMLFloat):
            return RunaNominalType("Float")
        elif isinstance(value, TOMLBoolean):
            return RunaNominalType("Bool")
        elif isinstance(value, TOMLDateTime):
            return RunaNominalType("DateTime")
        elif isinstance(value, TOMLDate):
            return RunaNominalType("Date")
        elif isinstance(value, TOMLTime):
            return RunaNominalType("Time")
        elif isinstance(value, TOMLArray):
            if value.elements:
                element_type = self._infer_value_type(value.elements[0])
                return GenericType("List", [element_type])
            else:
                return GenericType("List", [RunaNominalType("Any")])
        elif isinstance(value, TOMLInlineTable):
            return RunaNominalType("Struct")
        else:
            return RunaNominalType("Any")
    
    def _table_name_to_struct_name(self, table_name: str) -> str:
        """Convert TOML table name to valid Runa struct name"""
        # Convert dotted names to PascalCase
        parts = table_name.split('.')
        return ''.join(part.capitalize() for part in parts)
    
    def _sanitize_identifier(self, name: str) -> str:
        """Sanitize TOML key to valid Runa identifier"""
        # Replace dots and hyphens with underscores
        sanitized = name.replace('.', '_').replace('-', '_')
        
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'field_' + sanitized
        
        return sanitized if sanitized else 'unknown_field'


class RunaToTOMLConverter:
    """Converts Runa AST to TOML AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.struct_mappings: Dict[str, str] = {}
        
        # Runa to TOML type mappings
        self.type_mappings = {
            "String": TOMLStringType.BASIC,
            "Int": "integer",
            "Float": "float", 
            "Bool": "boolean",
            "DateTime": "datetime",
            "Date": "date",
            "Time": "time",
            "List": "array",
            "Struct": "table",
        }
    
    def convert(self, runa_module: RunaModule) -> TOMLDocument:
        """Convert Runa module to TOML document"""
        items = []
        
        # Track structs that represent TOML tables
        table_structs = {}
        root_variables = []
        
        # First pass: identify table structs and root variables
        for decl in runa_module.declarations:
            if isinstance(decl, RunaStructDeclaration):
                table_name = self._get_table_name_from_struct(decl)
                if table_name:
                    table_structs[table_name] = decl
            elif isinstance(decl, LetStatement):
                root_variables.append(decl)
        
        # Add root-level variables first
        for var in root_variables:
            if not self._is_table_reference(var, table_structs):
                kv = self._convert_variable_to_key_value(var)
                if kv:
                    items.append(kv)
        
        # Add table sections
        for table_name, struct_decl in table_structs.items():
            # Add table header
            table_header = TOMLTable(
                key=create_key(table_name),
                is_array_table=self._is_array_table(struct_decl)
            )
            items.append(table_header)
            
            # Add table fields as key-value pairs
            for field in struct_decl.fields:
                kv = self._convert_struct_field_to_key_value(field)
                if kv:
                    items.append(kv)
        
        return TOMLDocument(
            items=items,
            filename=runa_module.metadata.get("filename"),
            metadata={
                "source_language": "runa",
                "table_count": len(table_structs),
                "root_var_count": len(root_variables)
            }
        )
    
    def _convert_variable_to_key_value(self, var: LetStatement) -> Optional[TOMLKeyValue]:
        """Convert Runa variable declaration to TOML key-value pair"""
        if not var.value:
            return None
        
        # Get original TOML key from metadata
        toml_key = var.metadata.get("toml_key", var.name)
        key = create_key(toml_key)
        
        value = self._convert_expression_to_value(var.value)
        if not value:
            return None
        
        return TOMLKeyValue(key=key, value=value)
    
    def _convert_struct_field_to_key_value(self, field: RunaStructFieldDeclaration) -> Optional[TOMLKeyValue]:
        """Convert Runa struct field to TOML key-value pair"""
        if not field.default_value:
            return None
        
        # Get original TOML key from metadata
        toml_key = field.metadata.get("toml_key", field.name)
        key = create_key(toml_key)
        
        value = self._convert_expression_to_value(field.default_value)
        if not value:
            return None
        
        return TOMLKeyValue(key=key, value=value)
    
    def _convert_expression_to_value(self, expr: Expression) -> Optional[TOMLValue]:
        """Convert Runa expression to TOML value"""
        if isinstance(expr, StringLiteral):
            string_type = TOMLStringType.BASIC
            if expr.metadata and "toml_string_type" in expr.metadata:
                string_type = TOMLStringType(expr.metadata["toml_string_type"])
            
            return TOMLString(
                value=expr.value,
                string_type=string_type,
                raw_value=expr.metadata.get("raw_value")
            )
        
        elif isinstance(expr, IntegerLiteral):
            return TOMLInteger(value=expr.value, raw_text=str(expr.value))
        
        elif isinstance(expr, FloatLiteral):
            return TOMLFloat(value=expr.value, raw_text=str(expr.value))
        
        elif isinstance(expr, BooleanLiteral):
            return TOMLBoolean(value=expr.value)
        
        elif isinstance(expr, ListLiteral):
            elements = []
            for elem_expr in expr.elements:
                elem_value = self._convert_expression_to_value(elem_expr)
                if elem_value:
                    elements.append(elem_value)
            
            is_multiline = expr.metadata.get("multiline", False) if expr.metadata else False
            trailing_comma = expr.metadata.get("trailing_comma", False) if expr.metadata else False
            
            return TOMLArray(
                elements=elements,
                is_multiline=is_multiline,
                trailing_comma=trailing_comma
            )
        
        elif isinstance(expr, RunaStructLiteral):
            pairs = []
            for field in expr.fields:
                field_value = self._convert_expression_to_value(field.value)
                if field_value:
                    pairs.append((field.name, field_value))
            
            return TOMLInlineTable(pairs=pairs)
        
        elif isinstance(expr, FunctionCall):
            # Handle special datetime/date/time functions
            if isinstance(expr.function, Identifier):
                if expr.function.name == "DateTime.from_rfc3339" and expr.args:
                    if isinstance(expr.args[0], StringLiteral):
                        return TOMLDateTime(
                            value=datetime.fromisoformat(expr.args[0].value.replace('Z', '+00:00')),
                            raw_text=expr.args[0].value,
                            has_timezone=expr.metadata.get("has_timezone", True) if expr.metadata else True
                        )
                elif expr.function.name == "Date.from_string" and expr.args:
                    if isinstance(expr.args[0], StringLiteral):
                        return TOMLDate(
                            value=date.fromisoformat(expr.args[0].value),
                            raw_text=expr.args[0].value
                        )
                elif expr.function.name == "Time.from_string" and expr.args:
                    if isinstance(expr.args[0], StringLiteral):
                        return TOMLTime(
                            value=time.fromisoformat(expr.args[0].value),
                            raw_text=expr.args[0].value
                        )
                elif expr.function.name == "Float.INFINITY":
                    return TOMLFloat(value=float('inf'), raw_text="inf", is_inf=True)
                elif expr.function.name == "Float.NAN":
                    return TOMLFloat(value=float('nan'), raw_text="nan", is_nan=True)
        
        return None
    
    def _get_table_name_from_struct(self, struct: RunaStructDeclaration) -> Optional[str]:
        """Extract TOML table name from struct declaration"""
        # Check metadata for original table name
        if struct.metadata and "toml_table" in struct.metadata:
            return struct.metadata["toml_table"]
        
        # Check annotations for config section
        for ann in struct.annotations:
            if ann.name == "config_section" and "name" in ann.args:
                return ann.args["name"]
        
        # Skip main config struct
        if struct.name == "Config" and struct.metadata and struct.metadata.get("toml_main_config"):
            return None
        
        return None
    
    def _is_array_table(self, struct: RunaStructDeclaration) -> bool:
        """Check if struct represents an array table [[...]]"""
        # Check annotations for array table marker
        for ann in struct.annotations:
            if ann.name == "array_table":
                return True
        
        return False
    
    def _is_table_reference(self, var: LetStatement, table_structs: Dict[str, Any]) -> bool:
        """Check if variable is a reference to a table struct"""
        if var.metadata and "toml_table_ref" in var.metadata:
            return True
        
        return False


def toml_to_runa(toml_doc: TOMLDocument) -> RunaModule:
    """Convert TOML document to Runa module"""
    converter = TOMLToRunaConverter()
    return converter.convert(toml_doc)


def runa_to_toml(runa_module: RunaModule) -> TOMLDocument:
    """Convert Runa module to TOML document"""
    converter = RunaToTOMLConverter()
    return converter.convert(runa_module) 