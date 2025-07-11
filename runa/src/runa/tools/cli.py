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

# Import from new architecture
from ..languages.runa.runa_parser import RunaParser
from ..core.pipeline import TranslationPipeline, TranslationResult
from ..languages.shared.base_toolchain import ToolchainResult
import importlib
import os
import json
from pathlib import Path


class RunaCLI:
    """Main CLI application for Runa."""
    
    def __init__(self):
        self.parser = RunaParser()
        self.toolchains = {}
        self.supported_languages = {}
        self._discover_languages()
        self._init_toolchains()
    
    def _discover_languages(self):
        """Dynamically discover all supported languages from tier directories."""
        try:
            languages_path = Path(__file__).parent.parent / "languages"
            
            # Language tier mapping with extensions and priorities
            tier_info = {
                'tier1': {'priority': 1, 'category': 'Core Programming Languages'},
                'tier2': {'priority': 2, 'category': 'Modern Languages'}, 
                'tier3': {'priority': 3, 'category': 'Configuration/Markup'},
                'tier4': {'priority': 4, 'category': 'Specialized Languages'},
                'tier5': {'priority': 5, 'category': 'System/Functional Languages'},
                'tier6': {'priority': 6, 'category': 'Legacy/Enterprise Languages'}
            }
            
            # File extension and toolchain name mappings
            extension_map = {
                'python': 'py', 'javascript': 'js', 'typescript': 'ts', 'cpp': 'cpp',
                'csharp': 'cs', 'java': 'java', 'sql': 'sql', 'go': 'go', 'rust': 'rs',
                'php': 'php', 'swift': 'swift', 'kotlin': 'kt', 'r': 'r', 'julia': 'jl',
                'matlab': 'm', 'solidity': 'sol', 'haskell': 'hs', 'erlang': 'erl',
                'elixir': 'ex', 'lisp': 'lisp', 'assembly': 'asm', 'cobol': 'cob',
                'fortran': 'f90', 'ada': 'ada', 'perl': 'pl', 'html': 'html',
                'css': 'css', 'xml': 'xml', 'yaml': 'yml', 'json': 'json',
                'shell': 'sh', 'webassembly': 'wasm', 'graphql': 'graphql',
                'hcl': 'hcl', 'llvm_ir': 'll', 'objective_c': 'm', 'visual_basic': 'vb',
                # Tier 4 Blockchain Languages
                'vyper': 'vy', 'move': 'move', 'michelson': 'mich', 'scilla': 'scilla',
                'smartpy': 'py', 'ligo': 'ligo', 'plutus': 'hs', 'pact': 'pact', 'scrypto': 'rs'
            }
            
            # Toolchain filename mappings (for abbreviated names)
            toolchain_name_map = {
                'python': 'py', 'javascript': 'js', 'typescript': 'ts',
                'csharp': 'csharp', 'cpp': 'cpp', 'java': 'java', 'sql': 'sql'
            }
            
            for tier_name, tier_data in tier_info.items():
                tier_path = languages_path / tier_name
                if tier_path.exists():
                    for lang_dir in tier_path.iterdir():
                        if lang_dir.is_dir() and lang_dir.name != '__pycache__':
                            lang_name = lang_dir.name
                            
                            # Check if toolchain exists (handle abbreviated names)
                            toolchain_prefix = toolchain_name_map.get(lang_name, lang_name)
                            toolchain_file = lang_dir / f"{toolchain_prefix}_toolchain.py"
                            extension = extension_map.get(lang_name, lang_name.lower())
                            
                            self.supported_languages[lang_name] = {
                                'tier': tier_name,
                                'priority': tier_data['priority'],
                                'category': tier_data['category'],
                                'extension': extension,
                                'has_toolchain': toolchain_file.exists(),
                                'module_path': f"runa.languages.{tier_name}.{lang_name}"
                            }
            
            # Add special case for Runa round-trip
            self.supported_languages['runa'] = {
                'tier': 'core',
                'priority': 0,
                'category': 'Runa Language',
                'extension': 'runa',
                'has_toolchain': True,
                'module_path': 'runa.languages.runa'
            }
            
            if self.supported_languages:
                print(f"🌍 Discovered {len(self.supported_languages)} supported languages")
            
        except Exception as e:
            print(f"Warning: Language discovery failed: {e}")
            # Fallback to minimal set
            self.supported_languages = {
                'python': {'tier': 'tier1', 'priority': 1, 'category': 'Core', 'extension': 'py', 'has_toolchain': True},
                'javascript': {'tier': 'tier1', 'priority': 1, 'category': 'Core', 'extension': 'js', 'has_toolchain': True},
                'runa': {'tier': 'core', 'priority': 0, 'category': 'Runa', 'extension': 'runa', 'has_toolchain': True}
            }

    def _init_toolchains(self):
        """Initialize toolchains for languages that have them."""
        for lang_name, lang_info in self.supported_languages.items():
            if lang_info['has_toolchain'] and lang_name != 'runa':
                try:
                    if lang_name in ['python', 'javascript', 'typescript']:  # Known working toolchains
                        toolchain_class = self._load_toolchain_class(lang_name, lang_info)
                        if toolchain_class:
                            self.toolchains[lang_name] = toolchain_class()
                except Exception as e:
                    print(f"Warning: Failed to initialize {lang_name} toolchain: {e}")

    def _load_toolchain_class(self, lang_name: str, lang_info: dict):
        """Dynamically load toolchain class for a language."""
        try:
            # Known working toolchains with specific imports
            if lang_name == 'python':
                from ..languages.tier1.python.py_toolchain import PythonToolchain
                return PythonToolchain
            elif lang_name == 'javascript':
                from ..languages.tier1.javascript.js_toolchain import JavaScriptToolchain
                return JavaScriptToolchain
            elif lang_name == 'typescript':
                from ..languages.tier1.typescript.ts_toolchain import TypeScriptToolchain
                return TypeScriptToolchain
            else:
                # Dynamic loading for other languages
                toolchain_prefix = {
                    'python': 'py', 'javascript': 'js', 'typescript': 'ts',
                    'csharp': 'csharp', 'cpp': 'cpp', 'java': 'java', 'sql': 'sql'
                }.get(lang_name, lang_name)
                
                module_path = f"..languages.{lang_info['tier']}.{lang_name}.{toolchain_prefix}_toolchain"
                toolchain_class_name = f"{lang_name.title()}Toolchain"
                
                try:
                    module = importlib.import_module(module_path, package=__package__)
                    return getattr(module, toolchain_class_name)
                except (ImportError, AttributeError):
                    return None
                    
        except Exception as e:
            print(f"Warning: Could not load {lang_name} toolchain: {e}")
            return None

    def _get_toolchain(self, language: str):
        """Get toolchain for specified language."""
        if language not in self.toolchains:
            lang_info = self.supported_languages.get(language)
            if lang_info and lang_info['has_toolchain']:
                toolchain_class = self._load_toolchain_class(language, lang_info)
                if toolchain_class:
                    self.toolchains[language] = toolchain_class()
        return self.toolchains.get(language)
    
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
            if target_lang not in self.supported_languages:
                print(f"Error: Unsupported target language '{target_lang}'", file=sys.stderr)
                available_langs = [lang for lang, info in self.supported_languages.items() 
                                 if info['has_toolchain'] or lang == 'runa']
                print(f"Available languages: {', '.join(sorted(available_langs))}")
                return 1
            
            lang_info = self.supported_languages[target_lang]
            
            # Check if toolchain is available
            if not lang_info['has_toolchain'] and target_lang != 'runa':
                print(f"Error: {target_lang} toolchain not yet implemented", file=sys.stderr)
                return 1
            
            # Parse Runa source
            try:
                runa_ast = self.parser.parse(source_code, file_path or "")
            except Exception as e:
                print(f"Error: Parse failed: {e}", file=sys.stderr)
                return 1
            extension = lang_info['extension']
            
            if target_lang == 'runa':
                # Round-trip generation
                try:
                    from ..languages.runa.runa_generator import RunaGenerator
                    generator = RunaGenerator()
                    result = generator.generate(runa_ast)
                except Exception as e:
                    print(f"Error: Runa generation failed: {e}", file=sys.stderr)
                    return 1
            else:
                # Use toolchain for target language
                toolchain = self._get_toolchain(target_lang)
                if not toolchain:
                    print(f"Error: Could not load {target_lang} toolchain", file=sys.stderr)
                    return 1
                
                # Convert Runa AST to target language AST
                try:
                    from_runa_result = toolchain.from_runa(runa_ast)
                    if not from_runa_result.success:
                        print(f"Error: Conversion from Runa failed: {from_runa_result.error_message}", file=sys.stderr)
                        return 1
                    
                    target_ast = from_runa_result.target_ast
                    
                    # Generate target language code
                    gen_result = toolchain.generate(target_ast)
                    if not gen_result.success:
                        print(f"Error: Generation failed: {gen_result.error}", file=sys.stderr)
                        return 1
                    result = gen_result.data
                except Exception as e:
                    print(f"Error: Translation failed: {e}", file=sys.stderr)
                    return 1
            
            default_ext = f'.{extension}'
            
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
                ast = self.parser.parse(source_code, args.input)
                if args.verbose:
                    print(f"✅ Syntax validation passed ({len(ast.statements)} statements)")
            except Exception as e:
                errors.append(f"Syntax error: {e}")
            
            # Semantic validation (basic check)
            if not errors:
                try:
                    from ..core.semantic import SemanticAnalyzer
                    analyzer = SemanticAnalyzer()
                    analyzer.analyze(ast)
                    if args.verbose:
                        print("✅ Semantic validation passed")
                except Exception as e:
                    errors.append(f"Semantic error: {e}")
            
            # Round-trip validation
            if not errors and args.round_trip:
                try:
                    from ..languages.runa.runa_generator import RunaGenerator
                    generator = RunaGenerator()
                    regenerated = generator.generate(ast)
                    # Try to parse the regenerated code
                    try:
                        regenerated_ast = self.parser.parse(regenerated, "")
                        if args.verbose:
                            print("✅ Round-trip validation passed")
                    except Exception as parse_error:
                        warnings.append(f"Round-trip warning: {parse_error}")
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
        
        # Group by tier for better organization
        by_tier = {}
        for lang_name, lang_info in self.supported_languages.items():
            tier = lang_info['tier']
            if tier not in by_tier:
                by_tier[tier] = []
            by_tier[tier].append((lang_name, lang_info))
        
        # Sort tiers by priority
        for tier in sorted(by_tier.keys(), key=lambda t: by_tier[t][0][1]['priority']):
            tier_langs = by_tier[tier]
            category = tier_langs[0][1]['category']
            print(f"\n  📁 {category}:")
            
            for lang_name, lang_info in sorted(tier_langs):
                status = "✅" if lang_info['has_toolchain'] else "🔄"
                ext = lang_info['extension']
                print(f"    {status} {lang_name} (.{ext})")
        
        print(f"\n  📊 Total: {len(self.supported_languages)} languages")
        implemented = sum(1 for info in self.supported_languages.values() if info['has_toolchain'])
        print(f"  🚀 Implemented: {implemented}")
        print(f"  🔄 In Development: {len(self.supported_languages) - implemented}")
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