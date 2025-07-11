#!/usr/bin/env python3
"""
COBOL Converter Implementation

Bidirectional converter between Runa AST and COBOL AST with comprehensive
mainframe data type mappings, business logic conversion, and COBOL-specific constructs.
"""

from typing import List, Dict, Optional, Any, Union
import logging
from dataclasses import dataclass

from .cobol_ast import *
from ....core.runa_ast import *
from ....core.semantic_analyzer import TypeInformation
from ....core.error_handler import ErrorHandler, ErrorType
from ....core.translation_context import TranslationContext

# Type mapping configurations
COBOL_TO_RUNA_TYPE_MAP = {
    # COBOL PICTURE clauses to Runa types
    'PIC 9': 'Integer',
    'PIC 99': 'Integer',
    'PIC 999': 'Integer',
    'PIC 9999': 'Integer',
    'PIC 99999': 'Integer',
    'PIC S9': 'Integer',
    'PIC S99': 'Integer',
    'PIC S999': 'Integer',
    'PIC S9999': 'Integer',
    'PIC S99999': 'Integer',
    'PIC 9V99': 'Decimal',
    'PIC 99V99': 'Decimal',
    'PIC 999V99': 'Decimal',
    'PIC S9V99': 'Decimal',
    'PIC S99V99': 'Decimal',
    'PIC S999V99': 'Decimal',
    'PIC X': 'String',
    'PIC XX': 'String',
    'PIC XXX': 'String',
    'PIC XXXX': 'String',
    'PIC XXXXX': 'String',
    'PIC A': 'String',
    'PIC AA': 'String',
    'PIC AAA': 'String',
    'PIC AAAA': 'String',
    'PIC AAAAA': 'String',
    
    # COBOL USAGE clauses
    'COMP': 'Integer',
    'COMP-1': 'Float',
    'COMP-2': 'Double',
    'COMP-3': 'Decimal',
    'COMP-4': 'Integer',
    'COMP-5': 'Integer',
    'BINARY': 'Integer',
    'PACKED-DECIMAL': 'Decimal',
    'DISPLAY': 'String',
    'INDEX': 'Integer',
    'POINTER': 'Pointer',
    
    # Special COBOL types
    'FILLER': 'Void',
    'FILE': 'File',
    'RECORD': 'Record',
}

RUNA_TO_COBOL_TYPE_MAP = {
    'Integer': 'PIC S9(9) COMP',
    'Long': 'PIC S9(18) COMP',
    'Short': 'PIC S9(4) COMP',
    'Byte': 'PIC S9(3) COMP',
    'Float': 'COMP-1',
    'Double': 'COMP-2',
    'Decimal': 'PIC S9(15)V99 COMP-3',
    'Boolean': 'PIC X',
    'Character': 'PIC X',
    'String': 'PIC X(255)',
    'DateTime': 'PIC X(26)',
    'File': 'FILE',
    'Array': 'OCCURS',
    'Record': 'RECORD',
}

# Statement mappings
COBOL_TO_RUNA_STATEMENTS = {
    'MOVE': 'Assignment',
    'ADD': 'BinaryExpression',
    'SUBTRACT': 'BinaryExpression', 
    'MULTIPLY': 'BinaryExpression',
    'DIVIDE': 'BinaryExpression',
    'COMPUTE': 'Assignment',
    'IF': 'IfStatement',
    'PERFORM': 'Loop',
    'CALL': 'MethodCall',
    'DISPLAY': 'Print',
    'ACCEPT': 'Input',
    'READ': 'FileRead',
    'WRITE': 'FileWrite',
    'OPEN': 'FileOpen',
    'CLOSE': 'FileClose',
}

class COBOLToRunaConverter:
    """Converts COBOL AST to Runa AST."""
    
    def __init__(self, error_handler: ErrorHandler, context: TranslationContext):
        self.error_handler = error_handler
        self.context = context
        self.logger = logging.getLogger(__name__)
        self.data_items = {}  # Track data descriptions for type inference
    
    def convert(self, cobol_node: COBOLNode) -> RunaNode:
        """Convert COBOL AST node to Runa AST node."""
        try:
            return cobol_node.accept(self)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.CONVERSION_ERROR,
                f"Failed to convert COBOL node: {e}",
                getattr(cobol_node, 'line_number', 0),
                0
            )
            return EmptyStatement()
    
    # Visitor methods for COBOL AST nodes
    def visit_cobol_program(self, node: COBOLProgram) -> CompilationUnit:
        """Convert COBOL program to Runa compilation unit."""
        compilation_unit = CompilationUnit()
        
        # Convert to a main class representing the COBOL program
        main_class = ClassDeclaration(
            name=node.identification_division.program_id or "COBOLProgram",
            access_modifier=AccessModifier.PUBLIC
        )
        
        # Convert data division to fields
        if node.data_division:
            if node.data_division.working_storage_section:
                for data_desc in node.data_division.working_storage_section.data_descriptions:
                    field = self._convert_data_description_to_field(data_desc)
                    if field:
                        main_class.members.append(field)
        
        # Convert procedure division to main method
        if node.procedure_division:
            main_method = MethodDeclaration(
                name="Main",
                access_modifier=AccessModifier.PUBLIC,
                is_static=True
            )
            
            for stmt in node.procedure_division.statements:
                runa_stmt = self.convert(stmt)
                main_method.body.statements.append(runa_stmt)
            
            main_class.members.append(main_method)
        
        compilation_unit.declarations.append(main_class)
        return compilation_unit
    
    def visit_cobol_move_statement(self, node: COBOLMoveStatement) -> AssignmentStatement:
        """Convert MOVE statement to Runa assignment."""
        # COBOL MOVE can have multiple destinations
        # Convert to multiple assignments if needed
        if len(node.destinations) == 1:
            return AssignmentStatement(
                left=self.convert(node.destinations[0]),
                right=self.convert(node.source),
                operator=AssignmentOperator.ASSIGN
            )
        else:
            # For multiple destinations, create a block statement
            assignments = []
            for dest in node.destinations:
                assignments.append(AssignmentStatement(
                    left=self.convert(dest),
                    right=self.convert(node.source),
                    operator=AssignmentOperator.ASSIGN
                ))
            return BlockStatement(statements=assignments)
    
    def visit_cobol_add_statement(self, node: COBOLAddStatement) -> Union[AssignmentStatement, BinaryExpression]:
        """Convert ADD statement to Runa assignment or expression."""
        if node.giving_variable:
            # ADD operand1 operand2 TO operand3 GIVING result
            left_expr = self.convert(node.operands[0])
            for operand in node.operands[1:]:
                left_expr = BinaryExpression(
                    left=left_expr,
                    operator=BinaryOperator.ADD,
                    right=self.convert(operand)
                )
            
            for to_var in node.to_variables:
                left_expr = BinaryExpression(
                    left=left_expr,
                    operator=BinaryOperator.ADD,
                    right=self.convert(to_var)
                )
            
            return AssignmentStatement(
                left=self.convert(node.giving_variable),
                right=left_expr,
                operator=AssignmentOperator.ASSIGN
            )
        else:
            # ADD operand TO variable (modify in place)
            left_expr = self.convert(node.operands[0])
            for operand in node.operands[1:]:
                left_expr = BinaryExpression(
                    left=left_expr,
                    operator=BinaryOperator.ADD,
                    right=self.convert(operand)
                )
            
            for to_var in node.to_variables:
                return AssignmentStatement(
                    left=self.convert(to_var),
                    right=BinaryExpression(
                        left=self.convert(to_var),
                        operator=BinaryOperator.ADD,
                        right=left_expr
                    ),
                    operator=AssignmentOperator.ASSIGN
                )
    
    def visit_cobol_display_statement(self, node: COBOLDisplayStatement) -> MethodCallExpression:
        """Convert DISPLAY statement to Runa print call."""
        # Convert to Console.WriteLine or similar
        args = []
        for item in node.items:
            args.append(self.convert(item))
        
        return MethodCallExpression(
            receiver=IdentifierExpression(name="Console"),
            method_name="WriteLine",
            arguments=args
        )
    
    def visit_cobol_if_statement(self, node: COBOLIfStatement) -> IfStatement:
        """Convert IF statement to Runa if statement."""
        if_stmt = IfStatement(
            condition=self.convert(node.condition)
        )
        
        for stmt in node.then_statements:
            if_stmt.then_statement.statements.append(self.convert(stmt))
        
        if node.else_statements:
            else_block = BlockStatement()
            for stmt in node.else_statements:
                else_block.statements.append(self.convert(stmt))
            if_stmt.else_statement = else_block
        
        return if_stmt
    
    def visit_cobol_perform_statement(self, node: COBOLPerformStatement) -> Union[WhileStatement, ForStatement]:
        """Convert PERFORM statement to Runa loop."""
        if node.times_expression:
            # PERFORM TIMES -> for loop
            return ForStatement(
                init_statement=AssignmentStatement(
                    left=IdentifierExpression(name="__loop_counter"),
                    right=LiteralExpression(value=0),
                    operator=AssignmentOperator.ASSIGN
                ),
                condition=BinaryExpression(
                    left=IdentifierExpression(name="__loop_counter"),
                    operator=BinaryOperator.LESS_THAN,
                    right=self.convert(node.times_expression)
                ),
                update_statement=AssignmentStatement(
                    left=IdentifierExpression(name="__loop_counter"),
                    right=BinaryExpression(
                        left=IdentifierExpression(name="__loop_counter"),
                        operator=BinaryOperator.ADD,
                        right=LiteralExpression(value=1)
                    ),
                    operator=AssignmentOperator.ASSIGN
                ),
                body=BlockStatement(statements=[self.convert(stmt) for stmt in node.inline_statements])
            )
        elif node.until_condition:
            # PERFORM UNTIL -> while loop
            return WhileStatement(
                condition=UnaryExpression(
                    operator=UnaryOperator.NOT,
                    operand=self.convert(node.until_condition)
                ),
                body=BlockStatement(statements=[self.convert(stmt) for stmt in node.inline_statements])
            )
        else:
            # Simple PERFORM -> method call
            return MethodCallExpression(
                receiver=None,
                method_name=node.procedure_name,
                arguments=[]
            )
    
    def visit_cobol_identifier(self, node: COBOLIdentifier) -> IdentifierExpression:
        """Convert COBOL identifier to Runa identifier."""
        # Handle COBOL naming conventions (convert hyphens to underscores)
        runa_name = node.name.replace('-', '_')
        
        # Handle subscripts (array access)
        if node.subscripts:
            base_expr = IdentifierExpression(name=runa_name)
            for subscript in node.subscripts:
                base_expr = ArrayAccessExpression(
                    array=base_expr,
                    index=self.convert(subscript)
                )
            return base_expr
        
        return IdentifierExpression(name=runa_name)
    
    def visit_cobol_literal(self, node: COBOLLiteral) -> LiteralExpression:
        """Convert COBOL literal to Runa literal."""
        if node.is_figurative:
            # Handle COBOL figurative constants
            if node.value.upper() in ['ZERO', 'ZEROS', 'ZEROES']:
                return LiteralExpression(value=0)
            elif node.value.upper() in ['SPACE', 'SPACES']:
                return LiteralExpression(value=" ")
            elif node.value.upper() in ['HIGH-VALUE', 'HIGH-VALUES']:
                return LiteralExpression(value=chr(255))
            elif node.value.upper() in ['LOW-VALUE', 'LOW-VALUES']:
                return LiteralExpression(value=chr(0))
            else:
                return LiteralExpression(value=node.value)
        else:
            return LiteralExpression(value=node.value)
    
    def visit_cobol_condition(self, node: COBOLCondition) -> BinaryExpression:
        """Convert COBOL condition to Runa boolean expression."""
        # Map COBOL operators to Runa operators
        operator_map = {
            '=': BinaryOperator.EQUALS,
            'EQUAL': BinaryOperator.EQUALS,
            'NOT =': BinaryOperator.NOT_EQUALS,
            '<': BinaryOperator.LESS_THAN,
            'LESS': BinaryOperator.LESS_THAN,
            '>': BinaryOperator.GREATER_THAN,
            'GREATER': BinaryOperator.GREATER_THAN,
            '<=': BinaryOperator.LESS_EQUAL,
            '>=': BinaryOperator.GREATER_EQUAL,
        }
        
        runa_operator = operator_map.get(node.operator, BinaryOperator.EQUALS)
        
        condition = BinaryExpression(
            left=self.convert(node.left),
            operator=runa_operator,
            right=self.convert(node.right)
        )
        
        # Handle compound conditions
        if node.next_condition:
            logical_op = BinaryOperator.LOGICAL_AND if node.logical_operator == 'AND' else BinaryOperator.LOGICAL_OR
            condition = BinaryExpression(
                left=condition,
                operator=logical_op,
                right=self.convert(node.next_condition)
            )
        
        return condition
    
    def _convert_data_description_to_field(self, data_desc: COBOLDataDescription) -> Optional[FieldDeclaration]:
        """Convert COBOL data description to Runa field."""
        if data_desc.filler or data_desc.level_number == 88:  # Skip FILLER and condition names
            return None
        
        # Determine type from PICTURE clause
        field_type = None
        if data_desc.picture_clause:
            cobol_pic = data_desc.picture_clause.picture_string
            field_type = self._convert_picture_to_type(cobol_pic)
        elif data_desc.usage_clause:
            field_type = self._convert_usage_to_type(data_desc.usage_clause)
        else:
            field_type = TypeExpression(name="Object")
        
        # Convert COBOL name to Runa name
        field_name = data_desc.data_name.replace('-', '_')
        
        field = FieldDeclaration(
            name=field_name,
            field_type=field_type,
            access_modifier=AccessModifier.PRIVATE
        )
        
        # Handle initial value
        if data_desc.value_clause:
            if data_desc.value_clause.literal_value is not None:
                field.initializer = LiteralExpression(value=data_desc.value_clause.literal_value)
            elif data_desc.value_clause.figurative_constant:
                field.initializer = self._convert_figurative_constant(data_desc.value_clause.figurative_constant)
        
        # Store for later reference
        self.data_items[field_name] = field_type
        
        return field
    
    def _convert_picture_to_type(self, picture: str) -> TypeExpression:
        """Convert COBOL PICTURE clause to Runa type."""
        # Simplified conversion - in practice, this would be more sophisticated
        if '9' in picture and 'V' in picture:
            return TypeExpression(name="Decimal")
        elif '9' in picture:
            return TypeExpression(name="Integer")
        elif 'X' in picture or 'A' in picture:
            return TypeExpression(name="String")
        else:
            return TypeExpression(name="Object")
    
    def _convert_usage_to_type(self, usage: COBOLUsage) -> TypeExpression:
        """Convert COBOL USAGE clause to Runa type."""
        usage_map = {
            COBOLUsage.COMPUTATIONAL: "Integer",
            COBOLUsage.COMPUTATIONAL_1: "Float",
            COBOLUsage.COMPUTATIONAL_2: "Double",
            COBOLUsage.COMPUTATIONAL_3: "Decimal",
            COBOLUsage.BINARY: "Integer",
            COBOLUsage.PACKED_DECIMAL: "Decimal",
            COBOLUsage.DISPLAY: "String",
            COBOLUsage.INDEX: "Integer",
            COBOLUsage.POINTER: "IntPtr",
        }
        
        return TypeExpression(name=usage_map.get(usage, "Object"))
    
    def _convert_figurative_constant(self, constant: str) -> LiteralExpression:
        """Convert COBOL figurative constant to Runa literal."""
        upper_constant = constant.upper()
        if upper_constant in ['ZERO', 'ZEROS', 'ZEROES']:
            return LiteralExpression(value=0)
        elif upper_constant in ['SPACE', 'SPACES']:
            return LiteralExpression(value=" ")
        elif upper_constant in ['HIGH-VALUE', 'HIGH-VALUES']:
            return LiteralExpression(value=chr(255))
        elif upper_constant in ['LOW-VALUE', 'LOW-VALUES']:
            return LiteralExpression(value=chr(0))
        else:
            return LiteralExpression(value=constant)

class RunaToCOBOLConverter:
    """Converts Runa AST to COBOL AST."""
    
    def __init__(self, error_handler: ErrorHandler, context: TranslationContext):
        self.error_handler = error_handler
        self.context = context
        self.logger = logging.getLogger(__name__)
        self.next_field_level = 1
    
    def convert(self, runa_node: RunaNode) -> COBOLNode:
        """Convert Runa AST node to COBOL AST node."""
        try:
            return self._convert_node(runa_node)
        except Exception as e:
            self.error_handler.add_error(
                ErrorType.CONVERSION_ERROR,
                f"Failed to convert Runa node: {e}",
                getattr(runa_node, 'source_location', SourceLocation()).line,
                getattr(runa_node, 'source_location', SourceLocation()).column
            )
            return COBOLLiteral(value="CONVERSION-ERROR", is_alphanumeric=True)
    
    def _convert_node(self, node: RunaNode) -> COBOLNode:
        """Convert specific Runa node types."""
        if isinstance(node, CompilationUnit):
            return self._convert_compilation_unit(node)
        elif isinstance(node, ClassDeclaration):
            return self._convert_class_declaration(node)
        elif isinstance(node, MethodDeclaration):
            return self._convert_method_declaration(node)
        elif isinstance(node, FieldDeclaration):
            return self._convert_field_declaration(node)
        elif isinstance(node, AssignmentStatement):
            return self._convert_assignment_statement(node)
        elif isinstance(node, BinaryExpression):
            return self._convert_binary_expression(node)
        elif isinstance(node, LiteralExpression):
            return self._convert_literal_expression(node)
        elif isinstance(node, IdentifierExpression):
            return self._convert_identifier_expression(node)
        else:
            return COBOLLiteral(value=f"UNSUPPORTED-{type(node).__name__}", is_alphanumeric=True)
    
    def _convert_compilation_unit(self, node: CompilationUnit) -> COBOLProgram:
        """Convert Runa compilation unit to COBOL program."""
        program = COBOLProgram()
        
        # Create IDENTIFICATION DIVISION
        program.identification_division = COBOLIdentificationDivision(
            program_id="RUNA-PROGRAM",
            author="Runa Converter",
            date_written=str(datetime.now().date()) if 'datetime' in globals() else "TODAY"
        )
        
        # Create DATA DIVISION
        data_division = COBOLDataDivision()
        working_storage = COBOLWorkingStorageSection()
        
        # Create PROCEDURE DIVISION
        procedure_division = COBOLProcedureDivision()
        
        # Convert class declarations
        for decl in node.declarations:
            if isinstance(decl, ClassDeclaration):
                # Convert class fields to working storage
                for member in decl.members:
                    if isinstance(member, FieldDeclaration):
                        data_desc = self._convert_field_to_data_description(member)
                        working_storage.data_descriptions.append(data_desc)
                    elif isinstance(member, MethodDeclaration) and member.name == "Main":
                        # Convert main method to procedure division
                        for stmt in member.body.statements:
                            cobol_stmt = self._convert_node(stmt)
                            if isinstance(cobol_stmt, COBOLStatement):
                                procedure_division.statements.append(cobol_stmt)
        
        data_division.working_storage_section = working_storage
        program.data_division = data_division
        program.procedure_division = procedure_division
        
        return program
    
    def _convert_assignment_statement(self, node: AssignmentStatement) -> COBOLMoveStatement:
        """Convert Runa assignment to COBOL MOVE statement."""
        return COBOLMoveStatement(
            source=self._convert_node(node.right),
            destinations=[self._convert_node(node.left)]
        )
    
    def _convert_binary_expression(self, node: BinaryExpression) -> Union[COBOLAddStatement, COBOLComputeStatement]:
        """Convert Runa binary expression to COBOL arithmetic statement."""
        if node.operator == BinaryOperator.ADD:
            return COBOLComputeStatement(
                result_variables=[COBOLIdentifier(name="TEMP-RESULT")],
                arithmetic_expression=COBOLArithmeticExpression(
                    left=self._convert_node(node.left),
                    operator="+",
                    right=self._convert_node(node.right)
                )
            )
        else:
            # Use COMPUTE for other operations
            operator_map = {
                BinaryOperator.SUBTRACT: "-",
                BinaryOperator.MULTIPLY: "*",
                BinaryOperator.DIVIDE: "/",
                BinaryOperator.POWER: "**",
            }
            
            return COBOLComputeStatement(
                result_variables=[COBOLIdentifier(name="TEMP-RESULT")],
                arithmetic_expression=COBOLArithmeticExpression(
                    left=self._convert_node(node.left),
                    operator=operator_map.get(node.operator, "+"),
                    right=self._convert_node(node.right)
                )
            )
    
    def _convert_literal_expression(self, node: LiteralExpression) -> COBOLLiteral:
        """Convert Runa literal to COBOL literal."""
        if isinstance(node.value, (int, float)):
            return COBOLLiteral(value=node.value, is_numeric=True)
        else:
            return COBOLLiteral(value=str(node.value), is_alphanumeric=True)
    
    def _convert_identifier_expression(self, node: IdentifierExpression) -> COBOLIdentifier:
        """Convert Runa identifier to COBOL identifier."""
        # Convert underscores to hyphens for COBOL naming conventions
        cobol_name = node.name.replace('_', '-').upper()
        return COBOLIdentifier(name=cobol_name)
    
    def _convert_field_to_data_description(self, field: FieldDeclaration) -> COBOLDataDescription:
        """Convert Runa field to COBOL data description."""
        # Convert field name to COBOL conventions
        cobol_name = field.name.replace('_', '-').upper()
        
        # Determine PICTURE clause from type
        picture_clause = self._convert_type_to_picture(field.field_type)
        
        data_desc = COBOLDataDescription(
            level_number=self.next_field_level,
            data_name=cobol_name,
            picture_clause=picture_clause
        )
        
        # Handle initial value
        if field.initializer:
            if isinstance(field.initializer, LiteralExpression):
                data_desc.value_clause = COBOLValueClause(
                    literal_value=field.initializer.value
                )
        
        self.next_field_level += 1
        if self.next_field_level > 49:
            self.next_field_level = 1
        
        return data_desc
    
    def _convert_type_to_picture(self, runa_type: TypeExpression) -> COBOLPictureClause:
        """Convert Runa type to COBOL PICTURE clause."""
        type_name = runa_type.name if runa_type else "Object"
        
        picture_map = {
            "Integer": "PIC S9(9) COMP",
            "Long": "PIC S9(18) COMP",
            "Short": "PIC S9(4) COMP",
            "Byte": "PIC S9(3) COMP",
            "Float": "PIC S9(7)V99 COMP-1",
            "Double": "PIC S9(15)V99 COMP-2",
            "Decimal": "PIC S9(15)V99 COMP-3",
            "Boolean": "PIC X",
            "Character": "PIC X",
            "String": "PIC X(255)",
            "DateTime": "PIC X(26)",
        }
        
        picture_string = picture_map.get(type_name, "PIC X(255)")
        
        return COBOLPictureClause(
            picture_string=picture_string,
            data_type=COBOLDataType.ALPHANUMERIC if 'X' in picture_string else COBOLDataType.NUMERIC
        )

def convert_cobol_to_runa(cobol_ast: COBOLNode, error_handler: ErrorHandler,
                         context: TranslationContext) -> RunaNode:
    """Convert COBOL AST to Runa AST."""
    converter = COBOLToRunaConverter(error_handler, context)
    return converter.convert(cobol_ast)

def convert_runa_to_cobol(runa_ast: RunaNode, error_handler: ErrorHandler,
                         context: TranslationContext) -> COBOLNode:
    """Convert Runa AST to COBOL AST."""
    converter = RunaToCOBOLConverter(error_handler, context)
    return converter.convert(runa_ast) 