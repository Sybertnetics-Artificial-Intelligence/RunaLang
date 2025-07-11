#!/usr/bin/env python3
"""
COBOL Code Generator Implementation

Complete code generator for COBOL with fixed format support, proper column positioning,
mainframe coding standards, and COBOL-85/2002 compliance.
"""

from typing import List, Dict, Optional, Any, Union, Set
import logging
from dataclasses import dataclass
from enum import Enum, auto

from .cobol_ast import *
from ....core.error_handler import ErrorHandler, ErrorType
from ....core.translation_context import TranslationContext

class COBOLFormat(Enum):
    """COBOL source format options."""
    FIXED = "FIXED"      # Traditional 80-column fixed format
    FREE = "FREE"        # Free format (COBOL 2002+)
    VARIABLE = "VARIABLE" # Variable format

@dataclass
class COBOLGeneratorConfig:
    """Configuration for COBOL code generation."""
    format: COBOLFormat = COBOLFormat.FIXED
    sequence_numbers: bool = True
    use_copybooks: bool = True
    uppercase_keywords: bool = True
    indent_size: int = 4
    max_line_length: int = 72
    area_a_start: int = 8   # Column 8-11
    area_b_start: int = 12  # Column 12-72
    comment_style: str = "*"  # *, /, or C
    preserve_comments: bool = True
    generate_end_markers: bool = True

class COBOLCodeGenerator:
    """COBOL code generator with fixed format support."""
    
    def __init__(self, config: COBOLGeneratorConfig = None, error_handler: ErrorHandler = None):
        self.config = config or COBOLGeneratorConfig()
        self.error_handler = error_handler or ErrorHandler()
        self.logger = logging.getLogger(__name__)
        self._output: List[str] = []
        self._current_line = 1
        self._current_level = 0
        self._in_procedure_division = False
        
    def generate(self, node: COBOLNode) -> str:
        """Generate COBOL code from AST node."""
        self._output = []
        self._current_line = 1
        self._current_level = 0
        
        try:
            node.accept(self)
            return '\n'.join(self._output)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.GENERATION_ERROR,
                f"Failed to generate COBOL code: {e}",
                0, 0
            )
            return f"      * Generation error: {e}"
    
    # Visitor methods for COBOL AST nodes
    def visit_cobol_program(self, node: COBOLProgram):
        """Generate COBOL program."""
        # Generate IDENTIFICATION DIVISION
        node.identification_division.accept(self)
        self._write_blank_line()
        
        # Generate ENVIRONMENT DIVISION
        if node.environment_division:
            node.environment_division.accept(self)
            self._write_blank_line()
        
        # Generate DATA DIVISION
        if node.data_division:
            node.data_division.accept(self)
            self._write_blank_line()
        
        # Generate PROCEDURE DIVISION
        if node.procedure_division:
            self._in_procedure_division = True
            node.procedure_division.accept(self)
    
    def visit_cobol_identification_division(self, node: COBOLIdentificationDivision):
        """Generate IDENTIFICATION DIVISION."""
        self._write_division_header("IDENTIFICATION DIVISION")
        
        # PROGRAM-ID
        if node.program_id:
            self._write_area_a("PROGRAM-ID.")
            self._write_area_b(f"{node.program_id}.")
        
        # Optional clauses
        if node.author:
            self._write_area_a("AUTHOR.")
            self._write_area_b(f"{node.author}.")
        
        if node.date_written:
            self._write_area_a("DATE-WRITTEN.")
            self._write_area_b(f"{node.date_written}.")
        
        if node.installation:
            self._write_area_a("INSTALLATION.")
            self._write_area_b(f"{node.installation}.")
        
        if node.security:
            self._write_area_a("SECURITY.")
            self._write_area_b(f"{node.security}.")
        
        if node.remarks:
            self._write_area_a("REMARKS.")
            self._write_area_b(f"{node.remarks}.")
    
    def visit_cobol_environment_division(self, node: COBOLEnvironmentDivision):
        """Generate ENVIRONMENT DIVISION."""
        self._write_division_header("ENVIRONMENT DIVISION")
        
        if node.configuration_section:
            node.configuration_section.accept(self)
        
        if node.input_output_section:
            node.input_output_section.accept(self)
    
    def visit_cobol_data_division(self, node: COBOLDataDivision):
        """Generate DATA DIVISION."""
        self._write_division_header("DATA DIVISION")
        
        if node.file_section:
            node.file_section.accept(self)
        
        if node.working_storage_section:
            node.working_storage_section.accept(self)
        
        if node.linkage_section:
            node.linkage_section.accept(self)
        
        if node.local_storage_section:
            node.local_storage_section.accept(self)
    
    def visit_cobol_working_storage_section(self, node: COBOLWorkingStorageSection):
        """Generate WORKING-STORAGE SECTION."""
        self._write_section_header("WORKING-STORAGE SECTION")
        
        for data_desc in node.data_descriptions:
            data_desc.accept(self)
    
    def visit_cobol_file_section(self, node: COBOLFileSection):
        """Generate FILE SECTION."""
        self._write_section_header("FILE SECTION")
        
        for file_desc in node.file_descriptions:
            file_desc.accept(self)
    
    def visit_cobol_linkage_section(self, node: COBOLLinkageSection):
        """Generate LINKAGE SECTION."""
        self._write_section_header("LINKAGE SECTION")
        
        for data_desc in node.data_descriptions:
            data_desc.accept(self)
    
    def visit_cobol_local_storage_section(self, node: COBOLLocalStorageSection):
        """Generate LOCAL-STORAGE SECTION."""
        self._write_section_header("LOCAL-STORAGE SECTION")
        
        for data_desc in node.data_descriptions:
            data_desc.accept(self)
    
    def visit_cobol_procedure_division(self, node: COBOLProcedureDivision):
        """Generate PROCEDURE DIVISION."""
        division_line = "PROCEDURE DIVISION"
        
        # Add USING clause if present
        if node.using_clause:
            division_line += " USING " + " ".join(node.using_clause)
        
        # Add RETURNING clause if present
        if node.returning_clause:
            division_line += f" RETURNING {node.returning_clause}"
        
        self._write_division_header(division_line)
        
        # Generate statements
        for stmt in node.statements:
            stmt.accept(self)
        
        # Generate paragraphs
        for para in node.paragraphs:
            para.accept(self)
        
        # Generate sections
        for section in node.sections:
            section.accept(self)
    
    def visit_cobol_data_description(self, node: COBOLDataDescription):
        """Generate data description entry."""
        line = f"{node.level_number:02d}"
        
        # Data name or FILLER
        if node.filler:
            line += " FILLER"
        else:
            line += f" {node.data_name}"
        
        # REDEFINES clause
        if node.redefines_clause:
            line += f" REDEFINES {node.redefines_clause.redefined_name}"
        
        # PICTURE clause
        if node.picture_clause:
            if self.config.uppercase_keywords:
                line += f" PIC {node.picture_clause.picture_string}"
            else:
                line += f" PICTURE {node.picture_clause.picture_string}"
        
        # USAGE clause
        if node.usage_clause:
            line += f" USAGE {node.usage_clause.value}"
        
        # VALUE clause
        if node.value_clause:
            if node.value_clause.literal_value is not None:
                if isinstance(node.value_clause.literal_value, str):
                    line += f' VALUE "{node.value_clause.literal_value}"'
                else:
                    line += f" VALUE {node.value_clause.literal_value}"
            elif node.value_clause.figurative_constant:
                line += f" VALUE {node.value_clause.figurative_constant}"
        
        # OCCURS clause
        if node.occurs_clause:
            line += f" OCCURS {node.occurs_clause.minimum_times}"
            if node.occurs_clause.maximum_times:
                line += f" TO {node.occurs_clause.maximum_times}"
            if node.occurs_clause.depending_on:
                line += f" DEPENDING ON {node.occurs_clause.depending_on}"
        
        # Other clauses
        if node.is_external:
            line += " EXTERNAL"
        if node.is_global:
            line += " GLOBAL"
        if node.is_justified:
            line += " JUSTIFIED RIGHT"
        if node.is_synchronized:
            line += " SYNCHRONIZED"
        if node.is_blank_when_zero:
            line += " BLANK WHEN ZERO"
        
        line += "."
        
        self._write_area_a(line)
        
        # Generate subordinate items
        for sub_item in node.subordinate_items:
            sub_item.accept(self)
    
    def visit_cobol_move_statement(self, node: COBOLMoveStatement):
        """Generate MOVE statement."""
        line = "MOVE "
        
        # Source
        node.source.accept(self)
        source_text = self._get_last_generated()
        line += source_text
        
        line += " TO "
        
        # Destinations
        dest_texts = []
        for dest in node.destinations:
            dest.accept(self)
            dest_texts.append(self._get_last_generated())
        
        line += " ".join(dest_texts)
        
        # CORRESPONDING clause
        if node.is_corresponding:
            line = line.replace("MOVE", "MOVE CORRESPONDING")
        
        line += "."
        
        self._write_area_b(line)
    
    def visit_cobol_add_statement(self, node: COBOLAddStatement):
        """Generate ADD statement."""
        line = "ADD "
        
        # Operands
        operand_texts = []
        for operand in node.operands:
            operand.accept(self)
            operand_texts.append(self._get_last_generated())
        
        line += " ".join(operand_texts)
        
        # TO clause
        if node.to_variables:
            line += " TO "
            to_texts = []
            for to_var in node.to_variables:
                to_var.accept(self)
                to_texts.append(self._get_last_generated())
            line += " ".join(to_texts)
        
        # GIVING clause
        if node.giving_variable:
            line += " GIVING "
            node.giving_variable.accept(self)
            line += self._get_last_generated()
        
        # CORRESPONDING clause
        if node.is_corresponding:
            line = line.replace("ADD", "ADD CORRESPONDING")
        
        line += "."
        
        self._write_area_b(line)
        
        # Size error handling
        if node.on_size_error:
            self._write_area_b("ON SIZE ERROR")
            for stmt in node.on_size_error:
                stmt.accept(self)
        
        if node.not_on_size_error:
            self._write_area_b("NOT ON SIZE ERROR")
            for stmt in node.not_on_size_error:
                stmt.accept(self)
    
    def visit_cobol_display_statement(self, node: COBOLDisplayStatement):
        """Generate DISPLAY statement."""
        line = "DISPLAY "
        
        # Items
        item_texts = []
        for item in node.items:
            item.accept(self)
            item_texts.append(self._get_last_generated())
        
        line += " ".join(item_texts)
        
        # UPON clause
        if node.upon_device:
            line += f" UPON {node.upon_device}"
        
        # WITH NO ADVANCING
        if node.with_no_advancing:
            line += " WITH NO ADVANCING"
        
        line += "."
        
        self._write_area_b(line)
    
    def visit_cobol_if_statement(self, node: COBOLIfStatement):
        """Generate IF statement."""
        line = "IF "
        
        # Condition
        node.condition.accept(self)
        line += self._get_last_generated()
        
        if node.then_statements:
            line += " THEN"
        
        self._write_area_b(line)
        
        # THEN statements
        for stmt in node.then_statements:
            stmt.accept(self)
        
        # ELSE statements
        if node.else_statements:
            self._write_area_b("ELSE")
            for stmt in node.else_statements:
                stmt.accept(self)
        
        if self.config.generate_end_markers:
            self._write_area_b("END-IF.")
    
    def visit_cobol_perform_statement(self, node: COBOLPerformStatement):
        """Generate PERFORM statement."""
        line = "PERFORM"
        
        # Procedure name
        if node.procedure_name:
            line += f" {node.procedure_name}"
            
            if node.through_procedure:
                line += f" THROUGH {node.through_procedure}"
        
        # TIMES clause
        if node.times_expression:
            line += " "
            node.times_expression.accept(self)
            line += self._get_last_generated() + " TIMES"
        
        # UNTIL clause
        if node.until_condition:
            line += " UNTIL "
            node.until_condition.accept(self)
            line += self._get_last_generated()
        
        # VARYING clause
        if node.varying_clause:
            line += " VARYING "
            node.varying_clause.accept(self)
            line += self._get_last_generated()
        
        self._write_area_b(line)
        
        # Inline statements
        if node.inline_statements:
            for stmt in node.inline_statements:
                stmt.accept(self)
            
            if self.config.generate_end_markers:
                self._write_area_b("END-PERFORM.")
        else:
            # Add period for simple PERFORM
            self._output[-1] += "."
    
    def visit_cobol_identifier(self, node: COBOLIdentifier):
        """Generate COBOL identifier."""
        name = node.name
        
        # Add subscripts if present
        if node.subscripts:
            subscript_texts = []
            for subscript in node.subscripts:
                subscript.accept(self)
                subscript_texts.append(self._get_last_generated())
            name += f"({', '.join(subscript_texts)})"
        
        # Add reference modification if present
        if node.reference_modification:
            name += "("
            node.reference_modification.start_position.accept(self)
            name += self._get_last_generated()
            
            if node.reference_modification.length:
                name += ":"
                node.reference_modification.length.accept(self)
                name += self._get_last_generated()
            
            name += ")"
        
        self._temp_output = name
    
    def visit_cobol_literal(self, node: COBOLLiteral):
        """Generate COBOL literal."""
        if node.is_numeric:
            self._temp_output = str(node.value)
        elif node.is_alphanumeric:
            self._temp_output = f'"{node.value}"'
        elif node.is_national:
            self._temp_output = f'N"{node.value}"'
        elif node.is_figurative:
            self._temp_output = node.value.upper()
        else:
            self._temp_output = str(node.value)
    
    def visit_cobol_condition(self, node: COBOLCondition):
        """Generate COBOL condition."""
        # Left operand
        node.left.accept(self)
        condition = self._get_last_generated()
        
        # Operator
        condition += f" {node.operator} "
        
        # Right operand
        node.right.accept(self)
        condition += self._get_last_generated()
        
        # Logical operator and next condition
        if node.next_condition:
            condition += f" {node.logical_operator} "
            node.next_condition.accept(self)
            condition += self._get_last_generated()
        
        self._temp_output = condition
    
    def visit_cobol_copy_statement(self, node: COBOLCopyStatement):
        """Generate COPY statement."""
        line = f"COPY {node.copy_book_name}"
        
        if node.library_name:
            line += f" OF {node.library_name}"
        
        # REPLACING clauses
        if node.replacing_clauses:
            line += " REPLACING"
            for replacing in node.replacing_clauses:
                line += f" {replacing.old_text} BY {replacing.new_text}"
        
        line += "."
        
        self._write_area_b(line)
    
    # Helper methods
    def _write_division_header(self, division_name: str):
        """Write a division header."""
        if self.config.uppercase_keywords:
            division_name = division_name.upper()
        
        self._write_area_a(f"{division_name}.")
    
    def _write_section_header(self, section_name: str):
        """Write a section header."""
        if self.config.uppercase_keywords:
            section_name = section_name.upper()
        
        self._write_area_a(f"{section_name}.")
    
    def _write_area_a(self, text: str):
        """Write text in Area A (columns 8-11)."""
        if self.config.format == COBOLFormat.FIXED:
            line = self._format_fixed_line("", " ", text, True)
        else:
            line = text
        
        self._output.append(line)
        self._current_line += 1
    
    def _write_area_b(self, text: str):
        """Write text in Area B (columns 12-72)."""
        if self.config.format == COBOLFormat.FIXED:
            line = self._format_fixed_line("", " ", text, False)
        else:
            line = "    " + text  # Simple indentation for free format
        
        self._output.append(line)
        self._current_line += 1
    
    def _write_blank_line(self):
        """Write a blank line."""
        if self.config.format == COBOLFormat.FIXED:
            self._output.append("      " + " " * 66)
        else:
            self._output.append("")
        self._current_line += 1
    
    def _format_fixed_line(self, sequence: str, indicator: str, content: str, area_a: bool) -> str:
        """Format a line according to COBOL fixed format."""
        # Sequence area (columns 1-6)
        if self.config.sequence_numbers and not sequence:
            sequence = f"{self._current_line:06d}"
        sequence_area = (sequence or "").ljust(6)[:6]
        
        # Indicator area (column 7)
        indicator_area = indicator or " "
        
        # Content area (columns 8-72)
        if area_a:
            # Area A: columns 8-11
            content_area = content.ljust(65)[:65]
        else:
            # Area B: columns 12-72
            content_area = (" " * 4) + content
            content_area = content_area.ljust(65)[:65]
        
        return sequence_area + indicator_area + content_area
    
    def _get_last_generated(self) -> str:
        """Get the last generated text (from temp output)."""
        if hasattr(self, '_temp_output'):
            result = self._temp_output
            delattr(self, '_temp_output')
            return result
        return ""

def generate_cobol(node: COBOLNode, config: COBOLGeneratorConfig = None) -> str:
    """Generate COBOL code from AST node."""
    generator = COBOLCodeGenerator(config)
    return generator.generate(node)

def format_cobol_code(code: str, config: COBOLGeneratorConfig = None) -> str:
    """Format COBOL code according to configuration."""
    # This would typically involve parsing and regenerating
    # For now, just return the code as-is
    return code 