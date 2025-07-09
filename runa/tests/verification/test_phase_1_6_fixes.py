import unittest
from textwrap import dedent
from runa.compiler import compile_runa_to_python
import subprocess
import tempfile
import os

class TestPhase16Fixes(unittest.TestCase):
    def _execute_python_code(self, python_code: str) -> str:
        """Execute Python code and return stdout."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(python_code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ['python', temp_file], 
                capture_output=True, text=True, check=True, timeout=10
            )
            return result.stdout.strip()
        finally:
            os.unlink(temp_file)

    def test_subtraction_logic(self):
        """Verify that 'A minus B' is compiled correctly."""
        runa_code = dedent('''
            Let A be 100
            Let B be 40
            Let result be A minus B
            Display result
        ''')
        python_code = compile_runa_to_python(runa_code)
        output = self._execute_python_code(python_code)
        self.assertEqual(output, "60")

if __name__ == '__main__':
    unittest.main() 