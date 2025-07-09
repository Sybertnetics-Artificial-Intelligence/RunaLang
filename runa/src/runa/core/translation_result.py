#!/usr/bin/env python3
"""
Translation Result Classes

Classes for representing translation results and errors in the
Runa universal translation system.
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class TranslationError:
    """Translation error information."""
    error_type: str
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}


@dataclass
class TranslationResult:
    """Result of a translation operation."""
    success: bool
    source_language: str
    target_language: str
    
    # ASTs
    source_ast: Optional[Any] = None
    target_ast: Optional[Any] = None
    
    # Generated code
    source_code: Optional[str] = None
    target_code: Optional[str] = None
    
    # Error information
    error: Optional[TranslationError] = None
    warnings: List[str] = field(default_factory=list)
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ValidationResult:
    """Result of code validation."""
    valid: bool
    language: str
    errors: List[TranslationError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CompilationResult:
    """Result of a compilation operation."""
    success: bool
    source_files: List[str]
    target_files: List[str] = field(default_factory=list)
    errors: List[TranslationError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}