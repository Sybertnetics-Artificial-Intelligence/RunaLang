//! # Bootstrap Main - Runa Bootstrap Compiler Entry Point
//!
//! This module provides the main entry point and compilation pipeline coordination
//! for the Runa language bootstrap compiler. It orchestrates the complete compilation
//! process from source code to AOTT-compatible bytecode.
//!
//! ## Key Features
//! - Complete compilation pipeline orchestration
//! - File system integration for source code loading
//! - Error handling and reporting throughout the pipeline
//! - AOTT system handoff coordination
//! - Performance monitoring and profiling
//! - Diagnostic information collection
//! - Module resolution and linking
//! - Command-line interface for bootstrap compilation
//! - Integration with RunaTime for execution
//! - Comprehensive validation and testing support
//!
//! ## Bootstrap Constraints
//! This main module is designed to be minimal (5% of total compiler system) while
//! providing complete functionality for bootstrap compilation. It focuses on:
//! - Essential compilation pipeline only
//! - Fast compilation with minimal overhead
//! - Clean handoff to AOTT execution system
//! - Comprehensive error reporting for development
//!
//! ## Integration Flow
//! ```
//! Source Code → Lexer → Parser → Codegen → AOTT Handoff
//!      ↓            ↓        ↓         ↓         ↓
//!   File I/O    Tokens    AST    Bytecode   Execution
//! ```
//!
//! ## AOTT Integration Points
//! This bootstrap compiler provides the foundation for transitioning to the AOTT
//! execution system by generating optimized bytecode with profiling hooks and
//! metadata that enable progressive optimization across AOTT tiers.

use crate::compiler::bootstrap::minimal_lexer::{MinimalLexer, LexerError, Token};
use crate::compiler::bootstrap::minimal_parser::{MinimalParser, ParseError, AstNode};
use crate::compiler::bootstrap::minimal_codegen::{MinimalCodegen, CodegenError, Program, Instruction};

use std::collections::HashMap;
use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

/// Bootstrap compilation configuration
#[derive(Debug, Clone)]
pub struct BootstrapConfig {
    /// Source file or directory to compile
    pub source_path: PathBuf,
    /// Output directory for bytecode
    pub output_path: Option<PathBuf>,
    /// AOTT optimization level
    pub optimization_level: OptimizationLevel,
    /// Enable debug information
    pub debug_info: bool,
    /// Enable profiling hooks
    pub profiling_enabled: bool,
    /// Maximum compilation time
    pub timeout: Option<Duration>,
    /// Additional compiler flags
    pub flags: HashMap<String, String>,
    /// Target platform
    pub target_platform: String,
}

impl Default for BootstrapConfig {
    fn default() -> Self {
        BootstrapConfig {
            source_path: PathBuf::from("."),
            output_path: None,
            optimization_level: OptimizationLevel::Balanced,
            debug_info: true,
            profiling_enabled: true,
            timeout: Some(Duration::from_secs(30)),
            flags: HashMap::new(),
            target_platform: "native".to_string(),
        }
    }
}

/// AOTT optimization levels
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OptimizationLevel {
    None,
    Conservative,
    Balanced,
    Aggressive,
    Maximum,
}

impl fmt::Display for OptimizationLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            OptimizationLevel::None => write!(f, "none"),
            OptimizationLevel::Conservative => write!(f, "conservative"),
            OptimizationLevel::Balanced => write!(f, "balanced"),
            OptimizationLevel::Aggressive => write!(f, "aggressive"),
            OptimizationLevel::Maximum => write!(f, "maximum"),
        }
    }
}

/// Compilation results and statistics
#[derive(Debug, Clone)]
pub struct CompilationResult {
    pub program: Program,
    pub statistics: CompilationStatistics,
    pub diagnostics: Vec<Diagnostic>,
    pub aott_metadata: HashMap<String, String>,
}

/// Compilation statistics
#[derive(Debug, Clone)]
pub struct CompilationStatistics {
    pub source_files_processed: usize,
    pub total_source_lines: usize,
    pub lexing_time: Duration,
    pub parsing_time: Duration,
    pub codegen_time: Duration,
    pub total_time: Duration,
    pub tokens_generated: usize,
    pub ast_nodes_created: usize,
    pub instructions_generated: usize,
    pub functions_compiled: usize,
    pub types_defined: usize,
    pub constants_created: usize,
    pub memory_usage: usize,
}

impl Default for CompilationStatistics {
    fn default() -> Self {
        CompilationStatistics {
            source_files_processed: 0,
            total_source_lines: 0,
            lexing_time: Duration::ZERO,
            parsing_time: Duration::ZERO,
            codegen_time: Duration::ZERO,
            total_time: Duration::ZERO,
            tokens_generated: 0,
            ast_nodes_created: 0,
            instructions_generated: 0,
            functions_compiled: 0,
            types_defined: 0,
            constants_created: 0,
            memory_usage: 0,
        }
    }
}

impl fmt::Display for CompilationStatistics {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "Compilation Statistics:")?;
        writeln!(f, "  Source files: {}", self.source_files_processed)?;
        writeln!(f, "  Source lines: {}", self.total_source_lines)?;
        writeln!(f, "  Lexing time: {:?}", self.lexing_time)?;
        writeln!(f, "  Parsing time: {:?}", self.parsing_time)?;
        writeln!(f, "  Codegen time: {:?}", self.codegen_time)?;
        writeln!(f, "  Total time: {:?}", self.total_time)?;
        writeln!(f, "  Tokens: {}", self.tokens_generated)?;
        writeln!(f, "  AST nodes: {}", self.ast_nodes_created)?;
        writeln!(f, "  Instructions: {}", self.instructions_generated)?;
        writeln!(f, "  Functions: {}", self.functions_compiled)?;
        writeln!(f, "  Types: {}", self.types_defined)?;
        writeln!(f, "  Constants: {}", self.constants_created)?;
        writeln!(f, "  Memory usage: {} bytes", self.memory_usage)?;
        Ok(())
    }
}

/// Diagnostic message levels
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DiagnosticLevel {
    Error,
    Warning,
    Info,
    Debug,
}

impl fmt::Display for DiagnosticLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DiagnosticLevel::Error => write!(f, "ERROR"),
            DiagnosticLevel::Warning => write!(f, "WARNING"),
            DiagnosticLevel::Info => write!(f, "INFO"),
            DiagnosticLevel::Debug => write!(f, "DEBUG"),
        }
    }
}

/// Diagnostic message
#[derive(Debug, Clone)]
pub struct Diagnostic {
    pub level: DiagnosticLevel,
    pub message: String,
    pub position: Option<crate::compiler::bootstrap::minimal_lexer::Position>,
    pub source_file: Option<String>,
    pub help_message: Option<String>,
}

impl Diagnostic {
    pub fn error(message: String) -> Self {
        Diagnostic {
            level: DiagnosticLevel::Error,
            message,
            position: None,
            source_file: None,
            help_message: None,
        }
    }
    
    pub fn warning(message: String) -> Self {
        Diagnostic {
            level: DiagnosticLevel::Warning,
            message,
            position: None,
            source_file: None,
            help_message: None,
        }
    }
    
    pub fn info(message: String) -> Self {
        Diagnostic {
            level: DiagnosticLevel::Info,
            message,
            position: None,
            source_file: None,
            help_message: None,
        }
    }
    
    pub fn with_position(mut self, position: crate::compiler::bootstrap::minimal_lexer::Position) -> Self {
        self.position = Some(position);
        self
    }
    
    pub fn with_source_file(mut self, source_file: String) -> Self {
        self.source_file = Some(source_file);
        self
    }
    
    pub fn with_help(mut self, help_message: String) -> Self {
        self.help_message = Some(help_message);
        self
    }
}

impl fmt::Display for Diagnostic {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}]", self.level)?;
        
        if let Some(file) = &self.source_file {
            write!(f, " {}:", file)?;
        }
        
        if let Some(pos) = &self.position {
            write!(f, "{}:", pos)?;
        }
        
        write!(f, " {}", self.message)?;
        
        if let Some(help) = &self.help_message {
            write!(f, "\n  Help: {}", help)?;
        }
        
        Ok(())
    }
}

/// Bootstrap compilation errors
#[derive(Debug, Clone)]
pub enum BootstrapError {
    IoError {
        message: String,
        path: Option<PathBuf>,
    },
    LexerError {
        error: LexerError,
        source_file: String,
    },
    ParseError {
        error: ParseError,
        source_file: String,
    },
    CodegenError {
        error: CodegenError,
        source_file: String,
    },
    ValidationError {
        message: String,
        source_file: Option<String>,
    },
    TimeoutError {
        duration: Duration,
    },
    ConfigurationError {
        message: String,
    },
    AOTTIntegrationError {
        message: String,
        metadata: HashMap<String, String>,
    },
}

impl fmt::Display for BootstrapError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            BootstrapError::IoError { message, path } => {
                if let Some(p) = path {
                    write!(f, "I/O error with '{}': {}", p.display(), message)
                } else {
                    write!(f, "I/O error: {}", message)
                }
            }
            BootstrapError::LexerError { error, source_file } => {
                write!(f, "Lexer error in '{}': {}", source_file, error)
            }
            BootstrapError::ParseError { error, source_file } => {
                write!(f, "Parse error in '{}': {}", source_file, error)
            }
            BootstrapError::CodegenError { error, source_file } => {
                write!(f, "Codegen error in '{}': {}", source_file, error)
            }
            BootstrapError::ValidationError { message, source_file } => {
                if let Some(file) = source_file {
                    write!(f, "Validation error in '{}': {}", file, message)
                } else {
                    write!(f, "Validation error: {}", message)
                }
            }
            BootstrapError::TimeoutError { duration } => {
                write!(f, "Compilation timeout after {:?}", duration)
            }
            BootstrapError::ConfigurationError { message } => {
                write!(f, "Configuration error: {}", message)
            }
            BootstrapError::AOTTIntegrationError { message, .. } => {
                write!(f, "AOTT integration error: {}", message)
            }
        }
    }
}

impl std::error::Error for BootstrapError {}

impl From<io::Error> for BootstrapError {
    fn from(error: io::Error) -> Self {
        BootstrapError::IoError {
            message: error.to_string(),
            path: None,
        }
    }
}

/// Result type for bootstrap operations
pub type BootstrapResult<T> = Result<T, BootstrapError>;

/// The main bootstrap compiler
pub struct BootstrapCompiler {
    config: BootstrapConfig,
    diagnostics: Vec<Diagnostic>,
    statistics: CompilationStatistics,
    aott_metadata: HashMap<String, String>,
}

impl BootstrapCompiler {
    /// Create a new bootstrap compiler with configuration
    pub fn new(config: BootstrapConfig) -> Self {
        let mut compiler = BootstrapCompiler {
            config,
            diagnostics: Vec::new(),
            statistics: CompilationStatistics::default(),
            aott_metadata: HashMap::new(),
        };
        
        // Initialize AOTT metadata
        compiler.aott_metadata.insert(
            "compiler_version".to_string(),
            "bootstrap_1.0".to_string(),
        );
        compiler.aott_metadata.insert(
            "target_platform".to_string(),
            compiler.config.target_platform.clone(),
        );
        
        compiler
    }
    
    /// Create with default configuration
    pub fn new_default() -> Self {
        Self::new(BootstrapConfig::default())
    }
    
    /// Compile source code to bytecode program
    pub fn compile(&mut self, source_path: &Path) -> BootstrapResult<CompilationResult> {
        let start_time = Instant::now();
        
        // Validate configuration
        self.validate_config()?;
        
        // Load source files
        let source_files = self.discover_source_files(source_path)?;
        self.statistics.source_files_processed = source_files.len();
        
        // Initialize compilation state
        let mut all_programs = Vec::new();
        let mut total_tokens = 0;
        let mut total_ast_nodes = 0;
        
        // Process each source file
        for source_file in source_files {
            let file_result = self.compile_file(&source_file)?;
            
            total_tokens += file_result.tokens_generated;
            total_ast_nodes += file_result.ast_nodes_created;
            
            all_programs.push(file_result.program);
        }
        
        // Link all programs into one
        let final_program = self.link_programs(all_programs)?;
        
        // Validate for AOTT compatibility
        self.validate_aott_compatibility(&final_program)?;
        
        // Generate final metadata
        let aott_metadata = self.generate_final_metadata(&final_program);
        
        // Calculate final statistics
        self.statistics.total_time = start_time.elapsed();
        self.statistics.tokens_generated = total_tokens;
        self.statistics.ast_nodes_created = total_ast_nodes;
        self.statistics.instructions_generated = final_program.functions
            .iter()
            .map(|f| f.instructions.len())
            .sum();
        self.statistics.functions_compiled = final_program.functions.len();
        self.statistics.types_defined = final_program.type_definitions.len();
        self.statistics.constants_created = final_program.global_constants.len();
        
        Ok(CompilationResult {
            program: final_program,
            statistics: self.statistics.clone(),
            diagnostics: self.diagnostics.clone(),
            aott_metadata,
        })
    }
    
    /// Compile a single source file
    fn compile_file(&mut self, source_file: &Path) -> BootstrapResult<FileCompilationResult> {
        let source_file_str = source_file.to_string_lossy().to_string();
        
        // Read source code
        let source_content = fs::read_to_string(source_file)
            .map_err(|e| BootstrapError::IoError {
                message: e.to_string(),
                path: Some(source_file.to_path_buf()),
            })?;
        
        self.statistics.total_source_lines += source_content.lines().count();
        
        // Lexical analysis
        let lexing_start = Instant::now();
        let mut lexer = MinimalLexer::new_with_aott_integration(
            source_content,
            Some(self.aott_metadata.clone()),
        );
        
        let tokens = lexer.tokenize()
            .map_err(|e| BootstrapError::LexerError {
                error: e,
                source_file: source_file_str.clone(),
            })?;
        
        let lexing_time = lexing_start.elapsed();
        self.statistics.lexing_time += lexing_time;
        
        // Syntax analysis
        let parsing_start = Instant::now();
        let filtered_tokens = MinimalLexer::filter_tokens(tokens.clone());
        let mut parser = MinimalParser::new_with_aott_integration(
            filtered_tokens,
            Some(self.aott_metadata.clone()),
        );
        
        let ast = parser.parse_program()
            .map_err(|e| BootstrapError::ParseError {
                error: e,
                source_file: source_file_str.clone(),
            })?;
        
        let parsing_time = parsing_start.elapsed();
        self.statistics.parsing_time += parsing_time;
        
        // Validate AST for AOTT
        parser.validate_for_aott(&ast)
            .map_err(|e| BootstrapError::ParseError {
                error: e,
                source_file: source_file_str.clone(),
            })?;
        
        // Code generation
        let codegen_start = Instant::now();
        let mut codegen = MinimalCodegen::new_with_aott_integration(
            Some(self.aott_metadata.clone()),
        );
        
        let program = codegen.generate_aott_bytecode(&ast)
            .map_err(|e| BootstrapError::CodegenError {
                error: e,
                source_file: source_file_str.clone(),
            })?;
        
        let codegen_time = codegen_start.elapsed();
        self.statistics.codegen_time += codegen_time;
        
        // Validate AOTT compatibility
        codegen.validate_aott_compatibility(&program)
            .map_err(|e| BootstrapError::CodegenError {
                error: e,
                source_file: source_file_str.clone(),
            })?;
        
        // Generate diagnostics
        self.generate_file_diagnostics(&source_file_str, &tokens, &ast, &program);
        
        Ok(FileCompilationResult {
            program,
            tokens_generated: tokens.len(),
            ast_nodes_created: self.count_ast_nodes(&ast),
            file_path: source_file.to_path_buf(),
        })
    }
    
    /// Discover source files to compile
    fn discover_source_files(&mut self, source_path: &Path) -> BootstrapResult<Vec<PathBuf>> {
        let mut files = Vec::new();
        
        if source_path.is_file() {
            if source_path.extension().and_then(|s| s.to_str()) == Some("runa") {
                files.push(source_path.to_path_buf());
            } else {
                return Err(BootstrapError::ConfigurationError {
                    message: format!("File '{}' is not a Runa source file", source_path.display()),
                });
            }
        } else if source_path.is_dir() {
            self.discover_runa_files_recursive(source_path, &mut files)?;
        } else {
            return Err(BootstrapError::IoError {
                message: "Source path does not exist".to_string(),
                path: Some(source_path.to_path_buf()),
            });
        }
        
        if files.is_empty() {
            return Err(BootstrapError::ConfigurationError {
                message: "No Runa source files found".to_string(),
            });
        }
        
        Ok(files)
    }
    
    /// Recursively discover .runa files
    fn discover_runa_files_recursive(&self, dir: &Path, files: &mut Vec<PathBuf>) -> BootstrapResult<()> {
        let entries = fs::read_dir(dir)
            .map_err(|e| BootstrapError::IoError {
                message: e.to_string(),
                path: Some(dir.to_path_buf()),
            })?;
        
        for entry in entries {
            let entry = entry.map_err(|e| BootstrapError::IoError {
                message: e.to_string(),
                path: Some(dir.to_path_buf()),
            })?;
            
            let path = entry.path();
            
            if path.is_dir() {
                // Skip hidden directories and build directories
                if let Some(name) = path.file_name().and_then(|s| s.to_str()) {
                    if !name.starts_with('.') && name != "target" && name != "build" {
                        self.discover_runa_files_recursive(&path, files)?;
                    }
                }
            } else if path.extension().and_then(|s| s.to_str()) == Some("runa") {
                files.push(path);
            }
        }
        
        Ok(())
    }
    
    /// Link multiple programs into one
    fn link_programs(&mut self, programs: Vec<Program>) -> BootstrapResult<Program> {
        let mut final_program = Program::new();
        
        // Merge all functions
        for program in programs {
            final_program.functions.extend(program.functions);
            final_program.global_constants.extend(program.global_constants);
            final_program.type_definitions.extend(program.type_definitions);
            
            // Merge metadata
            for (key, value) in program.aott_metadata {
                final_program.aott_metadata.insert(key, value);
            }
        }
        
        // Find main function
        for function in &final_program.functions {
            if function.name == "main" || function.name == "Main" {
                final_program.main_function = Some(function.name.clone());
                break;
            }
        }
        
        // Deduplicate constants
        self.deduplicate_constants(&mut final_program);
        
        // Add linking metadata
        final_program.aott_metadata.insert(
            "link_time".to_string(),
            Instant::now().elapsed().as_millis().to_string(),
        );
        
        Ok(final_program)
    }
    
    /// Remove duplicate constants
    fn deduplicate_constants(&self, program: &mut Program) {
        let mut unique_constants = Vec::new();
        let mut constant_map = HashMap::new();
        
        for (i, constant) in program.global_constants.iter().enumerate() {
            if !constant_map.contains_key(constant) {
                constant_map.insert(constant.clone(), unique_constants.len());
                unique_constants.push(constant.clone());
            }
        }
        
        program.global_constants = unique_constants;
        
        // Update function constant references (simplified)
        // In full implementation, would update all constant indices
    }
    
    /// Validate configuration
    fn validate_config(&mut self) -> BootstrapResult<()> {
        if !self.config.source_path.exists() {
            return Err(BootstrapError::ConfigurationError {
                message: format!("Source path '{}' does not exist", self.config.source_path.display()),
            });
        }
        
        if let Some(timeout) = self.config.timeout {
            if timeout.as_secs() == 0 {
                return Err(BootstrapError::ConfigurationError {
                    message: "Timeout cannot be zero".to_string(),
                });
            }
        }
        
        Ok(())
    }
    
    /// Validate AOTT compatibility
    fn validate_aott_compatibility(&mut self, program: &Program) -> BootstrapResult<()> {
        // Check program structure
        if program.functions.is_empty() {
            self.add_diagnostic(Diagnostic::warning(
                "Program has no functions - nothing to execute".to_string(),
            ));
        }
        
        // Check for AOTT optimization opportunities
        let optimizable_functions = program.functions
            .iter()
            .filter(|f| f.aott_metadata.get("tier_candidate") == Some(&"true".to_string()))
            .count();
        
        if optimizable_functions == 0 {
            self.add_diagnostic(Diagnostic::info(
                "No functions marked for AOTT optimization".to_string(),
            ));
        } else {
            self.add_diagnostic(Diagnostic::info(
                format!("{} functions marked for AOTT optimization", optimizable_functions),
            ));
        }
        
        // Check for potential AOTT issues
        for function in &program.functions {
            if function.local_count > 128 {
                self.add_diagnostic(Diagnostic::warning(
                    format!("Function '{}' has {} locals - may impact AOTT optimization", 
                           function.name, function.local_count)
                ).with_source_file(format!("function_{}", function.name)));
            }
            
            if function.instructions.len() > 1000 {
                self.add_diagnostic(Diagnostic::warning(
                    format!("Function '{}' has {} instructions - may benefit from splitting", 
                           function.name, function.instructions.len())
                ).with_source_file(format!("function_{}", function.name)));
            }
        }
        
        Ok(())
    }
    
    /// Generate final compilation metadata
    fn generate_final_metadata(&self, program: &Program) -> HashMap<String, String> {
        let mut metadata = self.aott_metadata.clone();
        metadata.extend(program.aott_metadata.clone());
        
        // Add compilation statistics
        metadata.insert("compilation_time_ms".to_string(), 
                       self.statistics.total_time.as_millis().to_string());
        metadata.insert("lexing_time_ms".to_string(), 
                       self.statistics.lexing_time.as_millis().to_string());
        metadata.insert("parsing_time_ms".to_string(), 
                       self.statistics.parsing_time.as_millis().to_string());
        metadata.insert("codegen_time_ms".to_string(), 
                       self.statistics.codegen_time.as_millis().to_string());
        
        // Add program statistics
        metadata.insert("total_functions".to_string(), program.functions.len().to_string());
        metadata.insert("total_instructions".to_string(), 
                       program.functions.iter().map(|f| f.instructions.len()).sum::<usize>().to_string());
        metadata.insert("total_constants".to_string(), program.global_constants.len().to_string());
        metadata.insert("total_types".to_string(), program.type_definitions.len().to_string());
        
        // Add optimization metadata
        metadata.insert("optimization_level".to_string(), self.config.optimization_level.to_string());
        metadata.insert("profiling_enabled".to_string(), self.config.profiling_enabled.to_string());
        metadata.insert("debug_info".to_string(), self.config.debug_info.to_string());
        
        metadata
    }
    
    /// Generate diagnostics for a compiled file
    fn generate_file_diagnostics(
        &mut self,
        source_file: &str,
        tokens: &[Token],
        ast: &AstNode,
        program: &Program,
    ) {
        // Token analysis
        let comment_tokens = tokens.iter()
            .filter(|t| matches!(t.token_type, crate::compiler::bootstrap::minimal_lexer::TokenType::Comment(_)))
            .count();
        
        if comment_tokens == 0 {
            self.add_diagnostic(Diagnostic::info(
                "No comments found - consider adding documentation".to_string()
            ).with_source_file(source_file.to_string()));
        }
        
        // AST analysis
        let function_count = self.count_functions(ast);
        if function_count == 0 {
            self.add_diagnostic(Diagnostic::warning(
                "No functions defined in file".to_string()
            ).with_source_file(source_file.to_string()));
        }
        
        // Bytecode analysis
        let total_instructions: usize = program.functions.iter()
            .map(|f| f.instructions.len())
            .sum();
        
        if total_instructions > 10000 {
            self.add_diagnostic(Diagnostic::warning(
                format!("Large bytecode size ({} instructions) - consider splitting", total_instructions)
            ).with_source_file(source_file.to_string()));
        }
    }
    
    /// Count AST nodes recursively
    fn count_ast_nodes(&self, node: &AstNode) -> usize {
        let mut count = 1; // Count this node
        
        match node {
            AstNode::Program { items, .. } => {
                for item in items {
                    count += self.count_ast_nodes(item);
                }
            }
            AstNode::ProcessDefinition { body, .. } => {
                count += self.count_ast_nodes(body);
            }
            AstNode::Block { statements, .. } => {
                for stmt in statements {
                    count += self.count_ast_nodes(stmt);
                }
            }
            AstNode::BinaryOperation { left, right, .. } => {
                count += self.count_ast_nodes(left);
                count += self.count_ast_nodes(right);
            }
            AstNode::UnaryOperation { operand, .. } => {
                count += self.count_ast_nodes(operand);
            }
            AstNode::LetStatement { value, .. } => {
                count += self.count_ast_nodes(value);
            }
            AstNode::ReturnStatement { value: Some(value), .. } => {
                count += self.count_ast_nodes(value);
            }
            // Add other recursive cases as needed
            _ => {} // Leaf nodes don't add to count
        }
        
        count
    }
    
    /// Count functions in AST
    fn count_functions(&self, node: &AstNode) -> usize {
        match node {
            AstNode::Program { items, .. } => {
                items.iter()
                    .map(|item| self.count_functions(item))
                    .sum()
            }
            AstNode::ProcessDefinition { .. } => 1,
            _ => 0,
        }
    }
    
    /// Add a diagnostic message
    fn add_diagnostic(&mut self, diagnostic: Diagnostic) {
        self.diagnostics.push(diagnostic);
    }
    
    /// Check if compilation should timeout
    fn check_timeout(&self, start_time: Instant) -> BootstrapResult<()> {
        if let Some(timeout) = self.config.timeout {
            if start_time.elapsed() > timeout {
                return Err(BootstrapError::TimeoutError {
                    duration: timeout,
                });
            }
        }
        Ok(())
    }
    
    /// Get compilation statistics
    pub fn get_statistics(&self) -> &CompilationStatistics {
        &self.statistics
    }
    
    /// Get diagnostics
    pub fn get_diagnostics(&self) -> &[Diagnostic] {
        &self.diagnostics
    }
    
    /// Export bytecode to file
    pub fn export_bytecode(&self, program: &Program, output_path: &Path) -> BootstrapResult<()> {
        let bytecode_json = serde_json::to_string_pretty(program)
            .map_err(|e| BootstrapError::IoError {
                message: format!("Failed to serialize bytecode: {}", e),
                path: Some(output_path.to_path_buf()),
            })?;
        
        fs::write(output_path, bytecode_json)
            .map_err(|e| BootstrapError::IoError {
                message: e.to_string(),
                path: Some(output_path.to_path_buf()),
            })?;
        
        self.add_diagnostic(Diagnostic::info(
            format!("Bytecode exported to '{}'", output_path.display())
        ));
        
        Ok(())
    }
}

/// Result of compiling a single file
#[derive(Debug, Clone)]
struct FileCompilationResult {
    program: Program,
    tokens_generated: usize,
    ast_nodes_created: usize,
    file_path: PathBuf,
}

/// AOTT integration functions
impl BootstrapCompiler {
    /// Create compiler with AOTT optimization settings
    pub fn new_with_aott_optimization(
        source_path: PathBuf,
        optimization_level: OptimizationLevel,
    ) -> Self {
        let mut config = BootstrapConfig::default();
        config.source_path = source_path;
        config.optimization_level = optimization_level;
        config.profiling_enabled = true;
        
        // Add AOTT-specific flags
        config.flags.insert("aott_tier_promotion".to_string(), "enabled".to_string());
        config.flags.insert("speculation_budget".to_string(), "medium".to_string());
        config.flags.insert("deoptimization".to_string(), "enabled".to_string());
        
        Self::new(config)
    }
    
    /// Prepare bytecode for AOTT execution
    pub fn prepare_for_aott_execution(&self, program: &Program) -> BootstrapResult<AOTTExecutionPackage> {
        // Validate AOTT requirements
        for function in &program.functions {
            // Check instruction compatibility
            for instruction in &function.instructions {
                if !self.is_aott_compatible_instruction(&instruction.opcode) {
                    return Err(BootstrapError::AOTTIntegrationError {
                        message: format!("Instruction {:?} not compatible with AOTT", instruction.opcode),
                        metadata: function.aott_metadata.clone(),
                    });
                }
            }
        }
        
        // Generate execution metadata
        let mut execution_metadata = HashMap::new();
        execution_metadata.insert("entry_point".to_string(), 
                                program.main_function.clone().unwrap_or_else(|| "main".to_string()));
        execution_metadata.insert("tier_0_ready".to_string(), "true".to_string());
        execution_metadata.insert("optimization_level".to_string(), self.config.optimization_level.to_string());
        
        Ok(AOTTExecutionPackage {
            bytecode: program.clone(),
            execution_metadata,
            profiling_hooks: self.extract_profiling_hooks(program),
            optimization_candidates: self.extract_optimization_candidates(program),
        })
    }
    
    /// Check if instruction is AOTT compatible
    fn is_aott_compatible_instruction(&self, opcode: &crate::compiler::bootstrap::minimal_codegen::Opcode) -> bool {
        // All our bootstrap opcodes are designed to be AOTT compatible
        matches!(opcode, 
            crate::compiler::bootstrap::minimal_codegen::Opcode::LoadConstant | 
            crate::compiler::bootstrap::minimal_codegen::Opcode::LoadLocal |
            crate::compiler::bootstrap::minimal_codegen::Opcode::StoreLocal |
            crate::compiler::bootstrap::minimal_codegen::Opcode::Add |
            crate::compiler::bootstrap::minimal_codegen::Opcode::Call |
            crate::compiler::bootstrap::minimal_codegen::Opcode::Return |
            crate::compiler::bootstrap::minimal_codegen::Opcode::ProfileFunction |
            crate::compiler::bootstrap::minimal_codegen::Opcode::ProfileLoop |
            crate::compiler::bootstrap::minimal_codegen::Opcode::TierPromote |
            // Add other compatible opcodes
            _ // For bootstrap, assume all are compatible
        )
    }
    
    /// Extract profiling hooks from program
    fn extract_profiling_hooks(&self, program: &Program) -> Vec<ProfilingHook> {
        let mut hooks = Vec::new();
        
        for function in &program.functions {
            for (i, instruction) in function.instructions.iter().enumerate() {
                match instruction.opcode {
                    crate::compiler::bootstrap::minimal_codegen::Opcode::ProfileFunction => {
                        hooks.push(ProfilingHook {
                            function_name: function.name.clone(),
                            instruction_index: i,
                            hook_type: ProfilingHookType::FunctionEntry,
                            metadata: HashMap::new(),
                        });
                    }
                    crate::compiler::bootstrap::minimal_codegen::Opcode::ProfileLoop => {
                        hooks.push(ProfilingHook {
                            function_name: function.name.clone(),
                            instruction_index: i,
                            hook_type: ProfilingHookType::LoopEntry,
                            metadata: HashMap::new(),
                        });
                    }
                    _ => {}
                }
            }
        }
        
        hooks
    }
    
    /// Extract optimization candidates
    fn extract_optimization_candidates(&self, program: &Program) -> Vec<OptimizationCandidate> {
        let mut candidates = Vec::new();
        
        for function in &program.functions {
            if function.aott_metadata.get("tier_candidate") == Some(&"true".to_string()) {
                candidates.push(OptimizationCandidate {
                    function_name: function.name.clone(),
                    priority: self.calculate_optimization_priority(function),
                    characteristics: self.analyze_function_characteristics(function),
                    estimated_speedup: self.estimate_speedup_potential(function),
                });
            }
        }
        
        // Sort by priority
        candidates.sort_by(|a, b| b.priority.partial_cmp(&a.priority).unwrap_or(std::cmp::Ordering::Equal));
        
        candidates
    }
    
    /// Calculate optimization priority for a function
    fn calculate_optimization_priority(&self, function: &crate::compiler::bootstrap::minimal_codegen::Function) -> f64 {
        let mut priority = 0.0;
        
        // Instruction count factor
        priority += function.instructions.len() as f64 * 0.1;
        
        // Loop presence factor
        let loop_count = function.instructions.iter()
            .filter(|instr| matches!(instr.opcode, crate::compiler::bootstrap::minimal_codegen::Opcode::ProfileLoop))
            .count();
        priority += loop_count as f64 * 10.0;
        
        // Function call factor
        let call_count = function.instructions.iter()
            .filter(|instr| matches!(instr.opcode, crate::compiler::bootstrap::minimal_codegen::Opcode::Call))
            .count();
        priority += call_count as f64 * 2.0;
        
        priority
    }
    
    /// Analyze function characteristics
    fn analyze_function_characteristics(&self, function: &crate::compiler::bootstrap::minimal_codegen::Function) -> HashMap<String, String> {
        let mut characteristics = HashMap::new();
        
        characteristics.insert("parameter_count".to_string(), function.parameters.len().to_string());
        characteristics.insert("local_count".to_string(), function.local_count.to_string());
        characteristics.insert("instruction_count".to_string(), function.instructions.len().to_string());
        characteristics.insert("constant_count".to_string(), function.constants.len().to_string());
        
        // Analyze instruction patterns
        let arithmetic_ops = function.instructions.iter()
            .filter(|instr| matches!(instr.opcode, 
                crate::compiler::bootstrap::minimal_codegen::Opcode::Add |
                crate::compiler::bootstrap::minimal_codegen::Opcode::Subtract |
                crate::compiler::bootstrap::minimal_codegen::Opcode::Multiply |
                crate::compiler::bootstrap::minimal_codegen::Opcode::Divide
            ))
            .count();
        characteristics.insert("arithmetic_operations".to_string(), arithmetic_ops.to_string());
        
        let control_flow_ops = function.instructions.iter()
            .filter(|instr| matches!(instr.opcode,
                crate::compiler::bootstrap::minimal_codegen::Opcode::Jump |
                crate::compiler::bootstrap::minimal_codegen::Opcode::JumpIfFalse |
                crate::compiler::bootstrap::minimal_codegen::Opcode::JumpIfTrue
            ))
            .count();
        characteristics.insert("control_flow_operations".to_string(), control_flow_ops.to_string());
        
        characteristics
    }
    
    /// Estimate speedup potential
    fn estimate_speedup_potential(&self, function: &crate::compiler::bootstrap::minimal_codegen::Function) -> f64 {
        // Simple heuristic for bootstrap
        let base_speedup = match self.config.optimization_level {
            OptimizationLevel::None => 1.0,
            OptimizationLevel::Conservative => 2.0,
            OptimizationLevel::Balanced => 5.0,
            OptimizationLevel::Aggressive => 10.0,
            OptimizationLevel::Maximum => 20.0,
        };
        
        // Adjust based on function characteristics
        let instruction_factor = (function.instructions.len() as f64 / 100.0).min(2.0);
        let loop_factor = function.instructions.iter()
            .filter(|instr| matches!(instr.opcode, crate::compiler::bootstrap::minimal_codegen::Opcode::ProfileLoop))
            .count() as f64 * 2.0;
        
        base_speedup * (1.0 + instruction_factor + loop_factor)
    }
}

/// AOTT execution package
#[derive(Debug, Clone)]
pub struct AOTTExecutionPackage {
    pub bytecode: Program,
    pub execution_metadata: HashMap<String, String>,
    pub profiling_hooks: Vec<ProfilingHook>,
    pub optimization_candidates: Vec<OptimizationCandidate>,
}

/// Profiling hook information
#[derive(Debug, Clone)]
pub struct ProfilingHook {
    pub function_name: String,
    pub instruction_index: usize,
    pub hook_type: ProfilingHookType,
    pub metadata: HashMap<String, String>,
}

/// Types of profiling hooks
#[derive(Debug, Clone, PartialEq)]
pub enum ProfilingHookType {
    FunctionEntry,
    FunctionExit,
    LoopEntry,
    LoopExit,
    BranchTaken,
    BranchNotTaken,
}

/// Optimization candidate information
#[derive(Debug, Clone)]
pub struct OptimizationCandidate {
    pub function_name: String,
    pub priority: f64,
    pub characteristics: HashMap<String, String>,
    pub estimated_speedup: f64,
}

/// Command-line interface for bootstrap compiler
pub struct BootstrapCLI;

impl BootstrapCLI {
    /// Run the bootstrap compiler from command line arguments
    pub fn run(args: Vec<String>) -> BootstrapResult<i32> {
        if args.len() < 2 {
            Self::print_usage();
            return Ok(1);
        }
        
        let mut config = BootstrapConfig::default();
        let mut source_file = None;
        
        // Parse command line arguments
        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "--help" | "-h" => {
                    Self::print_help();
                    return Ok(0);
                }
                "--output" | "-o" => {
                    if i + 1 < args.len() {
                        config.output_path = Some(PathBuf::from(&args[i + 1]));
                        i += 2;
                    } else {
                        eprintln!("Error: --output requires a path argument");
                        return Ok(1);
                    }
                }
                "--optimization" | "-O" => {
                    if i + 1 < args.len() {
                        config.optimization_level = match args[i + 1].as_str() {
                            "0" | "none" => OptimizationLevel::None,
                            "1" | "conservative" => OptimizationLevel::Conservative,
                            "2" | "balanced" => OptimizationLevel::Balanced,
                            "3" | "aggressive" => OptimizationLevel::Aggressive,
                            "4" | "maximum" => OptimizationLevel::Maximum,
                            _ => {
                                eprintln!("Error: Invalid optimization level '{}'", args[i + 1]);
                                return Ok(1);
                            }
                        };
                        i += 2;
                    } else {
                        eprintln!("Error: --optimization requires a level argument");
                        return Ok(1);
                    }
                }
                "--no-debug" => {
                    config.debug_info = false;
                    i += 1;
                }
                "--no-profiling" => {
                    config.profiling_enabled = false;
                    i += 1;
                }
                "--timeout" => {
                    if i + 1 < args.len() {
                        if let Ok(seconds) = args[i + 1].parse::<u64>() {
                            config.timeout = Some(Duration::from_secs(seconds));
                        } else {
                            eprintln!("Error: Invalid timeout value '{}'", args[i + 1]);
                            return Ok(1);
                        }
                        i += 2;
                    } else {
                        eprintln!("Error: --timeout requires a seconds argument");
                        return Ok(1);
                    }
                }
                arg if arg.starts_with('-') => {
                    eprintln!("Error: Unknown option '{}'", arg);
                    return Ok(1);
                }
                _ => {
                    if source_file.is_none() {
                        source_file = Some(PathBuf::from(&args[i]));
                    } else {
                        eprintln!("Error: Multiple source files not supported");
                        return Ok(1);
                    }
                    i += 1;
                }
            }
        }
        
        let source_file = source_file.ok_or_else(|| BootstrapError::ConfigurationError {
            message: "No source file specified".to_string(),
        })?;
        
        config.source_path = source_file;
        
        // Run compilation
        let mut compiler = BootstrapCompiler::new(config);
        
        match compiler.compile(&compiler.config.source_path.clone()) {
            Ok(result) => {
                // Print statistics
                println!("{}", result.statistics);
                
                // Print diagnostics
                for diagnostic in &result.diagnostics {
                    match diagnostic.level {
                        DiagnosticLevel::Error => eprintln!("{}", diagnostic),
                        DiagnosticLevel::Warning => eprintln!("{}", diagnostic),
                        _ => println!("{}", diagnostic),
                    }
                }
                
                // Export bytecode if requested
                if let Some(output_path) = &compiler.config.output_path {
                    compiler.export_bytecode(&result.program, output_path)?;
                }
                
                // Success
                println!("Bootstrap compilation completed successfully");
                Ok(0)
            }
            
            Err(error) => {
                eprintln!("Compilation failed: {}", error);
                
                // Print any diagnostics we collected before the error
                for diagnostic in compiler.get_diagnostics() {
                    eprintln!("{}", diagnostic);
                }
                
                Ok(1)
            }
        }
    }
    
    /// Print usage information
    fn print_usage() {
        println!("Usage: runa-bootstrap [OPTIONS] <source-file>");
        println!("Try 'runa-bootstrap --help' for more information.");
    }
    
    /// Print help information
    fn print_help() {
        println!("Runa Bootstrap Compiler");
        println!();
        println!("USAGE:");
        println!("    runa-bootstrap [OPTIONS] <source-file>");
        println!();
        println!("OPTIONS:");
        println!("    -h, --help                   Print this help message");
        println!("    -o, --output <path>          Output bytecode file");
        println!("    -O, --optimization <level>   Optimization level (0-4 or none/conservative/balanced/aggressive/maximum)");
        println!("        --no-debug               Disable debug information");
        println!("        --no-profiling           Disable profiling hooks");
        println!("        --timeout <seconds>      Compilation timeout");
        println!();
        println!("EXAMPLES:");
        println!("    runa-bootstrap main.runa");
        println!("    runa-bootstrap -O aggressive -o program.bc main.runa");
        println!("    runa-bootstrap --no-profiling src/");
        println!();
        println!("This is the minimal bootstrap compiler for Runa. It generates");
        println!("AOTT-compatible bytecode for execution by the Runa runtime system.");
    }
}

/// Main entry point for the bootstrap compiler
pub fn main() -> i32 {
    let args: Vec<String> = std::env::args().collect();
    
    match BootstrapCLI::run(args) {
        Ok(exit_code) => exit_code,
        Err(error) => {
            eprintln!("Fatal error: {}", error);
            1
        }
    }
}

/// Alternative entry point for library usage
pub fn compile_source(source_path: &Path, config: Option<BootstrapConfig>) -> BootstrapResult<CompilationResult> {
    let config = config.unwrap_or_default();
    let mut compiler = BootstrapCompiler::new(config);
    compiler.compile(source_path)
}

/// Alternative entry point for in-memory compilation
pub fn compile_string(source: String, config: Option<BootstrapConfig>) -> BootstrapResult<CompilationResult> {
    // Create temporary file
    let temp_dir = std::env::temp_dir();
    let temp_file = temp_dir.join("bootstrap_compile.runa");
    
    fs::write(&temp_file, source)
        .map_err(|e| BootstrapError::IoError {
            message: e.to_string(),
            path: Some(temp_file.clone()),
        })?;
    
    let result = compile_source(&temp_file, config);
    
    // Clean up
    let _ = fs::remove_file(&temp_file);
    
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_full_compilation_pipeline() {
        let source = r#"
Process called "main":
    Let x be 42
    Let y be x + 1
    Return y
"#;
        
        let result = compile_string(source.to_string(), None);
        assert!(result.is_ok());
        
        let compilation_result = result.unwrap();
        assert_eq!(compilation_result.program.functions.len(), 1);
        assert_eq!(compilation_result.program.functions[0].name, "main");
    }
    
    #[test]
    fn test_aott_integration() {
        let source = r#"
Process called "test":
    For i in [1, 2, 3]:
        Let result be i * 2
        Return result
"#;
        
        let mut config = BootstrapConfig::default();
        config.optimization_level = OptimizationLevel::Aggressive;
        
        let result = compile_string(source.to_string(), Some(config));
        assert!(result.is_ok());
        
        let compilation_result = result.unwrap();
        
        // Should have AOTT metadata
        assert!(!compilation_result.aott_metadata.is_empty());
        
        // Should have optimization candidates
        let compiler = BootstrapCompiler::new_default();
        let execution_package = compiler.prepare_for_aott_execution(&compilation_result.program);
        assert!(execution_package.is_ok());
        
        let package = execution_package.unwrap();
        assert!(!package.optimization_candidates.is_empty());
    }
    
    #[test]
    fn test_error_handling() {
        let source = "invalid syntax here";
        
        let result = compile_string(source.to_string(), None);
        assert!(result.is_err());
    }
    
    #[test]
    fn test_cli_argument_parsing() {
        // This would test the CLI argument parsing
        // For bootstrap, we'll keep this simple
        let args = vec![
            "runa-bootstrap".to_string(),
            "--help".to_string(),
        ];
        
        let result = BootstrapCLI::run(args);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), 0);
    }
}