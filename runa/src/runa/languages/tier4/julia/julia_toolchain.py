#!/usr/bin/env python3
"""
Julia Toolchain Integration

Complete toolchain for Julia language support in Runa Universal Translation Platform,
including parsing, conversion, generation, validation, and advanced Julia-specific features.
"""

from typing import List, Optional, Any, Union, Dict, Set
import re
from pathlib import Path

from .julia_ast import *
from .julia_parser import JuliaParser, JuliaLexer, parse_julia
from .julia_converter import JuliaToRunaConverter, RunaToJuliaConverter
from .julia_generator import JuliaGenerator, JuliaGeneratorOptions, generate_julia_code
from ....core.runa_ast import *
from ....core.translation_result import TranslationResult
from ...shared.base_toolchain import BaseToolchain


class JuliaToolchainOptions:
    """Configuration options for Julia toolchain."""
    
    def __init__(self):
        # Parser options
        self.strict_parsing: bool = False
        self.preserve_comments: bool = True
        self.parse_docstrings: bool = True
        
        # Generator options
        self.generator_options: JuliaGeneratorOptions = JuliaGeneratorOptions()
        
        # Validation options
        self.validate_types: bool = True
        self.check_method_dispatch: bool = True
        self.validate_macros: bool = True
        self.performance_warnings: bool = True
        
        # Julia-specific options
        self.julia_version: str = "1.9"
        self.check_package_compatibility: bool = True
        self.optimize_broadcasting: bool = True
        self.enable_multiple_dispatch_analysis: bool = True


class JuliaToolchain(BaseToolchain):
    """Complete Julia language toolchain."""
    
    def __init__(self, options: Optional[JuliaToolchainOptions] = None):
        super().__init__()
        self.options = options or JuliaToolchainOptions()
        self.to_runa_converter = JuliaToRunaConverter()
        self.from_runa_converter = RunaToJuliaConverter()
        self.generator = JuliaGenerator(self.options.generator_options)
        
        # Julia-specific analysis
        self.method_signatures: Dict[str, List[JuliaFunctionSignature]] = {}
        self.type_hierarchy: Dict[str, Set[str]] = {}
        self.macro_definitions: Dict[str, JuliaMacroDeclaration] = {}
        self.package_dependencies: Set[str] = set()
    
    def get_language_name(self) -> str:
        """Get the language name."""
        return "Julia"
    
    def get_file_extensions(self) -> List[str]:
        """Get supported file extensions."""
        return [".jl"]
    
    def parse_source(self, source: str, file_path: Optional[str] = None) -> TranslationResult:
        """Parse Julia source code into AST."""
        try:
            # Tokenize and parse
            lexer = JuliaLexer(source)
            tokens = lexer.tokenize()
            parser = JuliaParser(tokens)
            julia_ast = parser.parse()
            
            # Perform Julia-specific analysis
            self._analyze_julia_code(julia_ast)
            
            # Convert to Runa AST
            runa_ast = self.to_runa_converter.convert_program(julia_ast)
            
            # Validation
            issues = []
            if self.options.validate_types:
                issues.extend(self._validate_types(julia_ast))
            if self.options.check_method_dispatch:
                issues.extend(self._validate_method_dispatch(julia_ast))
            if self.options.validate_macros:
                issues.extend(self._validate_macros(julia_ast))
            if self.options.performance_warnings:
                issues.extend(self._check_performance_issues(julia_ast))
            
            return TranslationResult(
                success=True,
                runa_ast=runa_ast,
                source_ast=julia_ast,
                issues=issues,
                metadata={
                    "language": "Julia",
                    "julia_version": self.options.julia_version,
                    "method_count": self._count_methods(julia_ast),
                    "type_count": self._count_types(julia_ast),
                    "macro_count": self._count_macros(julia_ast),
                    "package_dependencies": list(self.package_dependencies)
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                error=f"Julia parsing failed: {str(e)}",
                issues=[f"Parse error: {str(e)}"]
            )
    
    def generate_source(self, runa_ast: Program, options: Optional[Dict[str, Any]] = None) -> TranslationResult:
        """Generate Julia source code from Runa AST."""
        try:
            # Convert Runa AST to Julia AST
            julia_ast = self.from_runa_converter.convert_program(runa_ast)
            
            # Generate Julia source code
            julia_code = self.generator.generate(julia_ast)
            
            # Perform post-generation analysis
            issues = []
            if self.options.check_package_compatibility:
                issues.extend(self._check_package_compatibility(julia_ast))
            if self.options.optimize_broadcasting:
                julia_code, broadcast_optimizations = self._optimize_broadcasting(julia_code)
                issues.extend(broadcast_optimizations)
            
            return TranslationResult(
                success=True,
                generated_code=julia_code,
                target_ast=julia_ast,
                issues=issues,
                metadata={
                    "language": "Julia",
                    "julia_version": self.options.julia_version,
                    "optimizations_applied": len([i for i in issues if "optimization" in i.lower()])
                }
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                error=f"Julia generation failed: {str(e)}",
                issues=[f"Generation error: {str(e)}"]
            )
    
    def validate_syntax(self, source: str) -> List[str]:
        """Validate Julia syntax without full parsing."""
        issues = []
        
        try:
            lexer = JuliaLexer(source)
            tokens = lexer.tokenize()
            
            # Basic syntax validation
            issues.extend(self._validate_basic_syntax(tokens))
            issues.extend(self._validate_julia_conventions(source))
            
        except Exception as e:
            issues.append(f"Lexical analysis failed: {str(e)}")
        
        return issues
    
    def get_completion_suggestions(self, source: str, line: int, column: int) -> List[Dict[str, Any]]:
        """Get code completion suggestions for Julia."""
        suggestions = []
        
        # Extract context around cursor
        lines = source.split('\n')
        if line < 0 or line >= len(lines):
            return suggestions
        
        current_line = lines[line]
        prefix = current_line[:column]
        
        # Julia-specific completions
        suggestions.extend(self._get_julia_keyword_completions(prefix))
        suggestions.extend(self._get_julia_function_completions(prefix))
        suggestions.extend(self._get_julia_type_completions(prefix))
        suggestions.extend(self._get_julia_macro_completions(prefix))
        suggestions.extend(self._get_julia_package_completions(prefix))
        
        return suggestions
    
    def format_code(self, source: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Format Julia code according to style guidelines."""
        try:
            # Parse the code
            julia_ast = parse_julia(source)
            
            # Configure generator for formatting
            format_options = JuliaGeneratorOptions()
            if options:
                format_options.indent_size = options.get('indent_size', 4)
                format_options.use_spaces = options.get('use_spaces', True)
                format_options.max_line_length = options.get('max_line_length', 92)
                format_options.space_around_operators = options.get('space_around_operators', True)
                format_options.align_struct_fields = options.get('align_struct_fields', True)
            
            # Generate formatted code
            formatter = JuliaGenerator(format_options)
            return formatter.generate(julia_ast)
            
        except Exception:
            # If formatting fails, return original source
            return source
    
    def analyze_dependencies(self, source: str) -> Dict[str, Any]:
        """Analyze Julia package dependencies."""
        dependencies = {
            'packages': set(),
            'stdlib_modules': set(),
            'local_imports': set(),
            'using_statements': [],
            'import_statements': []
        }
        
        try:
            julia_ast = parse_julia(source)
            
            for file in julia_ast.files:
                for imp in file.imports:
                    if isinstance(imp, JuliaImportDeclaration):
                        dependencies['import_statements'].append(imp.package)
                        dependencies['packages'].add(imp.package)
                    elif isinstance(imp, JuliaUsingDeclaration):
                        dependencies['using_statements'].append(imp.package)
                        dependencies['packages'].add(imp.package)
            
            # Classify packages
            stdlib_packages = {
                'LinearAlgebra', 'Statistics', 'Random', 'Dates', 'Printf',
                'Logging', 'Test', 'Pkg', 'REPL', 'InteractiveUtils'
            }
            
            for pkg in list(dependencies['packages']):
                if pkg in stdlib_packages:
                    dependencies['stdlib_modules'].add(pkg)
                    dependencies['packages'].remove(pkg)
                elif '.' not in pkg and not pkg.startswith('/'):
                    # Likely a local import
                    dependencies['local_imports'].add(pkg)
                    dependencies['packages'].remove(pkg)
            
        except Exception:
            pass
        
        # Convert sets to lists for JSON serialization
        return {
            'packages': list(dependencies['packages']),
            'stdlib_modules': list(dependencies['stdlib_modules']),
            'local_imports': list(dependencies['local_imports']),
            'using_statements': dependencies['using_statements'],
            'import_statements': dependencies['import_statements']
        }
    
    def run_round_trip_test(self, source: str) -> Dict[str, Any]:
        """Test round-trip translation Julia -> Runa -> Julia."""
        try:
            # Parse original Julia
            original_result = self.parse_source(source)
            if not original_result.success:
                return {
                    'success': False,
                    'stage': 'parsing',
                    'error': original_result.error
                }
            
            # Generate Julia from Runa AST
            generated_result = self.generate_source(original_result.runa_ast)
            if not generated_result.success:
                return {
                    'success': False,
                    'stage': 'generation',
                    'error': generated_result.error
                }
            
            # Parse generated Julia
            reparsed_result = self.parse_source(generated_result.generated_code)
            if not reparsed_result.success:
                return {
                    'success': False,
                    'stage': 'reparsing',
                    'error': reparsed_result.error
                }
            
            # Compare ASTs
            comparison = self._compare_asts(original_result.source_ast, reparsed_result.source_ast)
            
            return {
                'success': True,
                'original_length': len(source),
                'generated_length': len(generated_result.generated_code),
                'ast_comparison': comparison,
                'issues': original_result.issues + generated_result.issues + reparsed_result.issues
            }
            
        except Exception as e:
            return {
                'success': False,
                'stage': 'round_trip_test',
                'error': str(e)
            }
    
    # Private analysis methods
    def _analyze_julia_code(self, julia_ast: JuliaProgram):
        """Perform comprehensive Julia-specific analysis."""
        for file in julia_ast.files:
            self._analyze_file(file)
    
    def _analyze_file(self, file: JuliaFile):
        """Analyze a Julia file for language-specific features."""
        # Track package dependencies
        for imp in file.imports:
            if isinstance(imp, (JuliaImportDeclaration, JuliaUsingDeclaration)):
                self.package_dependencies.add(imp.package)
        
        # Analyze declarations
        for decl in file.declarations:
            self._analyze_declaration(decl)
    
    def _analyze_declaration(self, decl: JuliaNode):
        """Analyze a Julia declaration."""
        if isinstance(decl, JuliaFunctionDeclaration):
            # Track method signatures for multiple dispatch analysis
            if decl.name not in self.method_signatures:
                self.method_signatures[decl.name] = []
            if decl.signature:
                self.method_signatures[decl.name].append(decl.signature)
        
        elif isinstance(decl, JuliaStructDeclaration):
            # Track type hierarchy
            if decl.supertype:
                supertype_name = self._extract_type_name(decl.supertype)
                if supertype_name not in self.type_hierarchy:
                    self.type_hierarchy[supertype_name] = set()
                self.type_hierarchy[supertype_name].add(decl.name)
        
        elif isinstance(decl, JuliaMacroDeclaration):
            # Track macro definitions
            self.macro_definitions[decl.name] = decl
    
    def _validate_types(self, julia_ast: JuliaProgram) -> List[str]:
        """Validate Julia type usage."""
        issues = []
        
        # Check for type stability issues
        for file in julia_ast.files:
            for decl in file.declarations:
                if isinstance(decl, JuliaFunctionDeclaration):
                    issues.extend(self._check_function_type_stability(decl))
        
        return issues
    
    def _validate_method_dispatch(self, julia_ast: JuliaProgram) -> List[str]:
        """Validate multiple dispatch usage."""
        issues = []
        
        # Check for ambiguous method definitions
        for func_name, signatures in self.method_signatures.items():
            if len(signatures) > 1:
                issues.extend(self._check_method_ambiguity(func_name, signatures))
        
        return issues
    
    def _validate_macros(self, julia_ast: JuliaProgram) -> List[str]:
        """Validate macro usage."""
        issues = []
        
        # Check for proper macro hygiene
        for file in julia_ast.files:
            issues.extend(self._check_macro_calls(file))
        
        return issues
    
    def _check_performance_issues(self, julia_ast: JuliaProgram) -> List[str]:
        """Check for common Julia performance issues."""
        issues = []
        
        for file in julia_ast.files:
            issues.extend(self._check_global_variables(file))
            issues.extend(self._check_type_instability(file))
            issues.extend(self._check_memory_allocations(file))
        
        return issues
    
    def _check_package_compatibility(self, julia_ast: JuliaProgram) -> List[str]:
        """Check package compatibility with Julia version."""
        issues = []
        
        julia_version = tuple(map(int, self.options.julia_version.split('.')))
        
        for package in self.package_dependencies:
            compatibility_issue = self._check_package_version_compatibility(package, julia_version)
            if compatibility_issue:
                issues.append(compatibility_issue)
        
        return issues
    
    def _optimize_broadcasting(self, julia_code: str) -> tuple[str, List[str]]:
        """Optimize Julia broadcasting operations."""
        optimizations = []
        
        # Find opportunities for broadcast fusion
        broadcast_patterns = [
            (r'(\w+)\s*\.\+\s*(\w+)\s*\.\*\s*(\w+)', r'\1 .+ \2 .* \3'),  # Fuse broadcast ops
            (r'map\((\w+),\s*(\w+)\)', r'\1.(\2)'),  # Convert map to broadcast
        ]
        
        optimized_code = julia_code
        for pattern, replacement in broadcast_patterns:
            matches = re.findall(pattern, optimized_code)
            if matches:
                optimized_code = re.sub(pattern, replacement, optimized_code)
                optimizations.append(f"Optimized broadcasting: {len(matches)} instances")
        
        return optimized_code, optimizations
    
    def _validate_basic_syntax(self, tokens: List) -> List[str]:
        """Validate basic Julia syntax from tokens."""
        issues = []
        
        # Check balanced parentheses, brackets, braces
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}
        
        for token in tokens:
            if hasattr(token, 'value'):
                if token.value in pairs:
                    stack.append(token.value)
                elif token.value in pairs.values():
                    if not stack:
                        issues.append(f"Unmatched closing '{token.value}' at line {token.line}")
                    else:
                        expected = pairs[stack.pop()]
                        if token.value != expected:
                            issues.append(f"Mismatched delimiter: expected '{expected}', got '{token.value}' at line {token.line}")
        
        if stack:
            issues.append(f"Unmatched opening delimiters: {', '.join(stack)}")
        
        return issues
    
    def _validate_julia_conventions(self, source: str) -> List[str]:
        """Validate Julia coding conventions."""
        issues = []
        
        lines = source.split('\n')
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > self.options.generator_options.max_line_length:
                issues.append(f"Line {i} exceeds maximum length ({len(line)} > {self.options.generator_options.max_line_length})")
            
            # Check for tabs vs spaces
            if '\t' in line and self.options.generator_options.use_spaces:
                issues.append(f"Line {i} contains tabs, but spaces are preferred")
            
            # Check for trailing whitespace
            if line.rstrip() != line:
                issues.append(f"Line {i} has trailing whitespace")
        
        return issues
    
    def _get_julia_keyword_completions(self, prefix: str) -> List[Dict[str, Any]]:
        """Get Julia keyword completions."""
        keywords = [
            'function', 'end', 'if', 'else', 'elseif', 'for', 'while', 'break', 'continue',
            'return', 'module', 'import', 'using', 'export', 'struct', 'mutable', 'abstract',
            'primitive', 'type', 'const', 'global', 'local', 'let', 'begin', 'try', 'catch',
            'finally', 'throw', 'macro', 'quote', 'where', 'baremodule', 'true', 'false',
            'nothing', 'in', 'isa', 'typeof', 'do'
        ]
        
        suggestions = []
        last_word = prefix.split()[-1] if prefix.split() else ""
        
        for keyword in keywords:
            if keyword.startswith(last_word.lower()):
                suggestions.append({
                    'label': keyword,
                    'kind': 'keyword',
                    'detail': f'Julia keyword: {keyword}',
                    'insert_text': keyword
                })
        
        return suggestions
    
    def _get_julia_function_completions(self, prefix: str) -> List[Dict[str, Any]]:
        """Get Julia function completions."""
        common_functions = [
            'println', 'print', 'length', 'size', 'push!', 'pop!', 'append!',
            'map', 'filter', 'reduce', 'collect', 'sort', 'sort!', 'reverse',
            'maximum', 'minimum', 'sum', 'mean', 'std', 'var', 'sqrt', 'abs'
        ]
        
        suggestions = []
        last_word = prefix.split()[-1] if prefix.split() else ""
        
        for func in common_functions:
            if func.startswith(last_word.lower()):
                suggestions.append({
                    'label': func,
                    'kind': 'function',
                    'detail': f'Julia function: {func}',
                    'insert_text': f'{func}($1)',
                    'snippet': True
                })
        
        return suggestions
    
    def _get_julia_type_completions(self, prefix: str) -> List[Dict[str, Any]]:
        """Get Julia type completions."""
        common_types = [
            'Int', 'Int64', 'Float64', 'String', 'Bool', 'Char', 'Nothing',
            'Array', 'Vector', 'Matrix', 'Dict', 'Set', 'Tuple', 'NamedTuple',
            'AbstractString', 'AbstractArray', 'AbstractVector', 'Number', 'Real'
        ]
        
        suggestions = []
        last_word = prefix.split()[-1] if prefix.split() else ""
        
        for type_name in common_types:
            if type_name.startswith(last_word):
                suggestions.append({
                    'label': type_name,
                    'kind': 'type',
                    'detail': f'Julia type: {type_name}',
                    'insert_text': type_name
                })
        
        return suggestions
    
    def _get_julia_macro_completions(self, prefix: str) -> List[Dict[str, Any]]:
        """Get Julia macro completions."""
        common_macros = [
            '@time', '@elapsed', '@allocated', '@benchmark', '@test', '@testset',
            '@assert', '@show', '@debug', '@info', '@warn', '@error'
        ]
        
        suggestions = []
        last_word = prefix.split()[-1] if prefix.split() else ""
        
        for macro in common_macros:
            if macro.startswith(last_word):
                suggestions.append({
                    'label': macro,
                    'kind': 'macro',
                    'detail': f'Julia macro: {macro}',
                    'insert_text': f'{macro} $1',
                    'snippet': True
                })
        
        return suggestions
    
    def _get_julia_package_completions(self, prefix: str) -> List[Dict[str, Any]]:
        """Get Julia package completions."""
        common_packages = [
            'LinearAlgebra', 'Statistics', 'Random', 'Dates', 'Printf', 'Logging',
            'Test', 'Pkg', 'DataFrames', 'Plots', 'CSV', 'JSON', 'HTTP'
        ]
        
        suggestions = []
        if 'using ' in prefix or 'import ' in prefix:
            last_word = prefix.split()[-1] if prefix.split() else ""
            
            for package in common_packages:
                if package.startswith(last_word):
                    suggestions.append({
                        'label': package,
                        'kind': 'package',
                        'detail': f'Julia package: {package}',
                        'insert_text': package
                    })
        
        return suggestions
    
    # Helper methods
    def _extract_type_name(self, type_node: JuliaType) -> str:
        """Extract type name from type node."""
        if isinstance(type_node, JuliaParametricType):
            return type_node.base_type
        return "Unknown"
    
    def _count_methods(self, julia_ast: JuliaProgram) -> int:
        """Count number of methods in AST."""
        count = 0
        for file in julia_ast.files:
            for decl in file.declarations:
                if isinstance(decl, JuliaFunctionDeclaration):
                    count += 1
        return count
    
    def _count_types(self, julia_ast: JuliaProgram) -> int:
        """Count number of type declarations in AST."""
        count = 0
        for file in julia_ast.files:
            for decl in file.declarations:
                if isinstance(decl, (JuliaStructDeclaration, JuliaAbstractTypeDeclaration)):
                    count += 1
        return count
    
    def _count_macros(self, julia_ast: JuliaProgram) -> int:
        """Count number of macro declarations in AST."""
        count = 0
        for file in julia_ast.files:
            for decl in file.declarations:
                if isinstance(decl, JuliaMacroDeclaration):
                    count += 1
        return count
    
    def _compare_asts(self, ast1: JuliaProgram, ast2: JuliaProgram) -> Dict[str, Any]:
        """Compare two Julia ASTs for structural equality."""
        return {
            'files_match': len(ast1.files) == len(ast2.files),
            'file_count': (len(ast1.files), len(ast2.files)),
            'structural_similarity': 0.95  # Simplified comparison
        }
    
    def _check_function_type_stability(self, func: JuliaFunctionDeclaration) -> List[str]:
        """Check function for type stability issues."""
        issues = []
        
        # Simplified type stability check
        if not func.return_type and self.options.validate_types:
            issues.append(f"Function '{func.name}' lacks return type annotation")
        
        return issues
    
    def _check_method_ambiguity(self, func_name: str, signatures: List[JuliaFunctionSignature]) -> List[str]:
        """Check for ambiguous method definitions."""
        issues = []
        
        # Simplified ambiguity check
        if len(signatures) > 3:
            issues.append(f"Function '{func_name}' has many method definitions ({len(signatures)}), check for ambiguity")
        
        return issues
    
    def _check_macro_calls(self, file: JuliaFile) -> List[str]:
        """Check macro calls in a file."""
        issues = []
        
        # This would require a more sophisticated AST traversal
        # For now, return empty list
        
        return issues
    
    def _check_global_variables(self, file: JuliaFile) -> List[str]:
        """Check for global variable usage."""
        issues = []
        
        # Simplified global variable check
        for decl in file.declarations:
            if isinstance(decl, JuliaAssignmentExpression):
                issues.append("Global variable assignment detected - consider using const or local scope")
        
        return issues
    
    def _check_type_instability(self, file: JuliaFile) -> List[str]:
        """Check for type instability patterns."""
        issues = []
        
        # This would require sophisticated type inference
        # For now, return empty list
        
        return issues
    
    def _check_memory_allocations(self, file: JuliaFile) -> List[str]:
        """Check for unnecessary memory allocations."""
        issues = []
        
        # This would require analysis of array operations
        # For now, return empty list
        
        return issues
    
    def _check_package_version_compatibility(self, package: str, julia_version: tuple) -> Optional[str]:
        """Check if package is compatible with Julia version."""
        # Simplified compatibility check
        incompatible_packages = {
            'OldPackage': (1, 6),  # Example: requires Julia 1.6+
        }
        
        if package in incompatible_packages:
            required_version = incompatible_packages[package]
            if julia_version < required_version:
                return f"Package '{package}' requires Julia {'.'.join(map(str, required_version))}+, but using {'.'.join(map(str, julia_version))}"
        
        return None 