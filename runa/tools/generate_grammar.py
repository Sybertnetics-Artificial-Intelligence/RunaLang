#!/usr/bin/env python3
"""
Generate the EBNF grammar file for the Runa language.

This script generates a formal EBNF grammar specification for the Runa language
based on the grammar defined in the grammar module.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the Runa modules
sys.path.append(str(Path(__file__).parent.parent))

from runa.src.parser.grammar import export_grammar_to_file


def main():
    """Generate the EBNF grammar file."""
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Calculate the path to the output file
    output_dir = script_dir.parent / "docs" / "grammar"
    output_file = output_dir / "RunaGrammar.ebnf"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate the grammar file
    export_grammar_to_file(str(output_file))
    
    print(f"Generated EBNF grammar file: {output_file}")


if __name__ == "__main__":
    main() 