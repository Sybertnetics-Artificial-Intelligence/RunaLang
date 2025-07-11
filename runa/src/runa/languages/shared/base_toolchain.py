#!/usr/bin/env python3
"""
Base Language Toolchain

Abstract base class and common functionality for all language toolchains
in the Runa universal translation system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import time
import hashlib

from ...core.runa_ast import Program
from ...core.translation_result import TranslationResult, TranslationError


@dataclass
class ToolchainResult:
    """Generic result from toolchain operations."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RoundTripResult:
    """Result from round-trip translation verification."""
    success: bool
    original_ast: Optional[Any] = None
    runa_ast: Optional[Program] = None
    regenerated_ast: Optional[Any] = None
    original_code: Optional[str] = None
    regenerated_code: Optional[str] = None
    syntax_preserved: bool = False
    semantics_preserved: bool = False
    differences: List[str] = field(default_factory=list)
    similarity_score: float = 0.0


@dataclass
class LanguageMetadata:
    """Metadata about a programming language."""
    name: str
    id: str
    tier: int
    file_extensions: List[str]
    mime_types: List[str] = field(default_factory=list)
    features: Dict[str, bool] = field(default_factory=dict)
    description: str = ""
    homepage: str = ""
    specification: str = ""


class BaseLanguageToolchain(ABC):
    """Abstract base class for all language toolchains."""
    
    def __init__(self, language_id: str, version: str = "1.0.0"):
        self.language_id = language_id
        self.version = version
        
        # Statistics tracking
        self.parser_stats = {
            "files_parsed": 0,
            "parse_errors": 0,
            "lines_parsed": 0,
            "total_parse_time_ms": 0,
        }
        
        self.conversion_stats = {
            "to_runa_conversions": 0,
            "from_runa_conversions": 0,
            "conversion_errors": 0,
            "total_conversion_time_ms": 0,
        }
        
        self.generation_stats = {
            "files_generated": 0,
            "lines_generated": 0,
            "generation_errors": 0,
            "total_generation_time_ms": 0,
        }
        
        # Caching
        self._parse_cache = {}
        self._conversion_cache = {}
        self.cache_enabled = True
        self.max_cache_size = 1000
    
    @property
    @abstractmethod
    def metadata(self) -> LanguageMetadata:
        """Get language metadata."""
        pass
    
    @property
    @abstractmethod
    def supported_features(self) -> Dict[str, bool]:
        """Get supported language features."""
        pass
    
    # Core toolchain methods
    @abstractmethod
    def parse(self, source_code: str, file_path: Optional[str] = None) -> ToolchainResult:
        """Parse source code into language-specific AST."""
        pass
    
    @abstractmethod
    def to_runa(self, language_ast: Any) -> TranslationResult:
        """Convert language AST to Runa AST."""
        pass
    
    @abstractmethod
    def from_runa(self, runa_ast: Program) -> TranslationResult:
        """Convert Runa AST to language AST."""
        pass
    
    @abstractmethod
    def generate(self, language_ast: Any, **options) -> ToolchainResult:
        """Generate source code from language AST."""
        pass
    
    # Common functionality
    def round_trip_verify(self, source_code: str, **options) -> RoundTripResult:
        """Perform round-trip translation verification."""
        start_time = time.time()
        
        try:
            # Step 1: Parse original source
            parse_result = self.parse(source_code)
            if not parse_result.success:
                return RoundTripResult(
                    success=False,
                    differences=[f"Failed to parse original code: {parse_result.error}"]
                )
            
            original_ast = parse_result.data
            
            # Step 2: Convert to Runa
            to_runa_result = self.to_runa(original_ast)
            if not to_runa_result.success:
                return RoundTripResult(
                    success=False,
                    original_ast=original_ast,
                    differences=[f"Failed to convert to Runa: {to_runa_result.error}"]
                )
            
            runa_ast = to_runa_result.target_ast
            
            # Step 3: Convert back to original language
            from_runa_result = self.from_runa(runa_ast)
            if not from_runa_result.success:
                return RoundTripResult(
                    success=False,
                    original_ast=original_ast,
                    runa_ast=runa_ast,
                    differences=[f"Failed to convert from Runa: {from_runa_result.error}"]
                )
            
            regenerated_ast = from_runa_result.target_ast
            
            # Step 4: Generate code from regenerated AST
            gen_result = self.generate(regenerated_ast, **options)
            if not gen_result.success:
                return RoundTripResult(
                    success=False,
                    original_ast=original_ast,
                    runa_ast=runa_ast,
                    regenerated_ast=regenerated_ast,
                    differences=[f"Failed to generate code: {gen_result.error}"]
                )
            
            regenerated_code = gen_result.data
            
            # Step 5: Compare results
            syntax_preserved = self._compare_ast_structure(original_ast, regenerated_ast)
            semantics_preserved = self._compare_semantics(original_ast, regenerated_ast)
            differences = self._find_differences(original_ast, regenerated_ast)
            similarity_score = self._calculate_similarity(source_code, regenerated_code)
            
            success = syntax_preserved and semantics_preserved and len(differences) == 0
            
            return RoundTripResult(
                success=success,
                original_ast=original_ast,
                runa_ast=runa_ast,
                regenerated_ast=regenerated_ast,
                original_code=source_code,
                regenerated_code=regenerated_code,
                syntax_preserved=syntax_preserved,
                semantics_preserved=semantics_preserved,
                differences=differences,
                similarity_score=similarity_score
            )
            
        except Exception as e:
            return RoundTripResult(
                success=False,
                differences=[f"Round-trip verification failed: {str(e)}"]
            )
    
    def validate_syntax(self, source_code: str) -> Dict[str, Any]:
        """Validate source code syntax."""
        parse_result = self.parse(source_code)
        
        return {
            "valid": parse_result.success,
            "error": parse_result.error if not parse_result.success else None,
            "warnings": [],
            "features_used": self._detect_features(parse_result.data) if parse_result.success else [],
            "complexity_score": self._calculate_complexity(parse_result.data) if parse_result.success else 0,
            "language": self.language_id,
        }
    
    def compile_to_target(self, source_code: str, target_language: str) -> TranslationResult:
        """Compile source code to another target language via Runa."""
        # Parse source
        parse_result = self.parse(source_code)
        if not parse_result.success:
            return TranslationResult(
                success=False,
                source_language=self.language_id,
                target_language=target_language,
                error=TranslationError(
                    error_type="parse_error",
                    message=parse_result.error
                )
            )
        
        # Convert to Runa
        to_runa_result = self.to_runa(parse_result.data)
        if not to_runa_result.success:
            return to_runa_result
        
        # Return intermediate result (target toolchain will handle final conversion)
        return TranslationResult(
            success=True,
            source_language=self.language_id,
            target_language="runa",  # Intermediate
            source_ast=parse_result.data,
            target_ast=to_runa_result.target_ast,
            metadata={
                "intermediate_conversion": True,
                "final_target": target_language
            }
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get toolchain statistics."""
        return {
            "language": self.language_id,
            "version": self.version,
            "parser": self.parser_stats.copy(),
            "conversion": self.conversion_stats.copy(),
            "generation": self.generation_stats.copy(),
            "supported_features": self.supported_features.copy(),
            "cache": {
                "enabled": self.cache_enabled,
                "parse_cache_size": len(self._parse_cache),
                "conversion_cache_size": len(self._conversion_cache),
            }
        }
    
    def clear_cache(self):
        """Clear all caches."""
        self._parse_cache.clear()
        self._conversion_cache.clear()
    
    # Protected helper methods
    def _get_cache_key(self, data: str) -> str:
        """Generate cache key for data."""
        return hashlib.md5(data.encode()).hexdigest()
    
    def _update_parse_stats(self, lines: int, time_ms: float, success: bool):
        """Update parser statistics."""
        self.parser_stats["files_parsed"] += 1
        self.parser_stats["lines_parsed"] += lines
        self.parser_stats["total_parse_time_ms"] += time_ms
        if not success:
            self.parser_stats["parse_errors"] += 1
    
    def _update_conversion_stats(self, time_ms: float, success: bool, direction: str):
        """Update conversion statistics."""
        if direction == "to_runa":
            self.conversion_stats["to_runa_conversions"] += 1
        else:
            self.conversion_stats["from_runa_conversions"] += 1
        
        self.conversion_stats["total_conversion_time_ms"] += time_ms
        if not success:
            self.conversion_stats["conversion_errors"] += 1
    
    def _update_generation_stats(self, lines: int, time_ms: float, success: bool):
        """Update generation statistics."""
        self.generation_stats["files_generated"] += 1
        self.generation_stats["lines_generated"] += lines
        self.generation_stats["total_generation_time_ms"] += time_ms
        if not success:
            self.generation_stats["generation_errors"] += 1
    
    # Abstract methods for subclasses to implement
    @abstractmethod
    def _compare_ast_structure(self, ast1: Any, ast2: Any) -> bool:
        """Compare AST structure for syntax preservation."""
        pass
    
    @abstractmethod
    def _compare_semantics(self, ast1: Any, ast2: Any) -> bool:
        """Compare AST semantics."""
        pass
    
    @abstractmethod
    def _find_differences(self, ast1: Any, ast2: Any) -> List[str]:
        """Find differences between ASTs."""
        pass
    
    @abstractmethod
    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity score between code strings."""
        pass
    
    @abstractmethod
    def _detect_features(self, ast: Any) -> List[str]:
        """Detect language features used in AST."""
        pass
    
    @abstractmethod
    def _calculate_complexity(self, ast: Any) -> int:
        """Calculate complexity score of AST."""
        pass