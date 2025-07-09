import unittest, textwrap
from runa.compiler import parse_runa_source
from runa.compiler.ast_nodes import WhileLoop, ForEachLoop, ForRangeLoop

class TestParserLoops(unittest.TestCase):
    def parse(self, src: str):
        return parse_runa_source(textwrap.dedent(src).strip())

    def test_while_loop(self):
        src = '''
        While x is less than 10:
            Set x to x plus 1
        '''
        prog = self.parse(src)
        self.assertIsInstance(prog.statements[0], WhileLoop)

    def test_for_each_loop(self):
        src = '''
        For each item in items:
            Display item
        '''
        prog = self.parse(src)
        self.assertIsInstance(prog.statements[0], ForEachLoop)
        self.assertEqual(prog.statements[0].variable, 'item')

    def test_for_range_loop(self):
        src = '''
        For i from 1 to 5:
            Display i
        '''
        prog = self.parse(src)
        self.assertIsInstance(prog.statements[0], ForRangeLoop)
        self.assertEqual(prog.statements[0].variable, 'i')

if __name__ == '__main__':
    unittest.main() 