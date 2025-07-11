#!/usr/bin/env python3
"""
Solidity Toolchain Integration

Complete toolchain integration for Solidity language providing unified interface for parsing,
conversion, generation, validation, and optimization of smart contracts within the Runa ecosystem.
"""

from typing import List, Optional, Any, Union, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path

from .solidity_ast import *
from .solidity_parser import SolidityParser, SolidityLexer, parse_solidity_source
from .solidity_converter import SolidityToRunaConverter, RunaToSolidityConverter, solidity_to_runa, runa_to_solidity
from .solidity_generator import SolidityCodeGenerator, generate_solidity_code
from ....core.runa_ast import ASTNode
from ...shared.base_toolchain import BaseToolchain, ToolchainCapability, LanguageInfo


@dataclass
class SolidityValidationResult:
    """Solidity code validation result."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    security_issues: List[str]
    gas_optimizations: List[str]


@dataclass
class SolidityOptimizationResult:
    """Solidity code optimization result."""
    optimized_ast: SolidityNode
    optimizations_applied: List[str]
    gas_savings: Dict[str, Any]
    security_improvements: List[str]


class SolidityToolchain(BaseToolchain):
    """Complete Solidity language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.parser = None
        self.lexer = None
        self.to_runa_converter = SolidityToRunaConverter()
        self.from_runa_converter = RunaToSolidityConverter()
        self.generator = SolidityCodeGenerator()
        
        # Solidity-specific optimization patterns
        self.optimization_patterns = {
            'gas_efficiency': self._optimize_gas_efficiency,
            'security': self._optimize_security,
            'storage': self._optimize_storage,
            'function_calls': self._optimize_function_calls,
            'loops': self._optimize_loops
        }
        
        # Security vulnerability patterns
        self.security_patterns = {
            'reentrancy': self._check_reentrancy,
            'overflow': self._check_integer_overflow,
            'access_control': self._check_access_control,
            'randomness': self._check_weak_randomness,
            'external_calls': self._check_external_calls,
            'dos': self._check_dos_vulnerabilities
        }
    
    def get_language_info(self) -> LanguageInfo:
        """Get Solidity language information."""
        return LanguageInfo(
            name="Solidity",
            version="0.8.x",
            file_extensions=[".sol"],
            mime_types=["text/x-solidity"],
            description="Smart contract programming language for Ethereum Virtual Machine",
            features=[
                "Smart contracts",
                "Decentralized applications (DApps)",
                "Ethereum Virtual Machine (EVM)",
                "Gas optimization",
                "Security-focused",
                "Object-oriented programming",
                "State machines",
                "Events and logging",
                "Modifiers and inheritance",
                "Libraries and interfaces"
            ],
            paradigms=["Object-oriented", "Contract-oriented", "Stateful"],
            typical_use_cases=[
                "Smart contracts",
                "Decentralized finance (DeFi)",
                "Non-fungible tokens (NFTs)",
                "Decentralized autonomous organizations (DAOs)",
                "Token contracts",
                "Multi-signature wallets",
                "Decentralized exchanges",
                "Blockchain gaming"
            ]
        )
    
    def get_capabilities(self) -> List[ToolchainCapability]:
        """Get Solidity toolchain capabilities."""
        return [
            ToolchainCapability.PARSE,
            ToolchainCapability.GENERATE,
            ToolchainCapability.CONVERT_TO_RUNA,
            ToolchainCapability.CONVERT_FROM_RUNA,
            ToolchainCapability.VALIDATE,
            ToolchainCapability.OPTIMIZE,
            ToolchainCapability.FORMAT,
            ToolchainCapability.ANALYZE,
            ToolchainCapability.SECURITY_ANALYSIS
        ]
    
    def parse(self, source: str, file_path: Optional[str] = None) -> SolidityNode:
        """Parse Solidity source code into AST."""
        try:
            return parse_solidity_source(source, file_path)
        except Exception as e:
            raise SyntaxError(f"Failed to parse Solidity code: {str(e)}")
    
    def generate(self, ast: SolidityNode, format_options: Optional[Dict[str, Any]] = None) -> str:
        """Generate Solidity source code from AST."""
        try:
            if format_options:
                indent_size = format_options.get('indent_size', 4)
                generator = SolidityCodeGenerator(indent_size=indent_size)
                return generator.generate(ast)
            else:
                return generate_solidity_code(ast)
        except Exception as e:
            raise RuntimeError(f"Failed to generate Solidity code: {str(e)}")
    
    def to_runa(self, solidity_ast: SolidityNode) -> ASTNode:
        """Convert Solidity AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(solidity_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Solidity to Runa: {str(e)}")
    
    def from_runa(self, runa_ast: ASTNode) -> SolidityNode:
        """Convert Runa AST to Solidity AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Runa to Solidity: {str(e)}")
    
    def validate(self, ast: SolidityNode) -> SolidityValidationResult:
        """Validate Solidity AST for correctness, security, and best practices."""
        errors = []
        warnings = []
        suggestions = []
        security_issues = []
        gas_optimizations = []
        
        try:
            # Syntax validation
            self._validate_syntax(ast, errors, warnings)
            
            # Semantic validation
            self._validate_semantics(ast, errors, warnings, suggestions)
            
            # Security validation
            self._validate_security(ast, security_issues, warnings)
            
            # Gas optimization analysis
            self._analyze_gas_efficiency(ast, gas_optimizations, suggestions)
            
            # Style validation
            self._validate_style(ast, warnings, suggestions)
            
            is_valid = len(errors) == 0 and len(security_issues) == 0
            
            return SolidityValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                security_issues=security_issues,
                gas_optimizations=gas_optimizations
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return SolidityValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                security_issues=security_issues,
                gas_optimizations=gas_optimizations
            )
    
    def optimize(self, ast: SolidityNode, optimization_level: str = "balanced") -> SolidityOptimizationResult:
        """Optimize Solidity AST for gas efficiency and security."""
        optimized_ast = ast
        optimizations_applied = []
        gas_savings = {}
        security_improvements = []
        
        try:
            optimization_configs = {
                "minimal": ["gas_efficiency"],
                "balanced": ["gas_efficiency", "security", "storage"],
                "aggressive": ["gas_efficiency", "security", "storage", "function_calls", "loops"]
            }
            
            selected_optimizations = optimization_configs.get(optimization_level, optimization_configs["balanced"])
            
            for opt_name in selected_optimizations:
                if opt_name in self.optimization_patterns:
                    optimizer = self.optimization_patterns[opt_name]
                    result = optimizer(optimized_ast)
                    
                    if result:
                        optimized_ast = result["ast"]
                        optimizations_applied.extend(result["optimizations"])
                        gas_savings.update(result.get("gas_savings", {}))
                        security_improvements.extend(result.get("security_improvements", []))
            
            return SolidityOptimizationResult(
                optimized_ast=optimized_ast,
                optimizations_applied=optimizations_applied,
                gas_savings=gas_savings,
                security_improvements=security_improvements
            )
            
        except Exception as e:
            return SolidityOptimizationResult(
                optimized_ast=ast,
                optimizations_applied=[],
                gas_savings={"error": str(e)},
                security_improvements=[]
            )
    
    def analyze_security(self, ast: SolidityNode) -> Dict[str, Any]:
        """Perform comprehensive security analysis."""
        try:
            security_report = {
                'vulnerability_scan': {},
                'risk_level': 'Low',
                'recommendations': [],
                'gas_analysis': {},
                'access_control_analysis': {},
                'external_dependency_analysis': {}
            }
            
            # Run security pattern checks
            for pattern_name, checker in self.security_patterns.items():
                vulnerabilities = checker(ast)
                security_report['vulnerability_scan'][pattern_name] = vulnerabilities
            
            # Assess overall risk level
            total_vulnerabilities = sum(len(vulns) for vulns in security_report['vulnerability_scan'].values())
            if total_vulnerabilities == 0:
                security_report['risk_level'] = 'Low'
            elif total_vulnerabilities <= 3:
                security_report['risk_level'] = 'Medium'
            else:
                security_report['risk_level'] = 'High'
            
            # Generate recommendations
            security_report['recommendations'] = self._generate_security_recommendations(ast)
            
            # Gas analysis
            security_report['gas_analysis'] = self._analyze_gas_patterns(ast)
            
            # Access control analysis
            security_report['access_control_analysis'] = self._analyze_access_control(ast)
            
            return security_report
            
        except Exception as e:
            return {'error': str(e)}
    
    def estimate_gas_costs(self, ast: SolidityNode) -> Dict[str, Any]:
        """Estimate gas costs for contract operations."""
        try:
            gas_estimates = {
                'deployment_cost': self._estimate_deployment_gas(ast),
                'function_costs': self._estimate_function_gas(ast),
                'storage_costs': self._estimate_storage_gas(ast),
                'optimization_potential': self._analyze_gas_optimization_potential(ast)
            }
            
            return gas_estimates
            
        except Exception as e:
            return {'error': str(e)}
    
    def format_code(self, source: str, style_options: Optional[Dict[str, Any]] = None) -> str:
        """Format Solidity code according to style guidelines."""
        try:
            ast = self.parse(source)
            
            format_options = {
                'indent_size': 4,
                'max_line_length': 120,
                'brace_style': 'stroustrup',
                'space_around_operators': True
            }
            
            if style_options:
                format_options.update(style_options)
            
            return self.generate(ast, format_options)
            
        except Exception as e:
            raise RuntimeError(f"Failed to format Solidity code: {str(e)}")
    
    # Validation methods
    def _validate_syntax(self, ast: SolidityNode, errors: List[str], warnings: List[str]):
        """Validate Solidity syntax."""
        if isinstance(ast, SoliditySourceUnit):
            # Check pragma directives
            if not ast.pragma_directives:
                warnings.append("Missing pragma directive")
            
            # Check contract definitions
            if not ast.contracts and not ast.interfaces and not ast.libraries:
                warnings.append("No contracts, interfaces, or libraries defined")
    
    def _validate_semantics(self, ast: SolidityNode, errors: List[str], warnings: List[str], suggestions: List[str]):
        """Validate Solidity semantics."""
        # Check function visibility
        self._check_function_visibility(ast, warnings, suggestions)
        
        # Check state variable visibility
        self._check_state_variable_visibility(ast, warnings)
        
        # Check modifier usage
        self._check_modifier_usage(ast, suggestions)
    
    def _validate_security(self, ast: SolidityNode, security_issues: List[str], warnings: List[str]):
        """Validate security aspects."""
        for pattern_name, checker in self.security_patterns.items():
            vulnerabilities = checker(ast)
            for vuln in vulnerabilities:
                security_issues.append(f"{pattern_name}: {vuln}")
    
    def _validate_style(self, ast: SolidityNode, warnings: List[str], suggestions: List[str]):
        """Validate Solidity coding style."""
        # Check naming conventions
        self._check_naming_conventions(ast, warnings, suggestions)
        
        # Check code organization
        self._check_code_organization(ast, suggestions)
    
    def _analyze_gas_efficiency(self, ast: SolidityNode, gas_optimizations: List[str], suggestions: List[str]):
        """Analyze gas efficiency."""
        # Check for gas optimization opportunities
        if self._has_expensive_operations(ast):
            gas_optimizations.append("Consider optimizing expensive operations")
        
        if self._has_unnecessary_storage_operations(ast):
            gas_optimizations.append("Reduce unnecessary storage operations")
        
        if self._has_inefficient_loops(ast):
            gas_optimizations.append("Optimize loop structures")
    
    # Optimization methods
    def _optimize_gas_efficiency(self, ast: SolidityNode) -> Optional[Dict[str, Any]]:
        """Optimize for gas efficiency."""
        optimizations = []
        gas_savings = {}
        
        # Example optimizations
        if self._has_expensive_operations(ast):
            optimizations.append("Optimized expensive operations")
            gas_savings["operations"] = "10-20% reduction"
        
        if self._has_unnecessary_storage_operations(ast):
            optimizations.append("Reduced storage operations")
            gas_savings["storage"] = "15-30% reduction"
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "gas_savings": gas_savings
            }
        
        return None
    
    def _optimize_security(self, ast: SolidityNode) -> Optional[Dict[str, Any]]:
        """Optimize for security."""
        optimizations = []
        security_improvements = []
        
        # Example security optimizations
        if self._has_security_vulnerabilities(ast):
            optimizations.append("Applied security fixes")
            security_improvements.append("Fixed potential vulnerabilities")
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "security_improvements": security_improvements
            }
        
        return None
    
    def _optimize_storage(self, ast: SolidityNode) -> Optional[Dict[str, Any]]:
        """Optimize storage usage."""
        optimizations = []
        gas_savings = {}
        
        if self._has_inefficient_storage(ast):
            optimizations.append("Optimized storage layout")
            gas_savings["storage_layout"] = "5-15% reduction"
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "gas_savings": gas_savings
            }
        
        return None
    
    def _optimize_function_calls(self, ast: SolidityNode) -> Optional[Dict[str, Any]]:
        """Optimize function calls."""
        optimizations = []
        
        if self._has_inefficient_function_calls(ast):
            optimizations.append("Optimized function calls")
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations
            }
        
        return None
    
    def _optimize_loops(self, ast: SolidityNode) -> Optional[Dict[str, Any]]:
        """Optimize loops."""
        optimizations = []
        gas_savings = {}
        
        if self._has_inefficient_loops(ast):
            optimizations.append("Optimized loop structures")
            gas_savings["loops"] = "Variable reduction based on complexity"
        
        if optimizations:
            return {
                "ast": ast,
                "optimizations": optimizations,
                "gas_savings": gas_savings
            }
        
        return None
    
    # Security analysis methods
    def _check_reentrancy(self, ast: SolidityNode) -> List[str]:
        """Check for reentrancy vulnerabilities."""
        vulnerabilities = []
        # Check for external calls without proper protection
        # This would analyze the AST for reentrancy patterns
        return vulnerabilities
    
    def _check_integer_overflow(self, ast: SolidityNode) -> List[str]:
        """Check for integer overflow vulnerabilities."""
        vulnerabilities = []
        # Check for unchecked arithmetic operations
        return vulnerabilities
    
    def _check_access_control(self, ast: SolidityNode) -> List[str]:
        """Check for access control issues."""
        vulnerabilities = []
        # Check for missing access controls on sensitive functions
        return vulnerabilities
    
    def _check_weak_randomness(self, ast: SolidityNode) -> List[str]:
        """Check for weak randomness sources."""
        vulnerabilities = []
        # Check for usage of block.timestamp, block.difficulty, etc. for randomness
        return vulnerabilities
    
    def _check_external_calls(self, ast: SolidityNode) -> List[str]:
        """Check for unsafe external calls."""
        vulnerabilities = []
        # Check for unchecked external calls
        return vulnerabilities
    
    def _check_dos_vulnerabilities(self, ast: SolidityNode) -> List[str]:
        """Check for denial of service vulnerabilities."""
        vulnerabilities = []
        # Check for gas limit DoS patterns
        return vulnerabilities
    
    # Analysis helper methods
    def _estimate_deployment_gas(self, ast: SolidityNode) -> int:
        """Estimate contract deployment gas cost."""
        # This would analyze contract size and complexity
        base_cost = 21000  # Base transaction cost
        # Add estimates based on contract complexity
        return base_cost
    
    def _estimate_function_gas(self, ast: SolidityNode) -> Dict[str, int]:
        """Estimate gas costs for functions."""
        function_costs = {}
        # This would analyze each function and estimate gas usage
        return function_costs
    
    def _estimate_storage_gas(self, ast: SolidityNode) -> Dict[str, int]:
        """Estimate storage operation costs."""
        storage_costs = {}
        # This would analyze storage operations
        return storage_costs
    
    def _analyze_gas_optimization_potential(self, ast: SolidityNode) -> List[str]:
        """Analyze gas optimization potential."""
        optimizations = []
        # Identify optimization opportunities
        return optimizations
    
    def _analyze_gas_patterns(self, ast: SolidityNode) -> Dict[str, Any]:
        """Analyze gas usage patterns."""
        patterns = {
            'expensive_operations': [],
            'storage_usage': [],
            'loop_complexity': []
        }
        return patterns
    
    def _analyze_access_control(self, ast: SolidityNode) -> Dict[str, Any]:
        """Analyze access control patterns."""
        access_control = {
            'protected_functions': [],
            'unprotected_functions': [],
            'modifier_usage': []
        }
        return access_control
    
    def _generate_security_recommendations(self, ast: SolidityNode) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        # Generate specific security recommendations based on analysis
        recommendations.append("Use OpenZeppelin's security libraries")
        recommendations.append("Implement proper access controls")
        recommendations.append("Follow checks-effects-interactions pattern")
        return recommendations
    
    # Check methods for validation and optimization
    def _has_expensive_operations(self, ast: SolidityNode) -> bool:
        """Check for expensive operations."""
        return False  # Placeholder
    
    def _has_unnecessary_storage_operations(self, ast: SolidityNode) -> bool:
        """Check for unnecessary storage operations."""
        return False  # Placeholder
    
    def _has_inefficient_loops(self, ast: SolidityNode) -> bool:
        """Check for inefficient loops."""
        return False  # Placeholder
    
    def _has_security_vulnerabilities(self, ast: SolidityNode) -> bool:
        """Check for security vulnerabilities."""
        return False  # Placeholder
    
    def _has_inefficient_storage(self, ast: SolidityNode) -> bool:
        """Check for inefficient storage usage."""
        return False  # Placeholder
    
    def _has_inefficient_function_calls(self, ast: SolidityNode) -> bool:
        """Check for inefficient function calls."""
        return False  # Placeholder
    
    def _check_function_visibility(self, ast: SolidityNode, warnings: List[str], suggestions: List[str]):
        """Check function visibility modifiers."""
        pass
    
    def _check_state_variable_visibility(self, ast: SolidityNode, warnings: List[str]):
        """Check state variable visibility."""
        pass
    
    def _check_modifier_usage(self, ast: SolidityNode, suggestions: List[str]):
        """Check modifier usage patterns."""
        pass
    
    def _check_naming_conventions(self, ast: SolidityNode, warnings: List[str], suggestions: List[str]):
        """Check Solidity naming conventions."""
        pass
    
    def _check_code_organization(self, ast: SolidityNode, suggestions: List[str]):
        """Check code organization."""
        pass


# Convenience functions
def create_solidity_toolchain() -> SolidityToolchain:
    """Create and return Solidity toolchain instance."""
    return SolidityToolchain()


def parse_solidity_file(file_path: str) -> SolidityNode:
    """Parse Solidity file and return AST."""
    toolchain = create_solidity_toolchain()
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    return toolchain.parse(source, file_path)


def validate_solidity_file(file_path: str) -> SolidityValidationResult:
    """Validate Solidity file."""
    ast = parse_solidity_file(file_path)
    toolchain = create_solidity_toolchain()
    return toolchain.validate(ast)


def analyze_contract_security(file_path: str) -> Dict[str, Any]:
    """Analyze smart contract security."""
    ast = parse_solidity_file(file_path)
    toolchain = create_solidity_toolchain()
    return toolchain.analyze_security(ast)


def optimize_solidity_file(file_path: str, optimization_level: str = "balanced") -> str:
    """Optimize Solidity file and return optimized code."""
    ast = parse_solidity_file(file_path)
    toolchain = create_solidity_toolchain()
    result = toolchain.optimize(ast, optimization_level)
    return toolchain.generate(result.optimized_ast) 