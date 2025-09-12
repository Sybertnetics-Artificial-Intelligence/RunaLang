mod lexer;
mod parser;
mod semantic;
mod codegen;
mod disassembler;

use lexer::Lexer;
use parser::Parser;
use semantic::SemanticAnalyzer;
use codegen::CodeGenerator;
// use runa_rt::vm::{VirtualMachine, InterpretResult};  // Temporarily disabled
use runa_common::token::TokenType;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 2 {
        println!("Usage: {} <runa_file>", args[0]);
        return Ok(());
    }
    
    let filename = &args[1];
    let source = fs::read_to_string(filename)?;
    
    println!("=== Runa Lexer Test ===");
    println!("File: {}", filename);
    println!("Source length: {} characters", source.len());
    println!();
    
    // Test the lexer
    let mut lexer = Lexer::new(&source);
    match lexer.scan_tokens() {
        Ok(tokens) => {
            println!("✅ Lexer completed successfully!");
            println!("Generated {} tokens:", tokens.len());
            println!();
            
            for (i, token) in tokens.iter().enumerate() {
                println!("{:3}: {:?} '{}' (line {}, col {})", 
                    i, token.token_type, token.lexeme, token.line, token.column);
            }
            
            println!();
            println!("=== Token Statistics ===");
            let mut token_counts = std::collections::HashMap::new();
            for token in &tokens {
                *token_counts.entry(format!("{:?}", token.token_type)).or_insert(0) += 1;
            }
            
            for (token_type, count) in token_counts {
                println!("{:30}: {}", token_type, count);
            }
            
            // Now run the full compiler pipeline
            println!();
            println!("=== Full Compiler Pipeline ===");
            
            // Step 1: Parse
            println!("Starting parser...");
            let mut parser = Parser::new(tokens);
            println!("Parser created, about to parse...");
            match parser.parse() {
                Ok(ast) => {
                    println!("✅ Parser completed successfully!");
                    println!("Generated {} statements", ast.len());
                    
                    // Step 2: Semantic Analysis
                    println!("Starting semantic analysis...");
                    let mut analyzer = SemanticAnalyzer::new();
                    match analyzer.analyze(&ast) {
                        Ok(()) => {
                            println!("✅ Semantic analysis completed successfully!");
                            
                            // Step 3: Code Generation
                            println!("Starting code generation...");
                            match CodeGenerator::compile(&ast) {
                                Ok(chunk) => {
                                    println!("✅ Code generation completed successfully!");
                                    println!("Generated {} bytes of bytecode", chunk.code.len());
                                    println!("Constants: {:?}", chunk.constants);
                                    
                                    // Step 4: VM Execution (temporarily disabled)
                                    println!();
                                    println!("=== VM Execution (Disabled) ===");
                                    println!("✅ Compilation pipeline completed successfully!");
                                    println!("VM execution skipped - runtime compatibility pending");
                                    /*
                                    let mut vm = VirtualMachine::new();
                                    match vm.interpret_with_chunk(chunk) {
                                        InterpretResult::Ok => {
                                            println!("✅ VM execution completed successfully!");
                                        }
                                        InterpretResult::RuntimeError => {
                                            println!("❌ VM execution error: Runtime error occurred");
                                            return Err("VM runtime error".into());
                                        }
                                        InterpretResult::CompileError => {
                                            println!("❌ VM execution error: Compile error occurred");
                                            return Err("VM compile error".into());
                                        }
                                    }
                                    */
                                }
                                Err(error) => {
                                    println!("❌ Code generation error: {}", error);
                                    return Err(error.into());
                                }
                            }
                        }
                        Err(error) => {
                            println!("❌ Semantic analysis error: {}", error);
                            return Err(error.into());
                        }
                    }
                }
                Err(error) => {
                    println!("❌ Parser error: {}", error);
                    return Err(error.into());
                }
            }
            
        }
        Err(e) => {
            println!("❌ Lexer error: {}", e);
            return Err(e.into());
        }
    }
    
    Ok(())
}

