#!/usr/bin/env python3
"""
Command-line interface for the Runa programming language.

This module provides the CLI entry point for the Runa compiler and REPL.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

from runa.src.compiler import Compiler, CompilationResult


def setup_logger():
    """Set up the logger for the Runa compiler."""
    logger = logging.getLogger("runa")
    logger.setLevel(logging.INFO)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Add formatter
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def print_error_details(result: CompilationResult):
    """
    Print detailed error information from a compilation result.
    
    Args:
        result: The compilation result to print errors from
    """
    if result.lexer_errors:
        print("\nLexical errors:")
        for i, error in enumerate(result.lexer_errors, 1):
            print(f"  {i}. {error}")
    
    if result.parser_errors:
        print("\nSyntax errors:")
        for i, error in enumerate(result.parser_errors, 1):
            print(f"  {i}. {error}")
    
    if result.semantic_errors:
        print("\nSemantic errors:")
        for i, error in enumerate(result.semantic_errors, 1):
            print(f"  {i}. {error}")


def handle_compile(args):
    """
    Handle the 'compile' command.
    
    Args:
        args: The parsed command-line arguments
    """
    compiler = Compiler()
    
    for file_path in args.files:
        print(f"Compiling {file_path}...")
        result = compiler.compile_file(file_path)
        
        if result.success:
            print(f"✅ Successfully compiled {file_path}")
            if args.verbose:
                print(f"  AST has {len(result.program.statements)} statements")
        else:
            print(f"❌ Failed to compile {file_path} with {result.error_count()} errors")
            if args.verbose or args.show_errors:
                print_error_details(result)


def handle_run(args):
    """
    Handle the 'run' command.
    
    Args:
        args: The parsed command-line arguments
    """
    # For now, we can only compile (not run), so delegate to compile
    print("Note: Direct execution is not yet implemented. Compiling only...")
    handle_compile(args)


def handle_repl(args):
    """
    Handle the 'repl' command (interactive mode).
    
    Args:
        args: The parsed command-line arguments
    """
    print("Runa REPL v0.1.0")
    print("Type 'exit' or 'quit' to exit, 'help' for help.")
    
    compiler = Compiler()
    
    while True:
        try:
            user_input = input(">>> ")
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if user_input.lower() == "help":
                print("Available commands:")
                print("  exit, quit - Exit the REPL")
                print("  help       - Show this help message")
                continue
            
            # Compile and evaluate the input
            result = compiler.compile_string(user_input)
            
            if result.success:
                print("✅ Compiled successfully")
                # In the future, we would evaluate the program here
            else:
                print("❌ Compilation failed")
                print_error_details(result)
        
        except KeyboardInterrupt:
            print("\nKeyboard interrupt")
            break
        
        except EOFError:
            print("\nEOF")
            break
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def main():
    """Entry point for the Runa CLI."""
    # Set up logging
    logger = setup_logger()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Runa programming language compiler and interpreter"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="Runa v0.1.0"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="valid commands",
        help="command help"
    )
    
    # Compile command
    compile_parser = subparsers.add_parser(
        "compile", 
        help="compile Runa source files"
    )
    compile_parser.add_argument(
        "files", 
        nargs="+", 
        help="source files to compile"
    )
    compile_parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="verbose output"
    )
    compile_parser.add_argument(
        "-e", "--show-errors", 
        action="store_true", 
        help="show detailed error information"
    )
    
    # Run command
    run_parser = subparsers.add_parser(
        "run", 
        help="run Runa programs"
    )
    run_parser.add_argument(
        "files", 
        nargs="+", 
        help="source files to run"
    )
    run_parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="verbose output"
    )
    run_parser.add_argument(
        "-e", "--show-errors", 
        action="store_true", 
        help="show detailed error information"
    )
    
    # REPL command
    repl_parser = subparsers.add_parser(
        "repl", 
        help="start interactive REPL"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle command
    if args.command == "compile":
        handle_compile(args)
    elif args.command == "run":
        handle_run(args)
    elif args.command == "repl":
        handle_repl(args)
    else:
        # Default to REPL if no command is specified
        handle_repl(args)


if __name__ == "__main__":
    main() 