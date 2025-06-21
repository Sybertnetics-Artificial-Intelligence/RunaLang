"""
Runa Type Checker - Natural Language Syntax Validator
====================================================

Validates Runa's natural language syntax for type safety:
- "Let user name (String) be \"Alex\"" -> Valid
- "Let rectangle area be width multiplied by height" -> Valid
- "Set user name to user name followed by \" Smith\"" -> Valid
- "Process called \"Calculate Area\" that takes width and height returns Integer" -> Valid
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
import logging
import re
from .type_system import RunaType, RunaTypeSystem, RunaBasicType, RunaCollectionType, RunaFunctionType
from .type_inference import RunaTypeInferenceEngine, RunaTypeInferenceContext, RunaTypeInferenceResult

logger = logging.getLogger(__name__)


@dataclass
class RunaTypeError:
    """Represents a Runa type error with natural language description."""
    error_type: str
    message: str
    line: int
    column: int
    source_file: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    severity: str = "error"  # "error", "warning", "info"
    runa_expression: str = ""  # Original Runa expression
    
    def __init__(self, error_type: str, message: str, line: int, column: int,
                 source_file: Optional[str] = None, suggestions: Optional[List[str]] = None,
                 severity: str = "error", runa_expression: str = ""):
        self.error_type = error_type
        self.message = message
        self.line = line
        self.column = column
        self.source_file = source_file
        self.suggestions = suggestions or []
        self.severity = severity
        self.runa_expression = runa_expression


@dataclass
class RunaTypeCheckResult:
    """Result of Runa type checking operation."""
    is_valid: bool
    errors: List[RunaTypeError] = field(default_factory=list)
    warnings: List[RunaTypeError] = field(default_factory=list)
    inferred_types: Dict[str, RunaType] = field(default_factory=dict)
    
    def __init__(self, is_valid: bool, errors: Optional[List[RunaTypeError]] = None,
                 warnings: Optional[List[RunaTypeError]] = None,
                 inferred_types: Optional[Dict[str, RunaType]] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.inferred_types = inferred_types or {}


class RunaTypeChecker:
    """
    Type checker for Runa's natural language syntax.
    
    Validates Runa syntax like:
    - "Let user name (String) be \"Alex\"" -> Valid
    - "Let rectangle area be width multiplied by height" -> Valid
    - "Set user name to user name followed by \" Smith\"" -> Valid
    - "Process called \"Calculate Area\" that takes width and height returns Integer" -> Valid
    """
    
    def __init__(self, type_system: RunaTypeSystem, type_inference_engine: RunaTypeInferenceEngine):
        self.type_system = type_system
        self.type_inference_engine = type_inference_engine
        self.type_context: RunaTypeInferenceContext = RunaTypeInferenceContext()
        
        # Initialize error message templates for Runa syntax
        self._initialize_runa_error_templates()
    
    def _initialize_runa_error_templates(self):
        """Initialize natural language error message templates for Runa syntax."""
        self.error_templates = {
            "type_mismatch": {
                "message": "Expected {expected_type} but found {actual_type} in \"{runa_expression}\"",
                "suggestions": [
                    "Check if the variable was assigned the correct type",
                    "Consider adding explicit type annotation like \"Let {variable_name} ({expected_type}) be ...\"",
                    "Verify the expression produces the expected type"
                ]
            },
            "undefined_variable": {
                "message": "Variable \"{variable_name}\" is not defined in \"{runa_expression}\"",
                "suggestions": [
                    "Check if the variable name is spelled correctly",
                    "Make sure the variable is declared before use with \"Let {variable_name} be ...\"",
                    "Consider declaring the variable with \"Let {variable_name} be ...\""
                ]
            },
            "undefined_function": {
                "message": "Function \"{function_name}\" is not defined in \"{runa_expression}\"",
                "suggestions": [
                    "Check if the function name is spelled correctly",
                    "Make sure the function is declared before use",
                    "Consider declaring the function with \"Process called \"{function_name}\" that takes ...\""
                ]
            },
            "invalid_type_annotation": {
                "message": "Invalid type annotation \"{type_annotation}\" in \"{runa_expression}\"",
                "suggestions": [
                    "Use a valid type name like \"Integer\", \"String\", \"Boolean\"",
                    "For collections, use \"List of Type\" or \"Type[]\"",
                    "For functions, use \"Function that takes Type and returns Type\""
                ]
            },
            "invalid_runa_syntax": {
                "message": "Invalid Runa syntax in \"{runa_expression}\"",
                "suggestions": [
                    "Use \"Let variable name be expression\" for declarations",
                    "Use \"Set variable name to expression\" for assignments",
                    "Use \"Process called \"name\" that takes parameters\" for functions"
                ]
            },
            "arithmetic_type_error": {
                "message": "Cannot perform arithmetic on {actual_type} in \"{runa_expression}\"",
                "suggestions": [
                    "Use numeric types (Integer, Float) for arithmetic operations",
                    "Check that both operands are numeric types",
                    "Consider converting types if needed"
                ]
            },
            "string_operation_error": {
                "message": "Cannot perform string operation on {actual_type} in \"{runa_expression}\"",
                "suggestions": [
                    "Use String types for string operations like \"followed by\"",
                    "Check that both operands are String types",
                    "Consider converting types if needed"
                ]
            }
        }
    
    def check_runa_program(self, runa_program: List[str]) -> RunaTypeCheckResult:
        """
        Check types for an entire Runa program.
        
        Args:
            runa_program: List of Runa statements to check
            
        Returns:
            RunaTypeCheckResult with validation results
        """
        result = RunaTypeCheckResult(True)
        
        # Check all statements in the program
        for i, statement in enumerate(runa_program):
            statement_result = self.check_runa_statement(statement, i + 1)
            result.errors.extend(statement_result.errors)
            result.warnings.extend(statement_result.warnings)
            result.inferred_types.update(statement_result.inferred_types)
        
        # Determine overall validity
        result.is_valid = len(result.errors) == 0
        
        return result
    
    def check_runa_statement(self, runa_statement: str, line_number: int = 1) -> RunaTypeCheckResult:
        """
        Check types for a single Runa statement.
        
        Args:
            runa_statement: The Runa statement to check
            line_number: Line number for error reporting
            
        Returns:
            RunaTypeCheckResult with validation results
        """
        result = RunaTypeCheckResult(True)
        
        # Handle different Runa statement types
        if runa_statement.strip().lower().startswith('let '):
            result = self._check_runa_declaration(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('set '):
            result = self._check_runa_assignment(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('process called'):
            result = self._check_runa_function_declaration(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('type '):
            result = self._check_runa_type_definition(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('if '):
            result = self._check_runa_conditional(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('for each'):
            result = self._check_runa_loop(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('while '):
            result = self._check_runa_while_loop(runa_statement, line_number)
        elif runa_statement.strip().lower().startswith('match '):
            result = self._check_runa_pattern_matching(runa_statement, line_number)
        else:
            # Generic statement checking
            result = self._check_runa_generic_statement(runa_statement, line_number)
        
        return result
    
    def _check_runa_declaration(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa variable declarations."""
        result = RunaTypeCheckResult(True)
        
        # Parse "Let variable name (Type) be expression"
        declaration_pattern = r'Let\s+([^(]+?)\s*(?:\(([^)]+)\))?\s+be\s+(.+)'
        match = re.match(declaration_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid declaration syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        variable_name = match.group(1).strip()
        type_annotation = match.group(2)
        expression = match.group(3).strip()
        
        # Check type annotation if present
        expected_type = None
        if type_annotation:
            try:
                expected_type = self.type_system.parse_type(type_annotation)
            except ValueError:
                error = self._create_runa_type_error(
                    "invalid_type_annotation",
                    line=line_number,
                    column=runa_statement.find(type_annotation) + 1,
                    runa_expression=runa_statement,
                    type_annotation=type_annotation
                )
                result.errors.append(error)
                return result
        
        # Check expression
        try:
            expression_result = self.type_inference_engine.infer_type_from_runa_expression(
                expression, self.type_context
            )
            actual_type = expression_result.inferred_type
            
            # Check type compatibility if annotation was provided
            if expected_type and not expected_type.is_compatible_with(actual_type):
                error = self._create_runa_type_error(
                    "type_mismatch",
                    line=line_number,
                    column=1,
                    runa_expression=runa_statement,
                    expected_type=expected_type.name,
                    actual_type=actual_type.name,
                    variable_name=variable_name
                )
                result.errors.append(error)
            
            # Add variable to context
            self.type_context.variables[variable_name] = expected_type or actual_type
            result.inferred_types[variable_name] = expected_type or actual_type
            
        except Exception as e:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=runa_statement.find(expression) + 1,
                runa_expression=runa_statement,
                message=f"Could not infer type from expression: {str(e)}"
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_assignment(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa assignments."""
        result = RunaTypeCheckResult(True)
        
        # Parse "Set variable name to expression"
        assignment_pattern = r'Set\s+([^t]+?)\s+to\s+(.+)'
        match = re.match(assignment_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid assignment syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        variable_name = match.group(1).strip()
        expression = match.group(2).strip()
        
        # Check if variable is defined
        if variable_name not in self.type_context.variables:
            error = self._create_runa_type_error(
                "undefined_variable",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                variable_name=variable_name
            )
            result.errors.append(error)
            return result
        
        expected_type = self.type_context.variables[variable_name]
        
        # Check expression
        try:
            expression_result = self.type_inference_engine.infer_type_from_runa_expression(
                expression, self.type_context
            )
            actual_type = expression_result.inferred_type
            
            # Check type compatibility
            if not expected_type.is_compatible_with(actual_type):
                error = self._create_runa_type_error(
                    "type_mismatch",
                    line=line_number,
                    column=1,
                    runa_expression=runa_statement,
                    expected_type=expected_type.name,
                    actual_type=actual_type.name,
                    variable_name=variable_name
                )
                result.errors.append(error)
            
        except Exception as e:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=runa_statement.find(expression) + 1,
                runa_expression=runa_statement,
                message=f"Could not infer type from expression: {str(e)}"
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_function_declaration(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa function declarations."""
        result = RunaTypeCheckResult(True)
        
        # Parse "Process called \"name\" that takes parameters returns Type:"
        process_pattern = r'Process\s+called\s+"([^"]+)"\s+that\s+takes\s+(.+?)(?:\s+returns\s+([^:]+))?\s*:'
        match = re.match(process_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid process declaration syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        function_name = match.group(1)
        parameters_text = match.group(2).strip()
        return_type_text = match.group(3)
        
        # Parse parameters
        param_types = []
        if parameters_text.lower() != "nothing":
            param_parts = re.split(r'\s+and\s+|\s*,\s*', parameters_text)
            for param_part in param_parts:
                param_part = param_part.strip()
                if param_part:
                    # For now, assume all parameters are unknown type
                    param_types.append(RunaType("Unknown", "custom", param_part))
        
        # Parse return type
        return_type = self.type_system.basic_types["Void"]
        if return_type_text:
            try:
                return_type = self.type_system.parse_type(return_type_text.strip())
            except ValueError:
                error = self._create_runa_type_error(
                    "invalid_type_annotation",
                    line=line_number,
                    column=runa_statement.find(return_type_text) + 1,
                    runa_expression=runa_statement,
                    type_annotation=return_type_text
                )
                result.errors.append(error)
        
        # Add function to context
        function_type = RunaFunctionType(param_types, return_type, 
                                       f"Function that takes {', '.join(p.name for p in param_types)} and returns {return_type.name}")
        self.type_context.functions[function_name] = function_type
        result.inferred_types[function_name] = function_type
        
        return result
    
    def _check_runa_type_definition(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa type definitions."""
        result = RunaTypeCheckResult(True)
        
        # Parse "Type name is type_expression"
        type_pattern = r'Type\s+(\w+)\s+is\s+(.+)'
        match = re.match(type_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid type definition syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        type_name = match.group(1)
        type_expression = match.group(2).strip()
        
        # Parse type expression
        try:
            defined_type = self.type_system.parse_type(type_expression)
            self.type_context.variables[type_name] = defined_type
            result.inferred_types[type_name] = defined_type
        except ValueError:
            error = self._create_runa_type_error(
                "invalid_type_annotation",
                line=line_number,
                column=runa_statement.find(type_expression) + 1,
                runa_expression=runa_statement,
                type_annotation=type_expression
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_conditional(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa conditional statements."""
        result = RunaTypeCheckResult(True)
        
        # Parse "If expression:"
        conditional_pattern = r'If\s+(.+?)\s*:'
        match = re.match(conditional_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid conditional syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        condition_expression = match.group(1).strip()
        
        # Check condition expression
        try:
            condition_result = self.type_inference_engine.infer_type_from_runa_expression(
                condition_expression, self.type_context
            )
            condition_type = condition_result.inferred_type
            
            # Condition should be boolean
            if not isinstance(condition_type, RunaBasicType) or condition_type.name != "Boolean":
                error = self._create_runa_type_error(
                    "type_mismatch",
                    line=line_number,
                    column=runa_statement.find(condition_expression) + 1,
                    runa_expression=runa_statement,
                    expected_type="Boolean",
                    actual_type=condition_type.name
                )
                result.errors.append(error)
            
        except Exception as e:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=runa_statement.find(condition_expression) + 1,
                runa_expression=runa_statement,
                message=f"Could not infer type from condition: {str(e)}"
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_loop(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa for-each loops."""
        result = RunaTypeCheckResult(True)
        
        # Parse "For each variable in expression:"
        loop_pattern = r'For\s+each\s+(\w+)\s+in\s+(.+)'
        match = re.match(loop_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid loop syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        variable_name = match.group(1)
        collection_expression = match.group(2).strip()
        
        # Check collection expression
        try:
            collection_result = self.type_inference_engine.infer_type_from_runa_expression(
                collection_expression, self.type_context
            )
            collection_type = collection_result.inferred_type
            
            # Collection should be a collection type
            if not isinstance(collection_type, RunaCollectionType):
                error = self._create_runa_type_error(
                    "type_mismatch",
                    line=line_number,
                    column=runa_statement.find(collection_expression) + 1,
                    runa_expression=runa_statement,
                    expected_type="Collection",
                    actual_type=collection_type.name
                )
                result.errors.append(error)
            
        except Exception as e:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=runa_statement.find(collection_expression) + 1,
                runa_expression=runa_statement,
                message=f"Could not infer type from collection: {str(e)}"
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_while_loop(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa while loops."""
        result = RunaTypeCheckResult(True)
        
        # Parse "While expression:"
        while_pattern = r'While\s+(.+?)\s*:'
        match = re.match(while_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid while loop syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        condition_expression = match.group(1).strip()
        
        # Check condition expression (same as conditional)
        try:
            condition_result = self.type_inference_engine.infer_type_from_runa_expression(
                condition_expression, self.type_context
            )
            condition_type = condition_result.inferred_type
            
            # Condition should be boolean
            if not isinstance(condition_type, RunaBasicType) or condition_type.name != "Boolean":
                error = self._create_runa_type_error(
                    "type_mismatch",
                    line=line_number,
                    column=runa_statement.find(condition_expression) + 1,
                    runa_expression=runa_statement,
                    expected_type="Boolean",
                    actual_type=condition_type.name
                )
                result.errors.append(error)
            
        except Exception as e:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=runa_statement.find(condition_expression) + 1,
                runa_expression=runa_statement,
                message=f"Could not infer type from condition: {str(e)}"
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_pattern_matching(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for Runa pattern matching."""
        result = RunaTypeCheckResult(True)
        
        # Parse "Match expression:"
        match_pattern = r'Match\s+(.+?)\s*:'
        match = re.match(match_pattern, runa_statement, re.IGNORECASE)
        
        if not match:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=1,
                runa_expression=runa_statement,
                message=f"Invalid pattern matching syntax: {runa_statement}"
            )
            result.errors.append(error)
            return result
        
        matched_expression = match.group(1).strip()
        
        # Check matched expression
        try:
            expression_result = self.type_inference_engine.infer_type_from_runa_expression(
                matched_expression, self.type_context
            )
            # For now, just check that we can infer a type
            result.inferred_types[matched_expression] = expression_result.inferred_type
            
        except Exception as e:
            error = self._create_runa_type_error(
                "invalid_runa_syntax",
                line=line_number,
                column=runa_statement.find(matched_expression) + 1,
                runa_expression=runa_statement,
                message=f"Could not infer type from expression: {str(e)}"
            )
            result.errors.append(error)
        
        return result
    
    def _check_runa_generic_statement(self, runa_statement: str, line_number: int) -> RunaTypeCheckResult:
        """Check types for generic Runa statements."""
        result = RunaTypeCheckResult(True)
        
        # Try to infer type from the statement
        try:
            expression_result = self.type_inference_engine.infer_type_from_runa_expression(
                runa_statement, self.type_context
            )
            result.inferred_types["result"] = expression_result.inferred_type
            
        except Exception:
            # If we can't infer a type, it might be a valid statement we don't handle yet
            pass
        
        return result
    
    def _create_runa_type_error(self, error_type: str, line: int, column: int,
                               runa_expression: str = "", **kwargs) -> RunaTypeError:
        """Create a Runa type error with natural language message."""
        template = self.error_templates.get(error_type, {
            "message": f"Runa type error: {error_type}",
            "suggestions": ["Check the Runa syntax and type annotations"]
        })
        
        message = template["message"].format(**kwargs)
        suggestions = template.get("suggestions", [])
        
        return RunaTypeError(
            error_type=error_type,
            message=message,
            line=line,
            column=column,
            suggestions=suggestions,
            runa_expression=runa_expression
        )
    
    def suggest_runa_fixes(self, runa_expression: str) -> List[str]:
        """
        Suggest fixes for Runa syntax issues.
        
        Args:
            runa_expression: The Runa expression to suggest fixes for
            
        Returns:
            List of suggested fixes
        """
        suggestions = []
        
        # Check for common Runa syntax issues
        if "=" in runa_expression and not runa_expression.lower().startswith(('let ', 'set ')):
            suggestions.append("Use \"Let variable name be expression\" for declarations")
            suggestions.append("Use \"Set variable name to expression\" for assignments")
        
        if "function" in runa_expression.lower():
            suggestions.append("Use \"Process called \"name\" that takes parameters\" for functions")
        
        if "if" in runa_expression.lower() and ":" not in runa_expression:
            suggestions.append("Use \"If condition:\" for conditionals")
        
        if "for" in runa_expression.lower() and "each" not in runa_expression.lower():
            suggestions.append("Use \"For each item in collection:\" for loops")
        
        return suggestions 