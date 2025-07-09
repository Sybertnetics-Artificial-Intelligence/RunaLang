#!/usr/bin/env python3
"""
Java Code Generator

Generates clean, readable Java code from Java AST with support for
modern Java features (Java 8-21) and configurable code styles.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum, auto
import re

from .java_ast import *


class JavaBraceStyle(Enum):
    """Java brace placement styles."""
    SAME_LINE = auto()      # K&R style: if (condition) {
    NEXT_LINE = auto()      # Allman style: if (condition)\n{
    NEXT_LINE_INDENT = auto() # GNU style: if (condition)\n  {


class JavaDocStyle(Enum):
    """Java documentation styles."""
    JAVADOC = auto()        # /** ... */
    BLOCK = auto()          # /* ... */
    LINE = auto()           # // ...


@dataclass
class JavaCodeStyle:
    """Java code formatting configuration."""
    
    # Indentation
    indent_size: int = 4
    use_spaces: bool = True
    tab_size: int = 4
    continuation_indent: int = 8
    
    # Braces
    brace_style: JavaBraceStyle = JavaBraceStyle.SAME_LINE
    empty_block_style: str = "same_line"  # "same_line" or "next_line"
    
    # Spacing
    space_before_parentheses: bool = True
    space_after_comma: bool = True
    space_around_operators: bool = True
    space_before_colon: bool = True
    space_after_colon: bool = True
    space_before_question: bool = True
    space_after_question: bool = True
    
    # Line breaks
    max_line_length: int = 120
    break_before_operators: bool = False
    break_after_operators: bool = True
    keep_simple_blocks_in_one_line: bool = False
    keep_simple_methods_in_one_line: bool = False
    
    # Blank lines
    blank_lines_around_class: int = 1
    blank_lines_around_method: int = 1
    blank_lines_around_field: int = 0
    blank_lines_before_closing_brace: int = 0
    
    # Imports
    import_layout: List[str] = None
    group_imports: bool = True
    sort_imports: bool = True
    
    # Comments
    doc_comment_style: JavaDocStyle = JavaDocStyle.JAVADOC
    line_comment_at_first_column: bool = False
    
    # Java-specific
    use_fully_qualified_names: bool = False
    prefer_diamond_operator: bool = True
    use_var_for_local_variables: bool = False
    use_final_for_parameters: bool = False
    use_final_for_local_variables: bool = False
    add_override_annotation: bool = True
    
    # Modern Java features
    use_lambda_expressions: bool = True
    use_method_references: bool = True
    use_stream_api: bool = True
    use_optional: bool = True
    use_text_blocks: bool = True
    use_switch_expressions: bool = True
    use_pattern_matching: bool = True
    use_records: bool = True
    use_sealed_classes: bool = True
    
    def __post_init__(self):
        if self.import_layout is None:
            self.import_layout = [
                "java.**",
                "javax.**",
                "",
                "org.**",
                "com.**",
                "",
                "all_other_imports",
                "",
                "static_imports"
            ]


class JavaCodeGenerator:
    """Java code generator with configurable styling."""
    
    def __init__(self, style: Optional[JavaCodeStyle] = None):
        self.style = style or JavaCodeStyle()
        self.indent_level = 0
        self.imports = set()
        self.static_imports = set()
        self.current_package = ""
        self.suppress_semicolon = False
        
    def generate(self, ast: JavaCompilationUnit) -> str:
        """Generate Java code from AST."""
        self.indent_level = 0
        self.imports.clear()
        self.static_imports.clear()
        self.current_package = ""
        
        lines = []
        
        # Package declaration
        if ast.package_declaration:
            lines.append(self._generate_package_declaration(ast.package_declaration))
            lines.append("")
        
        # Import declarations
        if ast.import_declarations:
            import_lines = self._generate_import_declarations(ast.import_declarations)
            lines.extend(import_lines)
            if import_lines:
                lines.append("")
        
        # Type declarations
        for i, type_decl in enumerate(ast.type_declarations):
            if i > 0:
                lines.extend([""] * self.style.blank_lines_around_class)
            lines.append(self._generate_type_declaration(type_decl))
        
        # Module declaration (Java 9+)
        if ast.module_declaration:
            if ast.type_declarations:
                lines.append("")
            lines.append(self._generate_module_declaration(ast.module_declaration))
        
        # Join lines and clean up
        code = "\n".join(lines)
        return self._clean_up_code(code)
    
    def _generate_package_declaration(self, package_decl: JavaPackageDeclaration) -> str:
        """Generate package declaration."""
        package_name = self._generate_expression(package_decl.name)
        self.current_package = package_name
        
        result = f"package {package_name};"
        
        # Add annotations if present
        if package_decl.annotations:
            annotations = [self._generate_annotation(ann) for ann in package_decl.annotations]
            result = "\n".join(annotations) + "\n" + result
        
        return result
    
    def _generate_import_declarations(self, imports: List[JavaImportDeclaration]) -> List[str]:
        """Generate import declarations with proper grouping."""
        import_groups = {"java": [], "javax": [], "org": [], "com": [], "other": [], "static": []}
        
        for import_decl in imports:
            import_name = self._generate_expression(import_decl.name)
            
            if import_decl.is_on_demand:
                import_name += ".*"
            
            if import_decl.is_static:
                import_line = f"import static {import_name};"
                import_groups["static"].append(import_line)
            else:
                import_line = f"import {import_name};"
                
                if import_name.startswith("java."):
                    import_groups["java"].append(import_line)
                elif import_name.startswith("javax."):
                    import_groups["javax"].append(import_line)
                elif import_name.startswith("org."):
                    import_groups["org"].append(import_line)
                elif import_name.startswith("com."):
                    import_groups["com"].append(import_line)
                else:
                    import_groups["other"].append(import_line)
        
        # Sort imports within groups
        if self.style.sort_imports:
            for group in import_groups.values():
                group.sort()
        
        # Generate final import list
        lines = []
        groups_to_process = ["java", "javax", "org", "com", "other", "static"]
        
        for group_name in groups_to_process:
            group = import_groups[group_name]
            if group:
                if lines:  # Add blank line between groups
                    lines.append("")
                lines.extend(group)
        
        return lines
    
    def _generate_type_declaration(self, type_decl: JavaTypeDeclaration) -> str:
        """Generate type declaration."""
        if isinstance(type_decl, JavaClassDeclaration):
            return self._generate_class_declaration(type_decl)
        elif isinstance(type_decl, JavaInterfaceDeclaration):
            return self._generate_interface_declaration(type_decl)
        elif isinstance(type_decl, JavaEnumDeclaration):
            return self._generate_enum_declaration(type_decl)
        elif isinstance(type_decl, JavaRecordDeclaration):
            return self._generate_record_declaration(type_decl)
        elif isinstance(type_decl, JavaAnnotationDeclaration):
            return self._generate_annotation_declaration(type_decl)
        else:
            return f"// Unknown type declaration: {type(type_decl)}"
    
    def _generate_class_declaration(self, class_decl: JavaClassDeclaration) -> str:
        """Generate class declaration."""
        lines = []
        
        # Documentation
        if class_decl.javadoc:
            lines.append(self._generate_javadoc(class_decl.javadoc))
        
        # Annotations
        for annotation in class_decl.annotations:
            lines.append(self._generate_annotation(annotation))
        
        # Class signature
        signature_parts = []
        
        # Modifiers
        if class_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in class_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # Class keyword
        signature_parts.append("class")
        
        # Class name
        signature_parts.append(class_decl.name)
        
        # Type parameters
        if class_decl.type_parameters:
            type_params = [self._generate_type_parameter(tp) for tp in class_decl.type_parameters]
            signature_parts.append(f"<{', '.join(type_params)}>")
        
        # Extends clause
        if class_decl.superclass:
            signature_parts.append("extends")
            signature_parts.append(self._generate_type(class_decl.superclass))
        
        # Implements clause
        if class_decl.interfaces:
            signature_parts.append("implements")
            interfaces = [self._generate_type(iface) for iface in class_decl.interfaces]
            signature_parts.append(", ".join(interfaces))
        
        # Permits clause (Java 17+)
        if hasattr(class_decl, 'permits') and class_decl.permits:
            signature_parts.append("permits")
            permits = [self._generate_type(permit) for permit in class_decl.permits]
            signature_parts.append(", ".join(permits))
        
        # Build signature line
        signature = " ".join(signature_parts)
        
        # Handle line length
        if len(signature) > self.style.max_line_length:
            # Break into multiple lines
            lines.append(signature_parts[0])  # modifiers and class keyword
            self.indent_level += 1
            if class_decl.type_parameters:
                lines.append(self._indent() + f"<{', '.join(type_params)}>")
            if class_decl.superclass:
                lines.append(self._indent() + f"extends {self._generate_type(class_decl.superclass)}")
            if class_decl.interfaces:
                lines.append(self._indent() + f"implements {', '.join(interfaces)}")
            if hasattr(class_decl, 'permits') and class_decl.permits:
                lines.append(self._indent() + f"permits {', '.join(permits)}")
            self.indent_level -= 1
        else:
            lines.append(signature)
        
        # Opening brace
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines[-1] += " {"
        else:
            lines.append("{")
        
        # Class body
        self.indent_level += 1
        body_lines = self._generate_class_body(class_decl.body)
        if body_lines:
            lines.extend(body_lines)
        self.indent_level -= 1
        
        # Closing brace
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_interface_declaration(self, interface_decl: JavaInterfaceDeclaration) -> str:
        """Generate interface declaration."""
        lines = []
        
        # Documentation
        if interface_decl.javadoc:
            lines.append(self._generate_javadoc(interface_decl.javadoc))
        
        # Annotations
        for annotation in interface_decl.annotations:
            lines.append(self._generate_annotation(annotation))
        
        # Interface signature
        signature_parts = []
        
        # Modifiers
        if interface_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in interface_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # Interface keyword
        signature_parts.append("interface")
        
        # Interface name
        signature_parts.append(interface_decl.name)
        
        # Type parameters
        if interface_decl.type_parameters:
            type_params = [self._generate_type_parameter(tp) for tp in interface_decl.type_parameters]
            signature_parts.append(f"<{', '.join(type_params)}>")
        
        # Extends clause
        if interface_decl.extends:
            signature_parts.append("extends")
            extends = [self._generate_type(ext) for ext in interface_decl.extends]
            signature_parts.append(", ".join(extends))
        
        # Permits clause (Java 17+)
        if hasattr(interface_decl, 'permits') and interface_decl.permits:
            signature_parts.append("permits")
            permits = [self._generate_type(permit) for permit in interface_decl.permits]
            signature_parts.append(", ".join(permits))
        
        signature = " ".join(signature_parts)
        lines.append(signature)
        
        # Opening brace
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines[-1] += " {"
        else:
            lines.append("{")
        
        # Interface body
        self.indent_level += 1
        body_lines = self._generate_interface_body(interface_decl.body)
        if body_lines:
            lines.extend(body_lines)
        self.indent_level -= 1
        
        # Closing brace
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_enum_declaration(self, enum_decl: JavaEnumDeclaration) -> str:
        """Generate enum declaration."""
        lines = []
        
        # Documentation
        if enum_decl.javadoc:
            lines.append(self._generate_javadoc(enum_decl.javadoc))
        
        # Annotations
        for annotation in enum_decl.annotations:
            lines.append(self._generate_annotation(annotation))
        
        # Enum signature
        signature_parts = []
        
        # Modifiers
        if enum_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in enum_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # Enum keyword
        signature_parts.append("enum")
        
        # Enum name
        signature_parts.append(enum_decl.name)
        
        # Implements clause
        if enum_decl.interfaces:
            signature_parts.append("implements")
            interfaces = [self._generate_type(iface) for iface in enum_decl.interfaces]
            signature_parts.append(", ".join(interfaces))
        
        signature = " ".join(signature_parts)
        lines.append(signature)
        
        # Opening brace
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines[-1] += " {"
        else:
            lines.append("{")
        
        # Enum body
        self.indent_level += 1
        
        # Enum constants
        if enum_decl.constants:
            constant_lines = []
            for i, constant in enumerate(enum_decl.constants):
                constant_line = self._indent() + self._generate_enum_constant(constant)
                if i < len(enum_decl.constants) - 1:
                    constant_line += ","
                constant_lines.append(constant_line)
            lines.extend(constant_lines)
            
            # Add semicolon if there are other members
            if enum_decl.body:
                lines.append(self._indent() + ";")
        
        # Other members
        if enum_decl.body:
            if enum_decl.constants:
                lines.append("")
            body_lines = self._generate_class_body(enum_decl.body)
            lines.extend(body_lines)
        
        self.indent_level -= 1
        
        # Closing brace
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_record_declaration(self, record_decl: JavaRecordDeclaration) -> str:
        """Generate record declaration (Java 14+)."""
        lines = []
        
        # Documentation
        if record_decl.javadoc:
            lines.append(self._generate_javadoc(record_decl.javadoc))
        
        # Annotations
        for annotation in record_decl.annotations:
            lines.append(self._generate_annotation(annotation))
        
        # Record signature
        signature_parts = []
        
        # Modifiers
        if record_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in record_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # Record keyword
        signature_parts.append("record")
        
        # Record name
        signature_parts.append(record_decl.name)
        
        # Type parameters
        if record_decl.type_parameters:
            type_params = [self._generate_type_parameter(tp) for tp in record_decl.type_parameters]
            signature_parts.append(f"<{', '.join(type_params)}>")
        
        # Component list
        if record_decl.components:
            components = [self._generate_record_component(comp) for comp in record_decl.components]
            signature_parts.append(f"({', '.join(components)})")
        else:
            signature_parts.append("()")
        
        # Implements clause
        if record_decl.interfaces:
            signature_parts.append("implements")
            interfaces = [self._generate_type(iface) for iface in record_decl.interfaces]
            signature_parts.append(", ".join(interfaces))
        
        signature = " ".join(signature_parts)
        lines.append(signature)
        
        # Opening brace
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines[-1] += " {"
        else:
            lines.append("{")
        
        # Record body
        self.indent_level += 1
        body_lines = self._generate_class_body(record_decl.body)
        if body_lines:
            lines.extend(body_lines)
        self.indent_level -= 1
        
        # Closing brace
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_annotation_declaration(self, annotation_decl: JavaAnnotationDeclaration) -> str:
        """Generate annotation declaration."""
        lines = []
        
        # Documentation
        if annotation_decl.javadoc:
            lines.append(self._generate_javadoc(annotation_decl.javadoc))
        
        # Annotations
        for annotation in annotation_decl.annotations:
            lines.append(self._generate_annotation(annotation))
        
        # Annotation signature
        signature_parts = []
        
        # Modifiers
        if annotation_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in annotation_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # @interface keyword
        signature_parts.append("@interface")
        
        # Annotation name
        signature_parts.append(annotation_decl.name)
        
        signature = " ".join(signature_parts)
        lines.append(signature)
        
        # Opening brace
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines[-1] += " {"
        else:
            lines.append("{")
        
        # Annotation body
        self.indent_level += 1
        body_lines = self._generate_annotation_body(annotation_decl.body)
        if body_lines:
            lines.extend(body_lines)
        self.indent_level -= 1
        
        # Closing brace
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_class_body(self, body: List[JavaBodyDeclaration]) -> List[str]:
        """Generate class body members."""
        lines = []
        
        for i, member in enumerate(body):
            if i > 0:
                if isinstance(member, JavaFieldDeclaration):
                    lines.extend([""] * self.style.blank_lines_around_field)
                elif isinstance(member, JavaMethodDeclaration):
                    lines.extend([""] * self.style.blank_lines_around_method)
                else:
                    lines.append("")
            
            member_lines = self._generate_body_declaration(member)
            lines.extend(member_lines)
        
        return lines
    
    def _generate_interface_body(self, body: List[JavaBodyDeclaration]) -> List[str]:
        """Generate interface body members."""
        return self._generate_class_body(body)
    
    def _generate_annotation_body(self, body: List[JavaBodyDeclaration]) -> List[str]:
        """Generate annotation body members."""
        return self._generate_class_body(body)
    
    def _generate_body_declaration(self, decl: JavaBodyDeclaration) -> List[str]:
        """Generate body declaration."""
        if isinstance(decl, JavaFieldDeclaration):
            return [self._indent() + self._generate_field_declaration(decl)]
        elif isinstance(decl, JavaMethodDeclaration):
            return self._generate_method_declaration(decl)
        elif isinstance(decl, JavaConstructorDeclaration):
            return self._generate_constructor_declaration(decl)
        elif isinstance(decl, JavaClassDeclaration):
            return [self._generate_class_declaration(decl)]
        elif isinstance(decl, JavaInterfaceDeclaration):
            return [self._generate_interface_declaration(decl)]
        elif isinstance(decl, JavaEnumDeclaration):
            return [self._generate_enum_declaration(decl)]
        elif isinstance(decl, JavaRecordDeclaration):
            return [self._generate_record_declaration(decl)]
        elif isinstance(decl, JavaAnnotationDeclaration):
            return [self._generate_annotation_declaration(decl)]
        else:
            return [self._indent() + f"// Unknown body declaration: {type(decl)}"]
    
    def _generate_field_declaration(self, field_decl: JavaFieldDeclaration) -> str:
        """Generate field declaration."""
        parts = []
        
        # Annotations
        if field_decl.annotations:
            annotation_parts = [self._generate_annotation(ann) for ann in field_decl.annotations]
            parts.extend(annotation_parts)
        
        # Modifiers
        if field_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in field_decl.modifiers]
            parts.extend(modifiers)
        
        # Type
        parts.append(self._generate_type(field_decl.type))
        
        # Variable declarators
        declarators = []
        for declarator in field_decl.declarators:
            declarator_str = declarator.name
            
            # Array dimensions
            if declarator.array_dimensions:
                declarator_str += "[]" * declarator.array_dimensions
            
            # Initializer
            if declarator.initializer:
                declarator_str += " = " + self._generate_expression(declarator.initializer)
            
            declarators.append(declarator_str)
        
        parts.append(", ".join(declarators))
        
        return " ".join(parts) + ";"
    
    def _generate_method_declaration(self, method_decl: JavaMethodDeclaration) -> List[str]:
        """Generate method declaration."""
        lines = []
        
        # Documentation
        if method_decl.javadoc:
            lines.append(self._indent() + self._generate_javadoc(method_decl.javadoc))
        
        # Annotations
        for annotation in method_decl.annotations:
            lines.append(self._indent() + self._generate_annotation(annotation))
        
        # Method signature
        signature_parts = []
        
        # Modifiers
        if method_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in method_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # Type parameters
        if method_decl.type_parameters:
            type_params = [self._generate_type_parameter(tp) for tp in method_decl.type_parameters]
            signature_parts.append(f"<{', '.join(type_params)}>")
        
        # Return type
        signature_parts.append(self._generate_type(method_decl.return_type))
        
        # Method name
        signature_parts.append(method_decl.name)
        
        # Parameters
        if method_decl.parameters:
            params = [self._generate_parameter(param) for param in method_decl.parameters]
            signature_parts.append(f"({', '.join(params)})")
        else:
            signature_parts.append("()")
        
        # Throws clause
        if method_decl.throws:
            throws = [self._generate_type(exc) for exc in method_decl.throws]
            signature_parts.append(f"throws {', '.join(throws)}")
        
        signature = " ".join(signature_parts)
        
        # Method body
        if method_decl.body:
            # Opening brace
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + signature + " {")
            else:
                lines.append(self._indent() + signature)
                lines.append(self._indent() + "{")
            
            # Body statements
            self.indent_level += 1
            body_lines = self._generate_block_statement(method_decl.body)
            lines.extend(body_lines)
            self.indent_level -= 1
            
            # Closing brace
            lines.append(self._indent() + "}")
        else:
            # Abstract method
            lines.append(self._indent() + signature + ";")
        
        return lines
    
    def _generate_constructor_declaration(self, constructor_decl: JavaConstructorDeclaration) -> List[str]:
        """Generate constructor declaration."""
        lines = []
        
        # Documentation
        if constructor_decl.javadoc:
            lines.append(self._indent() + self._generate_javadoc(constructor_decl.javadoc))
        
        # Annotations
        for annotation in constructor_decl.annotations:
            lines.append(self._indent() + self._generate_annotation(annotation))
        
        # Constructor signature
        signature_parts = []
        
        # Modifiers
        if constructor_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in constructor_decl.modifiers]
            signature_parts.extend(modifiers)
        
        # Type parameters
        if constructor_decl.type_parameters:
            type_params = [self._generate_type_parameter(tp) for tp in constructor_decl.type_parameters]
            signature_parts.append(f"<{', '.join(type_params)}>")
        
        # Constructor name
        signature_parts.append(constructor_decl.name)
        
        # Parameters
        if constructor_decl.parameters:
            params = [self._generate_parameter(param) for param in constructor_decl.parameters]
            signature_parts.append(f"({', '.join(params)})")
        else:
            signature_parts.append("()")
        
        # Throws clause
        if constructor_decl.throws:
            throws = [self._generate_type(exc) for exc in constructor_decl.throws]
            signature_parts.append(f"throws {', '.join(throws)}")
        
        signature = " ".join(signature_parts)
        
        # Opening brace
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines.append(self._indent() + signature + " {")
        else:
            lines.append(self._indent() + signature)
            lines.append(self._indent() + "{")
        
        # Constructor body
        self.indent_level += 1
        body_lines = self._generate_block_statement(constructor_decl.body)
        lines.extend(body_lines)
        self.indent_level -= 1
        
        # Closing brace
        lines.append(self._indent() + "}")
        
        return lines
    
    def _generate_statement(self, stmt: JavaStatement) -> List[str]:
        """Generate statement."""
        if isinstance(stmt, JavaExpressionStatement):
            return [self._indent() + self._generate_expression(stmt.expression) + ";"]
        elif isinstance(stmt, JavaBlockStatement):
            return self._generate_block_statement(stmt)
        elif isinstance(stmt, JavaIfStatement):
            return self._generate_if_statement(stmt)
        elif isinstance(stmt, JavaWhileStatement):
            return self._generate_while_statement(stmt)
        elif isinstance(stmt, JavaForStatement):
            return self._generate_for_statement(stmt)
        elif isinstance(stmt, JavaEnhancedForStatement):
            return self._generate_enhanced_for_statement(stmt)
        elif isinstance(stmt, JavaDoStatement):
            return self._generate_do_statement(stmt)
        elif isinstance(stmt, JavaSwitchStatement):
            return self._generate_switch_statement(stmt)
        elif isinstance(stmt, JavaSwitchExpression):
            return self._generate_switch_expression(stmt)
        elif isinstance(stmt, JavaBreakStatement):
            return self._generate_break_statement(stmt)
        elif isinstance(stmt, JavaContinueStatement):
            return self._generate_continue_statement(stmt)
        elif isinstance(stmt, JavaReturnStatement):
            return self._generate_return_statement(stmt)
        elif isinstance(stmt, JavaThrowStatement):
            return self._generate_throw_statement(stmt)
        elif isinstance(stmt, JavaTryStatement):
            return self._generate_try_statement(stmt)
        elif isinstance(stmt, JavaSynchronizedStatement):
            return self._generate_synchronized_statement(stmt)
        elif isinstance(stmt, JavaAssertStatement):
            return self._generate_assert_statement(stmt)
        elif isinstance(stmt, JavaEmptyStatement):
            return [self._indent() + ";"]
        elif isinstance(stmt, JavaLabeledStatement):
            return self._generate_labeled_statement(stmt)
        elif isinstance(stmt, JavaYieldStatement):
            return self._generate_yield_statement(stmt)
        elif isinstance(stmt, JavaLocalVariableDeclaration):
            return [self._indent() + self._generate_local_variable_declaration(stmt)]
        else:
            return [self._indent() + f"// Unknown statement: {type(stmt)}"]
    
    def _generate_block_statement(self, block_stmt: JavaBlockStatement) -> List[str]:
        """Generate block statement."""
        lines = []
        
        for stmt in block_stmt.statements:
            stmt_lines = self._generate_statement(stmt)
            lines.extend(stmt_lines)
        
        return lines
    
    def _generate_if_statement(self, if_stmt: JavaIfStatement) -> List[str]:
        """Generate if statement."""
        lines = []
        
        # If condition
        condition = self._generate_expression(if_stmt.condition)
        if_line = f"if ({condition})"
        
        # Then statement
        if isinstance(if_stmt.then_statement, JavaBlockStatement):
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + if_line + " {")
            else:
                lines.append(self._indent() + if_line)
                lines.append(self._indent() + "{")
            
            self.indent_level += 1
            then_lines = self._generate_block_statement(if_stmt.then_statement)
            lines.extend(then_lines)
            self.indent_level -= 1
            
            if if_stmt.else_statement:
                lines.append(self._indent() + "} else")
            else:
                lines.append(self._indent() + "}")
        else:
            lines.append(self._indent() + if_line)
            self.indent_level += 1
            then_lines = self._generate_statement(if_stmt.then_statement)
            lines.extend(then_lines)
            self.indent_level -= 1
        
        # Else statement
        if if_stmt.else_statement:
            if isinstance(if_stmt.else_statement, JavaBlockStatement):
                if not isinstance(if_stmt.then_statement, JavaBlockStatement):
                    lines.append(self._indent() + "else")
                
                if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                    if lines[-1].endswith("else"):
                        lines[-1] += " {"
                    else:
                        lines.append(self._indent() + "{")
                else:
                    lines.append(self._indent() + "{")
                
                self.indent_level += 1
                else_lines = self._generate_block_statement(if_stmt.else_statement)
                lines.extend(else_lines)
                self.indent_level -= 1
                
                lines.append(self._indent() + "}")
            elif isinstance(if_stmt.else_statement, JavaIfStatement):
                # else if
                if not isinstance(if_stmt.then_statement, JavaBlockStatement):
                    lines.append(self._indent() + "else")
                
                if_lines = self._generate_if_statement(if_stmt.else_statement)
                # Modify first line to be "else if"
                if_lines[0] = if_lines[0].replace("if", "else if", 1)
                lines.extend(if_lines)
            else:
                if not isinstance(if_stmt.then_statement, JavaBlockStatement):
                    lines.append(self._indent() + "else")
                
                self.indent_level += 1
                else_lines = self._generate_statement(if_stmt.else_statement)
                lines.extend(else_lines)
                self.indent_level -= 1
        
        return lines
    
    def _generate_while_statement(self, while_stmt: JavaWhileStatement) -> List[str]:
        """Generate while statement."""
        lines = []
        
        condition = self._generate_expression(while_stmt.condition)
        while_line = f"while ({condition})"
        
        if isinstance(while_stmt.body, JavaBlockStatement):
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + while_line + " {")
            else:
                lines.append(self._indent() + while_line)
                lines.append(self._indent() + "{")
            
            self.indent_level += 1
            body_lines = self._generate_block_statement(while_stmt.body)
            lines.extend(body_lines)
            self.indent_level -= 1
            
            lines.append(self._indent() + "}")
        else:
            lines.append(self._indent() + while_line)
            self.indent_level += 1
            body_lines = self._generate_statement(while_stmt.body)
            lines.extend(body_lines)
            self.indent_level -= 1
        
        return lines
    
    def _generate_for_statement(self, for_stmt: JavaForStatement) -> List[str]:
        """Generate for statement."""
        lines = []
        
        # For parts
        init_part = ""
        if for_stmt.init:
            if isinstance(for_stmt.init, JavaLocalVariableDeclaration):
                init_part = self._generate_local_variable_declaration(for_stmt.init)
            else:
                init_exprs = [self._generate_expression(expr) for expr in for_stmt.init]
                init_part = ", ".join(init_exprs)
        
        condition_part = ""
        if for_stmt.condition:
            condition_part = self._generate_expression(for_stmt.condition)
        
        update_part = ""
        if for_stmt.update:
            update_exprs = [self._generate_expression(expr) for expr in for_stmt.update]
            update_part = ", ".join(update_exprs)
        
        for_line = f"for ({init_part}; {condition_part}; {update_part})"
        
        if isinstance(for_stmt.body, JavaBlockStatement):
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + for_line + " {")
            else:
                lines.append(self._indent() + for_line)
                lines.append(self._indent() + "{")
            
            self.indent_level += 1
            body_lines = self._generate_block_statement(for_stmt.body)
            lines.extend(body_lines)
            self.indent_level -= 1
            
            lines.append(self._indent() + "}")
        else:
            lines.append(self._indent() + for_line)
            self.indent_level += 1
            body_lines = self._generate_statement(for_stmt.body)
            lines.extend(body_lines)
            self.indent_level -= 1
        
        return lines
    
    def _generate_enhanced_for_statement(self, enhanced_for_stmt: JavaEnhancedForStatement) -> List[str]:
        """Generate enhanced for statement (for-each)."""
        lines = []
        
        # Parameter
        param = self._generate_parameter(enhanced_for_stmt.parameter)
        
        # Expression
        expr = self._generate_expression(enhanced_for_stmt.expression)
        
        for_line = f"for ({param} : {expr})"
        
        if isinstance(enhanced_for_stmt.body, JavaBlockStatement):
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + for_line + " {")
            else:
                lines.append(self._indent() + for_line)
                lines.append(self._indent() + "{")
            
            self.indent_level += 1
            body_lines = self._generate_block_statement(enhanced_for_stmt.body)
            lines.extend(body_lines)
            self.indent_level -= 1
            
            lines.append(self._indent() + "}")
        else:
            lines.append(self._indent() + for_line)
            self.indent_level += 1
            body_lines = self._generate_statement(enhanced_for_stmt.body)
            lines.extend(body_lines)
            self.indent_level -= 1
        
        return lines
    
    def _generate_do_statement(self, do_stmt: JavaDoStatement) -> List[str]:
        """Generate do-while statement."""
        lines = []
        
        # Do keyword
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines.append(self._indent() + "do {")
        else:
            lines.append(self._indent() + "do")
            lines.append(self._indent() + "{")
        
        # Body
        self.indent_level += 1
        if isinstance(do_stmt.body, JavaBlockStatement):
            body_lines = self._generate_block_statement(do_stmt.body)
        else:
            body_lines = self._generate_statement(do_stmt.body)
        lines.extend(body_lines)
        self.indent_level -= 1
        
        # While condition
        condition = self._generate_expression(do_stmt.condition)
        lines.append(self._indent() + f"}} while ({condition});")
        
        return lines
    
    def _generate_switch_statement(self, switch_stmt: JavaSwitchStatement) -> List[str]:
        """Generate switch statement."""
        lines = []
        
        # Switch expression
        expr = self._generate_expression(switch_stmt.expression)
        switch_line = f"switch ({expr})"
        
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines.append(self._indent() + switch_line + " {")
        else:
            lines.append(self._indent() + switch_line)
            lines.append(self._indent() + "{")
        
        # Switch cases
        self.indent_level += 1
        for case in switch_stmt.cases:
            lines.extend(self._generate_switch_case(case))
        self.indent_level -= 1
        
        lines.append(self._indent() + "}")
        
        return lines
    
    def _generate_switch_expression(self, switch_expr: JavaSwitchExpression) -> List[str]:
        """Generate switch expression (Java 14+)."""
        lines = []
        
        # Switch expression
        expr = self._generate_expression(switch_expr.expression)
        switch_line = f"switch ({expr})"
        
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines.append(self._indent() + switch_line + " {")
        else:
            lines.append(self._indent() + switch_line)
            lines.append(self._indent() + "{")
        
        # Switch cases
        self.indent_level += 1
        for case in switch_expr.cases:
            lines.extend(self._generate_switch_case(case))
        self.indent_level -= 1
        
        lines.append(self._indent() + "}")
        
        return lines
    
    def _generate_switch_case(self, case: JavaSwitchCase) -> List[str]:
        """Generate switch case."""
        lines = []
        
        if case.is_default:
            lines.append(self._indent() + "default:")
        else:
            # Case labels
            if case.is_rule_form:  # Java 14+ arrow form
                labels = [self._generate_expression(label) for label in case.labels]
                case_line = f"case {', '.join(labels)} ->"
                lines.append(self._indent() + case_line)
            else:  # Traditional colon form
                for label in case.labels:
                    label_expr = self._generate_expression(label)
                    lines.append(self._indent() + f"case {label_expr}:")
        
        # Case statements
        if case.statements:
            if case.is_rule_form and len(case.statements) == 1:
                # Single statement on same line
                stmt = case.statements[0]
                if isinstance(stmt, JavaExpressionStatement):
                    expr = self._generate_expression(stmt.expression)
                    lines[-1] += f" {expr};"
                elif isinstance(stmt, JavaBlockStatement):
                    lines[-1] += " {"
                    self.indent_level += 1
                    body_lines = self._generate_block_statement(stmt)
                    lines.extend(body_lines)
                    self.indent_level -= 1
                    lines.append(self._indent() + "}")
                else:
                    self.indent_level += 1
                    stmt_lines = self._generate_statement(stmt)
                    lines.extend(stmt_lines)
                    self.indent_level -= 1
            else:
                # Multiple statements
                self.indent_level += 1
                for stmt in case.statements:
                    stmt_lines = self._generate_statement(stmt)
                    lines.extend(stmt_lines)
                self.indent_level -= 1
        
        return lines
    
    def _generate_break_statement(self, break_stmt: JavaBreakStatement) -> List[str]:
        """Generate break statement."""
        if break_stmt.label:
            return [self._indent() + f"break {break_stmt.label};"]
        else:
            return [self._indent() + "break;"]
    
    def _generate_continue_statement(self, continue_stmt: JavaContinueStatement) -> List[str]:
        """Generate continue statement."""
        if continue_stmt.label:
            return [self._indent() + f"continue {continue_stmt.label};"]
        else:
            return [self._indent() + "continue;"]
    
    def _generate_return_statement(self, return_stmt: JavaReturnStatement) -> List[str]:
        """Generate return statement."""
        if return_stmt.expression:
            expr = self._generate_expression(return_stmt.expression)
            return [self._indent() + f"return {expr};"]
        else:
            return [self._indent() + "return;"]
    
    def _generate_throw_statement(self, throw_stmt: JavaThrowStatement) -> List[str]:
        """Generate throw statement."""
        expr = self._generate_expression(throw_stmt.expression)
        return [self._indent() + f"throw {expr};"]
    
    def _generate_try_statement(self, try_stmt: JavaTryStatement) -> List[str]:
        """Generate try statement."""
        lines = []
        
        # Try-with-resources
        if try_stmt.resources:
            resources = []
            for resource in try_stmt.resources:
                if isinstance(resource, JavaLocalVariableDeclaration):
                    resources.append(self._generate_local_variable_declaration(resource))
                else:
                    resources.append(self._generate_expression(resource))
            
            try_line = f"try ({'; '.join(resources)})"
        else:
            try_line = "try"
        
        # Try block
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines.append(self._indent() + try_line + " {")
        else:
            lines.append(self._indent() + try_line)
            lines.append(self._indent() + "{")
        
        self.indent_level += 1
        try_lines = self._generate_block_statement(try_stmt.try_block)
        lines.extend(try_lines)
        self.indent_level -= 1
        
        # Catch clauses
        for catch_clause in try_stmt.catch_clauses:
            # Exception parameter
            param = self._generate_parameter(catch_clause.parameter)
            
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + f"}} catch ({param}) {{")
            else:
                lines.append(self._indent() + f"}} catch ({param})")
                lines.append(self._indent() + "{")
            
            self.indent_level += 1
            catch_lines = self._generate_block_statement(catch_clause.body)
            lines.extend(catch_lines)
            self.indent_level -= 1
        
        # Finally block
        if try_stmt.finally_block:
            if self.style.brace_style == JavaBraceStyle.SAME_LINE:
                lines.append(self._indent() + "} finally {")
            else:
                lines.append(self._indent() + "} finally")
                lines.append(self._indent() + "{")
            
            self.indent_level += 1
            finally_lines = self._generate_block_statement(try_stmt.finally_block)
            lines.extend(finally_lines)
            self.indent_level -= 1
        
        lines.append(self._indent() + "}")
        
        return lines
    
    def _generate_synchronized_statement(self, sync_stmt: JavaSynchronizedStatement) -> List[str]:
        """Generate synchronized statement."""
        lines = []
        
        expr = self._generate_expression(sync_stmt.expression)
        sync_line = f"synchronized ({expr})"
        
        if self.style.brace_style == JavaBraceStyle.SAME_LINE:
            lines.append(self._indent() + sync_line + " {")
        else:
            lines.append(self._indent() + sync_line)
            lines.append(self._indent() + "{")
        
        self.indent_level += 1
        body_lines = self._generate_block_statement(sync_stmt.body)
        lines.extend(body_lines)
        self.indent_level -= 1
        
        lines.append(self._indent() + "}")
        
        return lines
    
    def _generate_assert_statement(self, assert_stmt: JavaAssertStatement) -> List[str]:
        """Generate assert statement."""
        expr = self._generate_expression(assert_stmt.expression)
        
        if assert_stmt.message:
            message = self._generate_expression(assert_stmt.message)
            return [self._indent() + f"assert {expr} : {message};"]
        else:
            return [self._indent() + f"assert {expr};"]
    
    def _generate_labeled_statement(self, labeled_stmt: JavaLabeledStatement) -> List[str]:
        """Generate labeled statement."""
        lines = []
        
        lines.append(self._indent() + f"{labeled_stmt.label}:")
        stmt_lines = self._generate_statement(labeled_stmt.statement)
        lines.extend(stmt_lines)
        
        return lines
    
    def _generate_yield_statement(self, yield_stmt: JavaYieldStatement) -> List[str]:
        """Generate yield statement (Java 14+)."""
        expr = self._generate_expression(yield_stmt.expression)
        return [self._indent() + f"yield {expr};"]
    
    def _generate_local_variable_declaration(self, var_decl: JavaLocalVariableDeclaration) -> str:
        """Generate local variable declaration."""
        parts = []
        
        # Modifiers
        if var_decl.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in var_decl.modifiers]
            parts.extend(modifiers)
        
        # Type
        parts.append(self._generate_type(var_decl.type))
        
        # Variable declarators
        declarators = []
        for declarator in var_decl.declarators:
            declarator_str = declarator.name
            
            # Array dimensions
            if declarator.array_dimensions:
                declarator_str += "[]" * declarator.array_dimensions
            
            # Initializer
            if declarator.initializer:
                declarator_str += " = " + self._generate_expression(declarator.initializer)
            
            declarators.append(declarator_str)
        
        parts.append(", ".join(declarators))
        
        return " ".join(parts) + ";"
    
    def _generate_expression(self, expr: JavaExpression) -> str:
        """Generate expression."""
        if isinstance(expr, JavaLiteral):
            return self._generate_literal(expr)
        elif isinstance(expr, JavaIdentifier):
            return expr.name
        elif isinstance(expr, JavaQualifiedName):
            return self._generate_qualified_name(expr)
        elif isinstance(expr, JavaBinaryExpression):
            return self._generate_binary_expression(expr)
        elif isinstance(expr, JavaUnaryExpression):
            return self._generate_unary_expression(expr)
        elif isinstance(expr, JavaConditionalExpression):
            return self._generate_conditional_expression(expr)
        elif isinstance(expr, JavaAssignmentExpression):
            return self._generate_assignment_expression(expr)
        elif isinstance(expr, JavaMethodInvocation):
            return self._generate_method_invocation(expr)
        elif isinstance(expr, JavaFieldAccess):
            return self._generate_field_access(expr)
        elif isinstance(expr, JavaArrayAccess):
            return self._generate_array_access(expr)
        elif isinstance(expr, JavaCastExpression):
            return self._generate_cast_expression(expr)
        elif isinstance(expr, JavaInstanceofExpression):
            return self._generate_instanceof_expression(expr)
        elif isinstance(expr, JavaThisExpression):
            return self._generate_this_expression(expr)
        elif isinstance(expr, JavaSuperExpression):
            return self._generate_super_expression(expr)
        elif isinstance(expr, JavaClassLiteral):
            return self._generate_class_literal(expr)
        elif isinstance(expr, JavaArrayCreation):
            return self._generate_array_creation(expr)
        elif isinstance(expr, JavaArrayInitializer):
            return self._generate_array_initializer(expr)
        elif isinstance(expr, JavaLambdaExpression):
            return self._generate_lambda_expression(expr)
        elif isinstance(expr, JavaMethodReference):
            return self._generate_method_reference(expr)
        elif isinstance(expr, JavaParenthesizedExpression):
            return self._generate_parenthesized_expression(expr)
        else:
            return f"/* Unknown expression: {type(expr)} */"
    
    def _generate_literal(self, literal: JavaLiteral) -> str:
        """Generate literal."""
        if literal.type == "string":
            if self.style.use_text_blocks and "\n" in literal.value:
                # Use text block (Java 15+)
                return f'"""\n{literal.value}"""'
            else:
                return f'"{literal.value}"'
        elif literal.type == "character":
            return f"'{literal.value}'"
        elif literal.type == "boolean":
            return str(literal.value).lower()
        elif literal.type == "null":
            return "null"
        else:
            return str(literal.value)
    
    def _generate_qualified_name(self, name: JavaQualifiedName) -> str:
        """Generate qualified name."""
        return f"{self._generate_expression(name.qualifier)}.{name.name}"
    
    def _generate_binary_expression(self, expr: JavaBinaryExpression) -> str:
        """Generate binary expression."""
        left = self._generate_expression(expr.left)
        right = self._generate_expression(expr.right)
        
        if self.style.space_around_operators:
            return f"{left} {expr.operator} {right}"
        else:
            return f"{left}{expr.operator}{right}"
    
    def _generate_unary_expression(self, expr: JavaUnaryExpression) -> str:
        """Generate unary expression."""
        operand = self._generate_expression(expr.operand)
        
        if expr.is_prefix:
            return f"{expr.operator}{operand}"
        else:
            return f"{operand}{expr.operator}"
    
    def _generate_conditional_expression(self, expr: JavaConditionalExpression) -> str:
        """Generate conditional expression."""
        condition = self._generate_expression(expr.condition)
        then_expr = self._generate_expression(expr.then_expression)
        else_expr = self._generate_expression(expr.else_expression)
        
        if self.style.space_before_question:
            return f"{condition} ? {then_expr} : {else_expr}"
        else:
            return f"{condition}? {then_expr} : {else_expr}"
    
    def _generate_assignment_expression(self, expr: JavaAssignmentExpression) -> str:
        """Generate assignment expression."""
        left = self._generate_expression(expr.left)
        right = self._generate_expression(expr.right)
        
        if self.style.space_around_operators:
            return f"{left} {expr.operator} {right}"
        else:
            return f"{left}{expr.operator}{right}"
    
    def _generate_method_invocation(self, expr: JavaMethodInvocation) -> str:
        """Generate method invocation."""
        parts = []
        
        # Expression (object)
        if expr.expression:
            parts.append(self._generate_expression(expr.expression))
            parts.append(".")
        
        # Type arguments
        if expr.type_arguments:
            type_args = [self._generate_type(arg) for arg in expr.type_arguments]
            parts.append(f"<{', '.join(type_args)}>")
        
        # Method name
        parts.append(expr.name)
        
        # Arguments
        if expr.arguments:
            args = [self._generate_expression(arg) for arg in expr.arguments]
            parts.append(f"({', '.join(args)})")
        else:
            parts.append("()")
        
        return "".join(parts)
    
    def _generate_field_access(self, expr: JavaFieldAccess) -> str:
        """Generate field access."""
        expression = self._generate_expression(expr.expression)
        return f"{expression}.{expr.name}"
    
    def _generate_array_access(self, expr: JavaArrayAccess) -> str:
        """Generate array access."""
        array = self._generate_expression(expr.array)
        index = self._generate_expression(expr.index)
        return f"{array}[{index}]"
    
    def _generate_cast_expression(self, expr: JavaCastExpression) -> str:
        """Generate cast expression."""
        type_str = self._generate_type(expr.type)
        expression = self._generate_expression(expr.expression)
        return f"({type_str}) {expression}"
    
    def _generate_instanceof_expression(self, expr: JavaInstanceofExpression) -> str:
        """Generate instanceof expression."""
        expression = self._generate_expression(expr.expression)
        type_str = self._generate_type(expr.type)
        
        result = f"{expression} instanceof {type_str}"
        
        # Pattern variable (Java 16+)
        if hasattr(expr, 'pattern_variable') and expr.pattern_variable:
            result += f" {expr.pattern_variable}"
        
        return result
    
    def _generate_this_expression(self, expr: JavaThisExpression) -> str:
        """Generate this expression."""
        if expr.qualifier:
            qualifier = self._generate_expression(expr.qualifier)
            return f"{qualifier}.this"
        else:
            return "this"
    
    def _generate_super_expression(self, expr: JavaSuperExpression) -> str:
        """Generate super expression."""
        if expr.qualifier:
            qualifier = self._generate_expression(expr.qualifier)
            return f"{qualifier}.super"
        else:
            return "super"
    
    def _generate_class_literal(self, expr: JavaClassLiteral) -> str:
        """Generate class literal."""
        type_str = self._generate_type(expr.type)
        return f"{type_str}.class"
    
    def _generate_array_creation(self, expr: JavaArrayCreation) -> str:
        """Generate array creation."""
        type_str = self._generate_type(expr.type)
        
        if expr.dimensions:
            dimensions = [self._generate_expression(dim) for dim in expr.dimensions]
            dim_str = "".join(f"[{dim}]" for dim in dimensions)
            return f"new {type_str}{dim_str}"
        elif expr.initializer:
            initializer = self._generate_array_initializer(expr.initializer)
            return f"new {type_str} {initializer}"
        else:
            return f"new {type_str}[]"
    
    def _generate_array_initializer(self, expr: JavaArrayInitializer) -> str:
        """Generate array initializer."""
        if expr.elements:
            elements = [self._generate_expression(elem) for elem in expr.elements]
            return f"{{{', '.join(elements)}}}"
        else:
            return "{}"
    
    def _generate_lambda_expression(self, expr: JavaLambdaExpression) -> str:
        """Generate lambda expression."""
        # Parameters
        if expr.parameters:
            params = [self._generate_parameter(param) for param in expr.parameters]
            if len(params) == 1 and not expr.parameters[0].type:
                # Single parameter without type
                param_str = params[0]
            else:
                # Multiple parameters or typed parameters
                param_str = f"({', '.join(params)})"
        else:
            param_str = "()"
        
        # Body
        if isinstance(expr.body, JavaBlockStatement):
            # Block body
            body_str = "{"
            self.indent_level += 1
            body_lines = self._generate_block_statement(expr.body)
            if body_lines:
                body_str += "\n" + "\n".join(body_lines) + "\n" + self._indent()[:-self.style.indent_size]
            self.indent_level -= 1
            body_str += "}"
        else:
            # Expression body
            body_str = self._generate_expression(expr.body)
        
        return f"{param_str} -> {body_str}"
    
    def _generate_method_reference(self, expr: JavaMethodReference) -> str:
        """Generate method reference."""
        expression = self._generate_expression(expr.expression)
        
        if expr.type_arguments:
            type_args = [self._generate_type(arg) for arg in expr.type_arguments]
            return f"{expression}::<{', '.join(type_args)}>{expr.name}"
        else:
            return f"{expression}::{expr.name}"
    
    def _generate_parenthesized_expression(self, expr: JavaParenthesizedExpression) -> str:
        """Generate parenthesized expression."""
        inner = self._generate_expression(expr.expression)
        return f"({inner})"
    
    def _generate_type(self, type_ref: JavaType) -> str:
        """Generate type reference."""
        if isinstance(type_ref, JavaPrimitiveType):
            return type_ref.name
        elif isinstance(type_ref, JavaNamedType):
            return type_ref.name
        elif isinstance(type_ref, JavaArrayType):
            element_type = self._generate_type(type_ref.element_type)
            return f"{element_type}[]"
        elif isinstance(type_ref, JavaParameterizedType):
            base_type = self._generate_type(type_ref.base_type)
            type_args = [self._generate_type(arg) for arg in type_ref.type_arguments]
            
            if self.style.prefer_diamond_operator and not type_args:
                return f"{base_type}<>"
            else:
                return f"{base_type}<{', '.join(type_args)}>"
        elif isinstance(type_ref, JavaWildcardType):
            if type_ref.bound:
                bound_type = self._generate_type(type_ref.bound)
                if type_ref.is_extends:
                    return f"? extends {bound_type}"
                else:
                    return f"? super {bound_type}"
            else:
                return "?"
        elif isinstance(type_ref, JavaUnionType):
            types = [self._generate_type(t) for t in type_ref.types]
            return " | ".join(types)
        elif isinstance(type_ref, JavaIntersectionType):
            types = [self._generate_type(t) for t in type_ref.types]
            return " & ".join(types)
        elif isinstance(type_ref, JavaVarType):
            return "var"
        else:
            return str(type_ref)
    
    def _generate_parameter(self, param: JavaParameter) -> str:
        """Generate parameter."""
        parts = []
        
        # Annotations
        if param.annotations:
            annotations = [self._generate_annotation(ann) for ann in param.annotations]
            parts.extend(annotations)
        
        # Modifiers
        if param.modifiers:
            modifiers = [self._generate_modifier(mod) for mod in param.modifiers]
            parts.extend(modifiers)
        
        # Type
        if param.type:
            parts.append(self._generate_type(param.type))
        
        # Varargs
        if param.is_varargs:
            parts[-1] += "..."
        
        # Name
        parts.append(param.name)
        
        return " ".join(parts)
    
    def _generate_type_parameter(self, type_param: JavaTypeParameter) -> str:
        """Generate type parameter."""
        parts = [type_param.name]
        
        # Bounds
        if type_param.bounds:
            bounds = [self._generate_type(bound) for bound in type_param.bounds]
            parts.append(f"extends {' & '.join(bounds)}")
        
        return " ".join(parts)
    
    def _generate_annotation(self, annotation: JavaAnnotation) -> str:
        """Generate annotation."""
        if isinstance(annotation, JavaNormalAnnotation):
            return self._generate_normal_annotation(annotation)
        elif isinstance(annotation, JavaMarkerAnnotation):
            return self._generate_marker_annotation(annotation)
        elif isinstance(annotation, JavaSingleMemberAnnotation):
            return self._generate_single_member_annotation(annotation)
        else:
            return f"@{annotation.name}"
    
    def _generate_normal_annotation(self, annotation: JavaNormalAnnotation) -> str:
        """Generate normal annotation."""
        name = self._generate_type(annotation.name)
        
        if annotation.pairs:
            pairs = []
            for pair in annotation.pairs:
                value = self._generate_expression(pair.value)
                pairs.append(f"{pair.name} = {value}")
            return f"@{name}({', '.join(pairs)})"
        else:
            return f"@{name}()"
    
    def _generate_marker_annotation(self, annotation: JavaMarkerAnnotation) -> str:
        """Generate marker annotation."""
        name = self._generate_type(annotation.name)
        return f"@{name}"
    
    def _generate_single_member_annotation(self, annotation: JavaSingleMemberAnnotation) -> str:
        """Generate single member annotation."""
        name = self._generate_type(annotation.name)
        value = self._generate_expression(annotation.value)
        return f"@{name}({value})"
    
    def _generate_modifier(self, modifier: JavaModifier) -> str:
        """Generate modifier."""
        return modifier.name.lower()
    
    def _generate_enum_constant(self, constant: JavaEnumConstant) -> str:
        """Generate enum constant."""
        parts = [constant.name]
        
        # Arguments
        if constant.arguments:
            args = [self._generate_expression(arg) for arg in constant.arguments]
            parts.append(f"({', '.join(args)})")
        
        # Body
        if constant.body:
            parts.append("{")
            # Note: enum constant body would need separate handling
            parts.append("}")
        
        return "".join(parts)
    
    def _generate_record_component(self, component: JavaRecordComponent) -> str:
        """Generate record component."""
        parts = []
        
        # Annotations
        if component.annotations:
            annotations = [self._generate_annotation(ann) for ann in component.annotations]
            parts.extend(annotations)
        
        # Type
        parts.append(self._generate_type(component.type))
        
        # Name
        parts.append(component.name)
        
        return " ".join(parts)
    
    def _generate_module_declaration(self, module_decl: JavaModuleDeclaration) -> str:
        """Generate module declaration."""
        lines = []
        
        # Annotations
        for annotation in module_decl.annotations:
            lines.append(self._generate_annotation(annotation))
        
        # Module keyword
        if module_decl.is_open:
            lines.append(f"open module {module_decl.name} {{")
        else:
            lines.append(f"module {module_decl.name} {{")
        
        # Module directives
        self.indent_level += 1
        for directive in module_decl.directives:
            lines.append(self._indent() + self._generate_module_directive(directive))
        self.indent_level -= 1
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_module_directive(self, directive: JavaModuleDirective) -> str:
        """Generate module directive."""
        if isinstance(directive, JavaRequiresDirective):
            parts = ["requires"]
            if directive.is_static:
                parts.append("static")
            if directive.is_transitive:
                parts.append("transitive")
            parts.append(directive.module_name)
            return " ".join(parts) + ";"
        elif isinstance(directive, JavaExportsDirective):
            parts = ["exports", directive.package_name]
            if directive.to_modules:
                parts.append("to")
                parts.append(", ".join(directive.to_modules))
            return " ".join(parts) + ";"
        elif isinstance(directive, JavaOpensDirective):
            parts = ["opens", directive.package_name]
            if directive.to_modules:
                parts.append("to")
                parts.append(", ".join(directive.to_modules))
            return " ".join(parts) + ";"
        elif isinstance(directive, JavaUsesDirective):
            return f"uses {directive.service_name};"
        elif isinstance(directive, JavaProvidesDirective):
            implementations = ", ".join(directive.implementations)
            return f"provides {directive.service_name} with {implementations};"
        else:
            return f"// Unknown directive: {type(directive)}"
    
    def _generate_javadoc(self, javadoc: str) -> str:
        """Generate Javadoc comment."""
        lines = javadoc.split('\n')
        
        if len(lines) == 1:
            return f"/** {lines[0]} */"
        else:
            result = ["/**"]
            for line in lines:
                result.append(f" * {line}")
            result.append(" */")
            return "\n".join(result)
    
    def _indent(self) -> str:
        """Get current indentation."""
        if self.style.use_spaces:
            return " " * (self.indent_level * self.style.indent_size)
        else:
            return "\t" * self.indent_level
    
    def _clean_up_code(self, code: str) -> str:
        """Clean up generated code."""
        # Remove excessive blank lines
        lines = code.split('\n')
        cleaned_lines = []
        blank_line_count = 0
        
        for line in lines:
            if line.strip() == "":
                blank_line_count += 1
                if blank_line_count <= 2:  # Allow at most 2 consecutive blank lines
                    cleaned_lines.append(line)
            else:
                blank_line_count = 0
                cleaned_lines.append(line)
        
        # Remove trailing whitespace
        cleaned_lines = [line.rstrip() for line in cleaned_lines]
        
        # Ensure file ends with newline
        result = '\n'.join(cleaned_lines)
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result


class JavaFormatter:
    """Java code formatter with predefined styles."""
    
    @staticmethod
    def google_style() -> JavaCodeStyle:
        """Google Java Style Guide."""
        return JavaCodeStyle(
            indent_size=2,
            use_spaces=True,
            brace_style=JavaBraceStyle.SAME_LINE,
            max_line_length=100,
            blank_lines_around_class=1,
            blank_lines_around_method=1,
            space_before_parentheses=False,
            use_fully_qualified_names=False,
            prefer_diamond_operator=True,
            add_override_annotation=True
        )
    
    @staticmethod
    def oracle_style() -> JavaCodeStyle:
        """Oracle Java Style Guide."""
        return JavaCodeStyle(
            indent_size=4,
            use_spaces=True,
            brace_style=JavaBraceStyle.SAME_LINE,
            max_line_length=120,
            blank_lines_around_class=1,
            blank_lines_around_method=1,
            space_before_parentheses=False,
            use_fully_qualified_names=False,
            prefer_diamond_operator=True,
            add_override_annotation=True
        )
    
    @staticmethod
    def eclipse_style() -> JavaCodeStyle:
        """Eclipse Java Style Guide."""
        return JavaCodeStyle(
            indent_size=4,
            use_spaces=False,  # Use tabs
            brace_style=JavaBraceStyle.NEXT_LINE,
            max_line_length=120,
            blank_lines_around_class=1,
            blank_lines_around_method=1,
            space_before_parentheses=False,
            use_fully_qualified_names=False,
            prefer_diamond_operator=True,
            add_override_annotation=True
        )
    
    @staticmethod
    def intellij_style() -> JavaCodeStyle:
        """IntelliJ IDEA Java Style Guide."""
        return JavaCodeStyle(
            indent_size=4,
            use_spaces=True,
            brace_style=JavaBraceStyle.SAME_LINE,
            max_line_length=120,
            blank_lines_around_class=1,
            blank_lines_around_method=1,
            space_before_parentheses=False,
            use_fully_qualified_names=False,
            prefer_diamond_operator=True,
            add_override_annotation=True
        )


# Convenience functions
def generate_java(ast: JavaCompilationUnit, style: Optional[JavaCodeStyle] = None, **options) -> str:
    """Generate Java code from AST."""
    generator = JavaCodeGenerator(style)
    return generator.generate(ast)


def format_java_code(code: str, style: Optional[JavaCodeStyle] = None) -> str:
    """Format Java code with given style."""
    # This would require parsing the code first
    # Implementation would depend on having a Java parser
    return code  # Placeholder