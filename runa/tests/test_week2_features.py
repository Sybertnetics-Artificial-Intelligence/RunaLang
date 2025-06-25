"""
Week 2 Feature Tests for Runa
============================

Tests for natural language grammar, vector-based semantic disambiguation,
and AI-native constructs implemented in Week 2.
"""

import unittest
import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from runa.compiler.lexer import RunaLexer
from runa.compiler.parser import RunaParser
from runa.compiler.semantic_analyzer import SemanticAnalyzer
from runa.compiler.context_manager import ContextManager, ContextType
from runa.compiler.vector_engine import VectorEngine, VectorType
from runa.compiler.ai_constructs import (
    LLMCommunication, AgentCoordination, SelfModification, KnowledgeGraphOperation
)


class TestWeek2Features(unittest.TestCase):
    """Test suite for Week 2 natural language grammar and AI constructs."""
    
    def setUp(self):
        """Set up test environment."""
        self.context_manager = ContextManager()
        self.vector_engine = VectorEngine()
        self.semantic_analyzer = SemanticAnalyzer()
    
    def test_context_manager_basic_operations(self):
        """Test basic context manager operations."""
        # Test context pushing and popping
        frame1 = self.context_manager.push_context(ContextType.FUNCTION_DEFINITION)
        self.assertEqual(self.context_manager.get_current_context().context_type, ContextType.FUNCTION_DEFINITION)
        
        frame2 = self.context_manager.push_context(ContextType.CONDITIONAL)
        self.assertEqual(self.context_manager.get_current_context().context_type, ContextType.CONDITIONAL)
        
        self.context_manager.pop_context()
        self.assertEqual(self.context_manager.get_current_context().context_type, ContextType.FUNCTION_DEFINITION)
        
        self.context_manager.pop_context()
        self.assertEqual(self.context_manager.get_current_context().context_type, ContextType.GLOBAL)
    
    def test_context_manager_symbol_tracking(self):
        """Test context manager symbol tracking."""
        # Add symbols to context
        self.context_manager.add_variable("x")
        self.context_manager.add_function("calculate")
        self.context_manager.add_agent("performance_agent")
        self.context_manager.add_llm("coding_llm")
        
        # Check symbols are tracked
        context = self.context_manager.get_current_context()
        self.assertIn("x", context.variables)
        self.assertIn("calculate", context.functions)
        self.assertIn("performance_agent", context.agents)
        self.assertIn("coding_llm", context.llms)
    
    def test_context_manager_disambiguation(self):
        """Test context manager disambiguation."""
        # Add symbols to context
        self.context_manager.add_variable("result")
        self.context_manager.add_function("calculate_result")
        self.context_manager.add_agent("result_agent")
        
        # Test disambiguation
        candidates = ["result", "calculate_result", "result_agent"]
        resolved = self.context_manager.resolve_ambiguity("result", candidates)
        
        # Should prefer variable in global context
        self.assertEqual(resolved, "result")
    
    def test_vector_engine_basic_operations(self):
        """Test basic vector engine operations."""
        # Test vector generation
        vector1 = self.vector_engine.generate_vector("hello", VectorType.TOKEN)
        vector2 = self.vector_engine.generate_vector("world", VectorType.TOKEN)
        
        self.assertEqual(len(vector1.vector), 16)
        self.assertEqual(len(vector2.vector), 16)
        
        # Test similarity calculation
        similarity = self.vector_engine.calculate_similarity(vector1, vector2)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 1.0)
    
    def test_vector_engine_disambiguation(self):
        """Test vector engine disambiguation."""
        # Test token disambiguation
        candidates = ["calculate", "compute", "process"]
        disambiguated = self.vector_engine.disambiguate_token("calc", candidates)
        
        # Should return one of the candidates
        self.assertIn(disambiguated, candidates)
    
    def test_vector_engine_context_vectors(self):
        """Test context vector creation and enhancement."""
        # Create context vector
        context_elements = ["function", "variable", "parameter"]
        context_vector = self.vector_engine.create_context_vector(context_elements, "function_definition")
        
        self.assertEqual(context_vector.vector_type, VectorType.CONTEXT)
        self.assertEqual(len(context_vector.vector), 16)
        
        # Test vector enhancement
        base_vector = self.vector_engine.generate_vector("test", VectorType.TOKEN)
        enhanced_vector = self.vector_engine.enhance_with_context(base_vector, context_vector)
        
        self.assertTrue(enhanced_vector.metadata.get("context_enhanced", False))
    
    def test_natural_language_parsing(self):
        """Test natural language parsing capabilities."""
        # Test natural language function declaration
        source = '''
Process called "Calculate Factorial" that takes n as Integer:
    If n is equal to 0:
        Return 1
    Otherwise:
        Return n times Calculate Factorial(n minus 1)
'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens)
        program = parser.parse()
        
        # Should parse without errors
        self.assertIsNotNone(program)
        self.assertGreater(len(program.statements), 0)
    
    def test_ai_constructs_parsing(self):
        """Test AI constructs parsing."""
        # Test LLM communication
        source = '''
Ask coding_llm about "How to implement quicksort in Python"
Delegate task "optimize database queries" to performance_agent
Modify function "calculate_fibonacci" to use memoization
Query knowledge graph for "machine learning algorithms"
'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens)
        program = parser.parse()
        
        # Should parse without errors
        self.assertIsNotNone(program)
    
    def test_context_sensitive_parsing(self):
        """Test context-sensitive parsing with disambiguation."""
        # Test parsing with context
        source = '''
Process called "Test Function" that takes x:
    Let result be x plus 10
    Return result
'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens)
        
        # Parse with function definition context
        program = parser.parse_with_context(ContextType.FUNCTION_DEFINITION)
        
        # Should parse successfully
        self.assertIsNotNone(program)
    
    def test_semantic_analysis_with_vectors(self):
        """Test semantic analysis with vector-based disambiguation."""
        # Test semantic analysis
        source = '''
Let x Be 10
Let y Be 20
Let result Be x plus y
'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens)
        program = parser.parse()
        
        # Analyze with context
        success = self.semantic_analyzer.analyze_with_context(program, ContextType.GLOBAL)
        
        if not success:
            print("Semantic errors:")
            for error in self.semantic_analyzer.get_errors():
                print(error)
        
        # Should analyze successfully
        self.assertTrue(success)
        
        # Check analysis stats
        stats = self.semantic_analyzer.get_analysis_stats()
        self.assertIn("disambiguation_count", stats)
        self.assertIn("vector_operations", stats)
    
    def test_performance_targets(self):
        """Test that Week 2 features meet performance targets."""
        # Test parsing performance
        source = '''
Process called "Performance Test" that takes n:
    Let result Be 0
    For each i In range(n):
        Let result Be result plus i
    Return result
'''
        
        start_time = time.perf_counter()
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens)
        program = parser.parse()
        
        semantic_analyzer = SemanticAnalyzer()
        success = semantic_analyzer.analyze(program)
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Should complete within 100ms target
        self.assertLess(total_time, 100.0, f"Parsing and analysis took {total_time:.2f}ms, exceeding 100ms target")
        self.assertTrue(success)
    
    def test_vector_cache_performance(self):
        """Test vector engine caching performance."""
        # Test cache efficiency
        start_time = time.perf_counter()
        
        # Generate vectors multiple times
        for i in range(100):
            self.vector_engine.generate_vector(f"token_{i}", VectorType.TOKEN)
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000
        
        # Should be fast due to caching
        self.assertLess(total_time, 50.0, f"Vector generation took {total_time:.2f}ms")
        
        # Check cache stats
        stats = self.vector_engine.get_cache_stats()
        self.assertGreater(stats["vector_cache_size"], 0)
    
    def test_error_recovery(self):
        """Test error recovery in context-sensitive parsing."""
        # Test with malformed input
        source = '''
Process called "Test" that takes:
    Let x be
    Return x
'''
        
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        parser = RunaParser(tokens)
        program = parser.parse()
        
        # Should handle errors gracefully
        self.assertIsNotNone(program)
        self.assertGreater(len(parser.errors), 0)
    
    def test_ai_constructs_creation(self):
        """Test AI constructs creation and manipulation."""
        # Test LLM communication creation
        llm_comm = LLMCommunication("ask", "coding_llm", "How to implement quicksort")
        self.assertEqual(llm_comm.operation, "ask")
        self.assertEqual(llm_comm.target_llm, "coding_llm")
        self.assertEqual(llm_comm.content, "How to implement quicksort")
        
        # Test agent coordination creation
        agent_coord = AgentCoordination("delegate", "optimize database", "performance_agent")
        self.assertEqual(agent_coord.operation, "delegate")
        self.assertEqual(agent_coord.task, "optimize database")
        self.assertEqual(agent_coord.target_agent, "performance_agent")
        
        # Test self-modification creation
        self_mod = SelfModification("modify", "calculate_fibonacci", "use memoization")
        self.assertEqual(self_mod.operation, "modify")
        self.assertEqual(self_mod.target, "calculate_fibonacci")
        self.assertEqual(self_mod.modification, "use memoization")
        
        # Test knowledge graph operation creation
        kg_op = KnowledgeGraphOperation("query", "machine learning", "algorithms")
        self.assertEqual(kg_op.operation, "query")
        self.assertEqual(kg_op.entity, "machine learning")
        self.assertEqual(kg_op.relationship, "algorithms")


class TestWeek2Integration(unittest.TestCase):
    """Integration tests for Week 2 features."""
    
    def test_end_to_end_natural_language_processing(self):
        """Test end-to-end natural language processing pipeline."""
        source = '''
Let x Be 10
Let y Be 20
Let result Be x plus y
Return result
'''
        
        # Lexical analysis
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        # Parsing with context
        parser = RunaParser(tokens)
        program = parser.parse_with_context(ContextType.FUNCTION_DEFINITION)
        
        # Semantic analysis with vectors
        semantic_analyzer = SemanticAnalyzer()
        success = semantic_analyzer.analyze_with_context(program, ContextType.FUNCTION_DEFINITION)
        
        # All stages should succeed
        self.assertIsNotNone(tokens)
        self.assertIsNotNone(program)
        self.assertTrue(success)
        
        # Check that we have statements
        self.assertGreater(len(program.statements), 0, "Should have parsed statements")
        
        # Check that context manager is working
        self.assertIsNotNone(parser.context_manager, "Context manager should be initialized")
        
        # Check that vector engine is working
        self.assertIsNotNone(semantic_analyzer.vector_semantic_engine, "Vector engine should be initialized")
    
    def test_vector_disambiguation_integration(self):
        """Test vector disambiguation integration across components."""
        # Create context with similar names
        context_manager = ContextManager()
        context_manager.add_variable("result")
        context_manager.add_function("calculate_result")
        context_manager.add_agent("result_processor")
        
        # Test disambiguation across different contexts
        vector_engine = VectorEngine()
        
        # Test in variable context
        context_manager.push_context(ContextType.ASSIGNMENT)
        disambiguated = vector_engine.disambiguate_token("res", ["result", "calculate_result", "result_processor"])
        context_manager.pop_context()
        
        # Should prefer variable in assignment context
        self.assertEqual(disambiguated, "result")
    
    def test_performance_integration(self):
        """Test performance integration across all Week 2 components."""
        source = '''
Process called Complex_Test with data as Any:
    Let processed_data Be data
    Ask coding_llm about "How to optimize this"
    Delegate task "analyze performance" to performance_agent
    Query knowledge graph for "optimization techniques"
    Return processed_data
'''
        
        start_time = time.perf_counter()
        
        # Full pipeline
        lexer = RunaLexer(source)
        tokens = lexer.tokenize()
        
        parser = RunaParser(tokens)
        program = parser.parse_with_context(ContextType.FUNCTION_DEFINITION)
        
        semantic_analyzer = SemanticAnalyzer()
        success = semantic_analyzer.analyze_with_context(program, ContextType.FUNCTION_DEFINITION)
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000
        
        # Should complete within performance targets
        self.assertLess(total_time, 100.0, f"Full pipeline took {total_time:.2f}ms")
        self.assertTrue(success)
        
        # Check all components are working
        self.assertGreater(len(tokens), 0)
        self.assertIsNotNone(program)
        self.assertGreater(len(program.statements), 0)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2) 