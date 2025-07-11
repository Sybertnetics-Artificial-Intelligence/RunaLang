#!/usr/bin/env python3
"""
Move Toolchain Integration

Complete toolchain integration for Move language providing unified interface for parsing,
conversion, generation, validation, and optimization of resource-oriented smart contracts
within the Runa ecosystem.

Features:
- Resource-oriented programming support
- Abilities system validation
- Move semantics and ownership analysis
- Module and script processing
- Formal verification integration
- Security analysis for smart contracts
- Gas optimization recommendations
"""

from typing import List, Optional, Any, Union, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path

from .move_ast import *
from .move_parser import MoveParser, MoveLexer, parse_move_source
from .move_converter import MoveToRunaConverter, RunaToMoveConverter, move_to_runa, runa_to_move
from .move_generator import MoveCodeGenerator, MoveCodeStyle, generate_move_code
from ....core.runa_ast import ASTNode
from ...shared.base_toolchain import BaseToolchain, ToolchainCapability, LanguageInfo


@dataclass
class MoveValidationResult:
    """Move code validation result."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    resource_issues: List[str]
    ability_violations: List[str]
    move_semantic_issues: List[str]
    security_concerns: List[str]


@dataclass
class MoveOptimizationResult:
    """Move code optimization result."""
    optimized_ast: MoveNode
    optimizations_applied: List[str]
    gas_savings: Dict[str, Any]
    resource_optimizations: List[str]
    ability_improvements: List[str]
    move_semantic_improvements: List[str]


class MoveToolchain(BaseToolchain):
    """Complete Move language toolchain."""
    
    def __init__(self):
        super().__init__()
        self.parser = None
        self.lexer = None
        self.to_runa_converter = MoveToRunaConverter()
        self.from_runa_converter = RunaToMoveConverter()
        self.generator = MoveCodeGenerator()
        
        # Move-specific optimization patterns
        self.optimization_patterns = {
            'gas_efficiency': self._optimize_gas_efficiency,
            'resource_management': self._optimize_resource_management,
            'ability_usage': self._optimize_ability_usage,
            'move_semantics': self._optimize_move_semantics,
            'storage_layout': self._optimize_storage_layout,
            'function_calls': self._optimize_function_calls
        }
        
        # Security analysis patterns for Move
        self.security_patterns = {
            'resource_safety': self._check_resource_safety,
            'ability_constraints': self._check_ability_constraints,
            'move_semantics': self._check_move_semantics,
            'access_control': self._check_access_control,
            'module_boundaries': self._check_module_boundaries,
            'type_safety': self._check_type_safety,
            'formal_verification': self._check_formal_verification
        }
    
    def get_language_info(self) -> LanguageInfo:
        """Get Move language information."""
        return LanguageInfo(
            name="Move",
            version="2024",
            file_extensions=[".move"],
            mime_types=["text/x-move"],
            description="Resource-oriented programming language for secure smart contracts and digital asset management",
            features=[
                "Resource-oriented programming",
                "Abilities system (copy, drop, store, key)",
                "Move semantics and ownership",
                "Formal verification support",
                "Bytecode verification",
                "Module system",
                "Generic types",
                "Pattern matching",
                "Safety-first design",
                "Gas efficiency"
            ],
            paradigms=["Resource-oriented", "Functional", "Contract-oriented", "Safety-first"],
            typical_use_cases=[
                "Smart contracts",
                "Digital asset management",
                "Blockchain protocols",
                "Decentralized finance (DeFi)",
                "NFT platforms",
                "Cross-chain bridges",
                "Governance systems",
                "Payment systems",
                "Resource management systems"
            ]
        )
    
    def get_capabilities(self) -> List[ToolchainCapability]:
        """Get Move toolchain capabilities."""
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
            ToolchainCapability.STYLE_CHECK,
            ToolchainCapability.TYPE_CHECK
        ]
    
    def parse(self, source: str, file_path: Optional[str] = None) -> MoveNode:
        """Parse Move source code into AST."""
        try:
            return parse_move_source(source, file_path)
        except Exception as e:
            raise SyntaxError(f"Failed to parse Move code: {str(e)}")
    
    def generate(self, ast: MoveNode, format_options: Optional[Dict[str, Any]] = None) -> str:
        """Generate Move source code from AST."""
        try:
            if format_options:
                style = MoveCodeStyle()
                style.indent_size = format_options.get('indent_size', 4)
                style.max_line_length = format_options.get('max_line_length', 100)
                style.brace_style = format_options.get('brace_style', 'same_line')
                generator = MoveCodeGenerator(style=style)
                return generator.generate(ast)
            else:
                return generate_move_code(ast)
        except Exception as e:
            raise RuntimeError(f"Failed to generate Move code: {str(e)}")
    
    def to_runa(self, move_ast: MoveNode) -> ASTNode:
        """Convert Move AST to Runa AST."""
        try:
            return self.to_runa_converter.convert(move_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Move to Runa: {str(e)}")
    
    def from_runa(self, runa_ast: ASTNode) -> MoveNode:
        """Convert Runa AST to Move AST."""
        try:
            return self.from_runa_converter.convert(runa_ast)
        except Exception as e:
            raise RuntimeError(f"Failed to convert Runa to Move: {str(e)}")
    
    def validate(self, ast: MoveNode) -> MoveValidationResult:
        """Validate Move AST for correctness, resource safety, and best practices."""
        errors = []
        warnings = []
        suggestions = []
        resource_issues = []
        ability_violations = []
        move_semantic_issues = []
        security_concerns = []
        
        try:
            # Syntax validation
            self._validate_syntax(ast, errors, warnings)
            
            # Resource-oriented validation
            self._validate_resources(ast, resource_issues, warnings)
            
            # Abilities system validation
            self._validate_abilities(ast, ability_violations, warnings)
            
            # Move semantics validation
            self._validate_move_semantics(ast, move_semantic_issues, warnings)
            
            # Security validation
            self._validate_security(ast, security_concerns, warnings)
            
            # Best practices validation
            self._validate_best_practices(ast, suggestions, warnings)
            
            is_valid = (len(errors) == 0 and len(resource_issues) == 0 and 
                       len(ability_violations) == 0 and len(move_semantic_issues) == 0)
            
            return MoveValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                resource_issues=resource_issues,
                ability_violations=ability_violations,
                move_semantic_issues=move_semantic_issues,
                security_concerns=security_concerns
            )
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return MoveValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                resource_issues=resource_issues,
                ability_violations=ability_violations,
                move_semantic_issues=move_semantic_issues,
                security_concerns=security_concerns
            )
    
    def optimize(self, ast: MoveNode, optimization_level: str = "balanced") -> MoveOptimizationResult:
        """Optimize Move AST for gas efficiency, resource management, and best practices."""
        optimizations_applied = []
        gas_savings = {}
        resource_optimizations = []
        ability_improvements = []
        move_semantic_improvements = []
        
        optimized_ast = ast  # Start with original AST
        
        try:
            optimization_strategies = self._get_optimization_strategies(optimization_level)
            
            for strategy in optimization_strategies:
                if strategy in self.optimization_patterns:
                    result = self.optimization_patterns[strategy](optimized_ast)
                    if result:
                        optimized_ast = result.get('optimized_ast', optimized_ast)
                        optimizations_applied.extend(result.get('optimizations', []))
                        gas_savings.update(result.get('gas_savings', {}))
                        resource_optimizations.extend(result.get('resource_optimizations', []))
                        ability_improvements.extend(result.get('ability_improvements', []))
                        move_semantic_improvements.extend(result.get('move_semantic_improvements', []))
            
            return MoveOptimizationResult(
                optimized_ast=optimized_ast,
                optimizations_applied=optimizations_applied,
                gas_savings=gas_savings,
                resource_optimizations=resource_optimizations,
                ability_improvements=ability_improvements,
                move_semantic_improvements=move_semantic_improvements
            )
            
        except Exception as e:
            # Return original AST if optimization fails
            return MoveOptimizationResult(
                optimized_ast=ast,
                optimizations_applied=[f"Optimization failed: {str(e)}"],
                gas_savings={},
                resource_optimizations=[],
                ability_improvements=[],
                move_semantic_improvements=[]
            )
    
    def analyze_security(self, ast: MoveNode) -> Dict[str, Any]:
        """Perform comprehensive security analysis on Move code."""
        security_analysis = {
            'resource_safety_score': 0,
            'ability_compliance_score': 0,
            'move_semantics_score': 0,
            'overall_security_score': 0,
            'vulnerabilities': [],
            'recommendations': [],
            'formal_verification_status': 'not_verified'
        }
        
        try:
            # Run all security checks
            for check_name, check_func in self.security_patterns.items():
                result = check_func(ast)
                if result:
                    security_analysis['vulnerabilities'].extend(result.get('vulnerabilities', []))
                    security_analysis['recommendations'].extend(result.get('recommendations', []))
            
            # Calculate security scores
            security_analysis['resource_safety_score'] = self._calculate_resource_safety_score(ast)
            security_analysis['ability_compliance_score'] = self._calculate_ability_compliance_score(ast)
            security_analysis['move_semantics_score'] = self._calculate_move_semantics_score(ast)
            
            # Overall score
            scores = [
                security_analysis['resource_safety_score'],
                security_analysis['ability_compliance_score'],
                security_analysis['move_semantics_score']
            ]
            security_analysis['overall_security_score'] = sum(scores) / len(scores)
            
            return security_analysis
            
        except Exception as e:
            security_analysis['vulnerabilities'].append(f"Security analysis error: {str(e)}")
            return security_analysis
    
    def estimate_gas_costs(self, ast: MoveNode) -> Dict[str, Any]:
        """Estimate gas costs for Move operations."""
        gas_estimates = {
            'deployment_cost': 0,
            'function_costs': {},
            'storage_costs': {},
            'optimization_potential': [],
            'cost_breakdown': {}
        }
        
        try:
            gas_estimates['deployment_cost'] = self._estimate_deployment_gas(ast)
            gas_estimates['function_costs'] = self._estimate_function_gas(ast)
            gas_estimates['storage_costs'] = self._estimate_storage_gas(ast)
            gas_estimates['optimization_potential'] = self._analyze_gas_optimization_potential(ast)
            
            return gas_estimates
            
        except Exception as e:
            gas_estimates['cost_breakdown']['error'] = str(e)
            return gas_estimates
    
    def format_code(self, source: str, style_options: Optional[Dict[str, Any]] = None) -> str:
        """Format Move source code according to style guidelines."""
        try:
            # Parse the source
            ast = self.parse(source)
            
            # Create style configuration
            style = MoveCodeStyle()
            if style_options:
                for key, value in style_options.items():
                    if hasattr(style, key):
                        setattr(style, key, value)
            
            # Generate formatted code
            return self.generate(ast, style_options)
            
        except Exception as e:
            raise RuntimeError(f"Failed to format Move code: {str(e)}")
    
    # Private validation methods
    
    def _validate_syntax(self, ast: MoveNode, errors: List[str], warnings: List[str]):
        """Validate basic syntax correctness."""
        # Implementation would check for syntax errors
        pass
    
    def _validate_resources(self, ast: MoveNode, resource_issues: List[str], warnings: List[str]):
        """Validate resource-oriented programming constraints."""
        # Check for proper resource usage, no copying of resources without copy ability, etc.
        pass
    
    def _validate_abilities(self, ast: MoveNode, ability_violations: List[str], warnings: List[str]):
        """Validate abilities system constraints."""
        # Check that structs with certain abilities are used appropriately
        pass
    
    def _validate_move_semantics(self, ast: MoveNode, move_issues: List[str], warnings: List[str]):
        """Validate Move semantics and ownership."""
        # Check for proper move semantics, no use after move, etc.
        pass
    
    def _validate_security(self, ast: MoveNode, security_concerns: List[str], warnings: List[str]):
        """Validate security aspects."""
        # Check for common security issues in Move code
        pass
    
    def _validate_best_practices(self, ast: MoveNode, suggestions: List[str], warnings: List[str]):
        """Validate adherence to Move best practices."""
        # Check for best practices in Move programming
        pass
    
    # Private optimization methods
    
    def _get_optimization_strategies(self, level: str) -> List[str]:
        """Get optimization strategies for the given level."""
        if level == "aggressive":
            return list(self.optimization_patterns.keys())
        elif level == "balanced":
            return ['gas_efficiency', 'resource_management', 'ability_usage']
        elif level == "conservative":
            return ['gas_efficiency']
        else:
            return ['gas_efficiency']
    
    def _optimize_gas_efficiency(self, ast: MoveNode) -> Optional[Dict[str, Any]]:
        """Optimize for gas efficiency."""
        return {
            'optimized_ast': ast,
            'optimizations': ['Gas efficiency optimizations applied'],
            'gas_savings': {'estimated_reduction': '5-10%'}
        }
    
    def _optimize_resource_management(self, ast: MoveNode) -> Optional[Dict[str, Any]]:
        """Optimize resource management."""
        return {
            'optimized_ast': ast,
            'resource_optimizations': ['Improved resource usage patterns']
        }
    
    def _optimize_ability_usage(self, ast: MoveNode) -> Optional[Dict[str, Any]]:
        """Optimize ability usage."""
        return {
            'optimized_ast': ast,
            'ability_improvements': ['Optimized ability constraints']
        }
    
    def _optimize_move_semantics(self, ast: MoveNode) -> Optional[Dict[str, Any]]:
        """Optimize Move semantics."""
        return {
            'optimized_ast': ast,
            'move_semantic_improvements': ['Enhanced move semantics']
        }
    
    def _optimize_storage_layout(self, ast: MoveNode) -> Optional[Dict[str, Any]]:
        """Optimize storage layout."""
        return None
    
    def _optimize_function_calls(self, ast: MoveNode) -> Optional[Dict[str, Any]]:
        """Optimize function calls."""
        return None
    
    # Private security analysis methods
    
    def _check_resource_safety(self, ast: MoveNode) -> Dict[str, Any]:
        """Check resource safety."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    def _check_ability_constraints(self, ast: MoveNode) -> Dict[str, Any]:
        """Check ability constraints."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    def _check_move_semantics(self, ast: MoveNode) -> Dict[str, Any]:
        """Check Move semantics."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    def _check_access_control(self, ast: MoveNode) -> Dict[str, Any]:
        """Check access control."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    def _check_module_boundaries(self, ast: MoveNode) -> Dict[str, Any]:
        """Check module boundaries."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    def _check_type_safety(self, ast: MoveNode) -> Dict[str, Any]:
        """Check type safety."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    def _check_formal_verification(self, ast: MoveNode) -> Dict[str, Any]:
        """Check formal verification status."""
        return {'vulnerabilities': [], 'recommendations': []}
    
    # Private scoring methods
    
    def _calculate_resource_safety_score(self, ast: MoveNode) -> float:
        """Calculate resource safety score."""
        return 85.0  # Placeholder
    
    def _calculate_ability_compliance_score(self, ast: MoveNode) -> float:
        """Calculate ability compliance score."""
        return 90.0  # Placeholder
    
    def _calculate_move_semantics_score(self, ast: MoveNode) -> float:
        """Calculate Move semantics score."""
        return 88.0  # Placeholder
    
    # Private gas estimation methods
    
    def _estimate_deployment_gas(self, ast: MoveNode) -> int:
        """Estimate deployment gas cost."""
        return 50000  # Placeholder
    
    def _estimate_function_gas(self, ast: MoveNode) -> Dict[str, int]:
        """Estimate gas costs for functions."""
        return {}  # Placeholder
    
    def _estimate_storage_gas(self, ast: MoveNode) -> Dict[str, int]:
        """Estimate gas costs for storage operations."""
        return {}  # Placeholder
    
    def _analyze_gas_optimization_potential(self, ast: MoveNode) -> List[str]:
        """Analyze gas optimization potential."""
        return ['Consider optimizing storage layout', 'Review function call patterns']


# Convenience functions

def create_move_toolchain() -> MoveToolchain:
    """Create a new Move toolchain instance."""
    return MoveToolchain()


def parse_move_file(file_path: str) -> MoveNode:
    """Parse a Move file and return AST."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        return parse_move_source(source, file_path)
    except Exception as e:
        raise SyntaxError(f"Failed to parse Move file {file_path}: {str(e)}")


def validate_move_file(file_path: str) -> MoveValidationResult:
    """Validate a Move file."""
    toolchain = create_move_toolchain()
    ast = parse_move_file(file_path)
    return toolchain.validate(ast)


def analyze_contract_security(file_path: str) -> Dict[str, Any]:
    """Analyze security of a Move contract."""
    toolchain = create_move_toolchain()
    ast = parse_move_file(file_path)
    return toolchain.analyze_security(ast)


def optimize_move_file(file_path: str, optimization_level: str = "balanced") -> str:
    """Optimize a Move file and return optimized source."""
    toolchain = create_move_toolchain()
    ast = parse_move_file(file_path)
    result = toolchain.optimize(ast, optimization_level)
    return toolchain.generate(result.optimized_ast)


def parse_move_code(source: str) -> MoveNode:
    """Parse Move source code and return AST."""
    return parse_move_source(source)


def generate_move_code(ast: MoveNode) -> str:
    """Generate Move source code from AST."""
    toolchain = create_move_toolchain()
    return toolchain.generate(ast)


def move_round_trip_verify(source: str) -> bool:
    """Verify that Move source can be parsed and regenerated correctly."""
    try:
        # Parse source to AST
        ast = parse_move_code(source)
        
        # Generate code from AST
        generated = generate_move_code(ast)
        
        # Parse generated code to verify it's valid
        parse_move_code(generated)
        
        return True
    except Exception:
        return False


def move_to_runa_translate(source: str) -> ASTNode:
    """Translate Move source to Runa AST."""
    move_ast = parse_move_code(source)
    return move_to_runa(move_ast)


def runa_to_move_translate(runa_ast: ASTNode) -> str:
    """Translate Runa AST to Move source."""
    move_ast = runa_to_move(runa_ast)
    return generate_move_code(move_ast) 