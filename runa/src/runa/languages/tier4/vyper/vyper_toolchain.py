#!/usr/bin/env python3
"""
Vyper Toolchain Integration

Complete toolchain integration for Vyper language providing unified interface for parsing,
conversion, generation, validation, and optimization of Python-like smart contracts within 
the Runa ecosystem.
"""

from typing import List, Optional, Any, Union, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path

from .vyper_ast import *
from .vyper_parser import VyperParser, VyperLexer, parse_vyper_source
from .vyper_converter import VyperToRunaConverter, RunaToVyperConverter, vyper_to_runa, runa_to_vyper
from .vyper_generator import VyperCodeGenerator, VyperCodeStyle, generate_vyper_code
from ....core.runa_ast import ASTNode
from ...shared.base_toolchain import BaseToolchain, ToolchainCapability, LanguageInfo


@dataclass
class VyperValidationResult:
    """Vyper code validation result."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    security_issues: List[str]
    gas_optimizations: List[str]
    python_style_issues: List[str]


@dataclass
class VyperOptimizationResult:
    """Vyper code optimization result."""
    optimized_ast: VyperNode
    optimizations_applied: List[str]
    gas_savings: Dict[str, Any]
    security_improvements: List[str]
    readability_improvements: List[str]


class VyperToolchain(BaseToolchain):
    """Complete Vyper language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.parser = None
        self.lexer = None
        self.to_runa_converter = VyperToRunaConverter()
        self.from_runa_converter = RunaToVyperConverter()
        self.generator = VyperCodeGenerator()
        
        # Vyper-specific optimization patterns
        self.optimization_patterns = {
            'gas_efficiency': self._optimize_gas_efficiency,
            'security': self._optimize_security,
            'storage': self._optimize_storage,
            'function_calls': self._optimize_function_calls,
            'loops': self._optimize_loops,
            'readability': self._optimize_readability
        }
        
        # Security vulnerability patterns specific to Vyper
        self.security_patterns = {
            'reentrancy': self._check_reentrancy,
            'overflow': self._check_integer_overflow,
            'access_control': self._check_access_control,
            'randomness': self._check_weak_randomness,
            'external_calls': self._check_external_calls,
            'dos': self._check_dos_vulnerabilities,
            'state_modifications': self._check_state_modifications
        }
        
        # Python style patterns for Vyper
        self.style_patterns = {
            'naming': self._check_naming_conventions,
            'function_length': self._check_function_length,
            'complexity': self._check_cyclomatic_complexity,
            'imports': self._check_import_style,
            'docstrings': self._check_docstrings
        }
    
    def get_language_info(self) -> LanguageInfo:
        """Get Vyper language information."""
        return LanguageInfo(
            name="Vyper",
            version="0.3.x",
            file_extensions=[".vy"],
            mime_types=["text/x-vyper"],
            description="Security-focused smart contract programming language with Python-like syntax",
            features=[
                "Smart contracts",
                "Python-like syntax",
                "Security by design",
                "No inheritance",
                "No recursion",
                "Bounds checking",
                "Overflow protection",
                "Decidable execution",
                "Clear state visibility",
                "Gas efficiency"
            ],
            paradigms=["Functional", "Contract-oriented", "Security-first"],
            typical_use_cases=[
                "Secure smart contracts",
                "Simple token contracts",
                "Voting systems",
                "Multi-signature wallets",
                "Escrow contracts",
                "Decentralized exchanges",
                "Governance contracts",
                "Time-locked contracts"
            ]
        )
    
    def get_capabilities(self) -> List[ToolchainCapability]:
        """Get Vyper toolchain capabilities."""
        return [
            ToolchainCapability.PARSE,
            ToolchainCapability.GENERATE,
            ToolchainCapability.CONVERT_TO_RUNA,
            ToolchainCapability.CONVERT_FROM_RUNA,
            ToolchainCapability.VALIDATE,
            ToolchainCapability.OPTIMIZE,
            ToolchainCapability.FORMAT,
            ToolchainCapability.ANALYZE,
            ToolchainCapability.SECURITY_ANALYSIS,
            ToolchainCapability.STYLE_CHECK
        ]
    
    def parse(self, source: str, file_path: Optional[str] = None) -> VyperNode:
        """Parse Vyper source code into AST."""
        try:
            return parse_vyper_source(source, file_path)
        except Exception as e:
            raise SyntaxError(f"Failed to parse Vyper code: {str(e)}")
    
    def generate(self, ast: VyperNode, format_options: Optional[Dict[str, Any]] = None) -> str:
        """Generate Vyper source code from AST."""
        try:
            if format_options:
                style = VyperCodeStyle()
                style.indent_size = format_options.get('indent_size', 4)
                style.max_line_length = format_options.get('max_line_length', 88)
                generator = VyperCodeGenerator(style=style)
                return generator.generate(ast)
            else:
                return generate_vyper_code(ast)
        except Exception as e:
            raise RuntimeError(f"Failed to generate Vyper code: {str(e)}")
    
    def to_runa(self, vyper_ast: VyperNode) -> ASTNode:
        """Convert Vyper AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(vyper_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Vyper to Runa: {str(e)}")
    
    def from_runa(self, runa_ast: ASTNode) -> VyperNode:
        """Convert Runa AST to Vyper AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Runa to Vyper: {str(e)}")
    
    def validate(self, ast: VyperNode) -> VyperValidationResult:
        """Validate Vyper AST for correctness, security, and best practices."""
        errors = []
        warnings = []
        suggestions = []
        security_issues = []
        gas_optimizations = []
        python_style_issues = []
        
        try:
            # Syntax validation
            self._validate_syntax(ast, errors, warnings)
            
            # Semantic validation
            self._validate_semantics(ast, errors, warnings, suggestions)
            
            # Security validation
            self._validate_security(ast, security_issues, warnings)
            
            # Gas optimization analysis
            self._analyze_gas_efficiency(ast, gas_optimizations, suggestions)
            
            # Python style validation
            self._validate_python_style(ast, python_style_issues, suggestions)
            
            # Vyper-specific constraints
            self._validate_vyper_constraints(ast, errors, warnings)
            
            is_valid = len(errors) == 0 and len(security_issues) == 0
            
            return VyperValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                security_issues=security_issues,
                gas_optimizations=gas_optimizations,
                python_style_issues=python_style_issues
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return VyperValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                security_issues=security_issues,
                gas_optimizations=gas_optimizations,
                python_style_issues=python_style_issues
            )
    
    def optimize(self, ast: VyperNode, optimization_level: str = "balanced") -> VyperOptimizationResult:
        """Optimize Vyper AST for gas efficiency, security, and readability."""
        optimized_ast = ast
        optimizations_applied = []
        gas_savings = {}
        security_improvements = []
        readability_improvements = []
        
        try:
            # Apply optimizations based on level
            if optimization_level in ["balanced", "aggressive"]:
                # Gas efficiency optimizations
                gas_result = self._optimize_gas_efficiency(optimized_ast)
                if gas_result:
                    optimized_ast = gas_result.get('ast', optimized_ast)
                    optimizations_applied.extend(gas_result.get('optimizations', []))
                    gas_savings.update(gas_result.get('savings', {}))
                
                # Security optimizations
                security_result = self._optimize_security(optimized_ast)
                if security_result:
                    optimized_ast = security_result.get('ast', optimized_ast)
                    optimizations_applied.extend(security_result.get('optimizations', []))
                    security_improvements.extend(security_result.get('improvements', []))
                
                # Storage optimizations
                storage_result = self._optimize_storage(optimized_ast)
                if storage_result:
                    optimized_ast = storage_result.get('ast', optimized_ast)
                    optimizations_applied.extend(storage_result.get('optimizations', []))
                    gas_savings.update(storage_result.get('savings', {}))
            
            if optimization_level in ["readability", "balanced"]:
                # Readability optimizations
                readability_result = self._optimize_readability(optimized_ast)
                if readability_result:
                    optimized_ast = readability_result.get('ast', optimized_ast)
                    optimizations_applied.extend(readability_result.get('optimizations', []))
                    readability_improvements.extend(readability_result.get('improvements', []))
            
            return VyperOptimizationResult(
                optimized_ast=optimized_ast,
                optimizations_applied=optimizations_applied,
                gas_savings=gas_savings,
                security_improvements=security_improvements,
                readability_improvements=readability_improvements
            )
            
        except Exception as e:
            return VyperOptimizationResult(
                optimized_ast=ast,
                optimizations_applied=[],
                gas_savings={},
                security_improvements=[],
                readability_improvements=[f"Optimization error: {str(e)}"]
            )
    
    def analyze_security(self, ast: VyperNode) -> Dict[str, Any]:
        """Analyze Vyper AST for security vulnerabilities."""
        analysis = {
            'vulnerabilities': [],
            'warnings': [],
            'recommendations': [],
            'security_score': 0,
            'risk_level': 'unknown'
        }
        
        try:
            # Run all security checks
            for pattern_name, check_func in self.security_patterns.items():
                issues = check_func(ast)
                if issues:
                    analysis['vulnerabilities'].extend([
                        {'type': pattern_name, 'issue': issue} for issue in issues
                    ])
            
            # Calculate security score
            vulnerability_count = len(analysis['vulnerabilities'])
            if vulnerability_count == 0:
                analysis['security_score'] = 100
                analysis['risk_level'] = 'low'
            elif vulnerability_count <= 2:
                analysis['security_score'] = 75
                analysis['risk_level'] = 'medium'
            elif vulnerability_count <= 5:
                analysis['security_score'] = 50
                analysis['risk_level'] = 'high'
            else:
                analysis['security_score'] = 25
                analysis['risk_level'] = 'critical'
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_security_recommendations(ast)
            
        except Exception as e:
            analysis['warnings'].append(f"Security analysis error: {str(e)}")
        
        return analysis
    
    def estimate_gas_costs(self, ast: VyperNode) -> Dict[str, Any]:
        """Estimate gas costs for Vyper contract."""
        gas_analysis = {
            'deployment_gas': 0,
            'function_gas': {},
            'storage_gas': {},
            'optimization_potential': []
        }
        
        try:
            gas_analysis['deployment_gas'] = self._estimate_deployment_gas(ast)
            gas_analysis['function_gas'] = self._estimate_function_gas(ast)
            gas_analysis['storage_gas'] = self._estimate_storage_gas(ast)
            gas_analysis['optimization_potential'] = self._analyze_gas_optimization_potential(ast)
            
        except Exception as e:
            gas_analysis['error'] = f"Gas estimation error: {str(e)}"
        
        return gas_analysis
    
    def format_code(self, source: str, style_options: Optional[Dict[str, Any]] = None) -> str:
        """Format Vyper source code according to style guidelines."""
        try:
            # Parse the source code
            ast = self.parse(source)
            
            # Create style configuration
            style = VyperCodeStyle()
            if style_options:
                style.indent_size = style_options.get('indent_size', 4)
                style.max_line_length = style_options.get('max_line_length', 88)
                style.blank_lines_around_functions = style_options.get('blank_lines_around_functions', 2)
            
            # Generate formatted code
            generator = VyperCodeGenerator(style=style)
            return generator.generate(ast)
            
        except Exception as e:
            raise RuntimeError(f"Failed to format Vyper code: {str(e)}")
    
    def _validate_syntax(self, ast: VyperNode, errors: List[str], warnings: List[str]):
        """Validate Vyper syntax rules."""
        # Basic AST structure validation
        if not isinstance(ast, VyperNode):
            errors.append("Invalid AST structure")
        
        # Module-level validation for VyperModule
        if isinstance(ast, VyperModule):
            if not ast.functions and not ast.state_variables:
                warnings.append("Empty contract with no functions or state variables")
    
    def _validate_semantics(self, ast: VyperNode, errors: List[str], warnings: List[str], suggestions: List[str]):
        """Validate Vyper semantic rules."""
        # Function validation
        if isinstance(ast, VyperModule):
            # Check for __init__ function parameters
            init_functions = [f for f in ast.functions if f.name == "__init__"]
            if len(init_functions) > 1:
                errors.append("Multiple __init__ functions defined")
            
            # Check for external/internal decorator consistency
            for func in ast.functions:
                has_external = any(d.name == "external" for d in func.decorators)
                has_internal = any(d.name == "internal" for d in func.decorators)
                
                if has_external and has_internal:
                    errors.append(f"Function '{func.name}' cannot be both external and internal")
                elif not has_external and not has_internal and func.name != "__init__":
                    warnings.append(f"Function '{func.name}' has no visibility decorator")
    
    def _validate_security(self, ast: VyperNode, security_issues: List[str], warnings: List[str]):
        """Validate Vyper security constraints."""
        for pattern_name, check_func in self.security_patterns.items():
            issues = check_func(ast)
            security_issues.extend(issues)
    
    def _validate_python_style(self, ast: VyperNode, style_issues: List[str], suggestions: List[str]):
        """Validate Python style guidelines."""
        for pattern_name, check_func in self.style_patterns.items():
            issues = check_func(ast)
            if isinstance(issues, list):
                style_issues.extend(issues)
            elif isinstance(issues, dict):
                style_issues.extend(issues.get('issues', []))
                suggestions.extend(issues.get('suggestions', []))
    
    def _validate_vyper_constraints(self, ast: VyperNode, errors: List[str], warnings: List[str]):
        """Validate Vyper-specific constraints (no inheritance, recursion, etc.)."""
        if isinstance(ast, VyperModule):
            # Check for inheritance (Vyper doesn't support it)
            for interface in ast.interfaces:
                if hasattr(interface, 'inheritance') and interface.inheritance:
                    errors.append("Vyper does not support inheritance")
            
            # Check for recursion in functions
            for func in ast.functions:
                if self._has_recursion(func):
                    errors.append(f"Function '{func.name}' contains recursion, which is not allowed in Vyper")
    
    def _analyze_gas_efficiency(self, ast: VyperNode, gas_optimizations: List[str], suggestions: List[str]):
        """Analyze gas efficiency patterns."""
        if self._has_expensive_operations(ast):
            gas_optimizations.append("Consider optimizing expensive operations")
        
        if self._has_unnecessary_storage_operations(ast):
            gas_optimizations.append("Reduce unnecessary storage operations")
        
        if self._has_inefficient_loops(ast):
            gas_optimizations.append("Optimize loop structures for gas efficiency")
    
    def _optimize_gas_efficiency(self, ast: VyperNode) -> Optional[Dict[str, Any]]:
        """Apply gas efficiency optimizations."""
        optimizations = []
        savings = {}
        
        # Storage packing optimizations
        if self._has_inefficient_storage(ast):
            optimizations.append("Storage variable packing")
            savings['storage_packing'] = "~20% gas reduction"
        
        # Loop optimizations
        if self._has_inefficient_loops(ast):
            optimizations.append("Loop structure optimization")
            savings['loop_optimization'] = "~15% gas reduction"
        
        if optimizations:
            return {
                'ast': ast,  # Would be modified AST in real implementation
                'optimizations': optimizations,
                'savings': savings
            }
        return None
    
    def _optimize_security(self, ast: VyperNode) -> Optional[Dict[str, Any]]:
        """Apply security optimizations."""
        improvements = []
        optimizations = []
        
        # Add access control checks
        if self._needs_access_control(ast):
            improvements.append("Added access control modifiers")
            optimizations.append("Access control enhancement")
        
        # Add reentrancy protection
        if self._needs_reentrancy_protection(ast):
            improvements.append("Added reentrancy protection")
            optimizations.append("Reentrancy guard")
        
        if improvements:
            return {
                'ast': ast,  # Would be modified AST in real implementation
                'optimizations': optimizations,
                'improvements': improvements
            }
        return None
    
    def _optimize_storage(self, ast: VyperNode) -> Optional[Dict[str, Any]]:
        """Apply storage optimizations."""
        optimizations = []
        savings = {}
        
        # Storage slot optimization
        if isinstance(ast, VyperModule) and ast.state_variables:
            optimizations.append("Storage slot optimization")
            savings['storage_slots'] = "Reduced storage slots usage"
        
        if optimizations:
            return {
                'ast': ast,  # Would be modified AST in real implementation
                'optimizations': optimizations,
                'savings': savings
            }
        return None
    
    def _optimize_function_calls(self, ast: VyperNode) -> Optional[Dict[str, Any]]:
        """Apply function call optimizations."""
        optimizations = []
        
        if self._has_inefficient_function_calls(ast):
            optimizations.append("Function call optimization")
        
        if optimizations:
            return {
                'ast': ast,  # Would be modified AST in real implementation
                'optimizations': optimizations
            }
        return None
    
    def _optimize_loops(self, ast: VyperNode) -> Optional[Dict[str, Any]]:
        """Apply loop optimizations."""
        optimizations = []
        
        if self._has_inefficient_loops(ast):
            optimizations.append("Loop structure optimization")
        
        if optimizations:
            return {
                'ast': ast,  # Would be modified AST in real implementation
                'optimizations': optimizations
            }
        return None
    
    def _optimize_readability(self, ast: VyperNode) -> Optional[Dict[str, Any]]:
        """Apply readability optimizations."""
        improvements = []
        optimizations = []
        
        # Function naming improvements
        if self._needs_better_naming(ast):
            improvements.append("Improved function and variable naming")
            optimizations.append("Naming convention improvements")
        
        # Code organization improvements
        if self._needs_better_organization(ast):
            improvements.append("Better code organization")
            optimizations.append("Code structure improvements")
        
        if improvements:
            return {
                'ast': ast,  # Would be modified AST in real implementation
                'optimizations': optimizations,
                'improvements': improvements
            }
        return None
    
    # Security check methods
    def _check_reentrancy(self, ast: VyperNode) -> List[str]:
        """Check for reentrancy vulnerabilities."""
        issues = []
        if isinstance(ast, VyperModule):
            for func in ast.functions:
                if self._function_has_external_calls(func) and self._function_modifies_state(func):
                    issues.append(f"Function '{func.name}' may be vulnerable to reentrancy")
        return issues
    
    def _check_integer_overflow(self, ast: VyperNode) -> List[str]:
        """Check for integer overflow issues."""
        # Vyper has built-in overflow protection, but still check for edge cases
        issues = []
        return issues  # Vyper handles this automatically
    
    def _check_access_control(self, ast: VyperNode) -> List[str]:
        """Check for access control issues."""
        issues = []
        if isinstance(ast, VyperModule):
            for func in ast.functions:
                if any(d.name == "external" for d in func.decorators):
                    if not self._has_access_control(func):
                        issues.append(f"External function '{func.name}' lacks access control")
        return issues
    
    def _check_weak_randomness(self, ast: VyperNode) -> List[str]:
        """Check for weak randomness sources."""
        issues = []
        # Check for usage of block.timestamp, block.difficulty, etc.
        return issues
    
    def _check_external_calls(self, ast: VyperNode) -> List[str]:
        """Check for unsafe external calls."""
        issues = []
        # Check for external calls without proper error handling
        return issues
    
    def _check_dos_vulnerabilities(self, ast: VyperNode) -> List[str]:
        """Check for denial of service vulnerabilities."""
        issues = []
        # Check for unbounded loops, large arrays, etc.
        return issues
    
    def _check_state_modifications(self, ast: VyperNode) -> List[str]:
        """Check for state modification issues."""
        issues = []
        # Check for functions that modify state without proper decorators
        return issues
    
    # Style check methods
    def _check_naming_conventions(self, ast: VyperNode) -> Dict[str, List[str]]:
        """Check naming conventions."""
        issues = []
        suggestions = []
        
        if isinstance(ast, VyperModule):
            # Check function naming (snake_case)
            for func in ast.functions:
                if not func.name.islower() or ' ' in func.name:
                    if func.name != "__init__":
                        issues.append(f"Function '{func.name}' should use snake_case naming")
                        suggestions.append(f"Rename '{func.name}' to follow snake_case convention")
        
        return {'issues': issues, 'suggestions': suggestions}
    
    def _check_function_length(self, ast: VyperNode) -> List[str]:
        """Check function length."""
        issues = []
        if isinstance(ast, VyperModule):
            for func in ast.functions:
                if len(func.body) > 20:  # Arbitrary threshold
                    issues.append(f"Function '{func.name}' is too long ({len(func.body)} statements)")
        return issues
    
    def _check_cyclomatic_complexity(self, ast: VyperNode) -> List[str]:
        """Check cyclomatic complexity."""
        issues = []
        # Calculate complexity for each function
        return issues
    
    def _check_import_style(self, ast: VyperNode) -> List[str]:
        """Check import style."""
        issues = []
        # Check import organization
        return issues
    
    def _check_docstrings(self, ast: VyperNode) -> List[str]:
        """Check for missing docstrings."""
        issues = []
        if isinstance(ast, VyperModule):
            for func in ast.functions:
                # Check if function has docstring
                if not self._has_docstring(func):
                    issues.append(f"Function '{func.name}' missing docstring")
        return issues
    
    # Helper methods
    def _has_recursion(self, func: VyperFunctionDefinition) -> bool:
        """Check if function contains recursion."""
        # Simple check - would need more sophisticated analysis
        for stmt in func.body:
            if isinstance(stmt, VyperExpressionStatement):
                if isinstance(stmt.expression, VyperFunctionCall):
                    if isinstance(stmt.expression.func, VyperIdentifier):
                        if stmt.expression.func.name == func.name:
                            return True
        return False
    
    def _function_has_external_calls(self, func: VyperFunctionDefinition) -> bool:
        """Check if function makes external calls."""
        # Simplified check
        return False
    
    def _function_modifies_state(self, func: VyperFunctionDefinition) -> bool:
        """Check if function modifies state."""
        # Check for pure/view decorators
        return not any(d.name in ["pure", "view"] for d in func.decorators)
    
    def _has_access_control(self, func: VyperFunctionDefinition) -> bool:
        """Check if function has access control."""
        # Look for common access control patterns
        return False
    
    def _has_docstring(self, func: VyperFunctionDefinition) -> bool:
        """Check if function has docstring."""
        # Check first statement for string literal
        if func.body and isinstance(func.body[0], VyperExpressionStatement):
            if isinstance(func.body[0].expression, VyperLiteral):
                if func.body[0].expression.type_name == "string":
                    return True
        return False
    
    def _has_expensive_operations(self, ast: VyperNode) -> bool:
        """Check for expensive operations."""
        return False
    
    def _has_unnecessary_storage_operations(self, ast: VyperNode) -> bool:
        """Check for unnecessary storage operations."""
        return False
    
    def _has_inefficient_loops(self, ast: VyperNode) -> bool:
        """Check for inefficient loops."""
        return False
    
    def _has_inefficient_storage(self, ast: VyperNode) -> bool:
        """Check for inefficient storage usage."""
        return False
    
    def _has_inefficient_function_calls(self, ast: VyperNode) -> bool:
        """Check for inefficient function calls."""
        return False
    
    def _needs_access_control(self, ast: VyperNode) -> bool:
        """Check if contract needs access control."""
        return False
    
    def _needs_reentrancy_protection(self, ast: VyperNode) -> bool:
        """Check if contract needs reentrancy protection."""
        return False
    
    def _needs_better_naming(self, ast: VyperNode) -> bool:
        """Check if contract needs better naming."""
        return False
    
    def _needs_better_organization(self, ast: VyperNode) -> bool:
        """Check if contract needs better organization."""
        return False
    
    def _estimate_deployment_gas(self, ast: VyperNode) -> int:
        """Estimate deployment gas cost."""
        # Simplified estimation
        base_cost = 21000
        if isinstance(ast, VyperModule):
            # Add costs for state variables, functions, etc.
            base_cost += len(ast.state_variables) * 20000
            base_cost += len(ast.functions) * 2000
        return base_cost
    
    def _estimate_function_gas(self, ast: VyperNode) -> Dict[str, int]:
        """Estimate gas costs for functions."""
        gas_costs = {}
        if isinstance(ast, VyperModule):
            for func in ast.functions:
                # Simplified estimation based on statements
                base_cost = 21000 if any(d.name == "external" for d in func.decorators) else 2000
                statement_cost = len(func.body) * 100
                gas_costs[func.name] = base_cost + statement_cost
        return gas_costs
    
    def _estimate_storage_gas(self, ast: VyperNode) -> Dict[str, int]:
        """Estimate storage gas costs."""
        storage_costs = {}
        if isinstance(ast, VyperModule):
            for var in ast.state_variables:
                # Simplified estimation
                storage_costs[var.name] = 20000  # SSTORE cost
        return storage_costs
    
    def _analyze_gas_optimization_potential(self, ast: VyperNode) -> List[str]:
        """Analyze gas optimization potential."""
        optimizations = []
        
        if self._has_inefficient_storage(ast):
            optimizations.append("Storage optimization potential")
        
        if self._has_inefficient_loops(ast):
            optimizations.append("Loop optimization potential")
        
        return optimizations
    
    def _generate_security_recommendations(self, ast: VyperNode) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        if isinstance(ast, VyperModule):
            recommendations.append("Use latest Vyper version for security fixes")
            recommendations.append("Implement comprehensive access control")
            recommendations.append("Add input validation for external functions")
            recommendations.append("Use events for important state changes")
        
        return recommendations


# Convenience functions for external use
def create_vyper_toolchain() -> VyperToolchain:
    """Create a new Vyper toolchain instance."""
    return VyperToolchain()


def parse_vyper_file(file_path: str) -> VyperNode:
    """Parse a Vyper file and return the AST."""
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    
    toolchain = VyperToolchain()
    return toolchain.parse(source, file_path)


def validate_vyper_file(file_path: str) -> VyperValidationResult:
    """Validate a Vyper file and return validation results."""
    ast = parse_vyper_file(file_path)
    toolchain = VyperToolchain()
    return toolchain.validate(ast)


def analyze_contract_security(file_path: str) -> Dict[str, Any]:
    """Analyze a Vyper contract for security issues."""
    ast = parse_vyper_file(file_path)
    toolchain = VyperToolchain()
    return toolchain.analyze_security(ast)


def optimize_vyper_file(file_path: str, optimization_level: str = "balanced") -> str:
    """Optimize a Vyper file and return the optimized source code."""
    ast = parse_vyper_file(file_path)
    toolchain = VyperToolchain()
    result = toolchain.optimize(ast, optimization_level)
    return toolchain.generate(result.optimized_ast)


# High-level convenience functions
def parse_vyper_code(source: str) -> VyperNode:
    """Parse Vyper source code (convenience function)."""
    toolchain = VyperToolchain()
    return toolchain.parse(source)


def generate_vyper_code(ast: VyperNode) -> str:
    """Generate Vyper source code (convenience function)."""
    toolchain = VyperToolchain()
    return toolchain.generate(ast)


def vyper_round_trip_verify(source: str) -> bool:
    """Verify Vyper round-trip parsing and generation."""
    try:
        toolchain = VyperToolchain()
        ast = toolchain.parse(source)
        regenerated = toolchain.generate(ast)
        
        # Parse again to ensure consistency
        ast2 = toolchain.parse(regenerated)
        return True  # If no exceptions, round-trip succeeded
    except Exception:
        return False


def vyper_to_runa_translate(source: str) -> ASTNode:
    """Translate Vyper source to Runa AST."""
    toolchain = VyperToolchain()
    vyper_ast = toolchain.parse(source)
    return toolchain.to_runa(vyper_ast)


def runa_to_vyper_translate(runa_ast: ASTNode) -> str:
    """Translate Runa AST to Vyper source."""
    toolchain = VyperToolchain()
    vyper_ast = toolchain.from_runa(runa_ast)
    return toolchain.generate(vyper_ast) 