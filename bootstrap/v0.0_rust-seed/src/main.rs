use std::env;
use std::fs;
use std::process;

mod lexer;
mod parser;
mod codegen;
mod typechecker;

use lexer::Lexer;
use parser::Parser;
use codegen::CodeGenerator;
use typechecker::TypeChecker;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <input.runa> <output>", args[0]);
        process::exit(1);
    }

    let input_file = &args[1];
    let output_file = &args[2];

    // Read source file
    let source = match fs::read_to_string(input_file) {
        Ok(content) => content,
        Err(err) => {
            eprintln!("Error reading file {}: {}", input_file, err);
            process::exit(1);
        }
    };

    // Tokenize
    let mut lexer = Lexer::new(&source);
    let tokens = match lexer.tokenize() {
        Ok(tokens) => {
            // Debug: print tokens if output is "debug"
            if output_file == "debug" {
                for token in &tokens {
                    println!("{:?}", token);
                }
                process::exit(0);
            }
            tokens
        },
        Err(err) => {
            eprintln!("Lexer error: {}", err);
            process::exit(1);
        }
    };

    // Parse
    let mut parser = Parser::new(tokens);
    let ast = match parser.parse() {
        Ok(ast) => ast,
        Err(err) => {
            eprintln!("Parser error: {}", err);
            process::exit(1);
        }
    };

    // Type check
    let mut typechecker = TypeChecker::new();
    if let Err(err) = typechecker.check(&ast) {
        eprintln!("Type error: {}", err);
        process::exit(1);
    }

    // Generate code
    let mut codegen = CodeGenerator::new();
    let assembly = match codegen.generate(&ast) {
        Ok(asm) => asm,
        Err(err) => {
            eprintln!("Code generation error: {}", err);
            process::exit(1);
        }
    };

    // Write assembly to file
    let asm_file = format!("{}.s", output_file);
    if let Err(err) = fs::write(&asm_file, assembly) {
        eprintln!("Error writing assembly file: {}", err);
        process::exit(1);
    }

    // Assemble and link
    let status = process::Command::new("gcc")
        .args(&["-o", output_file, &asm_file])
        .status();

    match status {
        Ok(exit_status) => {
            if exit_status.success() {
                println!("Successfully compiled {} to {}", input_file, output_file);
            } else {
                eprintln!("Assembly/linking failed");
                process::exit(1);
            }
        }
        Err(err) => {
            eprintln!("Error invoking gcc: {}", err);
            process::exit(1);
        }
    }
}
