#!/usr/bin/env python3
"""
Runa Multi-Language Build System

Universal build system supporting all language tiers with intelligent compilation,
optimization, cross-compilation, and asset management.
"""

import os
import shutil
import subprocess
import tempfile
import hashlib
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading

from ..package.manager import PackageMetadata, PackageManager
from ..package.resolver import CrossLanguageDependencyResolver
from ...core.pipeline import get_pipeline, translate_code


class BuildTarget(Enum):
    """Supported build targets."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"
    RELEASE = "release"


class OptimizationLevel(Enum):
    """Code optimization levels."""
    NONE = auto()
    BASIC = auto()
    AGGRESSIVE = auto()
    SIZE = auto()          # Optimize for size
    SPEED = auto()         # Optimize for speed


@dataclass
class BuildConfiguration:
    """Configuration for a build operation."""
    target: BuildTarget = BuildTarget.DEVELOPMENT
    optimization: OptimizationLevel = OptimizationLevel.BASIC
    
    # Language targets
    target_languages: List[str] = field(default_factory=list)
    exclude_languages: List[str] = field(default_factory=list)
    
    # Output configuration
    output_dir: str = "dist"
    clean_before_build: bool = True
    
    # Compilation options
    parallel_compilation: bool = True
    max_workers: int = 4
    
    # Asset management
    include_assets: bool = True
    minify_assets: bool = False
    bundle_assets: bool = False
    
    # Cross-compilation
    enable_cross_compilation: bool = True
    
    # Verification
    run_tests: bool = False
    verify_output: bool = True
    
    # Cache settings
    use_cache: bool = True
    cache_dir: str = ".runa_cache"


@dataclass
class BuildResult:
    """Result of a build operation."""
    success: bool
    target_outputs: Dict[str, str] = field(default_factory=dict)  # language -> output_path
    build_time_ms: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Build statistics
    files_processed: int = 0
    languages_built: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    # Asset information
    assets_processed: int = 0
    total_size_bytes: int = 0


class LanguageBuilder:
    """Base class for language-specific builders."""
    
    def __init__(self, language: str, tier: int):
        self.language = language
        self.tier = tier
        
        # Language-specific settings
        self.file_extensions = self._get_file_extensions()
        self.compile_command = self._get_compile_command()
        self.optimization_flags = self._get_optimization_flags()
    
    def _get_file_extensions(self) -> List[str]:
        """Get file extensions for this language."""
        extensions_map = {
            "runa": [".runa"],
            "javascript": [".js", ".mjs"],
            "typescript": [".ts", ".tsx"],
            "python": [".py"],
            "cpp": [".cpp", ".cxx", ".cc", ".c++"],
            "java": [".java"],
            "csharp": [".cs"],
            "sql": [".sql"],
            "rust": [".rs"],
            "go": [".go"],
            "swift": [".swift"],
            "kotlin": [".kt"],
            "php": [".php"],
            "html": [".html", ".htm"],
            "css": [".css", ".scss", ".sass"],
            "shell": [".sh", ".bash"],
            "yaml": [".yaml", ".yml"],
            "json": [".json"],
            "xml": [".xml"]
        }
        return extensions_map.get(self.language, [f".{self.language}"])
    
    def _get_compile_command(self) -> Optional[str]:
        """Get compilation command for this language."""
        commands_map = {
            "typescript": "tsc",
            "cpp": "g++",
            "java": "javac",
            "csharp": "csc",
            "rust": "rustc",
            "go": "go build",
            "swift": "swiftc",
            "kotlin": "kotlinc"
        }
        return commands_map.get(self.language)
    
    def _get_optimization_flags(self) -> Dict[OptimizationLevel, List[str]]:
        """Get optimization flags for this language."""
        if self.language == "cpp":
            return {
                OptimizationLevel.NONE: ["-O0"],
                OptimizationLevel.BASIC: ["-O1"],
                OptimizationLevel.AGGRESSIVE: ["-O3"],
                OptimizationLevel.SIZE: ["-Os"],
                OptimizationLevel.SPEED: ["-O3", "-march=native"]
            }
        elif self.language == "rust":
            return {
                OptimizationLevel.NONE: ["--opt-level=0"],
                OptimizationLevel.BASIC: ["--opt-level=1"],
                OptimizationLevel.AGGRESSIVE: ["--opt-level=3"],
                OptimizationLevel.SIZE: ["--opt-level=s"],
                OptimizationLevel.SPEED: ["--opt-level=3"]
            }
        elif self.language == "typescript":
            return {
                OptimizationLevel.NONE: [],
                OptimizationLevel.BASIC: ["--target", "ES2020"],
                OptimizationLevel.AGGRESSIVE: ["--target", "ES2020", "--strict"],
                OptimizationLevel.SIZE: ["--target", "ES5"],
                OptimizationLevel.SPEED: ["--target", "ES2020", "--strict"]
            }
        else:
            return {level: [] for level in OptimizationLevel}
    
    def can_build_natively(self) -> bool:
        """Check if this language can be built natively."""
        return self.compile_command is not None and shutil.which(self.compile_command.split()[0])
    
    def build_from_runa(self, runa_code: str, output_path: str, 
                       config: BuildConfiguration) -> bool:
        """Build this language from Runa code."""
        try:
            # Translate Runa to target language
            pipeline = get_pipeline()
            result = pipeline.translate(runa_code, "runa", self.language)
            
            if not result.success or not result.target_code:
                return False
            
            # Write translated code
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result.target_code)
            
            # If language supports native compilation, compile it
            if self.can_build_natively() and config.target in [BuildTarget.PRODUCTION, BuildTarget.RELEASE]:
                return self._compile_natively(output_path, config)
            
            return True
            
        except Exception as e:
            print(f"Error building {self.language}: {e}")
            return False
    
    def _compile_natively(self, source_path: str, config: BuildConfiguration) -> bool:
        """Compile source code natively."""
        if not self.compile_command:
            return True  # No compilation needed
        
        try:
            cmd = self.compile_command.split()
            
            # Add optimization flags
            opt_flags = self.optimization_flags.get(config.optimization, [])
            cmd.extend(opt_flags)
            
            # Add source file
            cmd.append(source_path)
            
            # Set output file
            output_path = source_path.replace(Path(source_path).suffix, self._get_executable_extension())
            cmd.extend(["-o", output_path])
            
            # Run compilation
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Compilation failed for {source_path}: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Native compilation error: {e}")
            return False
    
    def _get_executable_extension(self) -> str:
        """Get executable extension for this platform."""
        if os.name == 'nt':  # Windows
            return '.exe'
        return ''


class RunaMultiLanguageBuilder:
    """Main build system for multi-language Runa projects."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.package_manager = PackageManager(str(self.project_root))
        
        # Load project metadata
        self.metadata = self._load_project_metadata()
        
        # Language builders
        self.language_builders = self._initialize_language_builders()
        
        # Build cache
        self.cache_dir = Path(self.project_root) / ".runa_cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # Build lock for thread safety
        self.build_lock = threading.Lock()
    
    def _load_project_metadata(self) -> Optional[PackageMetadata]:
        """Load project metadata from runa.toml."""
        runa_toml = self.project_root / "runa.toml"
        if runa_toml.exists():
            try:
                return PackageMetadata.from_toml(str(runa_toml))
            except Exception as e:
                print(f"Warning: Failed to load runa.toml: {e}")
        return None
    
    def _initialize_language_builders(self) -> Dict[str, LanguageBuilder]:
        """Initialize builders for all supported languages."""
        builders = {}
        
        # Language tier mapping
        language_tiers = {
            1: ["javascript", "typescript", "python", "cpp", "java", "csharp", "sql"],
            2: ["rust", "go", "swift", "kotlin", "php", "webassembly"],
            3: ["html", "css", "shell", "hcl", "yaml", "json", "xml"],
            4: ["r", "matlab", "julia", "solidity", "graphql"],
            5: ["lisp", "haskell", "erlang", "elixir", "llvm_ir", "assembly"],
            6: ["objective_c", "visual_basic", "cobol", "ada", "perl", "fortran"]
        }
        
        for tier, languages in language_tiers.items():
            for language in languages:
                builders[language] = LanguageBuilder(language, tier)
        
        # Always include Runa itself
        builders["runa"] = LanguageBuilder("runa", 1)
        
        return builders
    
    def build(self, config: BuildConfiguration = None) -> BuildResult:
        """Build the project with the given configuration."""
        config = config or BuildConfiguration()
        start_time = time.time()
        
        result = BuildResult()
        
        try:
            with self.build_lock:
                # Clean output directory if requested
                if config.clean_before_build:
                    self._clean_output_directory(config.output_dir)
                
                # Resolve dependencies
                if not self._resolve_dependencies(config, result):
                    result.success = False
                    return result
                
                # Find Runa source files
                runa_files = self._find_runa_files()
                if not runa_files:
                    result.errors.append("No Runa source files found")
                    result.success = False
                    return result
                
                # Determine target languages
                target_languages = self._determine_target_languages(config)
                
                # Build for each target language
                if config.parallel_compilation and len(target_languages) > 1:
                    success = self._build_parallel(runa_files, target_languages, config, result)
                else:
                    success = self._build_sequential(runa_files, target_languages, config, result)
                
                if not success:
                    result.success = False
                    return result
                
                # Process assets
                if config.include_assets:
                    self._process_assets(config, result)
                
                # Run verification
                if config.verify_output:
                    self._verify_outputs(config, result)
                
                # Run tests if requested
                if config.run_tests:
                    self._run_tests(config, result)
                
                result.success = True
                result.languages_built = len(target_languages)
                result.files_processed = len(runa_files)
                
        except Exception as e:
            result.errors.append(f"Build failed: {e}")
            result.success = False
        
        finally:
            result.build_time_ms = (time.time() - start_time) * 1000
        
        return result
    
    def _resolve_dependencies(self, config: BuildConfiguration, result: BuildResult) -> bool:
        """Resolve project dependencies."""
        if not self.metadata:
            return True  # No dependencies to resolve
        
        try:
            resolver = CrossLanguageDependencyResolver(self.package_manager.registry)
            resolution_result = resolver.resolve_dependencies(
                self.metadata,
                include_dev=(config.target == BuildTarget.DEVELOPMENT),
                include_optional=True
            )
            
            if not resolution_result.success:
                for conflict in resolution_result.conflicts:
                    result.errors.append(f"Dependency conflict: {conflict['message']}")
                return False
            
            # Install missing dependencies
            for package in resolution_result.resolved_packages.values():
                if package.name not in self.package_manager.installed_packages:
                    success = self.package_manager.install(package.name, str(package.version))
                    if not success:
                        result.errors.append(f"Failed to install dependency: {package.name}")
                        return False
            
            return True
            
        except Exception as e:
            result.errors.append(f"Dependency resolution failed: {e}")
            return False
    
    def _find_runa_files(self) -> List[Path]:
        """Find all Runa source files in the project."""
        runa_files = []
        
        # Standard source directories
        source_dirs = ["src", "lib", "source", "."]
        
        for src_dir in source_dirs:
            src_path = self.project_root / src_dir
            if src_path.exists() and src_path.is_dir():
                for runa_file in src_path.rglob("*.runa"):
                    runa_files.append(runa_file)
        
        return runa_files
    
    def _determine_target_languages(self, config: BuildConfiguration) -> List[str]:
        """Determine which languages to build for."""
        if config.target_languages:
            return [lang for lang in config.target_languages if lang not in config.exclude_languages]
        
        # Default target languages based on project metadata
        if self.metadata and self.metadata.supported_languages:
            languages = [lang for lang in self.metadata.supported_languages if lang != "runa"]
        else:
            # Default to tier 1 languages
            languages = ["python", "javascript", "typescript"]
        
        # Remove excluded languages
        return [lang for lang in languages if lang not in config.exclude_languages]
    
    def _build_parallel(self, runa_files: List[Path], target_languages: List[str], 
                       config: BuildConfiguration, result: BuildResult) -> bool:
        """Build multiple languages in parallel."""
        with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
            futures = []
            
            for language in target_languages:
                future = executor.submit(
                    self._build_language, runa_files, language, config, result
                )
                futures.append((language, future))
            
            # Wait for all builds to complete
            success = True
            for language, future in futures:
                try:
                    lang_success = future.result()
                    if not lang_success:
                        success = False
                        result.errors.append(f"Failed to build {language}")
                except Exception as e:
                    success = False
                    result.errors.append(f"Error building {language}: {e}")
            
            return success
    
    def _build_sequential(self, runa_files: List[Path], target_languages: List[str],
                         config: BuildConfiguration, result: BuildResult) -> bool:
        """Build languages sequentially."""
        for language in target_languages:
            success = self._build_language(runa_files, language, config, result)
            if not success:
                result.errors.append(f"Failed to build {language}")
                return False
        
        return True
    
    def _build_language(self, runa_files: List[Path], language: str,
                       config: BuildConfiguration, result: BuildResult) -> bool:
        """Build a specific language from Runa files."""
        if language not in self.language_builders:
            result.warnings.append(f"No builder available for {language}")
            return True
        
        builder = self.language_builders[language]
        output_dir = Path(config.output_dir) / language
        output_dir.mkdir(parents=True, exist_ok=True)
        
        success = True
        
        for runa_file in runa_files:
            # Read Runa source
            with open(runa_file, 'r', encoding='utf-8') as f:
                runa_code = f.read()
            
            # Determine output file path
            rel_path = runa_file.relative_to(self.project_root)
            output_file = output_dir / rel_path.with_suffix(builder.file_extensions[0])
            
            # Check cache
            if config.use_cache and self._is_cached(runa_file, output_file, language):
                result.cache_hits += 1
                continue
            
            result.cache_misses += 1
            
            # Build the file
            file_success = builder.build_from_runa(runa_code, str(output_file), config)
            if not file_success:
                success = False
                result.errors.append(f"Failed to build {runa_file} for {language}")
            else:
                # Update cache
                if config.use_cache:
                    self._update_cache(runa_file, output_file, language)
        
        if success:
            result.target_outputs[language] = str(output_dir)
        
        return success
    
    def _is_cached(self, source_file: Path, output_file: Path, language: str) -> bool:
        """Check if the build output is cached and up-to-date."""
        if not output_file.exists():
            return False
        
        cache_file = self.cache_dir / f"{source_file.name}_{language}.json"
        if not cache_file.exists():
            return False
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if source file is newer than cache
            source_mtime = source_file.stat().st_mtime
            cached_mtime = cache_data.get('source_mtime', 0)
            
            return source_mtime <= cached_mtime
        
        except Exception:
            return False
    
    def _update_cache(self, source_file: Path, output_file: Path, language: str):
        """Update build cache for a file."""
        cache_file = self.cache_dir / f"{source_file.name}_{language}.json"
        
        cache_data = {
            'source_file': str(source_file),
            'output_file': str(output_file),
            'language': language,
            'source_mtime': source_file.stat().st_mtime,
            'build_time': time.time()
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception:
            pass  # Cache update is not critical
    
    def _process_assets(self, config: BuildConfiguration, result: BuildResult):
        """Process project assets (images, data files, etc.)."""
        assets_dir = self.project_root / "assets"
        if not assets_dir.exists():
            return
        
        output_assets_dir = Path(config.output_dir) / "assets"
        output_assets_dir.mkdir(parents=True, exist_ok=True)
        
        for asset_file in assets_dir.rglob("*"):
            if asset_file.is_file():
                rel_path = asset_file.relative_to(assets_dir)
                output_path = output_assets_dir / rel_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy asset
                shutil.copy2(asset_file, output_path)
                result.assets_processed += 1
                result.total_size_bytes += asset_file.stat().st_size
    
    def _verify_outputs(self, config: BuildConfiguration, result: BuildResult):
        """Verify that build outputs are valid."""
        for language, output_dir in result.target_outputs.items():
            output_path = Path(output_dir)
            if not output_path.exists():
                result.warnings.append(f"Output directory missing for {language}: {output_dir}")
                continue
            
            # Count output files
            output_files = list(output_path.rglob("*"))
            file_count = len([f for f in output_files if f.is_file()])
            
            if file_count == 0:
                result.warnings.append(f"No output files generated for {language}")
    
    def _run_tests(self, config: BuildConfiguration, result: BuildResult):
        """Run tests for the built project."""
        # Look for test command in project metadata
        if self.metadata and self.metadata.test_command:
            try:
                test_result = subprocess.run(
                    self.metadata.test_command.split(),
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                
                if test_result.returncode != 0:
                    result.warnings.append(f"Tests failed: {test_result.stderr}")
                
            except Exception as e:
                result.warnings.append(f"Failed to run tests: {e}")
    
    def _clean_output_directory(self, output_dir: str):
        """Clean the output directory."""
        output_path = Path(output_dir)
        if output_path.exists():
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
    
    def clean_cache(self):
        """Clean the build cache."""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_build_info(self) -> Dict[str, Any]:
        """Get information about the build system."""
        return {
            "project_root": str(self.project_root),
            "supported_languages": list(self.language_builders.keys()),
            "cache_dir": str(self.cache_dir),
            "metadata": {
                "name": self.metadata.name if self.metadata else None,
                "version": str(self.metadata.version) if self.metadata else None,
                "supported_languages": self.metadata.supported_languages if self.metadata else []
            }
        }


def main():
    """CLI entry point for the build system."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Runa Multi-Language Build System')
    parser.add_argument('--target', choices=['development', 'production', 'test', 'release'],
                       default='development', help='Build target')
    parser.add_argument('--optimization', choices=['none', 'basic', 'aggressive', 'size', 'speed'],
                       default='basic', help='Optimization level')
    parser.add_argument('--languages', nargs='*', help='Target languages to build')
    parser.add_argument('--exclude', nargs='*', default=[], help='Languages to exclude')
    parser.add_argument('--output', default='dist', help='Output directory')
    parser.add_argument('--parallel', action='store_true', default=True, help='Enable parallel compilation')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--no-cache', action='store_true', help='Disable build cache')
    parser.add_argument('--clean', action='store_true', help='Clean before build')
    parser.add_argument('--test', action='store_true', help='Run tests after build')
    parser.add_argument('--assets', action='store_true', default=True, help='Process assets')
    parser.add_argument('--verify', action='store_true', default=True, help='Verify outputs')
    parser.add_argument('--project-dir', default='.', help='Project directory')
    
    # Special commands
    parser.add_argument('--clean-cache', action='store_true', help='Clean build cache and exit')
    parser.add_argument('--info', action='store_true', help='Show build system info')
    
    args = parser.parse_args()
    
    # Initialize build system
    builder = RunaMultiLanguageBuilder(args.project_dir)
    
    if args.clean_cache:
        builder.clean_cache()
        print("Build cache cleaned")
        return 0
    
    if args.info:
        info = builder.get_build_info()
        print("Runa Build System Information:")
        print(f"  Project: {info['metadata']['name'] or 'Unknown'}")
        print(f"  Version: {info['metadata']['version'] or 'Unknown'}")
        print(f"  Root: {info['project_root']}")
        print(f"  Supported Languages: {len(info['supported_languages'])}")
        for lang in sorted(info['supported_languages']):
            print(f"    - {lang}")
        return 0
    
    # Build configuration
    config = BuildConfiguration(
        target=BuildTarget(args.target),
        optimization=OptimizationLevel[args.optimization.upper()],
        target_languages=args.languages or [],
        exclude_languages=args.exclude,
        output_dir=args.output,
        clean_before_build=args.clean,
        parallel_compilation=args.parallel,
        max_workers=args.workers,
        include_assets=args.assets,
        run_tests=args.test,
        verify_output=args.verify,
        use_cache=not args.no_cache
    )
    
    # Run build
    print(f"Building Runa project...")
    print(f"  Target: {config.target.value}")
    print(f"  Optimization: {config.optimization.name}")
    print(f"  Output: {config.output_dir}")
    
    result = builder.build(config)
    
    if result.success:
        print(f"✅ Build successful in {result.build_time_ms:.1f}ms")
        print(f"  Languages built: {result.languages_built}")
        print(f"  Files processed: {result.files_processed}")
        print(f"  Cache hits: {result.cache_hits}/{result.cache_hits + result.cache_misses}")
        
        if result.target_outputs:
            print("  Output directories:")
            for language, output_dir in result.target_outputs.items():
                print(f"    {language}: {output_dir}")
        
        if result.warnings:
            print(f"  Warnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"    - {warning}")
        
        return 0
    else:
        print(f"❌ Build failed after {result.build_time_ms:.1f}ms")
        if result.errors:
            print("  Errors:")
            for error in result.errors:
                print(f"    - {error}")
        
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())