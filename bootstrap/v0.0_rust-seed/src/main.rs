use std::env;
use std::fs;
use std::process;
use std::path::Path;
use std::collections::HashSet;

mod lexer;
mod parser;
mod codegen;
mod typechecker;

use lexer::Lexer;
use parser::Parser;
use codegen::CodeGenerator;
use typechecker::TypeChecker;
use parser::AstNode;

fn find_function_calls(ast: &AstNode, calls: &mut HashSet<String>) {
    match ast {
        AstNode::Program(statements) => {
            for stmt in statements {
                find_function_calls(stmt, calls);
            }
        }
        AstNode::FunctionCall { name, arguments } => {
            calls.insert(name.clone());
            for arg in arguments {
                find_function_calls(arg, calls);
            }
        }
        AstNode::BinaryExpression { left, right, .. } => {
            find_function_calls(left, calls);
            find_function_calls(right, calls);
        }
        AstNode::LetStatement { value, .. } => {
            find_function_calls(value, calls);
        }
        AstNode::SetStatement { value, .. } => {
            find_function_calls(value, calls);
        }
        AstNode::DisplayStatement { value } => {
            find_function_calls(value, calls);
        }
        AstNode::ReturnStatement { value: Some(value) } => {
            find_function_calls(value, calls);
        }
        AstNode::IfStatement { condition, then_block, else_block } => {
            find_function_calls(condition, calls);
            for stmt in then_block {
                find_function_calls(stmt, calls);
            }
            if let Some(else_stmts) = else_block {
                for stmt in else_stmts {
                    find_function_calls(stmt, calls);
                }
            }
        }
        AstNode::WhileStatement { condition, body } => {
            find_function_calls(condition, calls);
            for stmt in body {
                find_function_calls(stmt, calls);
            }
        }
        AstNode::ProcessDefinition { body, .. } => {
            for stmt in body {
                find_function_calls(stmt, calls);
            }
        }
        _ => {} // Other nodes don't contain function calls
    }
}

fn find_defined_functions(ast: &AstNode, functions: &mut HashSet<String>) {
    match ast {
        AstNode::Program(statements) => {
            for stmt in statements {
                find_defined_functions(stmt, functions);
            }
        }
        AstNode::ProcessDefinition { name, .. } => {
            functions.insert(name.clone());
        }
        _ => {} // Other nodes don't define functions
    }
}

fn compile_with_dependencies(input_file: &str, output_file: &str) -> Result<(), String> {
    let main_source = fs::read_to_string(input_file)
        .map_err(|e| format!("Error reading file {}: {}", input_file, e))?;

    // Parse main file to find function calls
    let mut lexer = Lexer::new(&main_source);
    let tokens = lexer.tokenize()
        .map_err(|e| format!("Lexer error in {}: {}", input_file, e))?;

    let mut parser = Parser::new(tokens);
    let main_ast = parser.parse()
        .map_err(|e| format!("Parser error in {}: {}", input_file, e))?;

    // Find all function calls and definitions in main file
    let mut called_functions = HashSet::new();
    let mut defined_functions = HashSet::new();

    find_function_calls(&main_ast, &mut called_functions);
    find_defined_functions(&main_ast, &mut defined_functions);

    // Find missing functions that need to be imported
    let missing_functions: Vec<String> = called_functions
        .difference(&defined_functions)
        .cloned()
        .collect();

    println!("Missing functions: {:?}", missing_functions);

    if missing_functions.is_empty() {
        // No dependencies, compile normally
        compile_single_file(input_file, output_file)
    } else {
        // Find dependency files
        let input_dir = Path::new(input_file).parent().unwrap_or(Path::new("."));
        let mut dependency_asts = Vec::new();
        let mut all_asts = vec![main_ast];

        for entry in fs::read_dir(input_dir).map_err(|e| format!("Error reading directory: {}", e))? {
            let entry = entry.map_err(|e| format!("Error reading directory entry: {}", e))?;
            let path = entry.path();

            if path.extension().and_then(|s| s.to_str()) == Some("runa") && path != Path::new(input_file) {
                let dep_source = fs::read_to_string(&path)
                    .map_err(|e| format!("Error reading dependency {}: {}", path.display(), e))?;

                let mut dep_lexer = Lexer::new(&dep_source);
                let dep_tokens = dep_lexer.tokenize()
                    .map_err(|e| format!("Lexer error in {}: {}", path.display(), e))?;

                let mut dep_parser = Parser::new(dep_tokens);
                let dep_ast = dep_parser.parse()
                    .map_err(|e| format!("Parser error in {}: {}", path.display(), e))?;

                dependency_asts.push(dep_ast);
            }
        }

        // Combine all ASTs into one program, avoiding duplicate function definitions
        all_asts.extend(dependency_asts);
        let mut combined_statements = Vec::new();
        let mut seen_functions = HashSet::new();

        for ast in all_asts {
            match ast {
                AstNode::Program(statements) => {
                    for stmt in statements {
                        match &stmt {
                            AstNode::ProcessDefinition { name, .. } => {
                                if !seen_functions.contains(name) {
                                    seen_functions.insert(name.clone());
                                    combined_statements.push(stmt);
                                }
                            }
                            _ => {
                                combined_statements.push(stmt);
                            }
                        }
                    }
                }
                other => combined_statements.push(other),
            }
        }

        let combined_ast = AstNode::Program(combined_statements);

        // Type check combined AST
        let mut typechecker = TypeChecker::new();
        typechecker.check(&combined_ast)
            .map_err(|e| format!("Type error: {}", e))?;

        // Generate code for combined AST
        let mut codegen = CodeGenerator::new();
        let assembly = codegen.generate(&combined_ast)
            .map_err(|e| format!("Code generation error: {}", e))?;

        // Write and assemble
        write_and_assemble(&assembly, output_file)
    }
}

fn compile_single_file(input_file: &str, output_file: &str) -> Result<(), String> {
    let source = fs::read_to_string(input_file)
        .map_err(|e| format!("Error reading file {}: {}", input_file, e))?;

    let mut lexer = Lexer::new(&source);
    let tokens = lexer.tokenize()
        .map_err(|e| format!("Lexer error: {}", e))?;

    let mut parser = Parser::new(tokens);
    let ast = parser.parse()
        .map_err(|e| format!("Parser error: {}", e))?;

    let mut typechecker = TypeChecker::new();
    typechecker.check(&ast)
        .map_err(|e| format!("Type error: {}", e))?;

    let mut codegen = CodeGenerator::new();
    let assembly = codegen.generate(&ast)
        .map_err(|e| format!("Code generation error: {}", e))?;

    write_and_assemble(&assembly, output_file)
}

fn write_and_assemble(assembly: &str, output_file: &str) -> Result<(), String> {
    let asm_file = format!("{}.s", output_file);
    fs::write(&asm_file, assembly)
        .map_err(|e| format!("Error writing assembly file: {}", e))?;

    // Path to the v0.1 runtime library
    let runtime_lib_path = "../v0.1_microruna-compiler/runtime/libruna_runtime.a";

    // Check if runtime library exists
    if !Path::new(runtime_lib_path).exists() {
        return Err(format!("Runtime library not found at {}", runtime_lib_path));
    }

    let status = process::Command::new("gcc")
        .args(&[
            "-o", output_file,      // Output executable
            &asm_file,              // Assembly file
            runtime_lib_path,       // Runtime library
            "-static",              // Static linking for self-contained executable
        ])
        .status()
        .map_err(|e| format!("Error invoking gcc: {}", e))?;

    if status.success() {
        println!("Successfully compiled to {} (with v0.1 runtime)", output_file);
        Ok(())
    } else {
        Err("Assembly/linking failed".to_string())
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <input.runa> <output>", args[0]);
        process::exit(1);
    }

    let input_file = &args[1];
    let output_file = &args[2];

    // Debug mode: print tokens
    if output_file == "debug" {
        let source = match fs::read_to_string(input_file) {
            Ok(content) => content,
            Err(err) => {
                eprintln!("Error reading file {}: {}", input_file, err);
                process::exit(1);
            }
        };

        let mut lexer = Lexer::new(&source);
        let tokens = match lexer.tokenize() {
            Ok(tokens) => tokens,
            Err(err) => {
                eprintln!("Lexer error: {}", err);
                process::exit(1);
            }
        };

        for token in &tokens {
            println!("{:?}", token);
        }
        process::exit(0);
    }

    // Compile with dependency resolution
    if let Err(err) = compile_with_dependencies(input_file, output_file) {
        eprintln!("{}", err);
        process::exit(1);
    }
}
