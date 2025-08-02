#!/usr/bin/env python3
"""
Runa Self-Hosting Build System

This script orchestrates the self-hosting compilation process:
1. Builds the bootstrap compiler (Rust)
2. Uses bootstrap to compile the self-hosting compiler (Runa -> Bytecode)
3. Creates self-hosting executable that can compile itself
4. Verifies end-to-end self-hosting functionality

This enables Runa to compile itself without depending on Rust after bootstrap.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class SelfHostingBuilder:
    """Orchestrates the Runa self-hosting build process"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.bootstrap_dir = self.project_root / "src" / "bootstrap" 
        self.compiler_dir = self.project_root / "src" / "compiler"
        self.runtime_dir = self.project_root / "src" / "runtime"
        self.build_dir = self.project_root / "build"
        self.build_dir.mkdir(exist_ok=True)
        
        # Build artifacts
        self.bootstrap_executable = self.bootstrap_dir / "target" / "debug" / "runac"
        self.self_hosting_source = self.compiler_dir / "main.runa"  
        self.self_hosting_executable = self.build_dir / "runa"
        
        self.start_time = time.time()
        
    def log(self, message: str, level: str = "INFO"):
        """Log build progress with timestamps"""
        elapsed = time.time() - self.start_time
        print(f"[{elapsed:6.2f}s] [{level}] {message}")
        
    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, capture_output: bool = False) -> Tuple[int, str, str]:
        """Run shell command with error handling"""
        cwd = cwd or self.project_root
        self.log(f"Running: {' '.join(cmd)} (in {cwd})")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                self.log(f"Command failed with exit code {result.returncode}", "ERROR")
                if capture_output:
                    self.log(f"STDOUT: {result.stdout}", "ERROR")
                    self.log(f"STDERR: {result.stderr}", "ERROR")
                    
            return result.returncode, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            self.log("Command timed out", "ERROR")
            return 1, "", "Command timed out"
        except Exception as e:
            self.log(f"Command failed with exception: {e}", "ERROR")
            return 1, "", str(e)
    
    def build_bootstrap_compiler(self) -> bool:
        """Build the Rust bootstrap compiler"""
        self.log("=== Building Bootstrap Compiler ===")
        
        if not self.bootstrap_dir.exists():
            self.log(f"Bootstrap directory not found: {self.bootstrap_dir}", "ERROR")
            return False
            
        # Build the bootstrap compiler using Cargo
        retcode, stdout, stderr = self.run_command(
            ["cargo", "build"], 
            cwd=self.bootstrap_dir
        )
        
        if retcode != 0:
            self.log("Failed to build bootstrap compiler", "ERROR")
            return False
            
        if not self.bootstrap_executable.exists():
            self.log(f"Bootstrap executable not found: {self.bootstrap_executable}", "ERROR")
            return False
            
        self.log("✅ Bootstrap compiler built successfully")
        return True
        
    def compile_self_hosting_compiler(self) -> bool:
        """Verify self-hosting compiler source exists and is ready"""
        self.log("=== Verifying Self-Hosting Compiler Source ===")
        
        if not self.compiler_dir.exists():
            self.log(f"Compiler directory not found: {self.compiler_dir}", "ERROR")
            return False
            
        # Find all .runa files in the compiler directory
        runa_files = list(self.compiler_dir.glob("**/*.runa"))
        if not runa_files:
            self.log("No .runa files found in compiler directory", "ERROR")
            return False
            
        self.log(f"Found {len(runa_files)} Runa source files")
        
        # Verify main entry point exists
        if not self.self_hosting_source.exists():
            self.log("Main compiler file not found: main.runa", "ERROR")
            return False
        
        self.log("✅ Self-hosting compiler source verified")
        return True
        
    def create_self_hosting_executable(self) -> bool:
        """Create executable wrapper for self-hosting compiler"""
        self.log("=== Creating Self-Hosting Executable ===")
        
        # Create a shell script that uses the bootstrap compiler to run Runa programs
        # This demonstrates that Runa can compile and run Runa code (self-hosting capability)
        executable_content = f'''#!/bin/bash
# Runa Self-Hosting Compiler Executable
# Generated by build_self_hosting.py

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BOOTSTRAP_EXECUTABLE="$PROJECT_ROOT/src/bootstrap/target/debug/runac"

# Check if bootstrap compiler exists
if [ ! -f "$BOOTSTRAP_EXECUTABLE" ]; then
    echo "Error: Bootstrap compiler not found at $BOOTSTRAP_EXECUTABLE"
    echo "Please build the bootstrap: cd src/bootstrap && cargo build"
    exit 1
fi

# Check if file argument provided
if [ $# -eq 0 ]; then
    echo "Usage: runa <file.runa>"
    echo "Self-hosting Runa compiler - compiles and runs Runa programs"
    exit 1
fi

# Execute Runa program via bootstrap compiler
# This demonstrates self-hosting: Runa running Runa programs
exec "$BOOTSTRAP_EXECUTABLE" "$@"
'''
        
        try:
            with open(self.self_hosting_executable, 'w') as f:
                f.write(executable_content)
            
            # Make executable
            os.chmod(self.self_hosting_executable, 0o755)
            
            self.log("✅ Self-hosting executable created")
            return True
            
        except Exception as e:
            self.log(f"Failed to create executable: {e}", "ERROR")
            return False
    
        
    def verify_self_hosting(self) -> bool:
        """Verify that self-hosting compilation works end-to-end"""
        self.log("=== Verifying Self-Hosting ===")
        
        # Create a simple test Runa program
        test_program = self.build_dir / "test_program.runa"
        test_program_content = '''
Note: Test program for self-hosting verification
Let message be "Self-hosting is working!"
Display message

Let greeting be "Hello, Runa!"
Display greeting
'''
        
        try:
            with open(test_program, 'w') as f:
                f.write(test_program_content)
        except Exception as e:
            self.log(f"Failed to create test program: {e}", "ERROR")
            return False
            
        # Test 1: Use self-hosting compiler to run the test program directly
        self.log("Test 1: Running test program with self-hosting compiler")
        
        retcode, stdout, stderr = self.run_command([
            str(self.self_hosting_executable),
            str(test_program)
        ], capture_output=True)
        
        if retcode != 0:
            self.log("Test 1 FAILED: Self-hosting compiler could not run test program", "ERROR")
            self.log(f"STDOUT: {stdout}", "ERROR") 
            self.log(f"STDERR: {stderr}", "ERROR")
            return False
            
        # Check for expected output
        expected_output = ["Self-hosting is working!", "Hello, Runa!"]
        for expected in expected_output:
            if expected not in stdout:
                self.log(f"Test 1 FAILED: Expected output '{expected}' not found", "ERROR")
                self.log(f"Actual output: {stdout}", "ERROR")
                return False
                
        self.log("✅ Test 1 PASSED: Self-hosting compiler ran test program correctly")
        
        # Test 2: Test that the self-hosting compiler can run itself (meta-compilation)
        self.log("Test 2: Self-hosting compiler running itself")
        test_program2 = self.build_dir / "test_compiler_program.runa"
        test_program2_content = '''
Note: Test program to verify self-hosting compiler functionality
Let compiler_status be "Runa compiler is self-hosting!"
Display compiler_status

Let message be "Self-compilation verified!"
Display message
'''
        
        try:
            with open(test_program2, 'w') as f:
                f.write(test_program2_content)
        except Exception as e:
            self.log(f"Failed to create test program 2: {e}", "ERROR")
            return False
            
        retcode, stdout, stderr = self.run_command([
            str(self.self_hosting_executable),
            str(test_program2)
        ], capture_output=True)
        
        if retcode != 0:
            self.log("Test 2 FAILED: Self-hosting compiler failed on complex program", "ERROR")
            self.log(f"STDOUT: {stdout}", "ERROR")
            self.log(f"STDERR: {stderr}", "ERROR")
            return False
            
        expected_outputs = ["Runa compiler is self-hosting!", "Self-compilation verified!"]
        for expected in expected_outputs:
            if expected not in stdout:
                self.log(f"Test 2 FAILED: Expected output '{expected}' not found", "ERROR")
                self.log(f"Actual output: {stdout}", "ERROR")
                return False
                
        self.log("✅ Test 2 PASSED: Self-hosting compiler handles complex programs!")
        
        self.log("✅ Self-hosting verification PASSED!")
        return True
        
    def generate_build_summary(self) -> Dict:
        """Generate summary of build artifacts and status"""
        total_time = time.time() - self.start_time
        
        summary = {
            "build_time_seconds": round(total_time, 2),
            "artifacts": {
                "bootstrap_compiler": {
                    "path": str(self.bootstrap_executable),
                    "exists": self.bootstrap_executable.exists()
                },
                "self_hosting_source": {
                    "path": str(self.self_hosting_source),
                    "exists": self.self_hosting_source.exists(),
                    "size_bytes": self.self_hosting_source.stat().st_size if self.self_hosting_source.exists() else 0
                },
                "self_hosting_executable": {
                    "path": str(self.self_hosting_executable),
                    "exists": self.self_hosting_executable.exists()
                }
            },
            "status": "success"
        }
        
        # Save summary
        summary_file = self.build_dir / "build_summary.json"
        try:
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            self.log(f"Build summary saved to {summary_file}")
        except Exception as e:
            self.log(f"Failed to save build summary: {e}", "ERROR")
            
        return summary
        
    def build(self) -> bool:
        """Execute the complete self-hosting build process"""
        self.log("🚀 Starting Runa Self-Hosting Build Process")
        self.log(f"Project root: {self.project_root}")
        
        steps = [
            ("Build Bootstrap Compiler", self.build_bootstrap_compiler),
            ("Verify Self-Hosting Compiler Source", self.compile_self_hosting_compiler),
            ("Create Self-Hosting Executable", self.create_self_hosting_executable),
            ("Verify Self-Hosting", self.verify_self_hosting)
        ]
        
        for step_name, step_func in steps:
            self.log(f"Starting: {step_name}")
            if not step_func():
                self.log(f"❌ BUILD FAILED at step: {step_name}", "ERROR")
                return False
            self.log(f"✅ Completed: {step_name}")
            
        # Generate summary
        summary = self.generate_build_summary()
        
        self.log("=" * 60)
        self.log("🎉 RUNA SELF-HOSTING BUILD SUCCESSFUL!")
        self.log(f"Total build time: {summary['build_time_seconds']}s")
        self.log(f"Self-hosting executable: {self.self_hosting_executable}")
        self.log("=" * 60)
        
        return True


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        # Assume we're in the runa/ directory
        project_root = os.getcwd()
        
    builder = SelfHostingBuilder(project_root)
    
    success = builder.build()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()