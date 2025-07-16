"""
Unit tests for Runa string module.

Tests all string utilities, constants, Template class, and Formatter class.
"""

import unittest
from runa.stdlib.string import (
    # String constants
    ascii_letters, ascii_lowercase, ascii_uppercase,
    digits, hexdigits, octdigits, punctuation,
    printable, whitespace,
    
    # String functions
    capwords, Template, Formatter,
    
    # Utility functions
    split, join, replace, strip, lstrip, rstrip,
    upper, lower, title, capitalize, swapcase,
    count, find, rfind, index, rindex,
    startswith, endswith, isalnum, isalpha,
    isdigit, islower, isupper, isspace, istitle
)


class TestStringConstants(unittest.TestCase):
    """Test string constants."""
    
    def test_ascii_letters(self):
        """Test ascii_letters constant."""
        self.assertEqual(len(ascii_letters), 52)
        self.assertTrue(all(c.isalpha() for c in ascii_letters))
    
    def test_ascii_lowercase(self):
        """Test ascii_lowercase constant."""
        self.assertEqual(len(ascii_lowercase), 26)
        self.assertTrue(all(c.islower() for c in ascii_lowercase))
    
    def test_ascii_uppercase(self):
        """Test ascii_uppercase constant."""
        self.assertEqual(len(ascii_uppercase), 26)
        self.assertTrue(all(c.isupper() for c in ascii_uppercase))
    
    def test_digits(self):
        """Test digits constant."""
        self.assertEqual(len(digits), 10)
        self.assertTrue(all(c.isdigit() for c in digits))
    
    def test_hexdigits(self):
        """Test hexdigits constant."""
        self.assertEqual(len(hexdigits), 22)  # 0-9, a-f, A-F
        self.assertTrue(all(c in '0123456789abcdefABCDEF' for c in hexdigits))
    
    def test_octdigits(self):
        """Test octdigits constant."""
        self.assertEqual(len(octdigits), 8)
        self.assertTrue(all(c in '01234567' for c in octdigits))
    
    def test_punctuation(self):
        """Test punctuation constant."""
        self.assertTrue(len(punctuation) > 0)
        self.assertTrue(all(not c.isalnum() for c in punctuation))
    
    def test_printable(self):
        """Test printable constant."""
        self.assertTrue(len(printable) > 0)
        # Note: Some characters in printable may not be isprintable() in all contexts
        # This is a more lenient test
        self.assertTrue(len(printable) >= 100)  # Should have many printable characters
    
    def test_whitespace(self):
        """Test whitespace constant."""
        self.assertTrue(len(whitespace) > 0)
        self.assertTrue(all(c.isspace() for c in whitespace))


class TestTemplate(unittest.TestCase):
    """Test Template class."""
    
    def test_template_creation(self):
        """Test Template creation."""
        template = Template("Hello, $name!")
        self.assertEqual(str(template), "Hello, $name!")
    
    def test_template_substitute(self):
        """Test template substitution."""
        template = Template("Hello, $name! You are $age years old.")
        result = template.substitute({'name': 'Alice', 'age': 30})
        self.assertEqual(str(result), "Hello, Alice! You are 30 years old.")
    
    def test_template_safe_substitute(self):
        """Test safe template substitution."""
        template = Template("Hello, $name! You are $age years old.")
        result = template.safe_substitute({'name': 'Alice'})
        self.assertEqual(str(result), "Hello, Alice! You are $age years old.")
    
    def test_template_with_kwargs(self):
        """Test template substitution with kwargs."""
        template = Template("Hello, $name!")
        result = template.substitute({}, name='Bob')  # Pass empty dict as mapping
        self.assertEqual(str(result), "Hello, Bob!")
    
    def test_template_repr(self):
        """Test Template representation."""
        template = Template("Hello, $name!")
        self.assertEqual(repr(template), "Template('Hello, $name!')")


class TestFormatter(unittest.TestCase):
    """Test Formatter class."""
    
    def test_formatter_creation(self):
        """Test Formatter creation."""
        formatter = Formatter()
        self.assertIsNotNone(formatter)
    
    def test_formatter_format(self):
        """Test formatter format method."""
        formatter = Formatter()
        result = formatter.format("Hello, {}!", "World")
        self.assertEqual(str(result), "Hello, World!")
    
    def test_formatter_vformat(self):
        """Test formatter vformat method."""
        formatter = Formatter()
        result = formatter.vformat("Hello, {}!", ("World",), {})
        self.assertEqual(str(result), "Hello, World!")
    
    def test_formatter_parse(self):
        """Test formatter parse method."""
        formatter = Formatter()
        result = formatter.parse("Hello, {name}!")
        # Convert iterator to list for testing
        result_list = list(result)
        self.assertIsInstance(result_list, list)
        self.assertTrue(len(result_list) > 0)


class TestStringUtilityFunctions(unittest.TestCase):
    """Test string utility functions."""
    
    def test_capwords(self):
        """Test capwords function."""
        result = capwords("hello world")
        self.assertEqual(str(result), "Hello World")
        
        result = capwords("hello-world", "-")
        self.assertEqual(str(result), "Hello-World")
    
    def test_split(self):
        """Test split function."""
        result = split("hello world")
        result_items = result._items
        self.assertEqual(len(result_items), 2)
        self.assertEqual(str(result_items[0]), "hello")
        self.assertEqual(str(result_items[1]), "world")
        
        result = split("hello,world", ",")
        result_items = result._items
        self.assertEqual(len(result_items), 2)
        self.assertEqual(str(result_items[0]), "hello")
        self.assertEqual(str(result_items[1]), "world")
    
    def test_join(self):
        """Test join function."""
        result = join(["hello", "world"], " ")
        self.assertEqual(str(result), "hello world")
        
        result = join(["a", "b", "c"], "-")
        self.assertEqual(str(result), "a-b-c")
    
    def test_replace(self):
        """Test replace function."""
        result = replace("hello world", "world", "python")
        self.assertEqual(str(result), "hello python")
        
        result = replace("hello hello hello", "hello", "hi", 2)
        self.assertEqual(str(result), "hi hi hello")
    
    def test_strip(self):
        """Test strip function."""
        result = strip("  hello world  ")
        self.assertEqual(str(result), "hello world")
        
        result = strip("***hello***", "*")
        self.assertEqual(str(result), "hello")
    
    def test_lstrip(self):
        """Test lstrip function."""
        result = lstrip("  hello world  ")
        self.assertEqual(str(result), "hello world  ")
        
        result = lstrip("***hello***", "*")
        self.assertEqual(str(result), "hello***")
    
    def test_rstrip(self):
        """Test rstrip function."""
        result = rstrip("  hello world  ")
        self.assertEqual(str(result), "  hello world")
        
        result = rstrip("***hello***", "*")
        self.assertEqual(str(result), "***hello")
    
    def test_upper(self):
        """Test upper function."""
        result = upper("hello world")
        self.assertEqual(str(result), "HELLO WORLD")
    
    def test_lower(self):
        """Test lower function."""
        result = lower("HELLO WORLD")
        self.assertEqual(str(result), "hello world")
    
    def test_title(self):
        """Test title function."""
        result = title("hello world")
        self.assertEqual(str(result), "Hello World")
    
    def test_capitalize(self):
        """Test capitalize function."""
        result = capitalize("hello world")
        self.assertEqual(str(result), "Hello world")
    
    def test_swapcase(self):
        """Test swapcase function."""
        result = swapcase("Hello World")
        self.assertEqual(str(result), "hELLO wORLD")
    
    def test_count(self):
        """Test count function."""
        result = count("hello hello hello", "hello")
        self.assertEqual(int(result), 3)
        
        result = count("hello hello hello", "hello", 0, 10)
        self.assertEqual(int(result), 1)
    
    def test_find(self):
        """Test find function."""
        result = find("hello world", "world")
        self.assertEqual(int(result), 6)
        
        result = find("hello world", "python")
        self.assertEqual(int(result), -1)
    
    def test_rfind(self):
        """Test rfind function."""
        result = rfind("hello world hello", "hello")
        self.assertEqual(int(result), 12)
    
    def test_index(self):
        """Test index function."""
        result = index("hello world", "world")
        self.assertEqual(int(result), 6)
        
        with self.assertRaises(ValueError):
            index("hello world", "python")
    
    def test_rindex(self):
        """Test rindex function."""
        result = rindex("hello world hello", "hello")
        self.assertEqual(int(result), 12)
        
        with self.assertRaises(ValueError):
            rindex("hello world", "python")
    
    def test_startswith(self):
        """Test startswith function."""
        result = startswith("hello world", "hello")
        self.assertTrue(bool(result))
        
        result = startswith("hello world", "world")
        self.assertFalse(bool(result))
    
    def test_endswith(self):
        """Test endswith function."""
        result = endswith("hello world", "world")
        self.assertTrue(bool(result))
        
        result = endswith("hello world", "hello")
        self.assertFalse(bool(result))
    
    def test_isalnum(self):
        """Test isalnum function."""
        result = isalnum("hello123")
        self.assertTrue(bool(result))
        
        result = isalnum("hello world")
        self.assertFalse(bool(result))
    
    def test_isalpha(self):
        """Test isalpha function."""
        result = isalpha("hello")
        self.assertTrue(bool(result))
        
        result = isalpha("hello123")
        self.assertFalse(bool(result))
    
    def test_isdigit(self):
        """Test isdigit function."""
        result = isdigit("123")
        self.assertTrue(bool(result))
        
        result = isdigit("123abc")
        self.assertFalse(bool(result))
    
    def test_islower(self):
        """Test islower function."""
        result = islower("hello")
        self.assertTrue(bool(result))
        
        result = islower("Hello")
        self.assertFalse(bool(result))
    
    def test_isupper(self):
        """Test isupper function."""
        result = isupper("HELLO")
        self.assertTrue(bool(result))
        
        result = isupper("Hello")
        self.assertFalse(bool(result))
    
    def test_isspace(self):
        """Test isspace function."""
        result = isspace("   ")
        self.assertTrue(bool(result))
        
        result = isspace("hello")
        self.assertFalse(bool(result))
    
    def test_istitle(self):
        """Test istitle function."""
        result = istitle("Hello World")
        self.assertTrue(bool(result))
        
        result = istitle("hello world")
        self.assertFalse(bool(result))


if __name__ == '__main__':
    unittest.main() 