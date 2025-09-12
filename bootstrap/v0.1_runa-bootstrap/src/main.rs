use anyhow::{Context, Result};
use clap::{Arg, ArgMatches, Command};
use std::path::PathBuf;

mod compiler;
mod runtime;
mod utils;

use compiler::CompilerDriver;
use utils::diagnostics::DiagnosticEngine;

fn main() -> Result<()> {
    let matches = create_cli().get_matches();
    let mut diagnostic_engine = DiagnosticEngine::new();
    
    match matches.subcommand() {
        Some(("compile", sub_matches)) => {
            handle_compile_command(sub_matches, &mut diagnostic_engine)
        }
        Some(("check", sub_matches)) => {
            handle_check_command(sub_matches, &mut diagnostic_engine)
        }
        _ => {
            eprintln!("No command specified. Use --help for usage information.");
            std::process::exit(1);
        }
    }
}

fn create_cli() -> Command {
    Command::new("runac")
        .about("Runa Bootstrap Compiler v0.1")
        .version("0.1.0")
        .author("Runa Language Team")
        .subcommand(
            Command::new("compile")
                .about("Compile Runa source code")
                .arg(
                    Arg::new("input")
                        .help("Input Runa source file")
                        .required(true)
                        .value_name("FILE")
                )
                .arg(
                    Arg::new("output")
                        .short('o')
                        .long("output")
                        .help("Output executable path")
                        .value_name("OUTPUT")
                )
                .arg(
                    Arg::new("target")
                        .long("target")
                        .help("Target platform (linux_x64, windows_x64, macos_arm64, etc.)")
                        .value_name("TARGET")
                        .default_value("host")
                )
                .arg(
                    Arg::new("optimize")
                        .short('O')
                        .long("optimize")
                        .help("Optimization level (0-3)")
                        .value_name("LEVEL")
                        .default_value("2")
                )
        )
        .subcommand(
            Command::new("check")
                .about("Check Runa source code for errors without compiling")
                .arg(
                    Arg::new("input")
                        .help("Input Runa source file")
                        .required(true)
                        .value_name("FILE")
                )
        )
}

fn handle_compile_command(matches: &ArgMatches, diagnostic_engine: &mut DiagnosticEngine) -> Result<()> {
    let input_file = PathBuf::from(matches.get_one::<String>("input").unwrap());
    let output_file = matches.get_one::<String>("output")
        .map(PathBuf::from)
        .unwrap_or_else(|| {
            let mut output = input_file.clone();
            output.set_extension("");
            output
        });
    
    let target = matches.get_one::<String>("target").unwrap();
    let optimize_level: u8 = matches.get_one::<String>("optimize")
        .unwrap()
        .parse()
        .context("Invalid optimization level")?;

    let mut compiler = CompilerDriver::new(diagnostic_engine);
    compiler.compile_file(&input_file, &output_file, target, optimize_level)
        .context("Compilation failed")?;

    if diagnostic_engine.has_errors() {
        diagnostic_engine.emit_all();
        std::process::exit(1);
    } else {
        println!("Compilation successful: {}", output_file.display());
        Ok(())
    }
}

fn handle_check_command(matches: &ArgMatches, diagnostic_engine: &mut DiagnosticEngine) -> Result<()> {
    let input_file = PathBuf::from(matches.get_one::<String>("input").unwrap());
    
    let mut compiler = CompilerDriver::new(diagnostic_engine);
    compiler.check_file(&input_file)
        .context("Syntax check failed")?;

    if diagnostic_engine.has_errors() {
        diagnostic_engine.emit_all();
        std::process::exit(1);
    } else {
        println!("No errors found in {}", input_file.display());
        Ok(())
    }
}