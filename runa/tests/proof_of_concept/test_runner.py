"""
Runa Proof of Concept Test Runner
=================================

This module handles the actual execution of test cases through the Runa pipeline.
It manages language toolchain registration, pipeline orchestration, and handles
the user-provided test cases through the complete translation workflow.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import logging

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

try:
    # Import the test framework and test cases
    from test_framework import (
        TestCase, TestComplexity, TestType, 
        ProofOfConceptTestFramework, accept_user_test_cases
    )
    
    # Import the user-provided test cases
    from tier1_test_cases import get_tier1_test_cases
    
    print("✅ Successfully imported test framework and test cases")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure test_framework.py and tier1_test_cases.py are in the same directory")
    sys.exit(1)


def run_tier1_tests():
    """Run all Tier 1 language tests."""
    print("🚀 Running Tier 1 Language Test Battery")
    print("="*60)
    
    # Get test cases
    test_cases = get_tier1_test_cases()
    print(f"Loaded {len(test_cases)} test cases")
    
    # Execute tests
    executions = accept_user_test_cases(test_cases)
    
    print(f"\n✅ Test execution completed. {len(executions)} tests run.")
    return executions


def run_specific_test(test_name: str):
    """Run a specific test by name."""
    test_cases = get_tier1_test_cases()
    
    matching_tests = [tc for tc in test_cases if tc.name == test_name]
    if not matching_tests:
        print(f"❌ Test '{test_name}' not found")
        print("Available tests:")
        for tc in test_cases:
            print(f"  - {tc.name}")
        return
    
    print(f"🔄 Running specific test: {test_name}")
    executions = accept_user_test_cases(matching_tests)
    print(f"✅ Test '{test_name}' completed")
    return executions


def run_tests_by_complexity(complexity: str):
    """Run tests filtered by complexity level."""
    try:
        complexity_enum = TestComplexity(complexity.lower())
    except ValueError:
        print(f"❌ Invalid complexity: {complexity}")
        print("Valid complexities: basic, intermediate, advanced, extreme, breaking")
        return
    
    test_cases = get_tier1_test_cases()
    filtered_tests = [tc for tc in test_cases if tc.complexity == complexity_enum]
    
    if not filtered_tests:
        print(f"❌ No tests found for complexity: {complexity}")
        return
    
    print(f"🔄 Running {len(filtered_tests)} tests with complexity: {complexity}")
    executions = accept_user_test_cases(filtered_tests)
    print(f"✅ Complexity '{complexity}' tests completed")
    return executions


def run_tests_by_language(language: str):
    """Run tests filtered by source language."""
    test_cases = get_tier1_test_cases()
    filtered_tests = [tc for tc in test_cases if tc.source_language == language.lower()]
    
    if not filtered_tests:
        print(f"❌ No tests found for language: {language}")
        available_langs = sorted(set(tc.source_language for tc in test_cases))
        print("Available languages:")
        for lang in available_langs:
            print(f"  - {lang}")
        return
    
    print(f"🔄 Running {len(filtered_tests)} tests for language: {language}")
    executions = accept_user_test_cases(filtered_tests)
    print(f"✅ Language '{language}' tests completed")
    return executions


def list_available_tests():
    """List all available test cases."""
    test_cases = get_tier1_test_cases()
    
    print("📋 Available Test Cases")
    print("="*60)
    
    # Group by source language
    by_language = {}
    for tc in test_cases:
        by_language.setdefault(tc.source_language, []).append(tc)
    
    for language, tests in sorted(by_language.items()):
        print(f"\n🔸 {language.upper()} ({len(tests)} tests):")
        for tc in tests:
            print(f"  • {tc.name} ({tc.complexity.value}) - {tc.description}")
    
    print(f"\nTotal: {len(test_cases)} test cases")


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Runa Proof of Concept Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py                           # Run all Tier 1 tests
  python test_runner.py --list                    # List available tests
  python test_runner.py --test js_basic_hello_world   # Run specific test
  python test_runner.py --complexity basic        # Run basic complexity tests
  python test_runner.py --language python         # Run all Python tests
        """
    )
    
    parser.add_argument('--list', action='store_true', 
                       help='List all available test cases')
    parser.add_argument('--test', type=str,
                       help='Run a specific test by name')
    parser.add_argument('--complexity', type=str,
                       choices=['basic', 'intermediate', 'advanced', 'extreme', 'breaking'],
                       help='Run tests of specific complexity level')
    parser.add_argument('--language', type=str,
                       help='Run tests for specific source language')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Execute based on arguments
    if args.list:
        list_available_tests()
    elif args.test:
        run_specific_test(args.test)
    elif args.complexity:
        run_tests_by_complexity(args.complexity)
    elif args.language:
        run_tests_by_language(args.language)
    else:
        # Run all tests
        run_tier1_tests()


if __name__ == "__main__":
    main()