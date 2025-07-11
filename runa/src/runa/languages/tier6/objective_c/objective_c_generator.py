#!/usr/bin/env python3
"""
Objective-C Code Generator

Comprehensive code generator for Objective-C language that produces clean, idiomatic code
from Objective-C AST nodes, following Apple coding conventions and best practices.

This generator handles:
- Message passing syntax: [object method:parameter]
- Interface and implementation declarations with proper formatting
- Protocols and categories with Apple style guidelines
- Properties with correct attribute formatting
- Blocks and closures with proper capture syntax
- Memory management constructs (ARC and manual)
- Foundation framework patterns and conventions
- Preprocessor directives and imports
- Proper indentation and code organization
"""

from typing import List, Dict, Optional, Any, Union
import re
from dataclasses import dataclass
from enum import Enum, auto

from ....core.base_components import BaseLanguageGenerator, LanguageInfo, GenerationError, LanguageTier
from .objective_c_ast import *


class ObjCFormattingStyle(Enum):
    """Objective-C code formatting styles."""
    APPLE = "apple"           # Apple's official style guide
    GOOGLE = "google"         # Google Objective-C style guide
    GNU = "gnu"              # GNU style formatting
    COMPACT = "compact"       # Compact formatting for small screens


@dataclass
class ObjCCodeStyle:
    """Objective-C code style configuration."""
    # Indentation
    indent_size: int = 4
    use_tabs: bool = False
    
    # Braces
    brace_style: str = "apple"  # "apple", "allman", "gnu"
    space_before_braces: bool = True
    
    # Spacing
    space_after_keywords: bool = True
    space_around_operators: bool = True
    space_after_comma: bool = True
    space_before_colon: bool = False
    space_after_colon: bool = True
    
    # Line breaks
    max_line_length: int = 120
    break_before_binary_operators: bool = False
    
    # Method formatting
    align_colons: bool = True
    space_before_method_braces: bool = True
    newline_before_method_braces: bool = False
    
    # Comments
    preserve_comments: bool = True
    generate_documentation: bool = True
    
    # Imports
    sort_imports: bool = True
    group_imports: bool = True
    
    # Naming conventions
    use_camel_case: bool = True
    prefix_instance_variables: bool = True
    ivar_prefix: str = "_"


class ObjCCodeGenerator(BaseLanguageGenerator):
    """Generates clean Objective-C code from AST nodes."""
    
    def __init__(self, style: ObjCCodeStyle = None):
        language_info = LanguageInfo(
            name="objective_c",
            tier=LanguageTier.TIER6,
            file_extensions=[".m", ".mm", ".h"],
            description="Objective-C code generator with Apple style guidelines"
        )
        super().__init__(language_info)
        
        self.style = style or ObjCCodeStyle()
        self.current_indent = 0
        self.output = []
        
        # Track context for better formatting
        self.in_interface = False
        self.in_implementation = False
        self.in_protocol = False
        self.in_method = False
        self.in_block = False
        
        # Foundation type mappings for better code generation
        self.foundation_literals = {
            'String': '@""',
            'Array': '@[]',
            'Dictionary': '@{}',
            'Number': '@0'
        }
    
    def generate(self, objc_ast: ObjCNode) -> str:
        """Generate Objective-C code from AST."""
        try:
            self.output = []
            self.current_indent = 0
            
            if isinstance(objc_ast, ObjCSourceUnit):
                self._generate_source_unit(objc_ast)
            elif isinstance(objc_ast, ObjCInterfaceDeclaration):
                self._generate_interface_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCImplementation):
                self._generate_implementation(objc_ast)
            elif isinstance(objc_ast, ObjCProtocolDeclaration):
                self._generate_protocol_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCMethodDeclaration):
                self._generate_method_declaration(objc_ast)
            elif isinstance(objc_ast, ObjCMethodImplementation):
                self._generate_method_implementation(objc_ast)
            elif isinstance(objc_ast, ObjCExpression):
                return self._generate_expression(objc_ast)
            else:
                raise GenerationError(f"Unsupported AST node type: {type(objc_ast)}", objc_ast)
            
            return self._finalize_output()
        
        except Exception as e:
            raise GenerationError(f"Failed to generate Objective-C code: {e}", objc_ast)
    
    def _generate_source_unit(self, source_unit: ObjCSourceUnit) -> None:
        """Generate complete source file."""
        # File header comment
        if self.style.generate_documentation:
            self._add_line("//")
            self._add_line("// Generated Objective-C code")
            self._add_line("//")
            self._add_line("")
        
        # Imports and preprocessor directives
        if source_unit.imports or source_unit.preprocessor_directives:
            self._generate_imports_and_preprocessor(source_unit)
            self._add_line("")
        
        # Forward declarations (if any interfaces are forward-declared)
        forward_declarations = [intf for intf in source_unit.interfaces if intf.is_forward_declaration]
        if forward_declarations:
            for intf in forward_declarations:
                self._add_line(f"@class {intf.name};")
            self._add_line("")
        
        # Protocol declarations
        for protocol in source_unit.protocols:
            self._generate_protocol_declaration(protocol)
            self._add_line("")
        
        # Interface declarations
        for interface in source_unit.interfaces:
            if not interface.is_forward_declaration:
                self._generate_interface_declaration(interface)
                self._add_line("")
        
        # Category interfaces
        for category in source_unit.categories:
            self._generate_category_interface(category)
            self._add_line("")
        
        # Class extensions
        for extension in source_unit.extensions:
            self._generate_class_extension(extension)
            self._add_line("")
        
        # Implementations
        for implementation in source_unit.implementations:
            self._generate_implementation(implementation)
            self._add_line("")
        
        # Category implementations
        for category_impl in source_unit.category_implementations:
            self._generate_category_implementation(category_impl)
            self._add_line("")
    
    def _generate_imports_and_preprocessor(self, source_unit: ObjCSourceUnit) -> None:
        """Generate imports and preprocessor directives."""
        # Group and sort imports if configured
        if self.style.group_imports:
            # System imports first
            system_imports = [imp for imp in source_unit.imports if imp.is_system_import]
            local_imports = [imp for imp in source_unit.imports if not imp.is_system_import]
            
            for imp in system_imports:
                self._generate_import_directive(imp)
            
            if system_imports and local_imports:
                self._add_line("")
            
            for imp in local_imports:
                self._generate_import_directive(imp)
        else:
            for imp in source_unit.imports:
                self._generate_import_directive(imp)
        
        # Preprocessor directives
        for directive in source_unit.preprocessor_directives:
            self._generate_preprocessor_directive(directive)
    
    def _generate_import_directive(self, import_dir: ObjCImportDirective) -> None:
        """Generate #import or @import directive."""
        if import_dir.is_framework_import:
            self._add_line(f"@import {import_dir.framework_name};")
        else:
            if import_dir.is_system_import:
                self._add_line(f"#import <{import_dir.path}>")
            else:
                self._add_line(f"#import \"{import_dir.path}\"")
    
    def _generate_preprocessor_directive(self, directive: ObjCPreprocessorDirective) -> None:
        """Generate preprocessor directive."""
        self._add_line(directive.content)
    
    def _generate_interface_declaration(self, interface: ObjCInterfaceDeclaration) -> None:
        """Generate @interface declaration."""
        self.in_interface = True
        
        # Build interface line
        interface_line = f"@interface {interface.name}"
        
        if interface.superclass:
            interface_line += f" : {interface.superclass}"
        
        if interface.protocols:
            protocols = ", ".join(interface.protocols)
            interface_line += f" <{protocols}>"
        
        self._add_line(interface_line)
        
        # Instance variables section
        if interface.instance_variables:
            self._add_line("{")
            self._indent()
            
            for ivar in interface.instance_variables:
                self._generate_ivar_declaration(ivar)
            
            self._dedent()
            self._add_line("}")
            self._add_line("")
        
        # Properties
        if interface.properties:
            for prop in interface.properties:
                self._generate_property_declaration(prop)
            self._add_line("")
        
        # Methods
        if interface.methods:
            for method in interface.methods:
                self._generate_method_declaration(method)
        
        self._add_line("@end")
        self.in_interface = False
    
    def _generate_implementation(self, implementation: ObjCImplementation) -> None:
        """Generate @implementation."""
        self.in_implementation = True
        
        self._add_line(f"@implementation {implementation.name}")
        self._add_line("")
        
        # Instance variables (if any)
        if implementation.instance_variables:
            self._add_line("{")
            self._indent()
            
            for ivar in implementation.instance_variables:
                self._generate_ivar_declaration(ivar)
            
            self._dedent()
            self._add_line("}")
            self._add_line("")
        
        # Property synthesis
        if implementation.properties:
            for prop in implementation.properties:
                self._generate_property_synthesis(prop)
            self._add_line("")
        
        # Method implementations
        if implementation.methods:
            for i, method in enumerate(implementation.methods):
                if i > 0:
                    self._add_line("")
                self._generate_method_implementation(method)
        
        self._add_line("")
        self._add_line("@end")
        self.in_implementation = False
    
    def _generate_protocol_declaration(self, protocol: ObjCProtocolDeclaration) -> None:
        """Generate @protocol declaration."""
        self.in_protocol = True
        
        protocol_line = f"@protocol {protocol.name}"
        
        if protocol.protocols:
            super_protocols = ", ".join(protocol.protocols)
            protocol_line += f" <{super_protocols}>"
        
        self._add_line(protocol_line)
        self._add_line("")
        
        # Required methods (default)
        if protocol.required_methods:
            self._add_line("@required")
            for method in protocol.required_methods:
                self._generate_method_declaration(method)
            self._add_line("")
        
        # Optional methods
        if protocol.optional_methods:
            self._add_line("@optional")
            for method in protocol.optional_methods:
                self._generate_method_declaration(method)
            self._add_line("")
        
        # Properties
        if protocol.properties:
            for prop in protocol.properties:
                self._generate_property_declaration(prop)
        
        self._add_line("@end")
        self.in_protocol = False
    
    def _generate_category_interface(self, category: ObjCCategoryInterface) -> None:
        """Generate category interface."""
        category_line = f"@interface {category.class_name} ({category.category_name})"
        
        if category.protocols:
            protocols = ", ".join(category.protocols)
            category_line += f" <{protocols}>"
        
        self._add_line(category_line)
        
        # Properties
        if category.properties:
            self._add_line("")
            for prop in category.properties:
                self._generate_property_declaration(prop)
        
        # Methods
        if category.methods:
            self._add_line("")
            for method in category.methods:
                self._generate_method_declaration(method)
        
        self._add_line("")
        self._add_line("@end")
    
    def _generate_category_implementation(self, category_impl: ObjCCategoryImplementation) -> None:
        """Generate category implementation."""
        self._add_line(f"@implementation {category_impl.class_name} ({category_impl.category_name})")
        
        if category_impl.methods:
            self._add_line("")
            for i, method in enumerate(category_impl.methods):
                if i > 0:
                    self._add_line("")
                self._generate_method_implementation(method)
        
        self._add_line("")
        self._add_line("@end")
    
    def _generate_class_extension(self, extension: ObjCClassExtension) -> None:
        """Generate class extension (anonymous category)."""
        self._add_line(f"@interface {extension.class_name} ()")
        
        # Instance variables
        if extension.instance_variables:
            self._add_line("{")
            self._indent()
            for ivar in extension.instance_variables:
                self._generate_ivar_declaration(ivar)
            self._dedent()
            self._add_line("}")
        
        # Properties
        if extension.properties:
            self._add_line("")
            for prop in extension.properties:
                self._generate_property_declaration(prop)
        
        # Methods
        if extension.methods:
            self._add_line("")
            for method in extension.methods:
                self._generate_method_declaration(method)
        
        self._add_line("")
        self._add_line("@end")
    
    def _generate_property_declaration(self, prop: ObjCPropertyDeclaration) -> None:
        """Generate @property declaration."""
        prop_line = "@property"
        
        # Attributes
        if prop.attributes:
            attr_strings = []
            for attr in prop.attributes:
                attr_strings.append(attr.value)
            
            # Add custom getter/setter names
            if prop.getter_name:
                attr_strings.append(f"getter={prop.getter_name}")
            if prop.setter_name:
                attr_strings.append(f"setter={prop.setter_name}")
            
            if attr_strings:
                prop_line += f" ({', '.join(attr_strings)})"
        
        # Type and name
        type_str = self._generate_type(prop.type_annotation)
        prop_line += f" {type_str} {prop.name};"
        
        self._add_line(prop_line)
    
    def _generate_property_synthesis(self, synthesis: ObjCPropertySynthesis) -> None:
        """Generate @synthesize or @dynamic."""
        if synthesis.is_dynamic:
            self._add_line(f"@dynamic {synthesis.property_name};")
        else:
            if synthesis.ivar_name:
                self._add_line(f"@synthesize {synthesis.property_name} = {synthesis.ivar_name};")
            else:
                self._add_line(f"@synthesize {synthesis.property_name};")
    
    def _generate_ivar_declaration(self, ivar: ObjCIvarDeclaration) -> None:
        """Generate instance variable declaration."""
        type_str = self._generate_type(ivar.type_annotation)
        line = f"{type_str} {ivar.name};"
        
        if ivar.initial_value:
            # Note: Objective-C doesn't support ivar initialization in declaration
            # This would need to be moved to init method
            pass
        
        self._add_line(line)
    
    def _generate_method_declaration(self, method: ObjCMethodDeclaration) -> None:
        """Generate method declaration."""
        method_line = self._build_method_signature(
            method.method_type,
            method.return_type,
            method.selector,
            method.parameters
        )
        
        self._add_line(f"{method_line};")
    
    def _generate_method_implementation(self, method: ObjCMethodImplementation) -> None:
        """Generate method implementation."""
        self.in_method = True
        
        method_line = self._build_method_signature(
            method.method_type,
            method.return_type,
            method.selector,
            method.parameters
        )
        
        if self.style.newline_before_method_braces:
            self._add_line(method_line)
            self._add_line("{")
        else:
            space = " " if self.style.space_before_method_braces else ""
            self._add_line(f"{method_line}{space}{{")
        
        # Method body
        if method.body:
            self._indent()
            for stmt in method.body:
                self._generate_statement(stmt)
            self._dedent()
        
        self._add_line("}")
        self.in_method = False
    
    def _build_method_signature(self, method_type: ObjCMethodType, return_type: ObjCType,
                               selector: ObjCSelector, parameters: List[ObjCParameter]) -> str:
        """Build method signature string."""
        # Method type (+ or -)
        signature = method_type.value
        
        # Return type
        if return_type:
            type_str = self._generate_type(return_type)
            signature += f"({type_str})"
        
        # Selector and parameters
        if not selector.parts:
            signature += "unknown"
        elif len(selector.parts) == 1 and not parameters:
            # Simple method with no parameters
            signature += selector.parts[0]
        else:
            # Method with parameters
            for i, part in enumerate(selector.parts):
                signature += part
                
                if i < len(parameters):
                    param = parameters[i]
                    type_str = self._generate_type(param.type_annotation)
                    signature += f":({type_str}){param.name}"
                    
                    # Add space before next part
                    if i < len(selector.parts) - 1:
                        signature += " "
                elif i < len(selector.parts) - 1:
                    signature += ":"
        
        return signature
    
    def _generate_statement(self, stmt: ObjCStatement) -> None:
        """Generate statement."""
        if isinstance(stmt, ObjCExpressionStatement):
            expr_str = self._generate_expression(stmt.expression)
            self._add_line(f"{expr_str};")
        elif isinstance(stmt, ObjCAutoreleasePool):
            self._generate_autorelease_pool(stmt)
        elif isinstance(stmt, ObjCSynchronizedStatement):
            self._generate_synchronized_statement(stmt)
        elif isinstance(stmt, ObjCTryCatchStatement):
            self._generate_try_catch_statement(stmt)
        else:
            # Generic statement fallback
            self._add_line("// Unknown statement")
    
    def _generate_autorelease_pool(self, pool: ObjCAutoreleasePool) -> None:
        """Generate @autoreleasepool block."""
        self._add_line("@autoreleasepool {")
        self._indent()
        
        for stmt in pool.body:
            self._generate_statement(stmt)
        
        self._dedent()
        self._add_line("}")
    
    def _generate_synchronized_statement(self, sync: ObjCSynchronizedStatement) -> None:
        """Generate @synchronized block."""
        expr_str = self._generate_expression(sync.expression)
        self._add_line(f"@synchronized({expr_str}) {{")
        self._indent()
        
        for stmt in sync.body:
            self._generate_statement(stmt)
        
        self._dedent()
        self._add_line("}")
    
    def _generate_try_catch_statement(self, try_stmt: ObjCTryCatchStatement) -> None:
        """Generate @try/@catch/@finally block."""
        self._add_line("@try {")
        self._indent()
        
        for stmt in try_stmt.try_body:
            self._generate_statement(stmt)
        
        self._dedent()
        self._add_line("}")
        
        # Catch clauses
        for catch in try_stmt.catch_clauses:
            type_str = self._generate_type(catch.exception_type) if catch.exception_type else "NSException"
            name = catch.exception_name or "exception"
            
            self._add_line(f"@catch ({type_str} *{name}) {{")
            self._indent()
            
            for stmt in catch.body:
                self._generate_statement(stmt)
            
            self._dedent()
            self._add_line("}")
        
        # Finally clause
        if try_stmt.finally_body:
            self._add_line("@finally {")
            self._indent()
            
            for stmt in try_stmt.finally_body:
                self._generate_statement(stmt)
            
            self._dedent()
            self._add_line("}")
    
    def _generate_expression(self, expr: ObjCExpression) -> str:
        """Generate expression."""
        if isinstance(expr, ObjCMessageExpression):
            return self._generate_message_expression(expr)
        elif isinstance(expr, ObjCBlockExpression):
            return self._generate_block_expression(expr)
        elif isinstance(expr, ObjCStringLiteral):
            if expr.is_nsstring:
                return f"@\"{expr.value}\""
            else:
                return f"\"{expr.value}\""
        elif isinstance(expr, ObjCNumberLiteral):
            if expr.is_nsnumber:
                return f"@{expr.value}"
            else:
                return str(expr.value)
        elif isinstance(expr, ObjCBoolLiteral):
            return "YES" if expr.value else "NO"
        elif isinstance(expr, ObjCNilExpression):
            return "nil"
        elif isinstance(expr, ObjCSelfExpression):
            return "self"
        elif isinstance(expr, ObjCSuperExpression):
            return "super"
        elif isinstance(expr, ObjCArrayLiteral):
            elements = [self._generate_expression(elem) for elem in expr.elements]
            return f"@[{', '.join(elements)}]"
        elif isinstance(expr, ObjCDictionaryLiteral):
            pairs = []
            for key, value in zip(expr.keys, expr.values):
                key_str = self._generate_expression(key)
                value_str = self._generate_expression(value)
                pairs.append(f"{key_str}: {value_str}")
            return f"@{{{', '.join(pairs)}}}"
        elif hasattr(expr, 'name'):
            return expr.name
        else:
            return "/* unknown expression */"
    
    def _generate_message_expression(self, msg: ObjCMessageExpression) -> str:
        """Generate message expression [receiver method:arg]."""
        receiver_str = self._generate_expression(msg.receiver) if msg.receiver else "nil"
        
        if not msg.arguments:
            # Simple message with no arguments
            selector_name = msg.selector.parts[0] if msg.selector.parts else "unknown"
            return f"[{receiver_str} {selector_name}]"
        
        # Message with arguments
        message_parts = [receiver_str]
        
        for i, (part, arg) in enumerate(zip(msg.selector.parts, msg.arguments)):
            if i == 0:
                message_parts.append(f" {part}:{self._generate_expression(arg.expression)}")
            else:
                message_parts.append(f" {part}:{self._generate_expression(arg.expression)}")
        
        return f"[{''.join(message_parts)}]"
    
    def _generate_block_expression(self, block: ObjCBlockExpression) -> str:
        """Generate block expression ^(params) { body }."""
        self.in_block = True
        
        block_str = "^"
        
        # Return type (if specified)
        if block.return_type:
            type_str = self._generate_type(block.return_type)
            block_str += f"{type_str} "
        
        # Parameters
        if block.parameters:
            param_strs = []
            for param in block.parameters:
                type_str = self._generate_type(param.type_annotation)
                param_strs.append(f"{type_str} {param.name}")
            block_str += f"({', '.join(param_strs)})"
        
        # Body
        if len(block.body) == 1 and not isinstance(block.body[0], ObjCBlock):
            # Single expression block
            stmt_str = self._generate_statement_inline(block.body[0])
            block_str += f" {{ {stmt_str} }}"
        else:
            # Multi-statement block
            block_str += " {\n"
            self._indent()
            
            for stmt in block.body:
                # Add indentation for each statement
                stmt_lines = self._generate_statement_to_lines(stmt)
                for line in stmt_lines:
                    block_str += self._get_indent() + line + "\n"
            
            self._dedent()
            block_str += self._get_indent() + "}"
        
        self.in_block = False
        return block_str
    
    def _generate_type(self, obj_type: Optional[ObjCType]) -> str:
        """Generate type annotation."""
        if not obj_type:
            return "id"
        
        if isinstance(obj_type, ObjCIdType):
            if obj_type.protocols:
                protocols = ", ".join(obj_type.protocols)
                return f"id<{protocols}>"
            return "id"
        elif isinstance(obj_type, ObjCInstanceType):
            return "instancetype"
        elif isinstance(obj_type, ObjCClassType):
            base = obj_type.class_name
            if obj_type.protocols:
                protocols = ", ".join(obj_type.protocols)
                return f"{base}<{protocols}>"
            return base
        elif isinstance(obj_type, ObjCPointerType):
            pointed = self._generate_type(obj_type.pointed_type)
            const = "const " if obj_type.is_const else ""
            return f"{const}{pointed} *"
        elif isinstance(obj_type, ObjCBlockType):
            return_type = self._generate_type(obj_type.return_type) if obj_type.return_type else "void"
            param_types = [self._generate_type(param) for param in obj_type.parameter_types]
            return f"{return_type} (^)({', '.join(param_types)})"
        else:
            return "id"
    
    def _generate_statement_inline(self, stmt: ObjCStatement) -> str:
        """Generate statement as inline string."""
        if isinstance(stmt, ObjCExpressionStatement):
            return self._generate_expression(stmt.expression)
        else:
            return "/* statement */"
    
    def _generate_statement_to_lines(self, stmt: ObjCStatement) -> List[str]:
        """Generate statement to list of lines."""
        # Save current output, generate statement, restore output
        saved_output = self.output
        saved_indent = self.current_indent
        
        self.output = []
        self.current_indent = 0
        
        self._generate_statement(stmt)
        
        lines = self.output
        self.output = saved_output
        self.current_indent = saved_indent
        
        return lines
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def _add_line(self, line: str = "") -> None:
        """Add line with proper indentation."""
        if line.strip():
            indented_line = self._get_indent() + line
        else:
            indented_line = ""
        self.output.append(indented_line)
    
    def _get_indent(self) -> str:
        """Get current indentation string."""
        if self.style.use_tabs:
            return "\t" * self.current_indent
        else:
            return " " * (self.current_indent * self.style.indent_size)
    
    def _indent(self) -> None:
        """Increase indentation level."""
        self.current_indent += 1
    
    def _dedent(self) -> None:
        """Decrease indentation level."""
        if self.current_indent > 0:
            self.current_indent -= 1
    
    def _finalize_output(self) -> str:
        """Finalize and return generated code."""
        # Remove trailing empty lines
        while self.output and not self.output[-1].strip():
            self.output.pop()
        
        # Join lines
        code = "\n".join(self.output)
        
        # Add final newline if not present
        if code and not code.endswith("\n"):
            code += "\n"
        
        return code
    
    def format_code(self, source_code: str) -> str:
        """Format existing Objective-C code."""
        # Basic formatting improvements
        lines = source_code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                formatted_lines.append("")
                continue
            
            # Adjust indentation for closing braces
            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
            
            # Add indented line
            if self.style.use_tabs:
                indent = "\t" * indent_level
            else:
                indent = " " * (indent_level * self.style.indent_size)
            
            formatted_lines.append(indent + stripped)
            
            # Adjust indentation for opening braces
            if stripped.endswith('{'):
                indent_level += 1
        
        return "\n".join(formatted_lines)


# Factory functions
def generate_objective_c(objc_ast: ObjCNode, style: ObjCCodeStyle = None) -> str:
    """Generate Objective-C code from AST."""
    generator = ObjCCodeGenerator(style)
    return generator.generate(objc_ast)


def create_apple_style() -> ObjCCodeStyle:
    """Create Apple-style code formatting configuration."""
    return ObjCCodeStyle(
        indent_size=4,
        use_tabs=False,
        brace_style="apple",
        space_before_braces=True,
        align_colons=True,
        max_line_length=120,
        use_camel_case=True,
        prefix_instance_variables=True
    )


def create_google_style() -> ObjCCodeStyle:
    """Create Google-style code formatting configuration."""
    return ObjCCodeStyle(
        indent_size=2,
        use_tabs=False,
        brace_style="google",
        space_before_braces=True,
        align_colons=False,
        max_line_length=100,
        use_camel_case=True,
        prefix_instance_variables=True
    )


def create_compact_style() -> ObjCCodeStyle:
    """Create compact code formatting configuration."""
    return ObjCCodeStyle(
        indent_size=2,
        use_tabs=False,
        brace_style="compact",
        space_before_braces=False,
        align_colons=False,
        max_line_length=80,
        use_camel_case=True,
        prefix_instance_variables=False
    ) 