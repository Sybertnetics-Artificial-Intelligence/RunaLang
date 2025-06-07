"""
Comprehensive error handling system for Runa Programming Language.

This module provides a complete hierarchy of error types with detailed
error reporting, source position tracking, and user-friendly messages.
"""

from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels for categorizing different types of errors."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class SourcePosition:
    """Represents a position in source code for error reporting."""
    line: int
    column: int
    filename: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of source position."""
        location = f"line {self.line}, column {self.column}"
        if self.filename:
            location = f"{self.filename}:{location}"
        return location


@dataclass
class ErrorContext:
    """Additional context information for error reporting."""
    source_line: Optional[str] = None
    surrounding_lines: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    related_errors: Optional[List["RunaError"]] = None


class RunaError(Exception):
    """Base class for all Runa programming language errors."""
    
    def __init__(
        self,
        message: str,
        position: Optional[SourcePosition] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        error_code: Optional[str] = None,
        context: Optional[ErrorContext] = None,
    ) -> None:
        self.message = message
        self.position = position
        self.severity = severity
        self.error_code = error_code or self._generate_error_code()
        self.context = context or ErrorContext()
        super().__init__(self.get_detailed_message())
    
    def _generate_error_code(self) -> str:
        """Generate a unique error code based on error type."""
        return f"RUNA_{self.__class__.__name__.upper()}"
    
    def get_detailed_message(self) -> str:
        """Generate a detailed error message with all available context."""
        parts = []
        
        # Error header
        if self.position:
            parts.append(f"{self.severity.value.upper()} at {self.position}")
        else:
            parts.append(f"{self.severity.value.upper()}")
        
        # Error code and message
        parts.append(f"[{self.error_code}] {self.message}")
        
        return "\n".join(parts)


class RunaSyntaxError(RunaError):
    """Syntax errors in Runa source code."""
    
    def _generate_error_code(self) -> str:
        """Generate specific syntax error code."""
        return "RUNA_SYNTAX_ERROR"


class RunaSemanticError(RunaError):
    """Semantic errors in Runa source code."""
    
    def _generate_error_code(self) -> str:
        """Generate specific semantic error code."""
        return "RUNA_SEMANTIC_ERROR"


class RunaTypeError(RunaError):
    """Type errors in Runa source code."""
    
    def _generate_error_code(self) -> str:
        """Generate specific type error code."""
        return "RUNA_TYPE_ERROR"


class RunaRuntimeError(RunaError):
    """Runtime errors in Runa source code."""
    
    def _generate_error_code(self) -> str:
        """Generate specific runtime error code."""
        return "RUNA_RUNTIME_ERROR"


class ErrorReporter:
    """Centralized error reporting and collection system."""
    
    def __init__(self, max_errors: int = 100) -> None:
        self.errors: List[RunaError] = []
        self.warnings: List[RunaError] = []
        self.max_errors = max_errors
    
    def report_error(self, error: RunaError) -> None:
        """Report an error to the collection."""
        if error.severity == ErrorSeverity.WARNING:
            self.warnings.append(error)
        else:
            self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Check if any errors have been reported."""
        return len(self.errors) > 0


def syntax_error(
    message: str,
    line: int,
    column: int,
    filename: Optional[str] = None,
    expected: Optional[str] = None,
    actual: Optional[str] = None,
    suggestions: Optional[List[str]] = None,
) -> RunaSyntaxError:
    """Create a syntax error with position and context."""
    position = SourcePosition(line, column, filename)
    context = ErrorContext(suggestions=suggestions)
    return RunaSyntaxError(message, position, context=context)


def semantic_error(
    message: str,
    position: SourcePosition,
    note: str = "",
    severity: ErrorSeverity = ErrorSeverity.ERROR,
) -> RunaSemanticError:
    """Create a semantic error with position and context."""
    context = ErrorContext(suggestions=[note] if note else None)
    return RunaSemanticError(message, position, severity, context=context)
