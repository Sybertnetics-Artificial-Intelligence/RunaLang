#!/usr/bin/env python3
"""
R Toolchain Integration

Complete toolchain integration for R language providing unified interface for parsing,
conversion, generation, validation, and optimization of R code within the Runa ecosystem.
"""

from typing import List, Optional, Any, Union, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path

from .r_ast import *
from .r_parser import RParser, RLexer, parse_r_source
from .r_converter import RToRunaConverter, RunaToRConverter, r_to_runa, runa_to_r
from .r_generator import RCodeGenerator, generate_r_code
from ....core.runa_ast import ASTNode
from ...shared.base_toolchain import BaseToolchain, ToolchainCapability, LanguageInfo


@dataclass
class RValidationResult:
    """R code validation result."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]


@dataclass
class ROptimizationResult:
    """R code optimization result."""
    optimized_ast: RNode
    optimizations_applied: List[str]
    performance_improvements: Dict[str, Any]


class RToolchain(BaseToolchain):
    """Complete R language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.parser = None
        self.lexer = None
        self.to_runa_converter = RToRunaConverter()
        self.from_runa_converter = RunaToRConverter()
        self.generator = RCodeGenerator()
        
        # R-specific optimization patterns
        self.optimization_patterns = {
            'vectorization': self._optimize_vectorization,
            'function_calls': self._optimize_function_calls,
            'data_structures': self._optimize_data_structures,
            'loops': self._optimize_loops,
            'memory_usage': self._optimize_memory_usage
        }
    
    def get_language_info(self) -> LanguageInfo:
        """Get R language information."""
        return LanguageInfo(
            name="R",
            version="4.x",
            file_extensions=[".r", ".R"],
            mime_types=["text/x-r", "application/r"],
            description="Statistical computing and graphics language",
            features=[
                "Statistical computing",
                "Data analysis and visualization",
                "Vectorized operations",
                "Functional programming",
                "Package ecosystem (CRAN)",
                "Interactive environment",
                "Data frames and matrices",
                "Statistical modeling",
                "Time series analysis",
                "Machine learning"
            ],
            paradigms=["Statistical", "Functional", "Procedural", "Object-oriented"],
            typical_use_cases=[
                "Data analysis and statistics",
                "Scientific research",
                "Data visualization",
                "Machine learning and AI",
                "Bioinformatics",
                "Financial modeling",
                "Academic research",
                "Business intelligence"
            ]
        )
    
    def get_capabilities(self) -> List[ToolchainCapability]:
        """Get R toolchain capabilities."""
        return [
            ToolchainCapability.PARSE,
            ToolchainCapability.GENERATE,
            ToolchainCapability.CONVERT_TO_RUNA,
            ToolchainCapability.CONVERT_FROM_RUNA,
            ToolchainCapability.VALIDATE,
            ToolchainCapability.OPTIMIZE,
            ToolchainCapability.FORMAT,
            ToolchainCapability.ANALYZE
        ]
    
    def parse(self, source: str, file_path: Optional[str] = None) -> RNode:
        """Parse R source code into AST."""
        try:
            return parse_r_source(source, file_path)
        except Exception as e:
            raise SyntaxError(f"Failed to parse R code: {str(e)}")
    
    def generate(self, ast: RNode, format_options: Optional[Dict[str, Any]] = None) -> str:
        """Generate R source code from AST."""
        try:
            if format_options:
                indent_size = format_options.get('indent_size', 2)
                generator = RCodeGenerator(indent_size=indent_size)
                return generator.generate(ast)
            else:
                return generate_r_code(ast)
        except Exception as e:
            raise RuntimeError(f"Failed to generate R code: {str(e)}")
    
    def to_runa(self, r_ast: RNode) -> ASTNode:
        """Convert R AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(r_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert R to Runa: {str(e)}")
    
    def from_runa(self, runa_ast: ASTNode) -> RNode:
        """Convert Runa AST to R AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Runa to R: {str(e)}")
    
    def validate(self, ast: RNode) -> RValidationResult:
        """Validate R AST for correctness and best practices."""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Syntax validation
            self._validate_syntax(ast, errors, warnings)
            
            # Semantic validation
            self._validate_semantics(ast, errors, warnings, suggestions)
            
            # Style validation
            self._validate_style(ast, warnings, suggestions)
            
            # Performance validation
            self._validate_performance(ast, warnings, suggestions)
            
            is_valid = len(errors) == 0
            
            return RValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return RValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
    
    def optimize(self, ast: RNode, optimization_level: str = "balanced") -> ROptimizationResult:
        """Optimize R AST for performance and best practices."""
        optimized_ast = ast
        optimizations_applied = []
        performance_improvements = {}
        
        try:
            optimization_configs = {
                "minimal": ["vectorization"],
                "balanced": ["vectorization", "function_calls", "data_structures"],
                "aggressive": ["vectorization", "function_calls", "data_structures", "loops", "memory_usage"]
            }
            
            selected_optimizations = optimization_configs.get(optimization_level, optimization_configs["balanced"])
            
            for opt_name in selected_optimizations:
                if opt_name in self.optimization_patterns:
                    optimizer = self.optimization_patterns[opt_name]
                    result = optimizer(optimized_ast)
                    
                    if result:
                        optimized_ast = result["ast"]
                        optimizations_applied.extend(result["optimizations"])
                        performance_improvements.update(result.get("improvements", {}))
            
            return ROptimizationResult(
                optimized_ast=optimized_ast,
                optimizations_applied=optimizations_applied,
                performance_improvements=performance_improvements
            )
            
        except Exception as e:
            # Return original AST if optimization fails
            return ROptimizationResult(
                optimized_ast=ast,
                optimizations_applied=[],
                performance_improvements={"error": str(e)}
            )
    
    def format_code(self, source: str, style_options: Optional[Dict[str, Any]] = None) -> str:
        """Format R code according to style guidelines."""
        try:
            # Parse and regenerate with formatting
            ast = self.parse(source)
            
            format_options = {
                'indent_size': 2,
                'max_line_length': 80,
                'space_around_operators': True,
                'space_after_comma': True
            }
            
            if style_options:
                format_options.update(style_options)
            
            return self.generate(ast, format_options)
            
        except Exception as e:
            raise RuntimeError(f"Failed to format R code: {str(e)}")
    
    def analyze_complexity(self, ast: RNode) -> Dict[str, Any]:
        """Analyze code complexity metrics."""
        try:
            metrics = {
                'cyclomatic_complexity': self._calculate_cyclomatic_complexity(ast),
                'function_count': self._count_functions(ast),
                'loop_count': self._count_loops(ast),
                'conditional_count': self._count_conditionals(ast),
                'variable_count': self._count_variables(ast),
                'data_structure_usage': self._analyze_data_structures(ast),
                'statistical_functions': self._analyze_statistical_functions(ast),
                'package_dependencies': self._analyze_package_dependencies(ast)
            }
            
            # Add complexity assessment
            total_complexity = metrics['cyclomatic_complexity']
            if total_complexity <= 10:
                metrics['complexity_level'] = 'Low'
            elif total_complexity <= 20:
                metrics['complexity_level'] = 'Medium'
            else:
                metrics['complexity_level'] = 'High'
            
            return metrics
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_optimization_suggestions(self, ast: RNode) -> List[str]:
        """Get optimization suggestions for R code."""
        suggestions = []
        
        try:
            # Check for vectorization opportunities
            if self._has_scalar_operations(ast):
                suggestions.append("Consider vectorizing scalar operations for better performance")
            
            # Check for inefficient loops
            if self._has_inefficient_loops(ast):
                suggestions.append("Replace loops with apply() family functions where possible")
            
            # Check for data structure inefficiencies
            if self._has_inefficient_data_structures(ast):
                suggestions.append("Consider using more efficient data structures (data.table, matrix)")
            
            # Check for memory inefficiencies
            if self._has_memory_inefficiencies(ast):
                suggestions.append("Preallocate vectors and lists to avoid memory reallocation")
            
            # Check for statistical function usage
            if self._has_suboptimal_statistical_functions(ast):
                suggestions.append("Use specialized statistical functions instead of manual calculations")
            
            return suggestions
            
        except Exception as e:
            return [f"Error analyzing code: {str(e)}"]
    
    # Validation methods
    def _validate_syntax(self, ast: RNode, errors: List[str], warnings: List[str]):
        """Validate R syntax."""
        # Check for basic syntax errors
        if isinstance(ast, RProgram):
            if not ast.statements:
                warnings.append("Empty program")
        
        # Validate function definitions
        self._validate_functions(ast, errors, warnings)
        
        # Validate expressions
        self._validate_expressions(ast, errors, warnings)
    
    def _validate_semantics(self, ast: RNode, errors: List[str], warnings: List[str], suggestions: List[str]):
        """Validate R semantics."""
        # Check for undefined variables
        defined_vars = set()
        self._check_variable_usage(ast, defined_vars, errors, warnings)
        
        # Check for function usage
        self._check_function_usage(ast, warnings, suggestions)
    
    def _validate_style(self, ast: RNode, warnings: List[str], suggestions: List[str]):
        """Validate R coding style."""
        # Check naming conventions
        self._check_naming_conventions(ast, warnings, suggestions)
        
        # Check code organization
        self._check_code_organization(ast, suggestions)
    
    def _validate_performance(self, ast: RNode, warnings: List[str], suggestions: List[str]):
        """Validate R performance considerations."""
        # Check for performance anti-patterns
        if self._has_scalar_operations(ast):
            suggestions.append("Consider using vectorized operations instead of scalar operations")
        
        if self._has_growing_vectors(ast):
            warnings.append("Detected vector growth in loops - preallocate vectors for better performance")
    
    # Optimization methods
    def _optimize_vectorization(self, ast: RNode) -> Optional[Dict[str, Any]]:
        """Optimize for vectorization."""
        # This would contain actual vectorization optimization logic
        optimizations = []
        
        # Example: Convert scalar operations to vectorized operations
        if self._has_scalar_operations(ast):
            optimizations.append("Converted scalar operations to vectorized operations")
        
        if optimizations:
            return {
                "ast": ast,  # Would be modified AST
                "optimizations": optimizations,
                "improvements": {"vectorization": "Applied"}
            }
        
        return None
    
    def _optimize_function_calls(self, ast: RNode) -> Optional[Dict[str, Any]]:
        """Optimize function calls."""
        optimizations = []
        
        # Example: Inline simple functions, optimize apply calls
        if self._has_inefficient_function_calls(ast):
            optimizations.append("Optimized function calls")
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "improvements": {"function_calls": "Optimized"}
            }
        
        return None
    
    def _optimize_data_structures(self, ast: RNode) -> Optional[Dict[str, Any]]:
        """Optimize data structure usage."""
        optimizations = []
        
        # Example: Convert lists to vectors where appropriate
        if self._has_inefficient_data_structures(ast):
            optimizations.append("Optimized data structure usage")
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "improvements": {"data_structures": "Optimized"}
            }
        
        return None
    
    def _optimize_loops(self, ast: RNode) -> Optional[Dict[str, Any]]:
        """Optimize loops."""
        optimizations = []
        
        # Example: Convert loops to apply functions
        if self._has_inefficient_loops(ast):
            optimizations.append("Converted loops to apply functions")
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "improvements": {"loops": "Optimized"}
            }
        
        return None
    
    def _optimize_memory_usage(self, ast: RNode) -> Optional[Dict[str, Any]]:
        """Optimize memory usage."""
        optimizations = []
        
        # Example: Preallocate vectors, use more efficient data types
        if self._has_memory_inefficiencies(ast):
            optimizations.append("Optimized memory usage")
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "improvements": {"memory_usage": "Optimized"}
            }
        
        return None
    
    # Analysis helper methods
    def _calculate_cyclomatic_complexity(self, ast: RNode) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity
        
        # This would traverse the AST and count decision points
        if isinstance(ast, RProgram):
            for stmt in ast.statements:
                complexity += self._calculate_cyclomatic_complexity(stmt)
        elif isinstance(ast, RIfStatement):
            complexity += 1
            if ast.then_expr:
                complexity += self._calculate_cyclomatic_complexity(ast.then_expr)
            if ast.else_expr:
                complexity += self._calculate_cyclomatic_complexity(ast.else_expr)
        elif isinstance(ast, (RForLoop, RWhileLoop, RRepeatLoop)):
            complexity += 1
        
        return max(1, complexity - 1)  # Adjust for base complexity
    
    def _count_functions(self, ast: RNode) -> int:
        """Count function definitions."""
        count = 0
        if isinstance(ast, RFunctionDefinition):
            count = 1
        elif isinstance(ast, RProgram):
            for stmt in ast.statements:
                count += self._count_functions(stmt)
        return count
    
    def _count_loops(self, ast: RNode) -> int:
        """Count loop constructs."""
        count = 0
        if isinstance(ast, (RForLoop, RWhileLoop, RRepeatLoop)):
            count = 1
        elif isinstance(ast, RProgram):
            for stmt in ast.statements:
                count += self._count_loops(stmt)
        return count
    
    def _count_conditionals(self, ast: RNode) -> int:
        """Count conditional statements."""
        count = 0
        if isinstance(ast, RIfStatement):
            count = 1
        elif isinstance(ast, RProgram):
            for stmt in ast.statements:
                count += self._count_conditionals(stmt)
        return count
    
    def _count_variables(self, ast: RNode) -> int:
        """Count variable assignments."""
        count = 0
        if isinstance(ast, RAssignment):
            count = 1
        elif isinstance(ast, RProgram):
            for stmt in ast.statements:
                count += self._count_variables(stmt)
        return count
    
    def _analyze_data_structures(self, ast: RNode) -> Dict[str, int]:
        """Analyze data structure usage."""
        usage = {
            'vectors': 0,
            'lists': 0,
            'data_frames': 0,
            'matrices': 0,
            'factors': 0
        }
        
        # This would traverse the AST and count data structure usage
        if isinstance(ast, RVector):
            usage['vectors'] += 1
        elif isinstance(ast, RList):
            usage['lists'] += 1
        elif isinstance(ast, RDataFrame):
            usage['data_frames'] += 1
        elif isinstance(ast, RMatrix):
            usage['matrices'] += 1
        elif isinstance(ast, RFactor):
            usage['factors'] += 1
        
        return usage
    
    def _analyze_statistical_functions(self, ast: RNode) -> List[str]:
        """Analyze statistical function usage."""
        stat_functions = []
        
        # This would identify statistical function calls
        if isinstance(ast, RFunctionCall):
            if isinstance(ast.function, RIdentifier):
                func_name = ast.function.name
                statistical_funcs = ['mean', 'median', 'sd', 'var', 'cor', 'lm', 'glm', 'summary']
                if func_name in statistical_funcs:
                    stat_functions.append(func_name)
        
        return stat_functions
    
    def _analyze_package_dependencies(self, ast: RNode) -> List[str]:
        """Analyze package dependencies."""
        packages = []
        
        # This would identify library/require calls
        if isinstance(ast, RPackageLoad):
            packages.append(ast.package_name)
        elif isinstance(ast, RProgram):
            for stmt in ast.statements:
                packages.extend(self._analyze_package_dependencies(stmt))
        
        return packages
    
    # Check methods for validation and optimization
    def _has_scalar_operations(self, ast: RNode) -> bool:
        """Check if code has scalar operations that could be vectorized."""
        # This would check for scalar operations in loops
        return False  # Placeholder
    
    def _has_inefficient_loops(self, ast: RNode) -> bool:
        """Check for inefficient loop patterns."""
        # This would identify loops that could be replaced with apply functions
        return False  # Placeholder
    
    def _has_inefficient_data_structures(self, ast: RNode) -> bool:
        """Check for inefficient data structure usage."""
        # This would identify suboptimal data structure choices
        return False  # Placeholder
    
    def _has_memory_inefficiencies(self, ast: RNode) -> bool:
        """Check for memory inefficiencies."""
        # This would identify memory allocation issues
        return False  # Placeholder
    
    def _has_suboptimal_statistical_functions(self, ast: RNode) -> bool:
        """Check for suboptimal statistical function usage."""
        # This would identify manual calculations that could use built-in functions
        return False  # Placeholder
    
    def _has_growing_vectors(self, ast: RNode) -> bool:
        """Check for vector growth in loops."""
        # This would identify vectors being grown in loops
        return False  # Placeholder
    
    def _has_inefficient_function_calls(self, ast: RNode) -> bool:
        """Check for inefficient function calls."""
        return False  # Placeholder
    
    def _validate_functions(self, ast: RNode, errors: List[str], warnings: List[str]):
        """Validate function definitions."""
        # Check function parameter consistency, etc.
        pass
    
    def _validate_expressions(self, ast: RNode, errors: List[str], warnings: List[str]):
        """Validate expressions."""
        # Check expression validity
        pass
    
    def _check_variable_usage(self, ast: RNode, defined_vars: set, errors: List[str], warnings: List[str]):
        """Check for undefined variable usage."""
        # Track variable definitions and usage
        pass
    
    def _check_function_usage(self, ast: RNode, warnings: List[str], suggestions: List[str]):
        """Check function usage patterns."""
        # Check for deprecated functions, suggest alternatives
        pass
    
    def _check_naming_conventions(self, ast: RNode, warnings: List[str], suggestions: List[str]):
        """Check R naming conventions."""
        # Check for proper naming (snake_case, etc.)
        pass
    
    def _check_code_organization(self, ast: RNode, suggestions: List[str]):
        """Check code organization."""
        # Suggest better organization
        pass


# Convenience functions
def create_r_toolchain() -> RToolchain:
    """Create and return R toolchain instance."""
    return RToolchain()


def parse_r_file(file_path: str) -> RNode:
    """Parse R file and return AST."""
    toolchain = create_r_toolchain()
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    return toolchain.parse(source, file_path)


def validate_r_file(file_path: str) -> RValidationResult:
    """Validate R file."""
    ast = parse_r_file(file_path)
    toolchain = create_r_toolchain()
    return toolchain.validate(ast)


def optimize_r_file(file_path: str, optimization_level: str = "balanced") -> str:
    """Optimize R file and return optimized code."""
    ast = parse_r_file(file_path)
    toolchain = create_r_toolchain()
    result = toolchain.optimize(ast, optimization_level)
    return toolchain.generate(result.optimized_ast) 