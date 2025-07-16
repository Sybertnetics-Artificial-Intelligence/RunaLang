#!/usr/bin/env python3
"""
Validation script for the Runa Proof of Concept Test Framework
============================================================

This script validates that the test framework is properly set up and can
run basic validation tests.
"""

import sys
from pathlib import Path
import traceback

def validate_framework_setup():
    """Validate that the test framework is properly set up."""
    print("🔍 Validating Runa Proof of Concept Test Framework Setup")
    print("=" * 60)
    
    errors = []
    
    # Check directory structure
    print("📁 Checking directory structure...")
    required_dirs = ["outputs", "reports"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   ✅ {dir_name}/ exists")
        else:
            errors.append(f"Missing directory: {dir_name}")
            print(f"   ❌ {dir_name}/ missing")
    
    # Check for tier subdirectories in outputs
    tier_dirs = ["tier1", "tier2", "tier3", "tier4", "tier5", "tier6", "tier7"]
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        for tier in tier_dirs:
            tier_path = outputs_dir / tier
            if tier_path.exists():
                print(f"   ✅ outputs/{tier}/ exists")
            else:
                print(f"   ⚠️  outputs/{tier}/ will be created as needed")
    
    # Check required files
    print("\n📄 Checking required files...")
    required_files = [
        "test_framework.py",
        "test_runner.py", 
        "tier1_test_cases.py",
        "README.md",
        "__init__.py"
    ]
    
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"   ✅ {file_name} exists")
        else:
            errors.append(f"Missing file: {file_name}")
            print(f"   ❌ {file_name} missing")
    
    # Test imports
    print("\n🔧 Testing imports...")
    try:
        from test_framework import TestCase, TestComplexity, TestType, ProofOfConceptTestFramework
        print("   ✅ test_framework imports successful")
    except ImportError as e:
        errors.append(f"test_framework import failed: {e}")
        print(f"   ❌ test_framework import failed: {e}")
    
    try:
        from tier1_test_cases import get_tier1_test_cases
        print("   ✅ tier1_test_cases imports successful")
    except ImportError as e:
        errors.append(f"tier1_test_cases import failed: {e}")
        print(f"   ❌ tier1_test_cases import failed: {e}")
    
    # Test basic functionality
    print("\n🧪 Testing basic functionality...")
    try:
        from tier1_test_cases import get_tier1_test_cases
        test_cases = get_tier1_test_cases()
        print(f"   ✅ Loaded {len(test_cases)} test cases")
        
        # Check test case structure
        if test_cases:
            first_test = test_cases[0]
            required_attrs = ['name', 'description', 'complexity', 'test_type', 
                            'source_language', 'target_languages', 'source_code']
            for attr in required_attrs:
                if hasattr(first_test, attr):
                    print(f"   ✅ Test case has {attr}")
                else:
                    errors.append(f"Test case missing attribute: {attr}")
                    print(f"   ❌ Test case missing {attr}")
        
    except Exception as e:
        errors.append(f"Basic functionality test failed: {e}")
        print(f"   ❌ Basic functionality test failed: {e}")
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("❌ VALIDATION FAILED")
        print(f"Found {len(errors)} error(s):")
        for error in errors:
            print(f"   • {error}")
        return False
    else:
        print("✅ VALIDATION SUCCESSFUL")
        print("The Runa Proof of Concept Test Framework is ready to use!")
        print("\nNext steps:")
        print("   1. Run 'python test_runner.py --list' to see available tests")
        print("   2. Run 'python test_runner.py --test js_basic_hello_world' for a quick test")
        print("   3. Run 'python test_runner.py' to execute the full test battery")
        return True

def main():
    """Main entry point."""
    try:
        success = validate_framework_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Unexpected error during validation: {e}")
        traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    main()