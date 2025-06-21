"""
Runa Error Handler - Production-Ready Framework

Comprehensive error handling and reporting for Runa language:
- Natural language error messages
- Helpful diagnostics and suggestions
- Error categorization and severity levels
- Error recovery strategies
- Comprehensive error logging
"""

import traceback
import sys
import os
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import json
import re


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""
    LEXICAL = "lexical"
    SYNTAX = "syntax"
    SEMANTIC = "semantic"
    TYPE = "type"
    RUNTIME = "runtime"
    SYSTEM = "system"
    COMPILATION = "compilation"
    VALIDATION = "validation"


class ErrorCode(Enum):
    """Standard error codes for Runa language."""
    # Lexical errors
    UNEXPECTED_CHARACTER = "LEX001"
    INVALID_TOKEN = "LEX002"
    UNTERMINATED_STRING = "LEX003"
    UNTERMINATED_COMMENT = "LEX004"
    
    # Syntax errors
    UNEXPECTED_TOKEN = "SYN001"
    MISSING_TOKEN = "SYN002"
    INVALID_EXPRESSION = "SYN003"
    UNBALANCED_PARENTHESES = "SYN004"
    INVALID_STATEMENT = "SYN005"
    
    # Semantic errors
    UNDEFINED_VARIABLE = "SEM001"
    UNDEFINED_FUNCTION = "SEM002"
    DUPLICATE_DECLARATION = "SEM003"
    INVALID_ASSIGNMENT = "SEM004"
    INVALID_OPERATION = "SEM005"
    
    # Type errors
    TYPE_MISMATCH = "TYP001"
    INVALID_TYPE_ANNOTATION = "TYP002"
    UNSUPPORTED_OPERATION = "TYP003"
    INVALID_TYPE_CONVERSION = "TYP004"
    
    # Runtime errors
    DIVISION_BY_ZERO = "RUN001"
    INDEX_OUT_OF_BOUNDS = "RUN002"
    NULL_REFERENCE = "RUN003"
    STACK_OVERFLOW = "RUN004"
    
    # System errors
    FILE_NOT_FOUND = "SYS001"
    PERMISSION_DENIED = "SYS002"
    MEMORY_ERROR = "SYS003"
    COMPILATION_FAILED = "SYS004"


@dataclass
class ErrorContext:
    """Context information for error reporting."""
    line: int
    column: int
    source_file: Optional[str] = None
    source_line: Optional[str] = None
    surrounding_context: Optional[str] = None
    stack_trace: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None


@dataclass
class RunaError:
    """Comprehensive error representation."""
    error_code: ErrorCode
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    natural_language_message: str
    context: ErrorContext
    suggestions: List[str]
    timestamp: datetime
    error_id: str
    related_errors: List[str] = None
    
    def __post_init__(self):
        if self.related_errors is None:
            self.related_errors = []


@dataclass
class ErrorReport:
    """Complete error report with analysis."""
    report_id: str
    timestamp: datetime
    total_errors: int
    errors_by_severity: Dict[str, int]
    errors_by_category: Dict[str, int]
    errors: List[RunaError]
    summary: str
    recommendations: List[str]


class ErrorPatterns:
    """Patterns for error detection and suggestion generation."""
    
    # Common error patterns and their suggestions
    PATTERNS = {
        ErrorCode.UNEXPECTED_CHARACTER: {
            "pattern": r"unexpected character",
            "suggestions": [
                "Check for typos or invalid characters in your code",
                "Ensure you're using valid Runa syntax",
                "Remove any special characters that aren't part of the language"
            ]
        },
        ErrorCode.UNDEFINED_VARIABLE: {
            "pattern": r"undefined variable|name.*not defined",
            "suggestions": [
                "Declare the variable before using it",
                "Check the variable name spelling",
                "Ensure the variable is in scope",
                "Use 'Let' or 'Define' to declare variables"
            ]
        },
        ErrorCode.TYPE_MISMATCH: {
            "pattern": r"type mismatch|incompatible types",
            "suggestions": [
                "Check the types of your variables and expressions",
                "Use explicit type annotations if needed",
                "Ensure operations are performed on compatible types",
                "Consider type conversion if appropriate"
            ]
        },
        ErrorCode.UNBALANCED_PARENTHESES: {
            "pattern": r"unbalanced|mismatched.*parentheses",
            "suggestions": [
                "Check for missing opening or closing parentheses",
                "Count opening and closing parentheses to ensure they match",
                "Use an editor with bracket matching to help identify issues"
            ]
        },
        ErrorCode.DIVISION_BY_ZERO: {
            "pattern": r"division by zero",
            "suggestions": [
                "Add a check to ensure the divisor is not zero",
                "Use conditional logic to handle zero cases",
                "Consider using a default value when division by zero is possible"
            ]
        }
    }
    
    # Natural language templates for error messages
    NATURAL_LANGUAGE_TEMPLATES = {
        ErrorCode.UNEXPECTED_CHARACTER: "I found an unexpected character '{character}' at line {line}, column {column}. This character isn't part of valid Runa syntax.",
        ErrorCode.UNDEFINED_VARIABLE: "I don't recognize the variable '{variable}' at line {line}, column {column}. You need to define it first using 'Let' or 'Define'.",
        ErrorCode.TYPE_MISMATCH: "There's a type mismatch at line {line}, column {column}. You're trying to use a {actual_type} where a {expected_type} is expected.",
        ErrorCode.UNBALANCED_PARENTHESES: "I found unbalanced parentheses at line {line}, column {column}. Make sure all opening and closing parentheses match.",
        ErrorCode.DIVISION_BY_ZERO: "You're trying to divide by zero at line {line}, column {column}. This operation isn't allowed in mathematics."
    }


class RunaErrorHandler:
    """
    Production-ready error handler for Runa language.
    
    Features:
    - Natural language error messages
    - Helpful diagnostics and suggestions
    - Error categorization and severity levels
    - Error recovery strategies
    - Comprehensive error logging
    """
    
    def __init__(self, output_dir: str = "error_logs"):
        self.output_dir = output_dir
        self.errors_logged = []
        self.error_callbacks = []
        self.recovery_strategies = {}
        self.error_patterns = ErrorPatterns()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "errors"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "reports"), exist_ok=True)
        
        # Initialize recovery strategies
        self._initialize_recovery_strategies()
    
    def _initialize_recovery_strategies(self):
        """Initialize error recovery strategies."""
        self.recovery_strategies = {
            ErrorCode.UNEXPECTED_CHARACTER: self._recover_unexpected_character,
            ErrorCode.UNDEFINED_VARIABLE: self._recover_undefined_variable,
            ErrorCode.TYPE_MISMATCH: self._recover_type_mismatch,
            ErrorCode.UNBALANCED_PARENTHESES: self._recover_unbalanced_parentheses,
            ErrorCode.MISSING_TOKEN: self._recover_missing_token,
            ErrorCode.UNTERMINATED_STRING: self._recover_unterminated_string
        }
    
    def create_error(self, error_code: ErrorCode, message: str, context: ErrorContext,
                    severity: ErrorSeverity = ErrorSeverity.ERROR,
                    suggestions: List[str] = None) -> RunaError:
        """Create a comprehensive error with natural language message."""
        
        # Generate natural language message
        natural_message = self._generate_natural_language_message(error_code, context)
        
        # Generate suggestions if not provided
        if suggestions is None:
            suggestions = self._generate_suggestions(error_code, context)
        
        # Create error
        error = RunaError(
            error_code=error_code,
            category=self._get_error_category(error_code),
            severity=severity,
            message=message,
            natural_language_message=natural_message,
            context=context,
            suggestions=suggestions,
            timestamp=datetime.now(),
            error_id=f"{error_code.value}_{int(datetime.now().timestamp() * 1000)}"
        )
        
        return error
    
    def _generate_natural_language_message(self, error_code: ErrorCode, context: ErrorContext) -> str:
        """Generate natural language error message."""
        template = self.error_patterns.NATURAL_LANGUAGE_TEMPLATES.get(error_code)
        
        if template:
            # Extract context information for template
            context_data = {
                'line': context.line,
                'column': context.column,
                'character': context.source_line[context.column - 1] if context.source_line and context.column <= len(context.source_line) else '?',
                'variable': self._extract_variable_name(context),
                'actual_type': self._extract_actual_type(context),
                'expected_type': self._extract_expected_type(context)
            }
            
            try:
                return template.format(**context_data)
            except KeyError:
                # Fallback if template variables are missing
                return f"I found an error at line {context.line}, column {context.column}. {self._get_default_message(error_code)}"
        
        return self._get_default_message(error_code)
    
    def _get_default_message(self, error_code: ErrorCode) -> str:
        """Get default error message for error code."""
        default_messages = {
            ErrorCode.UNEXPECTED_CHARACTER: "There's an unexpected character in your code.",
            ErrorCode.UNDEFINED_VARIABLE: "You're using a variable that hasn't been defined yet.",
            ErrorCode.TYPE_MISMATCH: "There's a type mismatch in your code.",
            ErrorCode.UNBALANCED_PARENTHESES: "Your parentheses don't match up properly.",
            ErrorCode.DIVISION_BY_ZERO: "You can't divide by zero.",
            ErrorCode.MISSING_TOKEN: "Something is missing from your code.",
            ErrorCode.UNTERMINATED_STRING: "Your string isn't properly closed.",
            ErrorCode.INVALID_EXPRESSION: "This expression isn't valid.",
            ErrorCode.DUPLICATE_DECLARATION: "You've declared this more than once.",
            ErrorCode.INVALID_ASSIGNMENT: "This assignment isn't valid."
        }
        
        return default_messages.get(error_code, "An error occurred in your code.")
    
    def _extract_variable_name(self, context: ErrorContext) -> str:
        """Extract variable name from error context."""
        if context.source_line:
            # Simple extraction - look for identifier at column
            words = context.source_line.split()
            for word in words:
                if word.isidentifier():
                    return word
        return "variable"
    
    def _extract_actual_type(self, context: ErrorContext) -> str:
        """Extract actual type from error context."""
        # This would be enhanced with actual type information
        return "unknown type"
    
    def _extract_expected_type(self, context: ErrorContext) -> str:
        """Extract expected type from error context."""
        # This would be enhanced with expected type information
        return "expected type"
    
    def _generate_suggestions(self, error_code: ErrorCode, context: ErrorContext) -> List[str]:
        """Generate helpful suggestions for error recovery."""
        pattern_info = self.error_patterns.PATTERNS.get(error_code)
        
        if pattern_info:
            return pattern_info["suggestions"]
        
        # Default suggestions based on error category
        category = self._get_error_category(error_code)
        default_suggestions = {
            ErrorCategory.LEXICAL: [
                "Check your spelling and syntax",
                "Make sure you're using valid Runa keywords",
                "Remove any invalid characters"
            ],
            ErrorCategory.SYNTAX: [
                "Check the syntax of your statement",
                "Make sure all brackets and parentheses match",
                "Verify that your code follows Runa grammar rules"
            ],
            ErrorCategory.SEMANTIC: [
                "Check the meaning and logic of your code",
                "Make sure variables are properly declared",
                "Verify that operations are valid"
            ],
            ErrorCategory.TYPE: [
                "Check the types of your variables",
                "Make sure operations are performed on compatible types",
                "Consider adding explicit type annotations"
            ],
            ErrorCategory.RUNTIME: [
                "Check your program logic",
                "Verify that all variables have valid values",
                "Add error handling for edge cases"
            ]
        }
        
        return default_suggestions.get(category, ["Review your code and try again"])
    
    def _get_error_category(self, error_code: ErrorCode) -> ErrorCategory:
        """Get error category for error code."""
        category_mapping = {
            # Lexical errors
            ErrorCode.UNEXPECTED_CHARACTER: ErrorCategory.LEXICAL,
            ErrorCode.INVALID_TOKEN: ErrorCategory.LEXICAL,
            ErrorCode.UNTERMINATED_STRING: ErrorCategory.LEXICAL,
            ErrorCode.UNTERMINATED_COMMENT: ErrorCategory.LEXICAL,
            
            # Syntax errors
            ErrorCode.UNEXPECTED_TOKEN: ErrorCategory.SYNTAX,
            ErrorCode.MISSING_TOKEN: ErrorCategory.SYNTAX,
            ErrorCode.INVALID_EXPRESSION: ErrorCategory.SYNTAX,
            ErrorCode.UNBALANCED_PARENTHESES: ErrorCategory.SYNTAX,
            ErrorCode.INVALID_STATEMENT: ErrorCategory.SYNTAX,
            
            # Semantic errors
            ErrorCode.UNDEFINED_VARIABLE: ErrorCategory.SEMANTIC,
            ErrorCode.UNDEFINED_FUNCTION: ErrorCategory.SEMANTIC,
            ErrorCode.DUPLICATE_DECLARATION: ErrorCategory.SEMANTIC,
            ErrorCode.INVALID_ASSIGNMENT: ErrorCategory.SEMANTIC,
            ErrorCode.INVALID_OPERATION: ErrorCategory.SEMANTIC,
            
            # Type errors
            ErrorCode.TYPE_MISMATCH: ErrorCategory.TYPE,
            ErrorCode.INVALID_TYPE_ANNOTATION: ErrorCategory.TYPE,
            ErrorCode.UNSUPPORTED_OPERATION: ErrorCategory.TYPE,
            ErrorCode.INVALID_TYPE_CONVERSION: ErrorCategory.TYPE,
            
            # Runtime errors
            ErrorCode.DIVISION_BY_ZERO: ErrorCategory.RUNTIME,
            ErrorCode.INDEX_OUT_OF_BOUNDS: ErrorCategory.RUNTIME,
            ErrorCode.NULL_REFERENCE: ErrorCategory.RUNTIME,
            ErrorCode.STACK_OVERFLOW: ErrorCategory.RUNTIME,
            
            # System errors
            ErrorCode.FILE_NOT_FOUND: ErrorCategory.SYSTEM,
            ErrorCode.PERMISSION_DENIED: ErrorCategory.SYSTEM,
            ErrorCode.MEMORY_ERROR: ErrorCategory.SYSTEM,
            ErrorCode.COMPILATION_FAILED: ErrorCategory.SYSTEM
        }
        
        return category_mapping.get(error_code, ErrorCategory.SYSTEM)
    
    def log_error(self, error: RunaError):
        """Log an error with comprehensive information."""
        self.errors_logged.append(error)
        
        # Save error to file
        error_file = os.path.join(self.output_dir, "errors", f"{error.error_id}.json")
        with open(error_file, 'w') as f:
            json.dump(asdict(error), f, indent=2, default=str)
        
        # Call error callbacks
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception as e:
                print(f"Error in error callback: {e}")
        
        # Print error to console
        self._print_error(error)
    
    def _print_error(self, error: RunaError):
        """Print error in a user-friendly format."""
        print(f"\n❌ {error.severity.value.upper()}: {error.natural_language_message}")
        
        if error.context.source_file:
            print(f"   File: {error.context.source_file}")
        
        print(f"   Line: {error.context.line}, Column: {error.context.column}")
        
        if error.context.source_line:
            print(f"   Code: {error.context.source_line.strip()}")
            # Show caret pointing to error location
            if error.context.column <= len(error.context.source_line):
                caret_line = " " * (error.context.column - 1) + "^"
                print(f"        {caret_line}")
        
        if error.suggestions:
            print(f"\n💡 Suggestions:")
            for i, suggestion in enumerate(error.suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        print(f"\n🔍 Error Code: {error.error_code.value}")
        print(f"📝 Category: {error.category.value}")
    
    def handle_compilation_error(self, error_code: ErrorCode, message: str, line: int, column: int,
                                source_file: str = None, source_line: str = None) -> RunaError:
        """Handle compilation error with full context."""
        context = ErrorContext(
            line=line,
            column=column,
            source_file=source_file,
            source_line=source_line,
            stack_trace=traceback.format_exc()
        )
        
        error = self.create_error(error_code, message, context)
        self.log_error(error)
        
        return error
    
    def handle_runtime_error(self, exception: Exception, context: ErrorContext = None) -> RunaError:
        """Handle runtime error with exception information."""
        if context is None:
            context = ErrorContext(
                line=0,
                column=0,
                stack_trace=traceback.format_exc()
            )
        
        # Map exception to error code
        error_code = self._map_exception_to_error_code(exception)
        
        error = self.create_error(
            error_code=error_code,
            message=str(exception),
            context=context,
            severity=ErrorSeverity.ERROR
        )
        
        self.log_error(error)
        return error
    
    def _map_exception_to_error_code(self, exception: Exception) -> ErrorCode:
        """Map Python exception to Runa error code."""
        exception_mapping = {
            ZeroDivisionError: ErrorCode.DIVISION_BY_ZERO,
            IndexError: ErrorCode.INDEX_OUT_OF_BOUNDS,
            KeyError: ErrorCode.INDEX_OUT_OF_BOUNDS,
            TypeError: ErrorCode.TYPE_MISMATCH,
            NameError: ErrorCode.UNDEFINED_VARIABLE,
            AttributeError: ErrorCode.UNDEFINED_VARIABLE,
            FileNotFoundError: ErrorCode.FILE_NOT_FOUND,
            PermissionError: ErrorCode.PERMISSION_DENIED,
            MemoryError: ErrorCode.MEMORY_ERROR,
            RecursionError: ErrorCode.STACK_OVERFLOW
        }
        
        return exception_mapping.get(type(exception), ErrorCode.SYSTEM)
    
    def attempt_recovery(self, error: RunaError) -> bool:
        """Attempt to recover from an error."""
        recovery_strategy = self.recovery_strategies.get(error.error_code)
        
        if recovery_strategy:
            try:
                return recovery_strategy(error)
            except Exception as e:
                print(f"Recovery strategy failed: {e}")
                return False
        
        return False
    
    def _recover_unexpected_character(self, error: RunaError) -> bool:
        """Recovery strategy for unexpected character errors."""
        # Could attempt to skip the character and continue parsing
        print("Attempting to skip unexpected character...")
        return True
    
    def _recover_undefined_variable(self, error: RunaError) -> bool:
        """Recovery strategy for undefined variable errors."""
        # Could attempt to suggest similar variable names
        print("Looking for similar variable names...")
        return False
    
    def _recover_type_mismatch(self, error: RunaError) -> bool:
        """Recovery strategy for type mismatch errors."""
        # Could attempt type conversion if safe
        print("Attempting type conversion...")
        return False
    
    def _recover_unbalanced_parentheses(self, error: RunaError) -> bool:
        """Recovery strategy for unbalanced parentheses."""
        # Could attempt to add missing parentheses
        print("Attempting to balance parentheses...")
        return False
    
    def _recover_missing_token(self, error: RunaError) -> bool:
        """Recovery strategy for missing token errors."""
        # Could attempt to insert expected token
        print("Attempting to insert missing token...")
        return False
    
    def _recover_unterminated_string(self, error: RunaError) -> bool:
        """Recovery strategy for unterminated string errors."""
        # Could attempt to close the string
        print("Attempting to close unterminated string...")
        return False
    
    def generate_error_report(self, duration_hours: float = 1.0) -> ErrorReport:
        """Generate comprehensive error report."""
        report_id = f"error_report_{int(datetime.now().timestamp() * 1000)}"
        
        # Filter errors by time
        cutoff_time = datetime.now().timestamp() - (duration_hours * 3600)
        recent_errors = [e for e in self.errors_logged if e.timestamp.timestamp() >= cutoff_time]
        
        # Calculate statistics
        errors_by_severity = {}
        errors_by_category = {}
        
        for error in recent_errors:
            severity = error.severity.value
            category = error.category.value
            
            errors_by_severity[severity] = errors_by_severity.get(severity, 0) + 1
            errors_by_category[category] = errors_by_category.get(category, 0) + 1
        
        # Generate summary
        summary = f"Found {len(recent_errors)} errors in the last {duration_hours} hours"
        
        # Generate recommendations
        recommendations = self._generate_error_recommendations(recent_errors)
        
        # Create report
        report = ErrorReport(
            report_id=report_id,
            timestamp=datetime.now(),
            total_errors=len(recent_errors),
            errors_by_severity=errors_by_severity,
            errors_by_category=errors_by_category,
            errors=recent_errors,
            summary=summary,
            recommendations=recommendations
        )
        
        # Save report
        report_file = os.path.join(self.output_dir, "reports", f"{report_id}.json")
        with open(report_file, 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)
        
        return report
    
    def _generate_error_recommendations(self, errors: List[RunaError]) -> List[str]:
        """Generate recommendations based on error patterns."""
        recommendations = []
        
        # Count error types
        error_counts = {}
        for error in errors:
            error_counts[error.error_code] = error_counts.get(error.error_code, 0) + 1
        
        # Generate specific recommendations
        if error_counts.get(ErrorCode.UNDEFINED_VARIABLE, 0) > 5:
            recommendations.append("Consider using a linter to catch undefined variables before compilation")
        
        if error_counts.get(ErrorCode.TYPE_MISMATCH, 0) > 3:
            recommendations.append("Add explicit type annotations to reduce type-related errors")
        
        if error_counts.get(ErrorCode.UNBALANCED_PARENTHESES, 0) > 2:
            recommendations.append("Use an editor with bracket matching to prevent parenthesis errors")
        
        if error_counts.get(ErrorCode.UNEXPECTED_CHARACTER, 0) > 1:
            recommendations.append("Review your code for typos and invalid characters")
        
        # General recommendations
        if len(errors) > 10:
            recommendations.append("Consider breaking down complex code into smaller, more manageable functions")
        
        if not recommendations:
            recommendations.append("Your code looks good! Keep up the good work.")
        
        return recommendations
    
    def add_error_callback(self, callback: Callable[[RunaError], None]):
        """Add callback function for error handling."""
        self.error_callbacks.append(callback)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics."""
        if not self.errors_logged:
            return {"total_errors": 0, "errors_by_severity": {}, "errors_by_category": {}}
        
        errors_by_severity = {}
        errors_by_category = {}
        
        for error in self.errors_logged:
            severity = error.severity.value
            category = error.category.value
            
            errors_by_severity[severity] = errors_by_severity.get(severity, 0) + 1
            errors_by_category[category] = errors_by_category.get(category, 0) + 1
        
        return {
            "total_errors": len(self.errors_logged),
            "errors_by_severity": errors_by_severity,
            "errors_by_category": errors_by_category,
            "most_common_error": max(errors_by_category.items(), key=lambda x: x[1])[0] if errors_by_category else None
        }


# Global error handler instance
_global_error_handler = None


def get_error_handler() -> RunaErrorHandler:
    """Get global error handler instance."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = RunaErrorHandler()
    return _global_error_handler


def handle_compilation_error(error_code: ErrorCode, message: str, line: int, column: int,
                           source_file: str = None, source_line: str = None) -> RunaError:
    """Handle compilation error globally."""
    return get_error_handler().handle_compilation_error(error_code, message, line, column, source_file, source_line)


def handle_runtime_error(exception: Exception, context: ErrorContext = None) -> RunaError:
    """Handle runtime error globally."""
    return get_error_handler().handle_runtime_error(exception, context)


def main():
    """Main function to test error handling."""
    handler = RunaErrorHandler()
    
    # Test compilation error
    error = handler.handle_compilation_error(
        ErrorCode.UNDEFINED_VARIABLE,
        "Name 'x' is not defined",
        5, 10,
        "test.runa",
        "Let result be x + 5"
    )
    
    # Test runtime error
    try:
        result = 10 / 0
    except Exception as e:
        handler.handle_runtime_error(e)
    
    # Generate report
    report = handler.generate_error_report(0.1)  # Last 6 minutes
    print(f"\nGenerated error report: {report.report_id}")
    print(f"Total errors: {report.total_errors}")
    print(f"Recommendations: {len(report.recommendations)}")
    
    # Get statistics
    stats = handler.get_error_statistics()
    print(f"Error statistics: {stats}")


if __name__ == "__main__":
    main()


class RunaRuntimeError(RunaError):
    def __init__(self, message: str, context: ErrorContext, suggestions: List[str] = None):
        super().__init__(
            error_code=ErrorCode.RUNTIME,
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.ERROR,
            message=message,
            natural_language_message=message,
            context=context,
            suggestions=suggestions or [],
            timestamp=datetime.now(),
            error_id=f"runtime_{int(datetime.now().timestamp() * 1000)}"
        )

class RunaTypeError(RunaError):
    def __init__(self, message: str, context: ErrorContext, suggestions: List[str] = None):
        super().__init__(
            error_code=ErrorCode.TYPE_MISMATCH,
            category=ErrorCategory.TYPE,
            severity=ErrorSeverity.ERROR,
            message=message,
            natural_language_message=message,
            context=context,
            suggestions=suggestions or [],
            timestamp=datetime.now(),
            error_id=f"type_{int(datetime.now().timestamp() * 1000)}"
        )

class RunaVMError(RunaError):
    def __init__(self, message: str, context: ErrorContext, suggestions: List[str] = None):
        super().__init__(
            error_code=ErrorCode.STACK_OVERFLOW,
            category=ErrorCategory.RUNTIME,
            severity=ErrorSeverity.ERROR,
            message=message,
            natural_language_message=message,
            context=context,
            suggestions=suggestions or [],
            timestamp=datetime.now(),
            error_id=f"vm_{int(datetime.now().timestamp() * 1000)}"
        )

class RunaCompilationError(RunaError):
    def __init__(self, message: str, context: ErrorContext, suggestions: List[str] = None):
        super().__init__(
            error_code=ErrorCode.COMPILATION_FAILED,
            category=ErrorCategory.COMPILATION,
            severity=ErrorSeverity.ERROR,
            message=message,
            natural_language_message=message,
            context=context,
            suggestions=suggestions or [],
            timestamp=datetime.now(),
            error_id=f"compilation_{int(datetime.now().timestamp() * 1000)}"
        ) 