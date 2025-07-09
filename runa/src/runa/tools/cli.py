#!/usr/bin/env python3
"""
Runa Command Line Interface

Provides command-line tools for compiling, validating, and working with Runa code.
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional, List

from .compiler import (
    compile_runa_to_python, compile_runa_to_javascript, compile_runa_to_runa,
    parse_runa_source, compile_runa_to_ir
)
from .compiler.bidirectional_translator import (
    BidirectionalTranslator, SupportedLanguage, 
    create_bidirectional_translator
)


class RunaCLI:
    """Main CLI application for Runa."""
    
    def __init__(self):
        self.translator = create_bidirectional_translator()
    
    def compile_command(self, args):
        """Handle runa compile command."""
        try:
            # Read source file
            if not os.path.exists(args.input):
                print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
                return 1
            
            with open(args.input, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Determine target language
            target_lang = args.target.lower()
            
            # Compile to target language
            if target_lang == 'python':
                result = compile_runa_to_python(source_code)
                default_ext = '.py'
            elif target_lang == 'javascript':
                result = compile_runa_to_javascript(source_code)
                default_ext = '.js'
            elif target_lang == 'runa':
                result = compile_runa_to_runa(source_code)
                default_ext = '.runa'
            else:
                # Use bidirectional translator for other languages
                try:
                    target_enum = SupportedLanguage(target_lang)
                    translation = self.translator.translate_runa_to_any(source_code, target_enum)
                    if not translation.success:
                        print(f"Error: Translation failed: {'; '.join(translation.errors)}", file=sys.stderr)
                        return 1
                    result = translation.target_code
                    default_ext = self.translator.extensions.get(target_enum, '.txt')
                except ValueError:
                    print(f"Error: Unsupported target language '{target_lang}'", file=sys.stderr)
                    print(f"Supported languages: {', '.join([lang.value for lang in SupportedLanguage])}")
                    return 1
            
            # Determine output file
            if args.output:
                output_file = args.output
            else:
                # Generate output filename
                input_path = Path(args.input)
                output_file = input_path.with_suffix(default_ext)
            
            # Write result
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            if args.verbose:
                print(f"Successfully compiled '{args.input}' to '{output_file}' ({target_lang})")
            
            return 0
            
        except Exception as e:
            print(f"Error: Compilation failed: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def validate_command(self, args):
        """Handle runa validate command."""
        try:
            # Read source file
            if not os.path.exists(args.input):
                print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
                return 1
            
            with open(args.input, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            errors = []
            warnings = []
            
            # Lexical and syntactic validation
            try:
                ast = parse_runa_source(source_code)
                if args.verbose:
                    print(f"✅ Syntax validation passed ({len(ast.statements)} statements)")
            except Exception as e:
                errors.append(f"Syntax error: {e}")
            
            # Semantic validation (through IR compilation)
            if not errors:
                try:
                    ir_module = compile_runa_to_ir(source_code)
                    if args.verbose:
                        print(f"✅ Semantic validation passed ({len(ir_module.functions)} functions)")
                except Exception as e:
                    errors.append(f"Semantic error: {e}")
            
            # Round-trip validation
            if not errors and args.round_trip:
                try:
                    regenerated = compile_runa_to_runa(source_code)
                    # Try to parse the regenerated code
                    parse_runa_source(regenerated)
                    if args.verbose:
                        print("✅ Round-trip validation passed")
                except Exception as e:
                    warnings.append(f"Round-trip warning: {e}")
            
            # Output results
            if args.output:
                # JSON output
                result = {
                    "file": args.input,
                    "valid": len(errors) == 0,
                    "errors": errors,
                    "warnings": warnings
                }
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                if args.verbose:
                    print(f"Validation results written to '{args.output}'")
            else:
                # Console output
                if errors:
                    print(f"❌ Validation failed for '{args.input}':")
                    for error in errors:
                        print(f"  • {error}")
                    return 1
                else:
                    print(f"✅ Validation passed for '{args.input}'")
                    if warnings:
                        print("⚠️  Warnings:")
                        for warning in warnings:
                            print(f"  • {warning}")
            
            return 0 if not errors else 1
            
        except Exception as e:
            print(f"Error: Validation failed: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def info_command(self, args):
        """Handle runa info command."""
        print("🌟 Runa Programming Language")
        print("Natural language programming for AI-to-AI communication")
        print()
        print("📋 Supported Features:")
        print("  • Natural language syntax")
        print("  • Self-hosting compilation")
        print("  • Bidirectional translation")
        print("  • Multiple target languages")
        print()
        print("🎯 Supported Target Languages:")
        for lang in SupportedLanguage:
            available = "✅" if lang in self.translator.generators else "🔄"
            print(f"  {available} {lang.value}")
        print()
        print("🔧 Available Commands:")
        print("  • runa compile <file> --target <language>")
        print("  • runa validate <file>")
        print("  • runa info")
        return 0
    
    def run(self, argv: Optional[List[str]] = None):
        """Main entry point for CLI."""
        parser = argparse.ArgumentParser(
            prog='runa',
            description='Runa Programming Language CLI',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  runa compile hello.runa --target python
  runa compile calculator.runa --target javascript -o calc.js
  runa validate my_program.runa --round-trip
  runa info
            """
        )
        
        parser.add_argument('--version', action='version', version='Runa 0.1.0')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Compile command
        compile_parser = subparsers.add_parser('compile', help='Compile Runa source code')
        compile_parser.add_argument('input', help='Input Runa source file')
        compile_parser.add_argument('-t', '--target', required=True,
                                   help='Target language (python, javascript, runa, etc.)')
        compile_parser.add_argument('-o', '--output', help='Output file (optional)')
        compile_parser.set_defaults(func=self.compile_command)
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate Runa source code')
        validate_parser.add_argument('input', help='Input Runa source file')
        validate_parser.add_argument('-o', '--output', help='Output JSON results to file')
        validate_parser.add_argument('--round-trip', action='store_true',
                                    help='Test round-trip compilation')
        validate_parser.set_defaults(func=self.validate_command)
        
        # Info command
        info_parser = subparsers.add_parser('info', help='Show Runa information')
        info_parser.set_defaults(func=self.info_command)
        
        # Parse arguments
        args = parser.parse_args(argv)
        
        if not args.command:
            parser.print_help()
            return 1
        
        # Execute command
        return args.func(args)


def main():
    """Entry point for the runa command."""
    cli = RunaCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()