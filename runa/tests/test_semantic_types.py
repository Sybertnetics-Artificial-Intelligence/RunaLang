import unittest, textwrap
from runa.compiler import parse_runa_source, analyze_semantics

class TestSemanticTypes(unittest.TestCase):
    def get_errors(self, src: str):
        program = parse_runa_source(textwrap.dedent(src).strip())
        return analyze_semantics(program)

    def test_list_type_mismatch(self):
        source = '''
        Let ints be list containing 1, 2, 3
        Set ints to list containing "a", "b"
        '''
        errs = [e.message for e in self.get_errors(source)]
        self.assertTrue(any("Type mismatch" in m for m in errs))

    def test_list_any_assignment(self):
        source = '''
        Let anylist be list containing 1, "a"
        Set anylist to list containing 2, 3, 4
        '''
        errs = self.get_errors(source)
        # Should be no mismatch (Any accepts Integer)
        self.assertEqual(len(errs), 0)

if __name__ == '__main__':
    unittest.main() 