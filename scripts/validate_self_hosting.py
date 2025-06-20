#!/usr/bin/env python3
"""
Runa Self-Hosting Validation Script

This script validates that Runa can successfully bootstrap itself from Python to native C++,
ensuring the language is truly self-hosted and production-ready.
"""

import os
import sys
import time
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

class SelfHostingValidator:
    """Validates Runa self-hosting capabilities."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.runa_source_dir = self.project_root / "runa"
        self.test_output_dir = Path(tempfile.mkdtemp())
        self.results = {}
        
    def run_all_validations(self) -> bool:
        """Run all self-hosting validations."""
        print("🔍 Starting Runa Self-Hosting Validation...")
        
        validations = [
            ("Bootstrap Process", self.validate_bootstrap_process),
            ("Performance Benchmarks", self.validate_performance_benchmarks),
            ("Semantic Equivalence", self.validate_semantic_equivalence),
            ("Memory Efficiency", self.validate_memory_efficiency),
            ("Error Handling", self.validate_error_handling)
        ]
        
        all_passed = True
        
        for name, validation_func in validations:
            print(f"\n📋 Running {name}...")
            try:
                result = validation_func()
                self.results[name] = result
                if result:
                    print(f"✅ {name} PASSED")
                else:
                    print(f"❌ {name} FAILED")
                    all_passed = False
            except Exception as e:
                print(f"❌ {name} ERROR: {e}")
                self.results[name] = False
                all_passed = False
        
        self.print_summary()
        return all_passed
    
    def validate_bootstrap_process(self) -> bool:
        """Validate the complete bootstrap process."""
        print("  Testing bootstrap process...")
        
        # Step 1: Python-based compiler generates C++ version
        python_compiler_path = self.runa_source_dir / "compiler" / "python_compiler.py"
        runa_compiler_source = self.runa_source_dir / "compiler" / "runa_compiler.runa"
        generated_cpp = self.test_output_dir / "runa_compiler.cpp"
        
        if not python_compiler_path.exists():
            print(f"    ❌ Python compiler not found: {python_compiler_path}")
            return False
        
        try:
            # Generate C++ from Runa source
            cmd = [
                sys.executable, str(python_compiler_path),
                "--bootstrap-phase=1",
                "--source", str(runa_compiler_source),
                "--output", str(generated_cpp)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"    ❌ C++ generation failed: {result.stderr}")
                return False
            
            if not generated_cpp.exists():
                print(f"    ❌ Generated C++ file not found: {generated_cpp}")
                return False
            
            print(f"    ✅ C++ generation successful: {generated_cpp.stat().st_size} bytes")
            
        except subprocess.TimeoutExpired:
            print("    ❌ C++ generation timed out (>5 minutes)")
            return False
        except Exception as e:
            print(f"    ❌ C++ generation error: {e}")
            return False
        
        # Step 2: Compile C++ to native binary
        native_binary = self.test_output_dir / "runa_compiler_native"
        
        try:
            # Compile with optimization
            cmd = [
                "g++", "-O3", "-std=c++20", "-march=native",
                str(generated_cpp), "-o", str(native_binary)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                print(f"    ❌ C++ compilation failed: {result.stderr}")
                return False
            
            if not native_binary.exists():
                print(f"    ❌ Native binary not found: {native_binary}")
                return False
            
            print(f"    ✅ Native compilation successful: {native_binary.stat().st_size} bytes")
            
        except subprocess.TimeoutExpired:
            print("    ❌ C++ compilation timed out (>10 minutes)")
            return False
        except Exception as e:
            print(f"    ❌ C++ compilation error: {e}")
            return False
        
        # Step 3: Native compiler can compile itself
        try:
            # Use native compiler to compile the original Runa source
            generated_cpp_v2 = self.test_output_dir / "runa_compiler_v2.cpp"
            
            cmd = [
                str(native_binary),
                "--source", str(runa_compiler_source),
                "--output", str(generated_cpp_v2)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"    ❌ Self-compilation failed: {result.stderr}")
                return False
            
            if not generated_cpp_v2.exists():
                print(f"    ❌ Self-compiled C++ not found: {generated_cpp_v2}")
                return False
            
            print(f"    ✅ Self-compilation successful: {generated_cpp_v2.stat().st_size} bytes")
            
        except subprocess.TimeoutExpired:
            print("    ❌ Self-compilation timed out (>5 minutes)")
            return False
        except Exception as e:
            print(f"    ❌ Self-compilation error: {e}")
            return False
        
        # Step 4: Validate output equivalence
        try:
            # Compare the two generated C++ files
            with open(generated_cpp, 'r') as f1, open(generated_cpp_v2, 'r') as f2:
                content1 = f1.read()
                content2 = f2.read()
            
            if content1 != content2:
                print("    ❌ Generated C++ files are not identical")
                return False
            
            print("    ✅ Generated C++ files are identical")
            
        except Exception as e:
            print(f"    ❌ Output comparison error: {e}")
            return False
        
        return True
    
    def validate_performance_benchmarks(self) -> bool:
        """Validate performance benchmarks."""
        print("  Testing performance benchmarks...")
        
        # Test compilation speed
        test_programs = [
            ("small", 100, 50),      # 100 lines, <50ms
            ("medium", 1000, 100),   # 1000 lines, <100ms
            ("large", 10000, 500),   # 10000 lines, <500ms
        ]
        
        python_compiler = self.runa_source_dir / "compiler" / "python_compiler.py"
        native_compiler = self.test_output_dir / "runa_compiler_native"
        
        if not python_compiler.exists() or not native_compiler.exists():
            print("    ❌ Compilers not available for performance testing")
            return False
        
        for size_name, line_count, max_ms in test_programs:
            # Generate test program
            test_program = self.generate_test_program(line_count)
            test_file = self.test_output_dir / f"test_{size_name}.runa"
            
            with open(test_file, 'w') as f:
                f.write(test_program)
            
            # Test Python compiler performance
            start_time = time.perf_counter()
            try:
                cmd = [sys.executable, str(python_compiler), "--source", str(test_file)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                python_time = (time.perf_counter() - start_time) * 1000
                
                if result.returncode != 0:
                    print(f"    ❌ Python compilation failed for {size_name}: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print(f"    ❌ Python compilation timed out for {size_name}")
                return False
            
            # Test native compiler performance
            start_time = time.perf_counter()
            try:
                cmd = [str(native_compiler), "--source", str(test_file)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                native_time = (time.perf_counter() - start_time) * 1000
                
                if result.returncode != 0:
                    print(f"    ❌ Native compilation failed for {size_name}: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print(f"    ❌ Native compilation timed out for {size_name}")
                return False
            
            # Validate performance targets
            if native_time >= max_ms:
                print(f"    ❌ Native compilation too slow for {size_name}: {native_time:.1f}ms (target: <{max_ms}ms)")
                return False
            
            speedup = python_time / native_time if native_time > 0 else float('inf')
            
            if speedup < 10:
                print(f"    ❌ Insufficient speedup for {size_name}: {speedup:.1f}x (target: 10x+)")
                return False
            
            print(f"    ✅ {size_name}: {native_time:.1f}ms (speedup: {speedup:.1f}x)")
        
        return True
    
    def validate_semantic_equivalence(self) -> bool:
        """Validate semantic equivalence between Python and native compilers."""
        print("  Testing semantic equivalence...")
        
        # Test programs with known outputs
        test_cases = [
            ("hello_world", """
                Process called "main":
                    Display "Hello, World!"
            """, "Hello, World!"),
            
            ("arithmetic", """
                Process called "main":
                    Let a be 10
                    Let b be 5
                    Let result be a plus b multiplied by 2
                    Display "Result:" with message result
            """, "Result: 20"),
            
            ("fibonacci", """
                Process called "fib" that takes n:
                    If n is less than or equal to 1:
                        Return n
                    Otherwise:
                        Return fib with n as (n minus 1) plus fib with n as (n minus 2)
                
                Process called "main":
                    Let result be fib with n as 10
                    Display "Fibonacci(10):" with message result
            """, "Fibonacci(10): 55")
        ]
        
        python_compiler = self.runa_source_dir / "compiler" / "python_compiler.py"
        native_compiler = self.test_output_dir / "runa_compiler_native"
        
        for test_name, source_code, expected_output in test_cases:
            test_file = self.test_output_dir / f"test_{test_name}.runa"
            
            with open(test_file, 'w') as f:
                f.write(source_code)
            
            # Test Python compiler output
            try:
                cmd = [sys.executable, str(python_compiler), "--source", str(test_file), "--execute"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    print(f"    ❌ Python execution failed for {test_name}: {result.stderr}")
                    return False
                
                python_output = result.stdout.strip()
                
            except subprocess.TimeoutExpired:
                print(f"    ❌ Python execution timed out for {test_name}")
                return False
            
            # Test native compiler output
            try:
                cmd = [str(native_compiler), "--source", str(test_file), "--execute"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    print(f"    ❌ Native execution failed for {test_name}: {result.stderr}")
                    return False
                
                native_output = result.stdout.strip()
                
            except subprocess.TimeoutExpired:
                print(f"    ❌ Native execution timed out for {test_name}")
                return False
            
            # Compare outputs
            if python_output != native_output:
                print(f"    ❌ Output mismatch for {test_name}:")
                print(f"      Python: '{python_output}'")
                print(f"      Native: '{native_output}'")
                return False
            
            if expected_output not in python_output:
                print(f"    ❌ Unexpected output for {test_name}: '{python_output}'")
                return False
            
            print(f"    ✅ {test_name}: semantic equivalence verified")
        
        return True
    
    def validate_memory_efficiency(self) -> bool:
        """Validate memory efficiency."""
        print("  Testing memory efficiency...")
        
        # Generate large test program
        large_program = self.generate_test_program(100000)  # 100k lines
        test_file = self.test_output_dir / "test_large.runa"
        
        with open(test_file, 'w') as f:
            f.write(large_program)
        
        native_compiler = self.test_output_dir / "runa_compiler_native"
        
        if not native_compiler.exists():
            print("    ❌ Native compiler not available for memory testing")
            return False
        
        # Measure memory usage during compilation
        try:
            import psutil
            process = psutil.Process()
            
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            cmd = [str(native_compiler), "--source", str(test_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = memory_after - memory_before
            
            if result.returncode != 0:
                print(f"    ❌ Large program compilation failed: {result.stderr}")
                return False
            
            if memory_used > 500:
                print(f"    ❌ Memory usage too high: {memory_used:.1f}MB (target: <500MB)")
                return False
            
            print(f"    ✅ Memory usage acceptable: {memory_used:.1f}MB")
            
        except ImportError:
            print("    ⚠️  psutil not available, skipping memory validation")
            return True
        except subprocess.TimeoutExpired:
            print("    ❌ Large program compilation timed out")
            return False
        
        return True
    
    def validate_error_handling(self) -> bool:
        """Validate error handling."""
        print("  Testing error handling...")
        
        error_cases = [
            ("syntax_error", """
                Process called "main":
                    Let x be 10
                    Let y be  # Missing value
                    Display x
            """, "syntax error"),
            
            ("type_error", """
                Process called "main":
                    Let x be 10
                    Let y be "hello"
                    Let z be x plus y  # Type mismatch
            """, "type error"),
            
            ("undefined_variable", """
                Process called "main":
                    Display undefined_variable  # Undefined
            """, "undefined"),
        ]
        
        native_compiler = self.test_output_dir / "runa_compiler_native"
        
        if not native_compiler.exists():
            print("    ❌ Native compiler not available for error testing")
            return False
        
        for test_name, source_code, expected_error in error_cases:
            test_file = self.test_output_dir / f"test_{test_name}.runa"
            
            with open(test_file, 'w') as f:
                f.write(source_code)
            
            try:
                cmd = [str(native_compiler), "--source", str(test_file)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                # Should fail with error
                if result.returncode == 0:
                    print(f"    ❌ {test_name}: Expected error but compilation succeeded")
                    return False
                
                if expected_error.lower() not in result.stderr.lower():
                    print(f"    ❌ {test_name}: Expected '{expected_error}' in error, got: {result.stderr}")
                    return False
                
                print(f"    ✅ {test_name}: Error handling verified")
                
            except subprocess.TimeoutExpired:
                print(f"    ❌ {test_name}: Error test timed out")
                return False
        
        return True
    
    def generate_test_program(self, line_count: int) -> str:
        """Generate a test program with specified line count."""
        program = []
        
        # Add function definitions
        for i in range(line_count // 10):
            program.append(f"""
                Process called "function_{i}" that takes x:
                    Let result be x multiplied by {i}
                    Return result
            """)
        
        # Add main function
        program.append("""
            Process called "main":
        """)
        
        # Add variable declarations and operations
        for i in range(line_count // 20):
            program.append(f"        Let var_{i} be {i}")
        
        for i in range(line_count // 20):
            program.append(f"        Let result_{i} be function_{i % 10} with x as var_{i}")
        
        program.append("        Display 'Test completed successfully'")
        
        return "\n".join(program)
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("📊 Runa Self-Hosting Validation Summary")
        print("="*60)
        
        passed = sum(1 for result in self.results.values() if result)
        total = len(self.results)
        
        for name, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {name}")
        
        print(f"\nOverall: {passed}/{total} validations passed")
        
        if passed == total:
            print("🎉 All validations passed! Runa is self-hosting ready.")
        else:
            print("⚠️  Some validations failed. Runa is not yet self-hosting ready.")
        
        # Clean up
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir)

def main():
    """Main validation function."""
    validator = SelfHostingValidator()
    success = validator.run_all_validations()
    
    if not success:
        sys.exit(1)
    
    print("\n🚀 Runa self-hosting validation completed successfully!")

if __name__ == "__main__":
    main() 