"""
Runa Type Inference Engine - Natural Language Expression Parser
==============================================================

Infers types from Runa's natural language expressions:
- "width multiplied by height" -> Integer
- "user name followed by \" Smith\"" -> String  
- "length of colors" -> Integer
- "colors at index 0" -> String
- "the sum of all numbers in list" -> Integer
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
import logging
import re
from .type_system import RunaType, RunaTypeSystem, RunaBasicType, RunaCollectionType, RunaFunctionType

logger = logging.getLogger(__name__)


@dataclass
class RunaTypeInferenceContext:
    """Context for Runa type inference operations."""
    variables: Dict[str, RunaType] = field(default_factory=dict)
    functions: Dict[str, RunaFunctionType] = field(default_factory=dict)
    expected_types: Dict[str, RunaType] = field(default_factory=dict)
    inference_cache: Dict[str, RunaType] = field(default_factory=dict)
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.expected_types = {}
        self.inference_cache = {}


@dataclass
class RunaTypeInferenceResult:
    """Result of Runa type inference operation."""
    inferred_type: RunaType
    confidence: float  # 0.0 to 1.0
    alternatives: List[RunaType] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    runa_expression: str = ""  # Original Runa expression
    
    def __init__(self, inferred_type: RunaType, confidence: float, runa_expression: str,
                 alternatives: Optional[List[RunaType]] = None,
                 suggestions: Optional[List[str]] = None):
        self.inferred_type = inferred_type
        self.confidence = confidence
        self.runa_expression = runa_expression
        self.alternatives = alternatives or []
        self.suggestions = suggestions or []


class RunaTypeInferenceEngine:
    """
    Type inference engine for Runa's natural language expressions.
    
    Handles Runa syntax like:
    - "width multiplied by height" -> Integer
    - "user name followed by \" Smith\"" -> String
    - "length of colors" -> Integer
    - "colors at index 0" -> String
    - "the sum of all numbers in list" -> Integer
    """
    
    def __init__(self, type_system: RunaTypeSystem):
        self.type_system = type_system
        self.inference_patterns: Dict[str, Any] = {}
        
        # Initialize inference patterns for Runa syntax
        self._initialize_runa_inference_patterns()
    
    def _initialize_runa_inference_patterns(self):
        """Initialize patterns for Runa type inference."""
        self.inference_patterns = {
            # Literal patterns
            "integer_literal": r'^-?\d+$',
            "float_literal": r'^-?\d+\.\d+$',
            "boolean_literal": r'^(true|false)$',
            "string_literal": r'^".*"$',
            "list_literal": r'^list\s+containing\s+',
            "dictionary_literal": r'^dictionary\s+with\s*:',
            
            # Runa arithmetic operations
            "runa_arithmetic": r'(\w+)\s+(?:multiplied\s+by|plus|minus|divided\s+by)\s+(\w+)',
            "runa_comparison": r'(\w+)\s+(?:is\s+greater\s+than|is\s+less\s+than|is\s+equal\s+to|is\s+not\s+equal\s+to)\s+(\w+)',
            "runa_logical": r'(\w+)\s+(?:and|or)\s+(\w+)',
            
            # Runa string operations
            "runa_string_concat": r'(\w+)\s+followed\s+by\s+(\w+)',
            
            # Runa collection operations
            "runa_length": r'length\s+of\s+(\w+)',
            "runa_index_access": r'(\w+)\s+at\s+index\s+(\w+)',
            "runa_sum": r'the\s+sum\s+of\s+all\s+(\w+)\s+in\s+(\w+)',
            
            # Runa function calls
            "runa_function_call": r'(\w+)\s+with\s+(.+)',
            "runa_process_call": r'(\w+)\s+with\s+(\w+)\s+as\s+(\w+)',
            
            # Runa assignments
            "runa_assignment": r'Set\s+(\w+)\s+to\s+(.+)',
            "runa_declaration": r'Let\s+(\w+)\s+(?:\(([^)]+)\))?\s+be\s+(.+)',
        }
    
    def infer_type_from_runa_expression(self, runa_expression: str, 
                                       context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """
        Infer type from Runa natural language expression.
        
        Args:
            runa_expression: The Runa expression to infer type for
            context: Type inference context
            
        Returns:
            RunaTypeInferenceResult with inferred type and confidence
        """
        # Check cache first
        if runa_expression in context.inference_cache:
            cached_type = context.inference_cache[runa_expression]
            return RunaTypeInferenceResult(cached_type, 1.0, runa_expression)
        
        # Try different inference strategies
        strategies = [
            self._infer_from_runa_literal,
            self._infer_from_runa_arithmetic,
            self._infer_from_runa_string_operations,
            self._infer_from_runa_collection_operations,
            self._infer_from_runa_function_call,
            self._infer_from_runa_variable,
            self._infer_from_runa_context
        ]
        
        best_result = None
        best_confidence = 0.0
        
        for strategy in strategies:
            try:
                result = strategy(runa_expression, context)
                if result.confidence > best_confidence:
                    best_result = result
                    best_confidence = result.confidence
            except Exception as e:
                logger.debug(f"Strategy {strategy.__name__} failed: {e}")
                continue
        
        if best_result is None:
            # Default to unknown type
            best_result = RunaTypeInferenceResult(
                RunaType("Unknown", "custom", runa_expression),
                0.0,
                runa_expression,
                suggestions=["Consider adding explicit type annotation"]
            )
        
        # Cache the result
        context.inference_cache[runa_expression] = best_result.inferred_type
        
        return best_result
    
    def _infer_from_runa_literal(self, runa_expression: str, 
                                context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa literal values."""
        runa_expression = runa_expression.strip()
        
        # Integer literal
        if re.match(self.inference_patterns["integer_literal"], runa_expression):
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Integer"],
                1.0,
                runa_expression
            )
        
        # Float literal
        if re.match(self.inference_patterns["float_literal"], runa_expression):
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Float"],
                1.0,
                runa_expression
            )
        
        # Boolean literal
        if re.match(self.inference_patterns["boolean_literal"], runa_expression, re.IGNORECASE):
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Boolean"],
                1.0,
                runa_expression
            )
        
        # String literal
        if re.match(self.inference_patterns["string_literal"], runa_expression):
            return RunaTypeInferenceResult(
                self.type_system.basic_types["String"],
                1.0,
                runa_expression
            )
        
        # List literal: "list containing item1, item2, item3"
        if re.match(self.inference_patterns["list_literal"], runa_expression, re.IGNORECASE):
            # Try to infer element type from first element
            match = re.match(r'list\s+containing\s+(.+)', runa_expression, re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                if content:
                    elements = [elem.strip() for elem in content.split(',')]
                    if elements:
                        first_element_result = self.infer_type_from_runa_expression(elements[0], context)
                        element_type = first_element_result.inferred_type
                        return RunaTypeInferenceResult(
                            RunaCollectionType("List", element_type, f"List of {element_type.name}"),
                            0.8,
                            runa_expression
                        )
            
            # Default to list of unknown type
            return RunaTypeInferenceResult(
                RunaCollectionType("List", RunaType("Unknown", "custom", "Unknown"), "List of Unknown"),
                0.5,
                runa_expression
            )
        
        # Dictionary literal: "dictionary with: key1 as value1 key2 as value2"
        if re.match(self.inference_patterns["dictionary_literal"], runa_expression, re.IGNORECASE):
            # Default to dictionary with unknown key and value types
            unknown_type = RunaType("Unknown", "custom", "Unknown")
            return RunaTypeInferenceResult(
                RunaCollectionType("Dictionary", unknown_type, "Dictionary of Unknown"),
                0.5,
                runa_expression
            )
        
        raise ValueError(f"Cannot infer type from Runa literal: {runa_expression}")
    
    def _infer_from_runa_arithmetic(self, runa_expression: str,
                                   context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa arithmetic operations."""
        # Runa arithmetic operations: "width multiplied by height"
        arithmetic_match = re.search(self.inference_patterns["runa_arithmetic"], runa_expression, re.IGNORECASE)
        if arithmetic_match:
            left_operand = arithmetic_match.group(1)
            right_operand = arithmetic_match.group(2)
            
            left_result = self.infer_type_from_runa_expression(left_operand, context)
            right_result = self.infer_type_from_runa_expression(right_operand, context)
            
            # Arithmetic operations typically return numeric types
            if (left_result.inferred_type.name in ["Integer", "Float"] and 
                right_result.inferred_type.name in ["Integer", "Float"]):
                # If both are integers, result is integer
                if (left_result.inferred_type.name == "Integer" and 
                    right_result.inferred_type.name == "Integer"):
                    return RunaTypeInferenceResult(
                        self.type_system.basic_types["Integer"],
                        0.9,
                        runa_expression
                    )
                # Otherwise, result is float
                else:
                    return RunaTypeInferenceResult(
                        self.type_system.basic_types["Float"],
                        0.9,
                        runa_expression
                    )
        
        # Runa comparison operations: "x is greater than y"
        comparison_match = re.search(self.inference_patterns["runa_comparison"], runa_expression, re.IGNORECASE)
        if comparison_match:
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Boolean"],
                0.9,
                runa_expression
            )
        
        # Runa logical operations: "x and y"
        logical_match = re.search(self.inference_patterns["runa_logical"], runa_expression, re.IGNORECASE)
        if logical_match:
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Boolean"],
                0.9,
                runa_expression
            )
        
        raise ValueError(f"Cannot infer type from Runa arithmetic: {runa_expression}")
    
    def _infer_from_runa_string_operations(self, runa_expression: str,
                                          context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa string operations."""
        # Runa string concatenation: "user name followed by \" Smith\""
        string_concat_match = re.search(self.inference_patterns["runa_string_concat"], runa_expression, re.IGNORECASE)
        if string_concat_match:
            return RunaTypeInferenceResult(
                self.type_system.basic_types["String"],
                0.9,
                runa_expression
            )
        
        raise ValueError(f"Cannot infer type from Runa string operation: {runa_expression}")
    
    def _infer_from_runa_collection_operations(self, runa_expression: str,
                                              context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa collection operations."""
        # Runa length operation: "length of colors"
        length_match = re.search(self.inference_patterns["runa_length"], runa_expression, re.IGNORECASE)
        if length_match:
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Integer"],
                0.9,
                runa_expression
            )
        
        # Runa index access: "colors at index 0"
        index_access_match = re.search(self.inference_patterns["runa_index_access"], runa_expression, re.IGNORECASE)
        if index_access_match:
            collection_name = index_access_match.group(1)
            
            # Try to infer collection type from context
            if collection_name in context.variables:
                collection_type = context.variables[collection_name]
                if isinstance(collection_type, RunaCollectionType):
                    return RunaTypeInferenceResult(
                        collection_type.element_type,
                        0.8,
                        runa_expression
                    )
            
            # Default to unknown type
            return RunaTypeInferenceResult(
                RunaType("Unknown", "custom", "Unknown"),
                0.5,
                runa_expression,
                suggestions=[f"Collection '{collection_name}' type not known"]
            )
        
        # Runa sum operation: "the sum of all numbers in list"
        sum_match = re.search(self.inference_patterns["runa_sum"], runa_expression, re.IGNORECASE)
        if sum_match:
            # Sum operations typically return numeric types
            return RunaTypeInferenceResult(
                self.type_system.basic_types["Integer"],
                0.8,
                runa_expression
            )
        
        raise ValueError(f"Cannot infer type from Runa collection operation: {runa_expression}")
    
    def _infer_from_runa_function_call(self, runa_expression: str,
                                      context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa function calls."""
        # Runa function call: "Calculate Area with width as 5 and height as 10"
        function_match = re.search(self.inference_patterns["runa_function_call"], runa_expression, re.IGNORECASE)
        if function_match:
            function_name = function_match.group(1)
            arguments = function_match.group(2)
            
            # Check if function is known
            if function_name in context.functions:
                function_type = context.functions[function_name]
                return RunaTypeInferenceResult(
                    function_type.return_type,
                    0.9,
                    runa_expression
                )
            
            # Assume function returns unknown type
            return RunaTypeInferenceResult(
                RunaType("Unknown", "custom", "Unknown"),
                0.5,
                runa_expression,
                suggestions=[f"Function '{function_name}' return type unknown"]
            )
        
        # Runa process call: "Process called \"Calculate Area\" with width as 5"
        process_match = re.search(self.inference_patterns["runa_process_call"], runa_expression, re.IGNORECASE)
        if process_match:
            process_name = process_match.group(1)
            
            # Check if process is known
            if process_name in context.functions:
                function_type = context.functions[process_name]
                return RunaTypeInferenceResult(
                    function_type.return_type,
                    0.9,
                    runa_expression
                )
            
            # Assume process returns unknown type
            return RunaTypeInferenceResult(
                RunaType("Unknown", "custom", "Unknown"),
                0.5,
                runa_expression,
                suggestions=[f"Process '{process_name}' return type unknown"]
            )
        
        raise ValueError(f"Cannot infer type from Runa function call: {runa_expression}")
    
    def _infer_from_runa_variable(self, runa_expression: str,
                                 context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa variable references."""
        runa_expression = runa_expression.strip()
        
        # Check if variable is in context
        if runa_expression in context.variables:
            return RunaTypeInferenceResult(
                context.variables[runa_expression],
                1.0,
                runa_expression
            )
        
        # Check for variable patterns like "user name", "rectangle area"
        variable_parts = runa_expression.split()
        if len(variable_parts) >= 2:
            # Try to find variable with space-separated name
            for var_name, var_type in context.variables.items():
                if var_name.replace('_', ' ') == runa_expression:
                    return RunaTypeInferenceResult(
                        var_type,
                        0.9,
                        runa_expression
                    )
        
        raise ValueError(f"Variable '{runa_expression}' not found in context")
    
    def _infer_from_runa_context(self, runa_expression: str,
                                context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from Runa context and expected types."""
        # Check if there's an expected type for this expression
        if runa_expression in context.expected_types:
            return RunaTypeInferenceResult(
                context.expected_types[runa_expression],
                0.6,
                runa_expression
            )
        
        # Look for similar variables in context
        for var_name, var_type in context.variables.items():
            if self._similar_runa_names(runa_expression, var_name):
                return RunaTypeInferenceResult(
                    var_type,
                    0.4,
                    runa_expression,
                    suggestions=[f"Similar to variable '{var_name}'"]
                )
        
        raise ValueError(f"Cannot infer type from Runa context: {runa_expression}")
    
    def _similar_runa_names(self, name1: str, name2: str) -> bool:
        """Check if two Runa names are similar."""
        # Simple similarity check
        if name1.lower() == name2.lower():
            return True
        
        # Check for common prefixes/suffixes
        if name1.lower().startswith(name2.lower()) or name2.lower().startswith(name1.lower()):
            return True
        
        # Check for common patterns in space-separated names
        name1_parts = name1.lower().split()
        name2_parts = name2.lower().split()
        
        if len(name1_parts) > 1 and len(name2_parts) > 1:
            if name1_parts[0] == name2_parts[0] or name1_parts[-1] == name2_parts[-1]:
                return True
        
        return False
    
    def infer_runa_function_type(self, function_name: str, parameters: List[str],
                                body_expressions: List[str], 
                                context: RunaTypeInferenceContext) -> RunaFunctionType:
        """
        Infer Runa function type from parameters and body.
        
        Args:
            function_name: Name of the function
            parameters: List of parameter names
            body_expressions: List of Runa expressions in function body
            context: Type inference context
            
        Returns:
            Inferred Runa function type
        """
        # Infer parameter types
        param_types = []
        for param in parameters:
            # Try to infer from usage in body
            param_type = self._infer_runa_parameter_type_from_usage(param, body_expressions, context)
            param_types.append(param_type)
        
        # Infer return type from last expression or return statements
        return_type = self._infer_runa_return_type(body_expressions, context)
        
        return RunaFunctionType(param_types, return_type, f"Function that takes {', '.join(p.name for p in param_types)} and returns {return_type.name}")
    
    def _infer_runa_parameter_type_from_usage(self, param_name: str, 
                                             body_expressions: List[str],
                                             context: RunaTypeInferenceContext) -> RunaType:
        """Infer parameter type from its usage in Runa function body."""
        # Look for Runa operations on the parameter
        for expression in body_expressions:
            if param_name in expression:
                # Check for Runa arithmetic operations
                if re.search(rf'{param_name}\s+(?:multiplied\s+by|plus|minus|divided\s+by)', expression, re.IGNORECASE):
                    return self.type_system.basic_types["Integer"]
                
                # Check for Runa string operations
                if re.search(rf'{param_name}\s+followed\s+by', expression, re.IGNORECASE):
                    return self.type_system.basic_types["String"]
                
                # Check for Runa boolean operations
                if re.search(rf'{param_name}\s+(?:and|or)', expression, re.IGNORECASE):
                    return self.type_system.basic_types["Boolean"]
        
        # Default to unknown type
        return RunaType("Unknown", "custom", "Unknown")
    
    def _infer_runa_return_type(self, body_expressions: List[str],
                               context: RunaTypeInferenceContext) -> RunaType:
        """Infer return type from Runa function body."""
        if not body_expressions:
            return self.type_system.basic_types["Void"]
        
        # Look for return statements
        for expression in reversed(body_expressions):
            if expression.strip().lower().startswith('return'):
                # Extract return value
                return_value = expression[6:].strip()
                if return_value:
                    result = self.infer_type_from_runa_expression(return_value, context)
                    return result.inferred_type
        
        # If no return statement, infer from last expression
        last_expression = body_expressions[-1]
        result = self.infer_type_from_runa_expression(last_expression, context)
        return result.inferred_type
    
    def suggest_runa_type_annotations(self, runa_expression: str,
                                    context: RunaTypeInferenceContext) -> List[str]:
        """
        Suggest Runa type annotations for expressions.
        
        Args:
            runa_expression: The Runa expression to suggest types for
            context: Type inference context
            
        Returns:
            List of suggested Runa type annotations
        """
        suggestions = []
        
        try:
            result = self.infer_type_from_runa_expression(runa_expression, context)
            
            if result.confidence > 0.7:
                suggestions.append(f"Consider: Let {runa_expression} ({result.inferred_type.name}) be ...")
            
            for alt_type in result.alternatives:
                suggestions.append(f"Alternative: Let {runa_expression} ({alt_type.name}) be ...")
        
        except Exception as e:
            suggestions.append(f"Could not infer type: {str(e)}")
        
        return suggestions

    def infer_type_from_expression(self, expression: str, context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Alias for infer_type_from_runa_expression to maintain backward compatibility."""
        return self.infer_type_from_runa_expression(expression, context)

    def infer_expression_type(self, expression: str, context: RunaTypeInferenceContext) -> RunaTypeInferenceResult:
        """Infer type from a Runa expression."""
        return self.infer_type_from_runa_expression(expression, context) 