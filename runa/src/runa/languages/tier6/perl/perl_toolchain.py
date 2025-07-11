"""
Perl Toolchain for Runa Universal Translation Platform
Manages Perl compilation, execution, and development tools

This toolchain provides comprehensive support for:
- Perl 5 execution and testing
- CPAN module management and installation
- Text processing and regex optimization
- Cross-platform Perl compatibility
- Performance profiling and optimization
- Code quality and best practices checking
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

from .perl_generator import PerlGenerator
from .perl_parser import PerlParser
from ...core.toolchain_base import BaseToolchain, CompilationError, ExecutionError
from ...shared.project_config import ProjectConfig

logger = logging.getLogger(__name__)

@dataclass
class PerlToolchainConfig:
    """Configuration for Perl toolchain"""
    perl_path: str = "perl"
    cpan_path: str = "cpan"
    cpanm_path: str = "cpanm"
    perl_version: str = "5.32"
    use_strict: bool = True
    use_warnings: bool = True
    enable_utf8: bool = True
    text_processing_mode: bool = True
    optimize_regex: bool = True
    enable_cpan_mirror: Optional[str] = None
    lib_paths: List[str] = field(default_factory=list)
    include_paths: List[str] = field(default_factory=list)
    environment_vars: Dict[str, str] = field(default_factory=dict)

class PerlToolchain(BaseToolchain):
    """Perl development toolchain"""
    
    def __init__(self, config: Optional[PerlToolchainConfig] = None):
        super().__init__()
        self.config = config or PerlToolchainConfig()
        self.generator = PerlGenerator()
        self.parser = PerlParser()
        
        # Perl-specific paths and settings
        self.perl_executable = self._find_perl_executable()
        self.cpan_home = self._get_cpan_home()
        self.temp_dir = tempfile.mkdtemp(prefix="runa_perl_")
        
        # Performance and optimization settings
        self.enable_warnings = True
        self.strict_mode = True
        self.taint_mode = False
        
    def compile(self, source_code: str, output_path: str, **kwargs) -> bool:
        """
        Compile Perl source code (syntax check)
        Perl is interpreted, so this performs syntax validation
        """
        try:
            # Write source to temporary file
            temp_file = os.path.join(self.temp_dir, "temp_program.pl")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(source_code)
            
            # Perform syntax check
            cmd = [self.perl_executable, "-c"]
            
            if self.config.use_strict:
                cmd.extend(["-M", "strict"])
            if self.config.use_warnings:
                cmd.extend(["-M", "warnings"])
            if self.config.enable_utf8:
                cmd.extend(["-M", "utf8"])
            
            cmd.append(temp_file)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(output_path) if os.path.dirname(output_path) else "."
            )
            
            if result.returncode == 0:
                # Copy source to output path if syntax is valid
                shutil.copy2(temp_file, output_path)
                logger.info(f"Perl syntax check passed: {output_path}")
                return True
            else:
                error_msg = result.stderr or result.stdout
                logger.error(f"Perl syntax check failed: {error_msg}")
                raise CompilationError(f"Perl syntax error: {error_msg}")
                
        except Exception as e:
            logger.error(f"Perl compilation error: {e}")
            raise CompilationError(f"Failed to compile Perl code: {e}")
        finally:
            # Cleanup temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def execute(self, script_path: str, args: List[str] = None, **kwargs) -> Tuple[int, str, str]:
        """Execute Perl script"""
        try:
            if not os.path.exists(script_path):
                raise ExecutionError(f"Perl script not found: {script_path}")
            
            cmd = [self.perl_executable]
            
            # Add Perl options
            if self.config.use_strict:
                cmd.extend(["-M", "strict"])
            if self.config.use_warnings:
                cmd.extend(["-M", "warnings"])
            if self.config.enable_utf8:
                cmd.extend(["-M", "utf8"])
            
            # Add library paths
            for lib_path in self.config.lib_paths:
                cmd.extend(["-I", lib_path])
            
            # Add script and arguments
            cmd.append(script_path)
            if args:
                cmd.extend(args)
            
            # Set environment
            env = os.environ.copy()
            env.update(self.config.environment_vars)
            
            if self.config.enable_cpan_mirror:
                env["PERL_CPANM_OPT"] = f"--mirror {self.config.enable_cpan_mirror}"
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=os.path.dirname(script_path) if os.path.dirname(script_path) else "."
            )
            
            return result.returncode, result.stdout, result.stderr
            
        except Exception as e:
            logger.error(f"Perl execution error: {e}")
            raise ExecutionError(f"Failed to execute Perl script: {e}")
    
    def test(self, test_path: str, **kwargs) -> bool:
        """Run Perl tests using prove or Test::Harness"""
        try:
            if os.path.isfile(test_path) and test_path.endswith('.t'):
                # Single test file
                cmd = [self.perl_executable, test_path]
            elif os.path.isdir(test_path):
                # Test directory - use prove if available
                prove_path = shutil.which("prove")
                if prove_path:
                    cmd = [prove_path, "-l", test_path]
                else:
                    # Fallback to running all .t files
                    test_files = []
                    for root, dirs, files in os.walk(test_path):
                        for file in files:
                            if file.endswith('.t'):
                                test_files.append(os.path.join(root, file))
                    
                    if not test_files:
                        logger.warning(f"No test files found in {test_path}")
                        return True
                    
                    # Run tests sequentially
                    for test_file in test_files:
                        retcode, stdout, stderr = self.execute(test_file)
                        if retcode != 0:
                            logger.error(f"Test failed: {test_file}\n{stderr}")
                            return False
                    return True
            else:
                raise ExecutionError(f"Invalid test path: {test_path}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Perl tests passed: {test_path}")
                return True
            else:
                logger.error(f"Perl tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Perl test execution error: {e}")
            return False
    
    def install_dependencies(self, dependencies: List[str], **kwargs) -> bool:
        """Install Perl modules using cpanm or cpan"""
        try:
            # Try cpanm first (faster, better dependency resolution)
            installer = shutil.which("cpanm") or shutil.which("cpan")
            
            if not installer:
                logger.error("Neither cpanm nor cpan found. Cannot install dependencies.")
                return False
            
            for dependency in dependencies:
                logger.info(f"Installing Perl module: {dependency}")
                
                cmd = [installer]
                if "cpanm" in installer:
                    cmd.extend(["--quiet", "--notest"])
                    if self.config.enable_cpan_mirror:
                        cmd.extend(["--mirror", self.config.enable_cpan_mirror])
                
                cmd.append(dependency)
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.error(f"Failed to install {dependency}: {result.stderr}")
                    return False
                
                logger.info(f"Successfully installed {dependency}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error installing Perl dependencies: {e}")
            return False
    
    def create_project(self, project_name: str, project_path: str, **kwargs) -> bool:
        """Create new Perl project structure"""
        try:
            project_dir = Path(project_path)
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Create project structure
            (project_dir / "lib").mkdir(exist_ok=True)
            (project_dir / "t").mkdir(exist_ok=True)
            (project_dir / "bin").mkdir(exist_ok=True)
            (project_dir / "docs").mkdir(exist_ok=True)
            
            # Create main module file
            main_module_path = project_dir / "lib" / f"{project_name}.pm"
            main_module_content = f'''package {project_name};

use strict;
use warnings;
use utf8;

our $VERSION = '0.01';

=head1 NAME

{project_name} - Brief description

=head1 SYNOPSIS

    use {project_name};
    
    # Your code here

=head1 DESCRIPTION

Description of the module.

=head1 METHODS

=head2 new

Constructor.

=cut

sub new {{
    my ($class, %args) = @_;
    my $self = bless {{
        # Initialize instance variables
    }}, $class;
    
    return $self;
}}

=head1 AUTHOR

Generated by Runa Universal Translation Platform

=head1 LICENSE

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

1;
'''
            
            with open(main_module_path, 'w', encoding='utf-8') as f:
                f.write(main_module_content)
            
            # Create main script
            main_script_path = project_dir / "bin" / f"{project_name.lower()}"
            main_script_content = f'''#!/usr/bin/env perl

use strict;
use warnings;
use utf8;
use FindBin qw($Bin);
use lib "$Bin/../lib";

use {project_name};

# Main program logic
my $app = {project_name}->new();

# Add your application logic here

print "Hello from {project_name}!\\n";
'''
            
            with open(main_script_path, 'w', encoding='utf-8') as f:
                f.write(main_script_content)
            
            # Make script executable
            os.chmod(main_script_path, 0o755)
            
            # Create test file
            test_path = project_dir / "t" / "01-basic.t"
            test_content = f'''#!/usr/bin/env perl

use strict;
use warnings;
use utf8;
use Test::More tests => 2;

BEGIN {{
    use_ok('{project_name}');
}}

my $obj = {project_name}->new();
isa_ok($obj, '{project_name}');

done_testing();
'''
            
            with open(test_path, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Create Makefile.PL
            makefile_path = project_dir / "Makefile.PL"
            makefile_content = f'''use ExtUtils::MakeMaker;

WriteMakefile(
    NAME         => '{project_name}',
    VERSION_FROM => 'lib/{project_name}.pm',
    PREREQ_PM    => {{
        'Test::More' => 0,
    }},
    EXE_FILES    => ['bin/{project_name.lower()}'],
    ($ExtUtils::MakeMaker::VERSION >= 6.3002
      ? ('LICENSE'=> 'perl')
      : ()),
);
'''
            
            with open(makefile_path, 'w', encoding='utf-8') as f:
                f.write(makefile_content)
            
            # Create README
            readme_path = project_dir / "README.md"
            readme_content = f'''# {project_name}

Brief description of {project_name}.

## Installation

```bash
perl Makefile.PL
make
make test
make install
```

## Usage

```perl
use {project_name};

my $obj = {project_name}->new();
```

## Testing

```bash
prove -l t/
```

## Documentation

See POD documentation in the module files.

## Author

Generated by Runa Universal Translation Platform

## License

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.
'''
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # Create .gitignore
            gitignore_path = project_dir / ".gitignore"
            gitignore_content = '''# Build artifacts
Makefile
Makefile.old
Build
Build.bat
_build/
blib/
pm_to_blib

# Temp files
*.tmp
*.bak
*.swp
*~

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/

# Perl specific
MYMETA.*
'''
            
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            
            logger.info(f"Created Perl project: {project_name} at {project_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating Perl project: {e}")
            return False
    
    def lint(self, source_path: str, **kwargs) -> Tuple[bool, List[str]]:
        """Lint Perl code using perl -c and optional Perl::Critic"""
        issues = []
        
        try:
            # Basic syntax check
            cmd = [self.perl_executable, "-c", source_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                issues.append(f"Syntax error: {result.stderr}")
            
            # Try Perl::Critic if available
            perlcritic_path = shutil.which("perlcritic")
            if perlcritic_path:
                cmd = [perlcritic_path, "--quiet", "--verbose", "8", source_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            issues.append(f"Style issue: {line}")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            logger.error(f"Error linting Perl code: {e}")
            return False, [f"Linting error: {e}"]
    
    def profile(self, script_path: str, **kwargs) -> Dict[str, Any]:
        """Profile Perl script performance"""
        try:
            # Use Devel::NYTProf if available
            cmd = [self.perl_executable, "-d:NYTProf", script_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            profile_data = {
                "execution_time": "N/A",
                "memory_usage": "N/A", 
                "subroutine_calls": "N/A",
                "notes": []
            }
            
            if result.returncode == 0:
                profile_data["notes"].append("Profiling completed successfully")
                
                # Check for nytprof.out file
                nytprof_file = "nytprof.out"
                if os.path.exists(nytprof_file):
                    profile_data["notes"].append(f"Profile data saved to {nytprof_file}")
                    profile_data["notes"].append("Run 'nytprofhtml' to generate HTML report")
            else:
                profile_data["notes"].append(f"Profiling failed: {result.stderr}")
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error profiling Perl script: {e}")
            return {"error": str(e)}
    
    def format_code(self, source_code: str, **kwargs) -> str:
        """Format Perl code using perltidy if available"""
        try:
            perltidy_path = shutil.which("perltidy")
            if not perltidy_path:
                logger.warning("perltidy not found, returning original code")
                return source_code
            
            # Create temporary files
            input_file = os.path.join(self.temp_dir, "input.pl")
            output_file = os.path.join(self.temp_dir, "output.pl")
            
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(source_code)
            
            cmd = [perltidy_path, "-o", output_file, input_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    formatted_code = f.read()
                return formatted_code
            else:
                logger.warning(f"perltidy formatting failed: {result.stderr}")
                return source_code
                
        except Exception as e:
            logger.error(f"Error formatting Perl code: {e}")
            return source_code
        finally:
            # Cleanup temporary files
            for temp_file in [input_file, output_file]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
    
    def get_version(self) -> str:
        """Get Perl version"""
        try:
            result = subprocess.run(
                [self.perl_executable, "-v"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Extract version from perl -v output
                output = result.stdout
                for line in output.split('\n'):
                    if 'This is perl' in line:
                        return line.strip()
                
                return output.split('\n')[0] if output else "Unknown"
            else:
                return "Unknown"
                
        except Exception as e:
            logger.error(f"Error getting Perl version: {e}")
            return "Unknown"
    
    def validate_environment(self) -> Tuple[bool, List[str]]:
        """Validate Perl development environment"""
        issues = []
        
        try:
            # Check Perl executable
            if not self.perl_executable:
                issues.append("Perl executable not found")
                return False, issues
            
            # Check Perl version
            version_info = self.get_version()
            if "Unknown" in version_info:
                issues.append("Could not determine Perl version")
            
            # Check for essential modules
            essential_modules = ['strict', 'warnings', 'utf8', 'Test::More']
            for module in essential_modules:
                cmd = [self.perl_executable, "-M" + module, "-e", "1"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    issues.append(f"Missing essential module: {module}")
            
            # Check for CPAN tools
            cpan_tools = ['cpan', 'cpanm']
            available_tools = []
            for tool in cpan_tools:
                if shutil.which(tool):
                    available_tools.append(tool)
            
            if not available_tools:
                issues.append("No CPAN installation tools found (cpan, cpanm)")
            
            return len(issues) == 0, issues
            
        except Exception as e:
            issues.append(f"Environment validation error: {e}")
            return False, issues
    
    def _find_perl_executable(self) -> Optional[str]:
        """Find Perl executable"""
        return shutil.which(self.config.perl_path) or shutil.which("perl")
    
    def _get_cpan_home(self) -> str:
        """Get CPAN home directory"""
        try:
            result = subprocess.run(
                [self.perl_executable, "-MConfig", "-e", "print $Config{sitearch}"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return os.path.expanduser("~/.cpan")
                
        except Exception:
            return os.path.expanduser("~/.cpan")
    
    def cleanup(self):
        """Clean up temporary files and resources"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.warning(f"Error cleaning up Perl toolchain: {e}")
    
    def __del__(self):
        """Destructor to clean up resources"""
        self.cleanup() 