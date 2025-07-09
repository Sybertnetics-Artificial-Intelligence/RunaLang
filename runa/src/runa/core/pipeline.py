"""
Runa Translation Pipeline Orchestrator

This is the central orchestrator for the hub-and-spoke translation system.
It manages the complete workflow:

source_lang_code -> Parser -> lang_AST_1
lang_AST_1 -> Converter -> Runa_AST_1
Runa_AST_1 -> Runa Text Generator -> runa_code
runa_code -> Runa Parser -> Runa_AST_2
Runa_AST_2 -> Converter -> target_lang_AST_1
target_lang_AST_1 -> Text Generator -> target_lang_code

Key Features:
- Orchestrates the complete translation pipeline
- Provides verification at each checkpoint
- Supports debugging with detailed error reporting
- Manages language-specific toolchain registration
- Handles translation metadata and confidence scoring
"""

from typing import Dict, List, Optional, Any, Tuple, Protocol, runtime_checkable
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod
import logging
from datetime import datetime
import time

from .runa_ast import ASTNode, SourceLocation, TranslationMetadata
from .verification import VerificationResult, PipelineVerifier, VerificationReporter


class PipelineStage(Enum):
    """Stages in the translation pipeline."""
    SOURCE_CODE = auto()           # Original source code
    SOURCE_AST = auto()           # Language-specific AST
    RUNA_AST_CHECKPOINT_1 = auto() # First Runa AST (from source)
    RUNA_CODE = auto()            # Generated Runa code
    RUNA_AST_CHECKPOINT_2 = auto() # Second Runa AST (from generated code)
    TARGET_AST = auto()           # Target language AST
    TARGET_CODE = auto()          # Final target language code


@dataclass
class PipelineCheckpoint:
    """A checkpoint in the translation pipeline."""
    stage: PipelineStage
    content: Any  # Could be code string or AST
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_ast(self) -> bool:
        """Check if this checkpoint contains an AST."""
        return isinstance(self.content, ASTNode)
    
    def is_code(self) -> bool:
        """Check if this checkpoint contains source code."""
        return isinstance(self.content, str)


@dataclass
class TranslationResult:
    """Result of a complete translation."""
    success: bool
    source_language: str
    target_language: str
    source_code: str
    target_code: Optional[str] = None
    checkpoints: List[PipelineCheckpoint] = field(default_factory=list)
    verification_results: Dict[str, VerificationResult] = field(default_factory=dict)
    error_message: Optional[str] = None
    total_time_ms: float = 0.0
    confidence_score: float = 0.0
    
    def get_checkpoint(self, stage: PipelineStage) -> Optional[PipelineCheckpoint]:
        """Get a specific checkpoint by stage."""
        for checkpoint in self.checkpoints:
            if checkpoint.stage == stage:
                return checkpoint
        return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the translation result."""
        return {
            "success": self.success,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "total_time_ms": self.total_time_ms,
            "confidence_score": self.confidence_score,
            "checkpoints_count": len(self.checkpoints),
            "verification_results": {k: v.is_identical for k, v in self.verification_results.items()},
            "error_message": self.error_message
        }


# Protocol definitions for language toolchains
@runtime_checkable
class LanguageParser(Protocol):
    """Protocol for language-specific parsers."""
    
    def parse(self, source_code: str, file_path: str = "") -> ASTNode:
        """Parse source code into language-specific AST."""
        ...


@runtime_checkable
class LanguageConverter(Protocol):
    """Protocol for bidirectional AST converters."""
    
    def to_runa_ast(self, language_ast: ASTNode) -> ASTNode:
        """Convert language-specific AST to Runa AST."""
        ...
    
    def from_runa_ast(self, runa_ast: ASTNode) -> ASTNode:
        """Convert Runa AST to language-specific AST."""
        ...


@runtime_checkable
class LanguageGenerator(Protocol):
    """Protocol for language-specific code generators."""
    
    def generate(self, language_ast: ASTNode) -> str:
        """Generate source code from language-specific AST."""
        ...


@dataclass
class LanguageToolchain:
    """Complete toolchain for a specific language."""
    name: str
    parser: LanguageParser
    converter: LanguageConverter
    generator: LanguageGenerator
    version: str = "1.0.0"
    
    def validate(self) -> bool:
        """Validate that all components are present and implement required protocols."""
        return (
            isinstance(self.parser, LanguageParser) and
            isinstance(self.converter, LanguageConverter) and
            isinstance(self.generator, LanguageGenerator)
        )


class TranslationPipeline:
    """Main translation pipeline orchestrator."""
    
    def __init__(self):
        self.toolchains: Dict[str, LanguageToolchain] = {}
        self.verifier = PipelineVerifier()
        self.logger = logging.getLogger(__name__)
        
        # Runa toolchain will be registered separately
        self.runa_parser: Optional[LanguageParser] = None
        self.runa_generator: Optional[LanguageGenerator] = None
    
    def register_toolchain(self, toolchain: LanguageToolchain) -> None:
        """Register a language toolchain."""
        if not toolchain.validate():
            raise ValueError(f"Invalid toolchain for {toolchain.name}: missing required components")
        
        self.toolchains[toolchain.name] = toolchain
        self.logger.info(f"Registered toolchain for {toolchain.name} v{toolchain.version}")
    
    def register_runa_toolchain(self, parser: LanguageParser, generator: LanguageGenerator) -> None:
        """Register the Runa language toolchain (special case)."""
        self.runa_parser = parser
        self.runa_generator = generator
        self.logger.info("Registered Runa language toolchain")
    
    def list_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self.toolchains.keys())
    
    def is_language_supported(self, language: str) -> bool:
        """Check if a language is supported."""
        return language.lower() in [lang.lower() for lang in self.toolchains.keys()]
    
    def translate(self, source_code: str, source_language: str, target_language: str,
                 file_path: str = "", verify_round_trip: bool = True) -> TranslationResult:
        """
        Perform complete translation from source language to target language.
        
        Args:
            source_code: Source code to translate
            source_language: Source language name (e.g., "python")
            target_language: Target language name (e.g., "javascript")
            file_path: Original file path for source location tracking
            verify_round_trip: Whether to perform round-trip verification
            
        Returns:
            TranslationResult with complete pipeline information
        """
        start_time = time.time()
        
        result = TranslationResult(
            success=False,
            source_language=source_language,
            target_language=target_language,
            source_code=source_code
        )
        
        try:
            # Validate languages are supported
            if not self.is_language_supported(source_language):
                raise ValueError(f"Unsupported source language: {source_language}")
            
            if not self.is_language_supported(target_language):
                raise ValueError(f"Unsupported target language: {target_language}")
            
            if not self.runa_parser or not self.runa_generator:
                raise ValueError("Runa toolchain not registered")
            
            # Step 1: Parse source code -> source AST
            source_toolchain = self.toolchains[source_language]
            source_ast = source_toolchain.parser.parse(source_code, file_path)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.SOURCE_AST,
                content=source_ast,
                metadata={"language": source_language}
            ))
            
            # Step 2: Convert source AST -> Runa AST (checkpoint 1)
            runa_ast_1 = source_toolchain.converter.to_runa_ast(source_ast)
            runa_ast_1.metadata.source_language = source_language
            runa_ast_1.metadata.target_language = target_language
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.RUNA_AST_CHECKPOINT_1,
                content=runa_ast_1,
                metadata={"source_language": source_language}
            ))
            
            # Step 3: Generate Runa code from Runa AST
            runa_code = self.runa_generator.generate(runa_ast_1)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.RUNA_CODE,
                content=runa_code,
                metadata={"generated_from": "runa_ast_1"}
            ))
            
            # Step 4: Parse Runa code -> Runa AST (checkpoint 2)
            runa_ast_2 = self.runa_parser.parse(runa_code, f"generated_{file_path}.runa")
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.RUNA_AST_CHECKPOINT_2,
                content=runa_ast_2,
                metadata={"source": "runa_code"}
            ))
            
            # Step 5: Verify round-trip if requested
            if verify_round_trip:
                verification_result = self.verifier.verify_round_trip(runa_ast_1, runa_ast_2)
                result.verification_results["runa_round_trip"] = verification_result
                
                if not verification_result.is_identical:
                    self.logger.warning(f"Round-trip verification failed: {len(verification_result.differences)} differences")
                    # Continue with translation but reduce confidence
                    result.confidence_score = max(0.0, result.confidence_score - 0.3)
            
            # Step 6: Convert Runa AST -> target AST
            target_toolchain = self.toolchains[target_language]
            target_ast = target_toolchain.converter.from_runa_ast(runa_ast_2)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.TARGET_AST,
                content=target_ast,
                metadata={"target_language": target_language}
            ))
            
            # Step 7: Generate target code from target AST
            target_code = target_toolchain.generator.generate(target_ast)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.TARGET_CODE,
                content=target_code,
                metadata={"language": target_language}
            ))
            
            # Set final result
            result.target_code = target_code
            result.success = True
            result.confidence_score = max(result.confidence_score, 0.8)  # Base confidence
            
        except Exception as e:
            result.error_message = str(e)
            result.success = False
            self.logger.error(f"Translation failed: {e}")
        
        finally:
            end_time = time.time()
            result.total_time_ms = (end_time - start_time) * 1000
        
        return result
    
    def translate_to_runa(self, source_code: str, source_language: str, 
                         file_path: str = "") -> TranslationResult:
        """
        Translate source code to Runa language.
        
        This is a simplified pipeline that stops at Runa generation.
        """
        return self.translate(source_code, source_language, "runa", file_path, verify_round_trip=False)
    
    def translate_from_runa(self, runa_code: str, target_language: str, 
                          file_path: str = "") -> TranslationResult:
        """
        Translate Runa code to target language.
        
        This starts from Runa code rather than another language.
        """
        start_time = time.time()
        
        result = TranslationResult(
            success=False,
            source_language="runa",
            target_language=target_language,
            source_code=runa_code
        )
        
        try:
            if not self.is_language_supported(target_language):
                raise ValueError(f"Unsupported target language: {target_language}")
            
            if not self.runa_parser:
                raise ValueError("Runa parser not registered")
            
            # Parse Runa code -> Runa AST
            runa_ast = self.runa_parser.parse(runa_code, file_path)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.RUNA_AST_CHECKPOINT_1,
                content=runa_ast,
                metadata={"source": "runa_code"}
            ))
            
            # Convert Runa AST -> target AST
            target_toolchain = self.toolchains[target_language]
            target_ast = target_toolchain.converter.from_runa_ast(runa_ast)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.TARGET_AST,
                content=target_ast,
                metadata={"target_language": target_language}
            ))
            
            # Generate target code
            target_code = target_toolchain.generator.generate(target_ast)
            result.checkpoints.append(PipelineCheckpoint(
                stage=PipelineStage.TARGET_CODE,
                content=target_code,
                metadata={"language": target_language}
            ))
            
            result.target_code = target_code
            result.success = True
            result.confidence_score = 0.9
            
        except Exception as e:
            result.error_message = str(e)
            result.success = False
            self.logger.error(f"Translation from Runa failed: {e}")
        
        finally:
            end_time = time.time()
            result.total_time_ms = (end_time - start_time) * 1000
        
        return result
    
    def verify_toolchain(self, language: str, test_code: str) -> Dict[str, Any]:
        """
        Verify a language toolchain with round-trip testing.
        
        This tests: code -> AST -> Runa AST -> Runa code -> Runa AST -> target AST -> code
        """
        if not self.is_language_supported(language):
            return {"success": False, "error": f"Language {language} not supported"}
        
        try:
            # Perform round-trip translation
            result = self.translate(test_code, language, language, verify_round_trip=True)
            
            # Additional verification: compare original and final code
            code_identical = result.source_code.strip() == (result.target_code or "").strip()
            
            return {
                "success": result.success,
                "code_identical": code_identical,
                "verification_results": {k: v.is_identical for k, v in result.verification_results.items()},
                "confidence_score": result.confidence_score,
                "total_time_ms": result.total_time_ms,
                "checkpoints_count": len(result.checkpoints),
                "error_message": result.error_message
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global pipeline instance
pipeline = TranslationPipeline()


def get_pipeline() -> TranslationPipeline:
    """Get the global translation pipeline instance."""
    return pipeline


def translate_code(source_code: str, source_language: str, target_language: str, 
                  file_path: str = "") -> TranslationResult:
    """Convenience function for code translation."""
    return pipeline.translate(source_code, source_language, target_language, file_path)


def register_language_toolchain(toolchain: LanguageToolchain) -> None:
    """Convenience function for registering language toolchains."""
    pipeline.register_toolchain(toolchain)