mod lexer;
mod parser;
mod codegen;

use lexer::Lexer;
use parser::Parser;
use codegen::CodeGenerator;
use std::env;
use std::fs;
use std::process::Command;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <source.runa> [output.s]", args[0]);
        std::process::exit(1);
    }

    let input_file = &args[1];
    let output_file = if args.len() >= 3 {
        args[2].clone()
    } else {
        format!("{}.s", input_file.trim_end_matches(".runa"))
    };

    // Read source file
    let source = match fs::read_to_string(input_file) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file {}: {}", input_file, e);
            std::process::exit(1);
        }
    };

    // Lex
    let mut lexer = Lexer::new(&source);
    let tokens = lexer.tokenize();

    // Parse
    let mut parser = Parser::new(tokens);
    let ast = match parser.parse() {
        Ok(ast) => ast,
        Err(e) => {
            eprintln!("Parse error: {}", e);
            std::process::exit(1);
        }
    };

    // Generate code
    let mut generator = CodeGenerator::new();
    let assembly = generator.generate(ast);

    // Write assembly file
    match fs::write(&output_file, assembly) {
        Ok(_) => println!("Generated assembly: {}", output_file),
        Err(e) => {
            eprintln!("Error writing output file: {}", e);
            std::process::exit(1);
        }
    };

    // Option to compile and link
    if args.len() >= 4 && args[3] == "--compile" {
        let exe_name = input_file.trim_end_matches(".runa");

        // Assemble
        let assemble = Command::new("as")
            .arg(&output_file)
            .arg("-o")
            .arg(format!("{}.o", exe_name))
            .output()
            .expect("Failed to run assembler");

        if !assemble.status.success() {
            eprintln!("Assembly failed");
            std::process::exit(1);
        }

        // Link with libc
        let link = Command::new("gcc")
            .arg(format!("{}.o", exe_name))
            .arg("-o")
            .arg(exe_name)
            .output()
            .expect("Failed to run linker");

        if !link.status.success() {
            eprintln!("Linking failed");
            std::process::exit(1);
        }

        println!("Created executable: {}", exe_name);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_compilation() {
        let code = r#"
Process called "main" returns Integer:
    Let x be 42
    Return x
End Process
"#;
        let mut lexer = Lexer::new(code);
        let tokens = lexer.tokenize();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();
        let mut generator = CodeGenerator::new();
        let asm = generator.generate(ast);
        assert!(asm.contains("main:"));
    }
}