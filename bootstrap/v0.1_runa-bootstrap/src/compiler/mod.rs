pub mod frontend;
pub mod middle;
pub mod backend;

use anyhow::Result;
use std::path::Path;

use crate::utils::diagnostics::DiagnosticEngine;
use frontend::{lexer::Lexer, parser::Parser};
use middle::{semantic::SemanticAnalyzer, type_checker::TypeChecker};
use backend::{llvm::LLVMBackend, codegen::CodeGenerator};

pub struct CompilerDriver<'a> {
    diagnostic_engine: &'a mut DiagnosticEngine,
}

impl<'a> CompilerDriver<'a> {
    pub fn new(diagnostic_engine: &'a mut DiagnosticEngine) -> Self {
        Self {
            diagnostic_engine,
        }
    }

    pub fn compile_file(&mut self, input: &Path, output: &Path, target: &str, opt_level: u8) -> Result<()> {
        // Frontend: Lexing and Parsing
        let source = std::fs::read_to_string(input)?;
        let mut lexer = Lexer::new(&source, input);
        let tokens = lexer.tokenize(self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        let mut parser = Parser::new(tokens);
        let ast = parser.parse(self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        // Middle-end: Semantic Analysis and Type Checking
        let mut semantic_analyzer = SemanticAnalyzer::new();
        let analyzed_ast = semantic_analyzer.analyze(ast, self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        let mut type_checker = TypeChecker::new();
        let typed_ast = type_checker.check_types(analyzed_ast, self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        // Backend: Code Generation
        let llvm_backend = LLVMBackend::new(target, opt_level)?;
        let mut code_generator = CodeGenerator::new(llvm_backend);
        code_generator.generate(typed_ast, output)?;

        Ok(())
    }

    pub fn check_file(&mut self, input: &Path) -> Result<()> {
        // Only run frontend and middle-end for syntax checking
        let source = std::fs::read_to_string(input)?;
        let mut lexer = Lexer::new(&source, input);
        let tokens = lexer.tokenize(self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        let mut parser = Parser::new(tokens);
        let ast = parser.parse(self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        let mut semantic_analyzer = SemanticAnalyzer::new();
        let analyzed_ast = semantic_analyzer.analyze(ast, self.diagnostic_engine)?;
        
        if self.diagnostic_engine.has_errors() {
            return Ok(());
        }

        let mut type_checker = TypeChecker::new();
        let _typed_ast = type_checker.check_types(analyzed_ast, self.diagnostic_engine)?;

        Ok(())
    }
}