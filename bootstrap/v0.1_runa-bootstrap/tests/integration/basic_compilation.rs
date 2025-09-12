// Integration tests for basic compilation functionality

use runa_bootstrap::compiler::CompilerDriver;
use runa_bootstrap::utils::diagnostics::DiagnosticEngine;
use std::fs;
use std::path::PathBuf;
use tempfile::TempDir;

#[test]
fn test_compile_simple_program() {
    let temp_dir = TempDir::new().expect("Failed to create temp directory");
    let input_file = temp_dir.path().join("simple.runa");
    let output_file = temp_dir.path().join("simple");
    
    // Write a simple Runa program
    let program = r#"
Process called "main" returns Integer:
    Return 42
End Process
    "#;
    
    fs::write(&input_file, program).expect("Failed to write test file");
    
    let mut diagnostic_engine = DiagnosticEngine::new();
    let mut compiler = CompilerDriver::new(&mut diagnostic_engine);
    
    // This should compile without errors (though may not link successfully without proper runtime)
    let result = compiler.compile_file(&input_file, &output_file, "host", 2);
    
    // Check that no compile errors occurred
    assert!(!diagnostic_engine.has_errors(), 
           "Compilation should succeed: {:?}", diagnostic_engine.diagnostics());
    
    if let Err(e) = result {
        // It's OK if the final linking fails, we're just testing parsing and code generation
        println!("Note: Final linking may fail in test environment: {}", e);
    }
}

#[test]
fn test_syntax_check() {
    let temp_dir = TempDir::new().expect("Failed to create temp directory");
    let input_file = temp_dir.path().join("syntax_test.runa");
    
    // Write a program with valid syntax
    let program = r#"
Process called "test" that takes x as Integer returns Integer:
    Let result be x + 1
    Return result
End Process
    "#;
    
    fs::write(&input_file, program).expect("Failed to write test file");
    
    let mut diagnostic_engine = DiagnosticEngine::new();
    let mut compiler = CompilerDriver::new(&mut diagnostic_engine);
    
    let result = compiler.check_file(&input_file);
    
    assert!(result.is_ok(), "Syntax check should succeed");
    assert!(!diagnostic_engine.has_errors(), 
           "Should have no syntax errors: {:?}", diagnostic_engine.diagnostics());
}

#[test]
fn test_syntax_error_detection() {
    let temp_dir = TempDir::new().expect("Failed to create temp directory");
    let input_file = temp_dir.path().join("error_test.runa");
    
    // Write a program with syntax errors
    let program = r#"
Process called test returns Integer  // Missing quotes and colon
    Let x be  // Missing initializer
    Return x
End Process
    "#;
    
    fs::write(&input_file, program).expect("Failed to write test file");
    
    let mut diagnostic_engine = DiagnosticEngine::new();
    let mut compiler = CompilerDriver::new(&mut diagnostic_engine);
    
    let _result = compiler.check_file(&input_file);
    
    // Should have detected syntax errors
    assert!(diagnostic_engine.has_errors(), 
           "Should detect syntax errors");
    assert!(diagnostic_engine.error_count() > 0, 
           "Should have at least one error");
}