use clap::Parser as ClapParser;
use anyhow::{Context, Result};
use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::collections::{HashMap, HashSet};

use runa_bootstrap::{Lexer, Parser, CodeGenerator};
use runa_bootstrap::parser::{Program, Item, ImportStatement};

#[derive(ClapParser, Debug)]
#[clap(name = "runac", version = "0.1.0", about = "Runa Bootstrap Compiler v0.1")]
struct Args {
    /// Input Runa source file
    input: PathBuf,

    /// Output file (default: input.o)
    #[clap(short, long)]
    output: Option<PathBuf>,

    /// Emit assembly instead of object file
    #[clap(short = 's', long)]
    assembly: bool,

    /// Just check syntax without generating code
    #[clap(long)]
    check: bool,

    /// Optimization level (0-3)
    #[clap(short = 'O', long, default_value = "0")]
    optimize: u8,

    /// Verbose output
    #[clap(short, long)]
    verbose: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();

    // Read source file
    let source = fs::read_to_string(&args.input)
        .with_context(|| format!("Failed to read file: {:?}", args.input))?;

    if args.verbose {
        eprintln!("Compiling {:?}...", args.input);
    }

    // Lexical analysis
    let mut lexer = Lexer::new(&source);
    let tokens = lexer.tokenize()
        .with_context(|| "Lexical analysis failed")?;

    if args.verbose {
        eprintln!("Lexer produced {} tokens", tokens.len());
    }

    // Parsing
    let mut parser = Parser::new(tokens);
    let ast = parser.parse()
        .with_context(|| "Parsing failed")?;

    if args.verbose {
        eprintln!("Parser produced AST with {} top-level items", ast.items.len());
    }

    // Resolve imports and create combined AST
    let resolved_ast = resolve_imports(ast, &args.input, args.verbose)
        .with_context(|| "Import resolution failed")?;

    if args.verbose {
        eprintln!("After import resolution: {} total items", resolved_ast.items.len());
    }

    // If just checking, we're done
    if args.check {
        println!("Syntax check passed");
        return Ok(());
    }

    // Code generation
    let output_path = args.output.unwrap_or_else(|| {
        let mut path = args.input.clone();
        path.set_extension(if args.assembly { "s" } else { "o" });
        path
    });

    if args.verbose {
        eprintln!("Creating CodeGenerator...");
    }

    let mut codegen = CodeGenerator::new(
        output_path.to_str().unwrap(),
        args.optimize,
    )?;

    if args.verbose {
        eprintln!("Starting code generation...");
    }

    if args.assembly {
        let asm = codegen.generate_assembly(&resolved_ast)?;
        fs::write(&output_path, asm)
            .with_context(|| format!("Failed to write assembly to {:?}", output_path))?;

        if args.verbose {
            eprintln!("Assembly written to {:?}", output_path);
        }
    } else {
        if args.verbose {
            eprintln!("Generating object file...");
        }
        codegen.generate_object(&resolved_ast, output_path.to_str().unwrap())?;

        if args.verbose {
            eprintln!("Object file written to {:?}", output_path);
        }
    }

    Ok(())
}

/// Resolve imports and create a combined program with all modules
fn resolve_imports(
    main_ast: Program,
    main_file_path: &PathBuf,
    verbose: bool,
) -> Result<Program> {
    let mut resolved_items = Vec::new();
    let mut processed_modules = HashSet::new();
    let mut module_queue = Vec::new();

    // Start with the main module
    module_queue.push((main_ast, main_file_path.clone()));

    while let Some((ast, current_path)) = module_queue.pop() {
        let module_key = current_path.to_string_lossy().to_string();
        if processed_modules.contains(&module_key) {
            continue;
        }
        processed_modules.insert(module_key);

        if verbose {
            eprintln!("Processing module: {:?}", current_path);
        }

        // Process each item in this module
        for item in ast.items {
            match &item {
                Item::Import(import_stmt) => {
                    // Resolve the imported module
                    if let Some(imported_ast) = resolve_single_import(import_stmt, &current_path, verbose)? {
                        module_queue.push(imported_ast);
                    }
                }
                _ => {
                    // Add non-import items to the resolved program
                    resolved_items.push(item);
                }
            }
        }
    }

    Ok(Program {
        items: resolved_items,
    })
}

/// Resolve a single import statement and return the AST and path
fn resolve_single_import(
    import: &ImportStatement,
    current_file: &PathBuf,
    verbose: bool,
) -> Result<Option<(Program, PathBuf)>> {
    // Get the directory containing the current file
    let current_dir = current_file.parent()
        .ok_or_else(|| anyhow::anyhow!("Cannot determine parent directory of {:?}", current_file))?;

    // Construct the imported file path
    let imported_file = current_dir.join(format!("{}.runa", import.module_name));

    if !imported_file.exists() {
        if verbose {
            eprintln!("Warning: Import file not found: {:?}", imported_file);
        }
        return Ok(None);
    }

    if verbose {
        eprintln!("Resolving import: {:?} -> {:?}", import.module_name, imported_file);
    }

    // Read and parse the imported file
    let source = fs::read_to_string(&imported_file)
        .with_context(|| format!("Failed to read imported file: {:?}", imported_file))?;

    let mut lexer = Lexer::new(&source);
    let tokens = lexer.tokenize()
        .with_context(|| format!("Failed to tokenize imported file: {:?}", imported_file))?;

    let mut parser = Parser::new(tokens);
    let ast = parser.parse()
        .with_context(|| format!("Failed to parse imported file: {:?}", imported_file))?;

    Ok(Some((ast, imported_file)))
}