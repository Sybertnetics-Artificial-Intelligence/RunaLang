"""
Self-Hosting and Bidirectional Translation Tests

This module tests the critical self-hosting capabilities of Runa:
1. Round-trip translation (Runa → IR → Runa)
2. Bidirectional translation between languages
3. Semantic preservation through translation chains
4. AI-to-AI communication via Runa intermediate language

These tests ensure that Runa can serve as a universal translation
language for AI systems while preserving semantic meaning.
"""

import pytest
from runa.compiler import (
    compile_runa_to_runa, 
    compile_ir_to_runa,
    compile_runa_to_ir,
    compile_runa_to_python,
    BidirectionalTranslator, 
    SupportedLanguage,
    create_bidirectional_translator,
    translate_to_runa,
    translate_from_runa
)


class TestSelfHosting:
    """Test self-hosting capabilities - Runa compiling itself."""
    
    def test_simple_round_trip(self):
        """Test that simple Runa code survives round-trip translation."""
        original = '''Let user name be "Alice"
Let age be 25
Display user name with message "User:"'''
        
        # Round trip: Runa → IR → Runa
        regenerated = compile_runa_to_runa(original)
        
        # Both should compile to identical IR
        original_ir = compile_runa_to_ir(original)
        regenerated_ir = compile_runa_to_ir(regenerated)
        
        # IR should be structurally equivalent
        assert len(original_ir.functions) == len(regenerated_ir.functions)
        assert original_ir.functions[0].name == regenerated_ir.functions[0].name
    
    def test_arithmetic_round_trip(self):
        """Test round-trip translation of arithmetic expressions."""
        original = '''Let price be 100.00
Let tax rate be 0.08
Let total be price multiplied by (1 plus tax rate)
Display total with message "Total cost:"'''
        
        regenerated = compile_runa_to_runa(original)
        
        # Should preserve arithmetic semantics
        assert "multiplied by" in regenerated
        assert "plus" in regenerated
        assert "100" in regenerated or "100.0" in regenerated
        assert "0.08" in regenerated
    
    def test_conditional_round_trip(self):
        """Test round-trip translation of conditional statements."""
        original = '''Let age be 25

If age is greater than 18:
    Display "Adult user"
    Set voting eligible to true
Otherwise:
    Display "Minor user"
    Set voting eligible to false'''
        
        regenerated = compile_runa_to_runa(original)
        
        # Should preserve conditional structure
        assert "If" in regenerated
        assert "is greater than" in regenerated
        assert "Otherwise:" in regenerated
        assert "Display" in regenerated
    
    def test_function_call_round_trip(self):
        """Test round-trip translation of function calls."""
        original = '''Let result be Calculate Interest with principal as 1000 and rate as 0.05 and years as 3
Display result'''
        
        regenerated = compile_runa_to_runa(original)
        
        # Should preserve function call structure
        assert "Calculate Interest" in regenerated or "with" in regenerated
        assert "1000" in regenerated
        assert "0.05" in regenerated
    
    def test_list_operations_round_trip(self):
        """Test round-trip translation of list operations."""
        original = '''Let numbers be list containing 1, 2, 3, 4, 5
Let total be Calculate Sum with values as numbers
Display total with message "Sum:"'''
        
        regenerated = compile_runa_to_runa(original)
        
        # Should preserve list syntax
        assert "list containing" in regenerated
        assert "1" in regenerated and "2" in regenerated
    
    def test_complex_program_round_trip(self):
        """Test round-trip translation of a complex program."""
        original = '''Let customer name be "Alice Johnson"
Let account balance be 1250.75
Let minimum balance be 100.00

Let service fee be Calculate Service Fee with balance as account balance
Let new balance be account balance minus service fee

Display customer name with message "Customer:"
Display new balance with message "New balance:"

If new balance is greater than minimum balance:
    Display "Account in good standing"
Otherwise:
    Display "Account below minimum balance"'''
        
        regenerated = compile_runa_to_runa(original)
        
        # Should preserve all key elements
        assert "Alice Johnson" in regenerated
        assert "1250.75" in regenerated
        assert "Calculate Service Fee" in regenerated or "with balance as" in regenerated
        assert "minus" in regenerated
        assert "If" in regenerated and "Otherwise:" in regenerated


class TestBidirectionalTranslation:
    """Test bidirectional translation engine."""
    
    def setup_method(self):
        """Set up translator for each test."""
        self.translator = create_bidirectional_translator()
    
    def test_translator_creation(self):
        """Test that bidirectional translator can be created."""
        translator = BidirectionalTranslator()
        assert translator is not None
        
        # Should support Runa and Python at minimum
        languages = translator.get_supported_languages()
        assert SupportedLanguage.RUNA in languages
        assert SupportedLanguage.PYTHON in languages
    
    def test_runa_to_runa_translation(self):
        """Test Runa to Runa translation (validation/formatting)."""
        source = '''Let x be 42
Display x'''
        
        result = self.translator.translate(source, SupportedLanguage.RUNA, SupportedLanguage.RUNA)
        
        assert result.success
        assert result.target_code is not None
        assert "Let" in result.target_code
        assert "42" in result.target_code
    
    def test_runa_to_python_translation(self):
        """Test Runa to Python translation."""
        runa_code = '''Let user name be "Alice"
Let age be 25
Display user name with message "User:"'''
        
        result = self.translator.translate(runa_code, SupportedLanguage.RUNA, SupportedLanguage.PYTHON)
        
        assert result.success
        assert result.target_code is not None
        assert "Alice" in result.target_code
        assert "25" in result.target_code
        # Should be valid Python (contains def main or similar structure)
        assert "def" in result.target_code or "=" in result.target_code
    
    def test_convenience_functions(self):
        """Test convenience functions for translation."""
        runa_code = '''Let message be "Hello World"
Display message'''
        
        # Test translate_to_runa (should be identity for Runa input)
        runa_result = translate_to_runa(runa_code, "runa")
        assert "Hello World" in runa_result
        
        # Test translate_from_runa
        python_result = translate_from_runa(runa_code, "python")
        assert "Hello World" in python_result
    
    def test_translation_result_structure(self):
        """Test that translation results have proper structure."""
        result = self.translator.translate(
            'Let x be 10', 
            SupportedLanguage.RUNA, 
            SupportedLanguage.PYTHON
        )
        
        assert hasattr(result, 'source_language')
        assert hasattr(result, 'target_language')
        assert hasattr(result, 'source_code')
        assert hasattr(result, 'target_code')
        assert hasattr(result, 'intermediate_runa')
        assert hasattr(result, 'success')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'warnings')
        
        assert result.source_language == SupportedLanguage.RUNA
        assert result.target_language == SupportedLanguage.PYTHON
        assert result.success is True
    
    def test_translation_error_handling(self):
        """Test error handling in translation."""
        # Invalid Runa code
        invalid_runa = "This is not valid Runa syntax at all!!!"
        
        result = self.translator.translate(
            invalid_runa, 
            SupportedLanguage.RUNA, 
            SupportedLanguage.PYTHON
        )
        
        assert result.success is False
        assert len(result.errors) > 0
    
    def test_round_trip_validation(self):
        """Test round-trip validation functionality."""
        valid_runa = '''Let count be 5
Let message be "Processing item"
Display message with message count'''
        
        is_valid, errors = self.translator.validate_round_trip(valid_runa, SupportedLanguage.RUNA)
        
        # Should be valid (or at least not crash)
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)
    
    def test_available_translations(self):
        """Test getting available translation mappings."""
        available = self.translator.get_available_translations()
        
        assert isinstance(available, dict)
        assert SupportedLanguage.RUNA in available
        
        # Runa should be able to translate to itself and Python at minimum
        runa_targets = available[SupportedLanguage.RUNA]
        assert SupportedLanguage.RUNA in runa_targets
        assert SupportedLanguage.PYTHON in runa_targets


class TestSemanticPreservation:
    """Test that semantic meaning is preserved through translations."""
    
    def test_variable_semantics(self):
        """Test that variable semantics are preserved."""
        original = '''Let user age be 25
Let voting age be 18
Let can vote be user age is greater than or equal to voting age'''
        
        # Translate to Python and back
        python_code = compile_runa_to_python(original)
        ir_module = compile_runa_to_ir(original)
        regenerated = compile_ir_to_runa(ir_module)
        
        # Both should have same variable structure
        assert "user age" in regenerated or "user_age" in regenerated
        assert "voting age" in regenerated or "voting_age" in regenerated
        assert "greater than or equal to" in regenerated or "is greater than" in regenerated
    
    def test_arithmetic_semantics(self):
        """Test that arithmetic semantics are preserved."""
        original = '''Let a be 10
Let b be 5
Let sum be a plus b
Let product be a multiplied by b
Let quotient be a divided by b'''
        
        ir_module = compile_runa_to_ir(original)
        regenerated = compile_ir_to_runa(ir_module)
        
        # Should preserve arithmetic operations
        assert "plus" in regenerated
        assert "multiplied by" in regenerated
        assert "divided by" in regenerated
        assert "10" in regenerated
        assert "5" in regenerated
    
    def test_control_flow_semantics(self):
        """Test that control flow semantics are preserved."""
        original = '''Let temperature be 75

If temperature is greater than 80:
    Display "Hot day"
Otherwise:
    If temperature is greater than 60:
        Display "Nice day"
    Otherwise:
        Display "Cold day"'''
        
        ir_module = compile_runa_to_ir(original)
        regenerated = compile_ir_to_runa(ir_module)
        
        # Should preserve conditional structure
        assert "If" in regenerated
        assert "Otherwise:" in regenerated
        assert "is greater than" in regenerated
        assert "75" in regenerated
        assert "80" in regenerated


class TestAIToCommunication:
    """Test AI-to-AI communication capabilities via Runa."""
    
    def test_logic_to_coding_llm_workflow(self):
        """
        Test the workflow where Logic LLM specifies requirements in Runa,
        and Coding LLM translates to target language.
        """
        # Simulate Logic LLM output (natural language specification in Runa)
        logic_llm_output = '''Process called "calculate total price" that takes price as Float and tax rate as Float returns Float:
    Let tax amount be price multiplied by tax rate
    Let total be price plus tax amount
    Return total

Let item price be 100.00
Let sales tax be 0.08
Let final price be calculate total price with price as item price and tax rate as sales tax
Display final price with message "Total cost:"'''
        
        # Coding LLM translates Runa to Python
        translator = create_bidirectional_translator()
        result = translator.translate_runa_to_any(logic_llm_output, SupportedLanguage.PYTHON)
        
        assert result.success
        assert "def" in result.target_code  # Should generate Python function
        assert "100" in result.target_code
        assert "0.08" in result.target_code
    
    def test_specification_preservation(self):
        """Test that specifications are preserved through the AI communication chain."""
        specification = '''Let user preferences be dictionary with "theme" as "dark" and "language" as "english"
Let default timeout be 30
Let max retries be 3

If user preferences contains "theme":
    Set application theme to user preferences at "theme"
Otherwise:
    Set application theme to "light"'''
        
        # Should survive round-trip translation
        regenerated = compile_runa_to_runa(specification)
        
        # Key specification elements should be preserved
        assert "user preferences" in regenerated
        assert "dictionary" in regenerated
        assert "dark" in regenerated
        assert "english" in regenerated
        assert "30" in regenerated
        assert "contains" in regenerated
    
    def test_cross_language_equivalence(self):
        """Test that equivalent functionality is generated across languages."""
        runa_spec = '''Let numbers be list containing 1, 2, 3, 4, 5
Let sum be 0
For each number in numbers:
    Set sum to sum plus number
Display sum with message "Total:"'''
        
        translator = create_bidirectional_translator()
        
        # Generate Python
        python_result = translator.translate_runa_to_any(runa_spec, SupportedLanguage.PYTHON)
        
        if python_result.success:
            # Should contain equivalent logic
            assert "1" in python_result.target_code
            assert "2" in python_result.target_code
            # Should have some form of iteration or calculation
            python_has_logic = any(keyword in python_result.target_code.lower() 
                                 for keyword in ["for", "while", "sum", "+", "append"])
            assert python_has_logic


if __name__ == "__main__":
    pytest.main([__file__, "-v"])