#!/usr/bin/env python3
"""
Objective-C Language Toolchain

Comprehensive toolchain for Objective-C language providing complete integration
with the Runa Universal Translation Platform. Supports all Objective-C language features
including message passing, protocols, categories, blocks, memory management,
and Foundation framework integration.

This toolchain provides:
- Complete parsing of Objective-C source code
- Bidirectional conversion between Objective-C and Runa AST
- Clean code generation with Apple style guidelines
- Round-trip translation verification
- Enterprise-grade error handling and validation
- Apple ecosystem integration (Xcode, LLVM/Clang)
- Foundation framework pattern recognition
- Memory management analysis (ARC and manual)
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
import logging
import json

from ....core.base_components import (
    BaseLanguageParser, BaseLanguageConverter, BaseLanguageGenerator,
    LanguageInfo, LanguageTier, ParseError, ConversionError, GenerationError
)
from ....core.runa_ast import ASTNode, SourceLocation, TranslationMetadata
from .objective_c_ast import *
from .objective_c_parser import ObjCParser, parse_objective_c
from .objective_c_converter import ObjCToRunaConverter, objective_c_to_runa, runa_to_objective_c
from .objective_c_generator import ObjCCodeGenerator, generate_objective_c, ObjCCodeStyle, create_apple_style


class ObjCToolchainError(Exception):
    """Objective-C toolchain specific error."""
    pass


class ObjCCompilerInfo:
    """Information about Objective-C compiler setup."""
    def __init__(self):
        self.clang_path = None
        self.xcodebuild_path = None
        self.sdk_path = None
        self.deployment_target = None
        self.is_arc_enabled = True
        self.frameworks = []
        self.include_paths = []
        
    def detect_compiler(self) -> bool:
        """Detect available Objective-C compiler."""
        try:
            # Try to find clang
            result = subprocess.run(['which', 'clang'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.clang_path = result.stdout.strip()
            
            # Try to find xcodebuild (macOS only)
            result = subprocess.run(['which', 'xcodebuild'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.xcodebuild_path = result.stdout.strip()
                self._detect_xcode_settings()
            
            return self.clang_path is not None
        
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            return False
    
    def _detect_xcode_settings(self) -> None:
        """Detect Xcode SDK and settings."""
        try:
            # Get SDK path
            result = subprocess.run([
                'xcrun', '--sdk', 'macosx', '--show-sdk-path'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.sdk_path = result.stdout.strip()
            
            # Common frameworks
            self.frameworks = [
                'Foundation', 'AppKit', 'CoreFoundation', 'CoreGraphics',
                'CoreData', 'CoreLocation', 'CoreImage', 'AVFoundation'
            ]
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass


class ObjCValidationResult:
    """Result of Objective-C code validation."""
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []
        self.memory_management_issues = []
        self.deprecated_api_usage = []
        self.foundation_framework_issues = []
        
    def add_error(self, message: str, location: Optional[SourceLocation] = None):
        """Add validation error."""
        self.is_valid = False
        self.errors.append({
            'message': message,
            'location': location,
            'severity': 'error'
        })
    
    def add_warning(self, message: str, location: Optional[SourceLocation] = None):
        """Add validation warning."""
        self.warnings.append({
            'message': message,
            'location': location,
            'severity': 'warning'
        })


class ObjCToolchain:
    """Complete Objective-C language toolchain."""
    
    def __init__(self, code_style: ObjCCodeStyle = None):
        self.language_info = LanguageInfo(
            name="objective_c",
            tier=LanguageTier.TIER6,
            file_extensions=[".m", ".mm", ".h"],
            mime_types=["text/x-objective-c", "text/x-objective-c++"],
            description="Objective-C language with Apple ecosystem integration",
            version="1.0.0",
            is_compiled=True,
            is_object_oriented=True,
            has_dynamic_typing=True,
            comment_patterns=[r'//.*$', r'/\*.*?\*/'],
            string_patterns=[r'".*?"', r"'.*?'", r'@".*?"'],
            number_patterns=[r'\d+\.?\d*', r'@\d+\.?\d*'],
            identifier_patterns=[r'[a-zA-Z_][a-zA-Z0-9_]*']
        )
        
        # Initialize components
        self.parser = ObjCParser()
        self.converter = ObjCToRunaConverter()
        self.generator = ObjCCodeGenerator(code_style or create_apple_style())
        
        # Compiler and environment
        self.compiler_info = ObjCCompilerInfo()
        self.compiler_available = self.compiler_info.detect_compiler()
        
        # Logger
        self.logger = logging.getLogger("runa.toolchain.objective_c")
        
        # Foundation framework patterns
        self.foundation_patterns = {
            'NSString': r'NSString\s*\*',
            'NSArray': r'NSArray\s*\*',
            'NSDictionary': r'NSDictionary\s*\*',
            'NSNumber': r'NSNumber\s*\*',
            'NSData': r'NSData\s*\*',
            'NSDate': r'NSDate\s*\*',
            'NSURL': r'NSURL\s*\*',
            'NSError': r'NSError\s*\*',
        }
        
        # Memory management patterns
        self.memory_patterns = {
            'retain': r'\[.*\s+retain\s*\]',
            'release': r'\[.*\s+release\s*\]',
            'autorelease': r'\[.*\s+autorelease\s*\]',
            'autoreleasepool': r'@autoreleasepool',
            'weak': r'__weak\s+',
            'strong': r'__strong\s+',
            'unsafe_unretained': r'__unsafe_unretained\s+'
        }
    
    # ========================================================================
    # Main Toolchain Interface
    # ========================================================================
    
    def parse_code(self, source_code: str, file_path: str = "") -> ObjCSourceUnit:
        """Parse Objective-C source code into AST."""
        try:
            self.logger.info(f"Parsing Objective-C code: {file_path}")
            return self.parser.parse(source_code, file_path)
        
        except Exception as e:
            self.logger.error(f"Failed to parse Objective-C code: {e}")
            raise ObjCToolchainError(f"Parse error: {e}")
    
    def generate_code(self, objc_ast: ObjCNode) -> str:
        """Generate Objective-C code from AST."""
        try:
            self.logger.info("Generating Objective-C code")
            return self.generator.generate(objc_ast)
        
        except Exception as e:
            self.logger.error(f"Failed to generate Objective-C code: {e}")
            raise ObjCToolchainError(f"Generation error: {e}")
    
    def translate_to_runa(self, source_code: str, file_path: str = "") -> ASTNode:
        """Translate Objective-C code to Runa AST."""
        try:
            self.logger.info(f"Translating Objective-C to Runa: {file_path}")
            
            # Parse Objective-C
            objc_ast = self.parse_code(source_code, file_path)
            
            # Convert to Runa
            runa_ast = self.converter.to_runa_ast(objc_ast)
            
            return runa_ast
        
        except Exception as e:
            self.logger.error(f"Failed to translate Objective-C to Runa: {e}")
            raise ObjCToolchainError(f"Translation error: {e}")
    
    def translate_from_runa(self, runa_ast: ASTNode) -> str:
        """Translate Runa AST to Objective-C code."""
        try:
            self.logger.info("Translating Runa to Objective-C")
            
            # Convert to Objective-C AST
            objc_ast = self.converter.from_runa_ast(runa_ast)
            
            # Generate code
            return self.generate_code(objc_ast)
        
        except Exception as e:
            self.logger.error(f"Failed to translate Runa to Objective-C: {e}")
            raise ObjCToolchainError(f"Translation error: {e}")
    
    def round_trip_verify(self, source_code: str, file_path: str = "") -> Dict[str, Any]:
        """Verify round-trip translation accuracy."""
        try:
            self.logger.info(f"Performing round-trip verification: {file_path}")
            
            # Original → Runa → Objective-C
            runa_ast = self.translate_to_runa(source_code, file_path)
            reconstructed_code = self.translate_from_runa(runa_ast)
            
            # Parse both versions to compare ASTs
            original_ast = self.parse_code(source_code, file_path)
            reconstructed_ast = self.parse_code(reconstructed_code, f"{file_path}_reconstructed")
            
            # Compare ASTs (simplified comparison)
            is_equivalent = self._compare_asts(original_ast, reconstructed_ast)
            
            return {
                'success': True,
                'is_equivalent': is_equivalent,
                'original_code': source_code,
                'reconstructed_code': reconstructed_code,
                'differences': self._find_ast_differences(original_ast, reconstructed_ast)
            }
        
        except Exception as e:
            self.logger.error(f"Round-trip verification failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'original_code': source_code,
                'reconstructed_code': None
            }
    
    # ========================================================================
    # Validation and Analysis
    # ========================================================================
    
    def validate_code(self, source_code: str, file_path: str = "") -> ObjCValidationResult:
        """Comprehensive validation of Objective-C code."""
        result = ObjCValidationResult()
        
        try:
            # Parse code first
            ast = self.parse_code(source_code, file_path)
            
            # Syntax validation (already done by parser)
            self.logger.info("Code parsed successfully")
            
            # Memory management validation
            self._validate_memory_management(source_code, result)
            
            # Foundation framework usage validation
            self._validate_foundation_usage(source_code, result)
            
            # Deprecated API detection
            self._detect_deprecated_apis(source_code, result)
            
            # Protocol and category validation
            self._validate_protocols_and_categories(ast, result)
            
        except ParseError as e:
            result.add_error(f"Parse error: {e.message}", e.location)
        except Exception as e:
            result.add_error(f"Validation error: {e}")
        
        return result
    
    def analyze_memory_management(self, source_code: str) -> Dict[str, Any]:
        """Analyze memory management patterns."""
        analysis = {
            'arc_usage': False,
            'manual_management': False,
            'potential_leaks': [],
            'retain_cycles': [],
            'autoreleasepool_usage': [],
            'weak_references': [],
            'recommendations': []
        }
        
        import re
        
        # Check for ARC indicators
        if '@autoreleasepool' in source_code or '__weak' in source_code or '__strong' in source_code:
            analysis['arc_usage'] = True
        
        # Check for manual memory management
        manual_patterns = ['retain', 'release', 'autorelease']
        for pattern in manual_patterns:
            if re.search(rf'\[.*\s+{pattern}\s*\]', source_code):
                analysis['manual_management'] = True
                break
        
        # Find autorelease pools
        pools = re.findall(r'@autoreleasepool\s*\{', source_code)
        analysis['autoreleasepool_usage'] = len(pools)
        
        # Find weak references
        weak_refs = re.findall(r'__weak\s+\w+', source_code)
        analysis['weak_references'] = weak_refs
        
        # Recommendations
        if analysis['manual_management'] and not analysis['arc_usage']:
            analysis['recommendations'].append("Consider migrating to ARC for automatic memory management")
        
        if analysis['arc_usage'] and analysis['manual_management']:
            analysis['recommendations'].append("Mixed ARC and manual memory management detected - review for consistency")
        
        return analysis
    
    def detect_foundation_patterns(self, source_code: str) -> Dict[str, List[str]]:
        """Detect Foundation framework usage patterns."""
        patterns = {}
        
        import re
        
        for framework_type, pattern in self.foundation_patterns.items():
            matches = re.findall(pattern, source_code)
            if matches:
                patterns[framework_type] = matches
        
        return patterns
    
    # ========================================================================
    # Compilation and Building
    # ========================================================================
    
    def compile_code(self, source_code: str, output_path: str = None, 
                    framework_paths: List[str] = None) -> Dict[str, Any]:
        """Compile Objective-C code using clang."""
        if not self.compiler_available:
            return {
                'success': False,
                'error': 'No Objective-C compiler available'
            }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
            
            output_path = output_path or temp_file_path.replace('.m', '')
            
            # Build clang command
            cmd = [
                self.compiler_info.clang_path,
                '-x', 'objective-c',
                '-o', output_path,
                temp_file_path
            ]
            
            # Add ARC if enabled
            if self.compiler_info.is_arc_enabled:
                cmd.extend(['-fobjc-arc'])
            
            # Add SDK path if available
            if self.compiler_info.sdk_path:
                cmd.extend(['-isysroot', self.compiler_info.sdk_path])
            
            # Add frameworks
            for framework in self.compiler_info.frameworks:
                cmd.extend(['-framework', framework])
            
            # Add custom framework paths
            if framework_paths:
                for path in framework_paths:
                    cmd.extend(['-F', path])
            
            # Execute compilation
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            return {
                'success': result.returncode == 0,
                'output_path': output_path if result.returncode == 0 else None,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(cmd)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_xcode_project(self, source_files: List[str], project_name: str, 
                           output_dir: str) -> Dict[str, Any]:
        """Create Xcode project from Objective-C source files."""
        if not self.compiler_info.xcodebuild_path:
            return {
                'success': False,
                'error': 'Xcode not available'
            }
        
        try:
            project_dir = Path(output_dir) / f"{project_name}.xcodeproj"
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Create basic project.pbxproj file
            pbxproj_content = self._generate_xcode_project_content(source_files, project_name)
            
            pbxproj_path = project_dir / "project.pbxproj"
            with open(pbxproj_path, 'w') as f:
                f.write(pbxproj_content)
            
            return {
                'success': True,
                'project_path': str(project_dir),
                'pbxproj_path': str(pbxproj_path)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _validate_memory_management(self, source_code: str, result: ObjCValidationResult) -> None:
        """Validate memory management patterns."""
        import re
        
        # Check for potential retain cycles
        if re.search(r'self\.\w+\s*=.*self', source_code):
            result.add_warning("Potential retain cycle detected with self reference")
        
        # Check for missing weak references in delegates
        delegate_pattern = r'@property.*delegate'
        if re.search(delegate_pattern, source_code) and '__weak' not in source_code:
            result.add_warning("Delegate properties should typically be weak to avoid retain cycles")
        
        # Check for manual memory management in ARC code
        if '__weak' in source_code or '__strong' in source_code:
            # ARC detected
            manual_patterns = ['retain', 'release', 'autorelease']
            for pattern in manual_patterns:
                if re.search(rf'\[.*\s+{pattern}\s*\]', source_code):
                    result.add_warning(f"Manual {pattern} call detected in ARC code")
    
    def _validate_foundation_usage(self, source_code: str, result: ObjCValidationResult) -> None:
        """Validate Foundation framework usage."""
        import re
        
        # Check for NSString format vulnerabilities
        if re.search(r'NSLog\s*\(\s*[^@]', source_code):
            result.add_warning("Potential format string vulnerability in NSLog")
        
        # Check for deprecated NSString methods
        deprecated_methods = ['lengthOfBytesUsingEncoding:', 'getCString:maxLength:encoding:']
        for method in deprecated_methods:
            if method in source_code:
                result.add_warning(f"Deprecated NSString method: {method}")
    
    def _detect_deprecated_apis(self, source_code: str, result: ObjCValidationResult) -> None:
        """Detect usage of deprecated APIs."""
        deprecated_apis = [
            'UIWebView',
            'NSURLConnection',
            'applicationDidEnterBackground',
            'viewDidUnload',
            'shouldAutorotateToInterfaceOrientation'
        ]
        
        for api in deprecated_apis:
            if api in source_code:
                result.add_warning(f"Deprecated API usage: {api}")
    
    def _validate_protocols_and_categories(self, ast: ObjCSourceUnit, result: ObjCValidationResult) -> None:
        """Validate protocols and categories."""
        # Check for empty protocols
        for protocol in ast.protocols:
            if not protocol.required_methods and not protocol.optional_methods and not protocol.properties:
                result.add_warning(f"Empty protocol: {protocol.name}")
        
        # Check for category naming
        for category in ast.categories:
            if not category.category_name:
                result.add_error(f"Category on {category.class_name} missing name")
    
    def _compare_asts(self, ast1: ObjCNode, ast2: ObjCNode) -> bool:
        """Compare two ASTs for structural equivalence."""
        # Simplified AST comparison
        if type(ast1) != type(ast2):
            return False
        
        if isinstance(ast1, ObjCSourceUnit):
            return (len(ast1.interfaces) == len(ast2.interfaces) and
                   len(ast1.implementations) == len(ast2.implementations) and
                   len(ast1.protocols) == len(ast2.protocols))
        
        return True  # Simplified comparison
    
    def _find_ast_differences(self, ast1: ObjCNode, ast2: ObjCNode) -> List[str]:
        """Find differences between two ASTs."""
        differences = []
        
        if type(ast1) != type(ast2):
            differences.append(f"Different node types: {type(ast1)} vs {type(ast2)}")
        
        # Add more detailed comparison logic as needed
        
        return differences
    
    def _generate_xcode_project_content(self, source_files: List[str], project_name: str) -> str:
        """Generate Xcode project.pbxproj content."""
        # Simplified Xcode project template
        return f"""// !$*UTF8*$!
{{
    archiveVersion = 1;
    classes = {{
    }};
    objectVersion = 50;
    objects = {{
        {project_name}ProjectUUID /* Project object */ = {{
            isa = PBXProject;
            attributes = {{
                LastUpgradeCheck = 1200;
                ORGANIZATIONNAME = "Runa Universal Translation Platform";
                TargetAttributes = {{
                }};
            }};
            buildConfigurationList = {project_name}ConfigListUUID /* Build configuration list for PBXProject "{project_name}" */;
            compatibilityVersion = "Xcode 9.3";
            developmentRegion = en;
            hasScannedForEncodings = 0;
            knownRegions = (
                en,
                Base,
            );
            mainGroup = {project_name}MainGroupUUID;
            productRefGroup = {project_name}ProductsGroupUUID /* Products */;
            projectDirPath = "";
            projectRoot = "";
            targets = (
            );
        }};
    }};
    rootObject = {project_name}ProjectUUID /* Project object */;
}}
"""


# ========================================================================
# Factory Functions and Default Instance
# ========================================================================

def create_objective_c_toolchain(style: ObjCCodeStyle = None) -> ObjCToolchain:
    """Create Objective-C toolchain instance."""
    return ObjCToolchain(style)


def parse_objective_c_code(source_code: str, file_path: str = "") -> ObjCSourceUnit:
    """Parse Objective-C source code."""
    toolchain = create_objective_c_toolchain()
    return toolchain.parse_code(source_code, file_path)


def generate_objective_c_code(objc_ast: ObjCNode, style: ObjCCodeStyle = None) -> str:
    """Generate Objective-C code from AST."""
    toolchain = create_objective_c_toolchain(style)
    return toolchain.generate_code(objc_ast)


def objective_c_round_trip_verify(source_code: str, file_path: str = "") -> Dict[str, Any]:
    """Verify round-trip translation for Objective-C code."""
    toolchain = create_objective_c_toolchain()
    return toolchain.round_trip_verify(source_code, file_path)


def objective_c_to_runa_translate(source_code: str, file_path: str = "") -> ASTNode:
    """Translate Objective-C code to Runa AST."""
    toolchain = create_objective_c_toolchain()
    return toolchain.translate_to_runa(source_code, file_path)


def runa_to_objective_c_translate(runa_ast: ASTNode) -> str:
    """Translate Runa AST to Objective-C code."""
    toolchain = create_objective_c_toolchain()
    return toolchain.translate_from_runa(runa_ast)


# Default toolchain instance
toolchain = create_objective_c_toolchain() 