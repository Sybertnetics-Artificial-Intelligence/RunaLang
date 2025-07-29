mod lexer;
mod parser;
mod semantic;
mod codegen;
mod disassembler;

use lexer::Lexer;
use parser::Parser;
use semantic::SemanticAnalyzer;
use codegen::CodeGenerator;
use runa_rt::vm::VirtualMachine;
use runa_common::bytecode::Chunk;
use std::env;
use std::fs;

fn main() {
    println!("--- Runa Compiler & VM ---");

    let args: Vec<String> = env::args().collect();
    let source_code = if args.len() > 1 {
        let filename = &args[1];
        match fs::read_to_string(filename) {
            Ok(contents) => contents,
            Err(e) => {
                eprintln!("Failed to read file {}: {}", filename, e);
                return;
            }
        }
    } else {
        // Final test program
        r#"
Let a = 0
For i from 0 to 10
    a = a + i
Return a
"#.to_string()
    };

    println!("Compiling and running source:{}", source_code);

    // 1. Lexing
    let mut lexer = Lexer::new(&source_code);
    let tokens = match lexer.scan_tokens() {
        Ok(tokens) => tokens.to_vec(),
        Err(e) => {
            eprintln!("Lexing error: {}", e);
            return;
        }
    };

    // 2. Parsing
    let mut parser = Parser::new(tokens.clone());
    let ast = match parser.parse() {
        Ok(ast) => ast,
        Err(e) => {
            eprintln!("Parsing error: {}", e);
            return;
        }
    };

    // 3. Semantic Analysis
    let mut analyzer = SemanticAnalyzer::new();
    if let Err(e) = analyzer.analyze(&ast) {
        eprintln!("Semantic analysis error: {}", e);
        return;
    }

    // 3.5. AST Dump for debugging
    println!("\n--- AST Dump ---");
    for (i, stmt) in ast.iter().enumerate() {
        println!("Statement {}: {:?}", i, stmt);
    }
    println!("--- End AST Dump ---\n");

    // 4. Code Generation
    match CodeGenerator::compile(&ast) {
        Ok(chunk) => {
            println!("\n--- Disassembly ---");
            disassembler::disassemble_chunk(&chunk, "main");
            
            println!("\n--- VM Execution ---");
            VirtualMachine::interpret(chunk);
        }
        Err(e) => {
            eprintln!("Code generation error: {}", e);
            return;
        }
    }
    
    // Test error handling with malformed bytecode
    println!("\n=== Testing Error Handling ===");
    let mut malformed_chunk = Chunk::new();
    malformed_chunk.write(0); // Constant
    malformed_chunk.write(0); // index
    malformed_chunk.write(255); // Unknown opcode
    malformed_chunk.write(0); // Constant
    // Missing operand for Constant
    
    disassembler::disassemble_chunk(&malformed_chunk, "malformed");
}
