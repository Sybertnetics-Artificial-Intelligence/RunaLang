"""
COBOL Toolchain for Runa Universal Translation Platform
Provides compilation, testing, and mainframe development tools for COBOL programs
Supports COBOL-85/2002 standards with enterprise-grade features
"""

import os
import sys
import subprocess
import tempfile
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging

from ...shared.base_toolchain import BaseToolchain, ToolchainError, CompilationResult, TestResult

# Configure logging
logger = logging.getLogger(__name__)

class COBOLStandard(Enum):
    """COBOL language standards"""
    COBOL_85 = "85"
    COBOL_2002 = "2002"
    COBOL_2014 = "2014"
    IBM_ENTERPRISE = "ibm"
    MICRO_FOCUS = "microfocus"

class COBOLDialect(Enum):
    """COBOL compiler dialects"""
    IBM_MVS = "ibm_mvs"
    IBM_VSE = "ibm_vse"
    MICRO_FOCUS = "micro_focus"
    GNU_COBOL = "gnu_cobol"
    FUJITSU = "fujitsu"
    OPEN_COBOL = "open_cobol"

@dataclass
class COBOLConfiguration:
    """COBOL project configuration"""
    project_name: str
    standard: COBOLStandard = COBOLStandard.COBOL_85
    dialect: COBOLDialect = COBOLDialect.GNU_COBOL
    
    # Fixed format settings
    use_fixed_format: bool = True
    sequence_area: bool = True
    indicator_area: bool = True
    
    # Compilation options
    debug_mode: bool = False
    optimize_level: int = 0
    pic_clause_validation: bool = True
    usage_clause_validation: bool = True
    
    # File organization
    default_file_organization: str = "SEQUENTIAL"
    default_access_mode: str = "SEQUENTIAL"
    
    # Mainframe compatibility
    mainframe_compatibility: bool = True
    ebcdic_support: bool = False
    record_length: int = 80
    
    # Enterprise features
    transaction_support: bool = False
    database_connectivity: bool = False
    copybook_directories: List[str] = None
    
    def __post_init__(self):
        if self.copybook_directories is None:
            self.copybook_directories = ["copybooks", "copy"]

class COBOLToolchain(BaseToolchain):
    """Complete COBOL development toolchain for enterprise applications"""
    
    def __init__(self, config: Optional[COBOLConfiguration] = None):
        """Initialize COBOL toolchain with configuration"""
        super().__init__("cobol", "cob")
        self.config = config or COBOLConfiguration("cobol_project")
        self.compiler_path = self._find_compiler()
        self.copybook_cache: Dict[str, str] = {}
        
    def _find_compiler(self) -> Optional[str]:
        """Find available COBOL compiler on system"""
        compilers = {
            COBOLDialect.GNU_COBOL: ["cobc", "gnucobol"],
            COBOLDialect.OPEN_COBOL: ["cobc", "open-cobol"],
            COBOLDialect.MICRO_FOCUS: ["cob", "cobcurses"],
            COBOLDialect.IBM_MVS: ["igy", "igyccrn"],
        }
        
        for dialect, compiler_names in compilers.items():
            for compiler in compiler_names:
                if shutil.which(compiler):
                    logger.info(f"Found COBOL compiler: {compiler} for {dialect.value}")
                    return compiler
                    
        logger.warning("No COBOL compiler found. Install GnuCOBOL for basic support.")
        return None
    
    def create_project(self, name: str, directory: str) -> bool:
        """Create new COBOL project with proper structure"""
        try:
            project_path = Path(directory) / name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Create COBOL project structure
            directories = [
                "src",           # Source programs
                "copybooks",     # COPY members
                "data",          # Data files
                "jcl",           # Job Control Language
                "procedures",    # Procedures/paragraphs
                "test",          # Test programs
                "docs",          # Documentation
            ]
            
            for dir_name in directories:
                (project_path / dir_name).mkdir(exist_ok=True)
                
            # Create project configuration
            config_data = {
                "name": name,
                "version": "1.0.0",
                "standard": self.config.standard.value,
                "dialect": self.config.dialect.value,
                "fixed_format": self.config.use_fixed_format,
                "copybook_directories": self.config.copybook_directories,
                "compile_options": {
                    "debug": self.config.debug_mode,
                    "optimize": self.config.optimize_level,
                    "mainframe_compat": self.config.mainframe_compatibility
                }
            }
            
            config_file = project_path / "cobol.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
            # Create sample COBOL program
            sample_program = self._generate_sample_program(name)
            sample_file = project_path / "src" / f"{name.upper()}.COB"
            with open(sample_file, 'w') as f:
                f.write(sample_program)
                
            # Create copybook template
            copybook_template = self._generate_copybook_template()
            copybook_file = project_path / "copybooks" / "COMMON.CBL"
            with open(copybook_file, 'w') as f:
                f.write(copybook_template)
                
            logger.info(f"COBOL project '{name}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create COBOL project: {e}")
            return False
    
    def _generate_sample_program(self, name: str) -> str:
        """Generate sample COBOL program with proper format"""
        program_name = name.upper()[:8]  # COBOL program names max 8 chars
        
        return f'''      *> Sample COBOL Program - {program_name}
      *> Generated by Runa Universal Translation Platform
       IDENTIFICATION DIVISION.
       PROGRAM-ID. {program_name}.
       AUTHOR. Runa Translator.
       DATE-WRITTEN. TODAY.
       
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SOURCE-COMPUTER. IBM-PC.
       OBJECT-COMPUTER. IBM-PC.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-MESSAGE           PIC X(30) VALUE 'Hello from COBOL!'.
       01  WS-COUNTER           PIC 9(3) VALUE ZERO.
       01  WS-RESULT            PIC 9(5) VALUE ZERO.
       
       PROCEDURE DIVISION.
       MAIN-PROGRAM.
           DISPLAY "Starting {program_name} program".
           DISPLAY WS-MESSAGE.
           
           PERFORM VARYING WS-COUNTER FROM 1 BY 1 
               UNTIL WS-COUNTER > 10
               COMPUTE WS-RESULT = WS-RESULT + WS-COUNTER
           END-PERFORM.
           
           DISPLAY "Sum of 1-10: " WS-RESULT.
           DISPLAY "Program completed successfully".
           STOP RUN.
'''
    
    def _generate_copybook_template(self) -> str:
        """Generate common copybook template"""
        return '''      *> Common Data Structures Copybook
      *> Generated by Runa Universal Translation Platform
       01  COMMON-ERROR-CODES.
           05  WS-SUCCESS       PIC 9(2) VALUE 00.
           05  WS-FILE-ERROR    PIC 9(2) VALUE 10.
           05  WS-DATA-ERROR    PIC 9(2) VALUE 20.
           05  WS-SYSTEM-ERROR  PIC 9(2) VALUE 99.
       
       01  COMMON-SWITCHES.
           05  WS-EOF-FLAG      PIC X VALUE 'N'.
               88  EOF-REACHED  VALUE 'Y'.
           05  WS-ERROR-FLAG    PIC X VALUE 'N'.
               88  ERROR-FOUND  VALUE 'Y'.
       
       01  COMMON-COUNTERS.
           05  WS-RECORD-COUNT  PIC 9(7) VALUE ZERO.
           05  WS-ERROR-COUNT   PIC 9(5) VALUE ZERO.
'''
    
    def compile(self, source_file: str, output_file: Optional[str] = None, 
                options: Optional[Dict[str, Any]] = None) -> CompilationResult:
        """Compile COBOL source file"""
        try:
            if not self.compiler_path:
                raise ToolchainError("No COBOL compiler available")
                
            source_path = Path(source_file)
            if not source_path.exists():
                raise ToolchainError(f"Source file not found: {source_file}")
                
            if output_file is None:
                output_file = source_path.stem + (".exe" if sys.platform == "win32" else "")
                
            # Build compiler command
            cmd = [self.compiler_path]
            
            # Add compiler-specific options
            if self.config.dialect == COBOLDialect.GNU_COBOL:
                cmd.extend(["-x", "-o", output_file])
                if self.config.debug_mode:
                    cmd.append("-g")
                if self.config.optimize_level > 0:
                    cmd.append(f"-O{self.config.optimize_level}")
                if self.config.use_fixed_format:
                    cmd.append("-fixed")
                    
            elif self.config.dialect == COBOLDialect.MICRO_FOCUS:
                cmd.extend(["-o", output_file])
                if self.config.debug_mode:
                    cmd.append("-g")
                    
            # Add copybook directories
            for copybook_dir in self.config.copybook_directories:
                if Path(copybook_dir).exists():
                    cmd.extend(["-I", copybook_dir])
                    
            cmd.append(str(source_path))
            
            # Execute compilation
            logger.info(f"Compiling COBOL: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            return CompilationResult(
                success=result.returncode == 0,
                output_file=output_file if result.returncode == 0 else None,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                compilation_time=0.0  # Could add timing if needed
            )
            
        except subprocess.TimeoutExpired:
            raise ToolchainError("COBOL compilation timed out")
        except Exception as e:
            raise ToolchainError(f"COBOL compilation failed: {e}")
    
    def format_code(self, source_code: str, style: str = "standard") -> str:
        """Format COBOL code according to style guidelines"""
        lines = source_code.split('\n')
        formatted_lines = []
        
        for line in lines:
            if not line.strip():
                formatted_lines.append('')
                continue
                
            # Handle fixed format (columns 1-80)
            if self.config.use_fixed_format:
                formatted_line = self._format_fixed_line(line, style)
            else:
                formatted_line = self._format_free_line(line, style)
                
            formatted_lines.append(formatted_line)
            
        return '\n'.join(formatted_lines)
    
    def _format_fixed_line(self, line: str, style: str) -> str:
        """Format line for COBOL fixed format"""
        if len(line) == 0:
            return line
            
        # Preserve sequence area (columns 1-6) if present
        sequence_area = line[:6] if len(line) >= 6 else line.ljust(6)
        
        # Handle indicator area (column 7)
        indicator = line[6] if len(line) > 6 else ' '
        
        # Format content area (columns 8-72)
        content = line[7:] if len(line) > 7 else ''
        content = content.rstrip()
        
        # Rebuild line with proper formatting
        if style == "mainframe":
            # Strict mainframe format
            if len(content) > 65:  # Max content length (72 - 7)
                content = content[:65]
            formatted = sequence_area + indicator + content.ljust(65)[:65]
        else:
            # Standard format
            formatted = sequence_area + indicator + content
            
        return formatted
    
    def _format_free_line(self, line: str, style: str) -> str:
        """Format line for COBOL free format"""
        # Basic indentation and spacing
        stripped = line.strip()
        if not stripped:
            return ''
            
        # Determine indentation level
        indent_level = 0
        if stripped.startswith('01 ') or stripped.startswith('77 '):
            indent_level = 0
        elif stripped.startswith(('05 ', '10 ', '15 ', '20 ')):
            indent_level = 1
        elif stripped.upper().endswith(' DIVISION.'):
            indent_level = 0
        elif stripped.upper().endswith(' SECTION.'):
            indent_level = 1
        else:
            indent_level = 2
            
        return '       ' + '    ' * indent_level + stripped
    
    def run_tests(self, test_directory: str = "test") -> TestResult:
        """Run COBOL test programs"""
        try:
            test_path = Path(test_directory)
            if not test_path.exists():
                logger.warning(f"Test directory not found: {test_directory}")
                return TestResult(success=True, total_tests=0, passed_tests=0, 
                                failed_tests=0, test_output="No tests found")
                
            # Find test COBOL programs
            test_files = list(test_path.glob("TEST*.COB")) + list(test_path.glob("*TEST.COB"))
            
            if not test_files:
                return TestResult(success=True, total_tests=0, passed_tests=0,
                                failed_tests=0, test_output="No test files found")
                
            total_tests = len(test_files)
            passed_tests = 0
            failed_tests = 0
            test_outputs = []
            
            for test_file in test_files:
                try:
                    # Compile test program
                    compile_result = self.compile(str(test_file))
                    if not compile_result.success:
                        failed_tests += 1
                        test_outputs.append(f"FAILED: {test_file.name} - Compilation failed")
                        continue
                        
                    # Run test program
                    if compile_result.output_file and Path(compile_result.output_file).exists():
                        run_result = subprocess.run([compile_result.output_file], 
                                                  capture_output=True, text=True, timeout=30)
                        
                        if run_result.returncode == 0:
                            passed_tests += 1
                            test_outputs.append(f"PASSED: {test_file.name}")
                        else:
                            failed_tests += 1
                            test_outputs.append(f"FAILED: {test_file.name} - Runtime error")
                            
                        # Clean up executable
                        try:
                            Path(compile_result.output_file).unlink()
                        except:
                            pass
                            
                except Exception as e:
                    failed_tests += 1
                    test_outputs.append(f"FAILED: {test_file.name} - {str(e)}")
                    
            return TestResult(
                success=failed_tests == 0,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                test_output='\n'.join(test_outputs)
            )
            
        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return TestResult(success=False, total_tests=0, passed_tests=0,
                            failed_tests=1, test_output=f"Test framework error: {e}")
    
    def generate_documentation(self, source_directory: str, output_directory: str) -> bool:
        """Generate documentation from COBOL source files"""
        try:
            src_path = Path(source_directory)
            doc_path = Path(output_directory)
            doc_path.mkdir(parents=True, exist_ok=True)
            
            # Find COBOL source files
            cobol_files = list(src_path.glob("*.COB")) + list(src_path.glob("*.CBL"))
            
            documentation = []
            documentation.append("# COBOL Project Documentation\n")
            documentation.append(f"Generated by Runa Universal Translation Platform\n\n")
            
            for cobol_file in cobol_files:
                doc_content = self._extract_documentation(cobol_file)
                if doc_content:
                    documentation.append(doc_content)
                    
            # Write documentation
            doc_file = doc_path / "README.md"
            with open(doc_file, 'w') as f:
                f.write('\n'.join(documentation))
                
            logger.info(f"Documentation generated: {doc_file}")
            return True
            
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            return False
    
    def _extract_documentation(self, cobol_file: Path) -> str:
        """Extract documentation from COBOL source file"""
        try:
            with open(cobol_file, 'r') as f:
                content = f.read()
                
            lines = content.split('\n')
            doc_lines = []
            doc_lines.append(f"## {cobol_file.stem}\n")
            
            # Extract program information
            program_id = None
            author = None
            date_written = None
            
            for line in lines:
                line_upper = line.upper().strip()
                if 'PROGRAM-ID.' in line_upper:
                    program_id = line.split('.')[-1].strip()
                elif 'AUTHOR.' in line_upper:
                    author = line.split('.')[-1].strip()
                elif 'DATE-WRITTEN.' in line_upper:
                    date_written = line.split('.')[-1].strip()
                    
            if program_id:
                doc_lines.append(f"**Program ID:** {program_id}")
            if author:
                doc_lines.append(f"**Author:** {author}")
            if date_written:
                doc_lines.append(f"**Date Written:** {date_written}")
                
            doc_lines.append("")
            
            # Extract comments and structure
            current_division = None
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('*>'):
                    comment = stripped[2:].strip()
                    doc_lines.append(f"- {comment}")
                elif ' DIVISION.' in line.upper():
                    division = line.upper().split()[0]
                    doc_lines.append(f"\n### {division} Division")
                    current_division = division
                    
            doc_lines.append("\n")
            return '\n'.join(doc_lines)
            
        except Exception as e:
            logger.error(f"Failed to extract documentation from {cobol_file}: {e}")
            return ""
    
    def validate_syntax(self, source_code: str) -> Tuple[bool, List[str]]:
        """Validate COBOL syntax and structure"""
        errors = []
        lines = source_code.split('\n')
        
        # Check for required divisions
        divisions_found = set()
        for line in lines:
            line_upper = line.upper().strip()
            if ' DIVISION.' in line_upper:
                division = line_upper.split()[0]
                divisions_found.add(division)
                
        required_divisions = {'IDENTIFICATION', 'PROCEDURE'}
        missing_divisions = required_divisions - divisions_found
        if missing_divisions:
            errors.append(f"Missing required divisions: {', '.join(missing_divisions)}")
            
        # Check PROGRAM-ID presence
        has_program_id = any('PROGRAM-ID.' in line.upper() for line in lines)
        if not has_program_id:
            errors.append("Missing PROGRAM-ID in IDENTIFICATION DIVISION")
            
        # Check fixed format compliance if enabled
        if self.config.use_fixed_format:
            for i, line in enumerate(lines, 1):
                if len(line) > 80:
                    errors.append(f"Line {i}: Exceeds 80 characters in fixed format")
                    
        # Check for proper paragraph structure
        in_procedure_division = False
        for i, line in enumerate(lines, 1):
            line_upper = line.upper().strip()
            if 'PROCEDURE DIVISION.' in line_upper:
                in_procedure_division = True
            elif in_procedure_division and line_upper.endswith('.') and not line_upper.startswith(('IF ', 'ELSE', 'END-')):
                # Potential paragraph name - basic validation
                paragraph_name = line_upper[:-1]
                if ' ' in paragraph_name and not any(keyword in paragraph_name for keyword in ['PERFORM', 'MOVE', 'DISPLAY']):
                    errors.append(f"Line {i}: Invalid paragraph name format: {paragraph_name}")
                    
        return len(errors) == 0, errors
    
    def get_dependencies(self, source_file: str) -> List[str]:
        """Get list of COBOL dependencies (copybooks, called programs)"""
        dependencies = []
        
        try:
            with open(source_file, 'r') as f:
                content = f.read()
                
            lines = content.split('\n')
            for line in lines:
                line_upper = line.upper().strip()
                
                # Find COPY statements
                if 'COPY ' in line_upper:
                    # Extract copybook name
                    copy_part = line_upper.split('COPY ')[1].split('.')[0]
                    copybook = copy_part.strip()
                    if copybook not in dependencies:
                        dependencies.append(copybook)
                        
                # Find CALL statements
                elif 'CALL ' in line_upper:
                    # Extract called program name
                    call_part = line_upper.split('CALL ')[1].split()[0]
                    program = call_part.strip().strip('"\'')
                    if program not in dependencies:
                        dependencies.append(program)
                        
        except Exception as e:
            logger.error(f"Failed to analyze dependencies: {e}")
            
        return dependencies

# Factory function for easy instantiation
def create_cobol_toolchain(config: Optional[COBOLConfiguration] = None) -> COBOLToolchain:
    """Create and return configured COBOL toolchain instance"""
    return COBOLToolchain(config)

# Export configuration classes and toolchain
__all__ = [
    'COBOLToolchain',
    'COBOLConfiguration', 
    'COBOLStandard',
    'COBOLDialect',
    'create_cobol_toolchain'
] 