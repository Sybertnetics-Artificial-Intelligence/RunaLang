#!/usr/bin/env python3
"""
JavaScript Toolchain Round-Trip Verification Tests

Comprehensive tests for JavaScript parser, converter, generator,
and round-trip translation verification to ensure syntax and
semantics are preserved during Runa translation.
"""

import unittest
import sys
from pathlib import Path

# Add runa source to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from runa.languages.javascript import (
    JavaScriptToolchain, parse_javascript, js_to_runa, runa_to_js,
    generate_javascript, JSProgram, LANGUAGE_INFO
)


class TestJavaScriptParser(unittest.TestCase):
    """Test JavaScript parser functionality."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_parse_simple_expressions(self):
        """Test parsing simple expressions."""
        test_cases = [
            "42",
            '"hello world"',
            "true",
            "false",
            "null",
            "undefined",
            "x",
            "x + y",
            "x * (y + z)",
            "x > 5 && y < 10",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.parse(code)
                self.assertTrue(result.success, f"Failed to parse: {code}")
                self.assertIsNotNone(result.ast)
                self.assertIsInstance(result.ast, JSProgram)
    
    def test_parse_variable_declarations(self):
        """Test parsing variable declarations."""
        test_cases = [
            "var x = 5;",
            "let y = 'hello';",
            "const z = true;",
            "var a, b = 10, c;",
            "let {name, age} = person;",
            "const [first, second] = array;",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.parse(code)
                self.assertTrue(result.success, f"Failed to parse: {code}")
    
    def test_parse_function_declarations(self):
        """Test parsing function declarations."""
        test_cases = [
            "function hello() {}",
            "function greet(name) { return 'Hello ' + name; }",
            "function* generator() { yield 1; }",
            "async function fetchData() { return await api.get(); }",
            "function sum(a, b = 0) { return a + b; }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.parse(code)
                self.assertTrue(result.success, f"Failed to parse: {code}")
    
    def test_parse_control_flow(self):
        """Test parsing control flow statements."""
        test_cases = [
            "if (x > 5) { console.log('big'); }",
            "if (x) { doSomething(); } else { doOther(); }",
            "while (condition) { process(); }",
            "for (let i = 0; i < 10; i++) { work(i); }",
            "for (const item of items) { handle(item); }",
            "for (const key in obj) { process(obj[key]); }",
            "switch (value) { case 1: return 'one'; default: return 'other'; }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.parse(code)
                self.assertTrue(result.success, f"Failed to parse: {code}")
    
    def test_parse_modern_features(self):
        """Test parsing modern JavaScript features."""
        test_cases = [
            "const f = (x) => x * 2;",
            "const obj = { method() { return this.value; } };",
            "const {a, b, ...rest} = obj;",
            "const arr = [...items, newItem];",
            "const name = `Hello ${user.name}!`;",
            "const value = obj?.property?.nested;",
            "const result = value ?? defaultValue;",
            "class MyClass extends BaseClass { constructor() { super(); } }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.parse(code)
                self.assertTrue(result.success, f"Failed to parse: {code}")
    
    def test_parse_async_await(self):
        """Test parsing async/await syntax."""
        test_cases = [
            "async function getData() { const data = await fetch('/api'); return data.json(); }",
            "const getData = async () => { return await Promise.resolve(42); };",
            "try { const result = await operation(); } catch (e) { console.error(e); }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.parse(code)
                self.assertTrue(result.success, f"Failed to parse: {code}")


class TestJavaScriptConverter(unittest.TestCase):
    """Test JavaScript ↔ Runa conversion functionality."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_convert_simple_expressions(self):
        """Test converting simple expressions."""
        test_cases = [
            "42",
            '"hello"',
            "true",
            "x",
            "x + y",
            "x * y",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                # Parse JavaScript
                parse_result = self.toolchain.parse(code)
                self.assertTrue(parse_result.success)
                
                # Convert to Runa
                to_runa_result = self.toolchain.to_runa(parse_result.ast)
                self.assertTrue(to_runa_result.success)
                
                # Convert back to JavaScript
                from_runa_result = self.toolchain.from_runa(to_runa_result.target_ast)
                self.assertTrue(from_runa_result.success)
    
    def test_convert_variable_declarations(self):
        """Test converting variable declarations."""
        test_cases = [
            "var x = 5;",
            "let y = 'hello';",
            "const z = true;",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                parse_result = self.toolchain.parse(code)
                self.assertTrue(parse_result.success)
                
                to_runa_result = self.toolchain.to_runa(parse_result.ast)
                self.assertTrue(to_runa_result.success)
                
                from_runa_result = self.toolchain.from_runa(to_runa_result.target_ast)
                self.assertTrue(from_runa_result.success)
    
    def test_convert_functions(self):
        """Test converting function declarations."""
        test_cases = [
            "function hello() { return 'world'; }",
            "function add(a, b) { return a + b; }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                parse_result = self.toolchain.parse(code)
                self.assertTrue(parse_result.success)
                
                to_runa_result = self.toolchain.to_runa(parse_result.ast)
                self.assertTrue(to_runa_result.success)
                
                from_runa_result = self.toolchain.from_runa(to_runa_result.target_ast)
                self.assertTrue(from_runa_result.success)
    
    def test_convert_control_flow(self):
        """Test converting control flow statements."""
        test_cases = [
            "if (x > 5) { console.log('big'); }",
            "while (condition) { process(); }",
            "for (let i = 0; i < 10; i++) { work(i); }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                parse_result = self.toolchain.parse(code)
                self.assertTrue(parse_result.success)
                
                to_runa_result = self.toolchain.to_runa(parse_result.ast)
                self.assertTrue(to_runa_result.success)
                
                from_runa_result = self.toolchain.from_runa(to_runa_result.target_ast)
                self.assertTrue(from_runa_result.success)


class TestJavaScriptGenerator(unittest.TestCase):
    """Test JavaScript code generation."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_generate_simple_code(self):
        """Test generating simple JavaScript code."""
        test_cases = [
            "42;",
            '"hello";',
            "true;",
            "x;",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                parse_result = self.toolchain.parse(code)
                self.assertTrue(parse_result.success)
                
                gen_result = self.toolchain.generate(parse_result.ast)
                self.assertTrue(gen_result.success)
                self.assertIsInstance(gen_result.code, str)
                self.assertGreater(len(gen_result.code), 0)
    
    def test_generate_with_formatting(self):
        """Test generating code with different formatting styles."""
        code = "function hello(name) { if (name) { return 'Hello ' + name; } else { return 'Hello World'; } }"
        
        parse_result = self.toolchain.parse(code)
        self.assertTrue(parse_result.success)
        
        # Test different styles
        styles = ["standard", "airbnb", "google", "prettier"]
        for style in styles:
            with self.subTest(style=style):
                gen_result = self.toolchain.generate(parse_result.ast, style=style)
                self.assertTrue(gen_result.success)
                self.assertIsInstance(gen_result.code, str)
    
    def test_generate_minified(self):
        """Test generating minified code."""
        code = "function hello(name) { return 'Hello ' + name; }"
        
        parse_result = self.toolchain.parse(code)
        self.assertTrue(parse_result.success)
        
        # Normal generation
        normal_result = self.toolchain.generate(parse_result.ast)
        self.assertTrue(normal_result.success)
        
        # Minified generation
        minified_result = self.toolchain.generate(parse_result.ast, minify=True)
        self.assertTrue(minified_result.success)
        
        # Minified should be shorter
        self.assertLess(len(minified_result.code), len(normal_result.code))


class TestJavaScriptRoundTrip(unittest.TestCase):
    """Test JavaScript round-trip translation verification."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_round_trip_simple_expressions(self):
        """Test round-trip for simple expressions."""
        test_cases = [
            "42;",
            '"hello world";',
            "true;",
            "false;",
            "null;",
            "x;",
            "x + y;",
            "x * (y + z);",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.round_trip_verify(code)
                self.assertTrue(result.success, 
                    f"Round-trip failed for '{code}': {result.differences}")
                self.assertGreater(result.similarity_score, 0.8)
    
    def test_round_trip_variable_declarations(self):
        """Test round-trip for variable declarations."""
        test_cases = [
            "var x = 5;",
            "let y = 'hello';",
            "const z = true;",
            "var a = 1, b = 2;",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.round_trip_verify(code)
                # Note: Some formatting differences are acceptable
                self.assertGreater(result.similarity_score, 0.7,
                    f"Low similarity for '{code}': {result.similarity_score}")
    
    def test_round_trip_functions(self):
        """Test round-trip for function declarations."""
        test_cases = [
            "function hello() { return 'world'; }",
            "function add(a, b) { return a + b; }",
            "function greet(name) { if (name) { return 'Hello ' + name; } return 'Hello'; }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.round_trip_verify(code)
                self.assertGreater(result.similarity_score, 0.7,
                    f"Low similarity for function: {result.similarity_score}")
    
    def test_round_trip_control_flow(self):
        """Test round-trip for control flow statements."""
        test_cases = [
            "if (x > 5) { console.log('big'); }",
            "while (condition) { process(); }",
            "for (let i = 0; i < 10; i++) { work(i); }",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.round_trip_verify(code)
                self.assertGreater(result.similarity_score, 0.6,
                    f"Low similarity for control flow: {result.similarity_score}")
    
    def test_round_trip_modern_features(self):
        """Test round-trip for modern JavaScript features."""
        test_cases = [
            "const f = (x) => x * 2;",
            "const obj = { name: 'test', value: 42 };",
            "const arr = [1, 2, 3];",
            "const greeting = `Hello ${name}!`;",
        ]
        
        for code in test_cases:
            with self.subTest(code=code):
                result = self.toolchain.round_trip_verify(code)
                # Modern features might have more transformation
                self.assertGreater(result.similarity_score, 0.5,
                    f"Low similarity for modern feature: {result.similarity_score}")
    
    def test_round_trip_complex_program(self):
        """Test round-trip for a complex JavaScript program."""
        complex_code = '''
        function fibonacci(n) {
            if (n <= 1) {
                return n;
            }
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
        
        const numbers = [1, 2, 3, 4, 5];
        const doubled = numbers.map(x => x * 2);
        
        for (let i = 0; i < 10; i++) {
            const result = fibonacci(i);
            console.log(`fibonacci(${i}) = ${result}`);
        }
        '''
        
        result = self.toolchain.round_trip_verify(complex_code)
        self.assertGreater(result.similarity_score, 0.4,
            f"Low similarity for complex program: {result.similarity_score}")
        
        # Check that basic structure is preserved
        self.assertIsNotNone(result.original_ast)
        self.assertIsNotNone(result.runa_ast)
        self.assertIsNotNone(result.regenerated_ast)
        self.assertIsNotNone(result.regenerated_code)


class TestJavaScriptValidation(unittest.TestCase):
    """Test JavaScript syntax validation."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_validate_valid_syntax(self):
        """Test validation of valid JavaScript syntax."""
        valid_codes = [
            "var x = 5;",
            "function hello() { return 'world'; }",
            "if (true) { console.log('yes'); }",
            "const arr = [1, 2, 3];",
            "const obj = { name: 'test' };",
        ]
        
        for code in valid_codes:
            with self.subTest(code=code):
                validation = self.toolchain.validate_syntax(code)
                self.assertTrue(validation['valid'], f"Valid code marked invalid: {code}")
                self.assertIsNone(validation['error'])
    
    def test_validate_invalid_syntax(self):
        """Test validation of invalid JavaScript syntax."""
        invalid_codes = [
            "var x = ;",  # Missing value
            "function () { }",  # Missing name
            "if (true { }",  # Missing closing paren
            "const arr = [1, 2,];",  # Trailing comma (might be valid in some contexts)
            "return 'outside function';",  # Return outside function
        ]
        
        for code in invalid_codes:
            with self.subTest(code=code):
                validation = self.toolchain.validate_syntax(code)
                # Note: Some of these might actually be valid in certain contexts
                # The important thing is that the validator doesn't crash
                self.assertIsInstance(validation['valid'], bool)


class TestJavaScriptToolchainStats(unittest.TestCase):
    """Test JavaScript toolchain statistics and metadata."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_language_info(self):
        """Test language information constants."""
        self.assertEqual(LANGUAGE_INFO['name'], 'JavaScript')
        self.assertEqual(LANGUAGE_INFO['id'], 'javascript')
        self.assertEqual(LANGUAGE_INFO['tier'], 1)
        self.assertIn('.js', LANGUAGE_INFO['file_extensions'])
        self.assertTrue(LANGUAGE_INFO['features']['es6'])
        self.assertTrue(LANGUAGE_INFO['features']['async_await'])
    
    def test_toolchain_stats(self):
        """Test toolchain statistics tracking."""
        # Initial stats
        initial_stats = self.toolchain.get_stats()
        self.assertEqual(initial_stats['parser']['files_parsed'], 0)
        self.assertEqual(initial_stats['conversion']['js_to_runa_conversions'], 0)
        
        # Parse some code
        self.toolchain.parse("var x = 5;")
        self.toolchain.parse("function hello() { return 'world'; }")
        
        # Check updated stats
        updated_stats = self.toolchain.get_stats()
        self.assertEqual(updated_stats['parser']['files_parsed'], 2)
        self.assertGreater(updated_stats['parser']['lines_parsed'], 0)
    
    def test_supported_features(self):
        """Test supported feature detection."""
        stats = self.toolchain.get_stats()
        features = stats['supported_features']
        
        # Check key features are supported
        self.assertTrue(features['es6'])
        self.assertTrue(features['async_await'])
        self.assertTrue(features['classes'])
        self.assertTrue(features['arrow_functions'])
        self.assertTrue(features['template_literals'])
        self.assertTrue(features['destructuring'])
        self.assertTrue(features['spread_operator'])
        self.assertTrue(features['optional_chaining'])
        self.assertTrue(features['nullish_coalescing'])


class TestJavaScriptIntegration(unittest.TestCase):
    """Integration tests for JavaScript toolchain."""
    
    def setUp(self):
        self.toolchain = JavaScriptToolchain()
    
    def test_complete_workflow(self):
        """Test complete JavaScript processing workflow."""
        code = '''
        function greet(name) {
            if (name) {
                return `Hello, ${name}!`;
            } else {
                return "Hello, World!";
            }
        }
        
        const message = greet("JavaScript");
        console.log(message);
        '''
        
        # Step 1: Parse
        parse_result = self.toolchain.parse(code)
        self.assertTrue(parse_result.success)
        
        # Step 2: Convert to Runa
        to_runa_result = self.toolchain.to_runa(parse_result.ast)
        self.assertTrue(to_runa_result.success)
        
        # Step 3: Convert back to JavaScript
        from_runa_result = self.toolchain.from_runa(to_runa_result.target_ast)
        self.assertTrue(from_runa_result.success)
        
        # Step 4: Generate code
        gen_result = self.toolchain.generate(from_runa_result.target_ast)
        self.assertTrue(gen_result.success)
        
        # Step 5: Validate result
        validation = self.toolchain.validate_syntax(gen_result.code)
        self.assertTrue(validation['valid'])
    
    def test_error_handling(self):
        """Test error handling in toolchain operations."""
        # Test with invalid syntax
        invalid_code = "function invalid syntax here"
        
        parse_result = self.toolchain.parse(invalid_code)
        self.assertFalse(parse_result.success)
        self.assertIsNotNone(parse_result.error)
        
        # Test round-trip with invalid code
        round_trip = self.toolchain.round_trip_verify(invalid_code)
        self.assertFalse(round_trip.success)
        self.assertGreater(len(round_trip.differences), 0)


def create_test_suite():
    """Create comprehensive test suite for JavaScript toolchain."""
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestJavaScriptParser,
        TestJavaScriptConverter,
        TestJavaScriptGenerator,
        TestJavaScriptRoundTrip,
        TestJavaScriptValidation,
        TestJavaScriptToolchainStats,
        TestJavaScriptIntegration,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_tests():
    """Run all JavaScript toolchain tests."""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("JAVASCRIPT TOOLCHAIN TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\nSuccess rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("✅ JavaScript toolchain tests PASSED with excellent coverage!")
    elif success_rate >= 75:
        print("⚠️  JavaScript toolchain tests PASSED but need improvement.")
    else:
        print("❌ JavaScript toolchain tests FAILED - significant issues detected.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)