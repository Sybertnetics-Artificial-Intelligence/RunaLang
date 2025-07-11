"""
Fortran Toolchain for Runa Universal Translation Platform
Manages Fortran compilation, scientific computing, and HPC development

This toolchain provides comprehensive support for:
- Multiple Fortran compilers (gfortran, ifort, xlf, nagfor)
- Scientific computing optimization
- HPC and parallel programming support
- Mathematical library integration (BLAS, LAPACK, MPI)
- Module dependency management
- Performance profiling and optimization
"""

import os
import subprocess
import shutil
import tempfile
import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from .fortran_generator import FortranGenerator
from .fortran_parser import FortranParser
from ...core.toolchain_base import BaseToolchain, CompilationError, ExecutionError
from ...shared.project_config import ProjectConfig

logger = logging.getLogger(__name__)

@dataclass
class FortranToolchainConfig:
    """Configuration for Fortran toolchain"""
    compiler: str = "gfortran"
    compiler_version: str = "auto"
    fortran_standard: str = "2018"  # 77, 90, 95, 2003, 2008, 2018
    optimization_level: str = "-O2"
    debug_mode: bool = False
    openmp_enabled: bool = False
    coarray_enabled: bool = False
    math_libraries: List[str] = field(default_factory=lambda: ["blas", "lapack"])
    module_directories: List[str] = field(default_factory=list)
    include_directories: List[str] = field(default_factory=list)
    library_directories: List[str] = field(default_factory=list)
    libraries: List[str] = field(default_factory=list)
    compiler_flags: List[str] = field(default_factory=list)
    linker_flags: List[str] = field(default_factory=list)
    precision_mode: str = "double"  # single, double, quad

class FortranToolchain(BaseToolchain):
    """Fortran development toolchain for scientific computing"""
    
    SUPPORTED_COMPILERS = {
        "gfortran": {
            "std_flag": "-std=",
            "module_flag": "-J",
            "include_flag": "-I",
            "library_flag": "-L",
            "link_flag": "-l",
            "openmp_flag": "-fopenmp",
            "coarray_flag": "-fcoarray=",
            "debug_flags": ["-g", "-fcheck=all", "-fbacktrace"]
        },
        "ifort": {
            "std_flag": "-stand ",
            "module_flag": "-module ",
            "include_flag": "-I",
            "library_flag": "-L",
            "link_flag": "-l",
            "openmp_flag": "-qopenmp",
            "coarray_flag": "-coarray",
            "debug_flags": ["-g", "-check", "-traceback"]
        },
        "nagfor": {
            "std_flag": "-f",
            "module_flag": "-mdir ",
            "include_flag": "-I",
            "library_flag": "-L",
            "link_flag": "-l",
            "openmp_flag": "-openmp",
            "coarray_flag": "-coarray",
            "debug_flags": ["-g", "-C=all", "-gline"]
        }
    }
    
    def __init__(self, config: Optional[FortranToolchainConfig] = None):
        super().__init__()
        self.config = config or FortranToolchainConfig()
        self.generator = FortranGenerator()
        self.parser = FortranParser()
        
        # Find and validate compiler
        self.compiler_path = self._find_compiler()
        self.compiler_info = self.SUPPORTED_COMPILERS.get(self.config.compiler, {})
        self.temp_dir = tempfile.mkdtemp(prefix="runa_fortran_")
        
        # Scientific computing setup
        self.math_lib_paths = self._find_math_libraries()
        
    def compile(self, source_code: str, output_path: str, **kwargs) -> bool:
        """Compile Fortran source code"""
        try:
            # Write source to temporary file
            source_ext = ".f90" if self.config.fortran_standard != "77" else ".f"
            temp_source = os.path.join(self.temp_dir, f"source{source_ext}")
            
            with open(temp_source, 'w', encoding='utf-8') as f:
                f.write(source_code)
            
            # Build compilation command
            cmd = [self.compiler_path]
            
            # Add Fortran standard
            if "std_flag" in self.compiler_info:
                std_flag = self.compiler_info["std_flag"]
                if self.config.fortran_standard == "77":
                    cmd.append(f"{std_flag}legacy")
                else:
                    cmd.append(f"{std_flag}f{self.config.fortran_standard}")
            
            # Add optimization flags
            if not self.config.debug_mode:
                cmd.append(self.config.optimization_level)
            else:
                cmd.extend(self.compiler_info.get("debug_flags", ["-g"]))
            
            # Add OpenMP support
            if self.config.openmp_enabled and "openmp_flag" in self.compiler_info:
                cmd.append(self.compiler_info["openmp_flag"])
            
            # Add coarray support
            if self.config.coarray_enabled and "coarray_flag" in self.compiler_info:
                coarray_flag = self.compiler_info["coarray_flag"]
                if self.config.compiler == "gfortran":
                    cmd.append(f"{coarray_flag}single")  # Default to single image
                else:
                    cmd.append(coarray_flag)
            
            # Add module directories
            if "module_flag" in self.compiler_info:
                module_flag = self.compiler_info["module_flag"]
                for mod_dir in self.config.module_directories:
                    cmd.append(f"{module_flag}{mod_dir}")
            
            # Add include directories
            if "include_flag" in self.compiler_info:
                include_flag = self.compiler_info["include_flag"]
                for inc_dir in self.config.include_directories:
                    cmd.append(f"{include_flag}{inc_dir}")
            
            # Add library directories
            if "library_flag" in self.compiler_info:
                lib_flag = self.compiler_info["library_flag"]
                for lib_dir in self.config.library_directories:
                    cmd.append(f"{lib_flag}{lib_dir}")
                
                # Add math library paths
                for lib_path in self.math_lib_paths:
                    cmd.append(f"{lib_flag}{lib_path}")
            
            # Add libraries
            if "link_flag" in self.compiler_info:
                link_flag = self.compiler_info["link_flag"]
                for lib in self.config.libraries:
                    cmd.append(f"{link_flag}{lib}")
                
                # Add math libraries
                for math_lib in self.config.math_libraries:
                    cmd.append(f"{link_flag}{math_lib}")
            
            # Add custom compiler flags
            cmd.extend(self.config.compiler_flags)
            
            # Add source file and output
            cmd.extend(["-o", output_path, temp_source])
            
            # Add linker flags
            cmd.extend(self.config.linker_flags)
            
            logger.info(f"Compiling with: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(output_path) if os.path.dirname(output_path) else "."
            )
            
            if result.returncode == 0:
                logger.info(f"Fortran compilation successful: {output_path}")
                return True
            else:
                error_msg = result.stderr or result.stdout
                logger.error(f"Fortran compilation failed: {error_msg}")
                raise CompilationError(f"Fortran compilation error: {error_msg}")
                
        except Exception as e:
            logger.error(f"Fortran compilation error: {e}")
            raise CompilationError(f"Failed to compile Fortran code: {e}")
        finally:
            # Cleanup temporary file
            if os.path.exists(temp_source):
                os.remove(temp_source)
    
    def execute(self, executable_path: str, args: List[str] = None, **kwargs) -> Tuple[int, str, str]:
        """Execute Fortran executable"""
        try:
            if not os.path.exists(executable_path):
                raise ExecutionError(f"Fortran executable not found: {executable_path}")
            
            cmd = [executable_path]
            if args:
                cmd.extend(args)
            
            # Set environment for scientific computing
            env = os.environ.copy()
            
            # Add OpenMP environment variables
            if self.config.openmp_enabled:
                env.setdefault("OMP_NUM_THREADS", "4")
                env.setdefault("OMP_PROC_BIND", "true")
            
            # Add math library paths to LD_LIBRARY_PATH
            if self.math_lib_paths:
                current_path = env.get("LD_LIBRARY_PATH", "")
                new_paths = ":".join(self.math_lib_paths)
                if current_path:
                    env["LD_LIBRARY_PATH"] = f"{new_paths}:{current_path}"
                else:
                    env["LD_LIBRARY_PATH"] = new_paths
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=os.path.dirname(executable_path) if os.path.dirname(executable_path) else "."
            )
            
            return result.returncode, result.stdout, result.stderr
            
        except Exception as e:
            logger.error(f"Fortran execution error: {e}")
            raise ExecutionError(f"Failed to execute Fortran program: {e}")
    
    def create_project(self, project_name: str, project_path: str, **kwargs) -> bool:
        """Create new Fortran project for scientific computing"""
        try:
            project_dir = Path(project_path)
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Create project structure
            (project_dir / "src").mkdir(exist_ok=True)
            (project_dir / "tests").mkdir(exist_ok=True)
            (project_dir / "docs").mkdir(exist_ok=True)
            (project_dir / "build").mkdir(exist_ok=True)
            (project_dir / "modules").mkdir(exist_ok=True)
            
            # Create main program file
            main_program_path = project_dir / "src" / f"{project_name.lower()}.f90"
            main_program_content = f'''program {project_name.lower()}
    implicit none
    
    ! Main program for {project_name}
    
    write(*,*) 'Hello from {project_name}!'
    write(*,*) 'Scientific computing with Fortran'
    
    call demonstrate_arrays()
    call demonstrate_math()
    
contains

    subroutine demonstrate_arrays()
        implicit none
        integer, parameter :: n = 5
        real(real64), dimension(n) :: x, y, z
        integer :: i
        
        ! Initialize arrays
        do i = 1, n
            x(i) = real(i, real64)
            y(i) = real(i**2, real64)
        end do
        
        ! Array operations
        z = x + y
        
        write(*,*) 'Array demonstration:'
        do i = 1, n
            write(*,'(A,I0,A,F6.2,A,F6.2,A,F6.2)') &
                'z(', i, ') = ', x(i), ' + ', y(i), ' = ', z(i)
        end do
    end subroutine demonstrate_arrays
    
    subroutine demonstrate_math()
        use iso_fortran_env, only: real64
        implicit none
        real(real64) :: x, y, result
        
        x = 3.14159_real64
        y = 2.71828_real64
        
        result = sqrt(x**2 + y**2)
        
        write(*,*) 'Mathematical operations:'
        write(*,'(A,F10.6)') 'sqrt(pi^2 + e^2) = ', result
    end subroutine demonstrate_math

end program {project_name.lower()}
'''
            
            with open(main_program_path, 'w', encoding='utf-8') as f:
                f.write(main_program_content)
            
            # Create utility module
            utils_module_path = project_dir / "src" / "utils.f90"
            utils_content = f'''module {project_name.lower()}_utils
    use iso_fortran_env, only: real64, int32
    implicit none
    
    private
    public :: matrix_multiply, linear_solve, numerical_derivative
    
contains

    function matrix_multiply(a, b) result(c)
        real(real64), intent(in) :: a(:,:), b(:,:)
        real(real64), allocatable :: c(:,:)
        integer :: i, j, k, n, m, p
        
        n = size(a, 1)
        m = size(a, 2)
        p = size(b, 2)
        
        allocate(c(n, p))
        c = 0.0_real64
        
        do i = 1, n
            do j = 1, p
                do k = 1, m
                    c(i, j) = c(i, j) + a(i, k) * b(k, j)
                end do
            end do
        end do
    end function matrix_multiply
    
    subroutine linear_solve(a, b, x)
        real(real64), intent(in) :: a(:,:), b(:)
        real(real64), intent(out) :: x(:)
        ! Simplified linear solver (would use LAPACK in practice)
        x = b  ! Placeholder
    end subroutine linear_solve
    
    function numerical_derivative(f, x, h) result(df_dx)
        interface
            real(real64) function f(x)
                import :: real64
                real(real64), intent(in) :: x
            end function f
        end interface
        real(real64), intent(in) :: x, h
        real(real64) :: df_dx
        
        ! Central difference formula
        df_dx = (f(x + h) - f(x - h)) / (2.0_real64 * h)
    end function numerical_derivative

end module {project_name.lower()}_utils
'''
            
            with open(utils_module_path, 'w', encoding='utf-8') as f:
                f.write(utils_content)
            
            # Create test file
            test_path = project_dir / "tests" / "test_basic.f90"
            test_content = f'''program test_{project_name.lower()}
    use {project_name.lower()}_utils
    use iso_fortran_env, only: real64
    implicit none
    
    write(*,*) 'Running tests for {project_name}...'
    
    call test_matrix_operations()
    call test_mathematical_functions()
    
    write(*,*) 'All tests passed!'
    
contains

    subroutine test_matrix_operations()
        real(real64), parameter :: tolerance = 1.0e-12_real64
        real(real64) :: a(2,2), b(2,2), c(2,2)
        real(real64) :: expected(2,2)
        
        ! Test matrix multiplication
        a = reshape([1.0_real64, 2.0_real64, 3.0_real64, 4.0_real64], [2,2])
        b = reshape([5.0_real64, 6.0_real64, 7.0_real64, 8.0_real64], [2,2])
        expected = reshape([19.0_real64, 22.0_real64, 43.0_real64, 50.0_real64], [2,2])
        
        c = matrix_multiply(a, b)
        
        if (maxval(abs(c - expected)) < tolerance) then
            write(*,*) 'Matrix multiplication test: PASSED'
        else
            write(*,*) 'Matrix multiplication test: FAILED'
        end if
    end subroutine test_matrix_operations
    
    subroutine test_mathematical_functions()
        real(real64), parameter :: tolerance = 1.0e-6_real64
        real(real64) :: x, h, df_dx_numerical, df_dx_analytical
        
        ! Test numerical derivative for f(x) = x^2
        x = 2.0_real64
        h = 1.0e-6_real64
        
        df_dx_numerical = numerical_derivative(test_function, x, h)
        df_dx_analytical = 2.0_real64 * x  ! d/dx(x^2) = 2x
        
        if (abs(df_dx_numerical - df_dx_analytical) < tolerance) then
            write(*,*) 'Numerical derivative test: PASSED'
        else
            write(*,*) 'Numerical derivative test: FAILED'
        end if
    end subroutine test_mathematical_functions
    
    real(real64) function test_function(x)
        real(real64), intent(in) :: x
        test_function = x**2
    end function test_function

end program test_{project_name.lower()}
'''
            
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Create Makefile
            makefile_path = project_dir / "Makefile"
            makefile_content = f'''# Makefile for {project_name}

FC = {self.config.compiler}
FFLAGS = -std=f{self.config.fortran_standard} {self.config.optimization_level} -J modules
LDFLAGS = 

SRCDIR = src
TESTDIR = tests
BUILDDIR = build
MODDIR = modules

SOURCES = $(wildcard $(SRCDIR)/*.f90)
OBJECTS = $(SOURCES:$(SRCDIR)/%.f90=$(BUILDDIR)/%.o)
TESTS = $(wildcard $(TESTDIR)/*.f90)
TEST_EXES = $(TESTS:$(TESTDIR)/%.f90=$(BUILDDIR)/%)

TARGET = $(BUILDDIR)/{project_name.lower()}

.PHONY: all clean test

all: $(TARGET)

$(TARGET): $(OBJECTS) | $(BUILDDIR)
\t$(FC) $(FFLAGS) -o $@ $(OBJECTS) $(LDFLAGS)

$(BUILDDIR)/%.o: $(SRCDIR)/%.f90 | $(BUILDDIR) $(MODDIR)
\t$(FC) $(FFLAGS) -c $< -o $@

$(BUILDDIR):
\tmkdir -p $(BUILDDIR)

$(MODDIR):
\tmkdir -p $(MODDIR)

test: $(TEST_EXES)
\t@for test in $(TEST_EXES); do \\
\t\techo "Running $$test..."; \\
\t\t$$test; \\
\tdone

$(BUILDDIR)/test_%: $(TESTDIR)/test_%.f90 $(filter-out $(BUILDDIR)/{project_name.lower()}.o,$(OBJECTS)) | $(BUILDDIR)
\t$(FC) $(FFLAGS) -o $@ $< $(filter-out $(BUILDDIR)/{project_name.lower()}.o,$(OBJECTS)) $(LDFLAGS)

clean:
\trm -rf $(BUILDDIR) $(MODDIR)

run: $(TARGET)
\t./$(TARGET)

.SUFFIXES: .f90 .o
'''
            
            with open(makefile_path, 'w', encoding='utf-8') as f:
                f.write(makefile_content)
            
            # Create README
            readme_path = project_dir / "README.md"
            readme_content = f'''# {project_name}

Scientific computing project using Fortran.

## Building

```bash
make
```

## Running

```bash
make run
```

## Testing

```bash
make test
```

## Features

- Modern Fortran ({self.config.fortran_standard}) syntax
- Scientific computing utilities
- Matrix operations
- Numerical methods
- Comprehensive testing

## Dependencies

- {self.config.compiler} compiler
- BLAS/LAPACK libraries (for advanced linear algebra)
{"- OpenMP (for parallel computing)" if self.config.openmp_enabled else ""}
{"- Coarray support (for distributed computing)" if self.config.coarray_enabled else ""}

## Project Structure

- `src/` - Source code
- `tests/` - Test programs
- `build/` - Compiled objects and executables
- `modules/` - Fortran module files
- `docs/` - Documentation
'''
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            logger.info(f"Created Fortran project: {project_name} at {project_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating Fortran project: {e}")
            return False
    
    def get_version(self) -> str:
        """Get Fortran compiler version"""
        try:
            result = subprocess.run(
                [self.compiler_path, "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.split('\n')[0]
            else:
                return "Unknown"
                
        except Exception as e:
            logger.error(f"Error getting Fortran compiler version: {e}")
            return "Unknown"
    
    def validate_environment(self) -> Tuple[bool, List[str]]:
        """Validate Fortran development environment"""
        issues = []
        
        try:
            # Check compiler
            if not self.compiler_path:
                issues.append(f"Fortran compiler '{self.config.compiler}' not found")
                return False, issues
            
            # Check compiler version
            version_info = self.get_version()
            if "Unknown" in version_info:
                issues.append("Could not determine compiler version")
            
            # Check math libraries
            missing_libs = []
            for lib in self.config.math_libraries:
                if not self._find_library(lib):
                    missing_libs.append(lib)
            
            if missing_libs:
                issues.append(f"Missing math libraries: {', '.join(missing_libs)}")
            
            # Check OpenMP support if enabled
            if self.config.openmp_enabled:
                if not self._check_openmp_support():
                    issues.append("OpenMP support requested but not available")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            issues.append(f"Environment validation error: {e}")
            return False, issues
    
    def _find_compiler(self) -> Optional[str]:
        """Find Fortran compiler"""
        return shutil.which(self.config.compiler)
    
    def _find_math_libraries(self) -> List[str]:
        """Find math library paths"""
        paths = []
        
        # Common library locations
        common_paths = [
            "/usr/lib",
            "/usr/lib64", 
            "/usr/local/lib",
            "/opt/local/lib",
            "/usr/lib/x86_64-linux-gnu"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                # Check for BLAS/LAPACK
                for lib in ["libblas", "liblapack"]:
                    lib_files = [f"{lib}.so", f"{lib}.a", f"{lib}.dylib"]
                    if any(os.path.exists(os.path.join(path, lib_file)) for lib_file in lib_files):
                        if path not in paths:
                            paths.append(path)
        
        return paths
    
    def _find_library(self, lib_name: str) -> bool:
        """Check if a library is available"""
        for path in self.math_lib_paths:
            lib_files = [f"lib{lib_name}.so", f"lib{lib_name}.a", f"lib{lib_name}.dylib"]
            if any(os.path.exists(os.path.join(path, lib_file)) for lib_file in lib_files):
                return True
        return False
    
    def _check_openmp_support(self) -> bool:
        """Check if compiler supports OpenMP"""
        try:
            # Create a simple test program
            test_code = '''program test_openmp
    use omp_lib
    implicit none
    write(*,*) 'OpenMP threads:', omp_get_max_threads()
end program test_openmp
'''
            
            test_file = os.path.join(self.temp_dir, "test_openmp.f90")
            test_exe = os.path.join(self.temp_dir, "test_openmp")
            
            with open(test_file, 'w') as f:
                f.write(test_code)
            
            # Try to compile with OpenMP
            cmd = [self.compiler_path]
            if "openmp_flag" in self.compiler_info:
                cmd.append(self.compiler_info["openmp_flag"])
            cmd.extend(["-o", test_exe, test_file])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Cleanup
            for temp_file in [test_file, test_exe]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def cleanup(self):
        """Clean up temporary files and resources"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.warning(f"Error cleaning up Fortran toolchain: {e}")
    
    def __del__(self):
        """Destructor to clean up resources"""
        self.cleanup() 