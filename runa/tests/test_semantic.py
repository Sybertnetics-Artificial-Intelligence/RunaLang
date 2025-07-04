import unittest
from runa.compiler import parse_runa_source, analyze_semantics, SemanticError
import textwrap

class TestSemanticAnalyzer(unittest.TestCase):

    def collect_errors(self, source: str):
        program = parse_runa_source(textwrap.dedent(source).strip())
        errors = analyze_semantics(program)
        return [e.message for e in errors]

    def test_duplicate_declaration(self):
        source = '''
        Let x be 1
        Let x be 2
        '''
        errors = self.collect_errors(source)
        self.assertTrue(any("Duplicate declaration" in msg for msg in errors))

    def test_undefined_identifier(self):
        source = '''
        Set y to 5
        '''
        errors = self.collect_errors(source)
        self.assertTrue(any("Undefined variable 'y'" in msg for msg in errors))

    def test_constant_reassignment(self):
        source = '''
        Define constant PI as 3.14
        Set PI to 3.14159
        '''
        errors = self.collect_errors(source)
        self.assertTrue(any("Cannot assign to constant" in msg for msg in errors))

    def test_type_mismatch(self):
        source = '''
        Let x be 5
        Set x to "hello"
        '''
        errors = self.collect_errors(source)
        self.assertTrue(any("Type mismatch" in msg for msg in errors))

    def test_valid_program(self):
        source = '''
        Let price be 100
        Let tax be 0.1
        Let total be price multiplied by (1 plus tax)
        '''
        errors = self.collect_errors(source)
        self.assertEqual(len(errors), 0)

if __name__ == '__main__':
    unittest.main() 