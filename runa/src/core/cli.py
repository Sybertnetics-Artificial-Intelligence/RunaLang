"""
Command-line interface for the Runa programming language.

This module provides a CLI for the Runa compiler and related tools.
"""

import argparse
import sys
from pathlib import Path

from runa.src.lexer.lexer import Lexer, RunaLexicalError
from runa.src.core import __version__


def tokenize_file(file_path: Path) -> None:
    """
    Tokenize a Runa source file and print the tokens.
    
    Args:
        file_path: Path to the source file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Print tokens
        for token in tokens:
            print(token)
            
    except RunaLexicalError as e:
        print(f"Lexical error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Entry point for the Runa CLI."""
    parser = argparse.ArgumentParser(
        description="Runa Programming Language - A natural language-like programming language."
    )
    
    parser.add_argument('--version', action='version', version=f'Runa {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Tokenize command
    tokenize_parser = subparsers.add_parser('tokenize', help='Tokenize a Runa source file')
    tokenize_parser.add_argument('file', type=Path, help='Path to the source file')
    
    # Run command (placeholder for now)
    run_parser = subparsers.add_parser('run', help='Run a Runa program')
    run_parser.add_argument('file', type=Path, help='Path to the source file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process commands
    if args.command == 'tokenize':
        tokenize_file(args.file)
    elif args.command == 'run':
        print("Run command not implemented yet")
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main() 