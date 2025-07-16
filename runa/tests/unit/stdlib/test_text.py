"""
Unit tests for Runa text module.

Tests all text processing utilities, TextWrapper class, and text analysis functions.
"""

import unittest
from runa.stdlib.text import (
    # Text formatting
    TextWrapper, dedent, indent, fill, shorten,
    
    # Text utilities
    wrap, get_text_width, justify, center, ljust, rjust,
    
    # Text analysis
    word_count, char_count, line_count, sentence_count,
    paragraph_count, readability_score, text_statistics
)


class TestTextWrapper(unittest.TestCase):
    """Test TextWrapper class."""
    
    def test_textwrapper_creation(self):
        """Test TextWrapper creation."""
        wrapper = TextWrapper(width=40)
        self.assertEqual(wrapper.width, 40)
    
    def test_textwrapper_wrap(self):
        """Test TextWrapper wrap method."""
        wrapper = TextWrapper(width=20)
        text = "This is a long text that should be wrapped to multiple lines."
        result = wrapper.wrap(text)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 1)
        
        # Check that no line exceeds width
        for line in result:
            self.assertLessEqual(len(line), 20)
    
    def test_textwrapper_fill(self):
        """Test TextWrapper fill method."""
        wrapper = TextWrapper(width=20)
        text = "This is a long text that should be wrapped."
        result = wrapper.fill(text)
        self.assertIsInstance(result, str)
        self.assertIn('\n', str(result))
    
    def test_textwrapper_with_indent(self):
        """Test TextWrapper with indentation."""
        wrapper = TextWrapper(width=30, initial_indent="  ", subsequent_indent="    ")
        text = "This is a long text that should be wrapped with indentation."
        result = wrapper.wrap(text)
        
        # Check first line has initial indent
        self.assertTrue(str(result[0]).startswith("  "))
        
        # Check subsequent lines have subsequent indent
        for line in result[1:]:
            self.assertTrue(str(line).startswith("    "))


class TestTextFormatting(unittest.TestCase):
    """Test text formatting functions."""
    
    def test_dedent(self):
        """Test dedent function."""
        text = """
            This text has
            common indentation
            that should be removed.
        """
        result = dedent(text)
        self.assertIsInstance(result, str)
        self.assertFalse(str(result).startswith(" "))
    
    def test_indent(self):
        """Test indent function."""
        text = "line1\nline2\nline3"
        result = indent(text, "  ")
        self.assertIsInstance(result, str)
        self.assertTrue(str(result).startswith("  "))
    
    def test_fill(self):
        """Test fill function."""
        text = "This is a long text that should be filled to a specific width."
        result = fill(text, width=20)
        self.assertIsInstance(result, str)
        self.assertIn('\n', str(result))
    
    def test_shorten(self):
        """Test shorten function."""
        text = "This is a very long text that should be shortened to fit in a small space."
        result = shorten(text, width=30)
        self.assertIsInstance(result, str)
        self.assertLessEqual(len(str(result)), 30)
    
    def test_wrap(self):
        """Test wrap function."""
        text = "This is a long text that should be wrapped to multiple lines."
        result = wrap(text, width=20)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 1)


class TestTextUtilities(unittest.TestCase):
    """Test text utility functions."""
    
    def test_get_text_width(self):
        """Test get_text_width function."""
        result = get_text_width("Hello")
        self.assertEqual(int(result), 5)
        
        result = get_text_width("Hello World")
        self.assertEqual(int(result), 11)
    
    def test_justify_left(self):
        """Test justify function with left alignment."""
        result = justify("Hello", 10, 'left')
        self.assertEqual(len(str(result)), 10)
        self.assertTrue(str(result).startswith("Hello"))
    
    def test_justify_right(self):
        """Test justify function with right alignment."""
        result = justify("Hello", 10, 'right')
        self.assertEqual(len(str(result)), 10)
        self.assertTrue(str(result).endswith("Hello"))
    
    def test_justify_center(self):
        """Test justify function with center alignment."""
        result = justify("Hello", 10, 'center')
        self.assertEqual(len(str(result)), 10)
        # Center alignment should have spaces on both sides
        self.assertNotEqual(str(result).strip(), str(result))
    
    def test_justify_full(self):
        """Test justify function with full justification."""
        result = justify("Hello World", 15, 'justify')
        self.assertEqual(len(str(result)), 15)
        # Should have extra spaces between words
        self.assertIn("  ", str(result))
    
    def test_center(self):
        """Test center function."""
        result = center("Hello", 10)
        self.assertEqual(len(str(result)), 10)
        self.assertTrue(str(result).strip() == "Hello")
    
    def test_ljust(self):
        """Test ljust function."""
        result = ljust("Hello", 10)
        self.assertEqual(len(str(result)), 10)
        self.assertTrue(str(result).startswith("Hello"))
    
    def test_rjust(self):
        """Test rjust function."""
        result = rjust("Hello", 10)
        self.assertEqual(len(str(result)), 10)
        self.assertTrue(str(result).endswith("Hello"))


class TestTextAnalysis(unittest.TestCase):
    """Test text analysis functions."""
    
    def test_word_count(self):
        """Test word_count function."""
        result = word_count("Hello world")
        self.assertEqual(int(result), 2)
        
        result = word_count("Hello world! How are you?")
        self.assertEqual(int(result), 5)
    
    def test_char_count(self):
        """Test char_count function."""
        result = char_count("Hello world")
        self.assertEqual(int(result), 11)  # Including space
        
        result = char_count("Hello world", include_spaces=False)
        self.assertEqual(int(result), 10)  # Excluding space
    
    def test_line_count(self):
        """Test line_count function."""
        result = line_count("line1\nline2\nline3")
        self.assertEqual(int(result), 3)
        
        result = line_count("single line")
        self.assertEqual(int(result), 1)
    
    def test_sentence_count(self):
        """Test sentence_count function."""
        result = sentence_count("Hello world. How are you? I am fine!")
        self.assertEqual(int(result), 3)
        
        result = sentence_count("No sentences here")
        self.assertEqual(int(result), 1)
    
    def test_paragraph_count(self):
        """Test paragraph_count function."""
        result = paragraph_count("para1\n\npara2\n\npara3")
        self.assertEqual(int(result), 3)
        
        result = paragraph_count("single paragraph")
        self.assertEqual(int(result), 1)
    
    def test_readability_score(self):
        """Test readability_score function."""
        # Simple text should have high readability
        result = readability_score("Hello world. This is simple.")
        self.assertGreater(float(result), 50)
        
        # Complex text should have lower readability
        complex_text = """
        The intricate complexity of this multifaceted linguistic construction 
        demonstrates the sophisticated nature of advanced vocabulary utilization 
        within the context of comprehensive textual analysis and evaluation.
        """
        result = readability_score(complex_text)
        self.assertLess(float(result), 50)
    
    def test_text_statistics(self):
        """Test text_statistics function."""
        text = "Hello world. This is a test. It has multiple sentences."
        result = text_statistics(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('characters', result)
        self.assertIn('words', result)
        self.assertIn('sentences', result)
        self.assertIn('readability_score', result)
        
        # Check that statistics are reasonable
        self.assertGreater(int(result['characters']), 0)
        self.assertGreater(int(result['words']), 0)
        self.assertGreater(int(result['sentences']), 0)
        self.assertGreaterEqual(float(result['readability_score']), 0)
        self.assertLessEqual(float(result['readability_score']), 100)


class TestTextEdgeCases(unittest.TestCase):
    """Test text functions with edge cases."""
    
    def test_empty_text(self):
        """Test functions with empty text."""
        self.assertEqual(int(word_count("")), 0)
        self.assertEqual(int(char_count("")), 0)
        self.assertEqual(int(line_count("")), 0)
        self.assertEqual(int(sentence_count("")), 0)
        self.assertEqual(int(paragraph_count("")), 0)
    
    def test_whitespace_only(self):
        """Test functions with whitespace-only text."""
        self.assertEqual(int(word_count("   \n\t   ")), 0)
        self.assertEqual(int(char_count("   \n\t   ", include_spaces=False)), 0)
    
    def test_single_character(self):
        """Test functions with single character."""
        self.assertEqual(int(word_count("a")), 1)
        self.assertEqual(int(char_count("a")), 1)
    
    def test_very_long_text(self):
        """Test functions with very long text."""
        long_text = "word " * 1000
        result = word_count(long_text)
        self.assertEqual(int(result), 1000)
        
        result = char_count(long_text)
        self.assertEqual(int(result), 5000)  # 1000 words * 5 chars each


if __name__ == '__main__':
    unittest.main() 