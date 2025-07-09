"""
Runa AST Verification System

This system provides comprehensive AST comparison and debugging capabilities
for the hub-and-spoke translation pipeline. It allows us to compare ASTs at
different stages to pinpoint exactly where translation bugs occur.

Key Features:
- Deep AST comparison with detailed diff reporting
- Translation pipeline verification
- Round-trip testing support
- Detailed error reporting with location tracking
"""

from typing import List, Dict, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum, auto
import json
from datetime import datetime

from .runa_ast import ASTNode, SourceLocation, TranslationMetadata


class DifferenceType(Enum):
    """Types of differences that can be found between ASTs."""
    MISSING_NODE = auto()           # Node exists in one AST but not the other
    EXTRA_NODE = auto()            # Node exists in one AST but not expected
    TYPE_MISMATCH = auto()         # Nodes have different types
    VALUE_MISMATCH = auto()        # Nodes have different values
    STRUCTURE_MISMATCH = auto()    # Different number of children
    METADATA_MISMATCH = auto()     # Different metadata
    LOCATION_MISMATCH = auto()     # Different source locations


@dataclass
class ASTDifference:
    """Represents a single difference between two AST nodes."""
    difference_type: DifferenceType
    path: List[str]  # Path to the node in the AST (e.g., ["program", "statements", "0", "condition"])
    expected_value: Any = None
    actual_value: Any = None
    expected_node_id: Optional[str] = None
    actual_node_id: Optional[str] = None
    message: str = ""
    location: Optional[SourceLocation] = None
    
    def __str__(self) -> str:
        path_str = " -> ".join(self.path) if self.path else "root"
        if self.message:
            return f"{self.difference_type.name} at {path_str}: {self.message}"
        elif self.expected_value is not None and self.actual_value is not None:
            return f"{self.difference_type.name} at {path_str}: expected {self.expected_value}, got {self.actual_value}"
        else:
            return f"{self.difference_type.name} at {path_str}"


@dataclass
class VerificationResult:
    """Result of AST verification/comparison."""
    is_identical: bool
    differences: List[ASTDifference]
    comparison_time: datetime = field(default_factory=datetime.now)
    nodes_compared: int = 0
    total_time_ms: float = 0.0
    
    def __str__(self) -> str:
        if self.is_identical:
            return f"ASTs are identical ({self.nodes_compared} nodes compared in {self.total_time_ms:.2f}ms)"
        else:
            return f"ASTs differ: {len(self.differences)} differences found ({self.nodes_compared} nodes compared)"
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the verification result."""
        return {
            "is_identical": self.is_identical,
            "difference_count": len(self.differences),
            "nodes_compared": self.nodes_compared,
            "total_time_ms": self.total_time_ms,
            "difference_types": [diff.difference_type.name for diff in self.differences]
        }


class ASTComparator:
    """Deep AST comparison with detailed difference reporting."""
    
    def __init__(self, ignore_metadata: bool = False, ignore_locations: bool = False, 
                 ignore_node_ids: bool = True):
        """
        Initialize the comparator.
        
        Args:
            ignore_metadata: If True, don't compare translation metadata
            ignore_locations: If True, don't compare source locations
            ignore_node_ids: If True, don't compare node IDs (usually desirable)
        """
        self.ignore_metadata = ignore_metadata
        self.ignore_locations = ignore_locations
        self.ignore_node_ids = ignore_node_ids
        self.differences: List[ASTDifference] = []
        self.nodes_compared = 0
    
    def compare(self, expected: ASTNode, actual: ASTNode) -> VerificationResult:
        """
        Compare two AST nodes and return detailed results.
        
        Args:
            expected: The expected AST node
            actual: The actual AST node
            
        Returns:
            VerificationResult with detailed comparison information
        """
        start_time = datetime.now()
        self.differences.clear()
        self.nodes_compared = 0
        
        self._compare_nodes(expected, actual, [])
        
        end_time = datetime.now()
        total_time_ms = (end_time - start_time).total_seconds() * 1000
        
        return VerificationResult(
            is_identical=len(self.differences) == 0,
            differences=self.differences.copy(),
            comparison_time=start_time,
            nodes_compared=self.nodes_compared,
            total_time_ms=total_time_ms
        )
    
    def _compare_nodes(self, expected: ASTNode, actual: ASTNode, path: List[str]) -> None:
        """Recursively compare two AST nodes."""
        self.nodes_compared += 1
        
        # Compare node types
        if type(expected) != type(actual):
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.TYPE_MISMATCH,
                path=path.copy(),
                expected_value=type(expected).__name__,
                actual_value=type(actual).__name__,
                message=f"Expected {type(expected).__name__}, got {type(actual).__name__}"
            ))
            return  # Can't continue comparison if types are different
        
        # Compare node IDs if not ignoring them
        if not self.ignore_node_ids and expected.node_id != actual.node_id:
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.VALUE_MISMATCH,
                path=path + ["node_id"],
                expected_value=expected.node_id,
                actual_value=actual.node_id,
                message="Node IDs differ"
            ))
        
        # Compare source locations if not ignoring them
        if not self.ignore_locations and expected.location != actual.location:
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.LOCATION_MISMATCH,
                path=path + ["location"],
                expected_value=str(expected.location),
                actual_value=str(actual.location),
                message="Source locations differ"
            ))
        
        # Compare metadata if not ignoring it
        if not self.ignore_metadata:
            self._compare_metadata(expected.metadata, actual.metadata, path + ["metadata"])
        
        # Compare node-specific attributes
        self._compare_node_attributes(expected, actual, path)
        
        # Compare children
        expected_children = expected.get_children()
        actual_children = actual.get_children()
        
        if len(expected_children) != len(actual_children):
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.STRUCTURE_MISMATCH,
                path=path + ["children"],
                expected_value=len(expected_children),
                actual_value=len(actual_children),
                message=f"Different number of children: expected {len(expected_children)}, got {len(actual_children)}"
            ))
        
        # Compare each child
        for i, (exp_child, act_child) in enumerate(zip(expected_children, actual_children)):
            self._compare_nodes(exp_child, act_child, path + ["children", str(i)])
    
    def _compare_metadata(self, expected: TranslationMetadata, actual: TranslationMetadata, path: List[str]) -> None:
        """Compare translation metadata."""
        if expected.source_language != actual.source_language:
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.METADATA_MISMATCH,
                path=path + ["source_language"],
                expected_value=expected.source_language,
                actual_value=actual.source_language
            ))
        
        if expected.target_language != actual.target_language:
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.METADATA_MISMATCH,
                path=path + ["target_language"],
                expected_value=expected.target_language,
                actual_value=actual.target_language
            ))
        
        if expected.confidence_score != actual.confidence_score:
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.METADATA_MISMATCH,
                path=path + ["confidence_score"],
                expected_value=expected.confidence_score,
                actual_value=actual.confidence_score
            ))
    
    def _compare_node_attributes(self, expected: ASTNode, actual: ASTNode, path: List[str]) -> None:
        """Compare node-specific attributes (not including universal ones)."""
        # Get all attributes except the universal ones we handle separately
        universal_attrs = {'node_id', 'location', 'metadata', 'parent', '_children'}
        
        expected_attrs = {k: v for k, v in expected.__dict__.items() if k not in universal_attrs}
        actual_attrs = {k: v for k, v in actual.__dict__.items() if k not in universal_attrs}
        
        # Compare each attribute
        all_attr_names = set(expected_attrs.keys()) | set(actual_attrs.keys())
        
        for attr_name in all_attr_names:
            if attr_name not in expected_attrs:
                self.differences.append(ASTDifference(
                    difference_type=DifferenceType.EXTRA_NODE,
                    path=path + [attr_name],
                    actual_value=actual_attrs[attr_name],
                    message=f"Unexpected attribute '{attr_name}'"
                ))
            elif attr_name not in actual_attrs:
                self.differences.append(ASTDifference(
                    difference_type=DifferenceType.MISSING_NODE,
                    path=path + [attr_name],
                    expected_value=expected_attrs[attr_name],
                    message=f"Missing attribute '{attr_name}'"
                ))
            elif expected_attrs[attr_name] != actual_attrs[attr_name]:
                # Handle list comparisons specially
                if isinstance(expected_attrs[attr_name], list) and isinstance(actual_attrs[attr_name], list):
                    self._compare_lists(expected_attrs[attr_name], actual_attrs[attr_name], path + [attr_name])
                else:
                    self.differences.append(ASTDifference(
                        difference_type=DifferenceType.VALUE_MISMATCH,
                        path=path + [attr_name],
                        expected_value=expected_attrs[attr_name],
                        actual_value=actual_attrs[attr_name]
                    ))
    
    def _compare_lists(self, expected: List[Any], actual: List[Any], path: List[str]) -> None:
        """Compare two lists, handling AST nodes specially."""
        if len(expected) != len(actual):
            self.differences.append(ASTDifference(
                difference_type=DifferenceType.STRUCTURE_MISMATCH,
                path=path,
                expected_value=len(expected),
                actual_value=len(actual),
                message=f"List length mismatch: expected {len(expected)}, got {len(actual)}"
            ))
        
        for i, (exp_item, act_item) in enumerate(zip(expected, actual)):
            if isinstance(exp_item, ASTNode) and isinstance(act_item, ASTNode):
                self._compare_nodes(exp_item, act_item, path + [str(i)])
            elif exp_item != act_item:
                self.differences.append(ASTDifference(
                    difference_type=DifferenceType.VALUE_MISMATCH,
                    path=path + [str(i)],
                    expected_value=exp_item,
                    actual_value=act_item
                ))


class PipelineVerifier:
    """Verifies the entire translation pipeline for correctness."""
    
    def __init__(self):
        self.comparator = ASTComparator(ignore_node_ids=True)
    
    def verify_round_trip(self, original_ast: ASTNode, round_trip_ast: ASTNode) -> VerificationResult:
        """
        Verify that a round-trip translation preserves the AST structure.
        
        This is critical for ensuring translation accuracy. The workflow is:
        Runa_AST_1 -> Target_Language -> Runa_AST_2
        
        Runa_AST_1 and Runa_AST_2 should be identical (or semantically equivalent).
        """
        return self.comparator.compare(original_ast, round_trip_ast)
    
    def verify_translation_chain(self, checkpoints: List[Tuple[str, ASTNode]]) -> Dict[str, VerificationResult]:
        """
        Verify a complete translation chain with multiple checkpoints.
        
        Args:
            checkpoints: List of (stage_name, ast) tuples representing pipeline stages
            
        Returns:
            Dictionary mapping stage transitions to verification results
        """
        results = {}
        
        for i in range(len(checkpoints) - 1):
            stage1_name, stage1_ast = checkpoints[i]
            stage2_name, stage2_ast = checkpoints[i + 1]
            
            transition_name = f"{stage1_name} -> {stage2_name}"
            
            # For round-trip verification, we expect ASTs to be identical
            # For forward translation, we might have different comparison strategies
            if "round_trip" in transition_name.lower():
                result = self.verify_round_trip(stage1_ast, stage2_ast)
            else:
                # For now, use standard comparison for all transitions
                result = self.comparator.compare(stage1_ast, stage2_ast)
            
            results[transition_name] = result
        
        return results


class VerificationReporter:
    """Generates detailed reports from verification results."""
    
    @staticmethod
    def generate_text_report(result: VerificationResult) -> str:
        """Generate a human-readable text report."""
        lines = [
            f"AST Verification Report",
            f"======================",
            f"",
            f"Overall Result: {'PASS' if result.is_identical else 'FAIL'}",
            f"Nodes Compared: {result.nodes_compared}",
            f"Comparison Time: {result.total_time_ms:.2f}ms",
            f"Differences Found: {len(result.differences)}",
            f"",
        ]
        
        if result.differences:
            lines.append("Differences:")
            lines.append("-----------")
            for i, diff in enumerate(result.differences, 1):
                lines.append(f"{i}. {diff}")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_json_report(result: VerificationResult) -> str:
        """Generate a machine-readable JSON report."""
        report_data = {
            "summary": result.get_summary(),
            "differences": [
                {
                    "type": diff.difference_type.name,
                    "path": diff.path,
                    "expected": str(diff.expected_value) if diff.expected_value is not None else None,
                    "actual": str(diff.actual_value) if diff.actual_value is not None else None,
                    "message": diff.message,
                    "location": str(diff.location) if diff.location else None
                }
                for diff in result.differences
            ]
        }
        
        return json.dumps(report_data, indent=2, default=str)
    
    @staticmethod
    def save_report(result: VerificationResult, file_path: str, format: str = "text") -> None:
        """Save verification report to file."""
        if format.lower() == "json":
            content = VerificationReporter.generate_json_report(result)
        else:
            content = VerificationReporter.generate_text_report(result)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


# Convenience functions for common verification tasks
def compare_asts(expected: ASTNode, actual: ASTNode, 
                ignore_metadata: bool = True, ignore_locations: bool = True) -> VerificationResult:
    """Quick AST comparison with sensible defaults."""
    comparator = ASTComparator(
        ignore_metadata=ignore_metadata, 
        ignore_locations=ignore_locations,
        ignore_node_ids=True
    )
    return comparator.compare(expected, actual)


def verify_round_trip(original: ASTNode, round_trip: ASTNode) -> VerificationResult:
    """Quick round-trip verification."""
    verifier = PipelineVerifier()
    return verifier.verify_round_trip(original, round_trip)


def print_verification_report(result: VerificationResult) -> None:
    """Print a verification report to console."""
    print(VerificationReporter.generate_text_report(result))