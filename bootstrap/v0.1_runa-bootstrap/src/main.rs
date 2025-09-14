use anyhow::Result;
use clap::Parser;
use std::path::PathBuf;

mod lexer;
mod parser;
mod codegen;
mod types;


#[derive(Parser)]
#[command(name = "runac")]
#[command(about = "Runa Bootstrap Compiler")]
struct Args {
    input: PathBuf,
    
    #[arg(short, long)]
    output: Option<PathBuf>,
}

fn main() -> Result<()> {
    let args = Args::parse();
    
    let output = args.output.unwrap_or_else(|| {
        let mut out = args.input.clone();
        out.set_extension("o");
        out
    });
    
    let source = std::fs::read_to_string(&args.input)?;
    
    let tokens = lexer::tokenize(&source)?;
    let program = parser::parse(tokens)?;
    codegen::compile_to_object(&program, &output)?;
    
    println!("Compiled {} -> {}", args.input.display(), output.display());
    Ok(())
}